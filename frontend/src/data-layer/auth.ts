import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import axios from "axios";
import router from "../router";
import {ref,computed, watchEffect} from 'vue';
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

const _useIsLoggedIn = () => {
  return useQuery({
    queryKey: ["isLoggedIn", "user"],
    queryFn: async () => {
      const response = await axios.get(`${API_BASE_URL}/user-info/`);
      return response.status === 200;
    },
    retry: false,
    initialData: ref(false),
  });
}

export const useIsLoggedIn = () => {
  const q = _useIsLoggedIn();
  const d = computed(() => q.isError.value ? false: q.isLoading.value ? false : q.data.value || false);
  watchEffect(() => {
    console.log("useIsLoggedIn", d.value);
    console.log("isLoading", q.isLoading.value);
    console.log("data", q.data.value);
    console.log("error", q.error.value);
  }
  );
  return {
    data: d,
    isLoading: q.isLoading,
    isError: q.isError,
  }
}

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
      router.push("/")
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["isLoggedIn", "user"] }); // Refresh user state
    },
  });
};

export const usePasswordResetMutation = () => {
  return useMutation({
    mutationFn: async (data) => {
      const response = await axios.post(`${API_BASE_URL}/auth/password-reset/`, data);
      return response.data;
    },
    onError: (error) => {
      console.error('El email introducido no tiene una cuenta con nosotros', error);
    },
  });
};
