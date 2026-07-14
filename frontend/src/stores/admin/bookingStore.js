import { defineStore } from "pinia";
import { computed, ref } from "vue";
import axiosInstance from "@/utils/axioUtil";

export const useBookingStore = defineStore("Booking", () => {

    // manageBookings
    // state
    const allBookings = ref([]);
    const loadingBookings = ref(false);
    const bookingSearchQuery = ref("");

    // getters
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

    // actions
    async function fetchAllBookings() {
        loadingBookings.value = true;
        try {
            const { data } = await axiosInstance.get("/admin/bookings");
            allBookings.value = data.bookings;
            return data;
        } finally {
            loadingBookings.value = false;
        }
    }

    return {
        allBookings,
        loadingBookings,
        bookingSearchQuery,

        filteredBookings,

        fetchAllBookings,
    };
});
