import { redirect, notFound } from "next/navigation";
import { trackReviewClick } from "./actions";

export default async function ReviewPage({
  params,
}: {
  params: Promise<{ cid: string }>;
}) {
  const { cid } = await params;

  try {
    const result = await trackReviewClick(cid);
    redirect(result.reviewUrl);
  } catch (error) {
    console.error("Error:", error);
    notFound();
  }
}
