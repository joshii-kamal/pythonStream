import json


def get_config():
    with open("config/config.json", "r") as config_file:
        config = json.load(config_file)
    return config
