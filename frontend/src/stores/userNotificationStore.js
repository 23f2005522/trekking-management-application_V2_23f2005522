import { defineStore } from "pinia";
import { computed, ref } from "vue";
import axiosInstance from "@/utils/axioUtil";

export const useUserNotificationStore = defineStore("userNotifications", () => {
    const notifications = ref([]);
    const loading = ref(false);

    const unreadCount = computed(
        () => notifications.value.filter((item) => !item.is_read).length
    );

    async function fetchNotifications(options = {}) {
        const silent = options.silent === true;

        if (!silent) {
            loading.value = true;
        }

        try {
            const { data } = await axiosInstance.get("/notifications");
            notifications.value = data.notifications || [];
        } finally {
            if (!silent) {
                loading.value = false;
            }
        }
    }

    async function markAsRead(notificationId) {
        const item = notifications.value.find((n) => n.id === notificationId);
        if (!item || item.is_read) return;

        item.is_read = true;

        try {
            await axiosInstance.post(`/notifications/${notificationId}/read`);
        } catch (error) {
            item.is_read = false;
            throw error;
        }
    }

    async function deleteNotification(notificationId) {
        const index = notifications.value.findIndex((n) => n.id === notificationId);
        if (index === -1) return;

        const removed = notifications.value[index];
        notifications.value.splice(index, 1);

        try {
            await axiosInstance.delete(`/notifications/${notificationId}`);
        } catch (error) {
            notifications.value.splice(index, 0, removed);
            throw error;
        }
    }

    async function markAllAsRead() {
        await axiosInstance.post("/notifications/read-all");
        notifications.value = notifications.value.map((item) => ({
            ...item,
            is_read: true,
        }));
    }

    function clearNotifications() {
        notifications.value = [];
    }

    return {
        notifications,
        loading,
        unreadCount,
        fetchNotifications,
        markAsRead,
        deleteNotification,
        markAllAsRead,
        clearNotifications,
    };
});
