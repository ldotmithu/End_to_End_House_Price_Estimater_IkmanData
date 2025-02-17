from house_project.Config.config_entity import DataTransfomationConfig
from sklearn.model_selection import train_test_split
import pandas as pd 
import numpy as np 
from house_project import logging
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder,PowerTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from house_project.Utility.common import *
from house_project.Utility.feature_engineering import FeatureEngineering
import os 
from pathlib import Path
import joblib

class DataTransfomation:
    def __init__(self):
        self.data_transform = DataTransfomationConfig()
        self.schema = Read_Yaml(self.data_transform.schema_path)
        self.data_clean = FeatureEngineering()
        
        Create_Dir(self.data_transform.root_dir)
            
    def preprocess_step(self):
        
        num_columns = self.schema.get('scaler',[])
        cat_columns = self.schema.get('one_hot',[])
        power_col = self.schema.get('power',[])
        
        num_pipleine = Pipeline([
            ('scaler',StandardScaler())
        ])    
        
        cat_pipeline = Pipeline([
            ('one_hot',OneHotEncoder(handle_unknown='ignore',drop=None,sparse_output=False))
        ])
        
        power_pipleine=Pipeline([
            ('power',PowerTransformer(method='yeo-johnson'))
        ])
        
        preprocess = ColumnTransformer([
            ('power_pipleine',power_pipleine,power_col),
            ('num_pipeline',num_pipleine,num_columns),
            ('cat_pipeline',cat_pipeline,cat_columns)
            
        ])
        return preprocess
    
    def apply_feature_engineering_and_data_transfomation(self):
        try:
            csv_file = check_csv_occur(self.data_transform.ingest_data_root)
            
            data = pd.read_csv(Path(os.path.join(self.data_transform.ingest_data_root,csv_file)))
            
            drop_columns = self.schema.get("drop_columns",[])
            
            data = data.drop(columns=drop_columns,axis=1)
            
            data = self.data_clean.clean_price(data)
            data = self.data_clean.clean_bath(data)
            data = self.data_clean.clean_bed(data)
            data = self.data_clean.clean_land_size(data)
            data = self.data_clean.clean_house_size(data)
            logging.info("data cleaning Completed ")
            
            outlier_columns = self.schema.get('outlier',[])
            data = self.data_clean.remove_outliers_iqr(data=data,columns=outlier_columns)
            logging.info('Outlier removel Completed')
            logging.info(f"Shape after outlier: {data.shape}")
            
            preprocess_obj = self.preprocess_step()
            
            
            train_data,test_data = train_test_split(data,test_size=0.2,random_state=42)
            target_col = self.schema.get('TARGET',[])
            
            train_data_input_feature = train_data.drop(columns = target_col,axis = 1)
            train_data_target_feature = train_data[target_col]
            
            test_data_input_feature = test_data.drop(columns = target_col,axis = 1)
            test_data_target_feature = test_data[target_col]
            
            train_pre = preprocess_obj.fit_transform(train_data_input_feature)
            test_pre = preprocess_obj.transform(test_data_input_feature)
            
            train_arr = np.c_[train_pre, np.array(train_data_target_feature)]
            test_arr = np.c_[test_pre, np.array(test_data_target_feature)]
            
            np.save(os.path.join(self.data_transform.root_dir,'train.npy'),train_arr)
            np.save(os.path.join(self.data_transform.root_dir,'test.npy'),test_arr)
            logging.info("Feature engineering and preprocessing completed.")
            logging.info("train and test npy save succesfully ")
            
            joblib.dump(preprocess_obj,os.path.join(self.data_transform.root_dir,self.data_transform.preprocess_file))
            logging.info("save the preprocess.pkl")
            
            
        except Exception as e:
            raise e     
        
        
        
        
        
        
        
