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