<script setup>
import StaffSidebar from './StaffSidebar.vue'
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col-1 p-0">
        <StaffSidebar />
      </div>

      <div class="col-11">
        <div class="py-4">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>
