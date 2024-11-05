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
    with open("config.json", "r") as config_file:
        config_dict: dict = json.load(config_file)
        return config_dict['font']


def set_font(font_name: str) -> None:
    """
    Writes to the config file and sets a new value for font key
    """
    with open("config.json", "r") as config_file:
        try:
            config_dict = json.load(config_file)
        except json.JSONDecodeError:
            # If the file is empty, initialize an empty dictionary
            config_dict = {}

    config_dict.setdefault('font', "").append(font_name)
    with open("config.json", "w") as config_file:
        json.dump(config_dict, config_file, indent=4)


def save_task(task_text: str) -> None:
    """
    Writes to the config file and saves task in tasks key
    """
    with open("config.json", "r") as config_file:
        try:
            config_dict = json.load(config_file)
        except json.JSONDecodeError:
            # If the file is empty, initialize an empty dictionary
            config_dict = {}

    config_dict.setdefault('tasks', []).append(task_text)
    with open("config.json", "w") as config_file:
        json.dump(config_dict, config_file, indent=4)


def get_tasks() -> list[str]:
    """
    Returns list saved in the tasks key
    """
    with open("config.json", "r") as config_file:
        config_dict: dict = json.load(config_file)
        try:
            return config_dict['tasks']
        except KeyError:
            return []


def remove_config_task(task_text: str) -> None:
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)

    # Check if the 'tasks' key exists and remove the task if it is in the list
    if 'tasks' in config_dict and task_text in config_dict['tasks']:
        config_dict['tasks'].remove(task_text)

        # Write the updated dictionary back to the file
        with open("config.json", "w") as config_file:
            json.dump(config_dict, config_file, indent=4)
