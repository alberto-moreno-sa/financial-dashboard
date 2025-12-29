import { useSuspenseQuery } from "@tanstack/react-query";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";
import { Card, CardHeader, CardTitle, CardContent } from "~/shared/ui/card";
import { holdingsQueries } from "~/entities/holding/api/queries";
import { formatCurrency } from "~/shared/lib/formatters";

const COLORS = [
  "#3b82f6", // blue-500
  "#10b981", // green-500
  "#f59e0b", // amber-500
  "#ef4444", // red-500
  "#8b5cf6", // purple-500
  "#ec4899", // pink-500
];

export function PortfolioDistribution() {
  const { data } = useSuspenseQuery(holdingsQueries.list());
  const items = data?.items || [];

  // Group by asset type and calculate totals
  const distribution = items.reduce((acc: any[], item) => {
    const existingType = acc.find((d) => d.type === item.type);

    if (existingType) {
      existingType.value += item.financials.totalValue;
    } else {
      acc.push({
        type: item.type,
        name: item.type === "equity" ? "Equities" : item.type === "fixed_income" ? "Fixed Income" : item.type,
        value: item.financials.totalValue,
      });
    }

    return acc;
  }, []);

  const totalValue = distribution.reduce((sum, item) => sum + item.value, 0);

  // Add percentage
  const distributionWithPercent = distribution.map((item) => ({
    ...item,
    percentage: ((item.value / totalValue) * 100).toFixed(1),
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="rounded-lg border bg-card p-3 shadow-lg">
          <p className="font-medium text-sm">{payload[0].name}</p>
          <p className="text-sm text-muted-foreground">
            {formatCurrency(payload[0].value)}
          </p>
          <p className="text-xs text-muted-foreground">
            {payload[0].payload.percentage}%
          </p>
        </div>
      );
    }
    return null;
  };

  const renderLegend = (props: any) => {
    const { payload } = props;
    return (
      <div className="flex flex-wrap justify-center gap-4 mt-4">
        {payload.map((entry: any, index: number) => (
          <div key={`legend-${index}`} className="flex items-center gap-2">
            <div
              className="h-3 w-3 rounded-full"
              style={{ backgroundColor: entry.color }}
            />
            <span className="text-sm text-gray-600">
              {entry.value} ({distributionWithPercent[index].percentage}%)
            </span>
          </div>
        ))}
      </div>
    );
  };

  if (items.length === 0) {
    return null;
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Asset Distribution</CardTitle>
      </CardHeader>
      <CardContent className="h-[350px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={distributionWithPercent}
              cx="50%"
              cy="45%"
              labelLine={false}
              label={({ name, percentage }) => `${name}: ${percentage}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {distributionWithPercent.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend content={renderLegend} />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
