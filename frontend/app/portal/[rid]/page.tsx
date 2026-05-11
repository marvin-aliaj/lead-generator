import { notFound } from "next/navigation";
import { getRestaurant } from "./actions";
import PortalForm from "@/components/PortalForm";

export default async function PortalPage({
  params,
}: {
  params: Promise<{ rid: string }>;
}) {
  const { rid } = await params;
  
  let restaurant;
  try {
    restaurant = await getRestaurant(rid);
  } catch (error) {
    notFound();
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-md mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
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
                  d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"
                />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              Welcome to {restaurant.name}
            </h1>
            <p className="text-gray-600">
              Please fill in your details to access free WiFi
            </p>
          </div>

          <PortalForm restaurantId={rid} />
        </div>
      </div>
    </div>
  );
}
