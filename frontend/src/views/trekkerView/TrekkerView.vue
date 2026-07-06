
<script setup>
import TrekkerSidebar from './TrekkerSidebar.vue';
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-auto p-0">
        <TrekkerSidebar />
      </div>

      <!-- Main -->
      <div class="col p-4">
        <router-view />
      </div>
    </div>
  </div>
</template>
