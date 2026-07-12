import { defineStore } from "pinia";
import { computed, ref, watch } from "vue";
import axiosInstance from "@/utils/axioUtil";

export const useStaffStore = defineStore("adminStaff", () => {

    const loadingStaffs = ref(false);
    const allStaffs = ref([]);
    const staffsearchQuery = ref("");

    const selectedStaffId = ref(null);
    const selectedStatus = ref("");
    const reason = ref("");

    const filteredStaffs = computed(() => {
        const query = staffsearchQuery.value.trim().toLowerCase();
        if (!query) return allStaffs.value;

        return allStaffs.value.filter((staff) => {
            return (
                staff.username.toLowerCase().includes(query) ||
                staff.email.toLowerCase().includes(query) ||
                staff.status.toLowerCase().includes(query) ||
                staff.staff_id == String(query)
            );
        });
    });

    const approvedStaffs = computed(() => {
        return allStaffs.value.filter((staff) => staff.status === "approved");
    });

    const pendingStaffs = computed(() => {
        return allStaffs.value.filter((staff) => staff.status === "pending");
    });

    const rejectedStaffs = computed(() => {
        return allStaffs.value.filter((staff) => staff.status === "rejected");
    });

    const blacklistedStaffs = computed(() => {
        return allStaffs.value.filter((staff) => staff.status === "blacklisted");
    });

    const selectedStaff = computed(() => {
        return allStaffs.value.find(
            staff => staff.user_id === selectedStaffId.value
        ) || null;
    })

    watch(
        selectedStaff,
        (newVal) => {
            if (!newVal) {
                selectedStatus.value = "";
                reason.value = "";
            } else {
                selectedStatus.value = newVal.status;
                reason.value = newVal.blacklisted_reason || "";
            }
        },
        { immediate: true },
    );

    async function allFetchStaffs() {
        loadingStaffs.value = true;
        try {
            const { data } = await axiosInstance.get("/admin/staffs");
            allStaffs.value = data.staffs;
            return data;
        } finally {
            loadingStaffs.value = false;
        }
    }

    async function fetchStaffs() {
        return allFetchStaffs();
    }

    async function handelEditStaff() {
        const response = await axiosInstance.post(
            `/admin/staffs/${selectedStaffId.value}/${selectedStatus.value}`,
            { reason: reason.value }
        );
        await allFetchStaffs();
        return response.data;
    }

    async function createStaff(staffData) {
        const response = await axiosInstance.post("/admin/create_staff", staffData);
        await allFetchStaffs();
        return response.data;
    }

    return {
        allStaffs,
        loadingStaffs,
        staffsearchQuery,

        selectedStaffId,
        selectedStaff,
        selectedStatus,
        reason,

        filteredStaffs,
        approvedStaffs,
        rejectedStaffs,
        pendingStaffs,
        blacklistedStaffs,

        allFetchStaffs,
        fetchStaffs,
        handelEditStaff,
        createStaff
    }

})
