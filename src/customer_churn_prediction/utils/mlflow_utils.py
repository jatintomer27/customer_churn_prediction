"""
Contains utility functions regarding the mlflow.
"""
from dotenv import load_dotenv
import mlflow
import os
import yaml

from customer_churn_prediction import logger

def setup_mlflow(config_path: str):
    """
    Reads credentials from .env and config from YAML,
    builds full tracking URI, and sets MLflow context.
    """
    load_dotenv()  # load username/password

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    mlflow_cfg = config.get("mlflow", {})

    username = os.getenv("MLFLOW_TRACKING_USERNAME")
    token = os.getenv("MLFLOW_TRACKING_PASSWORD")
    base_uri = mlflow_cfg.get("tracking_uri_base")

    # Build full DagsHub MLflow endpoint with credentials
    full_uri = f"https://{username}:{token}@{base_uri.removeprefix('https://')}"
    mlflow.set_tracking_uri(full_uri)
    mlflow.set_experiment(mlflow_cfg.get("experiment_name"))

    logger.info(f"MLflow connected to: {base_uri}")
    return mlflow
