from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import joblib
import numpy as np
import os
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import base64
import json
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from feature_extraction import extract_all_features, read_ecg
from fastapi.middleware.cors import CORSMiddleware
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

app = FastAPI()

HISTORY_FILE = "history.json"

def save_to_history(result):
    """Saves the last 5 test results to a JSON file."""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except:
                history = []
    
    # Add new result at the beginning
    result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.insert(0, result)
    
    # Keep only last 5
    history = history[:5]
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

@app.get("/history")
async def get_history():
    """Returns the list of recent test results."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load the highest performing model from our testing phase
xgb_model = joblib.load("models/xgb_classifier.pkl")

# Features used for training
FEATURES = [
    "MeanRR", "SD_RR", "RMSSD", "NN50", "pNN50", "AverageHeartRate",
    "StandardDeviationHeartRate", "Mean_R_Peak_Amplitudes",
    "QRS_Duration", "QRS_Amplitude", "QRS_Slope", "LF_HF_Ratio", "PSE"
]

def predict_model(feature_df):
    """Runs predictions using XGBoost model."""
    sc = StandardScaler()
    feature_array = sc.fit_transform(feature_df)
    
    xgb_preds = xgb_model.predict(feature_array)
    return xgb_preds

@app.post("/process_ecg/")
async def process_ecg(file: UploadFile = File(...), header: UploadFile = None):
    """API Endpoint for ECG processing."""
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    hea_file_path = None
    if file.filename.endswith(".dat"):
        if not header:
            return JSONResponse(status_code=400, content={"error": "A .hea file is required for .dat uploads!"})
        hea_file_path = os.path.join(UPLOAD_DIR, header.filename)
        with open(hea_file_path, "wb") as f:
            f.write(header.file.read())

    try:
        # Read ECG signal
        ecg_signal = read_ecg(file_path)
        print("ECG")
        segment_length = 6000  # 1-minute segments (100 Hz)
        num_segments = len(ecg_signal) // segment_length

        all_features = []
        print(num_segments)
        for i in range(num_segments):
            segment = ecg_signal[i * segment_length: (i + 1) * segment_length]
            features = extract_all_features(segment)
            try:
                # Ensure keys map cleanly despite case sensitivity issues in original mapping
                features_mapped = []
                for feat in FEATURES:
                   # Accommodate variations built into feature_extraction dict output
                   mapping_val = features.get(feat, features.get("mean_R_Peak_Amplitudes"))
                   features_mapped.append(mapping_val)
                all_features.append(features_mapped)
            except Exception as ex:
                print("Error",ex)

        feature_df = pd.DataFrame(all_features, columns=FEATURES)
        # Apply XGBoost Predictor
        predictions = predict_model(feature_df)

        # Compute AHI
        apnea_count = sum(predictions)
        ahi = (apnea_count / num_segments) * 60

        # Determine severity
        severity = classify_ahi(ahi)

        # Generate ECG waveform plot
        waveform_plot = plot_ecg(ecg_signal)

        # Delete files after processing
        os.remove(file_path)
        if hea_file_path:
            os.remove(hea_file_path)

        result_content = {
            "filename": file.filename,
            "AHI": float(ahi),
            "Severity": severity,
            "prediction_summary": {
                "total_segments": int(num_segments),
                "apnea_segments": int(apnea_count),
                "normal_segments": int(num_segments - apnea_count)
            }
        }
        
        # Save to history (excluding the heavy waveform image)
        save_to_history(result_content)

        # Add waveform for the immediate response
        result_content["ecg_waveform"] = waveform_plot

        return JSONResponse(content=result_content, media_type="application/json")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def classify_ahi(ahi):
    """Classifies severity based on AHI index."""
    if ahi < 5:
        return "Green (Normal)"
    elif 5 <= ahi < 15:
        return "Yellow (Mild)"
    elif 15 <= ahi < 30:
        return "Orange (Moderate)"
    else:
        return "Red (Severe)"

def plot_ecg(ecg_signal):
    """Generates a simple ECG waveform plot and returns as base64 image."""
    plt.figure(figsize=(10, 4))
    plt.plot(ecg_signal[:1000])
    plt.title("ECG Waveform")
    plt.xlabel("Time (samples)")
    plt.ylabel("Amplitude")
    plt.grid()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close()

    return encoded_string

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
