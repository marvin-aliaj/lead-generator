"use server";

const FASTAPI_URL = process.env.FASTAPI_URL || "http://localhost:8000";

export async function trackReviewClick(cid: string) {
  try {
    const response = await fetch(`${FASTAPI_URL}/review?cid=${cid}`, {
      redirect: "manual",
    });

    // Get the redirect URL from response
    if (response.status === 307 || response.status === 308) {
      const redirectUrl = response.headers.get("location");
      if (redirectUrl) {
        return { reviewUrl: redirectUrl };
      }
    }

    // Fallback: parse response body for URL
    const data = await response.json();
    return { reviewUrl: data.review_url || data.url };
  } catch (error) {
    console.error("Error tracking review click:", error);
    throw error;
  }
}
