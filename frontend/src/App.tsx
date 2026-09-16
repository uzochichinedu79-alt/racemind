import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import {
  getDrivers,
  getDriverPace,
  getDriverStints,
  compareStrategies,
  analyzeDrivers,
} from "./api";

function App() {
  const [drivers, setDrivers] = useState<any[]>([]);
  const [paceData, setPaceData] = useState<any[]>([]);
  const [stintData, setStintData] = useState<any[]>([]);
  const [strategyData, setStrategyData] =
    useState<any[]>([]);

  const [selectedDriver, setSelectedDriver] =
    useState("NOR");

  const [driverA, setDriverA] =
    useState("NOR");

  const [driverB, setDriverB] =
    useState("PIA");

  const [aiAnalysis, setAiAnalysis] =
    useState("");

  const [loading, setLoading] = useState(true);
  const [stintLoading, setStintLoading] =
    useState(false);
  const [strategyLoading, setStrategyLoading] =
    useState(false);
  const [aiLoading, setAiLoading] =
    useState(false);

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
        console.error(
          "Failed to load dashboard data:",
          error
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    setStintLoading(true);
    setStrategyLoading(true);

    Promise.all([
      getDriverStints(selectedDriver),
      compareStrategies(selectedDriver),
    ])
      .then(([stints, strategies]) => {
        setStintData(stints);
        setStrategyData(
          strategies.strategies
        );
      })
      .catch((error) => {
        console.error(
          "Failed to load strategy data:",
          error
        );

        setStintData([]);
        setStrategyData([]);
      })
      .finally(() => {
        setStintLoading(false);
        setStrategyLoading(false);
      });
  }, [selectedDriver]);

  async function handleAiAnalysis() {
    setAiLoading(true);
    setAiAnalysis("");

    try {
      const result = await analyzeDrivers(
        driverA,
        driverB
      );

      setAiAnalysis(result.analysis);
    } catch (error) {
      console.error(
        "AI analysis failed:",
        error
      );

      setAiAnalysis(
        "Unable to generate analysis. Please try again."
      );
    } finally {
      setAiLoading(false);
    }
  }

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
            <p className="eyebrow">
              RACE ANALYTICS
            </p>

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
              <p className="eyebrow">
                2025 MONACO GP
              </p>

              <h2>Race Overview</h2>
            </div>

            <button>
              View Full Race
            </button>
          </div>

          <div className="driver-grid">
            {loading ? (
              <p>Loading drivers...</p>
            ) : (
              drivers
                .slice(0, 3)
                .map((driver, index) => (
                  <div
                    className="driver-card"
                    key={driver.id}
                  >
                    <div className="driver-position">
                      {String(index + 1).padStart(
                        2,
                        "0"
                      )}
                    </div>

                    <div>
                      <p className="driver-code">
                        {driver.abbreviation}
                      </p>

                      <h3>
                        {driver.full_name}
                      </h3>

                      <p className="team">
                        {driver.team_name}
                      </p>
                    </div>

                    <div className="pace">
                      <span>DRIVER</span>

                      <strong>
                        {driver.abbreviation}
                      </strong>
                    </div>
                  </div>
                ))
            )}
          </div>
        </section>

        <section className="analysis-grid">
          <div className="panel pace-panel">
            <div className="panel-header">
              <div>
                <p className="eyebrow">
                  PERFORMANCE
                </p>

                <h2>Driver Pace</h2>
              </div>

              <span className="panel-label">
                AVERAGE LAP TIME
              </span>
            </div>

            <div className="chart-container">
              {loading ? (
                <p>
                  Loading pace data...
                </p>
              ) : (
                <ResponsiveContainer
                  width="100%"
                  height={300}
                >
                  <BarChart
                    data={paceData}
                    margin={{
                      top: 10,
                      right: 10,
                      left: 0,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid
                      strokeDasharray="3 3"
                      vertical={false}
                    />

                    <XAxis
                      dataKey="Driver"
                      tick={{
                        fontSize: 11,
                      }}
                      axisLine={false}
                      tickLine={false}
                    />

                    <YAxis
                      domain={[
                        "dataMin - 0.5",
                        "dataMax + 0.5",
                      ]}
                      tick={{
                        fontSize: 10,
                      }}
                      axisLine={false}
                      tickLine={false}
                      width={45}
                    />

                    <Tooltip
                      formatter={(value) => [
                        `${Number(value).toFixed(
                          3
                        )} s`,
                        "Average Lap",
                      ]}
                      cursor={{
                        fill:
                          "rgba(0, 0, 0, 0.04)",
                      }}
                    />

                    <Bar
                      dataKey="AverageLapTime"
                      radius={[
                        4,
                        4,
                        0,
                        0,
                      ]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>

          <div className="panel ai-panel">
            <div className="panel-header">
              <div>
                <p className="eyebrow">
                  RACEMIND AI
                </p>

                <h2>Race Analyst</h2>
              </div>

              <span className="ai-badge">
                AI
              </span>
            </div>

            <p className="ai-text">
              Compare drivers using real race
              pace, consistency, stint strategy,
              pit stops, and tyre degradation.
            </p>

            <button
              className="ai-button"
              onClick={() => {
                document
                  .getElementById("ai-analyst")
                  ?.scrollIntoView({
                    behavior: "smooth",
                  });
              }}
            >
              Open AI Analyst →
            </button>
          </div>
        </section>

        <section className="panel stint-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">
                RACE STRATEGY
              </p>

              <h2>Tyre Stints</h2>
            </div>

            <select
              value={selectedDriver}
              onChange={(event) =>
                setSelectedDriver(
                  event.target.value
                )
              }
              className="driver-select"
            >
              {drivers.map((driver) => (
                <option
                  key={driver.id}
                  value={driver.abbreviation}
                >
                  {driver.abbreviation}
                </option>
              ))}
            </select>
          </div>

          {stintLoading ? (
            <p>Loading stint data...</p>
          ) : stintData.length === 0 ? (
            <p>
              No stint data available.
            </p>
          ) : (
            <div className="stint-list">
              {stintData.map((stint) => (
                <div
                  className="stint-row"
                  key={`${stint.Driver}-${stint.Stint}`}
                >
                  <div className="stint-number">
                    STINT {stint.Stint}
                  </div>

                  <div className="stint-info">
                    <strong>
                      {stint.Compound}
                    </strong>

                    <span>
                      Laps {stint.StartLap}–
                      {stint.EndLap}
                    </span>
                  </div>

                  <div className="stint-bar">
                    <div
                      className="stint-bar-fill"
                      style={{
                        width: `${Math.min(
                          100,
                          (stint.Laps /
                            30) *
                            100
                        )}%`,
                      }}
                    ></div>
                  </div>

                  <div className="stint-laps">
                    <strong>
                      {stint.Laps}
                    </strong>

                    <span>
                      laps
                    </span>
                  </div>

                  <div className="stint-age">
                    <span>
                      AVG TYRE AGE
                    </span>

                    <strong>
                      {Number(
                        stint.AverageTyreLife
                      ).toFixed(1)}
                    </strong>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="panel strategy-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">
                STRATEGY SIMULATION
              </p>

              <h2>
                Strategy Comparison
              </h2>
            </div>

            <span className="panel-label">
              {selectedDriver}
            </span>
          </div>

          {strategyLoading ? (
            <p>
              Running strategy simulation...
            </p>
          ) : strategyData.length === 0 ? (
            <p>
              No strategy results available.
            </p>
          ) : (
            <div className="strategy-list">
              {strategyData.map(
                (strategy) => (
                  <div
                    className="strategy-card"
                    key={strategy.Strategy}
                  >
                    <div className="strategy-main">
                      <div>
                        <span className="strategy-name">
                          {strategy.Strategy}
                        </span>

                        <p className="strategy-tyres">
                          {strategy.Tyres}
                        </p>
                      </div>

                      <span
                        className={
                          strategy.Status ===
                          "Valid"
                            ? "strategy-status valid"
                            : "strategy-status rejected"
                        }
                      >
                        {strategy.Status}
                      </span>
                    </div>

                    {strategy.Status ===
                    "Valid" ? (
                      <div className="strategy-result">
                        <div>
                          <span>
                            ESTIMATED RACE TIME
                          </span>

                          <strong>
                            {strategy.EstimatedRaceTime.toFixed(
                              3
                            )}
                            s
                          </strong>
                        </div>

                        <div>
                          <span>
                            TIME DIFFERENCE
                          </span>

                          <strong>
                            {strategy.TimeDifference ===
                            0
                              ? "Fastest"
                              : `+${strategy.TimeDifference.toFixed(
                                  3
                                )} s`}
                          </strong>
                        </div>
                      </div>
                    ) : (
                      <div className="strategy-reason">
                        <span>
                          SIMULATION REJECTED
                        </span>

                        <p>
                          {strategy.Reason}
                        </p>
                      </div>
                    )}
                  </div>
                )
              )}
            </div>
          )}
        </section>

        <section
          className="panel ai-analyst-panel"
          id="ai-analyst"
        >
          <div className="panel-header">
            <div>
              <p className="eyebrow">
                RACEMIND AI
              </p>

              <h2>
                AI Driver Analyst
              </h2>
            </div>

            <span className="ai-badge">
              GEMINI
            </span>
          </div>

          <div className="ai-controls">
            <div>
              <label>
                DRIVER A
              </label>

              <select
                value={driverA}
                onChange={(event) =>
                  setDriverA(
                    event.target.value
                  )
                }
                className="driver-select"
              >
                {drivers.map((driver) => (
                  <option
                    key={driver.id}
                    value={driver.abbreviation}
                  >
                    {driver.abbreviation} —{" "}
                    {driver.full_name}
                  </option>
                ))}
              </select>
            </div>

            <div className="versus">
              VS
            </div>

            <div>
              <label>
                DRIVER B
              </label>

              <select
                value={driverB}
                onChange={(event) =>
                  setDriverB(
                    event.target.value
                  )
                }
                className="driver-select"
              >
                {drivers.map((driver) => (
                  <option
                    key={driver.id}
                    value={driver.abbreviation}
                  >
                    {driver.abbreviation} —{" "}
                    {driver.full_name}
                  </option>
                ))}
              </select>
            </div>

            <button
              className="analyse-button"
              onClick={handleAiAnalysis}
              disabled={aiLoading}
            >
              {aiLoading
                ? "Analysing..."
                : "Analyse Drivers"}
            </button>
          </div>

          {aiAnalysis && (
            <div className="ai-analysis-result">
              <div className="analysis-label">
                RACE ANALYST
              </div>

              <div className="analysis-text">
                {aiAnalysis}
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;