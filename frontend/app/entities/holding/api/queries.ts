import { queryOptions } from "@tanstack/react-query";
import { apiClient } from "~/shared/api/client";
import { type Holding } from "../model/types";

export const holdingsQueries = {
  list: () =>
    queryOptions({
      queryKey: ["holdings", "list"],
      queryFn: async () => (await apiClient.get<{ items: Holding[] }>("/portfolio/transactions")).data,
    }),
};
