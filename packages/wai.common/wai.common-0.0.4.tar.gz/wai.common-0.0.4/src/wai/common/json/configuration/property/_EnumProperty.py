from .._OptionallyPresent import OptionallyPresent
from ..._typing import RawJSONPrimitive
from ...schema import enum
from ._Property import Property


class EnumProperty(Property[RawJSONPrimitive]):
    """
    Property which accepts one of a set of specific primitive values.
    """
    def __init__(self,
                 name: str,
                 *values: RawJSONPrimitive,
                 optional: bool = False):
        super().__init__(
            name,
            enum(*values),
            optional=optional
        )

    def get_as_raw_json(self, instance) -> OptionallyPresent[RawJSONPrimitive]:
        return super().get_as_raw_json(instance)

    def set_from_raw_json(self, instance, value: OptionallyPresent[RawJSONPrimitive]):
        super().set_from_raw_json(instance, value)
