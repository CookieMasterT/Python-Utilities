"""
REST api - Representational State Transfer for managing both config files
"""

import json
from pathlib import Path
from typing import Union
from App.InternalScripts.Logging import LoggerSrv


CONFIGPATH = Path(__file__).parents[2].joinpath(r'.\config.json')
DEFAULTCONFIGPATH = Path(__file__).parents[0].joinpath(r'.\default_config.json')

LEGALJSONTYPES = Union[str | int | float | bool | list]

logger = LoggerSrv.LoggerManager().get_logger("ConfigREST")


def get(resource: str, check_both: bool = True) -> LEGALJSONTYPES:
    """
    Retrieves resources from the config files
    :param resource: Resource to fetch from the config file, example: "Utilities.InstaPicPaste.Use",
        "*" can be used as a wildcard symbol to fetch all options
    :param check_both: Whether to check "default_config.json" if the value doesn't exist
    """
    logger.debug(f"Getting {resource}")
    if resource == "*":
        answer = _fetch_all_config(DEFAULTCONFIGPATH, CONFIGPATH)
    else:
        answer = _fetch_config_from_file(resource, CONFIGPATH)
        if answer is None and check_both:
            answer = _fetch_config_from_file(resource, DEFAULTCONFIGPATH)
            if answer is None:
                raise NotImplementedError("default_config.json is missing values or is invalid (did you modify it?)")
    return answer


def _fetch_config_from_file(resource: str, file_path: Path) -> Union[LEGALJSONTYPES, None]:
    try:
        config = json.load(open(file_path))
        return config[resource]
    except json.JSONDecodeError:
        return None  # config file is empty, or has an invalid json
    except KeyError:
        return None  # config does not contain this option


def _fetch_all_config(default_config_path: Path, config_path: Path) -> LEGALJSONTYPES:
    files = [default_config_path, config_path]
    dicts = []
    for file in files:
        try:
            dicts.append(json.load(open(file)))
        except json.JSONDecodeError:
            dicts.append({})  # config file is empty or broken, so we append an empty dictionary
    final_dict = dicts[0]
    for entry in dicts[1]:
        final_dict[entry] = dicts[1][entry]
    return final_dict


def put(resource: str, value: LEGALJSONTYPES):
    """
    Inserts a value into the config file
    :param resource: The resource to which to assign the value, example: "Utilities.InstaPicPaste.Use"
    :param value: The value to set the key to
    """
    logger.debug(f"Setting {resource} to {value}")
    data = json.load(open(CONFIGPATH, "r"))
    data[resource] = value
    json.dump(data, open(CONFIGPATH, "w"))


def delete(resource: str):
    """
    Deletes resources from the config file
    :param resource: The resource to be erased from the config file
        "*" can be used to delete ALL configuration
    :return:
    """
    logger.debug(f"Deleting {resource}")
    if resource == "*":
        json.dump({}, open(CONFIGPATH, "w"))
    else:
        data = json.load(open(CONFIGPATH, "r"))
        try:
            del data[resource]
        except KeyError:
            logger.debug(f"Key {resource} not found in config file")
            pass  # The value that you are trying to delete does not exist, this is passed to guarantee idempotence
        json.dump(data, open(CONFIGPATH, "w"))
