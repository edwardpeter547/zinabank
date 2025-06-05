import os
from pathlib import Path
from typing import Optional


def is_valid_app(dir_item: Path) -> bool:
    """
    Check if the directory item is a valid Django app.
    A valid app must contain both an __init__.py file and an apps.py file.
    """
    package_file = os.path.join(dir_item, '__init__.py')
    apps_file = os.path.join(dir_item, 'apps.py')
    return all([dir_item.is_dir(), os.path.isfile(package_file), os.path.isfile(apps_file)])


def get_core_apps(exclude=[]):
    """
    Retrieve a list of core apps in the project. 
    Optionally exclude specified apps from the list.
    """
    core_apps_dir: Path = Path(__file__).resolve().parent
    apps = []
    for dir_item in core_apps_dir.iterdir():
        if is_valid_app(dir_item) and dir_item.name not in exclude:
            apps.append(f"core_apps.{dir_item.name}")
    return apps


    


