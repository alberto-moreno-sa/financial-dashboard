import { queryOptions } from "@tanstack/react-query";
import { apiClient } from "~/shared/api/client";
import { type PortfolioStats } from "../model/types";

export const portfolioQueries = {
  stats: () =>
    queryOptions({
      queryKey: ["portfolio", "stats"],
      queryFn: async () => (await apiClient.get<PortfolioStats>("/portfolio/dashboard/stats")).data,
    }),
};
