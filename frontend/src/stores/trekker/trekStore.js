import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import axiosInstance from '@/utils/axioUtil'

export const useTrekStore = defineStore("trekkerTrek", () => {
    const availableTreks = ref([])
    const filteredTreks = ref([]) // Note: Not currently used, but kept intact
    const loadingTreks = ref(false)

    const filters = ref({
        search: '',
        difficulty: '',
        location: '',
        duration: '',
    })

    const selectedTrek = ref(null)

    // : Watching local 'filters' and calling local 'fetchTreks'
    watch(
        filters,
        () => {
            fetchTreks()
        },
        { deep: true }
    )

    async function fetchTreks() {
        loadingTreks.value = true // Set loading state
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
        } catch (error) {
            console.error("Error fetching treks:", error)
        } finally {
            loadingTreks.value = false
        }
    }


    //booking State
    const bookingLoading = ref(false)


    async function bookTrek() {
        if (!selectedTrek.value) {
            throw new Error("No trek selected.")
        }

        bookingLoading.value = true

        try {
            const response = await axiosInstance.post('/trekker/booktrek', {
                trek_id: selectedTrek.value.id,
            })

            

            return response.data
        } finally {
            bookingLoading.value = false
        }
    }

    
    return {
        availableTreks,
        filteredTreks,
        loadingTreks,
        filters,
        selectedTrek,
        fetchTreks,
        bookingLoading,
        bookTrek,

    }
})