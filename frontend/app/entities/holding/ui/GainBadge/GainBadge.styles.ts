import { cva, type VariantProps } from "class-variance-authority";

export const gainBadgeVariants = cva(
  "inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium tabular-nums font-mono border",
  {
    variants: {
      trend: {
        up: "bg-gain-subtle text-gain border-gain/20",
        down: "bg-loss-subtle text-loss border-loss/20",
        neutral: "bg-muted text-muted-foreground border-transparent",
      },
    },
    defaultVariants: { trend: "neutral" },
  },
);

export type GainBadgeVariants = VariantProps<typeof gainBadgeVariants>;

export const deriveTrend = (value: number) => (value > 0 ? "up" : value < 0 ? "down" : "neutral");
