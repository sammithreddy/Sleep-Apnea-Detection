import numpy as np
import pandas as pd
import neurokit2 as nk
from scipy.signal import butter, filtfilt, iirnotch, welch
import os
import wfdb
import scipy.io

# ---------------------------- ECG FILE READING --------------------------------
def read_ecg(file_path):
    """
    Reads ECG files (.csv, .dat, .mat) and returns the raw ECG signal.
    """
    ext = os.path.splitext(file_path)[-1].lower()
    print(f"[INFO] Reading ECG file: {file_path} (Format: {ext})")

    if ext == ".csv":
        df = pd.read_csv(file_path)
        print(f"[DEBUG] CSV file loaded, shape: {df.shape}")
        return df.iloc[:, 1].values  # Assuming second column contains ECG signal

    elif ext == ".mat":
        mat_data = scipy.io.loadmat(file_path)
        key = list(mat_data.keys())[-1]  # Find ECG data key
        print(f"[DEBUG] MAT file loaded with key: {key}")
        return mat_data[key].flatten()

    elif ext == ".dat":
        hea_file = file_path.replace(".dat", ".hea")
        if not os.path.exists(hea_file):
            raise FileNotFoundError(f"[ERROR] Missing header file: {hea_file}")
        print(f"[INFO] Found header file: {hea_file}")
        record = wfdb.rdrecord(file_path.replace(".dat", ""))
        print(f"[DEBUG] DAT file loaded, shape: {record.p_signal.shape}")
        return record.p_signal[:, 0]

    else:
        raise ValueError(f"[ERROR] Unsupported file format: {ext}")

# ---------------------------- ECG FILTERING --------------------------------
def highpass_filter(signal, fs, cutoff=0.5, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, signal)

def notch_filter(signal, fs, f0=50, Q=30):
    b, a = iirnotch(f0, Q, fs)
    return filtfilt(b, a, signal)

# ---------------------------- R-PEAK DETECTION --------------------------------
def detect_r_peaks_sleepecg(segment, fs):
    _, results = nk.ecg_peaks(segment, sampling_rate=fs)
    return results["ECG_R_Peaks"]

# ---------------------------- HRV FEATURES --------------------------------
def compute_rr_intervals(r_peaks, fs):
    return np.diff(r_peaks) / fs if len(r_peaks) > 1 else []

def compute_hrv_features(rr_intervals):
    if len(rr_intervals) < 2:
        return {"MeanRR": None, "SD_RR": None, "RMSSD": None, "NN50": None, "pNN50": None}
    return {
        "MeanRR": np.mean(rr_intervals),
        "SD_RR": np.std(rr_intervals),
        "RMSSD": np.sqrt(np.mean(np.diff(rr_intervals) ** 2)),
        "NN50": np.sum(np.abs(np.diff(rr_intervals)) > 0.05),  # Count NN50 occurrences
        "pNN50": (np.sum(np.abs(np.diff(rr_intervals)) > 0.05) / len(rr_intervals)) * 100
    }

def compute_heart_rate_features(rr_intervals):
    if len(rr_intervals) < 1:
        return {"AverageHeartRate": None, "StandardDeviationHeartRate": None, "AverageHRV": None}
    heart_rates = 60 / rr_intervals
    return {
        "AverageHeartRate": np.mean(heart_rates),
        "StandardDeviationHeartRate": np.std(heart_rates),
        # "AverageHRV": np.sqrt(np.mean(np.diff(rr_intervals) ** 2))
    }

# ---------------------------- QRS COMPLEX FEATURES --------------------------------
def compute_qrs_features(r_peaks, segment, fs):
    if len(r_peaks) < 2:
        return {"QRS_Duration": None, "QRS_Amplitude": None, "QRS_Slope": None}
    qrs_durations = [(r_peaks[i + 1] - r_peaks[i]) / fs for i in range(len(r_peaks) - 1)]
    qrs_amplitudes = [segment[r_peaks[i + 1]] - segment[r_peaks[i]] for i in range(len(r_peaks) - 1)]
    qrs_slope = [amp / dur for amp, dur in zip(qrs_amplitudes, qrs_durations)]
    return {
        "QRS_Duration": np.mean(qrs_durations),
        "QRS_Amplitude": np.mean(qrs_amplitudes),
        "QRS_Slope": np.mean(qrs_slope)
    }

# ---------------------------- MORPHOLOGICAL FEATURES --------------------------------
def compute_r_peak_amplitude(r_peaks, segment):
    if len(r_peaks) < 1:
        return {"Mean_R_Peak_Amplitudes": None}
    amplitudes = [segment[r] for r in r_peaks]
    return {"Mean_R_Peak_Amplitudes": np.mean(amplitudes)}

# ---------------------------- FREQUENCY DOMAIN FEATURES --------------------------------
def compute_frequency_features(segment, fs):
    f, psd = welch(segment, fs=fs, nperseg=1024)
    total_power = np.sum(psd)
    psd_normalized = psd / total_power if total_power > 0 else np.zeros_like(psd)
    lf_power = np.sum(psd[(f >= 0.04) & (f <= 0.15)])
    hf_power = np.sum(psd[(f >= 0.15) & (f <= 0.4)])
    lf_hf_ratio = lf_power / hf_power if hf_power > 0 else None
    pse = -np.sum(psd_normalized * np.log2(psd_normalized, where=psd_normalized > 0))
    return {"LF_HF_Ratio": lf_hf_ratio, "PSE": pse}

# ---------------------------- FULL FEATURE EXTRACTION --------------------------------
def extract_all_features(segment, fs=100):
    """
    Extracts all statistical, morphological, and frequency-domain features from a 1-minute ECG segment.
    """
    segment = highpass_filter(segment, fs)
    segment = notch_filter(segment, fs)
    r_peaks = detect_r_peaks_sleepecg(segment, fs)
    rr_intervals = compute_rr_intervals(r_peaks, fs)
    features = {}
    features.update(compute_hrv_features(rr_intervals))
    features.update(compute_heart_rate_features(rr_intervals))
    features.update(compute_qrs_features(r_peaks, segment, fs))
    features.update(compute_r_peak_amplitude(r_peaks, segment))  # Added R-Peak Amplitudes
    features.update(compute_frequency_features(segment, fs))
    return features
