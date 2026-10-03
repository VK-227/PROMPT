(function () {
  "use strict";

  const params = new URLSearchParams(window.location.search);
  const requestedMode = params.get("mode");
  const hostname = window.location.hostname.toLowerCase();
  const localHost = hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1";

  // Static deployments (Vercel/custom domains) use the safe local demo by default.
  // Pass ?mode=api&baseUrl=https://... to explicitly connect to a deployed API.
  const mode = requestedMode === "api"
    ? "api"
    : (requestedMode === "mock" ? "mock" : (localHost ? "api" : "mock"));

  const baseUrl = params.get("baseUrl")
    || (localHost
      ? window.location.protocol + "//" + window.location.hostname + ":8000/api/v1"
      : "/api/v1");

  window.VAULT_CONFIG = { mode, baseUrl };
})();
