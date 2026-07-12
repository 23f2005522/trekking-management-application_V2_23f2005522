<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useTrekStore } from '@/stores/admin/trekStore'
import { useStaffStore } from '@/stores/admin/staffStore'
import { useFlashStore } from '@/stores/flashStore'

const trekStore = useTrekStore()
const staffStore = useStaffStore()
const flashStore = useFlashStore()
const fromData = ref({
  name: '',
  location: '',
  difficulty: '',
  duration: '',
  totalSlots: '',
  price: '',
  imageUrl: '',
  description: '',
  startDate: '',
  endDate: '',
  assignedStaffId: '',
})

const resetForm = () => {
  fromData.value = {
    name: '',
    location: '',
    difficulty: '',
    duration: '',
    totalSlots: '',
    price: '',
    imageUrl: '',
    description: '',
    startDate: '',
    endDate: '',
    assignedStaffId: '',
  }
}

onMounted(() => {
  staffStore.fetchStaffs().catch((error) => {
    flashStore.show(error.response?.data?.message || 'Failed to fetch staff.', 'error')
  })

  const modalEl = document.getElementById('addNewTrekModal')
  if (modalEl) {
    modalEl.addEventListener('hidden.bs.modal', resetForm)
  }
})

onUnmounted(() => {
  const modalEl = document.getElementById('addNewTrekModal')
  if (modalEl) {
    modalEl.removeEventListener('hidden.bs.modal', resetForm)
  }
})

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

  return null
}

const handleAddTrek = async () => {
  const validationError = validateTrek(fromData.value)
  if (validationError) {
    flashStore.show(validationError, 'error')
    return
  }

  try {
    const data = await trekStore.addTrek(fromData.value)
    flashStore.show(data?.message || 'Trek added successfully.', 'success')
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to add trek.', 'error')
  }
}
</script>

<template>
  <div
    id="addNewTrekModal"
    class="modal fade"
    tabindex="-1"
    aria-labelledby="addNewTrekModalLabel"
    aria-hidden="true"
    data-bs-backdrop="static"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="addNewTrekModalLabel">Add New Trek</h5>

          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body p-3">
          <form @submit.prevent="handleAddTrek">
            <div class="row g-3">
              <!-- Trek Name -->
              <div class="col-md-6">
                <label class="form-label">Trek Name</label>

                <input
                  v-model="fromData.name"
                  type="text"
                  class="form-control"
                  placeholder="Everest Base Camp"
                />
              </div>

              <!-- Location -->
              <div class="col-md-6">
                <label class="form-label">Location</label>

                <input
                  v-model="fromData.location"
                  type="text"
                  class="form-control"
                  placeholder="Nepal"
                />
              </div>

              <!-- Difficulty -->
              <div class="col-md-6">
                <label class="form-label">Difficulty</label>

                <select v-model="fromData.difficulty" class="form-select">
                  <option selected disabled>Select Difficulty</option>

                  <option value="easy">Easy</option>

                  <option value="moderate">Moderate</option>

                  <option value="difficult">Difficult</option>
                </select>
              </div>

              <!-- Duration -->
              <div class="col-md-6">
                <label class="form-label">Duration (Days)</label>

                <input
                  v-model="fromData.duration"
                  type="number"
                  min="1"
                  class="form-control"
                  placeholder="5"
                />
              </div>

              <!-- Total Slots -->
              <div class="col-md-6">
                <label class="form-label">Total Slots</label>

                <input
                  v-model="fromData.totalSlots"
                  type="number"
                  min="1"
                  class="form-control"
                  placeholder="25"
                />
              </div>

              <!-- Price -->
              <div class="col-md-6">
                <label class="form-label">Price (₹)</label>

                <input
                  v-model="fromData.price"
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-control"
                  placeholder="4500"
                />
              </div>

              <!-- Image URL -->
              <div class="col-12">
                <label class="form-label">Image URL</label>

                <input
                  v-model="fromData.imageUrl"
                  type="url"
                  class="form-control"
                  placeholder="https://example.com/image.jpg"
                />
              </div>

              <!-- Description -->
              <div class="col-12">
                <label class="form-label">Description</label>

                <textarea
                  v-model="fromData.description"
                  class="form-control"
                  rows="4"
                  placeholder="Write a brief description about the trek..."
                ></textarea>
              </div>

              <!-- Start Date -->
              <div class="col-md-6">
                <label class="form-label">Starting Date</label>

                <input v-model="fromData.startDate" type="date" class="form-control" />
              </div>

              <!-- End Date -->
              <div class="col-md-6">
                <label class="form-label">Ending Date</label>

                <input v-model="fromData.endDate" type="date" class="form-control" />
              </div>

              <!-- Assigned Staff -->
              <div class="col-md-6">
                <label class="form-label">Assign Staff</label>

                <select v-model="fromData.assignedStaffId" class="form-select" required>
                  <option value="" disabled>Select approved staff</option>
                  <option
                    v-for="staff in staffStore.approvedStaffs"
                    :key="staff.staff_id"
                    :value="staff.staff_id"
                  >
                    {{ staff.username }} (ID: {{ staff.staff_id }})
                  </option>
                </select>
                <small v-if="staffStore.approvedStaffs.length === 0" class="text-muted">
                  No approved staff available. Approve a staff account first.
                </small>
              </div>
            </div>
          </form>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>

          <button type="button" class="btn btn-success" @click="handleAddTrek">Save Trek</button>
        </div>
      </div>
    </div>
  </div>
</template>
