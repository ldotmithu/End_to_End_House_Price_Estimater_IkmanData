from house_project.components.data_ingestion import DataIngestion
from house_project.components.data_validation import DataValidation
from house_project.components.data_transfomation import DataTransfomation
from house_project.Config.config_entity import DataTransfomationConfig
from house_project.components.model_trainer import ModelTrainer
from house_project.components.model_evaluation import ModelEvaluation
from house_project import logging


class DataIngestionPipeline:
    def __init__(self):
        pass
    
    def Main(self):
        data_ingestion = DataIngestion()
        data_ingestion.Download_ZipFile()
        data_ingestion.Unzip_operation()

class DataValidationPipeline:
    def __init__(self):
        pass
    def Main(self):
        data_validation = DataValidation()
        data_validation.Check_Columns_validation()  
        
class DataTransformPipeline:
    def __init__(self):
        self.data_transform = DataTransfomationConfig()
    
    def Main(self):
        with open(self.data_transform.status_path,'r') as f:
                status = f.read().split(":")[-1].strip()
                
                if status != "True":
                    logging.error('Data Validation Sataus is False')
                       
                else:   
                    try:
                        data_transform = DataTransfomation()
                        data_transform.apply_feature_engineering_and_data_transfomation()
                    except Exception as e:
                        raise e      
                        
         
         
class ModelTrainerPipeline:
    def __init__(self):
        pass
    def Main(self):
        model_trainer = ModelTrainer()
        model_trainer.Model_building()         
        
class ModelEvaluationPipeline:
    def __init__(self):
        pass
    def Main(self):
        model_evaluation = ModelEvaluation()
        model_evaluation.apply_model_test_data()               