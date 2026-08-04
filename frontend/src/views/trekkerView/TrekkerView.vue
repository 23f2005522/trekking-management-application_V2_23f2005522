<script setup>
import { onMounted, onUnmounted } from 'vue'
import TrekkerSidebar from './TrekkerSidebar.vue'
import NotificationPanel from '@/components/NotificationPanel.vue'
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
        <TrekkerSidebar />
      </div>

      <div class="col-11">
        <div class="d-flex justify-content-end px-2 pt-3">
          <NotificationPanel panel-id="trekkerNotificationPanel" />
        </div>
        <div class="py-4">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>
