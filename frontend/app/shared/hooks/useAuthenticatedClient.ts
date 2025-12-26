import { useAuth0 } from "@auth0/auth0-react";
import { useEffect, useRef } from "react";
import { apiClient } from "~/shared/api/client";

/**
 * Hook that configures the API client with Auth0 token
 * This should be used at the app level to ensure all API requests are authenticated
 */
export function useAuthenticatedClient() {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();
  const interceptorIdRef = useRef<number | null>(null);

  // Use refs to store the latest values for use in the interceptor
  const authRef = useRef({ getAccessTokenSilently, isAuthenticated });

  // Update refs whenever auth state changes
  useEffect(() => {
    authRef.current = { getAccessTokenSilently, isAuthenticated };
  }, [getAccessTokenSilently, isAuthenticated]);

  useEffect(() => {
    // Only set up interceptor once
    if (interceptorIdRef.current !== null) {
      return;
    }

    // Set up request interceptor to get fresh token from Auth0
    const requestInterceptor = apiClient.interceptors.request.use(
      async (config) => {
        // Use the latest values from the ref
        const { isAuthenticated, getAccessTokenSilently } = authRef.current;

        if (isAuthenticated) {
          try {
            const token = await getAccessTokenSilently({
              cacheMode: "on", // Use cached token if available
            });
            config.headers.Authorization = `Bearer ${token}`;
          } catch (error) {
            console.error("Failed to get access token:", error);
            // Don't throw error, let the request proceed without auth
            // The backend will return 401/403 and the error will be handled by the component
          }
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    interceptorIdRef.current = requestInterceptor;

    // Cleanup interceptor on unmount
    return () => {
      if (interceptorIdRef.current !== null) {
        apiClient.interceptors.request.eject(interceptorIdRef.current);
        interceptorIdRef.current = null;
      }
    };
  }, []); // Empty deps - only run once
}
