"""
Module handle and execute model training pipeline.
"""

from customer_churn_prediction import logger
from customer_churn_prediction.config.configuration import ConfigurationManager
from customer_churn_prediction.components.model_trainer import ModelTrainer

class ModelTrainingPipeline:
    """
    Handle model training and selection pipeline 
    """
    def __init__(self):
        pass

    def main(self):
        """
        Execute model training and selection pipeline
        """
        try:
            config = ConfigurationManager()
            model_selection_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(model_selection_config)
            model_trainer.train_and_select_best_model()
        except Exception:
            logger.exception(
                f"Exception occured while executing the model training and selection pipeline")
            raise