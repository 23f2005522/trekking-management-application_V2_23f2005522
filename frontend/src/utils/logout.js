import router from "@/router";
import axiosInstance from "./axioUtil";
import { useNotificationStore } from "@/stores/notificationStore";
import { useUserNotificationStore } from "@/stores/userNotificationStore";

export default async function logout() {
    const notificationStore = useNotificationStore();
    const userNotificationStore = useUserNotificationStore();
    notificationStore.disconnectSSE();
    userNotificationStore.clearNotifications();

    try {
        await axiosInstance.post('/auth/logout');
        localStorage.removeItem('access_token');
        localStorage.removeItem('role');
        localStorage.removeItem('username');
        localStorage.removeItem('user_id');
        return { success: true };
    } catch (error) {
        return {
            success: false,
            message: error.response?.data?.message || 'Error occurred while logging out.',
        };
    } finally {
        router.push({ name: 'login' });
    }
}
