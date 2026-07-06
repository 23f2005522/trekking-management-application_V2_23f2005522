import axiosInstance from "@/utils/axioUtil";
import { defineStore } from "pinia";
import { computed, ref, } from "vue";
import { useFlashStore } from "../flashStore";


export const userTrekkerStore = defineStore("Trekker", () => {

    const flashStore = useFlashStore();


    // state
    const allTrekkers = ref([])
    const trekkersearchQuery = ref("")

    const selectedTrekkerId = ref(null)


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

    const selectedTrekker = computed(() => {
        return allTrekkers.value.find(
            trekker => trekker.user_id === selectedTrekkerId.value
        ) || null;
    })


    // actions
    const fetchAllTrekkers = async () => {
        const { data } = await axiosInstance.get("/admin/trekkers")
        allTrekkers.value = data.trekkers
    }

    const handleEditTrekker = async (userId, status, reason) => {
        try {
            const response = await axiosInstance.post(`/admin/trekkers/${userId}/${status}`, {
                reason: reason
            })
            flashStore.show(response.data.message, "success")
            await fetchAllTrekkers()
        } catch (error) {
            flashStore.show("Failed to update trekker status.", "error")
        }

    }




    return {
        // state
        allTrekkers,
        trekkersearchQuery,
        selectedTrekkerId,

        // getters
        filteredTrekkers,
        selectedTrekker,

        // actions
        fetchAllTrekkers,
        handleEditTrekker

    }
})