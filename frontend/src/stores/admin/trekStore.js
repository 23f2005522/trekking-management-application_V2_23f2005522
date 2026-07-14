import { defineStore } from "pinia";
import { computed, ref } from "vue";
import axiosInstance from "../../utils/axioUtil";

export const useTrekStore = defineStore("treks", () => {

    // manageTrek
    // state
    const treks = ref([]);
    const loadingtreks = ref(false);
    const treksearchQuery = ref("");

    // getters
    const filteredTreks = computed(() => {
        const query = treksearchQuery.value.trim().toLowerCase();
        if (!query) return treks.value;

        return treks.value.filter((trek) => {
            return (
                trek.name.toLowerCase().includes(query) ||
                trek.location.toLowerCase().includes(query) ||
                trek.difficulty.toLowerCase().includes(query) ||
                trek.status.toLowerCase().includes(query) ||
                trek.id == String(query)
            );
        });
    });

    // actions
    async function fetchTreks() {
        loadingtreks.value = true;
        try {
            const { data } = await axiosInstance.get("/admin/treks");
            treks.value = data.treks;
            return data;
        } finally {
            loadingtreks.value = false;
        }
    }

    async function deleteTrek(trekId) {
        const { data } = await axiosInstance.post(`/admin/deletetrek/${trekId}`);
        await fetchTreks();
        return data;
    }

    // addTrekModal
    // state — uses treks (above)

    // actions
    async function addTrek(trekData) {
        const { data } = await axiosInstance.post("/admin/addtrek", trekData);
        await fetchTreks();
        return data;
    }

    // editTrekModal
    // state
    const editingTrek = ref(null);
    const loadingEditingTrek = ref(false);

    // getters — savingTrek alias exported in return

    // actions
    async function fetchTrekById(trekId) {
        loadingEditingTrek.value = true;
        editingTrek.value = null;
        try {
            const { data } = await axiosInstance.get(`/admin/edittrek/${trekId}`);
            editingTrek.value = data.trek;
            return data.trek;
        } finally {
            loadingEditingTrek.value = false;
        }
    }

    function clearEditingTrek() {
        editingTrek.value = null;
    }

    async function updateTrek(trekId, trekData) {
        loadingEditingTrek.value = true;
        try {
            const { data } = await axiosInstance.post(`/admin/edittrek/${trekId}`, trekData);
            await fetchTreks();
            return data;
        } finally {
            loadingEditingTrek.value = false;
        }
    }

    return {
        treks,
        loadingtreks,
        editingTrek,
        loadingEditingTrek,
        savingTrek: loadingEditingTrek,
        treksearchQuery,
        filteredTreks,

        fetchTreks,
        fetchTrekById,
        clearEditingTrek,
        updateTrek,
        deleteTrek,
        addTrek,
    };
});
