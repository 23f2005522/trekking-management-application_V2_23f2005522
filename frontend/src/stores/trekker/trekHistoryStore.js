import { defineStore } from "pinia"
import { ref } from "vue"
import axiosInstance from "@/utils/axioUtil"

export const useTrekHistoryStore = defineStore("trekHistory", () => {

    const history = ref([])
    const loadingHistory = ref(false)




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
    

    // Export Jobs State Management
    const exportJobs = ref([])
    const exporting = ref(false)
    const EXPORT_COOLDOWN_MS = 5000 // keep button disabled 5s to prevent spam clicks

    async function fetchExportJobs() {
        const { data } = await axiosInstance.get("/trekker/export-jobs")
        exportJobs.value = data.export_jobs || []
        return data
    }

    async function startExport() {
        if (exporting.value) return

        exporting.value = true
        const startedAt = Date.now()

        try {
            const { data } = await axiosInstance.post("/trekker/export-history")
            await fetchExportJobs()

            const waitLeft = EXPORT_COOLDOWN_MS - (Date.now() - startedAt)
            if (waitLeft > 0) {
                await new Promise((resolve) => setTimeout(resolve, waitLeft))
            }

            return data
        } finally {
            exporting.value = false
        }
    }

    async function downloadExport(jobId) {
        const response = await axiosInstance.get(`/trekker/export/${jobId}/download`, {
            responseType: "blob",
        })

        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement("a")
        link.href = url
        link.setAttribute("download", `trek_history_${jobId}.csv`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
    }

    return {
        history,
        loadingHistory,
        exportJobs,
        exporting,
        fetchHistory,
        fetchExportJobs,
        startExport,
        downloadExport,
    }

})
