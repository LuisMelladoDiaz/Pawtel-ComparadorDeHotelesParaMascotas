import axios from "axios";

export function refreshAxiosInterceptor() {
  axios.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    // Check if the request URL starts with "/auth"
    if (token && config.url && !config.url.includes("/auth")) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    else {
      delete config.headers.Authorization;
    }

    return config;
  });
}

// if 401 is received, delete the access token and refresh token
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      refreshAxiosInterceptor();
    }

    return Promise.reject(error);
  }
);
