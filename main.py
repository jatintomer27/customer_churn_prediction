from customer_churn_prediction import logger
from customer_churn_prediction.pipeline.stage_01_data_ingestion import (
    DataIngestionPipeline
)
from customer_churn_prediction.pipeline.stage_02_data_validation import (
    DataValidationPipeline
)
from customer_churn_prediction.pipeline.stage_03_data_transformation import (
    DataTransformationPipeline
)
from customer_churn_prediction.pipeline.stage_04_model_training import (
    ModelTrainingPipeline
)
from customer_churn_prediction.pipeline.stage_05_model_evaluation import (
    ModelEvaluationPipeline
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


STAGE_NAME = "Data Transformation"

try:
    logger.info(f">>>>> Stage {STAGE_NAME} started <<<<<<")
    data_validation = DataTransformationPipeline()
    data_validation.main()
    logger.info(f">>>>> Stage {STAGE_NAME} Completed <<<<<<")
except Exception as e:
    logger.exception(e)
    raise


STAGE_NAME = "Model Training and Selection"

try:
    logger.info(f">>>>> Stage {STAGE_NAME} started <<<<<<")
    model_training = ModelTrainingPipeline()
    model_training.main()
    logger.info(f">>>>> Stage {STAGE_NAME} Completed <<<<<<")
except Exception as e:
    logger.exception(e)
    raise


STAGE_NAME = "Model Evaluation"

try:
    logger.info(f">>>>> Stage {STAGE_NAME} started <<<<<<")
    model_evaluation = ModelEvaluationPipeline()
    model_evaluation.main()
    logger.info(f">>>>> Stage {STAGE_NAME} Completed <<<<<<")
except Exception as e:
    logger.exception(e)
    raise
