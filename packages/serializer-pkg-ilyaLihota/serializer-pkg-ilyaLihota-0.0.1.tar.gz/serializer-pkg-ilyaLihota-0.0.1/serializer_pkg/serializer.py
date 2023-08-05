#!usr/bin/python3.7.3
# -*- coding: utf-8 -*-
"""Serializer."""


filename = "serialized.txt"

PRIMITIVE_TYPES = {
    int: "int",
    float: "float",
    complex: "complex",
    str: "str",
    bool: "bool"
}
CONTAINER_TYPES = {
    list: "list",
    tuple: "tuple",
    set: "set",
    frozenset: "frozenset"
}
DICT_TYPE = {dict: "dict"}


def deserialize(string: str) -> list:
    deserial_data = []
    parsed_data = parse_string(string)

    for el in parsed_data:
        obj_type, value = el.split("=")

        if obj_type in PRIMITIVE_TYPES.values():
            deserial_data.append(parse_type(obj_type)(value))

        elif obj_type in CONTAINER_TYPES.values():
            deserial_data.append(parse_type(obj_type)(deserialize(value)))

        elif obj_type in DICT_TYPE.values():
            deserial_string = deserialize(value)
            arr = [(deserial_string[index], deserial_string.pop(index+1))
                for index, el in enumerate(deserial_string)]
            deserial_data.append(parse_type(obj_type)(arr))

    return deserial_data


def dump(obj, filename=filename):
    with open(filename, "a") as f:
        f.write("{};\n".format(serialize(obj)))


def load(filename=filename):
    with open(filename) as f:
        lines = f.readlines()

    return [deserialize(line) for line in lines]


def parse_string(string: str) -> list:
    parsed_data = []
    obj_type = value = ""
    amount_of_parent = 0
    start = end = None

    for index, el in enumerate(string):
        if el == "(":
            amount_of_parent += 1

            if start == None:
                start = index + 1

        elif el == ")":
            amount_of_parent -= 1

            if amount_of_parent == 0:
                end = index
                value = string[start:end]
                parsed_data.append("{}={}".format(obj_type, value))
                obj_type, value = "", ""
                start = end = None

        elif amount_of_parent == 0 and el.isalpha():
            obj_type += el

    return parsed_data


def parse_type(str_type: str):
    if str_type == "int":
        return int
    elif str_type == "float":
        return float
    elif str_type == "complex":
        return complex
    elif str_type == "str":
        return str
    elif str_type == "list":
        return list
    elif str_type == "tuple":
        return tuple
    elif str_type == "set":
        return set
    elif str_type == "dict":
        return dict


def serialize(obj) -> str:
    serialized_data = ""

    if type(obj) in PRIMITIVE_TYPES:
        return serialized_data+"{}({})".format(PRIMITIVE_TYPES[type(obj)], obj)

    else:
        if type(obj) in CONTAINER_TYPES:
            serialized_data += CONTAINER_TYPES[type(obj)]

            return "{}({})".format(serialized_data, ", ".join([serialize(el)
                for el in obj]))

        elif type(obj) in DICT_TYPE:
            serialized_data += DICT_TYPE[type(obj)]
            arr =  ["{}:{}".format(serialize(key), serialize(value))
                for key, value in obj.items()]

            return "{}({})".format(serialized_data, ", ".join(arr))


if __name__ == "__main__":
    dump(54)
    dump(5j+3)
    dump(3.14)
    dump("abc")
    dump((1, 2, 3))
    dump([1, 2, 3, [4, 5]])
    dump([[1, 2], "b", 3, (5, 7, "c")])
    dump({1: "a", 2: "b"})

    print(load())
