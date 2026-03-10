import os
import glob
import pandas as pd
import numpy as np
import wfdb
import neurokit2
from scipy.signal import butter, filtfilt, iirnotch, welch

import warnings
warnings.filterwarnings('ignore')

dataset_path = './Apnea DataSet/apnea-ecg'
output_dir = './new_features'
os.makedirs(output_dir, exist_ok=True)

groups = {'A': [f'a{str(i).zfill(2)}' for i in range(1, 21)],
          'B': [f'b{str(i).zfill(2)}' for i in range(1, 6)],
          'C': [f'c{str(i).zfill(2)}' for i in range(1, 11)]}

def highpass_filter(signal, fs, cutoff=0.5, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, signal)

def notch_filter(signal, fs, f0=50, Q=30):
    b, a = iirnotch(f0, Q, fs)
    return filtfilt(b, a, signal)

for group_name, record_names in groups.items():
    print(f"\nProcessing Group {group_name}...")
    segmented_data_list = []
    
    for record_name in record_names:
        record_path = f"{dataset_path}/{record_name}"
        try:
            record = wfdb.rdrecord(record_path)
            annotation = wfdb.rdann(record_path, 'apn')
            
            raw_signal = record.p_signal[:, 0]
            fs = record.fs
            labels = annotation.symbol
            
            gain = record.adc_gain[0] if record.adc_gain[0] is not None else 1
            baseline = record.baseline[0] if record.baseline[0] is not None else 0
            scaled_signal = (raw_signal - baseline) / gain
            
            segment_length = int(fs * 60)
            total_samples = len(labels) * segment_length
            truncated_signal = scaled_signal[:total_samples]
            
            for i, label in enumerate(labels):
                start = i * segment_length
                end = (i + 1) * segment_length
                segment = truncated_signal[start:end]
                
                # Preprocess: highpass + notch
                hp_segment = highpass_filter(segment, fs)
                preprocessed_segment = notch_filter(hp_segment, fs)
                
                segmented_data_list.append({
                    "Record_ID": record_name,
                    "Segment_ID": i + 1,
                    "Signal": preprocessed_segment,
                    "Label": label
                })
            print(f"Loaded and preprocessed {record_name} (Segments: {len(labels)})")
        except Exception as e:
            print(f"Error with {record_name}: {e}")
            
    print(f"Extracting features for Group {group_name}...")
    all_features = []
    labels_list = []
    records_list = []
    
    for idx, row in enumerate(segmented_data_list):
        segment = row['Signal']
        label = row['Label']
        record_id = row['Record_ID']
        fs = 100
        
        try:
            _, results = neurokit2.ecg_peaks(segment, sampling_rate=fs)
            r_peaks = results["ECG_R_Peaks"]
            
            if len(r_peaks) < 2:
                all_features.append([None]*13)
                labels_list.append(label)
                records_list.append(record_id)
                continue
                
            rr_intervals = np.diff(r_peaks) / fs
            
            mean_rr = np.mean(rr_intervals)
            sd_rr = np.std(rr_intervals, ddof=1) if len(rr_intervals) > 1 else 0
            rmssd = np.sqrt(np.mean(np.diff(rr_intervals) ** 2)) if len(rr_intervals) > 1 else 0
            nn50 = np.sum(np.abs(np.diff(rr_intervals)) > 0.05) if len(rr_intervals) > 1 else 0
            pnn50 = (nn50 / len(rr_intervals)) * 100 if len(rr_intervals) > 1 else 0
            avg_hr = np.mean(60 / rr_intervals)
            std_hr = np.std(60 / rr_intervals, ddof=1) if len(rr_intervals) > 1 else 0
            
            baseline_val = np.median(segment)
            mean_r_amplitude = np.mean([segment[r] - baseline_val for r in r_peaks])
            
            qrs_durations = []
            qrs_amplitudes = []
            qrs_slopes = []
            for r_peak in r_peaks:
                pre_win = 10
                post_win = 10
                start_search = max(0, r_peak - pre_win)
                end_search = min(len(segment), r_peak + post_win)
                
                diffs_pre = np.diff(segment[start_search:r_peak]) if r_peak > start_search else []
                diffs_post = np.diff(segment[r_peak:end_search]) if end_search > r_peak else []
                
                if len(diffs_pre) > 0 and len(diffs_post) > 0:
                    start_idx = start_search + np.argmin(diffs_pre)
                    end_idx = r_peak + np.argmin(diffs_post)
                    if start_idx < end_idx:
                        dur = (end_idx - start_idx) / fs
                        amp = segment[end_idx] - segment[start_idx]
                        qrs_durations.append(dur)
                        qrs_amplitudes.append(amp)
                        qrs_slopes.append(amp / dur if dur > 0 else 0)
                        
            mean_qrs_duration = np.mean(qrs_durations) if len(qrs_durations) > 0 else 0
            mean_qrs_amplitude = np.mean(qrs_amplitudes) if len(qrs_amplitudes) > 0 else 0
            mean_qrs_slope = np.mean(qrs_slopes) if len(qrs_slopes) > 0 else 0
            
            # frequency features
            f, psd = welch(segment, fs=fs, nperseg=1024)
            total_power = np.sum(psd)
            psd_norm = psd / total_power if total_power > 0 else np.zeros_like(psd)
            
            lf_power = np.sum(psd[(f >= 0.04) & (f <= 0.15)])
            hf_power = np.sum(psd[(f >= 0.15) & (f <= 0.4)])
            lf_hf_ratio = lf_power / hf_power if hf_power > 0 else 0
            
            pse = -np.sum(psd_norm[psd_norm > 0] * np.log2(psd_norm[psd_norm > 0]))
            
            all_features.append([
                mean_rr, sd_rr, rmssd, nn50, pnn50, avg_hr, std_hr, mean_r_amplitude,
                mean_qrs_duration, mean_qrs_amplitude, mean_qrs_slope, lf_hf_ratio, pse
            ])
            labels_list.append(label)
            records_list.append(record_id)
            
        except Exception as e:
            all_features.append([None]*13)
            labels_list.append(label)
            records_list.append(record_id)

    feature_names = [
        "MeanRR", "SD_RR", "RMSSD", "NN50", "pNN50", "AverageHeartRate",
        "StandardDeviationHeartRate", "mean_R_Peak_Amplitudes",
        "QRS_Duration", "QRS_Amplitude", "QRS_Slope", "LF_HF_Ratio", "PSE"
    ]
    
    df = pd.DataFrame(all_features, columns=feature_names)
    df["Label"] = labels_list
    df["Record_ID"] = records_list
    
    # drop rows where features couldn't be extracted
    df = df.dropna()
    
    output_file = f"{output_dir}/features_of_{group_name}.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved {output_file} with shape {df.shape}")

print('Pipeline completed successfully!')
