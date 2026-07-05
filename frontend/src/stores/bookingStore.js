import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { useFlashStore } from "./flashStore";
import axiosInstance from "@/utils/axioUtil";

export const useBookingStore = defineStore("Booking", () => {

    const flashStore = useFlashStore();

    // State variables
    const allBookings = ref([]);
    const loadingBookings = ref(false);
    const bookingSearchQuery = ref("");

    // Getters
    const filteredBookings = computed(() => {
        const query = bookingSearchQuery.value.trim().toLowerCase();
        if (!query) return allBookings.value;

        return allBookings.value.filter((booking) => {
            return (
                booking.username.toLowerCase().includes(query) ||
                booking.user_email.toLowerCase().includes(query) ||
                booking.trek_name.toLowerCase().includes(query) ||
                booking.status.toLowerCase().includes(query) ||
                booking.payment_status.toLowerCase().includes(query) ||
                booking.id == String(query)
            );
        });
    });

    // Actions
    async function fetchAllBookings() {
        loadingBookings.value = true;
        try {
            const { data } = await axiosInstance.get("/admin/bookings");
            allBookings.value = data.bookings;
        } catch (error) {
            flashStore.show(error.response?.data?.message || "Failed to fetch bookings.", "error");
            console.error("Error fetching bookings:", error);
        } finally {
            loadingBookings.value = false;
        }
    }

    return {
        // State
        allBookings,
        loadingBookings,
        bookingSearchQuery,

        // Getters
        filteredBookings,

        // Actions
        fetchAllBookings,
    };
});