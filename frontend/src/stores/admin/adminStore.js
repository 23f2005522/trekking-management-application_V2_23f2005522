import { defineStore } from "pinia";
import { ref } from "vue";
import axiosInstance from "../../utils/axioUtil";

export const useAdminStore = defineStore("Admin", () => {

    // adminDashboardView
    // state
    const admin = ref(null);
    const dashboardData = ref(null);
    const loadingAdmin = ref(false);

    // actions
    const fetchAdminData = async () => {
        if (admin.value && dashboardData.value) return;

        loadingAdmin.value = true;

        try {
            const { data } = await axiosInstance.get("/admin/data");

            admin.value = data.admin_user;
            dashboardData.value = data.dashboard_stats;

            return data;
        } catch (error) {
            throw error;
        } finally {
            loadingAdmin.value = false;
        }
    };

    // adminReport
    // state
    const report = ref(null);
    const loadingReport = ref(false);

    // actions
    async function fetchReport() {
        loadingReport.value = true;

        try {
            const { data } = await axiosInstance.get("/admin/report");
            report.value = data;
            return data;
        } catch (error) {
            throw error;
        } finally {
            loadingReport.value = false;
        }
    }

    return {
        admin,
        loadingAdmin,
        dashboardData,
        report,
        loadingReport,

        fetchAdminData,
        fetchReport,
    };
});
