import axios from "axios";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: `${BASE_URL}/api/v1`,
  headers: { "Content-Type": "application/json" },
});

// Inject auth token
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const stored = localStorage.getItem("core-studio-auth");
    if (stored) {
      const { accessToken } = JSON.parse(stored).state || {};
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
    }
  }
  return config;
});

// Token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;

      try {
        const stored = localStorage.getItem("core-studio-auth");
        const { refreshToken } = stored ? JSON.parse(stored).state || {} : {};

        if (refreshToken) {
          const res = await axios.post(`${BASE_URL}/api/v1/auth/refresh`, {
            refresh_token: refreshToken,
          });
          const { access_token } = res.data;

          // Update stored token
          const parsed = JSON.parse(stored!);
          parsed.state.accessToken = access_token;
          localStorage.setItem("core-studio-auth", JSON.stringify(parsed));

          original.headers.Authorization = `Bearer ${access_token}`;
          return api(original);
        }
      } catch {
        // Refresh failed — clear auth and redirect
        localStorage.removeItem("core-studio-auth");
        if (typeof window !== "undefined") window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);
