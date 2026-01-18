"""
Model Trainer component to trains multiple models with different hyperparameters
and selects the best one based on evaluation metrics.
"""


import importlib
import itertools
import joblib
import numpy as np
import os
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score
from urllib.parse import urlparse

from customer_churn_prediction import logger
from customer_churn_prediction.constants import CONFIG_FILE_PATH
from customer_churn_prediction.entity.config_entity import ModelTrainerConfig
from customer_churn_prediction.utils.mlflow_utils import setup_mlflow

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        self.mlflow = setup_mlflow(CONFIG_FILE_PATH)

    def _get_class_from_string(self, full_class_path):
        """
        Dynamically import model class.
        """
        module_name, class_name = full_class_path.rsplit('.',1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    
    def load_train_test_data_and_split(self):
        """
        Load and split the training and testing datasets into features and target variables.
        """
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        train_x = train_data.drop([self.config.target_column],axis=1)
        train_y = train_data[self.config.target_column]

        test_x = test_data.drop([self.config.target_column],axis=1)
        test_y = test_data[self.config.target_column]

        return train_x, train_y, test_x, test_y

    def train_and_select_best_model(self):
        """
        Train specified models, log each experiment to MLflow,
        and return the best model.
        """
        best_model = None
        best_score = - np.inf
        best_model_name = None
        train_x, train_y, test_x, test_y = self.load_train_test_split()
        for model_name, model_config in self.config.params.models.items():
            model_class = self._get_class_from_string(model_config.model_class)
            param_grid = model_config.params

            keys, values = zip(*param_grid.items())
            for combination in itertools.product(*values):
                params_dict = dict(zip(keys, combination))
                model = model_class(**params_dict)

                # Start MLflow run for each model-param combo
                with self.mlflow.start_run(run_name=f"{model_name}"):
                    self.mlflow.log_params(params_dict)

                    model.fit(train_x,train_y)
                    y_pred = model.predict(test_x)

                    acc = accuracy_score(test_y, y_pred)
                    f1 = f1_score(test_y, y_pred)
                    roc_auc = roc_auc_score(test_y, y_pred)
                    recall = recall_score(test_y, y_pred) # As our False Negative is more important in this usecase
        

                    self.mlflow.log_metric("accuracy",acc)
                    self.mlflow.log_metric("f1_score",f1)
                    self.mlflow.log_metric("roc_auc", roc_auc)
                    self.mlflow.log_metric("recall", recall)

                    tracking_scheme = urlparse(self.mlflow.get_tracking_uri()).scheme

                    if tracking_scheme != "file":
                        self.mlflow.sklearn.log_model(
                            model,
                            artifact_path=model_name,
                            registered_model_name=model_name
                        )
                    else:
                        self.mlflow.sklearn.log_model(model, artifact_path=model_name)

                logger.info(f"{model_name} | Params: {params_dict} | F1: {f1:.4f}")

                if recall > best_score:
                    best_score = recall
                    best_model = model
                    best_model_name = model_name
        logger.info(f"Best model: {best_model_name} with F1-score={best_score:.4f}")
        joblib.dump(best_model, os.path.join(self.config.root_dir,self.config.model_name))
        logger.info(f"Best model saved at: {os.path.join(self.config.root_dir,self.config.model_name)}")
        return best_model, best_model_name, best_score


    
