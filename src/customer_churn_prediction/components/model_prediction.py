"""
Model Prediction component validate the passed data and apply all the preprocessing steps .
Then predict the data based on the processed data
"""

import pandas as pd
from pathlib import Path
import pickle
import joblib

from customer_churn_prediction import logger
from customer_churn_prediction.entity.config_entity import ModelPredictionConfig

class ModelPrediction:
    def __init__(self, config: ModelPredictionConfig):
        self.config = config

    def validate_data(self,data: pd.DataFrame):
        """
        Validate the passed data columns on the specified schema.

        Params:
            data (pd.DataFrame): Data to validate the schema

        Stores:
            msg (str): Whether the passed data is validated along with data type specifed in schema

        Returns:
            msg (str): Whether the passed data validated on schema or not
        """
        try:
            data_columns = data.dtypes.astype(str).to_dict()
            schema = self.config.schema
            msg = ""
            valiation_status = True
            for column_name,datatype in schema.items():
                if data_columns.get(column_name):
                    valiation_status = True if valiation_status else False
                    if data_columns.get(column_name) == datatype:
                        valiation_status = True if valiation_status else False
                        msg += f"{column_name} validated along with datatype"
                    else:
                        valiation_status = False
                        msg += f"{column_name} validated without datatype"
                else:
                    valiation_status = False
                    msg += f"{column_name} not validated"
                msg += "\n"
            with open(self.config.status_file,'w+') as f:
                f.write(f"Validation status: {valiation_status}")
            logger.info(f"Model Prediction stage data validation: \n {msg}")
        except Exception:
            logger.exception(f"Exception occured while validating the columns")
            return "Something went wrong"
        else:
            return msg

    def pre_process_data(self, data: pd.DataFrame):
        """
        Check whether the passed data is validated based on the specified schema.

        If the data is validated then transform the data by the encoders applied while training the data.

        Params:
            data (pd.DataFrame): Data to validate the schema

        Returns:
            msg (str): Whether data is processed or not.
            is_data_processed (bool): Whether data is processed successfully or not.
            relevant_data (pd.DataFrame): Relevant data after transformation based on the schema.
        """
        msg, is_data_processed, relevant_data = '', False, pd.DataFrame()
        
        status = False
        with open(self.config.status_file,'r+') as f:
            status_file_data = f.read()
            if status_file_data:
                status = status_file_data.rsplit(" ",1)
        if status:
            with open(self.config.encoder_file,"rb") as f:
                encoders = pickle.load(f)
                for col, encoder in encoders.items():
                    if col in data.columns:
                        data[col] = encoder.transform(data[col])
            relevant_data = data[list(self.config.schema.keys())]
            msg = "Data processed successfully"
            is_data_processed = True
        else:
            msg = "Data columns are not validated"
            is_data_processed = False
        return msg, is_data_processed, relevant_data 

    def predict(self, data: pd.DataFrame):
        """
        Check whether data is validated based on the schema.
        Preprocess the passed data as applied while training the model

        Predict wherther the customer will churn or not

        Params:
            data (pd.DataFrame): Data used to predict the churn.

        Returns:
            status (bool): Whether prediction is successfull.
            prediction (class) : Whether customer will churn or not or None
            msg (str): Data preprocessing message
        """
        status, prediction, msg = False, None, ''          
        validation_msg = self.validate_data(data)
        processing_msg, is_data_processed, relevant_data = self.pre_process_data(data)
        if is_data_processed:
            model_path = Path(self.config.model_path)
            if model_path:
                model = joblib.load(Path(self.config.model_path))
                prediction = model.predict(relevant_data)
                status = True
            else:
                msg = "Model is not exist yet train the model first"
        else:
            msg = processing_msg
        return status, prediction, msg
            