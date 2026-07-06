import { defineStore } from "pinia";
import { computed, ref } from "vue";
import axiosInstance from "../../utils/axioUtil";
import { useFlashStore } from "../flashStore";

export const userStaffStore = defineStore("staffDashboard", () => {
    const flashStore = useFlashStore();

    // State variables
    const staffProfile = ref(null);
    const assignedTreks = ref([]);
    const loadingDashboard = ref(false);


    //getters (computed properties) 
    const dashboardStats = computed(() => {
        const totalAssignedTreks = assignedTreks.value.length;
        const activeAssignedTreks = assignedTreks.value.filter(
            (trek) => trek.status === "open" || trek.status === "approved"
        ).length;
        const totalParticipants = assignedTreks.value.reduce(
            (total, trek) => total + (trek.total_participants || 0),
            0
        );

        return {
            totalAssignedTreks,
            activeAssignedTreks,
            totalParticipants,
        };
    });




    // Actions
    async function fetchDashboardData() {
        if (loadingDashboard.value) return;

        loadingDashboard.value = true;

        try {
            const { data } = await axiosInstance.get("/staff/dashboard");

            staffProfile.value = data.staff_profile;
            assignedTreks.value = data.assigned_treks ?? [];
        } catch (error) {
            flashStore.show(
                error.response?.data?.message || "Failed to fetch staff dashboard data.",
                "error"
            );
        } finally {
            loadingDashboard.value = false;
        }
    }

    function resetDashboardData() {
        staffProfile.value = null;
        assignedTreks.value = [];
        loadingDashboard.value = false;
    }

    return {
        staffProfile,
        assignedTreks,
        loadingDashboard,
        dashboardStats,
        fetchDashboardData,
        resetDashboardData,
    };
});