from abc import ABC
from typing import Dict, TypeVar, List, Any

from .._deep_copy import deep_copy
from ._Absent import Absent
from ..schema import JSONSchema, standard_object
from .property import Property
from .._typing import RawJSONObject
from ..serialise import JSONValidatedBiserialisable

T = TypeVar("T", bound="Configuration")


class Configuration(JSONValidatedBiserialisable[T], ABC):
    """
    Base class for Python representations of JSON-format configuration files.
    All configurations are validated against a schema for format correctness.
    The attributes of a configuration should be either JSON types or nested
    configurations.
    """
    def __init__(self, **initial_values):
        # Storage for any additional properties found in the JSON
        self._additional_properties = {}

        # Get the properties, prioritising attribute names
        properties = self.get_all_properties(True)
        properties.update(self.get_all_properties(False))

        # Set the properties
        for name, initial_value in initial_values.items():
            if name not in properties:
                raise ValueError(f"{self.__class__.__name__} has no property '{name}'")

            properties[name].__set__(self, initial_value)

    def to_raw_json(self) -> RawJSONObject:
        # Get a list of all properties
        properties = list(self.get_all_properties().values())

        # Convert the properties to JSON (includes Absent values)
        json_with_absents = {
            property.name(): property.get_as_raw_json(self)
            for property in properties
        }

        # Strip the absent values
        json = {
            key: value
            for key, value in json_with_absents.items()
            if value is not Absent
        }

        # Add any additional properties
        json.update(self._additional_properties)

        return json

    @classmethod
    def from_raw_json(cls, raw_json: RawJSONObject) -> T:
        # Create the instance
        instance = cls()

        # Initialise the additional properties to all of the JSON
        instance._additional_properties = deep_copy(raw_json)

        # Get the properties of this configuration type
        properties: Dict[str, Property] = cls.get_all_properties(True)

        # Set the value of each property to the JSON value,
        # and remove it from the additional properties
        for name, property in properties.items():
            if name in raw_json:
                property.set_from_raw_json(instance, raw_json[name])
                instance._additional_properties.pop(name)
            else:
                property.set_from_raw_json(instance, Absent)

        return instance

    @classmethod
    def get_json_validation_schema(cls) -> JSONSchema:
        # Get the properties of this configuration type
        properties: Dict[str, Property] = cls.get_all_properties(True)

        # Extract the required property schemas
        required_properties: Dict[str, JSONSchema] = {
            name: property.get_json_validation_schema()
            for name, property in properties.items()
            if not property.is_optional()
        }

        # Extract the optional property schemas
        optional_properties: Dict[str, JSONSchema] = {
            name: property.get_json_validation_schema()
            for name, property in properties.items()
            if property.is_optional()
        }

        return standard_object(required_properties, optional_properties, additional_properties=True)

    @classmethod
    def get_all_properties(cls, with_property_names: bool = False) -> Dict[str, Property]:
        """
        Gets all properties of this configuration.

        :param with_property_names:     Whether the keys should be the property names (by default
                                        they are the attribute names).
        :return:                        A dictionary of the properties of this configuration.
        """
        # Get the attribute names
        attribute_names: List[str] = dir(cls)

        # Get the mapping from attribute name to attribute
        attributes: Dict[str, Any] = {name: getattr(cls, name)
                                      for name in attribute_names
                                      if not name.startswith("_")}

        # Get the properties
        properties = {
            name: attribute
            for name, attribute in attributes.items()
            if isinstance(attribute, Property)
        }

        # Convert the names to the property names if requested
        if with_property_names:
            properties = {property.name(): property for property in properties.values()}

        return properties

    def __init_subclass__(cls, **kwargs):
        # Make sure the property names are unique
        property_names = [property.name() for property in cls.get_all_properties().values()]
        if len(property_names) != len(set(property_names)):
            raise TypeError(f"Duplicate property names in {cls.__name__}: {', '.join(property_names)}")
