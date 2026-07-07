import { defineStore } from "pinia"
import { ref } from "vue"
import axiosInstance from "@/utils/axioUtil"

export const useTrekHistoryStore = defineStore("trekHistory", () => {

    // State
    const history = ref([])
    const loadingHistory = ref(false)

    // Action
    async function fetchHistory() {

        loadingHistory.value = true

        try {

            const response = await axiosInstance.get("/trekker/history")

            history.value = response.data.history

            return response.data

        } finally {

            loadingHistory.value = false

        }

    }

    return {

        history,
        loadingHistory,

        fetchHistory,

    }

})