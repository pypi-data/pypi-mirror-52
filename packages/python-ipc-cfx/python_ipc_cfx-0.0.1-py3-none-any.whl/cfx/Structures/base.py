from enum import IntEnum
from numbers import Number, Integral
from json import dumps


class CFXEnum(IntEnum):
    def __str__(self):
        return self._name_  # pylint: disable=no-member;

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self._name_)  # pylint: disable=no-member;

    @classmethod
    def default(cls):
        return next(iter(cls))

    @classmethod
    def from_str(cls, s):
        for idx, value in enumerate([str(item) for item in list(cls)]):
            if value == s:
                return cls(idx)
        raise ValueError("{class_name}: Could not build object from value {value}".format(
            class_name=cls.__class__.__name__,
            value=s
        ))


class CFXStructure():
    def __str__(self):
        return dumps(self.as_dict())

    def as_dict(self):
        obj = {}
        for key in self.__dict__:
            val = self.__dict__[key]
            if isinstance(val, CFXEnum):
                obj[key] = str(val)
            elif isinstance(val, CFXStructure):
                obj[key] = val.as_dict()
            elif isinstance(val, list):
                obj[key] = _unroll_list(val)
            else:
                obj[key] = val
        return obj


def _unroll_list(l):
    if not isinstance(l, list):
        raise TypeError("unroll_list: unroll_list only takes lists as arguments")
    out = []
    for value in l:
        if isinstance(value, CFXEnum):
            out.append(str(value))
        elif isinstance(value, CFXStructure):
            out.append(value.as_dict())
        elif isinstance(value, list):
            out.append(_unroll_list(value))
        else:
            out.append(value)
    return out


def load_basic(kwargs, name, type, default=None):
    if type == "number":
        type = Number
    if default is not None and not isinstance(default, type):
        raise TypeError("load_basic: default value {default} is not of type {type}".format(
            default=default,
            type=type
        ))
    value = kwargs.get(name, default)
    if value is not None and not isinstance(value, type):
        raise TypeError("load_basic: {name} provided ({value}), but not of type {type}".format(
            name=name,
            type=type,
            value=value
        ))
    return value


def load_enum(kwargs, name, expected_type: CFXEnum, default=None):
    if not issubclass(expected_type, CFXEnum):
        raise TypeError("load_enum: load_enum only works with subclasses of CFXEnum, not %s" % expected_type.__name__)
    if default is not None and not isinstance(default, expected_type):
        raise TypeError("load_enum: default %s is not of type %s" % (default, expected_type.__name__))
    val = kwargs.get(name, default)
    if val is None:
        return None
    if isinstance(val, str):
        val = expected_type.from_str(val)
    if not isinstance(val, expected_type):
        raise TypeError("load_enum: {name} provided ({value}), but not a {expected_type}".format(
            name=name,
            value=val,
            expected_type=expected_type.__name__
        ))
    return val


def load_structure(kwargs, name, expected_structure, default=None):
    if not issubclass(expected_structure, CFXStructure):
        raise TypeError(
            "load_structure: load_structure only works with subclasses of CFXStructure, not %s"
            % expected_structure.__name__
        )
    if default is not None and not isinstance(default, expected_structure):
        raise TypeError("load_structure: default %s is not of type %s" % (default, expected_structure.__name__))
    val = kwargs.get(name, default)
    if val is None:
        return None
    if isinstance(val, dict):
        val = expected_structure(**val)
    if not isinstance(val, expected_structure):
        raise TypeError("load_structure: {name} provided ({value}), but not a {expected_type}".format(
            name=name,
            value=val,
            expected_type=expected_structure.__name__
        ))
    return val


def load_list_enum(kwargs, name, expected_type, default=None):
    default = default or []
    if not issubclass(expected_type, CFXEnum):
        raise TypeError("load_list_enum: load_enum only works with subclasses of CFXEnum, not %s" % expected_type.__name__)
    if isinstance(default, dict) or isinstance(default, expected_type):
        default = [default]
    if not isinstance(default, list):
        raise TypeError("load_list_enum: default {} is a wrong type".format(default))
    for item in default:
        if not isinstance(item, dict) or isinstance(item, expected_type):
            raise TypeError("load_list_enum: default {} is a wrong type".format(item))
    values = kwargs.get(name, default)
    if isinstance(values, dict):
        values = [values]
    if not isinstance(values, list):
        raise TypeError("load_list_enum: {name} provided ({value}), but not a list".format(
            name=name,
            value=values
        ))
    out = []
    for val in values:
        if isinstance(val, str):
            val = expected_type.from_str(val)
        if not isinstance(val, expected_type):
            raise TypeError("load_enum: {name} provided ({value}), but not a {expected_type}".format(
                name=name,
                value=val,
                expected_type=expected_type.__name__
            ))
        out.append(val)
    return out


def load_list_structure(kwargs, name, expected_structure, default=None):
    default = default or []
    if not issubclass(expected_structure, CFXStructure):
        raise TypeError("load_list_structure: load_list_structure only works with subclasses of CFXStructure, not %s" % expected_structure.__name__)
    if isinstance(default, dict) or isinstance(default, expected_structure):
        default = [default]
    if not isinstance(default, list):
        raise TypeError("load_list_structure: default {} is a wrong type".format(default))
    for item in default:
        if not (isinstance(item, dict) or isinstance(item, expected_structure)):
            raise TypeError("load_list_structure: default {} is a wrong type".format(item))
    values = kwargs.get(name, default)
    if isinstance(values, dict):
        values = [values]
    if not isinstance(values, list):
        raise TypeError("load_list_structure: {name} provided ({value}), but not a list".format(
            name=name,
            value=values
        ))
    out = []
    for val in values:
        if isinstance(val, dict):
            val = expected_structure(**val)
        if not isinstance(val, expected_structure):
            raise TypeError("load_list_structure: {name} provided ({value}), but not a {expected_type}".format(
                name=name,
                value=val,
                expected_type=expected_structure.__name__
            ))
        out.append(val)
    return out


def is_nullable_number(n):
    return n is None or isinstance(n, Number)


def is_nullable_int(n):
    return n is None or (isinstance(n, Integral) and n >= 0)
