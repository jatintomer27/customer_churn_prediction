"""
Data ingestion component for Downloading the data from Kaggle.
"""

import kaggle
import os

from customer_churn_prediction import logger
from customer_churn_prediction.utils.common import get_size
from customer_churn_prediction.entity.config_entity import DataIngestionConfig

class DataIngestion:
    """
    Handles downloading dataset files from kaggle. 
    """
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        """
        Downloads the dataset file from Kaggle if it does not exist locally.
        """
        try:
            if not os.path.exists(self.config.local_data_file):
                res = kaggle.api.dataset_download_file(
                    self.config.kaggle_dataset,
                    self.config.file,
                    self.config.data_dir
                )
                if res:
                    logger.info(
                        f"File: {self.config.local_data_file} downloaded successfully")
                else:
                    logger.info(
                        f"File: {self.config.local_data_file} failed to download")
            else:
                logger.info(
                    f"File: {self.config.local_data_file} "
                    f"already exists, size: {get_size(self.config.local_data_file)}"
                )
        except Exception as e:
            logger.exception(
                f"Exception occurred while downloading the file: "
                f"{self.config.local_data_file}"
            )
            raise
