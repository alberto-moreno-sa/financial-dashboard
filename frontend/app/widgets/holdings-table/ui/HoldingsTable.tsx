import { useSuspenseQuery } from "@tanstack/react-query";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/shared/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "~/shared/ui/card";
import { GainBadge } from "~/entities/holding/ui/GainBadge/GainBadge";
import { formatCurrency } from "~/shared/lib/formatters";
import { holdingsQueries } from "~/entities/holding/api/queries";

export function HoldingsTable() {
  const { data } = useSuspenseQuery(holdingsQueries.list());
  const items = data?.items || [];

  if (items.length === 0) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Portfolio Holdings</CardTitle>
        </CardHeader>
        <CardContent className="flex h-64 items-center justify-center text-gray-400">
          <div className="text-center">
            <p className="text-lg font-medium">No positions yet</p>
            <p className="mt-2 text-sm">Your portfolio holdings will appear here once you add transactions</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full shadow-sm">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle>Portfolio Holdings</CardTitle>
          <span className="rounded-full bg-gray-100 px-2 py-1 text-sm text-gray-500">
            {items.length} Assets
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[100px]">Ticker</TableHead>
                <TableHead>Name</TableHead>
                <TableHead className="text-right">Qty</TableHead>
                <TableHead className="text-right">Avg Cost</TableHead>
                <TableHead className="text-right">Price</TableHead>
                <TableHead className="text-right">Market Value</TableHead>
                <TableHead className="text-right">P/L</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {items.map((item) => (
                <TableRow key={item.id} className="hover:bg-gray-50/50">
                  <TableCell className="font-bold text-gray-900">{item.ticker}</TableCell>
                  <TableCell className="max-w-[200px] truncate text-xs text-gray-600">
                    {item.name}
                    <div className="mt-0.5">
                      <span className="inline-flex items-center rounded-md bg-gray-50 px-1.5 py-0.5 text-xs font-medium text-gray-600 ring-1 ring-gray-500/10 ring-inset">
                        {item.type}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell className="text-right font-mono text-sm">
                    {item.details.quantity}
                  </TableCell>
                  <TableCell className="text-right text-sm text-gray-500">
                    {formatCurrency(item.details.avgCost)}
                  </TableCell>
                  <TableCell className="text-right text-sm">
                    {formatCurrency(item.details.currentPrice)}
                  </TableCell>
                  <TableCell className="text-right font-medium">
                    {formatCurrency(item.financials.totalValue)}
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex flex-col items-end gap-1">
                      {/* Valor monetario */}
                      <span
                        className={
                          item.financials.unrealizedGain >= 0
                            ? "text-xs font-medium text-green-700"
                            : "text-xs font-medium text-red-700"
                        }
                      >
                        {item.financials.unrealizedGain >= 0 ? "+" : ""}
                        {formatCurrency(item.financials.unrealizedGain)}
                      </span>
                      {/* TU Badge para el porcentaje */}
                      <GainBadge
                        value={item.financials.unrealizedGain}
                        percentage={item.financials.unrealizedGainPercent}
                      />
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}
