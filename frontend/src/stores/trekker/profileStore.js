import { defineStore } from "pinia"
import { ref } from "vue"
import axiosInstance from "@/utils/axioUtil"

export const useProfileStore = defineStore("trekkerProfile", () => {

    // TrekkerProfile
    // state
    const profile = ref(null)
    const loadingProfile = ref(false)
    const updatingProfile = ref(false)

    // actions
    async function fetchProfile() {
        loadingProfile.value = true

        try {
            const response = await axiosInstance.get("/trekker/profile")

            profile.value = response.data.trekker_profile

            return response.data
        } finally {
            loadingProfile.value = false
        }
    }

    async function updateProfile() {
        updatingProfile.value = true

        try {
            const response = await axiosInstance.post(
                "/trekker/profile",
                {
                    username: profile.value.username,
                    email: profile.value.email,
                    phone: profile.value.phone,
                }
            )

            profile.value = response.data.trekker_profile

            return response.data
        } finally {
            updatingProfile.value = false
        }
    }

    return {
        profile,
        loadingProfile,
        updatingProfile,

        fetchProfile,
        updateProfile,
    }
})
