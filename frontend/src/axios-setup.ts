import axios from "axios";

export function refreshAxiosInterceptor() {
  axios.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    console.log(config)
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
