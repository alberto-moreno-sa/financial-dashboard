import { useSuspenseQuery } from "@tanstack/react-query";
import {
  Area,
  AreaChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import { historyQueries } from "~/entities/history/api/queries";
import { Card, CardHeader, CardTitle, CardContent } from "~/shared/ui/card";
import { formatCurrency, formatDate } from "~/shared/lib/formatters";

export function HistoryChart() {
  const { data } = useSuspenseQuery(historyQueries.chart());
  return (
    <Card className="col-span-4 lg:col-span-3">
      <CardHeader>
        <CardTitle>Performance History</CardTitle>
      </CardHeader>
      <CardContent className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data.points}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-chart-1)" stopOpacity={0.3} />
                <stop offset="95%" stopColor="var(--color-chart-1)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis
              dataKey="date"
              tickFormatter={(d) => formatDate(d)}
              axisLine={false}
              tickLine={false}
              fontSize={12}
              stroke="var(--muted-foreground)"
            />
            <YAxis
              tickFormatter={(val) => `$${val / 1000}k`}
              axisLine={false}
              tickLine={false}
              fontSize={12}
              stroke="var(--muted-foreground)"
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "var(--card)",
                borderColor: "var(--border)",
                borderRadius: "0.5rem",
              }}
              formatter={(val: number) => [formatCurrency(val), "Value"]}
              labelFormatter={(d) => formatDate(d)}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="var(--color-chart-1)"
              fillOpacity={1}
              fill="url(#colorValue)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
