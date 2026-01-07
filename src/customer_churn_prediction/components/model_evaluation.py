"""
Model Evaluation component evaluate the model based on the multiple evaluation metrics
"""

import pandas as pd
from pathlib import Path
import joblib

from sklearn.metrics import ( accuracy_score, auc, fbeta_score, precision_score, recall_score, roc_auc_score )

from customer_churn_prediction import logger
from customer_churn_prediction.utils.common import save_json
from customer_churn_prediction.entity.config_entity import ModelEvaluationConfig

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        """
        Calculate the evaluation metrics of the selected model

        Params:
            actual (str): Actual value of the record.
            pred (str): Predicted value of the record

        Returns:
            pass
        """
        accuracy = accuracy_score(actual, pred)
        precision = precision_score(actual,pred)
        recall = recall_score(actual,pred)
        fbeta = fbeta_score(actual, pred)
        roc_auc = roc_auc_score(actual, pred)
        auc_area = auc(actual, pred)
        logger.info(f"Metrics of the selected model is {[accuracy, precision, recall, fbeta, roc_auc, auc_area]}")
        return accuracy, precision, recall, fbeta, roc_auc, auc_area
    
    def save_result(self):
        """
        Save the Evaluation mertics at the specified path in json.
        """
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)
        test_x = test_data.drop([self.config.target_column],axis=1)
        test_y = test_data[[self.config.target_column]]
        y_pred = model.predict(test_x)
        accuracy, precision, recall, fbeta, roc_auc, auc_area = self.eval_metrics(test_y, y_pred)
        scores = {
            'accuracy':accuracy,
            'precision':precision, 
            'recall': recall, 
            'fbeta':fbeta, 
            'roc_auc':roc_auc, 
            'auc_area': auc_area
        }
        save_json(path = Path(self.config.metric_file_name), data=scores)
        logger.info(f"Evaluation metrics of the selected model are saved at the path {Path(self.config.metric_file_name)}")
