import { defineStore } from "pinia";
import { computed, ref } from "vue";
import axiosInstance from "../../utils/axioUtil";

export const userStaffStore = defineStore("staffDashboard", () => {

    // staffDashboardView
    // state
    const staffProfile = ref(null);
    const assignedTreks = ref([]);
    const upcomingTreks = ref([]);
    const loadingDashboard = ref(false);

    // getters
    const dashboardStats = computed(() => {
        const totalAssignedTreks = assignedTreks.value.length;
        const activeAssignedTreks = assignedTreks.value.filter(
            (trek) => trek.status === "open"
        ).length;
        const totalParticipants = assignedTreks.value.reduce(
            (total, trek) => total + (trek.total_participants || 0),
            0
        );

        return {
            totalAssignedTreks,
            activeAssignedTreks,
            totalParticipants,
            upcomingTreksCount: upcomingTreks.value.length,
        };
    });

    // actions
    async function fetchDashboardData(silent = false) {
        if (!silent) {
            if (loadingDashboard.value) return;
            loadingDashboard.value = true;
        }

        try {
            const { data } = await axiosInstance.get("/staff/dashboard");

            staffProfile.value = data.staff_profile;
            assignedTreks.value = data.assigned_treks ?? [];
            upcomingTreks.value = data.upcoming_treks ?? [];
            return data;
        } finally {
            if (!silent) {
                loadingDashboard.value = false;
            }
        }
    }

    // StaffManageTreks
    // state
    const loadingTreks = ref(false);
    const updatingSlotsId = ref(null);

    // getters — uses assignedTreks (above)

    // actions
    async function fetchAssignedTreks(silent = false) {
        if (!silent && loadingTreks.value) return;

        if (!silent) {
            loadingTreks.value = true;
        }

        try {
            const { data } = await axiosInstance.get("/staff/treks");
            assignedTreks.value = data.assigned_treks ?? [];
            return data;
        } finally {
            if (!silent) {
                loadingTreks.value = false;
            }
        }
    }

    function clearStaleStaffViews() {
        if (managingTrek.value) {
            const stillAssigned = assignedTreks.value.some(
                (trek) => trek.id === managingTrek.value.id
            );
            if (!stillAssigned) {
                managingTrek.value = null;
            }
        }

        if (participantsTrek.value) {
            const stillAssigned = assignedTreks.value.some(
                (trek) => trek.id === participantsTrek.value.id
            );
            if (!stillAssigned) {
                participantsTrek.value = null;
                participants.value = [];
            }
        }
    }

    async function refreshAssignedData() {
        await fetchDashboardData(true);
        await fetchAssignedTreks(true);
        clearStaleStaffViews();
    }

    async function updateTrekSlots(trekId, availableSlots) {
        updatingSlotsId.value = trekId;

        try {
            const { data } = await axiosInstance.post(`/staff/treks/${trekId}/slots`, {
                available_slots: availableSlots,
            });

            await fetchAssignedTreks();
            return data;
        } finally {
            updatingSlotsId.value = null;
        }
    }

    // StaffProfile
    // state
    const loadingProfile = ref(false);

    // actions
    async function fetchProfile() {
        loadingProfile.value = true;

        try {
            const { data } = await axiosInstance.get("/staff/profile");
            staffProfile.value = data.staff_profile;
            return data.staff_profile;
        } finally {
            loadingProfile.value = false;
        }
    }

    // staffManageTrekModal, staffDashboardView
    // state
    const managingTrek = ref(null);
    const loadingManagingTrek = ref(false);
    const savingTrekStatus = ref(false);

    // actions
    async function fetchTrekById(trekId) {
        if (!trekId) {
            managingTrek.value = null;
            return null;
        }

        loadingManagingTrek.value = true;
        managingTrek.value = null;

        try {
            const { data } = await axiosInstance.get(`/staff/treks/${trekId}`);
            managingTrek.value = data.trek;
            return data.trek;
        } catch (error) {
            managingTrek.value = null;
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
            await fetchDashboardData(true);
            return data;
        } finally {
            savingTrekStatus.value = false;
        }
    }

    // StaffParticipants
    // state
    const participantsTrek = ref(null);
    const participants = ref([]);
    const loadingParticipants = ref(false);

    // actions
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
            return data;
        } catch (error) {
            participantsTrek.value = null;
            participants.value = [];
            throw error;
        } finally {
            loadingParticipants.value = false;
        }
    }

    async function toggleParticipantPayment(trekId, bookingId) {
        const { data } = await axiosInstance.post(
            `/staff/treks/${trekId}/participants/${bookingId}/payment`
        );

        const participant = participants.value.find((p) => p.id === bookingId);
        if (participant) {
            participant.payment_status = data.payment_status;
        }

        return data;
    }

    async function markAllParticipantsPaid(trekId) {
        const { data } = await axiosInstance.post(
            `/staff/treks/${trekId}/participants/mark-all-paid`
        );
        await fetchParticipants(trekId);
        return data;
    }

    return {
        staffProfile,
        assignedTreks,
        upcomingTreks,
        loadingDashboard,
        loadingTreks,
        loadingProfile,
        dashboardStats,
        fetchDashboardData,
        fetchAssignedTreks,
        refreshAssignedData,
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
        markAllParticipantsPaid,
    };
});
