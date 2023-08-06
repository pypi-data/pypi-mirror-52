from ...schema import one_of, JSONSchema
from ._Property import Property, InternalType


class OneOfProperty(Property[InternalType]):
    """
    Property which validates JSON that matches exactly one of
    a number of schema.
    """
    def __init__(self,
                 name: str,
                 *sub_schema: JSONSchema,
                 optional: bool = False):
        super().__init__(
            name,
            one_of(*sub_schema),
            optional=optional
        )
