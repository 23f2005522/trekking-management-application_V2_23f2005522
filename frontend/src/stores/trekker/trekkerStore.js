import { defineStore } from "pinia";
import { ref } from "vue";
import axiosInstance from "@/utils/axioUtil";
import { useFlashStore } from "@/stores/flashStore";

export const useTrekkerStore = defineStore("trekker", () => {
    const flashStore = useFlashStore();

    // Dashboard state
    const trekkerProfile = ref(null);
    const dashboardStats = ref(null);
    const recentOpenTreks = ref([]);
    const recentBookings = ref([]);
    const loadingDashboard = ref(false);




    // Fetch trekker dashboard data from backend
    async function fetchDashboardData() {
        loadingDashboard.value = true;

        try {
            const { data } = await axiosInstance.get("/trekker/dashboard");

            trekkerProfile.value = data.trekker_profile;
            dashboardStats.value = data.dashboard_stats;
            recentOpenTreks.value = data.recent_open_treks || [];
            recentBookings.value = data.recent_bookings || [];
        } catch (error) {
            flashStore.show(
                error.response?.data?.message || "Failed to load trekker dashboard.",
                "error"
            );
        } finally {
            loadingDashboard.value = false;
        }
    }

    function resetDashboardData() {
        trekkerProfile.value = null;
        dashboardStats.value = null;
        recentOpenTreks.value = [];
        recentBookings.value = [];
        loadingDashboard.value = false;
    }




    






    return {
        trekkerProfile,
        dashboardStats,
        recentOpenTreks,
        recentBookings,
        loadingDashboard,
        fetchDashboardData,
        resetDashboardData,
    };
});
