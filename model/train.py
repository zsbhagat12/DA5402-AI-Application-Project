# model/train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib
import numpy as np
from pathlib import Path
import mlflow
import mlflow.keras
from tensorflow.keras import losses

PROJECT_ROOT = Path(__file__).parent.parent

def train_and_save_model():
    # Initialize MLflow experiment
    mlflow.set_experiment("Wine_Quality_Prediction")
    mlflow.keras.autolog()
    
    # Load dataset
    data_path = PROJECT_ROOT / 'data/winequality-white.csv'
    df = pd.read_csv(data_path, sep=';')
    
    # Preprocessing
    X = df.drop('quality', axis=1)
    y = df['quality'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    with mlflow.start_run():
        # Log data metadata
        mlflow.log_param("dataset_path", str(data_path))
        mlflow.log_param("dataset_shape", df.shape)
        mlflow.log_param("test_size", 0.2)
        
        # Log preprocessing details
        mlflow.log_param("scaler", type(scaler).__name__)
        
        # Build ANN
        model = Sequential([
            Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
            Dense(32, activation='relu'),
            Dense(1)
        ])
        
        model.compile(
            optimizer='adam',
            loss=losses.MeanSquaredError(),
            metrics=['mae']
        )
        
        # Log model architecture
        mlflow.log_param("layers", [
            {"units": 64, "activation": "relu"},
            {"units": 32, "activation": "relu"},
            {"units": 1}
        ])
        
        # Train model with validation
        history = model.fit(
            X_train, y_train,
            epochs=50,
            validation_split=0.2,
            verbose=1
        )
        
        # Log final training metrics
        mlflow.log_metrics({
            "final_train_loss": history.history['loss'][-1],
            "final_train_mae": history.history['mae'][-1],
            "final_val_loss": history.history['val_loss'][-1],
            "final_val_mae": history.history['val_mae'][-1]
        })
        
        # Evaluate on test set
        test_loss, test_mae = model.evaluate(X_test, y_test)
        mlflow.log_metrics({
            "test_loss": test_loss,
            "test_mae": test_mae
        })
        
        # Create model directory if not exists
        # model_dir = Path(__file__).parent.resolve()
        model_dir = PROJECT_ROOT / 'model'
        model_dir.mkdir(exist_ok=True)
        
        # Save artifacts
        scaler_path =  model_dir / 'scaler.pkl'
        model_path = model_dir / 'wine_quality_ann.keras'
        
        joblib.dump(scaler, scaler_path)
        model.save(model_path)
        
        # Log artifacts to MLflow
        mlflow.log_artifact(str(scaler_path))
        mlflow.keras.log_model(
            model,
            "model",
            registered_model_name="WineQualityANN",
            signature=mlflow.models.infer_signature(X_train, model.predict(X_train))
        )

if __name__ == "__main__":
    train_and_save_model()
