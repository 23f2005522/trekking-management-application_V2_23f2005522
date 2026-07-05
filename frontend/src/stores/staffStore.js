import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { useFlashStore } from "./flashStore";
import axiosInstance from "@/utils/axioUtil";


export const useStaffStore = defineStore("Staff", () => {

    const flashStore = useFlashStore();

    // State variables
    const loadingStaffs = ref(false);
    const allStaffs = ref([]);
    const staffsearchQuery = ref("");

    const selectedStaffId = ref(null);

    //gettres
    const filteredStaffs = computed(() => {
        const query = staffsearchQuery.value.trim().toLowerCase();
        if (!query) return allStaffs.value; // return the all staffs if no search query is provided

        return allStaffs.value.filter((staff) => { // filter the staffs array based on the search query
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
    }
    );

    const blacklistedStaffs = computed(() => {
        return allStaffs.value.filter((staff) => staff.status === "blacklisted");
    });

    const selectedStaff = computed(() => {
        return allStaffs.value.find(
            staff => staff.user_id === selectedStaffId.value
        ) || null;
    })

    // Actions
    async function allFetchStaffs() {
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

    async function handelEditStaff(staffId, updateStatus, reason) {
        console.log("Editing staff with ID:", staffId, "Updated Status:", updateStatus, "Reason:", reason);
        try {
            const response = await axiosInstance.post(`/admin/staffs/${staffId}/${updateStatus}`, { reason });

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