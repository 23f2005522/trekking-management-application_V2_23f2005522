import axiosInstance from "@/utils/axioUtil";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const userTrekkerStore = defineStore("Trekker", () => {

    // manageTrekkers
    // state
    const allTrekkers = ref([]);
    const trekkersearchQuery = ref("");
    const loadingTrekkers = ref(false);

    // getters
    const filteredTrekkers = computed(() => {
        const query = trekkersearchQuery.value.trim().toLowerCase();
        if (!query) return allTrekkers.value;
        return allTrekkers.value.filter((trekker) => {
            return (
                trekker.username.toLowerCase().includes(query) ||
                trekker.email.toLowerCase().includes(query) ||
                trekker.is_blacklisted.toString().includes(query) ||
                trekker.user_id == String(query)
            );
        });
    });

    // actions
    const fetchAllTrekkers = async () => {
        loadingTrekkers.value = true;
        try {
            const { data } = await axiosInstance.get("/admin/trekkers");
            allTrekkers.value = data.trekkers;
            return data;
        } finally {
            loadingTrekkers.value = false;
        }
    };

    // manageTrekkerModal
    // state
    const selectedTrekkerId = ref(null);

    // getters
    const selectedTrekker = computed(() => {
        return allTrekkers.value.find(
            (trekker) => trekker.user_id === selectedTrekkerId.value
        ) || null;
    });

    // actions
    const handleEditTrekker = async (userId, status, reason) => {
        const response = await axiosInstance.post(`/admin/trekkers/${userId}/${status}`, {
            reason: reason,
        });
        await fetchAllTrekkers();
        return response.data;
    };

    return {
        allTrekkers,
        trekkersearchQuery,
        selectedTrekkerId,
        loadingTrekkers,

        filteredTrekkers,
        selectedTrekker,

        fetchAllTrekkers,
        handleEditTrekker,
    };
});
