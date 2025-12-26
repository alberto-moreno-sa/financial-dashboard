import axios from "axios";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
});

// Note: Authorization header is added by useAuthenticatedClient hook
// which uses Auth0's getAccessTokenSilently() to get fresh tokens

// Response interceptor: Handle errors
apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    // Return a meaningful error message
    const errorMessage = err.response?.data?.detail || err.message || "An error occurred";
    return Promise.reject(errorMessage);
  }
);
