from house_project.Config.config_entity import DataValidationCOnfig
from house_project import logging
import pandas as pd 
from house_project.Utility.common import Create_Dir,Read_Yaml,check_csv_occur
import os 
import csv

class DataValidation:
    def __init__(self):
        self.data_validation = DataValidationCOnfig()
        self.schema = Read_Yaml(self.data_validation.schema_path)['COLUMNS']
        
        Create_Dir(self.data_validation.root_dir)
        
          
    def Check_Columns_validation(self):
        csv_file = check_csv_occur(self.data_validation.ingest_data_root)
        data = pd.read_csv(os.path.join(self.data_validation.ingest_data_root,csv_file))
        logging.info("Load the Data through Pandas")
        all_columns = list(data.columns)
        schema_columns = self.schema.keys()
        try:
            miss_columns = [col for col in schema_columns if col not in all_columns]
            if miss_columns:
                Validation_Status =False
                with open(self.data_validation.status_path,'w') as f:
                    f.write(f"Validation_Status :{Validation_Status}")
                    logging.info(f'Validation_Status : {Validation_Status}')
                    logging.info(f"Missing_Columns :{miss_columns}")
            else:
                Validation_Status = True
                with open (self.data_validation.status_path,'w') as f:
                    f.write(f"Validation_Status : {Validation_Status}")
                    logging.info(f'Validation_Status : {Validation_Status}') 
                    
        except Exception as e:
            raise e 
                               
        
        
           
        
        