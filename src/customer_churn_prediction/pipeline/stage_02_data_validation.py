"""
Module Handle and execute data validation pipeline.
"""

from customer_churn_prediction import logger
from customer_churn_prediction.config.configuration import ConfigurationManager
from customer_churn_prediction.components.data_validation import DataValidation

class DataValidationPipeline:
    """
    Handles the data validation pipeline.
    """
    def __init__(self):
        pass

    def main(self):
        """
        Execute the data validation pipeline.
        """
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(data_validation_config)
            data_validation.validate_all_columns()
        except Exception:
            logger.exception(
                f"Exception occured while executing the data validation pipeline"
            )