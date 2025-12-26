import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { useAuth0 } from "@auth0/auth0-react";
import { clearAllAuthData } from "~/shared/lib/auth-utils";
import { DashboardSkeleton } from "./DashboardSkeleton";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const navigate = useNavigate();
  const { isAuthenticated, isLoading, getAccessTokenSilently } = useAuth0();
  const [tokenReady, setTokenReady] = useState(false);

  useEffect(() => {
    // Redirect to login if not authenticated and not loading
    if (!isLoading && !isAuthenticated) {
      // Clear all auth data before redirecting
      clearAllAuthData();
      navigate("/");
    }
  }, [isLoading, isAuthenticated, navigate]);

  // Pre-fetch token when authenticated to avoid race condition
  useEffect(() => {
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
