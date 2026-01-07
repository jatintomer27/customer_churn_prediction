"""
Data validation component for validating the columns and their data types based on schema.
"""

import pandas as pd

from customer_churn_prediction import logger
from customer_churn_prediction.entity.config_entity import DataValidationConfig

class DataValidation:
    """
    Handles dataset validation based on schema
    """
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self):
        """
        Validate the dataset columns based on the predefined schema.
        """
        try:
            data = pd.read_csv(self.config.local_data_file)
            dataset_columns = data.dtypes.astype(str).to_dict()
            all_schema = self.config.all_schema.items()
            msg = ""
            valiation_status = True
            for column_name,datatype in all_schema:
                if dataset_columns.get(column_name):
                    valiation_status = True if valiation_status else False
                    if dataset_columns.get(column_name) == datatype:
                        valiation_status = True if valiation_status else False
                        msg += f"{column_name} validated along with datatype"
                    else:
                        valiation_status = False
                        msg += f"{column_name} validated without datatype"
                else:
                    valiation_status = False
                    msg += f"{column_name} not validated"
                msg += "\n"
            with open(self.config.status_message_file,'w+') as f:
                f.write(msg)
            with open(self.config.status_file,'w+') as f:
                f.write(f"Validation status: {valiation_status}")
        except Exception:
            logger.exception(f"Exception occured while validating the columns")
            raise
