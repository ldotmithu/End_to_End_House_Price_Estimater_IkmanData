import pandas as pd 
import numpy as np 
from house_project.Utility.common import check_csv_occur
from house_project import logging


class FeatureEngineering:
    
    def __init__(self):
        pass
    
    def clean_price(self,data):
        data["Price"] = data['Price'].apply(lambda x: x.split(" ")[-1])
        data['Price'] = data['Price'].str.replace(',', '', regex=True)
        data.dropna(subset=['Price'], inplace=True)
        data['Price'] = pd.to_numeric(data['Price'])
        return data
    
    def clean_bath(self,data):
        data["Baths"] = data['Baths'].apply(lambda x: x.replace('10+','10'))
        data.dropna(subset=['Baths'], inplace=True)
        data['Baths'] = pd.to_numeric(data['Baths'])
        return data
    
    def clean_bed(self,data):
        data["Beds"] = data['Beds'].apply(lambda x: x.replace('10+','10'))
        data.dropna(subset=['Beds'], inplace=True)
        data['Beds'] = pd.to_numeric(data['Beds'])
        return data 
    
    def clean_land_size(self,data):
        def check_land_size(x):
            try:
                return float(x)
            except:
                return None
        data["Land size"] = data['Land size'].str.replace('perches', '', regex=True)
        data['Land size'] = data['Land size'].apply(check_land_size)
        logging.info(f"Shape before dropna: {data.shape}")
        data.dropna(subset=['Land size'], inplace=True)
        data['Land size'] = pd.to_numeric(data['Land size'])
        logging.info(f"Shape after dropna: {data.shape}")
        return data
        
    def clean_house_size(self,data):
        data['House size'] = data['House size'].apply(lambda x: x.split(" ")[0])
        data["House size"] = data['House size'].str.replace(',', '', regex=True)
        data.dropna(subset=['House size'], inplace=True)
        data['House size'] = pd.to_numeric(data['House size'])
        
        return data  
    
    def Geo_Address(self,data):
        location_status = data['Geo_Address'].value_counts()
        location_status_less_5 = location_status[location_status<5]
        data['Geo_Address'] = data['Geo_Address'].apply(lambda x: 'Other' if x in location_status_less_5 else x)
        data.dropna(subset=['Geo_Address'], inplace=True)
        return data
    
    def remove_outliers_iqr(self,data,columns,multiplier =1.5):
        try:
            if isinstance(columns,str):
                columns = [columns]
            for col in columns:
                Q1 = np.percentile(data[col],25,method='midpoint')    
                Q3 = np.percentile(data[col],75,method='midpoint')   
                IQR = Q3 -Q1
                lower_bound = Q1 - (multiplier *IQR) 
                upper_bound = Q3 + (multiplier *IQR)
                data = data[(data[col] > lower_bound) & (data[col] < upper_bound)] 
                logging.info(f'Remove the outliers from {columns}')
            return data
        
                    
        except Exception as e:
            raise e     
    
        