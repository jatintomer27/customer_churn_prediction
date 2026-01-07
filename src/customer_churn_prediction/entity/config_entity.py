"""
This module contains all the entity classes responsible for storing the
configuration of all stages of the customer churn prediction project.
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
    local_data_file: Path
    status_file: str
    status_message_file: str
    all_schema: dict


@dataclass(frozen=True)
class DataTransformationConfig:
    """
    Storing configuration related to the data transformation.
    """
    root_dir: Path
    local_data_file: Path
    filtered_data_file: Path
    encoded_data_file: Path
    encoder_file: Path
    schema: dict
    target_column: dict
    params: dict


@dataclass(frozen=True)
class ModelTrainerConfig:
    """
    Storing configuration related to the model trainer.
    """
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    target_column: str

@dataclass(frozen=True)
class ModelEvaluationConfig:
    """
    Storing configuration related to the model evaluation.
    """
    root_dir: Path
    test_data_path: Path
    model_path: Path
    target_column: str
    metric_file_name: Path

@dataclass(frozen=True)
class ModelPredictionConfig:
    """
    Storing configuration related to the model evaluation.
    """
    root_dir: Path
    encoder_file: Path
    status_file: Path
    model_path: Path
    schema: dict
