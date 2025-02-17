from dataclasses import dataclass
import os 
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir:Path = "artifacts/data_ingestion"
    URL:str = "https://github.com/ldotmithu/Dataset/raw/refs/heads/main/house_prices.zip"
    local_data_path:Path = "artifacts/data_ingestion/data.zip"
    unzip_dir:Path = "artifacts/data_ingestion"
    
@dataclass
class DataValidationCOnfig:
    root_dir:Path = 'artifacts/data_validation'
    ingest_data_root:Path ="artifacts/data_ingestion"
    status_path:Path ="artifacts/data_validation/status.txt"
    schema_path:dict = "schema.yaml"
        
@dataclass
class DataTransfomationConfig:
    root_dir:Path = 'artifacts/data_transfomation'
    ingest_data_root:Path ="artifacts/data_ingestion"
    preprocess_file:Path = "preprocess.pkl"
    status_path:Path ="artifacts\data_validation\status.txt"
    schema_path:dict = "schema.yaml"
    
@dataclass
class ModelTrainerConfig:
    root_dir:Path =  'artifacts/model_trainer'
    train_path:Path = "artifacts/data_transfomation/train.npy"
    model_name =str = "model.pkl" 
    params_path:Path ="params.yaml"
    
    
@dataclass
class ModelEvaluationConfig:
    root_dir :Path = "artifacts/model_evaluation"
    model_path:Path ='artifacts/model_trainer/model.pkl'
    test_data_path:Path ="artifacts/data_transfomation/test.npy"
    metrics_name:str ="metrics.json"
        
    
    
            
    