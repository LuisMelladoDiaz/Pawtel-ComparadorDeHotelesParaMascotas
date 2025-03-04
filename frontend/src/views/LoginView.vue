<script setup lang="ts">
import { ref } from "vue";
import { useLoginMutation, useLogoutMutation, useUserQuery } from "../data-layer/auth.ts";

const username = ref("");
const password = ref("");
const loginMutation = useLoginMutation();
const logoutMutation = useLogoutMutation();
const { data: user, isLoading } = useUserQuery();

const login = async () => {
  await loginMutation.mutateAsync({ username: username.value, password: password.value });
};

const logout = async () => {
  await logoutMutation.mutateAsync();
};
</script>

<template>
  <div>
    <div v-if="isLoading">Loading...</div>
    <div v-if="user">
      <p>Welcome, {{ user.username }}!</p>
      <button @click="logout">Logout</button>
    </div>
    <div v-else>
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="login">Login</button>
    </div>
  </div>
</template>
