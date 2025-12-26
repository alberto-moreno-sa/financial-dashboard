import { apiClient } from "~/shared/api/client";

export interface SnapshotSummary {
  id: string;
  snapshot_date: string;
  total_value: number;
  equity_value: number;
  fixed_income_value: number;
  cash_value: number;
  total_change: number | null;
  total_change_percent: number | null;
  created_at: string;
}

export interface SnapshotHistoryResponse {
  snapshots: SnapshotSummary[];
  total_count: number;
}

export async function getSnapshotHistory(limit: number = 12): Promise<SnapshotHistoryResponse> {
  const response = await apiClient.get<SnapshotHistoryResponse>(
    `/import/history?limit=${limit}`
  );
  return response.data;
}
