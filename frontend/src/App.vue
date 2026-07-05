<script setup>
import FlashMessage from './components/flashMessage.vue';
import Footer from './components/Footer.vue';
import NavBar from './components/NavBar.vue';




</script>

<template>
  <div class="d-flex flex-column min-vh-100">
    <!-- NavBar -->
    <NavBar />
    <!-- Flash Message -->
    <FlashMessage />
    <!-- Main Content -->
    <main class="flex-grow-1">
      <router-view />
    </main>
    <!-- Footer -->
    <Footer />
  </div>
</template>

<style scoped></style>
