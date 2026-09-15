import React, { useEffect, useState } from "react";

const API = "https://secret-leak-detector-idzg.onrender.com";
function App() {
  const [metrics, setMetrics] = useState({
    total_scans: 0,
    total_findings: 0,
    critical_findings: 0,
    high_findings: 0,
    medium_findings: 0,
    clean_scans: 0,
  });

  const [findings, setFindings] = useState([]);

  const [directory, setDirectory] = useState(
    "tests/sample_secrets"
  );

  const [message, setMessage] = useState("");

  async function loadDashboard() {
    try {
      const metricsResponse = await fetch(
        `${API}/metrics/`
      );

      const findingsResponse = await fetch(
        `${API}/findings/`
      );

      if (
        !metricsResponse.ok ||
        !findingsResponse.ok
      ) {
        throw new Error("API error");
      }

      const metricsData =
        await metricsResponse.json();

      const findingsData =
        await findingsResponse.json();

      setMetrics(metricsData);

      setFindings(
        findingsData.findings || []
      );

    } catch (error) {
      setMessage(
        "❌ Cannot connect to backend API."
      );
    }
  }

  async function runScan() {
    setMessage("🔍 Scanning...");

    try {
      const response = await fetch(
        `${API}/scan/`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            directory: directory,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Scan failed");
      }

      const data =
        await response.json();

      if (data.error) {
        setMessage(
          `❌ ${data.error}`
        );

        return;
      }

      if (
        data.total_findings === 0
      ) {
        setMessage(
          "✅ Scan completed. No secrets found."
        );
      } else {
        setMessage(
          `🚨 Scan completed. ${data.total_findings} finding(s) detected.`
        );
      }

      await loadDashboard();

    } catch (error) {
      setMessage(
        "❌ Scan failed. Check the backend API."
      );
    }
  }

  async function clearHistory() {
    const confirmed = window.confirm(
      "Are you sure you want to clear all scan history?"
    );

    if (!confirmed) {
      return;
    }

    try {
      const response = await fetch(
        `${API}/metrics/clear`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error(
          "Failed to clear data"
        );
      }

      setMessage(
        "🗑️ Scan history cleared successfully."
      );

      await loadDashboard();

    } catch (error) {
      setMessage(
        "❌ Failed to clear scan history."
      );
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  return (
    <div className="app">

      <header className="header">

        <div>
          <h1>
            🔐 Secret Leak Detector
          </h1>

          <p>
            Developer Security & Secret
            Scanning Dashboard
          </p>
        </div>

        <div className="status">
          ● API ONLINE
        </div>

      </header>

      <main className="main">

        {/* STATISTICS */}

        <section className="cards">

          <div className="card">
            <span>
              Total Scans
            </span>

            <strong>
              {metrics.total_scans}
            </strong>
          </div>

          <div className="card">
            <span>
              Total Findings
            </span>

            <strong>
              {metrics.total_findings}
            </strong>
          </div>

          <div className="card">
            <span>
              Critical
            </span>

            <strong>
              {metrics.critical_findings}
            </strong>
          </div>

          <div className="card">
            <span>
              High
            </span>

            <strong>
              {metrics.high_findings}
            </strong>
          </div>

          <div className="card">
            <span>
              Clean Scans
            </span>

            <strong>
              {metrics.clean_scans}
            </strong>
          </div>

        </section>


        {/* SCANNER */}

        <section className="panel">

          <div className="section-title">

            <h2>
              🔍 Scan Repository
            </h2>

            <button
              className="clear-button"
              onClick={clearHistory}
            >
              🗑️ Clear History
            </button>

          </div>

          <div className="scan-row">

            <input
              value={directory}
              onChange={(event) =>
                setDirectory(
                  event.target.value
                )
              }
              placeholder="Enter directory or GitHub URL"
            />

            <button
              onClick={runScan}
            >
              Scan Now
            </button>

          </div>

          {message && (
            <p className="message">
              {message}
            </p>
          )}

        </section>


        {/* FINDINGS */}

        <section className="panel">

          <div className="section-title">

            <h2>
              🚨 Security Findings
            </h2>

            <span>
              {findings.length} finding(s)
            </span>

          </div>


          {findings.length === 0 ? (

            <div className="empty">

              <div className="empty-icon">
                ✅
              </div>

              <h3>
                No secrets detected
              </h3>

              <p>
                Your scanned code is
                currently clean.
              </p>

            </div>

          ) : (

            <div className="table-container">

              <table>

                <thead>

                  <tr>

                    <th>
                      File
                    </th>

                    <th>
                      Line
                    </th>

                    <th>
                      Type
                    </th>

                    <th>
                      Severity
                    </th>

                    <th>
                      Detection
                    </th>

                    <th>
                      Confidence
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {findings.map(
                    (finding) => (

                      <tr
                        key={finding.id}
                      >

                        <td>
                          {finding.file}
                        </td>

                        <td>
                          {finding.line}
                        </td>

                        <td>
                          {finding.type}
                        </td>

                        <td>

                          <span
                            className={
                              `badge ${finding.severity.toLowerCase()}`
                            }
                          >
                            {finding.severity}
                          </span>

                        </td>

                        <td>
                          {finding.detection}
                        </td>

                        <td>
                          {(
                            finding.confidence *
                            100
                          ).toFixed(0)}
                          %
                        </td>

                      </tr>

                    )
                  )}

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