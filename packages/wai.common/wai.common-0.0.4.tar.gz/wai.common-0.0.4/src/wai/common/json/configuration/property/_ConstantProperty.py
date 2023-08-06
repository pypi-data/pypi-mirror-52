from ..._typing import RawJSONPrimitive
from .._OptionallyPresent import OptionallyPresent
from ._Property import Property
from ...schema import constant


class ConstantProperty(Property[RawJSONPrimitive]):
    """
    Configuration property which validates a constant primitive value.
    """
    def __init__(self,
                 name: str,
                 value: RawJSONPrimitive,
                 *,
                 optional: bool = False):
        super().__init__(
            name,
            constant(value),
            optional=optional
        )

    def get_as_raw_json(self, instance) -> OptionallyPresent[RawJSONPrimitive]:
        return super().get_as_raw_json(instance)

    def set_from_raw_json(self, instance, value: OptionallyPresent[RawJSONPrimitive]):
        super().set_from_raw_json(instance, value)
