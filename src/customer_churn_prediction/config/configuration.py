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
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPredictionConfig
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
    
    def get_data_transformation_config(self)-> DataTransformationConfig:
        """
        Return data transformation config
        """
        config = self.config.data_transformation
        schema = self.schema.COLUMNS
        target_column = self.schema.TARGET_COLUMN
        params = self.params
        create_directory([config.root_dir])
        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            filtered_data_file=config.filtered_data_file,
            encoded_data_file=config.encoded_data_file,
            encoder_file=config.encoder_file,
            schema=schema,
            target_column=target_column,
            params=params
        )
        return data_transformation_config
    
    def get_model_trainer_config(self)-> ModelTrainerConfig:
        """
        Train the multiple models and pick the best one
        """
        config = self.config.model_trainer
        params = self.params
        target_column = self.schema.TARGET_COLUMN
        create_directory([config.root_dir])
        model_trainer = ModelTrainerConfig(
            root_dir=config.root_dir,
            train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,
            model_name=config.model_name,
            params=params,
            target_column=target_column.name
        )
        return model_trainer
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        """
        Return Model Evaluation config
        """
        config = self.config.model_evaluation
        create_directory([config.root_dir])
        model_evaluation_config = ModelEvaluationConfig(
            root_dir = config.root_dir,
            test_data_path = config.test_data_path,
            model_path = config.model_path,
            target_column = self.schema.TARGET_COLUMN.name,
            metric_file_name = config.metric_file_name
        )
        return model_evaluation_config
    
    def get_prediction_config(self)->ModelPredictionConfig:
        """
        Return the Model Predictor config
        """
        transformation_config = self.config.data_transformation
        config = self.config.model_prediction
        schema = self.schema.COLUMNS

        create_directory([config.root_dir])

        model_predictor_config = ModelPredictionConfig(
            root_dir = config.root_dir,
            encoder_file = transformation_config.encoder_file,
            status_file = config.status_file,
            model_path = config.model_path,
            schema = schema
        )
        return model_predictor_config
    
    

