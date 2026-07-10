<script setup>
import { onMounted } from 'vue'
import Loader from '@/components/Loader.vue'
import { useFlashStore } from '@/stores/flashStore'
import { useProfileStore } from '@/stores/trekker/profileStore'

const profileStore = useProfileStore()
const flashStore = useFlashStore()

onMounted(async () => {
  try {
    await profileStore.fetchProfile()
  } catch (error) {
    flashStore.show(
      error.response?.data?.message || 'Failed to fetch profile.',
      'danger'
    )
  }
})

const handleUpdateProfile = async () => {
  try {
    await profileStore.updateProfile()
    flashStore.show('Profile updated successfully.', 'success')
  } catch (error) {
    flashStore.show(
      error.response?.data?.message || 'Failed to update profile.',
      'danger'
    )
  }
}

</script>

<template>
  <div>
    <h2 class="fw-bold mb-4">
      My Profile
    </h2>

    <div
      v-if="profileStore.loadingProfile"
      class="text-center py-5"
    >
      <Loader />
    </div>

    <div
      v-else-if="profileStore.profile"
      class="card shadow-sm"
    >
      <div class="card-body">

        <div class="text-center mb-4">

          <div
            class="rounded-circle bg-success text-white d-inline-flex align-items-center justify-content-center"
            style="width:90px;height:90px;font-size:2rem"
          >
            <i class="bi bi-person-fill"></i>
          </div>

          <h4 class="mt-3 mb-1">
            {{ profileStore.profile.username }}
          </h4>

          <span class="badge bg-success text-uppercase">
            {{ profileStore.profile.role }}
          </span>

        </div>

        <div class="row g-3">

          <div class="col-md-6">
            <label class="form-label">
              Username
            </label>

            <input
              v-model="profileStore.profile.username"
              class="form-control"
              type="text"
            />
          </div>

          <div class="col-md-6">
            <label class="form-label">
              Email
            </label>

            <input
              v-model="profileStore.profile.email"
              class="form-control"
              type="email"
            />
          </div>

          <div class="col-md-6">
            <label class="form-label">
              Phone Number
            </label>

            <input
              v-model="profileStore.profile.phone"
              class="form-control"
              type="text"
            />
          </div>

          <div class="col-md-6">
            <label class="form-label">
              Role
            </label>

            <input
              :value="profileStore.profile.role"
              class="form-control"
              disabled
            />
          </div>

          <div class="col-md-6">
            <label class="form-label">
              Account Status
            </label>

            <input
              :value="profileStore.profile.is_active ? 'Active' : 'Inactive'"
              class="form-control"
              disabled
            />
          </div>

          <div class="col-md-6">
            <label class="form-label">
              Blacklisted
            </label>

            <input
              :value="profileStore.profile.is_blacklisted ? 'Yes' : 'No'"
              class="form-control"
              disabled
            />
          </div>

          <div
            v-if="profileStore.profile.is_blacklisted"
            class="col-12"
          >
            <label class="form-label">
              Blacklist Reason
            </label>

            <textarea
              class="form-control"
              rows="3"
              disabled
            >{{ profileStore.profile.blacklisted_reason }}</textarea>
          </div>

        </div>

        <hr>

        <div class="d-flex justify-content-end">

          <button
            class="btn btn-success"
            :disabled="profileStore.updatingProfile"
            @click="handleUpdateProfile"
          >
            <i class="bi bi-pencil-square me-2"></i>

            {{ profileStore.updatingProfile ? 'Updating...' : 'Update Profile' }}
          </button>

        </div>

      </div>
    </div>
  </div>
</template>