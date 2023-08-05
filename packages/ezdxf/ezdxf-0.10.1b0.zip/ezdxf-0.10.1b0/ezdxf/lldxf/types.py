# Created: 30.04.2014
# Copyright (c) 2014-2018, Manfred Moitzi
# License: MIT License
"""

DXF Types
=========

Required DXF tag interface:

    - property :attr:`code`: group code as int
    - property :attr:`value`: tag value of unspecific type
    - :meth:`dxfstr`: returns the DXF string
    - :meth:`clone`: returns a deep copy of tag

"""
from typing import Union, Tuple, Iterable, Callable, Sequence, Any, TYPE_CHECKING
from array import array
from itertools import chain
import reprlib
from ezdxf.math.vector import Vector

from ezdxf.tools.binarydata import hexstr_to_bytes, int_to_hexstr

if TYPE_CHECKING:
    from ezdxf.eztypes import TagValue

TAG_STRING_FORMAT = '%3d\n%s\n'
POINT_CODES = {10, 11, 12, 13, 14, 15, 16, 17, 18, 110, 111, 112, 210, 211, 212, 213, 1010, 1011, 1012, 1013}

GENERAL_MARKER = 0
SUBCLASS_MARKER = 100
XDATA_MARKER = 1001
EMBEDDED_OBJ_MARKER = 101
APP_DATA_MARKER = 102
EXT_DATA_MARKER = 1001
GROUP_MARKERS = {GENERAL_MARKER, SUBCLASS_MARKER, EMBEDDED_OBJ_MARKER, APP_DATA_MARKER, EXT_DATA_MARKER}
BINARY_FLAGS = {70, 90}
HANDLE_CODES = {5, 105}
POINTER_CODES = set(chain(range(320, 370), range(390, 400), (480, 481, 1005)))
HEX_HANDLE_CODES = set(chain(HANDLE_CODES, POINTER_CODES))
BINARAY_DATA = {310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 1004}
EMBEDDED_OBJ_STR = 'Embedded Object'


def handle_code(dxftype: str) -> int:
    return 105 if dxftype == 'DIMSTYLE' else 5


class DXFTag:
    """
    Immutable DXFTag class - immutable by design, not implementation - don't change it.

    Args:
        code: group code as int
        value: tag value, type depends on group code

    :ivar code: group code as int (do not change)
    :ivar value: tag value (read-only property)

    """
    __slots__ = ('code', '_value')

    def __init__(self, code: int, value: 'TagValue'):
        self.code = code  # type: int
        self._value = value  # type: TagValue

    def __str__(self) -> str:
        """ Returns content string ``'(code, value)'``. """
        return str((self.code, self.value))

    def __repr__(self) -> str:
        """ Returns representation string ``'DXFTag(code, value)'``. """
        return "DXFTag{}".format(str(self))

    @property
    def value(self) -> 'TagValue':
        return self._value

    def __getitem__(self, index: int):
        """ Returns :attr:`code` for index ``0`` and :attr:`value` for index ``1``, emulates a tuple."""
        return (self.code, self.value)[index]

    def __iter__(self) -> Iterable:
        """ Returns (code, value) tuples. """
        yield self.code
        yield self.value

    def __eq__(self, other) -> bool:
        """ ``True`` if `other` and `self` has same content for :attr:`code` and :attr:`value`. """
        return (self.code, self.value) == other

    def __hash__(self):
        """ Hash support, :class:`DXFTag` can be used in sets and as dict key. """
        return hash((self.code, self._value))

    def dxfstr(self) -> str:
        """ Returns the DXF string e.g. ``'  0\\nLINE\\n'`` """
        return TAG_STRING_FORMAT % (self.code, self._value)

    def clone(self) -> 'DXFTag':
        """ Returns a clone of itself, this method is necessary for the more complex (and not immutable) DXF tag types. """
        return self  # immutable tags


# Special marker tag
NONE_TAG = DXFTag(None, None)  # type: ignore


def uniform_appid(appid: str) -> str:
    if appid[0] == '{':
        return appid
    else:
        return '{' + appid


def is_app_data_marker(tag: DXFTag) -> bool:
    return tag.code == APP_DATA_MARKER and tag.value.startswith('{')


def is_embedded_object_marker(tag: DXFTag) -> bool:
    return tag.code == EMBEDDED_OBJ_MARKER and tag.value == EMBEDDED_OBJ_STR


