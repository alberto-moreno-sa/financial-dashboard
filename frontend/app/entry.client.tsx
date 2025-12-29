import { HydratedRouter } from "react-router/dom";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <HydratedRouter />
  </StrictMode>
);
