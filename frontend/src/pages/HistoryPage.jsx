import React, { useState, useEffect } from "react";
import { Container, Table, Badge, Card, Spinner, Alert, Button } from "react-bootstrap";
import axios from "axios";
import { Link } from "react-router-dom";

function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
      const response = await axios.get(`${baseUrl}/history`);
      setHistory(response.data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch history. Please ensure the backend server is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityBadge = (severity) => {
    if (severity.includes("Normal")) return <Badge bg="success">Normal</Badge>;
    if (severity.includes("Mild")) return <Badge bg="warning" className="text-dark">Mild</Badge>;
    if (severity.includes("Moderate")) return <Badge bg="warning">Moderate</Badge>;
    if (severity.includes("Severe")) return <Badge bg="danger">Severe</Badge>;
    return <Badge bg="secondary">{severity}</Badge>;
  };

  return (
    <Container className="mt-5 pt-4 animate-fade-in mb-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 style={{ fontWeight: "800", fontSize: "2.5rem", color: "var(--dark)" }}>Assessment History</h1>
          <p className="text-muted">Review your last 5 ECG analysis results</p>
        </div>
        <Button variant="outline-primary" onClick={fetchHistory} disabled={loading}>
          {loading ? <Spinner animation="border" size="sm" /> : "🔄 Refresh"}
        </Button>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      <Card className="border-0 shadow-sm overflow-hidden">
        {loading ? (
          <div className="text-center p-5">
            <Spinner animation="border" variant="primary" />
            <p className="mt-3 text-muted">Loading history...</p>
          </div>
        ) : history.length > 0 ? (
          <div className="table-responsive">
            <Table hover className="mb-0">
              <thead>
                <tr>
                  <th className="px-4 py-3">Timestamp</th>
                  <th className="px-4 py-3">Filename</th>
                  <th className="px-4 py-3">AHI Index</th>
                  <th className="px-4 py-3">Severity</th>
                  <th className="px-4 py-3 text-center">Summary (Apnea/Total)</th>
                </tr>
              </thead>
              <tbody>
                {history.map((record, index) => (
                  <tr key={index}>
                    <td className="px-4 py-3 text-muted" style={{ fontSize: "0.9rem" }}>{record.timestamp}</td>
                    <td className="px-4 py-3 font-weight-bold">{record.filename}</td>
                    <td className="px-4 py-3">
                      <span style={{ fontWeight: "700", color: "var(--primary)" }}>{record.AHI.toFixed(2)}</span>
                    </td>
                    <td className="px-4 py-3">{getSeverityBadge(record.Severity)}</td>
                    <td className="px-4 py-3 text-center">
                      <Badge bg="light" text="dark" className="border">
                        {record.prediction_summary.apnea_segments} / {record.prediction_summary.total_segments}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        ) : (
          <div className="text-center p-5">
            <div className="mb-3" style={{ fontSize: "3rem", opacity: 0.3 }}>📂</div>
            <h5>No history found</h5>
            <p className="text-muted">Conduct an ECG analysis to see results here.</p>
            <Link to="/analysis" className="btn btn-primary mt-3">Start Analysis</Link>
          </div>
        )}
      </Card>
    </Container>
  );
}

export default HistoryPage;
