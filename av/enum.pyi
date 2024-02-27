from typing import Literal, Sequence, overload

class EnumType(type):
    def __init__(self, name, bases, attrs, items): ...
    def _create(self, name: str, value: int, doc=None, by_value_only=False): ...
    def __len__(self): ...
    def __iter__(self): ...
    def __getitem__(self, key): ...
    def _get(self, value: int, create: bool = False): ...
    def _get_multi_flags(self, value: int): ...
    def get(
        self, key, default: int | None = None, create: bool = False
    ) -> int | None: ...

class EnumItem:
    name: str
    value: int

    def __int__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __reduce__(self): ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...

class EnumFlag(EnumItem):
    flags: tuple[EnumFlag]

    def __and__(self, other): ...
    def __or__(self, other): ...
    def __xor__(self, other): ...
    def __invert__(self): ...
    def __nonzero__(self) -> bool: ...

@overload
def define_enum(
    name: str,
    module: str,
    items: Sequence[tuple[str, int] | None],
    is_flags: Literal[True],
) -> EnumFlag: ...
@overload
def define_enum(
    name: str,
    module: str,
    items: Sequence[tuple[str, int] | None],
    is_flags: Literal[False],
) -> EnumItem: ...
@overload
def define_enum(
    name: str,
    module: str,
    items: Sequence[tuple[str, int] | None],
    is_flags: bool = False,
) -> EnumItem | EnumFlag: ...
