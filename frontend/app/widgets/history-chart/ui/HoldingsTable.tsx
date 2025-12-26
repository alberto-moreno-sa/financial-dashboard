import { useSuspenseQuery } from "@tanstack/react-query";
import { holdingsQueries } from "~/entities/holding/api/queries";
import { GainBadge } from "~/entities/holding/ui/GainBadge/GainBadge";
import { formatCurrency } from "~/shared/lib/formatters";
import { Card, CardHeader, CardTitle, CardContent } from "~/shared/ui/card";
import { Table, TableHeader, TableBody, TableHead, TableRow, TableCell } from "~/shared/ui/table";

export function HoldingsTable() {
  const { data } = useSuspenseQuery(holdingsQueries.list());
  return (
    <Card className="col-span-4">
      <CardHeader>
        <CardTitle>Active Positions</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Ticker</TableHead>
              <TableHead className="text-right">Qty</TableHead>
              <TableHead className="text-right">Price</TableHead>
              <TableHead className="text-right">Value</TableHead>
              <TableHead className="text-right">Alloc</TableHead>
              <TableHead className="text-right">P&L</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.items.map((h) => (
              <TableRow key={h.id}>
                <TableCell className="font-medium">
                  {h.ticker}
                  <div className="text-muted-foreground text-xs font-normal">{h.name}</div>
                </TableCell>
                <TableCell className="text-right font-mono">{h.details.quantity}</TableCell>
                <TableCell className="text-right font-mono">
                  {formatCurrency(h.details.currentPrice)}
                </TableCell>
                <TableCell className="text-right font-mono font-bold">
                  {formatCurrency(h.financials.totalValue)}
                </TableCell>
                <TableCell className="text-right font-mono">
                  {h.financials.allocation.toFixed(2)}%
                </TableCell>
                <TableCell className="text-right">
                  <GainBadge
                    value={h.financials.unrealizedGain}
                    percentage={h.financials.unrealizedGainPercent}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
