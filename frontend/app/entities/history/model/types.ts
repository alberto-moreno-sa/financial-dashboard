export interface HistoryPoint {
  date: string;
  value: number;
}
export interface HistoryResponse {
  points: HistoryPoint[];
}
