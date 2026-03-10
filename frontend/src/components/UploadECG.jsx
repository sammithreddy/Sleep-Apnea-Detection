import React, { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const UploadECG = () => {
  const [ecgFile, setEcgFile] = useState(null);
  const [heaFile, setHeaFile] = useState(null);
  const [ecgWaveform, setEcgWaveform] = useState(null);
  const [predictionSummary, setPredictionSummary] = useState(null);
  const [ahi, setAhi] = useState(null);
  const [severity, setSeverity] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleEcgFileChange = (event) => setEcgFile(event.target.files[0]);
  const handleHeaFileChange = (event) => setHeaFile(event.target.files[0]);

  const handleUpload = async () => {
    setError("");
    setLoading(true);

    if (!ecgFile) {
      setError("❌ Please select a .dat ECG file before uploading.");
      setLoading(false);
      return;
    }

    if (!heaFile) {
      setError("❌ Please upload the corresponding .hea file.");
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append("file", ecgFile);
    formData.append("header", heaFile);

    try {
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
      const baseUrl = apiBaseUrl.endsWith("/") ? apiBaseUrl.slice(0, -1) : apiBaseUrl;
      const response = await axios.post(`${baseUrl}/process_ecg/`, formData);
      const data = response.data;

      setEcgWaveform(data.ecg_waveform);
      setPredictionSummary(data.prediction_summary);
      setAhi(data.AHI);
      setSeverity(data.Severity);
    } catch (error) {
      setError("❌ Failed to process file. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container-fluid mt-5">
      <div className="card p-4 mx-auto shadow-lg" style={{ maxWidth: "900px" }}>
        <h2 className="text-center text-primary">Upload & Analyze ECG File</h2>

        {/* ECG File Upload */}
        <div className="mt-3">
          <label className="font-weight-bold">Upload .dat File:</label>
          <input type="file" onChange={handleEcgFileChange} className="form-control" />
        </div>

        {/* HEA File Upload */}
        <div className="mt-3">
          <label className="font-weight-bold">Upload Corresponding .hea File:</label>
          <input type="file" onChange={handleHeaFileChange} className="form-control" />
        </div>

        {/* Upload Button */}
        {!loading && (
          <button onClick={handleUpload} className="btn btn-primary btn-lg mt-4 w-100">
            Upload & Analyze
          </button>
        )}

        {/* Loading Indicator */}
        {loading && (
          <div className="text-center mt-3">
            <div className="spinner-border text-primary" style={{ width: "3rem", height: "3rem" }} role="status"></div>
            <p className="mt-2 font-weight-bold">Processing your ECG file, please wait...</p>
          </div>
        )}

        {/* Error Message */}
        {error && <div className="alert alert-danger mt-3 text-center">{error}</div>}

        {/* 📈 ECG Waveform Image */}
        {ecgWaveform && (
          <div className="card p-4 mt-4 text-center">
            <h4 className="text-dark">📈 ECG Waveform</h4>
            <img src={`data:image/png;base64,${ecgWaveform}`} alt="ECG Waveform" className="img-fluid rounded w-100" />
          </div>
        )}

        {/* 📊 Final Prediction Summary + AHI Table */}
        {predictionSummary && (
          <div className="row mt-4">
            {/* Prediction Summary */}
            <div className="col-md-6">
              <div className="card p-4 text-center">
                <h4 className="text-dark">📊 Final Prediction Summary</h4>
                <p><strong>Total Segments:</strong> {predictionSummary.total_segments}</p>
                <p><strong>Apnea Segments:</strong> {predictionSummary.apnea_segments}</p>
                <p><strong>Normal Segments:</strong> {predictionSummary.normal_segments}</p>
                <h4><strong>AHI:</strong> {ahi.toFixed(2)} events/hour</h4>
                <h5><strong>Severity:</strong> <span className="badge bg-danger">{severity}</span></h5>
              </div>
            </div>

            {/* AHI Severity Table */}
            <div className="col-md-6">
              <div className="card p-4 text-center">
                <h4 className="text-dark">📋 AHI Severity Levels</h4>
                <table className="table table-bordered mt-3">
                  <thead className="thead-light">
                    <tr>
                      <th>AHI Range</th>
                      <th>Severity</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr><td>0 – 5</td><td>Normal</td></tr>
                    <tr><td>5 – 15</td><td>Mild</td></tr>
                    <tr><td>15 – 30</td><td>Moderate</td></tr>
                    <tr><td> &gt; 30</td><td>Severe</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadECG;
