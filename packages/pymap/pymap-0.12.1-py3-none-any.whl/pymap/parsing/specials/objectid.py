
from __future__ import annotations

import random as _random
from typing import Optional, Tuple, AnyStr

from .. import Params, Parseable
from ..exceptions import NotParseable
from ...bytes import rev

__all__ = ['ObjectId']


class ObjectId(Parseable[bytes]):
    """Represents an object ID, used to identify a mailbox, message, or thread.

    An *object_id* value of ``None`` is a special case indicating that this
    object ID is not defined.

    Args:
        object_id: The object ID bytestring, or ``None``.

    See Also:
        `RFC 8474 <https://tools.ietf.org/html/rfc8474>`_

    """

    _pattern = rev.compile(br'[a-zA-Z0-9_-]{1,255}')

    def __init__(self, object_id: Optional[bytes]) -> None:
        super().__init__()
        if object_id == b'':
            raise ValueError(object_id)
        self.object_id = object_id

    @property
    def value(self) -> bytes:
        """The object ID value."""
        if self.object_id is None:
            raise ValueError(self.object_id)
        return self.object_id

    @property
    def parens(self) -> bytes:
        """The object ID value surrounded by parentheses."""
        return b'(%b)' % (self.value, )

    @classmethod
    def parse(cls, buf: memoryview, params: Params) \
            -> Tuple[ObjectId, memoryview]:
        start = cls._whitespace_length(buf)
        match = cls._pattern.match(buf, start)
        if not match:
            raise NotParseable(buf)
        return cls(match.group(0)), buf[match.end(0):]

    @classmethod
    def _random(cls, prefix: bytes) -> ObjectId:
        return cls(b'%b%032x' % (prefix, _random.getrandbits(128)))

    @classmethod
    def random_mailbox_id(cls) -> ObjectId:
        """Return a new randomized mailbox ID."""
        return cls._random(b'F')

    @classmethod
    def random_email_id(cls) -> ObjectId:
        """Return a new randomized email ID."""
        return cls._random(b'M')

    @classmethod
    def random_thread_id(cls) -> ObjectId:
        """Return a new randomized thread ID."""
        return cls._random(b'T')

    @classmethod
    def maybe(cls, value: Optional[AnyStr]) -> ObjectId:
        """Return an object ID representing the string or bytestring value. If
        the input is empty or ``None``, the object ID returned will have
        :attr:`.not_defined` be true.

        Args:
            value: The object ID string or bytestring.

        """
        if not value:
            return cls(None)
        elif isinstance(value, str):
            return cls(value.encode('ascii', 'ignore'))
        else:
            return cls(value)

    def __eq__(self, other) -> bool:
        if isinstance(other, ObjectId):
            return self.object_id == other.object_id
        elif isinstance(other, bytes):
            return self.object_id == other
        return super().__eq__(other)

    def __hash__(self) -> int:
        return hash(self.object_id)

    def __str__(self) -> str:
        try:
            return self.parens.decode('ascii')
        except ValueError:
            return 'NIL'

    def __repr__(self) -> str:
        return '<ObjectId {0!s}>'.format(self)

    def __bytes__(self) -> bytes:
        return self.value
