<script setup>
import { computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import Loader from '@/components/Loader.vue'
import { userStaffStore } from '@/stores/staff/staffStore'

const staffStore = userStaffStore()
const { staffProfile, loadingProfile } = storeToRefs(staffStore)

const profileStatusLabel = computed(() => {
  const status = staffProfile.value?.profile_status
  if (!status) return '-'
  return status.charAt(0).toUpperCase() + status.slice(1)
})

const profileStatusClass = computed(() => {
  const status = staffProfile.value?.profile_status

  const statusClassMap = {
    approved: 'bg-success',
    pending: 'bg-warning text-dark',
    rejected: 'bg-danger',
    blacklisted: 'bg-dark',
  }

  return statusClassMap[status] || 'bg-secondary'
})

onMounted(async () => {
  try {
    await staffStore.fetchProfile()
  } catch {
    // staffStore already shows flash on failure
  }
})
</script>

<template>
  <div>
    <h2 class="fw-bold mb-4">My Profile</h2>

    <div v-if="loadingProfile" class="text-center py-5">
      <Loader />
    </div>

    <div v-else-if="staffProfile" class="card shadow-sm">
      <div class="card-body">
        <div class="text-center mb-4">
          <div
            class="rounded-circle bg-success text-white d-inline-flex align-items-center justify-content-center"
            style="width: 90px; height: 90px; font-size: 2rem"
          >
            <i class="bi bi-person-fill"></i>
          </div>

          <h4 class="mt-3 mb-1">{{ staffProfile.username }}</h4>

          <span class="badge bg-success text-uppercase">Staff</span>
        </div>

        <div class="alert alert-light border mb-4" role="alert">
          <i class="bi bi-info-circle me-2 text-success"></i>
          This page is <strong>view-only</strong>. Profile updates are managed by the admin.
        </div>

        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label">Username</label>
            <input :value="staffProfile.username" class="form-control" type="text" disabled />
          </div>

          <div class="col-md-6">
            <label class="form-label">Email</label>
            <input :value="staffProfile.email" class="form-control" type="email" disabled />
          </div>

          <div class="col-md-6">
            <label class="form-label">Phone Number</label>
            <input :value="staffProfile.phone" class="form-control" type="text" disabled />
          </div>

          <div class="col-md-6">
            <label class="form-label">Role</label>
            <input :value="staffProfile.role" class="form-control text-capitalize" disabled />
          </div>

          <div class="col-md-6">
            <label class="form-label">Profile Status</label>
            <div class="input-group">
              <input :value="profileStatusLabel" class="form-control" disabled />
              <span :class="['badge d-flex align-items-center px-3', profileStatusClass]">
                {{ profileStatusLabel }}
              </span>
            </div>
          </div>

          <div class="col-md-6">
            <label class="form-label">Experience (Years)</label>
            <input :value="staffProfile.experience" class="form-control" type="text" disabled />
          </div>

          <div class="col-md-6">
            <label class="form-label">Joining Date</label>
            <input :value="staffProfile.joining_date" class="form-control" type="text" disabled />
          </div>

          <div class="col-md-6">
            <label class="form-label">Address</label>
            <input :value="staffProfile.address" class="form-control" type="text" disabled />
          </div>

          <div class="col-12">
            <label class="form-label">Bio</label>
            <textarea class="form-control" rows="3" disabled>{{ staffProfile.bio }}</textarea>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
