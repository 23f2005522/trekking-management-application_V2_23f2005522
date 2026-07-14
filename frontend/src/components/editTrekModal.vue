<script setup>
import { onMounted, onUnmounted } from 'vue'
import Loader from '@/components/Loader.vue'
import { useTrekStore } from '@/stores/admin/trekStore'
import { useStaffStore } from '@/stores/admin/staffStore'
import { useFlashStore } from '@/stores/flashStore'

const trekStore = useTrekStore()
const staffStore = useStaffStore()
const flashStore = useFlashStore()

onMounted(() => {
  staffStore.fetchStaffs().catch((error) => {
    flashStore.show(error.response?.data?.message || 'Failed to fetch staff.', 'error')
  })

  const modalEl = document.getElementById('editTrekModal')
  if (modalEl) {
    modalEl.addEventListener('hidden.bs.modal', onModalHidden)
  }
})

onUnmounted(() => {
  const modalEl = document.getElementById('editTrekModal')
  if (modalEl) {
    modalEl.removeEventListener('hidden.bs.modal', onModalHidden)
  }
})

function onModalHidden() {
  trekStore.clearEditingTrek()
}

const validateTrek = (trek) => {
  const start = new Date(trek.startDate)
  const end = new Date(trek.endDate)

  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
    return 'Please provide valid start and end dates.'
  }

  if (end <= start) {
    return 'Ending date must be after the starting date.'
  }

  const calculatedDuration =
    Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1

  if (Number(trek.duration) !== calculatedDuration) {
    return 'Duration must match the number of days between start and end dates.'
  }

  if (Number(trek.availableSlots) > Number(trek.totalSlots)) {
    return 'Available slots cannot be greater than total slots.'
  }

  return null
}

const handleSaveTrek = async () => {
  if (!trekStore.editingTrek) return

  const validationError = validateTrek(trekStore.editingTrek)
  if (validationError) {
    flashStore.show(validationError, 'error')
    return
  }

  try {
    const data = await trekStore.updateTrek(trekStore.editingTrek.id, trekStore.editingTrek)
    flashStore.show(data?.message || 'Trek saved successfully.', 'success')
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Error saving trek.', 'error')
  }
}
</script>

<template>
  <div>
    <div>
      <div
        id="editTrekModal"
        class="modal fade"
        tabindex="-1"
        aria-labelledby="editTrekModalLabel"
        aria-hidden="true"
        data-bs-backdrop="static"
      >
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="editTrekModalLabel">Edit Trek</h5>

              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>

            <div class="modal-body p-3">
              <div v-if="trekStore.loadingEditingTrek" class="d-flex justify-content-center py-4">
                <Loader />
              </div>
              <form v-else-if="trekStore.editingTrek">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label">Trek Name</label>
                    <input
                      v-model="trekStore.editingTrek.name"
                      type="text"
                      class="form-control"
                      placeholder="Everest Base Camp"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Location</label>
                    <input
                      v-model="trekStore.editingTrek.location"
                      type="text"
                      class="form-control"
                      placeholder="Nepal"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Difficulty</label>
                    <select v-model="trekStore.editingTrek.difficulty" class="form-select">
                      <option selected disabled>Select Difficulty</option>
                      <option value="easy">Easy</option>
                      <option value="moderate">Moderate</option>
                      <option value="difficult">Difficult</option>
                    </select>
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Duration (Days)</label>
                    <input
                      v-model="trekStore.editingTrek.duration"
                      type="number"
                      min="1"
                      class="form-control"
                      placeholder="5"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Total Slots</label>
                    <input
                      v-model="trekStore.editingTrek.totalSlots"
                      type="number"
                      min="1"
                      class="form-control"
                      placeholder="25"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Price (₹)</label>
                    <input
                      v-model="trekStore.editingTrek.price"
                      type="number"
                      step="0.01"
                      min="0"
                      class="form-control"
                      placeholder="4500"
                    />
                  </div>

                  <div class="col-12">
                    <label class="form-label">Image URL</label>
                    <input
                      v-model="trekStore.editingTrek.imageUrl"
                      type="url"
                      class="form-control"
                      placeholder="link to image"
                    />
                  </div>

                  <div class="col-12">
                    <label class="form-label">Description</label>
                    <textarea
                      v-model="trekStore.editingTrek.description"
                      class="form-control"
                      rows="4"
                      placeholder="Write a brief description about the trek..."
                    ></textarea>
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Starting Date</label>
                    <input
                      v-model="trekStore.editingTrek.startDate"
                      type="date"
                      class="form-control"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Ending Date</label>
                    <input
                      v-model="trekStore.editingTrek.endDate"
                      type="date"
                      class="form-control"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Assign Staff</label>
                    <select
                      v-model="trekStore.editingTrek.assigned_staff_id"
                      class="form-select"
                      required
                    >
                      <option value="" disabled>Select approved staff</option>
                      <option
                        v-for="staff in staffStore.approvedStaffs"
                        :key="staff.staff_id"
                        :value="staff.staff_id"
                      >
                        {{ staff.username }} (ID: {{ staff.staff_id }})
                      </option>
                    </select>
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Status</label>
                    <select v-model="trekStore.editingTrek.status" class="form-select">
                      <option value="pending">Pending</option>
                      <option value="approved">Approved</option>
                      <option value="open">Open</option>
                      <option value="ongoing">Ongoing</option>
                      <option value="closed">Closed</option>
                      <option value="completed">Completed</option>
                    </select>
                    <small class="text-muted"> Keep Pending until every detail is verified. </small>
                  </div>
                </div>
              </form>
              <div v-else class="text-center py-4 text-muted">No trek selected.</div>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>

              <button
                type="button"
                class="btn"
                :class="
                  trekStore.editingTrek?.status === 'completed' ? 'btn-secondary' : 'btn-success'
                "
                :disabled="trekStore.savingTrek || trekStore.editingTrek?.status === 'completed'"
                @click="handleSaveTrek"
              >
                <span
                  v-if="trekStore.savingTrek"
                  class="spinner-border spinner-border-sm me-1"
                ></span>
                {{ trekStore.editingTrek?.status === 'completed' ? 'Trek Completed' : 'Save Trek' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
