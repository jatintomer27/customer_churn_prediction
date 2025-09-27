from customer_churn_prediction import logger
from customer_churn_prediction.pipeline.stage_01_data_ingestion import (
    DataIngestionPipeline
)
from customer_churn_prediction.pipeline.stage_02_data_validation import (
    DataValidationPipeline
)

STAGE_NAME = "Data Ingestion"

try:
    logger.info(f">>>>> Stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>> Stage {STAGE_NAME} Completed <<<<<<")
except Exception as e:
    logger.exception(e)
    raise


STAGE_NAME = "Data Validation"

try:
    logger.info(f">>>>> Stage {STAGE_NAME} started <<<<<<")
    data_validation = DataValidationPipeline()
    data_validation.main()
    logger.info(f">>>>> Stage {STAGE_NAME} Completed <<<<<<")
except Exception as e:
    logger.exception(e)
    raise