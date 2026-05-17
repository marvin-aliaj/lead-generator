import { redirect, notFound } from "next/navigation";
import { trackReviewClick } from "./actions";

export default async function ReviewPage({
  params,
}: {
  params: Promise<{ cid: string }>;
}) {
  const { cid } = await params;

  let result;
  try {
    result = await trackReviewClick(cid);
  } catch (error) {
    console.error("Error tracking review click:", error);
    notFound();
  }

  if (result?.reviewUrl) {
    redirect(result.reviewUrl);
  }

  notFound();
}
