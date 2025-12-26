import { useQuery } from "@tanstack/react-query";
import { TrendingUp, TrendingDown, Calendar, DollarSign } from "lucide-react";
import { getSnapshotHistory } from "../api/snapshotHistory";
import { Card, CardContent, CardHeader, CardTitle } from "~/shared/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/shared/ui/table";

export function SnapshotHistory() {
  const { data, isLoading } = useQuery({
    queryKey: ["snapshot-history"],
    queryFn: () => getSnapshotHistory(12),
  });

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
      minimumFractionDigits: 2,
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("es-MX", {
      year: "numeric",
      month: "long",
    }).format(date);
  };

  const formatPercent = (value: number | null) => {
    if (value === null) return "N/A";
    const sign = value >= 0 ? "+" : "";
    return `${sign}${value.toFixed(2)}%`;
  };

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Portfolio History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!data || data.total_count === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Portfolio History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <Calendar className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <p className="text-gray-600">No snapshots recorded</p>
            <p className="text-sm text-gray-500 mt-2">
              Upload your first statement to start tracking your portfolio
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Calculate overall statistics
  const latestSnapshot = data.snapshots[0];
  const oldestSnapshot = data.snapshots[data.snapshots.length - 1];
  const totalGrowth = latestSnapshot.total_value - oldestSnapshot.total_value;
  const totalGrowthPercent = (totalGrowth / oldestSnapshot.total_value) * 100;

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Current Balance</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(latestSnapshot.total_value)}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {formatDate(latestSnapshot.snapshot_date)}
                </p>
              </div>
              <DollarSign className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Monthly Change</p>
                <p className={`text-2xl font-bold ${
                  (latestSnapshot.total_change || 0) >= 0 ? "text-green-600" : "text-red-600"
                }`}>
                  {latestSnapshot.total_change !== null
                    ? formatCurrency(latestSnapshot.total_change)
                    : "N/A"}
                </p>
                <p className={`text-xs mt-1 ${
                  (latestSnapshot.total_change_percent || 0) >= 0 ? "text-green-600" : "text-red-600"
                }`}>
                  {formatPercent(latestSnapshot.total_change_percent)}
                </p>
              </div>
              {(latestSnapshot.total_change || 0) >= 0 ? (
                <TrendingUp className="h-8 w-8 text-green-600" />
              ) : (
                <TrendingDown className="h-8 w-8 text-red-600" />
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Growth</p>
                <p className={`text-2xl font-bold ${
                  totalGrowth >= 0 ? "text-green-600" : "text-red-600"
                }`}>
                  {formatCurrency(totalGrowth)}
                </p>
                <p className={`text-xs mt-1 ${
                  totalGrowthPercent >= 0 ? "text-green-600" : "text-red-600"
                }`}>
                  {formatPercent(totalGrowthPercent)}
                </p>
              </div>
              <Calendar className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Historical Table */}
      <Card>
        <CardHeader>
          <CardTitle>Snapshot History ({data.total_count})</CardTitle>
          <p className="text-sm text-gray-500 mt-2">
            History of uploaded statements and portfolio evolution
          </p>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead className="text-right">Equity</TableHead>
                  <TableHead className="text-right">Fixed Income</TableHead>
                  <TableHead className="text-right">Cash</TableHead>
                  <TableHead className="text-right">Total</TableHead>
                  <TableHead className="text-right">Monthly Change</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.snapshots.map((snapshot, index) => (
                  <TableRow key={snapshot.id} className={index === 0 ? "bg-blue-50" : ""}>
                    <TableCell className="font-medium">
                      {formatDate(snapshot.snapshot_date)}
                      {index === 0 && (
                        <span className="ml-2 rounded-full bg-blue-600 px-2 py-0.5 text-xs font-semibold text-white">
                          Current
                        </span>
                      )}
                    </TableCell>
                    <TableCell className="text-right">
                      {formatCurrency(snapshot.equity_value)}
                    </TableCell>
                    <TableCell className="text-right">
                      {formatCurrency(snapshot.fixed_income_value)}
                    </TableCell>
                    <TableCell className="text-right">
                      {formatCurrency(snapshot.cash_value)}
                    </TableCell>
                    <TableCell className="text-right font-bold">
                      {formatCurrency(snapshot.total_value)}
                    </TableCell>
                    <TableCell className="text-right">
                      {snapshot.total_change !== null ? (
                        <div className="flex flex-col items-end">
                          <span className={`font-medium ${
                            snapshot.total_change >= 0 ? "text-green-600" : "text-red-600"
                          }`}>
                            {formatCurrency(snapshot.total_change)}
                          </span>
                          <span className={`text-xs ${
                            (snapshot.total_change_percent || 0) >= 0 ? "text-green-600" : "text-red-600"
                          }`}>
                            {formatPercent(snapshot.total_change_percent)}
                          </span>
                        </div>
                      ) : (
                        <span className="text-gray-400 text-sm">First snapshot</span>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* Portfolio Composition - Latest Snapshot */}
      <Card>
        <CardHeader>
          <CardTitle>Current Portfolio Composition</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium text-gray-700">Equity</span>
                <span className="font-semibold text-gray-900">
                  {formatCurrency(latestSnapshot.equity_value)}
                </span>
              </div>
              <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200">
                <div
                  className="h-full bg-blue-600"
                  style={{
                    width: `${(latestSnapshot.equity_value / latestSnapshot.total_value) * 100}%`,
                  }}
                />
              </div>
              <p className="mt-1 text-xs text-gray-500">
                {((latestSnapshot.equity_value / latestSnapshot.total_value) * 100).toFixed(1)}%
              </p>
            </div>

            <div>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium text-gray-700">Fixed Income</span>
                <span className="font-semibold text-gray-900">
                  {formatCurrency(latestSnapshot.fixed_income_value)}
                </span>
              </div>
              <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200">
                <div
                  className="h-full bg-green-600"
                  style={{
                    width: `${(latestSnapshot.fixed_income_value / latestSnapshot.total_value) * 100}%`,
                  }}
                />
              </div>
              <p className="mt-1 text-xs text-gray-500">
                {((latestSnapshot.fixed_income_value / latestSnapshot.total_value) * 100).toFixed(1)}%
              </p>
            </div>

            <div>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium text-gray-700">Cash</span>
                <span className="font-semibold text-gray-900">
                  {formatCurrency(latestSnapshot.cash_value)}
                </span>
              </div>
              <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200">
                <div
                  className="h-full bg-yellow-600"
                  style={{
                    width: `${(latestSnapshot.cash_value / latestSnapshot.total_value) * 100}%`,
                  }}
                />
              </div>
              <p className="mt-1 text-xs text-gray-500">
                {((latestSnapshot.cash_value / latestSnapshot.total_value) * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
