import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import axiosInstance from '@/utils/axioUtil'
import { useUserNotificationStore } from '@/stores/userNotificationStore'
import { useBookingStore } from '@/stores/trekker/bookingStore'
import { useTrekkerStore } from '@/stores/trekker/trekkerStore'

export const useTrekStore = defineStore("trekkerTrek", () => {

    // TrekkerTreks
    // state
    const availableTreks = ref([])
    const loadingTreks = ref(false)
    const filters = ref({
        search: '',
        difficulty: '',
        location: '',
        duration: '',
    })
    const filterOptions = ref({
        locations: [],
        durations: [],
        difficulties: ['easy', 'moderate', 'difficult'],
    })

    let fetchTimeout = null

    // actions
    function scheduleFetchTreks(delay = 0) {
        if (fetchTimeout) {
            clearTimeout(fetchTimeout)
        }

        fetchTimeout = setTimeout(() => {
            fetchTreks()
        }, delay)
    }

    watch(
        () => filters.value.difficulty,
        () => scheduleFetchTreks()
    )

    watch(
        () => filters.value.location,
        () => scheduleFetchTreks()
    )

    watch(
        () => filters.value.duration,
        () => scheduleFetchTreks()
    )

    watch(
        () => filters.value.search,
        () => scheduleFetchTreks(400)
    )

    async function fetchTreks(silent = false) {
        if (!silent) {
            loadingTreks.value = true
        }
        try {
            const params = {}

            if (filters.value.search) params.search = filters.value.search
            if (filters.value.location) params.location = filters.value.location
            if (filters.value.difficulty) params.difficulty = filters.value.difficulty
            if (filters.value.duration) params.duration = filters.value.duration

            const response = await axiosInstance.get('/trekker/treks', {
                params: params
            })
            availableTreks.value = response.data.treks

            if (response.data.filter_options) {
                filterOptions.value = response.data.filter_options
            }
        } catch (error) {
            console.error("Error fetching treks:", error)
        } finally {
            if (!silent) {
                loadingTreks.value = false
            }
        }
    }

    // BookingModal
    // state
    const selectedTrek = ref(null)
    const bookingTrekLoading = ref(false)

    // actions
    async function bookTrek() {
        if (!selectedTrek.value) {
            throw new Error("No trek selected.")
        }

        bookingTrekLoading.value = true
        try {
            const response = await axiosInstance.post('/trekker/booktrek', {
                trek_id: selectedTrek.value.id,
            })

            const userNotificationStore = useUserNotificationStore()
            const bookingStore = useBookingStore()
            const trekkerStore = useTrekkerStore()

            await Promise.all([
                userNotificationStore.fetchNotifications({ silent: true }),
                bookingStore.fetchBookings(true),
                trekkerStore.fetchDashboardData(true),
            ])

            return response.data
        } finally {
            bookingTrekLoading.value = false
        }
    }

    return {
        availableTreks,
        loadingTreks,
        filters,
        filterOptions,
        selectedTrek,
        fetchTreks,
        bookingTrekLoading,
        bookTrek,
    }
})
