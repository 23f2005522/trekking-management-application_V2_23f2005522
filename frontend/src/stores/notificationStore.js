import { defineStore } from "pinia"
import { useFlashStore } from "@/stores/flashStore"
import { useTrekHistoryStore } from "@/stores/trekker/trekHistoryStore"

const SSE_BASE = "http://127.0.0.1:5000/stream"

export const useNotificationStore = defineStore("notifications", () => {
    let eventSource = null

    function connectSSE() {
        const userId = localStorage.getItem("user_id")
        const token = localStorage.getItem("access_token")

        if (!userId || !token) return

        disconnectSSE()

        eventSource = new EventSource(`${SSE_BASE}?channel=user_${userId}`)

        eventSource.addEventListener("notification", (event) => {
            try {
                const data = JSON.parse(event.data)
                const flashStore = useFlashStore()
                flashStore.show(data.message || "New notification", "success")

                // When export finishes, refresh Export History table (no polling needed)
                if (data.type === "export") {
                    const historyStore = useTrekHistoryStore()
                    historyStore.fetchExportJobs()
                }
            } catch (err) {
                console.error("SSE parse error:", err)
            }
        })

        eventSource.onerror = () => {
            console.warn("SSE connection error — will retry automatically")
        }
    }

    function disconnectSSE() {
        if (eventSource) {
            eventSource.close()
            eventSource = null
        }
    }

    return {
        connectSSE,
        disconnectSSE,
    }
})
