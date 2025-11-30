import json
from pathlib import Path


def fetch_shortcut(utility_name : str):
    try:
        config = json.load(open(Path(__file__).parents[1].joinpath('.\\config.json')))
        try:
            return config[f'Utilities.{utility_name}.Use']
        except KeyError:
            pass
            #normal config does not contain this option
    except json.JSONDecodeError:
        pass
        #config file is empty
    backup_config = json.load(open(Path(__file__).parents[0].joinpath('.\\default_config.json')))
    try:
        return backup_config[f'Utilities.{utility_name}.Use']
    except KeyError:
        raise NotImplementedError("Config does not exist in default_config.json")
