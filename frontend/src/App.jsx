import React, { useEffect, useState } from "react";


const API = "http://127.0.0.1:8000";

function App() {
  const [metrics, setMetrics] = useState(null);
  const [findings, setFindings] = useState([]);
  const [directory, setDirectory] = useState("tests/sample_secrets");
  const [message, setMessage] = useState("");

  async function loadDashboard() {
    try {
      const metricsResponse = await fetch(`${API}/metrics/`);
      const findingsResponse = await fetch(`${API}/findings/`);

      const metricsData = await metricsResponse.json();
      const findingsData = await findingsResponse.json();

      setMetrics(metricsData);
      setFindings(findingsData.findings || []);
    } catch (error) {
      setMessage("❌ Backend API is not reachable.");
    }
  }

  async function runScan() {
    setMessage("🔍 Scanning...");

    try {
      const response = await fetch(`${API}/scan/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ directory }),
      });

      if (!response.ok) {
        throw new Error("Scan failed");
      }

      const data = await response.json();

      setMessage(
        data.total_findings === 0
          ? "✅ No secrets found."
          : `🚨 ${data.total_findings} potential secret(s) found!`
      );

      await loadDashboard();
    } catch (error) {
      setMessage("❌ Scan failed. Check the backend.");
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  return (
    <div className="app">
      <header>
        <div>
          <h1>🔐 Secret Leak Detector</h1>
          <p>Developer Security & Secret Scanning Dashboard</p>
        </div>

        <span className="status">● API ONLINE</span>
      </header>

      <main>
        <section className="cards">
          <div className="card">
            <span>Total Scans</span>
            <strong>{metrics?.total_scans ?? 0}</strong>
          </div>

          <div className="card danger">
            <span>Total Findings</span>
            <strong>{metrics?.total_findings ?? 0}</strong>
          </div>

          <div className="card critical">
            <span>Critical</span>
            <strong>{metrics?.critical_findings ?? 0}</strong>
          </div>

          <div className="card high">
            <span>High</span>
            <strong>{metrics?.high_findings ?? 0}</strong>
          </div>

          <div className="card safe">
            <span>Clean Scans</span>
            <strong>{metrics?.clean_scans ?? 0}</strong>
          </div>
        </section>

        <section className="scan-panel">
          <h2>🔍 Scan Repository</h2>

          <div className="scan-row">
            <input
              value={directory}
              onChange={(event) => setDirectory(event.target.value)}
              placeholder="Directory path"
            />

            <button onClick={runScan}>
              Scan Now
            </button>
          </div>

          {message && <p className="message">{message}</p>}
        </section>

        <section className="findings">
          <div className="section-title">
            <h2>🚨 Security Findings</h2>
            <span>{findings.length} findings</span>
          </div>

          {findings.length === 0 ? (
            <div className="empty">
              <div>✅</div>
              <h3>No secrets detected</h3>
              <p>Your scanned code is currently clean.</p>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>File</th>
                    <th>Line</th>
                    <th>Type</th>
                    <th>Severity</th>
                    <th>Detection</th>
                    <th>Confidence</th>
                  </tr>
                </thead>

                <tbody>
                  {findings.map((finding) => (
                    <tr key={finding.id}>
                      <td>{finding.file}</td>
                      <td>{finding.line}</td>
                      <td>{finding.type}</td>
                      <td>
                        <span
                          className={`badge ${finding.severity.toLowerCase()}`}
                        >
                          {finding.severity}
                        </span>
                      </td>
                      <td>{finding.detection}</td>
                      <td>
                        {(finding.confidence * 100).toFixed(0)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;