# model/preprocess.py
import pandas as pd
from pathlib import Path
import sys

if str(Path(__file__).parent.parent / 'logs') not in sys.path:
    sys.path.append(str(Path(__file__).parent.parent / "logs"))
from logging_utils import setup_logger

logger = setup_logger('train', 'preprocess.log')

PROJECT_ROOT = Path(__file__).parent.parent

def preprocess():
    # data_path = Path('data/winequality-white.csv')
    data_path = PROJECT_ROOT / 'data/raw/winequality-white.csv'
    df = pd.read_csv(data_path, sep=';')
  
    df = df.drop_duplicates()
    df = df.dropna()
    processed_path = Path('data/processed/winequality-white_processed.csv')
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed_path, index=False)

if __name__ == "__main__":
    preprocess()
