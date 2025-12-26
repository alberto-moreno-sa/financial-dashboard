import * as React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "~/shared/ui/card";
import { Skeleton } from "~/shared/ui/skeleton";
import { formatCurrency, formatPercent } from "~/shared/lib/formatters";
import { cn } from "~/shared/lib/utils";
import type { LucideIcon } from "lucide-react";
import { statCardVariants, getTrendColor, type StatCardVariants } from "./StatCard.styles";

interface StatCardProps extends React.HTMLAttributes<HTMLDivElement>, StatCardVariants {
  title: string;
  value: number;
  currency?: string;
  percentage?: number;
  trend?: "up" | "down" | "neutral";
  icon?: LucideIcon;
  loading?: boolean;
}

export const StatCard = React.forwardRef<HTMLDivElement, StatCardProps>(
  (
    {
      title,
      value,
      currency = "MXN",
      percentage,
      trend,
      icon: Icon,
      loading,
      status,
      className,
      ...props
    },
    ref,
  ) => {
    if (loading) return <Skeleton className="h-32 w-full rounded-xl" />;
    return (
      <Card ref={ref} className={cn(statCardVariants({ status }), className)} {...props}>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-muted-foreground text-sm font-medium">{title}</CardTitle>
          {Icon && <Icon className="text-muted-foreground h-4 w-4" />}
        </CardHeader>
        <CardContent>
          <div className="font-mono text-2xl font-bold tabular-nums">
            {formatCurrency(value, currency)}
          </div>
          {percentage !== undefined && (
            <p className={cn("mt-1 text-xs font-medium", getTrendColor(trend))}>
              {formatPercent(percentage)}
            </p>
          )}
        </CardContent>
      </Card>
    );
  },
);
StatCard.displayName = "StatCard";
