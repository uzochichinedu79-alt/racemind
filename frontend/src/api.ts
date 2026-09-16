const API_URL = "http://127.0.0.1:8000";

export async function getDrivers() {
  const response = await fetch(`${API_URL}/drivers/`);

  if (!response.ok) {
    throw new Error("Failed to fetch drivers");
  }

  return response.json();
}

export async function getDriverPace() {
  const response = await fetch(`${API_URL}/analytics/pace`);

  if (!response.ok) {
    throw new Error("Failed to fetch driver pace");
  }

  return response.json();
}

export async function getDriverStints(driver: string) {
  const response = await fetch(
    `${API_URL}/analytics/stints/${driver}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch driver stints");
  }

  return response.json();
}

export async function compareStrategies(
  driver: string
) {
  const response = await fetch(
    `${API_URL}/strategy/compare/${driver}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "Actual Strategy": [
          "MEDIUM",
          "HARD",
          "HARD",
        ],
        "One Stop": [
          "MEDIUM",
          "HARD",
        ],
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to compare strategies"
    );
  }

  return response.json();
}

export async function analyzeDrivers(
  driverA: string,
  driverB: string
) {
  const response = await fetch(
    `${API_URL}/ai/compare`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        driver_a: driverA,
        driver_b: driverB,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to analyse drivers"
    );
  }

  return response.json();
}