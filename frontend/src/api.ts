import ky, { HTTPError } from "ky";
import router from "./router";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

const api = ky.create({
  prefixUrl: API_BASE_URL,
  credentials: "include",
  hooks: {
    beforeRequest: [
      (request) => {
        const token = localStorage.getItem("access_token");
        if (token) {
          request.headers.set("Authorization", `Bearer ${token}`);
        } else {
          request.headers.delete("Authorization");
        }
      },
    ],
    afterResponse: [
      async (request, _options, response) => {
        // If not 401, handle empty body
        if (response.status !== 401) {
          return response;
        }

        // 401 handling (token refresh logic)
        if (request.headers.get("x-auth-retry") === "true" || request.url.includes("token/refresh")) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          if (!request.url.includes("user-info")) router.push("/login");
          throw new HTTPError(response, request, _options);
        }

        const refreshToken = localStorage.getItem("refresh_token");
        if (!refreshToken) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          throw new HTTPError(response, request, _options);
        }

        try {
          const { access, refresh } = await ky
            .post("token/refresh/", {
              prefixUrl: API_BASE_URL,
              json: { refresh: refreshToken },
              credentials: "include",
            })
            .json<{ access: string; refresh?: string }>();

          localStorage.setItem("access_token", access);
          if (refresh) localStorage.setItem("refresh_token", refresh);

          const newHeaders = new Headers(request.headers);
          newHeaders.set("Authorization", `Bearer ${access}`);
          newHeaders.set("x-auth-retry", "true");

          const retryRequest = new Request(request, { headers: newHeaders });
          return api(retryRequest);
        } catch (err) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          if (!request.url.includes("user-info")) router.push("/login");
          throw err;
        }
      },
    ],
  },
});

export default api;
