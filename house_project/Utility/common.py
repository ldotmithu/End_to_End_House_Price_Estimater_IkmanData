from house_project import logging
from pathlib import Path
import os 
import yaml,json
from yaml import safe_load
import numpy as np 

def Create_Dir(file_path):
    try:
        os.makedirs(file_path,exist_ok=True)
        logging.info(f"{file_path} Created Succesfully")
    except:
        logging.info("Invalid Dir Path")    
        
        
def Read_Yaml(file_path):
    try:
        with open(file_path,'r') as f:
            file = yaml.safe_load(f)
            logging.info(f"Read the {file_path} Yaml file")
            return file
    except yaml.YAMLError as e:
        logging.error("YAML file is empty")
        raise e 
    
def check_csv_occur(dir_path):
    files = os.listdir(dir_path)
    csv_file = [file for file in files if file.endswith(".csv")] 
    if len(csv_file) == 1:
            return csv_file[0]
    elif len(csv_file) == 0:
        logging.error("Don't have any csv files")
        return None
    else:
        logging.error("Multipule csv files are there")
        return None   
    
def save_object(file_path,obj):
    try:
        with open(file_path,'w') as f:
            metrics =json.dump(obj,f)      
            logging.info(f'save the {file_path}')
            return metrics
    except Exception as e:
        raise e         
    
    
 
        