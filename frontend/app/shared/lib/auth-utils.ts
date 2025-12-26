/**
 * Authentication utility functions
 */

/**
 * Completely clears all authentication data from localStorage and cookies
 * This should be called on logout or when authentication fails
 */
export function clearAllAuthData() {
  if (typeof window === "undefined") return;

  // Clear localStorage items
  localStorage.removeItem("auth-storage"); // Zustand store
  localStorage.removeItem("auth_token"); // Legacy token storage

  // Clear Auth0 cache (these are the keys Auth0 SDK uses)
  const keysToRemove = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && (
      key.startsWith("@@auth0spajs@@") || // Auth0 SPA JS cache
      key.startsWith("a0.spajs.txs") ||   // Auth0 transaction state
      key.includes("auth0")                // Any other auth0 keys
    )) {
      keysToRemove.push(key);
    }
  }

  keysToRemove.forEach(key => localStorage.removeItem(key));

  // Clear sessionStorage
  sessionStorage.clear();

  // Clear cookies (best effort - may not work for httpOnly cookies)
  document.cookie.split(";").forEach((c) => {
    document.cookie = c
      .replace(/^ +/, "")
      .replace(/=.*/, `=;expires=${new Date().toUTCString()};path=/`);
  });

  console.log("✅ All authentication data cleared");
}

/**
 * Check if user has valid authentication data in localStorage
 */
export function hasAuthData(): boolean {
  if (typeof window === "undefined") return false;

  const authStorage = localStorage.getItem("auth-storage");
  if (!authStorage) return false;

  try {
    const parsed = JSON.parse(authStorage);
    return !!(parsed?.state?.token && parsed?.state?.user);
  } catch {
    return false;
  }
}
