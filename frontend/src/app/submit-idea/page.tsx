"use client";
import { useState } from "react";
import axios from "axios";

interface ValidationResponse {
  marketDemand: string;
  competitors: string[];
  pricingStrategy: string;
  growthPotential: string;
  aiAnalysis: string;
}

const SubmitIdea: React.FC = () => {
  const [idea, setIdea] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [response, setResponse] = useState<ValidationResponse | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);

    try {
      const res = await axios.post<ValidationResponse>(
        "http://localhost:8000/validate",
        { idea },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setResponse(res.data);
    } catch (error) {
      console.error("Error submitting idea:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Submit Your Idea</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          placeholder="Enter you idea here..."
          rows={5}
          className="w-full p-3 border border-gray-300 rounded-md mb-4"
        ></textarea>
        <button
          type="submit"
          className="bg-blue-500 text-white p-3 rounded-md"
          disabled={loading}
        >
          {loading ? "Validating..." : "Validate Idea"}
        </button>
      </form>

      {response && (
        <div className="mt-6">
          <h2 className="text-2xl font-semibold mb-4">Validation Result</h2>
          <div className="overflow-auto">
            <table className="min-w-full bg-white border border-gray-300 rounded-md">
              <tbody>
                <tr className="border-b">
                  <td className="p-3 font-semibold">Market Demand:</td>
                  <td className="p-3">{response.marketDemand}</td>
                </tr>
                <tr className="border-b">
                  <td className="p-3 font-semibold">Competitors:</td>
                  <td className="p-3">
                    {response.competitors && response.competitors.length > 0
                      ? response.competitors.join(", ")
                      : "None"}
                  </td>
                </tr>
                <tr className="border-b">
                  <td className="p-3 font-semibold">Pricing Strategy:</td>
                  <td className="p-3">{response.pricingStrategy}</td>
                </tr>
                <tr className="border-b">
                  <td className="p-3 font-semibold">Growth Potential:</td>
                  <td className="p-3">{response.growthPotential}</td>
                </tr>
                <tr>
                  <td className="p-3 font-semibold">AI Analysis:</td>
                  <td className="p-3">{response.aiAnalysis}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default SubmitIdea;
