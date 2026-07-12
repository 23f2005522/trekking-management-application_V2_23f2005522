import router from "@/router";
import axiosInstance from "./axioUtil";
import { useNotificationStore } from "@/stores/notificationStore";

export default async function logout() {
    const notificationStore = useNotificationStore();
    notificationStore.disconnectSSE();

    try {
        localStorage.removeItem('access_token');
        localStorage.removeItem('role');
        localStorage.removeItem('username');
        localStorage.removeItem('user_id');
        await axiosInstance.post('/auth/logout');
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
