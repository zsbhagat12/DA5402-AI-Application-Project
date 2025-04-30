from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model
import joblib
import numpy as np
import argparse
from pathlib import Path
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import sys
from tensorflow.keras import losses
# Add the logs directory to sys.path
if str(Path(__file__).parent.parent / 'logs') not in sys.path:
    sys.path.append(str(Path(__file__).parent.parent / "logs"))

from logging_utils import setup_logger
logger = setup_logger('server', 'server.log')

app = Flask(__name__)
CORS(app)  # Add this line

model = None
scaler = None

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/static/swagger.json'  # Path to your Swagger spec
PROJECT_ROOT = Path(__file__).parent.parent

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Wine Quality Prediction API"}
)

app.register_blueprint(swaggerui_blueprint)
app.logger.handlers = logger.handlers

def load_or_train_model(force_retrain=False):
    global model, scaler
    model_path = PROJECT_ROOT / 'model/wine_quality_ann.keras'
    scaler_path = PROJECT_ROOT / 'model/scaler.pkl'
    print(f"Model path: {model_path}")
    print(f"Scaler path: {scaler_path}")
    logger.info(f"Model path: {model_path}")
    logger.info(f"Scaler path: {scaler_path}")
    if force_retrain:
        print("Force retraining requested...")
        logger.warning("Force retraining requested...")
        if str(PROJECT_ROOT/ 'model') not in sys.path:
            sys.path.append(str(PROJECT_ROOT/ 'model'))
        # print(sys.path)
        import train
        train.train_and_save_model()

    try:
        model = load_model(
            model_path,
            compile=True,
            custom_objects={'MeanSquaredError': losses.MeanSquaredError}
        )
        scaler = joblib.load(scaler_path)
        print("Model and scaler loaded successfully")
        logger.info("Model and scaler loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        logger.error(f"Error loading model: {e}")
        if not force_retrain:  # Prevent infinite loop
            if str(PROJECT_ROOT/ 'model') not in sys.path:
                sys.path.append(str(PROJECT_ROOT/ 'model'))
            # print(sys.path)
            import train
            train.train_and_save_model()
            model = load_model(
                model_path,
                compile=True,
                custom_objects={'MeanSquaredError': losses.MeanSquaredError}
            )
            scaler = joblib.load(scaler_path)
        else:
            raise RuntimeError("Failed to load model after forced retraining") from e

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        feature_order = [
            'fixed acidity', 'volatile acidity', 'citric acid',
            'residual sugar', 'chlorides', 'free sulfur dioxide',
            'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol'
        ]
        
        # Validate all required fields
        missing = [field for field in feature_order if field not in data]
        if missing:
            return jsonify({
                'error': f'Missing fields: {", ".join(missing)}',
                'status': 'error'
            }), 400
            
        features = [data[field] for field in feature_order]
        
        scaled = scaler.transform(np.array([features]))
        prediction = model.predict(scaled)[0][0]
        return jsonify({
            'prediction': max(0, min(10, round(prediction))),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400
    
@app.route('/retrain', methods=['POST'])
def trigger_retraining():
    try:
        print("Retraining triggered...")
        load_or_train_model(force_retrain=True)
        return jsonify({
            "status": "success",
            "message": "Model retrained successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5001)
    parser.add_argument('--retrain', action='store_true', 
                       help='Force model retraining regardless of existing files')
    args = parser.parse_args()
    
    load_or_train_model(force_retrain=args.retrain)
    
    app.run(host=args.host, port=args.port, debug=True)
