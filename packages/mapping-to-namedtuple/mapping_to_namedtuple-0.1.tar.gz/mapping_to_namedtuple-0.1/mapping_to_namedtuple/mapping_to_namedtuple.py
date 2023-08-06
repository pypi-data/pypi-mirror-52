from collections import namedtuple
from collections.abc import Mapping


def mapping_to_named_tuple(mapping, name="root"):
    """
    Converts python Mapping to namedtuple recursively

    :param mapping: mapping to convert
    :param name: name to set as name of named tuple root
    :return: namedtuple with name <name> that corresponds with mapping <mapping>
    """
    if isinstance(mapping, Mapping):
        mapping = {key: mapping_to_named_tuple(value, key) for key, value in mapping.items()}
        return namedtuple(name, mapping.keys())(**mapping)
    elif isinstance(mapping, list):
        return tuple([mapping_to_named_tuple(item, name) for item in mapping])
    else:
        return mapping
