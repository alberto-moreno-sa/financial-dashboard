import { Suspense, useState } from "react";
import { PortfolioStats } from "~/widgets/portfolio-stats/ui/PortfolioStats";
import { HoldingsTable } from "~/widgets/holdings-table/ui/HoldingsTable";
import { Skeleton } from "~/shared/ui/skeleton";
import { UploadPortfolio } from "~/features/portfolio/components/UploadPortfolio";
import { BulkUploadPortfolio } from "~/features/portfolio/components/BulkUploadPortfolio";
import { SnapshotHistory } from "~/features/portfolio/components/SnapshotHistory";
import { Upload, History, UploadCloud } from "lucide-react";

export default function PortfolioPage() {
  const [showUpload, setShowUpload] = useState(false);
  const [uploadMode, setUploadMode] = useState<"single" | "bulk">("single");
  const [view, setView] = useState<"overview" | "history">("overview");

  return (
    <div className="space-y-8">
      {/* Page header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">
            {view === "overview" ? "General Overview" : "Portfolio History"}
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            {view === "overview"
              ? "Detailed view of your assets, returns and distribution."
              : "Historical evolution of your portfolio and monthly snapshots."}
          </p>
        </div>
        <div className="flex gap-2">
          <div className="inline-flex rounded-md shadow-sm" role="group">
            <button
              onClick={() => setView("overview")}
              className={`inline-flex items-center gap-2 rounded-l-md border px-4 py-2 text-sm font-medium transition-colors ${
                view === "overview"
                  ? "bg-blue-600 text-white border-blue-600"
                  : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setView("history")}
              className={`inline-flex items-center gap-2 rounded-r-md border-t border-b border-r px-4 py-2 text-sm font-medium transition-colors ${
                view === "history"
                  ? "bg-blue-600 text-white border-blue-600"
                  : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
              }`}
            >
              <History className="h-4 w-4" />
              History
            </button>
          </div>
          <button
            onClick={() => setShowUpload(!showUpload)}
            className="inline-flex items-center gap-2 rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
          >
            <Upload className="h-4 w-4" />
            {showUpload ? "Close" : "Upload Statement"}
          </button>
        </div>
      </div>

      {/* Upload Section */}
      {showUpload && (
        <section className="space-y-4">
          {/* Upload Mode Toggle */}
          <div className="flex items-center justify-center">
            <div className="inline-flex rounded-md shadow-sm" role="group">
              <button
                onClick={() => setUploadMode("single")}
                className={`inline-flex items-center gap-2 rounded-l-md border px-4 py-2 text-sm font-medium transition-colors ${
                  uploadMode === "single"
                    ? "bg-green-600 text-white border-green-600"
                    : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
                }`}
              >
                <Upload className="h-4 w-4" />
                Single Upload
              </button>
              <button
                onClick={() => setUploadMode("bulk")}
                className={`inline-flex items-center gap-2 rounded-r-md border-t border-b border-r px-4 py-2 text-sm font-medium transition-colors ${
                  uploadMode === "bulk"
                    ? "bg-green-600 text-white border-green-600"
                    : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
                }`}
              >
                <UploadCloud className="h-4 w-4" />
                Bulk Upload
              </button>
            </div>
          </div>

          {/* Upload Component */}
          {uploadMode === "single" ? <UploadPortfolio /> : <BulkUploadPortfolio />}
        </section>
      )}

      {/* Overview View */}
      {view === "overview" && (
        <>
          {/* Section 1: Statistics Cards */}
          <section>
            <Suspense
              fallback={
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                  <Skeleton className="h-32 rounded-xl" />
                  <Skeleton className="h-32 rounded-xl" />
                  <Skeleton className="h-32 rounded-xl" />
                  <Skeleton className="h-32 rounded-xl" />
                </div>
              }
            >
              <PortfolioStats />
            </Suspense>
          </section>

          {/* Section 2: Positions Table */}
          <section className="grid gap-6 lg:grid-cols-1">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-900">Active Positions</h3>
              </div>

              <Suspense
                fallback={
                  <div className="space-y-3">
                    <Skeleton className="h-12 w-full rounded-md" />
                    <Skeleton className="h-12 w-full rounded-md" />
                    <Skeleton className="h-12 w-full rounded-md" />
                    <Skeleton className="h-12 w-full rounded-md" />
                  </div>
                }
              >
                <HoldingsTable />
              </Suspense>
            </div>
          </section>
        </>
      )}

      {/* History View */}
      {view === "history" && (
        <section>
          <Suspense
            fallback={
              <div className="space-y-4">
                <Skeleton className="h-32 rounded-xl" />
                <Skeleton className="h-64 rounded-xl" />
              </div>
            }
          >
            <SnapshotHistory />
          </Suspense>
        </section>
      )}
    </div>
  );
}
