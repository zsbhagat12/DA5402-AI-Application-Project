# DA5402-AI-Application-Project

Code Structure

```
.
.
├── backend/
│   ├── static/
│   │   └── swagger.json
│   ├── server.py                 # Model inference API server
│   └── Dockerfile                
├── data/
│   ├── winequality-red.csv
│   ├── winequality-white.csv
│   └── winequality.names
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   └── script/
│   ├── templates/
│   │   ├── 404.html
│   │   └── index.html
│   ├── app.py                   # User-facing frontend Flask app
│   └── Dockerfile                   
├── grafana/
│   ├── dashboards/
│   │   └── wine_dashboard.json  # Exported dashboard
│   ├── provisioning/
│   │   ├── dashboards/
│   │   │   └── dashboard.yml    # Load custom dashboards
│   │   └── datasources/
│   │       └── datasource.yml   # Prometheus data source config
├── logs/
│   ├── logs/
│   │   ├── app.log
│   │   └── server.log
│   └── logging_utils.py         # Custom logging formatter
├── mlruns/                      # MLflow experiment tracking
├── model/
│   ├── scaler.pkl
│   ├── train.py
│   ├── wine_quality_ann.h5      # (existing)
│   └── wine_quality_ann.keras   # (optional Keras format)
├── prometheus/
│   └── prometheus.yml           # Prometheus configuration
├── requirements.txt             # All libraries present here to be installed beforehand
├── README.md                    # This file
├── dvc.yaml                     # DVC Pipeline
└── docker-compose.yml           # (included to launch full stack)

```
