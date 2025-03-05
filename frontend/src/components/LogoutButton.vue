<script setup lang="ts">
import { useLogoutMutation } from "@/data-layer/auth";

const logoutMutation = useLogoutMutation();

const logout = async () => {
  await logoutMutation.mutateAsync();
};
</script>

<template>
  <button @click="logout">Logout</button>
</template>
