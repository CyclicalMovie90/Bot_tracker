import os
import sys
import json
import joblib
from sklearn.ensemble import RandomForestClassifier

# ✅ Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from backend_api.utils import extract_features

X, y = [], []
with open("backend-api/raw_data/sessions.jsonl", "r") as f:
    for line in f:
        session = json.loads(line)
        label = 0 if session["verdict"] == "human" else 1
        features = extract_features(session["raw"])
        X.append(features)
        y.append(label)

clf = RandomForestClassifier()
clf.fit(X, y)
joblib.dump(clf, "ml_model/bot_detector.joblib")

print("✅ Model retrained and saved as backend-api/bot_detector.joblib")
