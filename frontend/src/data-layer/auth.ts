import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/auth";

export const useUserQuery = () => {
  return useQuery({
    queryKey: ["user"],
    queryFn: async () => {
      const token = localStorage.getItem("access_token");
      if (!token) throw new Error("No token available"); // Evita peticiones innecesarias

      const response = await axios.get(`${API_BASE_URL}/user-info/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      return response.data;
    },
    retry: false,
  });
};


export const useLoginMutation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (credentials: { username: string; password: string }) => {
      const response = await axios.post(`${API_BASE_URL}/login/`, credentials);

      const { access, refresh } = response.data;
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);

      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user"] });
    },
  });
};


export const useLogoutMutation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user"] }); // Para actualizar el estado del usuario
    },
  });
};
