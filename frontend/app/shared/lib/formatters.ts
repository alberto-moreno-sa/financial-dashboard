export const formatCurrency = (value: number, currency = "MXN") =>
  new Intl.NumberFormat("es-MX", { style: "currency", currency }).format(value);

export const formatPercent = (value: number) => `${value > 0 ? "+" : ""}${value.toFixed(2)}%`;

export const formatDate = (iso: string) =>
  new Intl.DateTimeFormat("en-US", { dateStyle: "medium" }).format(new Date(iso));
