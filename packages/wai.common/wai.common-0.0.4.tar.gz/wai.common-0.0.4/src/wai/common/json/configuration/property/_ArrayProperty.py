from typing import Optional, Type, Union, List, TypeVar, Generic

from .._OptionallyPresent import OptionallyPresent
from ._Property import Property
from ._ProxyProperty import ProxyProperty
from ._ArrayProxy import ArrayProxy

ElementType = TypeVar("ElementType")


class ArrayProperty(ProxyProperty[ArrayProxy], Generic[ElementType]):
    """
    Property which validates a regular array of elements.
    """
    def __init__(self,
                 sub_property: Property[ElementType],
                 min_elements: int = 0,
                 max_elements: Optional[int] = None,
                 unique_elements: bool = False):

        # Create a closure class to proxy the array
        class ClosureArrayProxy(ArrayProxy[ElementType]):
            @classmethod
            def sub_property(cls) -> Property[ElementType]:
                return sub_property

            @classmethod
            def min_elements(cls) -> int:
                return min_elements

            @classmethod
            def max_elements(cls) -> Optional[int]:
                return max_elements

            @classmethod
            def unique_elements(cls) -> bool:
                return unique_elements

        super().__init__(
            sub_property.name(),
            ClosureArrayProxy,
            optional=sub_property.is_optional()
        )

        self.__proxy: Type[ArrayProxy[ElementType]] = ClosureArrayProxy

    def __set__(self, instance, value: OptionallyPresent[Union[ArrayProxy[ElementType], List[ElementType]]]):
        # Convert raw lists to proxies
        if isinstance(value, list):
            value = self.__proxy(value)

        super().__set__(instance, value)
