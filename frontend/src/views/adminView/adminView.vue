<script setup>
import { onMounted, onUnmounted } from 'vue'
import AdminSidebar from './adminSidebar.vue'
import { useNotificationStore } from '@/stores/notificationStore'

const notificationStore = useNotificationStore()

onMounted(() => {
  notificationStore.connectSSE()
})

onUnmounted(() => {
  notificationStore.disconnectSSE()
})
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col-1 p-0">
        <AdminSidebar />
      </div>

      <div class="col-11">
        <div class="py-4">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>
