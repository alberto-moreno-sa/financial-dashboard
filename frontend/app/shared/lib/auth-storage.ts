/**
 * Authentication token storage utilities
 * Handles JWT token persistence in localStorage
 */

const TOKEN_KEY = "auth_token";

export const authStorage = {
  getToken: (): string | null => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(TOKEN_KEY);
  },

  setToken: (token: string): void => {
    if (typeof window === "undefined") return;
    localStorage.setItem(TOKEN_KEY, token);
  },

  removeToken: (): void => {
    if (typeof window === "undefined") return;
    localStorage.removeItem(TOKEN_KEY);
  },

  hasToken: (): boolean => {
    return authStorage.getToken() !== null;
  },
};
