from flask import Flask, render_template, request, jsonify
import requests
import sys
from pathlib import Path

# Add the logs directory to sys.path
if str(Path(__file__).parent.parent / 'logs') not in sys.path:
    sys.path.append(str(Path(__file__).parent.parent / "logs"))
from logging_utils import setup_logger

logger = setup_logger('app', 'app.log')

app = Flask(__name__)

# URL of the model server's predict endpoint
MODEL_SERVER_URL = "http://localhost:5001/predict"  # Change if hosted elsewhere
MODEL_SERVER_RETRAIN_URL = "http://localhost:5001/retrain"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Create dictionary with server's expected parameter names
            features = {
                'fixed acidity': float(request.form['fixed_acidity']),
                'volatile acidity': float(request.form['volatile_acidity']),
                'citric acid': float(request.form['citric_acid']),
                'residual sugar': float(request.form['residual_sugar']),
                'chlorides': float(request.form['chlorides']),
                'free sulfur dioxide': float(request.form['free_sulfur_dioxide']),
                'total sulfur dioxide': float(request.form['total_sulfur_dioxide']),
                'density': float(request.form['density']),
                'pH': float(request.form['pH']),
                'sulphates': float(request.form['sulphates']),
                'alcohol': float(request.form['alcohol'])
            }

            # Send POST request to model server
            response = requests.post(
                MODEL_SERVER_URL,
                json=features,  # Send as direct JSON object
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    return render_template("index.html", response=result["prediction"])
                else:
                    
                    return render_template("404.html", error=result.get("error", "Unknown error"))
            else:
                logger.error(f"Model server error: {response.text}")
                return render_template("404.html", error=f"Model server error: {response.text}")

        except Exception as e:
            return render_template("404.html", error=str(e))

    return render_template("index.html")

@app.route("/retrain", methods=["POST"])
def retrain():
    try:
        response = requests.post(MODEL_SERVER_RETRAIN_URL, timeout=120)
        return jsonify({
            "status": "success" if response.ok else "error",
            "message": response.json().get("message", "Retraining completed")
        }), response.status_code
    except Exception as e:
        logger.error(f"Error during retraining: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
if __name__ == "__main__":
    logger.info("App started")
    app.run(host='0.0.0.0', port=5000, debug=True)
