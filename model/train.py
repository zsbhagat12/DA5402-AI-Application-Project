import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib
import numpy as np
from pathlib import Path

def train_and_save_model():
    # Load dataset
    data_path = Path(__file__).parent.parent / 'data/winequality-white.csv'
    df = pd.read_csv(data_path, sep=';')
    # print(df.head(5))  # Debugging line to check the data
    
    # Preprocessing
    X = df.drop('quality', axis=1)
    y = df['quality']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # print(X_train.shape, X_test.shape)  # Debugging line to check the shapes
    # print(y_train.shape, y_test.shape)  # Debugging line to check the shapes
    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Save scaler
    joblib.dump(scaler, 'scaler.pkl')
    
    # Build ANN
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    # Train
    model.fit(X_train, y_train, epochs=50, validation_split=0.2)
    
    # Save model
    model_path = Path(__file__).parent / 'wine_quality_ann.h5'
    model.save(model_path)

    scaler_path = Path(__file__).parent / 'scaler.pkl' 
    joblib.dump(scaler, scaler_path)

if __name__ == "__main__":
    train_and_save_model()
