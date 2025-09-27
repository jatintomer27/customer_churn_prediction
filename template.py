"""
Script to create the initial project structure for customer churn prediction. 
"""

import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]:%(levelname)s:%(module)s:%(message)s')

PROJECT_NAME = 'customer_churn_prediction'

list_of_files = [
    f'src/{PROJECT_NAME}/__init__.py',
    f'src/{PROJECT_NAME}/components/__init__.py',
    f'src/{PROJECT_NAME}/entity/__init__.py',
    f'src/{PROJECT_NAME}/entity/config_entity.py',
    f'src/{PROJECT_NAME}/config/__init__.py',
    f'src/{PROJECT_NAME}/config/configuration.py',
    f'src/{PROJECT_NAME}/utils/__init__.py',
    f'src/{PROJECT_NAME}/utils/common.py',
    f'src/{PROJECT_NAME}/constants/__init__.py',
    f'src/{PROJECT_NAME}/pipeline/__init__.py',
    f'src/{PROJECT_NAME}/pipeline/stage_01_data_ingestion.py',
    f'resarch/trials.ipynb',
    f'config/config.yaml',
    f'params.yaml',
    f'schema.yaml',
    f'main.py',
    f'pyproject.toml',
    f'requirements.txt',
]

for file in list_of_files:
    filepath = Path(file)
    filedir, filename = os.path.split(filepath)

    if filedir != '':
        os.makedirs(filedir,exist_ok=True)
        logging.info(f'Directory {filedir} is created successfully for file {filename}')

    if not (os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
            logging.info(f'Creating empty file {filename}')
    else:
        logging.info(f'{filename} already exist')