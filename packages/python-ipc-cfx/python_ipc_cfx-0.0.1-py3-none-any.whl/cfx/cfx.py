import abc
import json
from .utils.factory import create_object


class CFXMessage(abc.ABC):
    """
    Abstract base class for all CFX Messages.

    Contains no data members.

    Provides for the serialization and deserialization of messages to and from JSON format.
    """
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def from_dict(obj):
        """Instanciates an IPC CFX Object from its dict form (see to_dict).

        Args:
            obj (dict): serialized dict IPC CFX object

        Returns
            CFXMessage: an IPC CFX object
        """
        if not isinstance(obj, dict):
            raise TypeError("CFXMessage: FromBytes expects a dict argument")
        try:
            class_name = list(obj.keys())[0]
        except IndexError:
            raise ValueError("CFXMessage: FromBytes corrupt argument")
        return create_object(class_name, obj[class_name])

    @staticmethod
    def from_json(raw_data):
        """Instanciates an IPC CFX Object from its JSON-as-string form (see ToJson).

        Args:
            raw_data (string - json): JSON object as a string

        Returns
            CFXMessage: an IPC CFX object
        """
        if not isinstance(raw_data, str):
            raise TypeError("CFXMessage: FromJson expects a string argument")
        try:
            obj = json.loads(raw_data)
        except json.JSONDecodeError:
            raise ValueError("CFXMessage: FromJson corrupt argument")
        return CFXMessage.from_dict(obj)

    @staticmethod
    def from_type_name(class_name):
        """Instanciates the default IPC CFX object corresponding to the class_name.

        Args:
            class_name (str): Name of the IPC CFX object to instanciate

        Returns
            CFXMessage: an IPC CFX object
        """
        if not isinstance(class_name, str):
            raise TypeError("CFXMessage: FromTypeName expects a string argument")
        return create_object(class_name, {})

    def to_dict(self):
        """Transforms an IPC CFX object into a simple dict.

        Returns:
            dict: The object as a dict.

        Format is as follows:
        {
            class_name: {
                key:value
                key:value,
                ...
            }
        }
        """
        return {
            self.__class__.__name__: vars(self)
        }

    def to_json(self, formatted=False):
        """Transforms an IPC CFX object into a JSON representation of its bytes form.

        Args:
            formatted (bool): Optional, whether or not the output string should be pretty-fied
        Returns:
            string - JSON: The object as a dict, as a string.
        """
        obj = self.to_dict()
        if formatted:
            return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
        return json.dumps(obj)


class CFXEnvelope():
    pass


class NotSupportedResponse():
    pass
