import axiosInstance from "@/utils/axioUtil";
import { defineStore } from "pinia";
import { computed, ref, } from "vue";

export const userTrekkerStore = defineStore("Trekker", () => {

    const allTrekkers = ref([])
    const trekkersearchQuery = ref("")
    const selectedTrekkerId = ref(null)

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

    const selectedTrekker = computed(() => {
        return allTrekkers.value.find(
            trekker => trekker.user_id === selectedTrekkerId.value
        ) || null;
    })

    const fetchAllTrekkers = async () => {
        const { data } = await axiosInstance.get("/admin/trekkers")
        allTrekkers.value = data.trekkers
        return data
    }

    const handleEditTrekker = async (userId, status, reason) => {
        const response = await axiosInstance.post(`/admin/trekkers/${userId}/${status}`, {
            reason: reason
        })
        await fetchAllTrekkers()
        return response.data
    }

    return {
        allTrekkers,
        trekkersearchQuery,
        selectedTrekkerId,

        filteredTrekkers,
        selectedTrekker,

        fetchAllTrekkers,
        handleEditTrekker
    }
})
