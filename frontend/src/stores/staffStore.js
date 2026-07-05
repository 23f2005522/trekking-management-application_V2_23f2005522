import { defineStore } from "pinia";
import { computed, ref, watch } from "vue";
import { useFlashStore } from "./flashStore";
import axiosInstance from "@/utils/axioUtil";


export const useStaffStore = defineStore("Staff", () => {

    const flashStore = useFlashStore();

    // State variables
    const loadingStaffs = ref(false);
    const allStaffs = ref([]);
    const staffsearchQuery = ref("");

    const selectedStaffId = ref(null);

    // moved in from the modal
    const selectedStatus = ref("");
    const reason = ref("");

    //gettres
    const filteredStaffs = computed(() => {
        const query = staffsearchQuery.value.trim().toLowerCase();
        if (!query) return allStaffs.value;

        return allStaffs.value.filter((staff) => {
            return (
                staff.username.toLowerCase().includes(query) ||
                staff.email.toLowerCase().includes(query) ||
                staff.status.toLowerCase().includes(query) ||
                staff.user_id == String(query)
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
    // (this replaces the watch that used to live inside manageStaffModal.vue)
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

    // Actions
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

    async function handelEditStaff() {
        try {
            const response = await axiosInstance.post(
                `/admin/staffs/${selectedStaffId.value}/${selectedStatus.value}`,
                { reason: reason.value }
            );

            flashStore.show(response.data.message || "Staff updated successfully.", "success");

            //refresh the staff list after editing
            await allFetchStaffs();

        } catch (error) {
            flashStore.show(error.response?.data?.message || "Failed to edit staff.", "error");
            console.error("Error editing staff:", error);
        }
    }


    return {
        // State variables
        allStaffs,
        loadingStaffs,
        staffsearchQuery,

        selectedStaffId,
        selectedStaff,
        selectedStatus,
        reason,

        // Getters
        filteredStaffs,
        approvedStaffs,
        rejectedStaffs,
        pendingStaffs,
        blacklistedStaffs,

        // Actions
        allFetchStaffs,
        handelEditStaff

    }

})