import { Outlet, Link, useLocation } from "react-router";
import { useAuth0 } from "@auth0/auth0-react";
import { ProtectedRoute } from "~/features/auth/components/ProtectedRoute";
import { useAuthStore } from "~/shared/stores/auth-store";
import { useAuthenticatedClient } from "~/shared/hooks/useAuthenticatedClient";
import { clearAllAuthData } from "~/shared/lib/auth-utils";

export default function DashboardLayout() {
  const location = useLocation();
  const { logout } = useAuth0();
  const { clearAuth } = useAuthStore();

  // Configure API client to use Auth0 tokens
  useAuthenticatedClient();

  const isActive = (path: string) => location.pathname.startsWith(path);

  const handleLogout = () => {
    // Clear ALL authentication data (localStorage, sessionStorage, cookies)
    clearAllAuthData();

    // Clear Zustand store
    clearAuth();

    // Logout from Auth0 and redirect to home
    logout({
      logoutParams: {
        returnTo: window.location.origin,
      },
    });
  };

  return (
    <ProtectedRoute>
      <div className="flex h-screen bg-gray-50">
      {/* Sidebar Fijo */}
      <aside className="hidden w-64 flex-col border-r border-gray-200 bg-white md:flex">
        <div className="border-b border-gray-100 p-6">
          <h1 className="text-xl font-bold tracking-tight text-gray-900">Portfolio</h1>
        </div>

        <nav className="flex-1 space-y-2 overflow-y-auto px-4 py-6">
          <Link
            to="/dashboard/portfolio"
            className={`flex items-center rounded-md px-4 py-2.5 text-sm font-medium transition-colors ${
              isActive("/dashboard/portfolio")
                ? "bg-gray-100 text-gray-900"
                : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
            }`}
          >
            Resumen Portafolio
          </Link>

          {/* Puedes agregar más enlaces aquí en el futuro */}
        </nav>

        <div className="border-t border-gray-100 p-4">
          <button
            onClick={handleLogout}
            className="flex w-full items-center justify-center rounded-md bg-red-50 px-4 py-2 text-sm font-medium text-red-600 transition-colors hover:bg-red-100"
          >
            Cerrar Sesión
          </button>
        </div>
      </aside>

      {/* Área de Contenido Principal */}
      <main className="flex min-w-0 flex-1 flex-col overflow-hidden">
        {/* Header Móvil (opcional, visible solo en pantallas pequeñas) */}
        <div className="flex items-center justify-between border-b border-gray-200 bg-white p-4 md:hidden">
          <h1 className="text-lg font-bold text-gray-900">Portfolio</h1>
          <button onClick={handleLogout} className="text-sm font-medium text-red-600">
            Salir
          </button>
        </div>

        {/* Contenido Scrollable */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          {/* Aquí se renderizan las rutas hijas (como _dashboard.portfolio.tsx) */}
          <Outlet />
        </div>
      </main>
      </div>
    </ProtectedRoute>
  );
}
