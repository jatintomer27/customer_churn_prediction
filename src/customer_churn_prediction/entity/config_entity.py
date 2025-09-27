"""
This module contains the all the entity classes responsible for storing 
the configuration of all stages of the customer churn prediction project.
"""


from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Storing configuration related to data ingestion
    """
    root_dir: Path
    kaggle_dataset: str
    file: str
    local_data_file: str
    data_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    """
    Storing configuration related to data validation
    """
    root_dir: Path
    local_data_file: str
    status_file: str
    status_message_file: str
    all_schema: dict