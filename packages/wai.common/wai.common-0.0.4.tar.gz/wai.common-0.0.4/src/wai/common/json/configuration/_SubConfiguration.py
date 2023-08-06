from typing import Type, TypeVar

from .property import ProxyProperty
from ._Configuration import Configuration

T = TypeVar("T", bound=Configuration)


class SubConfiguration(ProxyProperty[T]):
    """
    Property which validates a sub-configuration (essentially an object).
    """
    def __init__(self,
                 name: str,
                 configuration_type: Type[T],
                 *,
                 optional: bool = False):
        super().__init__(
            name,
            configuration_type,
            optional=optional
        )
