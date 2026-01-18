"""
Module handles the prediction pipeline.
"""
from customer_churn_prediction import logger
from customer_churn_prediction.config.configuration import ConfigurationManager
from customer_churn_prediction.components.model_prediction import ModelPrediction

class PredictionPipeline:
    """
    Handle preprocessing of the data and prediction.
    """

    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_prediction_config = config.get_prediction_config()
            model_prediction = ModelPrediction(data_prediction_config)
        except Exception:
            logger.exception(
                f"Exception occured while executing the model evaluation pipeline")
            raise
        else:
            return model_prediction

    def predict(self,data):
        try:
            model = self.main()
            status, prediction, msg = model.predict(data)
        except Exception:
            logger.exception(
                f"Exception occured while predicting")
        return status, prediction, msg
             

if __name__ == "__main__":
    PredictionPipeline().predict()