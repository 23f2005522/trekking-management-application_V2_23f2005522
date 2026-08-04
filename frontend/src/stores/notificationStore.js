import { defineStore } from "pinia"
import { useFlashStore } from "@/stores/flashStore"
import { useAdminStore } from "@/stores/admin/adminStore"
import { useTrekStore as useAdminTrekStore } from "@/stores/admin/trekStore"
import { userStaffStore } from "@/stores/staff/staffStore"
import { useTrekkerStore } from "@/stores/trekker/trekkerStore"
import { useTrekStore } from "@/stores/trekker/trekStore"
import { useBookingStore } from "@/stores/trekker/bookingStore"
import { useTrekHistoryStore } from "@/stores/trekker/trekHistoryStore"
import { useUserNotificationStore } from "@/stores/userNotificationStore"
import { useBookingStore as useAdminBookingStore } from "@/stores/admin/bookingStore"

const SSE_BASE = "http://127.0.0.1:5000/stream"

async function refreshStoresForNotification(data) {
    const role = localStorage.getItem("role")
    const action = data.action || data.type

    if (role === "staff") {
        const staffStore = userStaffStore()

        if (
            action === "staff_trek_assigned" ||
            action === "staff_trek_reassigned" ||
            action === "staff_deactivated" ||
            action === "staff_reactivated" ||
            action === "reminder"
        ) {
            await staffStore.refreshAssignedData()
        }
        return
    }

    if (role === "trekker") {
        const trekkerStore = useTrekkerStore()
        const trekStore = useTrekStore()
        const bookingStore = useBookingStore()
        const historyStore = useTrekHistoryStore()

        if (action === "export" || action === "export_failed") {
            await historyStore.fetchExportJobs()
            return
        }

        if (
            action === "reminder" ||
            action === "booking" ||
            action === "trekker_booking" ||
            action === "trekker_booking_cancel"
        ) {
            await Promise.all([
                trekkerStore.fetchDashboardData(true),
                trekStore.fetchTreks(true),
                bookingStore.fetchBookings(true),
            ])
        }
        return
    }

    if (role === "admin") {
        const adminStore = useAdminStore()
        const adminTrekStore = useAdminTrekStore()
        const adminBookingStore = useAdminBookingStore()

        if (action === "export" || action === "export_failed") {
            await Promise.all([
                adminBookingStore.fetchExportJobs(),
                adminStore.fetchAdminData(true),
            ])
            return
        }

        if (action === "report") {
            await Promise.all([
                adminStore.fetchAdminData(true),
                adminStore.fetchReport(),
            ])
            return
        }

        if (action === "reminder" || action === "booking") {
            await Promise.all([
                adminStore.fetchAdminData(true),
                adminTrekStore.fetchTreks(true),
            ])
        }
    }
}

export const useNotificationStore = defineStore("notifications", () => {
    let eventSource = null

    function connectSSE() {
        const userId = localStorage.getItem("user_id")
        const token = localStorage.getItem("access_token")

        if (!userId || !token) return

        disconnectSSE()

        const userNotificationStore = useUserNotificationStore()
        userNotificationStore.fetchNotifications({ silent: true })

        eventSource = new EventSource(`${SSE_BASE}?channel=user_${userId}`)

        eventSource.addEventListener("notification", async (event) => {
            try {
                const data = JSON.parse(event.data)
                const flashStore = useFlashStore()
                if (!data.skip_toast) {
                    const toastType = data.action === "export_failed" ? "error" : "success"
                    flashStore.show(data.message || "New notification", toastType)
                }

                const userNotificationStore = useUserNotificationStore()
                await userNotificationStore.fetchNotifications({ silent: true })
                await refreshStoresForNotification(data)
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
        refreshStoresForNotification,
    }
})
