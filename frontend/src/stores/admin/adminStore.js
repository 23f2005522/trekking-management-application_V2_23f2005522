import { defineStore } from "pinia";
import { reactive, ref } from "vue";
import axiosInstance from "../../utils/axioUtil";
import { useFlashStore } from "../flashStore";

const flashStore = useFlashStore();

export const useAdminStore = defineStore("Admin", () => {

    // state
    const admin = ref(null);

    const dashboardData = ref(null);

    const loadingAdmin = ref(false);

    const report = ref(null);
    const loadingReport = ref(false);

    // actions
    const fetchAdminData = async () => {
        
        // if data already exists, no need to fetch again
        if( admin.value && dashboardData.value) return;
        
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


    async function fetchReport() {
        loadingReport.value = true;

        try {
            const { data } = await axiosInstance.get("/admin/report");
            report.value = data;
        } catch (error) {
            flashStore.show(
                error.response?.data?.message || "Failed to load report.",
                "error"
            );
        } finally {
            loadingReport.value = false;
        }
    }

    function resetAdminData() {
        admin.value = null;
        dashboardData.value = null;
        loadingAdmin.value = false;
        report.value = null;
        loadingReport.value = false;
    }

    return {
        admin,
        loadingAdmin,
        dashboardData,
        report,
        loadingReport,

        fetchAdminData,
        fetchReport,
        resetAdminData

    }

})