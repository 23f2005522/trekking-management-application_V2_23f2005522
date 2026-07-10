<script setup>
import { Modal } from 'bootstrap'
import { onMounted, ref } from 'vue'
import { useTrekStore } from '@/stores/admin/trekStore'
import { useStaffStore } from '@/stores/admin/staffStore'

const trekStore = useTrekStore()
const staffStore = useStaffStore()
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

onMounted(() => {
  staffStore.fetchStaffs()
})

const handleAddTrek = async (e) => {
  e.preventDefault()
  try {
    await trekStore.addTrek(fromData.value)
    const modalEl = document.getElementById('addNewTrekModal')
    if (modalEl) Modal.getOrCreateInstance(modalEl).hide()
  } catch {
    // trekStore already shows flash on failure
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
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="addNewTrekModalLabel">Add New Trek</h5>

          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body p-3">
          <form>
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
