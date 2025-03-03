import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";
import { refreshAxiosInterceptor } from "../axios-setup";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL as string) + '/auth';

export const useUserQuery = () => {
  return useQuery({
    queryKey: ["user"],
    queryFn: async () => {
      const response = await axios.get(`${API_BASE_URL}/user-info/`);
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
      refreshAxiosInterceptor();
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
      refreshAxiosInterceptor();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user"] }); // Refresh user state
    },
  });
};
