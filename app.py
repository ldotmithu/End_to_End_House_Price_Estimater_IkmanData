from flask import Flask, render_template, request
import os
from house_project.Pipeline.prediction_pipeline import Predication_Pipeline
import pandas as pd 


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/train', methods=['GET'])
def training():
    os.system('python main.py')
    return "training done"

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get form data
            input_data = [request.form.get('Baths'), request.form.get('Land size'), request.form.get('Beds'), request.form.get('House size'), request.form.get('Geo_Address')]
            columns = ['Baths', 'Land size', 'Beds', 'House size', 'Geo_Address']
            input_df = pd.DataFrame([input_data], columns=columns)

            pipeline = Predication_Pipeline()
            preprocess_data = pipeline.transform(input_df)
            prediction = pipeline.prediction(preprocess_data)

            # Return the prediction
            return render_template('predict.html', prediction=round(prediction[0],2))
        except Exception as e:
            return render_template('error.html', error_message=str(e))
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
