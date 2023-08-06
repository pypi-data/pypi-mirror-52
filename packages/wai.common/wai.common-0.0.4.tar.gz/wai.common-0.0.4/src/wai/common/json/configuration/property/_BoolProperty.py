from ...schema import BOOL_SCHEMA
from .._OptionallyPresent import OptionallyPresent
from ._Property import Property


class BoolProperty(Property):
    """
    Configuration property which validates a boolean value.
    """
    def __init__(self,
                 name: str,
                 *,
                 optional: bool = False):
        super().__init__(
            name,
            BOOL_SCHEMA,
            optional=optional
        )

    def get_as_raw_json(self, instance) -> OptionallyPresent[bool]:
        return super().get_as_raw_json(instance)

    def set_from_raw_json(self, instance, value: OptionallyPresent[bool]):
        super().set_from_raw_json(instance, value)
