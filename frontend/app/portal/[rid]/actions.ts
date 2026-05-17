"use server";

const FASTAPI_URL = process.env.FASTAPI_URL || "http://localhost:8000";

export async function getRestaurant(rid: string) {
  try {
    const response = await fetch(`${FASTAPI_URL}/restaurant/${rid}`);
    if (!response.ok) {
      throw new Error("Restaurant not found");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching restaurant:", error);
    throw error;
  }
}

export async function submitCheckin(data: {
  name: string;
  phone: string;
  email?: string;
  restaurant_id: string;
}) {
  try {
    const response = await fetch(`${FASTAPI_URL}/checkin`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error("Failed to submit checkin");
    }

    return await response.json();
  } catch (error) {
    console.error("Error submitting checkin:", error);
    throw error;
  }
}
