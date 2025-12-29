import { useNavigate } from "react-router";
import { useEffect } from "react";

export default function DemoRedirect() {
  const navigate = useNavigate();

  useEffect(() => {
    // In demo mode, redirect directly to portfolio
    navigate("/dashboard/portfolio", { replace: true });
  }, [navigate]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h1 className="text-2xl font-bold">Loading Demo...</h1>
        <p className="mt-2 text-gray-600">Redirecting to portfolio</p>
      </div>
    </div>
  );
}
