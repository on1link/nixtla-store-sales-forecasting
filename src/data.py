import pandas as pd
from pathlib import Path
import mlflow
from mlflow.client import MlflowClient
import os
import kagglehub

experiment_name: str = os.getenv("experiment_name")
competition_name: str = os.getenv("competition_name")

project_root = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()

db_path = project_root / "mlflow.db"
artifact_path = project_root / "mlartifacts"

# Set tracking URI to SQLite
mlflow.set_tracking_uri(f"sqlite:///{db_path.as_posix()}")

# Create experiment with explicit artifact destination
client = MlflowClient()

experiment = client.get_experiment_by_name(experiment_name)
if experiment is None:
    client.create_experiment(
        name=experiment_name,
        artifact_location=artifact_path.as_uri()
    )

mlflow.set_experiment(experiment_name)

kagglehub.login()
path = kagglehub.competition_download(competition_name)

def data_ingestion(path):
    train = pd.read_csv("".join([path, '/train.csv']), parse_dates=['date'])
    test = pd.read_csv("".join([path, '/test.csv']), parse_dates=['date'])
    return train, test

