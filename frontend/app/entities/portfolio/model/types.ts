export type Trend = "up" | "down" | "neutral";

export interface PortfolioStats {
  currency: string;
  netWorth: { value: number; label: string };
  cash: { value: number; label: string; percentageOfTotal: number };
  investments: { value: number; label: string; percentageOfTotal: number };
  performance: { dailyChange: number; dailyChangePercentage: number; trend: Trend };
}
