from typing import Optional

from ...schema import string_schema
from .._OptionallyPresent import OptionallyPresent
from ._Property import Property


class StringProperty(Property[str]):
    """
    Configuration property which validates a string.
    """
    def __init__(self,
                 name: str,
                 min_length: Optional[int] = None,
                 max_length: Optional[int] = None,
                 pattern: Optional[str] = None,
                 format: Optional[str] = None,
                 *,
                 optional: bool = False):
        super().__init__(
            name,
            string_schema(
                min_length,
                max_length,
                pattern,
                format
            ),
            optional=optional
        )

    def get_as_raw_json(self, instance) -> OptionallyPresent[str]:
        return super().get_as_raw_json(instance)

    def set_from_raw_json(self, instance, value: OptionallyPresent[str]):
        super().set_from_raw_json(instance, value)
