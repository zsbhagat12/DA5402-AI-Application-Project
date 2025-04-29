from flask import Flask, render_template, request
import numpy as np
from tensorflow.keras.models import load_model
import joblib
import os
from pathlib import Path

app = Flask(__name__)
# Load model from parent directory
model_path = Path(__file__).parent.parent / 'model/wine_quality_ann.h5'
scaler_path = Path(__file__).parent.parent / 'model/scaler.pkl'

# Load model and scaler
try:
    model = load_model(model_path)
    scaler = joblib.load(scaler_path)
except Exception as e:
    raise RuntimeError("Model/scaler not found. Run server.py first") from e

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get form data
            features = [
                float(request.form['fixed_acidity']),
                float(request.form['volatile_acidity']),
                float(request.form['citric_acid']),
                float(request.form['residual_sugar']),
                float(request.form['chlorides']),
                float(request.form['free_sulfur_dioxide']),
                float(request.form['total_sulfur_dioxide']),
                float(request.form['density']),
                float(request.form['pH']),
                float(request.form['sulphates']),
                float(request.form['alcohol'])
            ]
            
            # Preprocess
            scaled_features = scaler.transform(np.array([features]))
            
            # Predict
            prediction = model.predict(scaled_features)[0][0]
            response = max(0, min(10, round(prediction)))
            
            return render_template("index.html", response=response)
            
        except Exception as e:
            return render_template("404.html", error=str(e))
            
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
