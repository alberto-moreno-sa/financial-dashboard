import { queryOptions } from "@tanstack/react-query";
import { apiClient } from "~/shared/api/client";
import { type HistoryResponse } from "../model/types";

export const historyQueries = {
  chart: () =>
    queryOptions({
      queryKey: ["history", "chart"],
      queryFn: async () => (await apiClient.get<HistoryResponse>("/dashboard/chart")).data,
    }),
};
