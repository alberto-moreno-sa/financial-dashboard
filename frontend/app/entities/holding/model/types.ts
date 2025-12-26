export interface Holding {
  id: string;
  ticker: string;
  name: string;
  type: "ETF" | "Stock" | "Bond" | "Cash";
  details: { quantity: number; avgCost: number; currentPrice: number };
  financials: {
    totalValue: number;
    allocation: number;
    unrealizedGain: number;
    unrealizedGainPercent: number;
  };
}

export interface HoldingDetails {
  quantity: number;
  avgCost: number;
  currentPrice: number;
}

export interface HoldingFinancials {
  totalValue: number;
  allocation: number;
  unrealizedGain: number;
  unrealizedGainPercent: number;
}

export interface HoldingItem {
  id: string;
  ticker: string;
  name: string;
  type: string; // "Stock" | "ETF" | "Bond"
  details: HoldingDetails;
  financials: HoldingFinancials;
}
