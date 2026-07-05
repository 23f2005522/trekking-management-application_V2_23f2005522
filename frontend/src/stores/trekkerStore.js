import axiosInstance from "@/utils/axioUtil";
import { defineStore } from "pinia";
import { computed, ref, } from "vue";


export const userTrekkerStore = defineStore("Trekker", () => {



    // state
    const allTrekkers = ref([])
    const trekkersearchQuery = ref("")

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
        const { data } = await axiosInstance.get("/admin/trekkers")
        allTrekkers.value = data.trekkers
    }



    return {
        // state
        allTrekkers,
        trekkersearchQuery,

        // getters
        filteredTrekkers,

        // actions
        fetchAllTrekkers

    }
})