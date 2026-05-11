"use client";

import { useState, FormEvent } from "react";
import { submitFeedback } from "@/app/feedback/[cid]/actions";

const IMPROVEMENT_AREAS = [
  { id: "food", label: "Food Quality" },
  { id: "service", label: "Service" },
  { id: "speed", label: "Speed" },
  { id: "atmosphere", label: "Atmosphere" },
  { id: "price", label: "Price" },
];

export default function FeedbackForm({ customerId }: { customerId: string }) {
  const [rating, setRating] = useState(0);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [improvementAreas, setImprovementAreas] = useState<string[]>([]);
  const [comment, setComment] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    if (rating === 0) {
      setError("Please select a rating");
      return;
    }

    if (improvementAreas.length === 0) {
      setError("Please select at least one area for improvement");
      return;
    }

    setIsSubmitting(true);

    try {
      await submitFeedback({
        customer_id: customerId,
        rating,
        improvement_areas: improvementAreas,
        comment: comment.trim() || undefined,
      });

      setIsSuccess(true);
    } catch (err) {
      setError("Failed to submit feedback. Please try again.");
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const toggleImprovementArea = (area: string) => {
    setImprovementAreas((prev) =>
      prev.includes(area)
        ? prev.filter((a) => a !== area)
        : [...prev, area]
    );
  };

  if (isSuccess) {
    return (
      <div className="text-center py-8">
        <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
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
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          Thank You!
        </h2>
        <p className="text-gray-600">
          Your feedback has been submitted. We appreciate you taking the time to
          help us improve!
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          How would you rate your experience? *
        </label>
        <div className="flex justify-center gap-2">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              type="button"
              onClick={() => setRating(star)}
              onMouseEnter={() => setHoveredRating(star)}
              onMouseLeave={() => setHoveredRating(0)}
              className="transition-transform hover:scale-110"
              disabled={isSubmitting}
            >
              <svg
                className={`w-12 h-12 ${
                  star <= (hoveredRating || rating)
                    ? "text-yellow-400 fill-current"
                    : "text-gray-300"
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                />
              </svg>
            </button>
          ))}
        </div>
        {rating > 0 && (
          <p className="text-center text-sm text-gray-600 mt-2">
            {rating === 5
              ? "Excellent!"
              : rating === 4
              ? "Good"
              : rating === 3
              ? "Average"
              : rating === 2
              ? "Below Average"
              : "Poor"}
          </p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          What areas could we improve? * (Select all that apply)
        </label>
        <div className="space-y-2">
          {IMPROVEMENT_AREAS.map((area) => (
            <button
              key={area.id}
              type="button"
              onClick={() => toggleImprovementArea(area.id)}
              disabled={isSubmitting}
              className={`w-full px-4 py-3 rounded-lg border-2 transition-colors text-left ${
                improvementAreas.includes(area.id)
                  ? "border-purple-600 bg-purple-50 text-purple-800"
                  : "border-gray-300 bg-white text-gray-700 hover:border-purple-300"
              }`}
            >
              <span className="flex items-center">
                <span
                  className={`w-5 h-5 rounded border-2 mr-3 flex items-center justify-center ${
                    improvementAreas.includes(area.id)
                      ? "border-purple-600 bg-purple-600"
                      : "border-gray-300"
                  }`}
                >
                  {improvementAreas.includes(area.id) && (
                    <svg
                      className="w-3 h-3 text-white"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={3}
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  )}
                </span>
                {area.label}
              </span>
            </button>
          ))}
        </div>
      </div>

      <div>
        <label
          htmlFor="comment"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Additional Comments (Optional)
        </label>
        <textarea
          id="comment"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          rows={4}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none resize-none text-gray-800"
          placeholder="Tell us more about your experience..."
          disabled={isSubmitting}
        />
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-purple-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {isSubmitting ? "Submitting..." : "Submit Feedback"}
      </button>
    </form>
  );
}
