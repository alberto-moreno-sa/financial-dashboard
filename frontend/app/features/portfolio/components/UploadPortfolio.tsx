import { useState, useRef } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Upload, FileText, CheckCircle, XCircle, Loader2 } from "lucide-react";
import { uploadStatement, saveSnapshot, type PortfolioSnapshotResponse } from "../api/uploadPortfolio";
import { Card, CardContent, CardHeader, CardTitle } from "~/shared/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/shared/ui/table";
import { toast } from "sonner";

// Simple hash function for file content (not cryptographic, just for tracking)
async function computeFileHash(file: File): Promise<string> {
  const arrayBuffer = await file.arrayBuffer();
  const hashBuffer = await crypto.subtle.digest('SHA-256', arrayBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

export function UploadPortfolio() {
  const [isDragging, setIsDragging] = useState(false);
  const [snapshotData, setSnapshotData] = useState<PortfolioSnapshotResponse | null>(null);
  const [fileHash, setFileHash] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const queryClient = useQueryClient();

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const hash = await computeFileHash(file);
      setFileHash(hash);
      return uploadStatement(file);
    },
    onSuccess: (response) => {
      setSnapshotData(response);
      toast.success("Estado de cuenta procesado exitosamente");
    },
    onError: (error: any) => {
      const message = error?.response?.data?.detail || error?.message || "No se pudo procesar el estado de cuenta";
      toast.error("Error al procesar el PDF", {
        description: message,
      });
    },
  });

  const saveMutation = useMutation({
    mutationFn: () => {
      if (!snapshotData) throw new Error("No hay datos para guardar");
      return saveSnapshot(snapshotData, fileHash);
    },
    onSuccess: (response) => {
      toast.success(response.message);
      // Invalidate queries to refresh data
      queryClient.invalidateQueries({ queryKey: ["portfolio"] });
      queryClient.invalidateQueries({ queryKey: ["holdings"] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
      // Reset state
      setSnapshotData(null);
      setFileHash("");
      uploadMutation.reset();
    },
    onError: (error: any) => {
      const message = error?.response?.data?.detail || error?.message || "No se pudo guardar el snapshot";
      toast.error("Error al guardar", {
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
    const pdfFile = files.find((f) => f.type === "application/pdf");

    if (pdfFile) {
      uploadMutation.mutate(pdfFile);
    } else {
      toast.error("Tipo de archivo inválido", {
        description: "Por favor sube un archivo PDF de GBM",
      });
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      uploadMutation.mutate(files[0]);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleConfirmImport = () => {
    if (!snapshotData) return;
    saveMutation.mutate();
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
    }).format(value);
  };

  const formatPercent = (value: number) => {
    return `${value >= 0 ? "+" : ""}${value.toFixed(2)}%`;
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="h-5 w-5" />
          Subir Estado de Cuenta GBM
        </CardTitle>
        <p className="mt-2 text-sm text-gray-500">
          Arrastra y suelta tu estado de cuenta en PDF o haz clic para seleccionar
        </p>
      </CardHeader>
      <CardContent>
        {/* Show confirmation card if data was extracted */}
        {snapshotData ? (
          <div className="space-y-6">
            {/* Summary Card */}
            <div className="rounded-lg border border-green-200 bg-green-50 p-6">
              <div className="mb-4 flex items-center gap-2 text-green-800">
                <CheckCircle className="h-5 w-5" />
                <h3 className="font-semibold">Portafolio Detectado</h3>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Titular:</span>
                  <span className="font-medium">{snapshotData.metadata.account_holder}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Fecha:</span>
                  <span className="font-medium">{snapshotData.metadata.detected_date}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Archivo:</span>
                  <span className="font-medium text-xs">{snapshotData.metadata.filename}</span>
                </div>
                <div className="my-4 border-t border-green-200" />
                <div className="flex justify-between text-lg">
                  <span className="font-semibold text-gray-900">Valor Total:</span>
                  <span className="font-bold text-green-700">
                    {formatCurrency(snapshotData.portfolio.total_value)}
                  </span>
                </div>
                <div className="space-y-2 rounded bg-white p-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Renta Variable:</span>
                    <span className="font-medium">
                      {formatCurrency(snapshotData.portfolio.equity_value)}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Deuda:</span>
                    <span className="font-medium">
                      {formatCurrency(snapshotData.portfolio.fixed_income_value)}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Efectivo:</span>
                    <span className="font-medium">
                      {formatCurrency(snapshotData.portfolio.cash_value)}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Breakdown Table */}
            {snapshotData.breakdown.length > 0 && (
              <div className="rounded-lg border border-gray-200 bg-white">
                <div className="border-b border-gray-200 p-4">
                  <h4 className="font-semibold text-gray-900">
                    Desglose de Posiciones ({snapshotData.breakdown.length})
                  </h4>
                </div>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Ticker</TableHead>
                        <TableHead>Nombre</TableHead>
                        <TableHead className="text-right">Cantidad</TableHead>
                        <TableHead className="text-right">Precio Promedio</TableHead>
                        <TableHead className="text-right">Precio Actual</TableHead>
                        <TableHead className="text-right">Valor de Mercado</TableHead>
                        <TableHead className="text-right">Ganancia/Pérdida</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {snapshotData.breakdown.map((position) => (
                        <TableRow key={position.ticker}>
                          <TableCell className="font-bold">{position.ticker}</TableCell>
                          <TableCell className="max-w-[200px] truncate text-xs">
                            {position.name}
                          </TableCell>
                          <TableCell className="text-right font-mono text-sm">
                            {position.quantity}
                          </TableCell>
                          <TableCell className="text-right text-sm">
                            {formatCurrency(position.avg_cost)}
                          </TableCell>
                          <TableCell className="text-right text-sm">
                            {formatCurrency(position.current_price)}
                          </TableCell>
                          <TableCell className="text-right font-medium">
                            {formatCurrency(position.market_value)}
                          </TableCell>
                          <TableCell className="text-right">
                            <div className="flex flex-col items-end gap-1">
                              <span
                                className={
                                  position.unrealized_gain >= 0
                                    ? "text-xs font-medium text-green-700"
                                    : "text-xs font-medium text-red-700"
                                }
                              >
                                {formatCurrency(position.unrealized_gain)}
                              </span>
                              <span
                                className={
                                  position.unrealized_gain >= 0
                                    ? "text-xs text-green-600"
                                    : "text-xs text-red-600"
                                }
                              >
                                {formatPercent(position.unrealized_gain_percent)}
                              </span>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                onClick={handleConfirmImport}
                disabled={saveMutation.isPending}
                className="flex-1 rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {saveMutation.isPending ? (
                  <span className="flex items-center justify-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Guardando...
                  </span>
                ) : (
                  "Confirmar e Importar"
                )}
              </button>
              <button
                onClick={() => {
                  setSnapshotData(null);
                  setFileHash("");
                  uploadMutation.reset();
                }}
                disabled={saveMutation.isPending}
                className="rounded-md border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Cancelar
              </button>
            </div>
          </div>
        ) : (
          <div
            onClick={handleClick}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`
              relative flex min-h-[200px] cursor-pointer flex-col items-center justify-center
              rounded-lg border-2 border-dashed p-8 transition-all
              ${isDragging
                ? "border-blue-500 bg-blue-50"
                : "border-gray-300 bg-gray-50 hover:border-blue-400 hover:bg-gray-100"
              }
              ${uploadMutation.isPending ? "cursor-wait opacity-60" : ""}
            `}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="application/pdf"
              onChange={handleFileSelect}
              className="hidden"
              disabled={uploadMutation.isPending}
            />

            {uploadMutation.isPending ? (
              <>
                <Loader2 className="h-12 w-12 animate-spin text-blue-600" />
                <p className="mt-4 text-sm font-medium text-gray-700">Procesando PDF...</p>
              </>
            ) : uploadMutation.isError ? (
              <>
                <XCircle className="h-12 w-12 text-red-600" />
                <p className="mt-4 text-sm font-medium text-gray-700">Error al procesar</p>
                <p className="mt-1 text-xs text-gray-500">Haz clic para intentar de nuevo</p>
              </>
            ) : (
              <>
                <FileText className="h-12 w-12 text-gray-400" />
                <p className="mt-4 text-sm font-medium text-gray-700">
                  Arrastra tu estado de cuenta de GBM aquí
                </p>
                <p className="mt-1 text-xs text-gray-500">o haz clic para seleccionar (PDF)</p>
              </>
            )}
          </div>
        )}

        {/* Info box */}
        {!snapshotData && (
          <div className="mt-4 rounded-md bg-blue-50 p-4">
            <p className="text-xs font-medium text-blue-900">Formatos soportados:</p>
            <ul className="mt-2 list-inside list-disc space-y-1 text-xs text-blue-800">
              <li>Estados de cuenta GBM en formato PDF</li>
              <li>El archivo debe contener el resumen del portafolio</li>
              <li>Se extraerán automáticamente: Renta Variable, Deuda, Efectivo y Posiciones</li>
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
