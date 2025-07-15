from fastapi import FastAPI, Request, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import sys, joblib, json, os
from datetime import datetime
import pandas as pd

# Add the parent directory of backend-api to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend_api.utils import extract_features

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "../ml_model/bot_detector_bundle.joblib"))

# Load the model bundle
model_bundle = joblib.load(MODEL_PATH)
model = model_bundle["model"]
encoders = model_bundle["encoders"]  # Dictionary of label encoders for categorical features

app = FastAPI()
API_KEY = "e5a74d0c291f4603f99de0cf607492a6"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"]   # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the PEDIASCAPE API!"}

@app.post("/api/verify")
async def verify_user(request: Request, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        data = await request.json()
        print("Received data:", json.dumps(data, indent=2))

        # Extract features in the order expected by the model
        features = [
            data.get("userAgent", ""),
            data.get("screenResolution", ""),
            data.get("os", ""),
            data.get("language", ""),
              # CPU/GPU Specs
            data.get("cpuThreads", ""),
            data.get("browserFingerprinting", ""),
            data.get("plugins", ""),
            data.get("canvasFingerprint", ""),
            data.get("timezone", ""),
            data.get("ipAddressMasked", ""),
            data.get("connectionSpeed", ""),
            data.get("proxyVPNDetection", ""),
            json.dumps(data.get("mouseMovementPatterns", [])),
            json.dumps(data.get("clickTimings", [])),
            data.get("scrollDepth", ""),
            data.get("touchPressure", ""),
            str(data.get("pageLoadTimes", [])),
            str(data.get("dwellTimes", [])),
            json.dumps(data.get("inactivityPatterns", [])),
            json.dumps(data.get("keystrokeDynamics", [])),
            json.dumps(data.get("smallPointerMovements", [])),
        ]

        feature_names = [
            "User-Agent", "Screen Resolution", "OS", "Language",
            "CPU/GPU Specs", "Browser Fingerprinting", "Plugins",
            "Canvas Fingerprint", "Timezone", "IP Address (Masked)",
            "Connection Speed", "Proxy/VPN Detection", "Mouse Movement Patterns",
            "Click Timings", "Scroll Depth", "Touch Pressure",
            "Page Load Time", "Dwell Time", "Inactivity Patterns",
            "Keystroke Dynamics", "Small Pointer Movements"
        ]
        
        # Create a DataFrame with raw features
        features_df = pd.DataFrame([features], columns=feature_names)
        
        # Apply encoders to transform categorical features to numeric
        processed_features = features_df.copy()
        for column, encoder in encoders.items():
            if column in processed_features.columns:
                try:
                    processed_features[column] = encoder.transform(processed_features[column])
                except Exception as e:
                    # Handle unknown categories
                    print(f"Error encoding {column}: {e}")
                    # Use a default value for unknown categories
                    processed_features[column] = 0  # Or some other appropriate default
        
        # Make prediction using processed features
        prediction = model.predict(processed_features)[0]
        score = model.predict_proba(processed_features)[0][1]

        log = {
            "timestamp": datetime.now().isoformat(),
            "verdict": "human" if prediction == 0 else "bot",
            "confidence": round(score, 2),
            "raw": data
        }

        raw_data_path = os.path.join(BASE_DIR, "raw_data/sessions.jsonl")
        os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)
        with open(raw_data_path, "a") as f:
            f.write(json.dumps(log) + "\n")

        return {"verdict": log["verdict"], "confidence": log["confidence"]}
    except Exception as e:
        print(f"Error in verify_user: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/sessions")
def get_sessions(limit: int = Query(None), offset: int = Query(0)):
    """
    Get all sessions with optional pagination.
    
    Parameters:
    - limit: Optional maximum number of sessions to return
    - offset: Optional offset for pagination (default 0)
    
    Returns all sessions if limit is None, otherwise returns paginated results.
    """
    raw_data_path = os.path.join(BASE_DIR, "raw_data/sessions.jsonl")
    logs = []
    
    try:
        with open(raw_data_path, "r") as f:
            logs = [json.loads(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        return []
    
    # Sort logs by timestamp (newest first)
    logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # Apply pagination if limit is provided
    if limit is not None:
        return logs[offset:offset+limit]
    
    # Return all logs if no limit specified
    return logs

@app.get("/api/session")
def get_current_session():
    print("Endpoint /api/session was called")  # Debug log
    raw_data_path = os.path.join(BASE_DIR, "raw_data/sessions.jsonl")
    try:
        with open(raw_data_path, "r") as f:
            logs = [json.loads(line.strip()) for line in f.readlines()]
        if logs:
            return logs[-1]  # Return the most recent session
    except FileNotFoundError:
        pass
    return {"message": "No session data available"}