# DA5402-AI-Application-Project

Code Structure

```
.
├── backend/
│   ├── static/
│   │   └── swagger.json         # OpenAPI/Swagger specification for API docs
│   └── server.py                # Model inference API server (Flask, Swagger UI)
├── data/
│   ├── winequality-red.csv      # Red wine dataset
│   ├── winequality-white.csv    # White wine dataset
│   └── winequality.names        # Dataset feature descriptions
├── frontend/
│   ├── static/
│   │   ├── css/                 # Custom CSS for frontend
│   │   └── script/              # Custom JS for frontend
│   ├── templates/
│   │   ├── 404.html             # Error page template
│   │   └── index.html           # Main UI template for wine quality prediction
│   └── app.py                   # Frontend Flask app (user interface, form handling)
├── model/
│   ├── scaler.pkl               # Saved StandardScaler for feature normalization
│   ├── train.py                 # Model training script (ANN)
│   └── wine_quality_ann.h5      # Trained ANN model file
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
└── 
```
