"""
Configuration manager module for the Customer Churn Prediction project.
Handles loading and managing project configuration, parameters, and schema.
"""

from customer_churn_prediction.constants import (
    CONFIG_FILE_PATH, 
    PARAMS_FILE_PATH,
    SCHEMA_FILE_PATH 
)
from customer_churn_prediction.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig
)
from customer_churn_prediction.utils.common import create_directory, read_yaml


class ConfigurationManager:
    """
    Handles loading and managing configuration, 
    parameters and schema for the project.
    """
    def __init__(
            self,
            config_path=CONFIG_FILE_PATH,
            schema_path=SCHEMA_FILE_PATH,
            params_path=PARAMS_FILE_PATH):
        
        self.config = read_yaml(config_path)
        self.schema = read_yaml(schema_path)
        self.params = read_yaml(params_path)

        create_directory([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Return Data Ingestion configuration.
        """
        config = self.config.data_ingestion
        create_directory([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            kaggle_dataset = config.kaggle_dataset,
            file = config.file,
            local_data_file = config.local_data_file,
            data_dir = config.data_dir
        )
        return data_ingestion_config

    def get_data_validation_config(self)-> DataValidationConfig:
        """
        Return Data validation configuration.
        """
        config = self.config.data_validation
        schema = self.schema.COLUMNS
        create_directory([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            status_file=config.status_file,
            status_message_file=config.status_message_file,
            all_schema=schema
        )
        return data_validation_config

