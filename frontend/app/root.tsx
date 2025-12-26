import { Links, Meta, Outlet, Scripts, ScrollRestoration } from "react-router";
import { Auth0Provider } from "@auth0/auth0-react";
// NOTA: Ruta actualizada a 'core'
import styles from "./core/styles/app.css?url";
import { QueryProvider } from "~/core/providers/QueryProvider";
import { Toaster } from "sonner";
import type { LinksFunction } from "react-router";

export const links: LinksFunction = () => [
  { rel: "stylesheet", href: styles },
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  { rel: "preconnect", href: "https://fonts.gstatic.com", crossOrigin: "anonymous" },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  },
];

export default function App() {
  const onRedirectCallback = (appState: any) => {
    window.location.href = appState?.returnTo || "/dashboard/portfolio";
  };

  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        <Auth0Provider
          domain={import.meta.env.VITE_AUTH0_DOMAIN}
          clientId={import.meta.env.VITE_AUTH0_CLIENT_ID}
          authorizationParams={{
            redirect_uri: import.meta.env.VITE_AUTH0_REDIRECT_URI,
            audience: import.meta.env.VITE_AUTH0_AUDIENCE,
          }}
          onRedirectCallback={onRedirectCallback}
          useRefreshTokens
          cacheLocation="localstorage"
        >
          <QueryProvider>
            <Outlet />
            <Toaster richColors position="top-right" />
          </QueryProvider>
        </Auth0Provider>
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}
