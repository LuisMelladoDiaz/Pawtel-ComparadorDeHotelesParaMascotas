import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import api from "@/api";
import router from "../router";
import { ref, computed, watchEffect } from "vue";

export const useUserQuery = () => {
  return useQuery({
    queryKey: ["user"],
    queryFn: async () => {
      const response = await api.get("auth/user-info/");
      return await response.json();
    },
    retry: false,
  });
};

const _useIsLoggedIn = () => {
  return useQuery({
    queryKey: ["isLoggedIn", "user"],
    queryFn: async () => {
      const response = await api.get("auth/user-info/");
      return response.ok;
    },
    retry: false,
    initialData: ref(false),
  });
};

export const useIsLoggedIn = () => {
  const q = _useIsLoggedIn();
  const d = computed(() => q.isError.value ? false : q.isLoading.value ? false : q.data.value || false);
  watchEffect(() => {
    console.log("useIsLoggedIn", d.value, import.meta.env.VITE_API_BASE_URL);
    console.log("isLoading", q.isLoading.value);
    console.log("data", q.data.value);
    console.log("error", q.error.value);
  });
  return {
    data: d,
    isLoading: q.isLoading,
    isError: q.isError,
  };
};

export const useLoginMutation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (credentials: { username: string; password: string }) => {
      const response = await api.post("auth/login/", { json: credentials }).json<{ access: string; refresh: string }>();
      const { access, refresh } = response;
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      return response;
    },
    onSuccess: () => {
      queryClient.invalidateQueries();
    },
  });
};

export const useLogoutMutation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      router.push("/login");
    },
    onSuccess: () => {
      queryClient.clear();
      router.push("/login");
    },
  });
};

export const useRoleQuery = () => {
  return useQuery({
    queryKey: ["role"],
    queryFn: async () => {
      const response = await api.get("auth/user-info/");
      const data = await response.json() as any;
      return data.role;
    },
    retry: false,
  });
};

export const useIsRole = (role: string) => {
  const roleQuery = useRoleQuery();

  const isRole = computed(() => {
    return roleQuery.isLoading.value ? false : roleQuery.data.value == role;
  });

  return {
    isRole,
    isLoading: roleQuery.isLoading,
    isError: roleQuery.isError,
  };
};

export const usePasswordResetMutation = () => {
  return useMutation({
    mutationFn: async (data: { email: string }) => {
      const response = await api.post("auth/email-password-reset/", { json: data });
      return await response.json();
    },
    onError: (error) => {
      console.error("El email introducido no tiene una cuenta con nosotros", error);
    },
  });
};

export const usePasswordResetConfirmMutation = () => {
  return useMutation({
    mutationFn: async ({ uidb64, token, password }: { uidb64: string; token: string; password: string }) => {
      const response = await api.post(`auth/password-reset-confirm/${uidb64}/${token}/`, { json: { password } });
      return await response.json();
    },
    onError: (error) => {
      console.error("Error al restablecer la contraseña", error);
    },
  });
};
