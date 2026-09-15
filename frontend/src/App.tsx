import { useEffect, useState } from "react";
import { getDrivers, getDriverPace } from "./api";

function App() {
  const [drivers, setDrivers] = useState<any[]>([]);
  const [paceData, setPaceData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getDrivers(),
      getDriverPace(),
    ])
      .then(([driverData, paceData]) => {
        setDrivers(driverData);
        setPaceData(paceData);
      })
      .catch((error) => {
        console.error("Failed to load dashboard data:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          RACE<span>MIND</span>
        </div>

        <nav>
          <a className="active">Dashboard</a>
          <a>Races</a>
          <a>Drivers</a>
          <a>Strategy</a>
          <a>AI Analyst</a>
        </nav>

        <div className="sidebar-footer">
          <p>2025 Season</p>
          <span>Monaco Grand Prix</span>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">RACE ANALYTICS</p>
            <h1>Monaco Grand Prix</h1>
          </div>

          <div className="race-status">
            <span className="status-dot"></span>
            Race Complete
          </div>
        </header>

        <section className="overview">
          <div className="section-heading">
            <div>
              <p className="eyebrow">2025 MONACO GP</p>
              <h2>Race Overview</h2>
            </div>

            <button>View Full Race</button>
          </div>

          <div className="driver-grid">
            {loading ? (
              <p>Loading drivers...</p>
            ) : (
              drivers.slice(0, 3).map((driver, index) => (
                <div className="driver-card" key={driver.id}>
                  <div className="driver-position">
                    {String(index + 1).padStart(2, "0")}
                  </div>

                  <div>
                    <p className="driver-code">
                      {driver.abbreviation}
                    </p>

                    <h3>{driver.full_name}</h3>

                    <p className="team">
                      {driver.team_name}
                    </p>
                  </div>

                  <div className="pace">
                    <span>DRIVER</span>
                    <strong>{driver.abbreviation}</strong>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>

        <section className="analysis-grid">
          <div className="panel">
            <div className="panel-header">
              <div>
                <p className="eyebrow">PERFORMANCE</p>
                <h2>Driver Pace</h2>
              </div>

              <span className="panel-label">
                SECONDS / LAP
              </span>
            </div>

            <div className="pace-list">
              {paceData.slice(0, 5).map((driver) => (
                <div
                  className="pace-row"
                  key={driver.Driver}
                >
                  <span>{driver.Driver}</span>

                  <div className="bar">
                    <div
                      className="bar-fill"
                      style={{
                        width: `${Math.max(
                          20,
                          100 -
                            (driver.AverageLapTime - 75) * 20
                        )}%`,
                      }}
                    ></div>
                  </div>

                  <strong>
                    {driver.AverageLapTime.toFixed(3)}
                  </strong>
                </div>
              ))}
            </div>
          </div>

          <div className="panel ai-panel">
            <div className="panel-header">
              <div>
                <p className="eyebrow">RACEMIND AI</p>
                <h2>Race Analyst</h2>
              </div>

              <span className="ai-badge">AI</span>
            </div>

            <p className="ai-text">
              RaceMind combines race pace, tyre behaviour,
              stint data, pit stops, and strategy simulations
              to analyse Formula 1 race performance.
            </p>

            <button className="ai-button">
              Open AI Analyst →
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;