class DXFVertex(DXFTag):
    """
    Represents a 2D or 3D vertex, stores only the group code of the x-component of the vertex, because the
    y-group-code is x-group-code + 10 and z-group-code id x-group-code+20, this is a rule that ALWAYS applies.
    This tag is `immutable` by design, not by implementation.

    Args:
        code: group code of x-component
        value: sequence of x, y and optional z values

    """
    __slots__ = ()

    def __init__(self, code: int, value: Sequence[float]):
        super(DXFVertex, self).__init__(code, array('d', value))  # type: ignore # array is like a tuple

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return "DXFVertex({}, {})".format(self.code, str(self))

    def __hash__(self):
        x, y, *z = self._value
        z = 0. if len(z) == 0 else z[0]
        return hash((self.code, x, y, z))

    @property
    def value(self) -> Tuple:
        return tuple(self._value)

    def dxftags(self) -> Iterable[Tuple]:
        """ Returns all vertex components as single :class:`DXFTag` objects. """
        c = self.code
        return ((code, value) for code, value in zip((c, c + 10, c + 20), self.value))

    def dxfstr(self) -> str:
        """ Returns the DXF string for all vertex components. """
        return ''.join(TAG_STRING_FORMAT % tag for tag in self.dxftags())


class DXFBinaryTag(DXFTag):
    """ Immutable BinaryTags class - immutable by design, not by implementation - don't change it. """
    __slots__ = ()

    def __str__(self) -> str:
        return "({}, {})".format(self.code, self.tostring())

    def __repr__(self) -> str:
        return "DXFBinaryTag({}, {})".format(self.code, reprlib.repr(self.tostring()))

    def tostring(self) -> str:  # value to string
        """ Returns binary value as single hex-string. """
        return ''.join(int_to_hexstr(b) for b in self.value)

    def dxfstr(self) -> str:
        """ Returns the DXF string for all vertex components. """
        return TAG_STRING_FORMAT % (self.code, self.tostring())

    @classmethod
    def from_string(cls, code: int, value: str):
        return cls(code, hexstr_to_bytes(value))


def dxftag(code: int, value: 'TagValue') -> DXFTag:
    """
    DXF tag factory function.

    Args:
        code: group code
        value: tag value

    Returns: :class:`DXFTag` or inherited

    """
    if code in BINARAY_DATA:
        return DXFBinaryTag(code, value)
    elif code in POINT_CODES:
        return DXFVertex(code, value)
    else:
        return DXFTag(code, cast_tag_value(code, value))


def tuples_to_tags(iterable: Iterable[Tuple[int, 'TagValue']]) -> Iterable[DXFTag]:
    """ Returns an iterable if :class: `DXFTag` or inherited, accepts an iterable of (code, value) tuples as input. """
    for code, value in iterable:
        if code in POINT_CODES:
            yield DXFVertex(code, value)
        elif code in BINARAY_DATA:
            yield DXFBinaryTag.from_string(code, value)
        else:
            yield DXFTag(code, value)


def _build_type_table(types):
    table = {}
    for caster, codes in types:
        for code in codes:
            table[code] = caster
    return table


TYPE_TABLE = _build_type_table([
    # all group code < 0 are spacial tags for internal use, but not accessible by get_dxf_attrib()
    (float, range(10, 60)),
    (int, range(60, 100)),
    (float, range(110, 150)),
    (int, range(160, 170)),
    (int, range(170, 180)),
    (float, range(210, 240)),
    (int, range(270, 290)),
    (int, range(290, 300)),  # bool 1=True 0=False
    (int, range(370, 390)),
    (int, range(400, 410)),
    (int, range(420, 430)),
    (int, range(440, 460)),
    (float, range(460, 470)),
    (float, range(1010, 1060)),
    (int, range(1060, 1072)),
])


def is_binary_data(code: int) -> bool:
    return code in BINARAY_DATA


def is_pointer_code(code: int) -> bool:
    return code in POINTER_CODES


def is_point_code(code: int) -> bool:
    return code in POINT_CODES


def is_point_tag(tag: Tuple) -> bool:
    return tag[0] in POINT_CODES


def cast_tag_value(code: int, value: 'TagValue') -> 'TagValue':
    return TYPE_TABLE.get(code, str)(value)


def tag_type(code: int) -> Callable:
    return TYPE_TABLE.get(code, str)


def strtag(tag: Union[DXFTag, Tuple[int, Any]]) -> str:
    return TAG_STRING_FORMAT % tuple(tag)


def get_xcode_for(code) -> int:
    if code in HEX_HANDLE_CODES:
        return 1005
    if code in BINARAY_DATA:
        return 1004
    type_ = TYPE_TABLE.get(code, str)
    if type_ is int:
        return 1070
    if type_ is float:
        return 1040
    return 1000


def cast_value(code: int, value):
    if value is not None:
        if code in POINT_CODES:  # cast vertices to Vector()
            return Vector(value)
        return TYPE_TABLE.get(code, str)(value)
    else:
        return None
