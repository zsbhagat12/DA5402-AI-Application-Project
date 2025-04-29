from tensorflow.keras.models import load_model
import joblib
import numpy as np
import argparse
from pathlib import Path

def load_or_train_model():
    model_path = Path(__file__).parent.parent / 'model/wine_quality_ann.h5'
    scaler_path = Path(__file__).parent.parent / 'model/scaler.pkl'
    
    try:
        model = load_model(model_path)
        scaler = joblib.load(scaler_path)
    except:
        # Import from model directory
        import sys
        sys.path.append(str(Path(__file__).parent.parent / 'model'))
        import train
        train.train_and_save_model()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true', help='Force retrain model')
    args = parser.parse_args()
    
    if args.train:
        import train
        train.train_and_save_model()
    else:
        model, scaler = load_or_train_model()
