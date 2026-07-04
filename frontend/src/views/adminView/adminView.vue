<script setup>
import AdminSidebar from "./adminSidebar.vue";
</script>

<template>
  <div class="container-fluid">
    <div class="row">

      <!-- Sidebar -->
      <div class="col-auto p-0">
        <AdminSidebar />
      </div>

      <!-- Dynamic Page -->
      <div class="col p-4">
        <RouterView />
      </div>

    </div>
  </div>
</template>