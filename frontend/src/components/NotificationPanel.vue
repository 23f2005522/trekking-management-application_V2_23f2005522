<script setup>
import { ref } from 'vue'
import { Offcanvas } from 'bootstrap'
import { useUserNotificationStore } from '@/stores/userNotificationStore'
import { useFlashStore } from '@/stores/flashStore'

const props = defineProps({
  panelId: {
    type: String,
    required: true,
  },
})

const notificationStore = useUserNotificationStore()
const flashStore = useFlashStore()
const expandedId = ref(null)

const typeBadgeClass = (type) => {
  const map = {
    reminder: 'bg-info text-dark',
    report: 'bg-primary',
    export: 'bg-success',
    booking: 'bg-warning text-dark',
  }
  return map[type] || 'bg-secondary'
}

const typeLabel = (type) => {
  if (!type) return 'Notice'
  return type.charAt(0).toUpperCase() + type.slice(1)
}

const openPanel = async () => {
  try {
    await notificationStore.fetchNotifications()
    const panel = document.getElementById(props.panelId)
    if (panel) {
      Offcanvas.getOrCreateInstance(panel).show()
    }
  } catch (error) {
    flashStore.show(
      error?.response?.data?.message || 'Failed to load notifications.',
      'error'
    )
  }
}

const handleAccordionToggle = async (notification) => {
  if (expandedId.value === notification.id) {
    expandedId.value = null
    return
  }

  expandedId.value = notification.id

  try {
    await notificationStore.markAsRead(notification.id)
  } catch (error) {
    flashStore.show(
      error?.response?.data?.message || 'Failed to mark notification as read.',
      'error'
    )
  }
}

const handleDelete = async (notificationId) => {
  try {
    await notificationStore.deleteNotification(notificationId)
    if (expandedId.value === notificationId) {
      expandedId.value = null
    }
    flashStore.show('Notification deleted.', 'success')
  } catch (error) {
    flashStore.show(
      error?.response?.data?.message || 'Failed to delete notification.',
      'error'
    )
  }
}

const handleMarkAllRead = async () => {
  try {
    await notificationStore.markAllAsRead()
    flashStore.show('All notifications marked as read.', 'success')
  } catch (error) {
    flashStore.show(
      error?.response?.data?.message || 'Failed to mark all as read.',
      'error'
    )
  }
}
</script>

<template>
  <div>
    <button
      type="button"
      class="btn btn-outline-success position-relative"
      aria-label="Open notifications"
      @click="openPanel"
    >
      <i class="bi bi-bell fs-5"></i>
      <span
        v-if="notificationStore.unreadCount > 0"
        class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
      >
        {{ notificationStore.unreadCount > 9 ? '9+' : notificationStore.unreadCount }}
      </span>
    </button>

    <div
      class="offcanvas offcanvas-end notification-panel"
      tabindex="-1"
      :id="panelId"
    >
      <div class="offcanvas-header bg-success text-white border-bottom border-light">
        <h5 class="offcanvas-title fw-bold mb-0">
          <i class="bi bi-bell-fill me-2"></i>
          Notifications
        </h5>
        <div class="d-flex align-items-center gap-2">
          <button
            v-if="notificationStore.unreadCount > 0"
            type="button"
            class="btn btn-sm btn-light text-success"
            @click="handleMarkAllRead"
          >
            Mark all read
          </button>
          <button
            type="button"
            class="btn-close btn-close-white"
            data-bs-dismiss="offcanvas"
            aria-label="Close"
          ></button>
        </div>
      </div>

      <div class="offcanvas-body bg-light p-0">
        <div v-if="notificationStore.loading" class="text-center text-muted py-5">
          <div class="spinner-border text-success" role="status"></div>
          <p class="mt-2 mb-0">Loading notifications...</p>
        </div>

        <div
          v-else-if="notificationStore.notifications.length === 0"
          class="text-center text-muted py-5 px-3"
        >
          <i class="bi bi-bell-slash fs-1 d-block mb-2"></i>
          <p class="mb-0">No notifications yet.</p>
        </div>

        <div v-else class="accordion accordion-flush" id="notificationAccordion">
          <div
            v-for="notification in notificationStore.notifications"
            :key="notification.id"
            class="accordion-item border-0 border-bottom"
          >
            <h2 class="accordion-header">
              <button
                class="accordion-button collapsed py-3"
                :class="{ 'unread-notification': !notification.is_read }"
                type="button"
                data-bs-toggle="collapse"
                :data-bs-target="`#notification-body-${notification.id}`"
                @click="handleAccordionToggle(notification)"
              >
                <div class="w-100 pe-2">
                  <div class="d-flex justify-content-between align-items-start gap-2 mb-1">
                    <span
                      class="badge rounded-pill"
                      :class="typeBadgeClass(notification.type)"
                    >
                      {{ typeLabel(notification.type) }}
                    </span>
                    <small class="text-muted">{{ notification.created_at }}</small>
                  </div>
                  <div class="d-flex align-items-center gap-2">
                    <span
                      v-if="!notification.is_read"
                      class="badge bg-danger rounded-pill"
                    >
                      New
                    </span>
                    <span class="text-truncate notification-preview">
                      {{ notification.message_text }}
                    </span>
                  </div>
                </div>
              </button>
            </h2>

            <div
              :id="`notification-body-${notification.id}`"
              class="accordion-collapse collapse"
              data-bs-parent="#notificationAccordion"
            >
              <div class="accordion-body bg-white">
                <p class="mb-3">{{ notification.message_text }}</p>
                <div class="d-flex justify-content-between align-items-center">
                  <small class="text-muted">
                    <i class="bi bi-clock me-1"></i>
                    {{ notification.created_at }}
                  </small>
                  <button
                    type="button"
                    class="btn btn-sm btn-outline-danger"
                    @click.stop="handleDelete(notification.id)"
                  >
                    <i class="bi bi-trash me-1"></i>
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.notification-panel {
  width: min(420px, 92vw);
}

.unread-notification {
  background-color: #e8f5e9;
  font-weight: 600;
}

.notification-preview {
  max-width: 240px;
}

.accordion-button:not(.collapsed) {
  background-color: #f1f8f4;
  color: #198754;
  box-shadow: none;
}

.accordion-button:focus {
  box-shadow: none;
  border-color: rgba(25, 135, 84, 0.25);
}
</style>
