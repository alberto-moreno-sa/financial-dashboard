import * as React from "react";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { cn } from "~/shared/lib/utils";
import { gainBadgeVariants, deriveTrend, type GainBadgeVariants } from "./GainBadge.styles";
import { formatPercent } from "~/shared/lib/formatters";

interface GainBadgeProps extends React.HTMLAttributes<HTMLSpanElement>, GainBadgeVariants {
  value: number;
  percentage: number;
}
const Icons = { up: TrendingUp, down: TrendingDown, neutral: Minus };

export const GainBadge = React.forwardRef<HTMLSpanElement, GainBadgeProps>(
  ({ value, percentage, trend, className, ...props }, ref) => {
    const resolvedTrend = trend ?? deriveTrend(value);
    const Icon = Icons[resolvedTrend];
    return (
      <span
        ref={ref}
        className={cn(gainBadgeVariants({ trend: resolvedTrend }), className)}
        {...props}
      >
        <Icon className="h-3 w-3" />
        {formatPercent(percentage)}
      </span>
    );
  },
);
GainBadge.displayName = "GainBadge";
