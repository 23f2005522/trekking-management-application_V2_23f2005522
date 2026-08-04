import { defineStore } from "pinia"
import { ref } from "vue"
import axiosInstance from "@/utils/axioUtil"
import { useUserNotificationStore } from "@/stores/userNotificationStore"
import { useTrekkerStore } from "@/stores/trekker/trekkerStore"

export const useBookingStore = defineStore("booking", () => {

    // TrekkerBookings
    // state
    const bookings = ref([])
    const loadingBookings = ref(false)
    const cancelBookingLoading = ref(false)

    // actions
    async function fetchBookings(silent = false) {
        if (!silent) {
            loadingBookings.value = true
        }

        try {
            const response = await axiosInstance.get("/trekker/bookings")

            bookings.value = response.data.bookings

            return response.data
        } finally {
            if (!silent) {
                loadingBookings.value = false
            }
        }
    }

    async function cancelBooking(bookingId) {
        cancelBookingLoading.value = true

        try {
            const response = await axiosInstance.get(
                `/trekker/deletebooking/${bookingId}`
            )

            await fetchBookings(true)

            const userNotificationStore = useUserNotificationStore()
            const trekkerStore = useTrekkerStore()
            await Promise.all([
                userNotificationStore.fetchNotifications({ silent: true }),
                trekkerStore.fetchDashboardData(true),
            ])

            return response.data
        } finally {
            cancelBookingLoading.value = false
        }
    }

    return {
        bookings,
        loadingBookings,
        cancelBookingLoading,

        fetchBookings,
        cancelBooking,
    }
})
