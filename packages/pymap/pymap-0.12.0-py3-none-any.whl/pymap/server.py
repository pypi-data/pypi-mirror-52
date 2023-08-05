"""Defines socket interaction, accepting connections and handling a basic
command/response flow.

"""

import asyncio
import binascii
import re
import sys
from asyncio import shield, IncompleteReadError, StreamReader, StreamWriter, \
    CancelledError
from base64 import b64encode, b64decode
from ssl import SSLContext
from typing import TypeVar, Iterable, List, Optional, Awaitable

from pysasl import ServerChallenge, AuthenticationError, \
    AuthenticationCredentials

from .concurrent import Event
from .config import IMAPConfig
from .context import subsystem, current_command, socket_info
from .exceptions import ResponseError
from .interfaces.session import LoginProtocol
from .parsing.command import Command
from .parsing.commands import Commands
from .parsing.command.nonauth import AuthenticateCommand, StartTLSCommand
from .parsing.command.select import IdleCommand
from .parsing.exceptions import RequiresContinuation
from .parsing.response import ResponseContinuation, Response, ResponseCode, \
    ResponseBad, ResponseNo, ResponseBye, ResponseOk
from .sockinfo import SocketInfo
from .state import ConnectionState

__all__ = ['IMAPServer', 'IMAPConnection']

_Ret = TypeVar('_Ret')


class Disconnected(Exception):
    """Thrown if the remote socket closes when the server expected input."""
    pass


class IMAPServer:
    """Callable object that creates and runs :class:`IMAPConnection` objects
    when :func:`asyncio.start_server` receives a new connection.

    Args:
        login: Login callback that takes authentication credentials and
            returns a :class:`~pymap.interfaces.session.SessionInterface`
            object.
        config: Settings to use for the IMAP server.

    """

    __slots__ = ['commands', '_login', '_config']

    def __init__(self, login: LoginProtocol, config: IMAPConfig) -> None:
        super().__init__()
        self.commands = config.commands
        self._login = login
        self._config = config

    @property
    def login(self) -> LoginProtocol:
        return self._login

    @property
    def config(self) -> IMAPConfig:
        return self._config

    async def __call__(self, reader: StreamReader,
                       writer: StreamWriter) -> None:
        conn = IMAPConnection(self.commands, self.config, reader, writer)
        state = ConnectionState(self._login, self._config)
        try:
            await conn.run(state)
        finally:
            writer.close()


