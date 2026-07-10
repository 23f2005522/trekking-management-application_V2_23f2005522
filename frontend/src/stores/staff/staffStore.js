import { defineStore } from "pinia";
import { computed, ref } from "vue";
import axiosInstance from "../../utils/axioUtil";
import { useFlashStore } from "../flashStore";

export const userStaffStore = defineStore("staffDashboard", () => {
    const flashStore = useFlashStore();

    // state
    const staffProfile = ref(null);
    const assignedTreks = ref([]);
    const loadingDashboard = ref(false);
    const loadingProfile = ref(false);

    const managingTrek = ref(null);
    const loadingManagingTrek = ref(false);
    const savingTrekStatus = ref(false);
    const updatingSlotsId = ref(null);

    const participantsTrek = ref(null);
    const participants = ref([]);
    const loadingParticipants = ref(false);

    // getters
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

    // actions
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
            throw error;
        } finally {
            loadingDashboard.value = false;
        }
    }

    async function fetchProfile() {
        loadingProfile.value = true;

        try {
            const { data } = await axiosInstance.get("/staff/profile");
            staffProfile.value = data.staff_profile;
            return data.staff_profile;
        } catch (error) {
            flashStore.show(
                error.response?.data?.message || "Failed to fetch profile.",
                "error"
            );
            throw error;
        } finally {
            loadingProfile.value = false;
        }
    }

    async function fetchTrekById(trekId) {
        if (!trekId) {
            managingTrek.value = null;
            return null;
        }

        loadingManagingTrek.value = true;

        try {
            const { data } = await axiosInstance.get(`/staff/treks/${trekId}`);
            managingTrek.value = data.trek;
            return data.trek;
        } catch (error) {
            managingTrek.value = null;
            flashStore.show(
                error.response?.data?.message || "Failed to load trek details.",
                "error"
            );
            throw error;
        } finally {
            loadingManagingTrek.value = false;
        }
    }

    async function updateTrekStatus(trekId, status) {
        savingTrekStatus.value = true;

        try {
            const { data } = await axiosInstance.post(`/staff/treks/${trekId}/status`, {
                status,
            });

            managingTrek.value = data.trek;
            await fetchDashboardData();
            flashStore.show(data.message || "Trek status updated successfully.", "success");
            return data.trek;
        } catch (error) {
            flashStore.show(
                error.response?.data?.message || "Failed to update trek status.",
                "error"
            );
            throw error;
        } finally {
            savingTrekStatus.value = false;
        }
    }

    async function updateTrekSlots(trekId, availableSlots) {
        updatingSlotsId.value = trekId;

        try {
            const { data } = await axiosInstance.post(`/staff/treks/${trekId}/slots`, {
                available_slots: availableSlots,
            });

            flashStore.show(data.message || "Available slots updated successfully.", "success");
            await fetchDashboardData();
            return data.trek;
        } catch (error) {
            flashStore.show(
                error.response?.data?.message || "Failed to update available slots.",
                "error"
            );
            throw error;
        } finally {
            updatingSlotsId.value = null;
        }
    }

    async function fetchParticipants(trekId) {
        if (!trekId) {
            participantsTrek.value = null;
            participants.value = [];
            return;
        }

        loadingParticipants.value = true;

        try {
            const { data } = await axiosInstance.get(`/staff/treks/${trekId}/participants`);
            participantsTrek.value = data.trek;
            participants.value = data.participants || [];
        } catch (error) {
            participantsTrek.value = null;
            participants.value = [];
            flashStore.show(
                error.response?.data?.message || "Failed to load participants.",
                "error"
            );
        } finally {
            loadingParticipants.value = false;
        }
    }

    async function toggleParticipantPayment(trekId, bookingId) {
        try {
            const { data } = await axiosInstance.post(
                `/staff/treks/${trekId}/participants/${bookingId}/payment`
            );

            const participant = participants.value.find((p) => p.id === bookingId);
            if (participant) {
                participant.payment_status = data.payment_status;
            }

            flashStore.show(data.message, "success");
            return data.payment_status;
        } catch (error) {
            flashStore.show(
                error.response?.data?.message || "Failed to update payment status.",
                "error"
            );
            throw error;
        }
    }

    function resetDashboardData() {
        staffProfile.value = null;
        assignedTreks.value = [];
        loadingDashboard.value = false;
        loadingProfile.value = false;
        managingTrek.value = null;
        loadingManagingTrek.value = false;
        savingTrekStatus.value = false;
        updatingSlotsId.value = null;
        participantsTrek.value = null;
        participants.value = [];
        loadingParticipants.value = false;
    }

    return {
        staffProfile,
        assignedTreks,
        loadingDashboard,
        loadingProfile,
        dashboardStats,
        fetchDashboardData,
        fetchProfile,

        managingTrek,
        loadingManagingTrek,
        savingTrekStatus,
        updatingSlotsId,
        fetchTrekById,
        updateTrekStatus,
        updateTrekSlots,

        participantsTrek,
        participants,
        loadingParticipants,
        fetchParticipants,
        toggleParticipantPayment,

        resetDashboardData,
    };
});
