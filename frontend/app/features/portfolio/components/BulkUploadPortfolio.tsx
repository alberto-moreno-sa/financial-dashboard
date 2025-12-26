import { useState, useRef } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Upload, FileText, CheckCircle, XCircle, AlertCircle, Loader2 } from "lucide-react";
import { bulkUploadStatements, type BulkUploadResponse, type FileUploadResult } from "../api/uploadPortfolio";
import { Card, CardContent, CardHeader, CardTitle } from "~/shared/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/shared/ui/table";
import { toast } from "sonner";

export function BulkUploadPortfolio() {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadResults, setUploadResults] = useState<BulkUploadResponse | null>(null);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const queryClient = useQueryClient();

  const bulkUploadMutation = useMutation({
    mutationFn: (files: File[]) => bulkUploadStatements(files),
    onSuccess: (response) => {
      setUploadResults(response);

      // Show summary toast
      if (response.successful > 0) {
        toast.success(`${response.successful} files processed successfully`, {
          description: `Duplicates: ${response.duplicates}, Errors: ${response.errors}`,
        });
      } else if (response.duplicates > 0 && response.errors === 0) {
        toast.info("All files already exist", {
          description: `${response.duplicates} duplicates detected`,
        });
      } else {
        toast.error("Failed to process files", {
          description: `${response.errors} errors found`,
        });
      }

      // Invalidate queries to refresh dashboard
      if (response.successful > 0) {
        queryClient.invalidateQueries({ queryKey: ["portfolio"] });
        queryClient.invalidateQueries({ queryKey: ["holdings"] });
        queryClient.invalidateQueries({ queryKey: ["stats"] });
        queryClient.invalidateQueries({ queryKey: ["snapshot-history"] });
      }

      // Clear selected files
      setSelectedFiles([]);
    },
    onError: (error: any) => {
      const message = error?.response?.data?.detail || error?.message || "Error processing files";
      toast.error("Bulk upload error", {
        description: message,
      });
    },
  });

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    const pdfFiles = files.filter((f) => f.type === "application/pdf");

    if (pdfFiles.length === 0) {
      toast.error("Invalid file type", {
        description: "Please upload GBM PDF files",
      });
      return;
    }

    if (pdfFiles.length > 100) {
      toast.error("Too many files", {
        description: "Maximum 100 files per batch",
      });
      return;
    }

    setSelectedFiles(pdfFiles);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const pdfFiles = Array.from(files).filter((f) => f.type === "application/pdf");

      if (pdfFiles.length === 0) {
        toast.error("Invalid file type", {
          description: "Please upload GBM PDF files",
        });
        return;
      }

      if (pdfFiles.length > 100) {
        toast.error("Too many files", {
          description: "Maximum 100 files per batch",
        });
        return;
      }

      setSelectedFiles(pdfFiles);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleUpload = () => {
    if (selectedFiles.length === 0) return;
    bulkUploadMutation.mutate(selectedFiles);
  };

  const handleReset = () => {
    setSelectedFiles([]);
    setUploadResults(null);
    bulkUploadMutation.reset();
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "success":
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case "duplicate":
        return <AlertCircle className="h-5 w-5 text-yellow-600" />;
      case "error":
        return <XCircle className="h-5 w-5 text-red-600" />;
      default:
        return <Loader2 className="h-5 w-5 animate-spin text-blue-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "success":
        return "bg-green-50 border-green-200";
      case "duplicate":
        return "bg-yellow-50 border-yellow-200";
      case "error":
        return "bg-red-50 border-red-200";
      default:
        return "bg-gray-50 border-gray-200";
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="h-5 w-5" />
          Bulk Statement Upload
        </CardTitle>
        <p className="mt-2 text-sm text-gray-500">
          Upload multiple statements (up to 100 files) organized by year and period
        </p>
      </CardHeader>
      <CardContent>
        {/* Show results if upload completed */}
        {uploadResults ? (
          <div className="space-y-6">
            {/* Summary Card */}
            <div className="rounded-lg border border-blue-200 bg-blue-50 p-6">
              <div className="mb-4 flex items-center gap-2 text-blue-800">
                <CheckCircle className="h-5 w-5" />
                <h3 className="font-semibold">Processing Summary</h3>
              </div>

              <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
                <div className="rounded bg-white p-3">
                  <p className="text-xs text-gray-600">Total Files</p>
                  <p className="text-2xl font-bold text-gray-900">{uploadResults.total_files}</p>
                </div>
                <div className="rounded bg-white p-3">
                  <p className="text-xs text-gray-600">Successful</p>
                  <p className="text-2xl font-bold text-green-600">{uploadResults.successful}</p>
                </div>
                <div className="rounded bg-white p-3">
                  <p className="text-xs text-gray-600">Duplicates</p>
                  <p className="text-2xl font-bold text-yellow-600">{uploadResults.duplicates}</p>
                </div>
                <div className="rounded bg-white p-3">
                  <p className="text-xs text-gray-600">Errors</p>
                  <p className="text-2xl font-bold text-red-600">{uploadResults.errors}</p>
                </div>
              </div>
            </div>

            {/* Results Table */}
            <div className="rounded-lg border border-gray-200 bg-white">
              <div className="border-b border-gray-200 p-4">
                <h4 className="font-semibold text-gray-900">
                  Processing Detail ({uploadResults.results.length} files)
                </h4>
              </div>
              <div className="max-h-[500px] overflow-y-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Status</TableHead>
                      <TableHead>File</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Message</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {uploadResults.results.map((result, index) => (
                      <TableRow key={index} className={getStatusColor(result.status)}>
                        <TableCell>{getStatusIcon(result.status)}</TableCell>
                        <TableCell className="font-medium text-sm max-w-[200px] truncate">
                          {result.filename}
                        </TableCell>
                        <TableCell className="text-sm">
                          {result.snapshot_date || "-"}
                        </TableCell>
                        <TableCell className="text-sm">
                          <div className="flex flex-col gap-1">
                            <span>{result.message}</span>
                            {result.error_detail && (
                              <span className="text-xs text-gray-500">{result.error_detail}</span>
                            )}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </div>

            {/* Reset Button */}
            <div className="flex justify-end">
              <button
                onClick={handleReset}
                className="rounded-md bg-blue-600 px-6 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
              >
                Process More Files
              </button>
            </div>
          </div>
        ) : selectedFiles.length > 0 ? (
          /* File list and upload button */
          <div className="space-y-4">
            <div className="rounded-lg border border-gray-200 bg-gray-50 p-4">
              <h4 className="mb-3 font-semibold text-gray-900">
                Selected Files ({selectedFiles.length})
              </h4>
              <div className="max-h-[300px] space-y-2 overflow-y-auto">
                {selectedFiles.map((file, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-3 rounded bg-white p-3 text-sm"
                  >
                    <FileText className="h-4 w-4 text-gray-400" />
                    <span className="flex-1 truncate font-medium text-gray-700">{file.name}</span>
                    <span className="text-xs text-gray-500">
                      {(file.size / 1024).toFixed(1)} KB
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleUpload}
                disabled={bulkUploadMutation.isPending}
                className="flex-1 rounded-md bg-green-600 px-4 py-3 text-sm font-medium text-white transition-colors hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {bulkUploadMutation.isPending ? (
                  <span className="flex items-center justify-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Processing {selectedFiles.length} files...
                  </span>
                ) : (
                  `Process ${selectedFiles.length} files`
                )}
              </button>
              <button
                onClick={handleReset}
                disabled={bulkUploadMutation.isPending}
                className="rounded-md border border-gray-300 px-6 py-3 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          /* Drop zone */
          <div
            onClick={handleClick}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`
              relative flex min-h-[250px] cursor-pointer flex-col items-center justify-center
              rounded-lg border-2 border-dashed p-8 transition-all
              ${isDragging
                ? "border-blue-500 bg-blue-50"
                : "border-gray-300 bg-gray-50 hover:border-blue-400 hover:bg-gray-100"
              }
              ${bulkUploadMutation.isPending ? "cursor-wait opacity-60" : ""}
            `}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="application/pdf"
              multiple
              onChange={handleFileSelect}
              className="hidden"
              disabled={bulkUploadMutation.isPending}
            />

            <Upload className="h-16 w-16 text-gray-400" />
            <p className="mt-4 text-base font-medium text-gray-700">
              Drag multiple statements here
            </p>
            <p className="mt-2 text-sm text-gray-500">
              or click to select files (up to 100 PDFs)
            </p>
          </div>
        )}

        {/* Info box */}
        {!uploadResults && selectedFiles.length === 0 && (
          <div className="mt-4 rounded-md bg-blue-50 p-4">
            <p className="text-xs font-medium text-blue-900">Instructions:</p>
            <ul className="mt-2 list-inside list-disc space-y-1 text-xs text-blue-800">
              <li>You can select up to 100 PDF files at once</li>
              <li>Files will be processed automatically detecting date and period</li>
              <li>Duplicates will be detected and skipped</li>
              <li>You will receive a detailed report for each file processed</li>
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
