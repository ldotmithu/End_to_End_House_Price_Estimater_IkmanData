from house_project.Config.config_entity import ModelEvaluationConfig
from house_project import logging
from house_project.Utility.common import Create_Dir,save_object
import joblib
import numpy as np 
from sklearn.metrics import r2_score
import os 


class ModelEvaluation:
    def __init__(self):
        self.model_evaluation = ModelEvaluationConfig()
        
        Create_Dir(self.model_evaluation.root_dir)
        
    def apply_model_test_data(self):
        test_data =  np.load(self.model_evaluation.test_data_path)
        
        test_data_input_features = test_data[:,:-1]
        test_data_target_feature = test_data[:,-1]  
        
        model = joblib.load(self.model_evaluation.model_path)
        prd = model.predict(test_data_input_features)
        metrics=r2_score(test_data_target_feature,prd)
        save_object(os.path.join(self.model_evaluation.root_dir,self.model_evaluation.metrics_name),metrics)
        logging.info(f"{r2_score(test_data_target_feature,prd)}")