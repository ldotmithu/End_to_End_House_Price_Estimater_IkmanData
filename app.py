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
            Baths = int(request.form.get('Baths'))
            Land_size = float(request.form.get('Land size'))
            Beds = int(request.form.get('Beds'))
            House_size = float(request.form.get('House size'))
            Location = request.form.get('Location')
            
            if not (Baths and Land_size and Beds and House_size and Location):
                raise ValueError("All fields are required!")
            data = {
            'Baths': [Baths],
            'Land size': [Land_size],
            'Beds': [Beds],
            'House size': [House_size],
            'Location': [Location]
            }
            data_df = pd.DataFrame(data)

            pipeline = Predication_Pipeline()
            preprocess_data = pipeline.transform(data_df)
            prediction = pipeline.prediction(preprocess_data)

            # Return the prediction
            return render_template('predict.html', prediction=round(prediction[0],2))
        except Exception as e:
            return render_template('error.html', error_message=str(e))
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
