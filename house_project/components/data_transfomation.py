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
        
        
        preprocess = ColumnTransformer([
            ('power_pipleine',PowerTransformer(method='yeo-johnson'),power_col),
            ('num_pipeline',StandardScaler(),num_columns),
            ('cat_pipeline',OneHotEncoder(handle_unknown='ignore',sparse_output=False),cat_columns)
            
        ])
        return preprocess
    
    def apply_feature_engineering_and_data_transfomation(self):
        try:
  
            csv_file = check_csv_occur(self.data_transform.ingest_data_root)
            data = pd.read_csv(Path(os.path.join(self.data_transform.ingest_data_root, csv_file)))
            
   
            drop_columns = self.schema.get("drop_columns", [])
            data = data.drop(columns=drop_columns, axis=1)
          
            data = self.data_clean.clean_bath(data)
            data = self.data_clean.clean_bed(data)
            data = self.data_clean.clean_land_size(data)
            data = self.data_clean.clean_house_size(data)
            data = self.data_clean.clean_price(data)
            data = self.data_clean.Geo_Address(data)
            logging.info("Data cleaning completed.")
            
   
            outlier_columns = self.schema.get('outlier', [])
            data = self.data_clean.remove_outliers_iqr(data=data, columns=outlier_columns)
            logging.info('Outlier removal completed.')
            logging.info(f"Shape after outlier removal: {data.shape}")
            
            data = data.dropna()  
            if data.empty:
                raise ValueError("Data is empty after dropping missing values. Check the dataset.")
            
           
            preprocess_obj = self.preprocess_step()
            
          
            train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
            logging.info(f"Shape of train_data: {train_data.shape}")
            logging.info(f"Shape of test_data: {test_data.shape}")
            
  
            target_col = self.schema.get('TARGET', [])
            if not target_col:
                raise ValueError("Target column not found in the schema.")
            
            train_data_input_feature = train_data.drop(columns=target_col, axis=1)
            train_data_target_feature = train_data[target_col]
            
            test_data_input_feature = test_data.drop(columns=target_col, axis=1)
            test_data_target_feature = test_data[target_col]
            
    
            train_pre = preprocess_obj.fit_transform(train_data_input_feature)
            test_pre = preprocess_obj.transform(test_data_input_feature)
            
  
            logging.info(f"Shape of train_pre: {train_pre.shape}")
            logging.info(f"Shape of train_data_target_feature: {train_data_target_feature.shape}")
            
            logging.info(f"Shape of test_pre: {test_pre.shape}")
            logging.info(f"Shape of train_data_target_feature: {test_data_target_feature.shape}")
            
            # Convert sparse matrix to dense array if necessary
            #if hasattr(train_pre, "toarray"):
                #train_pre = train_pre.toarray()
                #test_pre = test_pre.toarray()

            
            train_arr = np.c_[train_pre, np.array(train_data_target_feature)]
            test_arr = np.c_[test_pre, np.array(test_data_target_feature)]
            
            
            np.save(os.path.join(self.data_transform.root_dir, 'train.npy'), train_arr)
            np.save(os.path.join(self.data_transform.root_dir, 'test.npy'), test_arr)
            logging.info("Feature engineering and preprocessing completed.")
            logging.info("Train and test .npy files saved successfully.")
           
            joblib.dump(preprocess_obj, os.path.join(self.data_transform.root_dir, self.data_transform.preprocess_file))
            logging.info("Preprocessing object saved as preprocess.pkl.")
            
        except Exception as e:
            logging.error(f"Error in apply_feature_engineering_and_data_transfomation: {e}")
            raise e
            
            
            
            
        
        
        
