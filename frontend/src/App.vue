<template>
  <h1>Hello App!</h1>
  <p>
    <strong>Current route path:</strong> {{ $route.fullPath }}
  </p>
  <nav>
    <RouterLink to="/">Go to Home</RouterLink>
    <RouterLink to="/pets">Go to Pets</RouterLink>
    <RouterLink to="/componentesSergio">Go to componentes Sergio</RouterLink>
    <RouterLink to="/componentesLuis">Go to componentes Luis</RouterLink>
  </nav>
  <main>
    <RouterView />
  </main>
</template>