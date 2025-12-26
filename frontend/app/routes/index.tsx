import { useNavigate } from "react-router";
import { useAuth0 } from "@auth0/auth0-react";
import { useEffect } from "react";
import { Button } from "~/shared/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "~/shared/ui/card";

export default function LoginPage() {
  const navigate = useNavigate();
  const { loginWithRedirect, isAuthenticated, isLoading } = useAuth0();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard/portfolio");
    }
  }, [isAuthenticated, navigate]);

  const handleLogin = () => {
    loginWithRedirect({
      appState: {
        returnTo: "/dashboard/portfolio",
      },
    });
  };

  return (
    <div className="bg-muted/20 flex min-h-screen items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-center text-2xl font-bold">Financial Dashboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="mb-4 text-center text-sm text-gray-500">
              Sign in to view your investment portfolio
            </div>

            <Button
              className="w-full"
              onClick={handleLogin}
              disabled={isLoading}
            >
              {isLoading ? "Loading..." : "Sign In with Auth0"}
            </Button>

            <div className="text-center text-xs text-gray-400 mt-4">
              You can use Google, GitHub or email/password
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
