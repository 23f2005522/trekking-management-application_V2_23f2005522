import router from "@/router";
import axiosInstance from "./axioUtil";
import { useFlashStore } from "@/stores/flashStore";

export default async function logout() {

    try {
        localStorage.removeItem('access_token');
        localStorage.removeItem('role');
        localStorage.removeItem('username');
        const { data } = await axiosInstance.post('/auth/logout');
    } catch (error) {
        useFlashStore().show(error.response?.data?.message || 'Error occurred while logging out.', 'error');
    } finally {
        useFlashStore().show('Logged out.', 'success');
        router.push({ name: 'login' });
    }
}     
