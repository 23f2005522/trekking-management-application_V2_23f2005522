<script setup>
import { ref } from 'vue'
import { Modal } from 'bootstrap'
import { useStaffStore } from '@/stores/admin/staffStore'
import { useFlashStore } from '@/stores/flashStore'

const staffStore = useStaffStore()
const flashStore = useFlashStore()

const formData = ref({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  experience: 0,
  address: '',
  contact_number: '',
  staff_bio: '',
})

const resetForm = () => {
  formData.value = {
    username: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    experience: 0,
    address: '',
    contact_number: '',
    staff_bio: '',
  }
}

const handleCreateStaff = async (e) => {
  e.preventDefault()

  if (formData.value.password !== formData.value.confirmPassword) {
    flashStore.show('Passwords do not match.', 'error')
    return
  }

  try {
    await staffStore.createStaff({
      username: formData.value.username,
      email: formData.value.email,
      phone: formData.value.phone,
      password: formData.value.password,
      experience: formData.value.experience,
      address: formData.value.address || undefined,
      contact_number: formData.value.contact_number || undefined,
      staff_bio: formData.value.staff_bio || undefined,
    })
    resetForm()
    const modalEl = document.getElementById('createStaffModal')
    if (modalEl) Modal.getOrCreateInstance(modalEl).hide()
  } catch {
    // flash message handled in store
  }
}
</script>

<template>
  <div
    id="createStaffModal"
    class="modal fade"
    tabindex="-1"
    aria-labelledby="createStaffModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header bg-success text-white">
          <h5 class="modal-title" id="createStaffModalLabel">Add Trek Staff</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>

        <form @submit.prevent="handleCreateStaff">
          <div class="modal-body">
            <p class="text-muted small mb-4">
              Staff accounts start as <strong>pending</strong>. Approve them before they can log in.
            </p>

            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Username</label>
                <input
                  v-model="formData.username"
                  type="text"
                  class="form-control"
                  placeholder="Staff username"
                  required
                />
              </div>

              <div class="col-md-6">
                <label class="form-label">Phone</label>
                <input
                  v-model="formData.phone"
                  type="tel"
                  class="form-control"
                  placeholder="Phone number"
                  required
                />
              </div>

              <div class="col-12">
                <label class="form-label">Email</label>
                <input
                  v-model="formData.email"
                  type="email"
                  class="form-control"
                  placeholder="Email address"
                  required
                />
              </div>

              <div class="col-md-6">
                <label class="form-label">Password</label>
                <input
                  v-model="formData.password"
                  type="password"
                  class="form-control"
                  placeholder="Temporary password"
                  required
                />
              </div>

              <div class="col-md-6">
                <label class="form-label">Confirm Password</label>
                <input
                  v-model="formData.confirmPassword"
                  type="password"
                  class="form-control"
                  placeholder="Re-enter password"
                  required
                />
              </div>

              <div
                v-if="formData.password && formData.confirmPassword && formData.password !== formData.confirmPassword"
                class="col-12"
              >
                <div class="alert alert-danger py-2 mb-0">Passwords do not match.</div>
              </div>

              <div class="col-md-4">
                <label class="form-label">Experience (years)</label>
                <input
                  v-model.number="formData.experience"
                  type="number"
                  min="0"
                  class="form-control"
                />
              </div>

              <div class="col-md-8">
                <label class="form-label">Contact Number</label>
                <input
                  v-model="formData.contact_number"
                  type="tel"
                  class="form-control"
                  placeholder="Optional alternate contact"
                />
              </div>

              <div class="col-12">
                <label class="form-label">Address</label>
                <input
                  v-model="formData.address"
                  type="text"
                  class="form-control"
                  placeholder="Optional address"
                />
              </div>

              <div class="col-12">
                <label class="form-label">Bio</label>
                <textarea
                  v-model="formData.staff_bio"
                  rows="3"
                  class="form-control"
                  placeholder="Optional staff bio"
                ></textarea>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button
              type="submit"
              class="btn btn-success"
              :disabled="formData.password !== formData.confirmPassword"
            >
              Create Staff
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
