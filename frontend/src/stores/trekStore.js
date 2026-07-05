import { defineStore } from "pinia";
import { computed, ref } from "vue";
import axiosInstance from "../utils/axioUtil";
import { useFlashStore } from "./flashStore";

export const useTrekStore = defineStore("treks", () => {

    const flashStore = useFlashStore();

    // State variables
    const treks = ref([]);
    const loadingtreks = ref(false);
    const editingTrek = ref(null)
    const loadingEditingTrek = ref(false)
    const treksearchQuery = ref("");

    // Getters 
    const filteredTreks = computed(() => {

        const query = treksearchQuery.value.trim().toLowerCase();

        if (!query) return treks.value; // return the all treks if no search query is provided

        return treks.value.filter((trek) => { // filter the treks array based on the search query

            return (

                trek.name.toLowerCase().includes(query) ||

                trek.location.toLowerCase().includes(query) ||

                trek.difficulty.toLowerCase().includes(query) ||

                trek.status.toLowerCase().includes(query) ||

                trek.id == String(query)

            );

        });

    });


    // Actions
    async function fetchTreks() {

        loadingtreks.value = true;

        try {

            const { data } = await axiosInstance.get("/admin/treks");


            treks.value = data.treks;

        } finally {

            loadingtreks.value = false;

        }
    }

    async function fetchTrekById(trekId) {
        try {
            const { data } = await axiosInstance.get(`/admin/edittrek/${trekId}`);
            editingTrek.value = data.trek;
        } catch (error) {
            console.error("Error fetching trek by ID:", error);
        }
    }

    async function updateTrek(trekId, trekData) {
        loadingEditingTrek.value = true;
        try {
            await axiosInstance.post(`/admin/edittrek/${trekId}`, trekData);
            fetchTreks();
            flashStore.show("Trek saved successfully.", "success");
            // close the modal after saving
            // editingTrek.value = null;
        } catch (error) {
            console.log(error)
            flashStore.show(error.response?.data?.message || "Error saving trek.", "error");
            loadingEditingTrek.value = false;
        } finally {
            loadingEditingTrek.value = false;
        }
    }

    async function deleteTrek(trekId) {
        try {
            await axiosInstance.post(`/admin/deletetrek/${trekId}`);
            fetchTreks();
            flashStore.show("Trek deleted successfully.", "success");
        } catch (error) {
            flashStore.show(error.response?.data?.message || "Error deleting trek.", "error");
        }
    }

    return {
        // State
        treks,
        loadingtreks,
        editingTrek,
        treksearchQuery,
        filteredTreks,


        // Actions
        fetchTreks,
        fetchTrekById,
        updateTrek,
        deleteTrek
    };
});