class IMAPConnection:
    """Runs a single IMAP connection from start to finish.

    Args:
        commands: Defines the IMAP commands available to the connection.
        config: Settings to use for the IMAP connection.
        reader: The input stream for the socket.
        writer: The output stream for the socket.

    """

    _lines = re.compile(br'\r?\n')
    _literal_plus = re.compile(br'{(\d+)\+}\r?\n$')

    __slots__ = ['commands', 'config', 'params', 'bad_command_limit',
                 '_print', 'reader', 'writer']

    def __init__(self, commands: Commands, config: IMAPConfig,
                 reader: StreamReader,
                 writer: StreamWriter) -> None:
        super().__init__()
        self.commands = commands
        self.config = config
        self.params = config.parsing_params
        self.bad_command_limit = config.bad_command_limit
        self._print = self._real_print if config.debug else self._noop_print
        self._reset_streams(reader, writer)

    def _reset_streams(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer
        socket_info.set(SocketInfo(writer))

    @classmethod
    def _real_print(cls, prefix: str, output: bytes) -> None:
        prefix = prefix % socket_info.get().socket.fileno()
        lines = cls._lines.split(output)
        if not lines[-1]:
            lines = lines[:-1]
        for line in lines:
            line_str = str(line, 'utf-8', 'replace')
            print(prefix, line_str)

    @classmethod
    def _noop_print(cls, prefix: str, output: bytes) -> None:
        pass

    def _exec(self, future: Awaitable[_Ret]) -> Awaitable[_Ret]:
        return subsystem.get().execute(future)

    async def readline(self) -> memoryview:
        buf = bytearray(await self.reader.readline())
        while True:
            if buf.endswith(b'+}\n') or buf.endswith(b'+}\r\n'):
                lit_plus = self._literal_plus.search(buf)
            else:
                lit_plus = None
            if lit_plus:
                literal_length = int(lit_plus.group(1))
                try:
                    buf += await self.reader.readexactly(literal_length)
                except IncompleteReadError:
                    raise Disconnected
                buf += await self.reader.readline()
            else:
                self._print('%d -->|', buf)
                return memoryview(buf)

    async def read_continuation(self, literal_length: int) -> memoryview:
        try:
            extra_literal = await self.reader.readexactly(literal_length)
        except IncompleteReadError:
            raise Disconnected
        self._print('%d -->|', extra_literal)
        extra_line = await self.readline()
        extra = extra_literal + bytes(extra_line)
        return memoryview(extra)

    async def authenticate(self, state: ConnectionState, mech_name: bytes) \
            -> Optional[AuthenticationCredentials]:
        mech = state.auth.get_server(mech_name)
        if not mech:
            return None
        responses: List[ServerChallenge] = []
        while True:
            try:
                return mech.server_attempt(responses)
            except ServerChallenge as chal:
                chal_bytes = b64encode(chal.get_challenge())
                cont = ResponseContinuation(chal_bytes)
                await self.write_response(cont)
                resp_bytes = bytes(await self.read_continuation(0))
                try:
                    chal.set_response(b64decode(resp_bytes))
                except binascii.Error as exc:
                    raise AuthenticationError(exc)
                if resp_bytes.rstrip(b'\r\n') == b'*':
                    raise AuthenticationError('Authentication canceled.')
                responses.append(chal)

    async def read_command(self) -> Command:
        line = await self.readline()
        conts: List[memoryview] = []
        while True:
            if self.reader.at_eof():
                raise Disconnected
            try:
                cmd, _ = self.commands.parse(
                    line, self.params.copy(continuations=conts.copy()))
            except RequiresContinuation as req:
                cont = ResponseContinuation(req.message)
                await self.write_response(cont)
                ret = await self.read_continuation(req.literal_length)
                conts.append(ret)
            else:
                return cmd

    async def read_idle_done(self, cmd: IdleCommand) -> bool:
        buf = await self.read_continuation(0)
        ok, _ = cmd.parse_done(buf)
        return ok

    async def write_response(self, resp: Response) -> None:
        raw = bytes(resp)
        resp.write(self.writer)
        await self.writer.drain()
        self._print('%d <--|', raw)

    async def start_tls(self, ssl_context: SSLContext) -> None:
        loop = asyncio.get_event_loop()
        transport = self.writer.transport
        protocol = transport.get_protocol()  # type: ignore
        new_transport = await loop.start_tls(  # type: ignore
            transport, protocol, ssl_context, server_side=True)
        protocol._stream_reader = StreamReader(loop=loop)
        protocol._client_connected_cb = self._reset_streams
        protocol.connection_made(new_transport)
        self._print('%d <->|', b'<TLS handshake>')

    async def send_error_disconnect(self) -> None:
        exc_type, exc, exc_tb = sys.exc_info()
        if isinstance(exc, CancelledError):
            resp = ResponseBye(b'Server has closed the connection.',
                               ResponseCode.of(b'UNAVAILABLE'))
        else:
            resp = ResponseBye(b'Unhandled server error.',
                               ResponseCode.of(b'SERVERBUG'))
        try:
            await self.write_response(resp)
        except IOError:
            pass

    async def write_updates(self, untagged: Iterable[Response]) -> None:
        for i, resp in enumerate(untagged):
            await self.write_response(resp)

    async def handle_updates(self, state: ConnectionState, done: Event,
                             cmd: IdleCommand) -> None:
        timeout = self.config.max_idle_wait
        while not done.is_set():
            receive_task = asyncio.create_task(
                self._exec(state.receive_updates(cmd, done)))
            try:
                untagged = await asyncio.wait_for(receive_task, timeout)
            except TimeoutError:
                pass
            else:
                await shield(self.write_updates(untagged))

    async def idle(self, state: ConnectionState, cmd: IdleCommand) -> Response:
        response = await self._exec(state.do_command(cmd))
        if not isinstance(response, ResponseOk):
            return response
        await self.write_response(ResponseContinuation(b'Idling.'))
        done = subsystem.get().new_event()
        updates_task = asyncio.create_task(
            self.handle_updates(state, done, cmd))
        done_task = asyncio.create_task(self.read_idle_done(cmd))
        updates_exc: Optional[Exception] = None
        done_exc: Optional[Exception] = None
        try:
            ok = await done_task
        except Exception as exc:
            done_exc = exc
        finally:
            done.set()
        try:
            await updates_task
        except Exception as exc:
            updates_exc = exc
        if updates_exc:
            raise updates_exc
        elif done_exc:
            raise done_exc
        elif not ok:
            return ResponseBad(cmd.tag, b'Expected "DONE".')
        else:
            return response

    async def run(self, state: ConnectionState) -> None:
        """Start the socket communication with the IMAP greeting, and then
        enter the command/response cycle.

        Args:
            state: Defines the interaction with the backend plugin.

        """
        self._print('%d +++|', bytes(socket_info.get()))
        bad_commands = 0
        try:
            greeting = await self._exec(state.do_greeting())
        except ResponseError as exc:
            resp = exc.get_response(b'*')
            resp.condition = ResponseBye.condition
            await self.write_response(resp)
            return
        else:
            await self.write_response(greeting)
        while True:
            try:
                cmd = await self.read_command()
            except (ConnectionResetError, BrokenPipeError):
                break
            except Disconnected:
                break
            except CancelledError:
                await self.send_error_disconnect()
                break
            except Exception:
                await self.send_error_disconnect()
                raise
            else:
                prev_cmd = current_command.set(cmd)
                try:
                    if isinstance(cmd, AuthenticateCommand):
                        creds = await self.authenticate(state, cmd.mech_name)
                        response, _ = await self._exec(
                            state.do_authenticate(cmd, creds))
                    elif isinstance(cmd, IdleCommand):
                        response = await self.idle(state, cmd)
                    else:
                        response = await self._exec(state.do_command(cmd))
                except ResponseError as exc:
                    resp = exc.get_response(cmd.tag)
                    await self.write_response(resp)
                    if resp.is_terminal:
                        break
                except AuthenticationError as exc:
                    msg = bytes(str(exc), 'utf-8', 'surrogateescape')
                    resp = ResponseBad(cmd.tag, msg)
                    await self.write_response(resp)
                except TimeoutError:
                    resp = ResponseNo(cmd.tag, b'Operation timed out.',
                                      ResponseCode.of(b'TIMEOUT'))
                    await self.write_response(resp)
                except CancelledError:
                    await self.send_error_disconnect()
                    break
                except Exception:
                    await self.send_error_disconnect()
                    raise
                else:
                    await self.write_response(response)
                    if response.is_bad:
                        bad_commands += 1
                        if self.bad_command_limit \
                                and bad_commands >= self.bad_command_limit:
                            msg = b'Too many errors, disconnecting.'
                            response.add_untagged(ResponseBye(msg))
                    else:
                        bad_commands = 0
                    if response.is_terminal:
                        break
                    if isinstance(cmd, StartTLSCommand) and state.ssl_context \
                            and isinstance(response, ResponseOk):
                        await self.start_tls(state.ssl_context)
                finally:
                    current_command.reset(prev_cmd)
        self._print('%d ---|', b'<disconnected>')
