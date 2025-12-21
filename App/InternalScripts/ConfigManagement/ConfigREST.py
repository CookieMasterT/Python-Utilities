"""
REST api - Representational State Transfer for managing both config files
"""

import json
from pathlib import Path
from typing import Union
from App.InternalScripts.Logging import LoggerSrv


CONFIGPATH = Path(__file__).parents[2] / "config.json"
DEFAULTCONFIGPATH = Path(__file__).parent / "default_config.json"

LEGALJSONTYPES = str | int | float | bool | list

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
                logger.error("default_config.json is missing values or is invalid (did you modify it?)")
                raise NotImplementedError("Attempted to fetch a config value that does not exist or is invalid")
    return answer


def _fetch_config_from_file(resource: str, file_path: Path) -> Union[LEGALJSONTYPES, None]:
    try:
        with open(file_path) as f:
            config = json.load(f)
        return config[resource]
    except json.JSONDecodeError as e:
        logger.debug("config file is empty, or has an invalid json")
        logger.debug(e)
        return None
    except KeyError as e:
        logger.debug("config does not contain this option")
        logger.debug(e)
        return None


def _fetch_all_config(default_config_path: Path, config_path: Path) -> LEGALJSONTYPES:
    files = [default_config_path, config_path]
    dicts = []
    for file in files:
        try:
            with open(file) as f:
                dicts.append(json.load(f))
        except json.JSONDecodeError as e:  # config file is empty or broken, so we append an empty dictionary
            logger.warning("Config file is empty or invalid")
            logger.warning(e)
            dicts.append({})
    final_dict = dicts[0]
    for entry in dicts[1]:
        final_dict[entry] = dicts[1][entry]
    return final_dict


def put(resource: str, value: LEGALJSONTYPES):
    """
    Inserts a value into the config file or updates it
    :param resource: The resource to which to assign the value, example: "Utilities.InstaPicPaste.Use"
    :param value: The value to set the key to
    """
    logger.debug(f"Setting {resource} to {value}")
    with open(CONFIGPATH, "r") as f:
        data = json.load(f)
    data[resource] = value
    with open(CONFIGPATH, "w") as f:
        json.dump(data, f)


def delete(resource: str):
    """
    Deletes resources from the config file
    :param resource: The resource to be erased from the config file
        "*" can be used to delete ALL configuration
    :return:
    """
    logger.debug(f"Deleting {resource}")
    if resource == "*":
        with open(CONFIGPATH, "w") as f:
            json.dump({}, f)
    else:
        with open(CONFIGPATH, "r") as f:
            data = json.load(f)
        try:
            del data[resource]
        except KeyError as e:  # The value that you are trying to delete does not exist
            # this is passed to guarantee idempotence
            logger.debug(f"Key {resource} not found in config file")
            logger.debug(e)
        with open(CONFIGPATH, "w") as f:
            json.dump(data, f)
