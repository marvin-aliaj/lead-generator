import { notFound } from "next/navigation";
import { getCustomerInfo } from "./actions";
import FeedbackForm from "@/components/FeedbackForm";

export default async function FeedbackPage({
  params,
}: {
  params: Promise<{ cid: string }>;
}) {
  const { cid } = await params;

  let customer;
  try {
    customer = await getCustomerInfo(cid);
  } catch (error) {
    notFound();
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 py-8 px-4">
      <div className="max-w-md mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-8 h-8 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"
                />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              Help Us Improve
            </h1>
            <p className="text-gray-600">
              Hi {customer.name}! We'd love your feedback about your experience
              at {customer.restaurant_name}.
            </p>
          </div>

          <FeedbackForm customerId={cid} />
        </div>
      </div>
    </div>
  );
}
