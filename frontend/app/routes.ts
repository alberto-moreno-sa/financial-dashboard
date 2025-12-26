import { type RouteConfig, index, route, layout } from "@react-router/dev/routes";

export default [
  // Ruta índice (Login)
  index("routes/index.tsx"),

  // Ruta de callback de Auth0
  route("callback", "routes/callback.tsx"),

  // Layout del Dashboard (Sidebar, etc.)
  layout("routes/dashboard.tsx", [
    // Rutas anidadas dentro del dashboard
    route("dashboard/portfolio", "routes/dashboard.portfolio.tsx"),
  ]),
] satisfies RouteConfig;
