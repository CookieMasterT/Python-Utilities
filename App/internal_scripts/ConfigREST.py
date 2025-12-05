"""
REST api - Representational State Transfer for managing both config files
"""

import json
from pathlib import Path
from typing import Union

CONFIGPATH = Path(__file__).parents[1].joinpath('.\\config.json')
DEFAULTCONFIGPATH = Path(__file__).parents[0].joinpath('.\\default_config.json')

LEGALJSONTYPES = Union[str | int | float | bool | list]


def get(resource: str, check_both: bool = True) -> LEGALJSONTYPES:
    """
    Retrieves a value from the config files
    :param resource: Resource to fetch from the config file, example: "Utilities.InstaPicPaste.Use"
    :param check_both: Whether to check "default_config.json" if the value doesn't exist
    """
    answer = _fetch_config_from_file(resource, CONFIGPATH)
    if answer is None and check_both:
        answer = _fetch_config_from_file(resource, DEFAULTCONFIGPATH)
        if answer is None:
            raise NotImplementedError("default_config.json is missing values or is invalid (did you modify it?)")
    return answer


def _fetch_config_from_file(resource: str, file_path: Path):
    try:
        config = json.load(open(file_path))
        return config[resource]
    except json.JSONDecodeError:
        return None  # config file is empty, or has an invalid json
    except KeyError:
        return None  # config does not contain this option


def put(resource: str, value: LEGALJSONTYPES):
    """
    Inserts a value into the config file
    :param resource: The resource to which to assign the value, example: "Utilities.InstaPicPaste.Use"
    :param value: The value to set the key to
    """
    data = json.load(open(CONFIGPATH, "r"))
    data[resource] = value
    json.dump(data, open(CONFIGPATH, "w"))


def delete(resource: str):
    """
    Deletes a resource
    :param resource: The resource to be erased from the config file
    :return:
    """
    data = json.load(open(CONFIGPATH, "r"))
    del data[resource]
    json.dump(data, open(CONFIGPATH, "w"))
    pass
