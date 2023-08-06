from typing import Optional

from ...schema import number
from .._OptionallyPresent import OptionallyPresent
from ..._typing import RawJSONNumber
from ._Property import Property


class NumberProperty(Property[RawJSONNumber]):
    """
    Property which validates a number.
    """
    def __init__(self,
                 name: str,
                 minimum: Optional[RawJSONNumber] = None,
                 maximum: Optional[RawJSONNumber] = None,
                 integer_only: bool = False,
                 multiple_of: Optional[RawJSONNumber] = None,
                 exclusive_minimum: bool = False,
                 exclusive_maximum: bool = False,
                 *,
                 optional: bool = False):
        super().__init__(
            name,
            number(
                minimum,
                maximum,
                integer_only,
                multiple_of,
                exclusive_minimum,
                exclusive_maximum
            ),
            optional=optional
        )

    def get_as_raw_json(self, instance) -> OptionallyPresent[RawJSONNumber]:
        return super().get_as_raw_json(instance)

    def set_from_raw_json(self, instance, value: OptionallyPresent[RawJSONNumber]):
        super().set_from_raw_json(instance, value)
