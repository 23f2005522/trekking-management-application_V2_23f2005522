import { defineStore } from "pinia";
import { reactive, ref } from "vue";
import axiosInstance from "../../utils/axioUtil";
import { useFlashStore } from "./flashStore";

const flashStore = useFlashStore();

export const useAdminStore = defineStore("Admin", () => {

    //State variables
    const admin = ref(null);

    const dashboardData = ref(null);

    const loadingAdmin = ref(false);

    // Actions
    const fetchAdminData = async () => {
        loadingAdmin.value = true;

        try {
            const { data } = await axiosInstance.get("/admin/data");

            admin.value = data.admin_user;
            dashboardData.value = data.dashboard_stats;

            flashStore.show(data.message, "success");

        } catch (error) {
            flashStore.show(error.response?.data?.message || "Failed to fetch admin data.", "error");
        } finally {
            loadingAdmin.value = false;
        }
    }


    function resetAdminData() {
        admin.value = null;
        dashboardData.value = null;
        loadingAdmin.value = false;
    }

    return {
        // State
        admin,
        loadingAdmin,
        dashboardData,

        //Actions
        fetchAdminData,
        resetAdminData

    }

})