import { apiClient } from "~/shared/api/client";

export interface PositionBreakdown {
  ticker: string;
  name: string;
  quantity: number;
  avg_cost: number;
  current_price: number;
  market_value: number;
  unrealized_gain: number;
  unrealized_gain_percent: number;
}

export interface PortfolioSummary {
  equity_value: number;  // RENTA VARIABLE
  fixed_income_value: number;  // DEUDA
  cash_value: number;  // EFECTIVO
  total_value: number;
}

export interface Metadata {
  filename: string;
  detected_date: string;
  account_holder: string;
  currency: string;
}

export interface PortfolioSnapshotResponse {
  status: string;
  metadata: Metadata;
  portfolio: PortfolioSummary;
  breakdown: PositionBreakdown[];
}

export async function uploadStatement(file: File): Promise<PortfolioSnapshotResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post<PortfolioSnapshotResponse>(
    "/import/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}

export interface SaveSnapshotResponse {
  status: string;
  snapshot_id: string;
  message: string;
  total_change: number | null;
  total_change_percent: number | null;
}

export async function saveSnapshot(
  snapshotData: PortfolioSnapshotResponse,
  fileHash: string
): Promise<SaveSnapshotResponse> {
  const response = await apiClient.post<SaveSnapshotResponse>(
    "/import/save-snapshot",
    {
      snapshot_data: {
        statement_date: snapshotData.metadata.detected_date,
        account_holder: snapshotData.metadata.account_holder,
        currency: snapshotData.metadata.currency,
        metadata: {
          filename: snapshotData.metadata.filename,
        },
        portfolio_summary: snapshotData.portfolio,
        breakdown: snapshotData.breakdown,
      },
      file_hash: fileHash,
    }
  );

  return response.data;
}

export interface FileUploadResult {
  filename: string;
  status: "success" | "duplicate" | "error";
  message: string;
  snapshot_date?: string;
  snapshot_id?: string;
  error_detail?: string;
}

export interface BulkUploadResponse {
  total_files: number;
  successful: number;
  duplicates: number;
  errors: number;
  results: FileUploadResult[];
}

export async function bulkUploadStatements(files: File[]): Promise<BulkUploadResponse> {
  const formData = new FormData();

  // Append all files to the form data
  files.forEach((file) => {
    formData.append("files", file);
  });

  const response = await apiClient.post<BulkUploadResponse>(
    "/import/bulk-upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}
