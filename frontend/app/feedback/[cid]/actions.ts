"use server";

const FASTAPI_URL = process.env.FASTAPI_URL || "http://localhost:8000";

export async function getCustomerInfo(cid: string) {
  try {
    const response = await fetch(`${FASTAPI_URL}/customer/${cid}`);
    if (!response.ok) {
      throw new Error("Customer not found");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching customer info:", error);
    throw error;
  }
}

export async function submitFeedback(data: {
  customer_id: string;
  rating: number;
  improvement_areas: string[];
  comment?: string;
}) {
  try {
    const response = await fetch(`${FASTAPI_URL}/feedback`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error("Failed to submit feedback");
    }

    return await response.json();
  } catch (error) {
    console.error("Error submitting feedback:", error);
    throw error;
  }
}
