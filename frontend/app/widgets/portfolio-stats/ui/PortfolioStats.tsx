import { useSuspenseQuery } from "@tanstack/react-query";
import { portfolioQueries } from "~/entities/portfolio/api/queries";
import { StatCard } from "./StatCard/StatCard";
import { Wallet, TrendingUp, DollarSign, Activity } from "lucide-react";

export function PortfolioStats() {
  const { data } = useSuspenseQuery(portfolioQueries.stats());
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <StatCard
        title="Net Worth"
        value={data.netWorth.value}
        currency={data.currency}
        icon={Wallet}
      />
      <StatCard
        title="Cash"
        value={data.cash.value}
        currency={data.currency}
        percentage={data.cash.percentageOfTotal}
        icon={DollarSign}
      />
      <StatCard
        title="Invested"
        value={data.investments.value}
        currency={data.currency}
        percentage={data.investments.percentageOfTotal}
        icon={TrendingUp}
      />
      <StatCard
        title="Day Change"
        value={data.performance.dailyChange}
        currency={data.currency}
        percentage={data.performance.dailyChangePercentage}
        trend={data.performance.trend}
        icon={Activity}
      />
    </div>
  );
}
