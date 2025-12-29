import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { useAuth0 } from "@auth0/auth0-react";
import { clearAllAuthData } from "~/shared/lib/auth-utils";
import { DashboardSkeleton } from "./DashboardSkeleton";

// Check if running in demo mode
const isDemoMode = import.meta.env.VITE_AUTH0_DOMAIN === "demo" ||
                   import.meta.env.VITE_AUTH0_DOMAIN === "demo-financial.auth0.com" ||
                   !import.meta.env.VITE_AUTH0_DOMAIN;

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const navigate = useNavigate();
  const { isAuthenticated, isLoading, getAccessTokenSilently } = useAuth0();
  const [tokenReady, setTokenReady] = useState(isDemoMode); // In demo mode, token is always ready

  useEffect(() => {
    // Skip auth check in demo mode
    if (isDemoMode) return;

    // Redirect to login if not authenticated and not loading
    if (!isLoading && !isAuthenticated) {
      // Clear all auth data before redirecting
      clearAllAuthData();
      navigate("/");
    }
  }, [isLoading, isAuthenticated, navigate]);

  // Pre-fetch token when authenticated to avoid race condition (skip in demo mode)
  useEffect(() => {
    if (isDemoMode) return; // Skip token fetch in demo mode

    if (isAuthenticated && !tokenReady) {
      getAccessTokenSilently({ cacheMode: "on" })
        .then(() => {
          setTokenReady(true);
        })
        .catch((error) => {
          console.error("Failed to pre-fetch token:", error);
          // Still allow rendering, the API calls will handle auth errors
          setTokenReady(true);
        });
    }
  }, [isAuthenticated, tokenReady, getAccessTokenSilently]);

  // In demo mode, render children immediately
  if (isDemoMode) {
    return <>{children}</>;
  }

  // Show dashboard skeleton while Auth0 is checking authentication or fetching token
  if (isLoading || (isAuthenticated && !tokenReady)) {
    return <DashboardSkeleton />;
  }

  // Don't render children until auth check is complete
  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
