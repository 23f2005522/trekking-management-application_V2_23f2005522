import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import axiosInstance from '@/utils/axioUtil'

export const useTrekStore = defineStore("trekkerTrek", () => {
    const availableTreks = ref([])
    const filteredTreks = ref([])
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

    const selectedTrek = ref(null)

    let fetchTimeout = null

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

    async function fetchTreks() {
        loadingTreks.value = true
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
            loadingTreks.value = false
        }
    }


    const bookingTrekLoading = ref(false)

    async function bookTrek() {
        if (!selectedTrek.value) {
            throw new Error("No trek selected.")
        }

        bookingTrekLoading.value = true
        try {
            const response = await axiosInstance.post('/trekker/booktrek', {
            trek_id: selectedTrek.value.id,
            })

            return response.data
        } finally {
            bookingTrekLoading.value = false
        }
    }

    
    return {
        availableTreks,
        filteredTreks,
        loadingTreks,       
        filters,
        filterOptions,
        selectedTrek,
        fetchTreks,
        bookingTrekLoading,
        bookTrek,

    }
})
