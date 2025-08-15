# utils.py
import os
import json
from joblib import load

ARTIFACT_DIR = 'data/model_artifacts'


def load_model_and_artifacts():
    model_p = os.path.join(ARTIFACT_DIR, 'model.pkl')
    scaler_p = os.path.join(ARTIFACT_DIR, 'scaler.pkl')
    stats_p = os.path.join(ARTIFACT_DIR, 'stats.json')

    if not (os.path.exists(model_p) and os.path.exists(scaler_p) and os.path.exists(stats_p)):
        raise FileNotFoundError('Model artifacts not found. Run `python model_train.py` first to generate them.')

    model = load(model_p)
    scaler = load(scaler_p)
    with open(stats_p, 'r') as f:
        stats = json.load(f)
    return model, scaler, stats