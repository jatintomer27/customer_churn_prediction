"""
Module handle and execute model evaluation pipeline
"""

from customer_churn_prediction import logger
from customer_churn_prediction.config.configuration import ConfigurationManager
from customer_churn_prediction.components.model_evaluation import ModelEvaluation

class ModelEvaluationPipeline:
    """
    Handle model evaluation pipeline
    """
    def __init__(self):
        pass

    def main(self):
        """
        Execute model evaluation pipeline
        """
        try:
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(model_evaluation_config)
            model_evaluation.save_result()
        except Exception:
            logger.exception(
                f"Exception occured while executing the model evaluation pipeline")
            raise