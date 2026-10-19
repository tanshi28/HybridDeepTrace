import joblib
import numpy as np

from pathlib import Path
try:
    from .feature_extraction import extract_features
except ImportError:
    from feature_extraction import extract_features

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"

svm_model = joblib.load(MODEL_DIR / "svm_model.pkl")
scaler = joblib.load(MODEL_DIR / "scaler.pkl")
rf_model = joblib.load(MODEL_DIR / "random_forest_model.pkl")
xgb_model = joblib.load(MODEL_DIR / "xgboost_model.pkl")


def compare_models(image_path):

    features = extract_features(image_path).reshape(1, -1)

    scaled_features = scaler.transform(features)

    svm_prediction = svm_model.predict(scaled_features)[0]
    rf_prediction = rf_model.predict(features)[0]
    xgb_prediction = xgb_model.predict(features)[0]

    label_map = {
        0: "REAL",
        1: "FAKE"
    }

    results = {
        "SVM": label_map[int(svm_prediction)],
        "Random Forest": label_map[int(rf_prediction)],
        "XGBoost": label_map[int(xgb_prediction)]
    }

    return results