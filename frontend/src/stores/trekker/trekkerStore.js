import { defineStore } from "pinia";
import { ref } from "vue";
import axiosInstance from "@/utils/axioUtil";

export const useTrekkerStore = defineStore("trekker", () => {

    // TrekkerDashboard
    // state
    const trekkerProfile = ref(null);
    const dashboardStats = ref(null);
    const recentOpenTreks = ref([]);
    const recentBookings = ref([]);
    const loadingDashboard = ref(false);

    // actions
    async function fetchDashboardData() {
        loadingDashboard.value = true;

        try {
            const { data } = await axiosInstance.get("/trekker/dashboard");

            trekkerProfile.value = data.trekker_profile;
            dashboardStats.value = data.dashboard_stats;
            recentOpenTreks.value = data.recent_open_treks || [];
            recentBookings.value = data.recent_bookings || [];
            return data;
        } finally {
            loadingDashboard.value = false;
        }
    }

    return {
        trekkerProfile,
        dashboardStats,
        recentOpenTreks,
        recentBookings,
        loadingDashboard,
        fetchDashboardData,
    };
});
