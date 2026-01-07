"""
Module handle and execute data transformation pipeline.
"""

from customer_churn_prediction import logger
from customer_churn_prediction.config.configuration import (
    ConfigurationManager
)
from customer_churn_prediction.components.data_transformation import (
    DataTransformation
)

class DataTransformationPipeline:
    """
    Handle the data transformation pipeline.
    """

    def __init__(self):
        pass

    def main(self):
        """
        Execute data transformation pipeline.
        """
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            status_file = data_validation_config.status_file
            with open(status_file,'r') as f:
                status_file_data = f.read()
                logger.info(f"Status file: {status_file} data is {status_file_data}")
                status = status_file_data.split(" ")[-1]
            if status:
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(data_transformation_config)
                data_transformation.filter_dataset()
                data_transformation.drop_duplicates()
                data_transformation.categorical_column_encoder(encoding='label_encoding')
                data_transformation.train_test_splitting()
                data_transformation.manage_inbalanced_data()
            else:
                raise Exception("Your data schema is not validated")
        except Exception:
            logger.exception(
                f"Exception occured while executing the data transformation pipeline"
            )