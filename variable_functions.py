from tkinter.font import families
from os import path
import json


def init_config() -> None:
    """ Create empty config file if it doesn't exist """
    if not path.isfile("config.json"):
        with open("config.json", 'a+') as config_file:
            json.dump({}, config_file)


def validate_font(font_name: str) -> bool:
    """
    Ensures the font is valid by comparing it to the list of available fonts
    """
    return font_name in families()  # == tkinter.font.families()


def get_font() -> str:
    """
    Returns value of font key in config. KeyError handled outside
    """
    with open("config.json", "r+") as config_file:
        config_dict: dict = json.load(config_file)
        return config_dict['font']


def set_font(font_name: str) -> None:
    """
    Writes to the config file and sets a new value for font key
    """
    with open("config.json", "r+") as config_file:
        config_dict: dict = json.load(config_file)
        config_dict['font'] = font_name
        json.dump(config_dict, config_file, indent=4)
