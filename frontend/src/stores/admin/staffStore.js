import { defineStore } from "pinia";
import { computed, ref, watch } from "vue";
import { useFlashStore } from "../flashStore";
import axiosInstance from "@/utils/axioUtil";


export const useStaffStore = defineStore("adminStaff", () => {

    const flashStore = useFlashStore();

    // state
    const loadingStaffs = ref(false);
    const allStaffs = ref([]);
    const staffsearchQuery = ref("");

    const selectedStaffId = ref(null);
    const selectedStatus = ref("");
    const reason = ref("");

    // getters
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

    // whenever the selected staff changes, sync the form fields
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

    // actions
    async function allFetchStaffs() {
        loadingStaffs.value = true;
        try {
            const { data } = await axiosInstance.get("/admin/staffs");
            allStaffs.value = data.staffs;

        } catch (error) {
            flashStore.show(error.response?.data?.message || "Failed to fetch staffs.", "error");
            console.error("Error fetching staffs:", error);
        } finally {
            loadingStaffs.value = false;
        }
    }

    async function fetchStaffs() {
        return allFetchStaffs();
    }

    async function handelEditStaff() {
        try {
            const response = await axiosInstance.post(
                `/admin/staffs/${selectedStaffId.value}/${selectedStatus.value}`,
                { reason: reason.value }
            );

            flashStore.show(response.data.message || "Staff updated successfully.", "success");

            await allFetchStaffs();

        } catch (error) {
            flashStore.show(error.response?.data?.message || "Failed to edit staff.", "error");
            console.error("Error editing staff:", error);
        }
    }

    async function createStaff(staffData) {
        try {
            const response = await axiosInstance.post("/admin/create_staff", staffData);
            flashStore.show(response.data.message || "Staff created successfully.", "success");
            await allFetchStaffs();
            return response.data;
        } catch (error) {
            flashStore.show(error.response?.data?.message || "Failed to create staff.", "error");
            throw error;
        }
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