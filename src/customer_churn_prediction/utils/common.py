"""
Contains utility functions
"""

from box import ConfigBox
from box.exceptions import BoxValueError
from customer_churn_prediction import logger
from pathlib import Path
from ensure import ensure_annotations
import os
import yaml

@ensure_annotations
def read_yaml(path_to_file:Path) ->ConfigBox:
    """
    read the yaml file and return

    Args:
        path_to_file(str): Path of yaml file

    Raises:
        ValueError: if yaml file is empty
        e: otherwise

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_file,'r+') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"Yaml file: {path_to_file} is loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"Yaml file: {path_to_file} is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directory(path_to_directories:list,verbose=True):
    """
    Create list of directories

    Args:
        path_to_directories(list): list of directories path
        verbose(bool,optional): ignore logs. Default is false
    """
    for path in path_to_directories:
        os.makedirs(Path(path),exist_ok=True)
        if verbose:
            logger.info(f"Directory created at: {path}")

@ensure_annotations
def get_size(path:Path)->str:
    """
    get size in KB

    Args:
        path(str): path of the file

    Returns:
        size(str): size of file in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~{size_in_kb} KB"