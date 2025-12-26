import { apiClient } from "~/shared/api/client";

export interface HealthCheckResponse {
  status: string;
  environment: string;
  timestamp: string;
  database: string;
  version: string;
}

export const checkHealth = async (): Promise<HealthCheckResponse> => {
  const response = await apiClient.get("/health");
  return response.data;
};
