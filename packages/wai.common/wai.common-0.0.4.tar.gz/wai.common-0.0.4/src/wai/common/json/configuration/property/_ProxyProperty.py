from abc import ABC
from typing import Type, TypeVar

from ..._typing import RawJSONElement
from .._OptionallyPresent import OptionallyPresent
from .._Absent import Absent
from ...schema import TRIVIALLY_SUCCEED_SCHEMA
from ...serialise import JSONBiserialisable
from ._Property import Property

InternalType = TypeVar("InternalType", bound=JSONBiserialisable)


class ProxyProperty(Property[InternalType], ABC):
    """
    Property which takes values of a type that is serialisable
    to/from JSON.
    """
    def __init__(self,
                 name: str,
                 type: Type[InternalType],
                 *,
                 optional: bool = False):
        super().__init__(
            name,
            TRIVIALLY_SUCCEED_SCHEMA,  # Schema is not used for proxy properties
            optional=optional
        )

        self.__type: Type[InternalType] = type

    def type(self) -> Type[InternalType]:
        """
        Gets the type of this proxy-property.
        """
        return self.__type

    def get_as_raw_json(self, instance) -> OptionallyPresent[RawJSONElement]:
        # Get the proxy value
        value = self.__get__(instance, None)

        # If not absent, serialise it
        return value.to_raw_json() if isinstance(value, JSONBiserialisable) else value

    def set_from_raw_json(self, instance, value: OptionallyPresent[RawJSONElement]):
        # Serialise the value
        self.__set__(instance, self.__type.from_raw_json(value) if value is not Absent else Absent)

    def validate_value(self, value: InternalType):
        # Must be an instance of the correct type
        if not isinstance(value, self.__type):
            raise AttributeError(f"{value} is not an instance of {self.__type.__name__}")
