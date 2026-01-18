"""
Module Handles and execute the data ingestion pipeline
"""

from customer_churn_prediction import logger
from customer_churn_prediction.config.configuration import ConfigurationManager
from customer_churn_prediction.components.data_ingestion import DataIngestion

class DataIngestionPipeline:
    """
    Handles the data ingestion pipeline
    """
    def __init__(self):
        pass

    def main(self):
        """
        Execute the data ingestion pipeline
        """
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion.download_file()
        except Exception as e:
            logger.exception(
                f"Exception occured while executing the data ingestion pipeline")
            raise

if __name__ == "__main__":
    DataIngestionPipeline().main()
