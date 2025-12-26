import { cva, type VariantProps } from "class-variance-authority";

export const statCardVariants = cva("transition-all duration-200", {
  variants: {
    status: {
      positive: "border-l-4 border-l-gain",
      negative: "border-l-4 border-l-loss",
      neutral: "",
    },
  },
  defaultVariants: { status: "neutral" },
});
export type StatCardVariants = VariantProps<typeof statCardVariants>;

export const getTrendColor = (trend?: "up" | "down" | "neutral") => {
  if (trend === "up") return "text-gain";
  if (trend === "down") return "text-loss";
  return "text-muted-foreground";
};
