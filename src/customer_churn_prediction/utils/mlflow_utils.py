"""
Contains utility functions regarding the mlflow.
"""

import os
import yaml
import mlflow
from dotenv import load_dotenv
from customer_churn_prediction import logger


def setup_mlflow(config_path: str):
    """
    Loads MLflow configuration and credentials,
    sets tracking URI and experiment safely.
    """
    load_dotenv()

    # Load YAML config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    mlflow_cfg = config.get("mlflow", {})

    tracking_uri = mlflow_cfg.get("tracking_uri_base")
    experiment_name = mlflow_cfg.get("experiment_name")

    if not tracking_uri:
        raise ValueError("MLflow tracking_uri not found in config")
    if not experiment_name:
        raise ValueError("MLflow experiment_name not found in config")

    # Credentials via env (MLflow-native way)
    if not os.getenv("MLFLOW_TRACKING_USERNAME"):
        raise EnvironmentError("MLFLOW_TRACKING_USERNAME not set")
    if not os.getenv("MLFLOW_TRACKING_PASSWORD"):
        raise EnvironmentError("MLFLOW_TRACKING_PASSWORD not set")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    logger.info(f"MLflow tracking URI set to: {tracking_uri}")
    logger.info(f"MLflow experiment set to: {experiment_name}")

    return mlflow



"""
Qus >> How MLflow actually authenticates ?

MLflow supports Basic Auth via env vars:

MLFLOW_TRACKING_USERNAME
MLFLOW_TRACKING_PASSWORD

When you do: mlflow.set_tracking_uri("https://dagshub.com/owner/repo.mlflow")

MLflow internally sends: Authorization: Basic base64(username:password)

"""


"""
Here credentials are NOT in the URL.

They are passed implicitly via environment variables, which MLflow picks up internally.

MLflow internally reads these and sends them as HTTP auth headers.

"""
