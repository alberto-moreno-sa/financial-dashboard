import { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate } from "react-router";
import { toast } from "sonner";

export default function Callback() {
  const { isAuthenticated, isLoading, getAccessTokenSilently } = useAuth0();
  const navigate = useNavigate();
  const [isClient, setIsClient] = useState(false);

  // Ensure we're on the client
  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    async function handleCallback() {
      // Only run on client side
      if (!isClient) return;

      if (isLoading) return;

      if (!isAuthenticated) {
        toast.error("Authentication failed");
        navigate("/");
        return;
      }

      try {
        // Get Auth0 access token
        const token = await getAccessTokenSilently();

        // Get API URL from environment variable (already includes /api/v1)
        const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

        // Call backend to sync user data
        const response = await fetch(`${apiUrl}/users/sync`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error("Backend sync failed:", {
            status: response.status,
            statusText: response.statusText,
            body: errorText,
          });
          throw new Error(`Backend sync failed (${response.status}): ${errorText}`);
        }

        const data = await response.json();

        // Store user data in localStorage (Zustand will pick it up)
        if (typeof window !== "undefined") {
          // Store for Zustand
          localStorage.setItem("auth-storage", JSON.stringify({
            state: {
              token,
              user: {
                id: data.user.id,
                email: data.user.email,
                name: data.user.name || "",
                picture: data.user.picture,
              },
            },
            version: 0,
          }));

          // Store token separately for API client
          localStorage.setItem("auth_token", token);
        }

        if (data.is_new_user) {
          toast.success("Welcome! Your account has been created.");
        } else {
          toast.success(`Welcome back, ${data.user.name || data.user.email}!`);
        }

        // Use window.location for navigation to ensure full page load
        // This ensures Auth0Provider re-initializes properly
        window.location.href = "/dashboard/portfolio";
      } catch (error: any) {
        console.error("Error during user sync:", error);

        // Show detailed error message
        const errorMessage = error?.message || "Unknown error occurred";
        toast.error(`Failed to complete authentication: ${errorMessage}`);

        // Don't redirect immediately, show error for debugging
        console.log("Full error details:", {
          error,
          message: errorMessage,
          response: error?.response,
        });

        // Wait a bit before redirecting
        setTimeout(() => {
          navigate("/");
        }, 5000);
      }
    }

    handleCallback();
  }, [isAuthenticated, isLoading, isClient, getAccessTokenSilently, navigate]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
        <h2 className="text-xl font-semibold text-gray-700">Completing authentication...</h2>
        <p className="text-gray-500 mt-2">Please wait while we set up your account</p>
      </div>
    </div>
  );
}
