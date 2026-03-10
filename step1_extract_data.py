import pandas as pd



import wfdb
import os

dataset_path = './Apnea DataSet/apnea-ecg'

record_names = [
    # # Group A: 20 records
    # "a01", "a02", "a03", "a04", "a05", "a06", "a07", "a08", "a09", "a10",
    # "a11", "a12", "a13", "a14", "a15", "a16", "a17", "a18", "a19", "a20"
    # # Group B: 5 records
    # "b01", "b02", "b03", "b04", "b05",
    # # Group C: 10 records
    "c01", "c02", "c03", "c04", "c05", "c06", "c07", "c08", "c09", "c10",
    # "x01", "x02", "x03", "x04", "x05", "x06", "x07", "x08", "x09", "x10",
    # "x11", "x12", "x13", "x14", "x15", "x16", "x17", "x18", "x19", "x20",
    # "x21", "x22", "x23", "x24", "x25", "x26", "x27", "x28", "x29", "x30",
    # "x31", "x32", "x33", "x34", "x35"
]





segmented_data = []

for record_name in record_names:
    try:
        # Load the signal and annotations
        record_path = f"{dataset_path}/{record_name}"
        record = wfdb.rdrecord(record_path)
        annotation = wfdb.rdann(record_path, 'apn')

        raw_signal = record.p_signal[:, 0]  # ECG signal (first channel)
        sampling_frequency = record.fs
        labels = annotation.symbol  # Apnea/Normal labels

        # Apply scaling using gain and baseline
        gain = record.adc_gain[0]  # Gain for first channel
        baseline = record.baseline[0]  # Baseline for first channel
        scaled_signal = (raw_signal - baseline) / gain

        # Calculate segment length
        segment_length = int(sampling_frequency * 60)  # 1-minute segments

        # Truncate the signal to match the labels
        total_samples = len(labels) * segment_length
        truncated_signal = scaled_signal[:total_samples]

        # Segment and label
        for i, label in enumerate(labels):
            start = i * segment_length
            end = (i + 1) * segment_length
            segment = truncated_signal[start:end]

            segmented_data.append({
                "Record_ID": record_name,
                "Segment_ID": i + 1,
                "Signal_Data": segment.tolist(),
                "Label": label
            })

        print(f"Processed record: {record_name} (Segments: {len(labels)})")

    except Exception as e:
        print(f"Error processing record {record_name}: {e}")


for i in range(len(segmented_data)):
  segmented_data[i]['Signal_Data'] = [format(num, '.7f') for num in segmented_data[i]['Signal_Data']]

pd.DataFrame(segmented_data).to_csv("./C_DataSet.csv", index=False)



