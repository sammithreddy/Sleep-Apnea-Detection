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
import uuid
from feature_extraction import extract_all_features, read_ecg
from fastapi.middleware.cors import CORSMiddleware

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

# Enable CORS for frontend - allow all for deployment flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Must be False if using "*" for origins
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load the highest performing model
try:
    xgb_model = joblib.load("models/xgb_classifier.pkl")
except Exception as e:
    print(f"[CRITICAL] Failed to load model: {str(e)}")
    xgb_model = None

# Features used for training
FEATURES = [
    "MeanRR", "SD_RR", "RMSSD", "NN50", "pNN50", "AverageHeartRate",
    "StandardDeviationHeartRate", "Mean_R_Peak_Amplitudes",
    "QRS_Duration", "QRS_Amplitude", "QRS_Slope", "LF_HF_Ratio", "PSE"
]

def predict_model(feature_df):
    """Runs predictions using XGBoost model."""
    if xgb_model is None:
        raise Exception("ML Model not loaded on server.")
    sc = StandardScaler()
    feature_array = sc.fit_transform(feature_df)
    return xgb_model.predict(feature_array)

@app.post("/process_ecg/")
async def process_ecg(file: UploadFile = File(...), header: UploadFile = None):
    """API Endpoint for ECG processing."""
    try:
        # 1. Read files into memory
        ecg_content = await file.read()
        
        # 2. Save to unique subdirectory to maintain original filenames for wfdb
        request_id = str(uuid.uuid4())
        request_dir = os.path.join(UPLOAD_DIR, request_id)
        os.makedirs(request_dir, exist_ok=True)
        
        # Save files temporarily
        temp_dat_path = os.path.join(request_dir, file.filename)
        with open(temp_dat_path, "wb") as f:
            f.write(ecg_content)
        
        final_file_path = temp_dat_path
        if file.filename.endswith(".dat") and header:
            hea_content = await header.read()
            temp_hea_path = os.path.join(request_dir, header.filename)
            with open(temp_hea_path, "wb") as f:
                f.write(hea_content)
            
            # CRITICAL: wfdb expects the file names on disk to match the RECORD name inside the .hea file
            # We must parse the .hea file to find the actual record name
            try:
                hea_lines = hea_content.decode("utf-8").splitlines()
                if hea_lines:
                    # First line format: [record_name] [num_signals] [fs] [num_samples]
                    record_name = hea_lines[0].split()[0]
                    print(f"[INFO] Parsed record name: {record_name}")
                    
                    # Rename files to match record_name
                    new_hea_path = os.path.join(request_dir, f"{record_name}.hea")
                    new_dat_path = os.path.join(request_dir, f"{record_name}.dat")
                    
                    if os.path.abspath(temp_hea_path) != os.path.abspath(new_hea_path):
                        os.rename(temp_hea_path, new_hea_path)
                    if os.path.abspath(temp_dat_path) != os.path.abspath(new_dat_path):
                        os.rename(temp_dat_path, new_dat_path)
                    
                    final_file_path = new_dat_path
            except Exception as e:
                print(f"[WARNING] Failed to parse .hea file for record name: {str(e)}")

        # 3. Read ECG signal
        try:
            ecg_signal = read_ecg(final_file_path)
        except Exception as read_err:
            # Cleanup on failure
            import shutil
            if os.path.exists(request_dir): shutil.rmtree(request_dir)
            raise Exception(f"Failed to read ECG file: {str(read_err)}")
        
        # 4. Cleanup directory immediately after reading into memory
        import shutil
        if os.path.exists(request_dir): shutil.rmtree(request_dir)

        # 5. Process in segments
        segment_length = 6000  # 1-minute segments
        num_segments = len(ecg_signal) // segment_length
        
        if num_segments == 0:
            raise Exception("File too short for analysis (minimum 1 minute required).")

        # Limit segments to prevent timeouts
        MAX_SEGMENTS = 120 # 2 hours max for stability
        num_segments = min(num_segments, MAX_SEGMENTS)

        all_features = []
        for i in range(num_segments):
            segment = ecg_signal[i * segment_length: (i + 1) * segment_length]
            features = extract_all_features(segment)
            # Use 0 if feature extraction fails for a specific metric
            features_mapped = [features.get(feat, 0) for feat in FEATURES]
            all_features.append(features_mapped)

        # 6. Predict
        feature_df = pd.DataFrame(all_features, columns=FEATURES)
        predictions = predict_model(feature_df)

        # 7. Summarize
        apnea_count = sum(predictions)
        ahi = float((apnea_count / num_segments) * 60)
        severity = classify_ahi(ahi)
        waveform_plot = plot_ecg(ecg_signal)

        result_content = {
            "filename": file.filename,
            "AHI": ahi,
            "Severity": severity,
            "prediction_summary": {
                "total_segments": int(num_segments),
                "apnea_segments": int(apnea_count),
                "normal_segments": int(num_segments - apnea_count)
            }
        }
        
        save_to_history(result_content)
        result_content["ecg_waveform"] = waveform_plot

        return JSONResponse(content=result_content)
    except Exception as e:
        # Critical for debugging: show exactly what failed
        error_msg = str(e)
        print(f"[ERROR] {error_msg}")
        return JSONResponse(status_code=500, content={"error": error_msg})

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
