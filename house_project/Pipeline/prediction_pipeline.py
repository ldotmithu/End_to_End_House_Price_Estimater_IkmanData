import joblib
from pathlib import Path

model_path = Path("artifacts\model_trainer\model.pkl")
preprocess_path = Path("artifacts\data_transfomation\preprocess.pkl")

class Predication_Pipeline:
    def __init__(self):
        # Load the model and preprocessing pipeline
        self.model = joblib.load(model_path)
        self.preprocessing_pipeline = joblib.load(preprocess_path)  # Renamed to avoid conflict
        
    def transform(self, data):
        """Preprocess the data using the loaded preprocessing pipeline"""
        transformed_data = self.preprocessing_pipeline.transform(data)
        return transformed_data
    
    def prediction(self, data):
        """Predict the outcome using the loaded model"""
        prediction = self.model.predict(data)
        return prediction
