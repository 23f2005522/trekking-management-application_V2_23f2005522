import { defineStore } from "pinia"
import { ref } from "vue"
import axiosInstance from "@/utils/axioUtil"

export const useBookingStore = defineStore("booking", () => {

    // TrekkerBookings
    // state
    const bookings = ref([])
    const loadingBookings = ref(false)
    const cancelBookingLoading = ref(false)

    // actions
    async function fetchBookings() {
        loadingBookings.value = true

        try {
            const response = await axiosInstance.get("/trekker/bookings")

            bookings.value = response.data.bookings

            return response.data
        } finally {
            loadingBookings.value = false
        }
    }

    async function cancelBooking(bookingId) {
        cancelBookingLoading.value = true

        try {
            const response = await axiosInstance.get(
                `/trekker/deletebooking/${bookingId}`
            )

            await fetchBookings()

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
