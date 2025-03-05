import axios from "axios";

export function refreshAxiosInterceptor(){
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
}


// if response is 401, remove access token and refresh token
axios.interceptors.response.use(
  (response) => {
    if (response.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    }
    return response;
    },
    (error) => {
        if (error.response.status === 401) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
        }
        return Promise.reject(error);
        }
);
