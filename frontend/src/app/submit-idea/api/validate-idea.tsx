import { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === "POST") {
    // const { idea } = req.body;
    // Just a dummy response for now
    const response = {
      marketDemand: "High",
      competitors: ["Competitor A", "Competitor B"],
      pricingStrategy: "Freemium",
      growthPotential: "Moderate",
    };

    return res.status(200).json(response);
  } else {
    return res.status(405).json({ error: "Method Not Allowed" });
  }
}
