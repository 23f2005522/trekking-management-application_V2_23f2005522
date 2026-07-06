<script setup>
import { onMounted, onUnmounted, watch } from 'vue'
import { useTrekStore } from '@/stores/admin/trekStore'
import { hideBootstrapModal, registerModalCleanup } from '@/utils/bootstrapModal'

const props = defineProps({
  trekId: {
    type: [String, Number, null],
    required: true,
    default: null,
  },
})

const trekStore = useTrekStore()
let cleanupModal = () => {}

onMounted(() => {
  cleanupModal = registerModalCleanup('editTrekModal')
})

onUnmounted(() => {
  cleanupModal()
})

const handleSaveTrek = async () => {
  if (!trekStore.editingTrek) return

  await trekStore.updateTrek(trekStore.editingTrek.id, trekStore.editingTrek)
  hideBootstrapModal('editTrekModal')
}

//selectedTrekIdAndFire
watch(
  () => props.trekId,
  async (id) => {
    if (!id) return
    await trekStore.fetchTrekById(id)
  },
  { immediate: true },
)
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
      >
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="editTrekModalLabel">Edit Trek</h5>

              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>

            <div class="modal-body p-3">
              <div v-if="!trekStore.editingTrek">Loading...</div>
              <form v-else>
                <div class="row g-3">
                  <!-- Trek Name -->
                  <div class="col-md-6">
                    <label class="form-label">Trek Name</label>

                    <input
                      v-model="trekStore.editingTrek.name"
                      type="text"
                      class="form-control"
                      placeholder="Everest Base Camp"
                    />
                  </div>

                  <!-- Location -->
                  <div class="col-md-6">
                    <label class="form-label">Location</label>

                    <input
                      v-model="trekStore.editingTrek.location"
                      type="text"
                      class="form-control"
                      placeholder="Nepal"
                    />
                  </div>

                  <!-- Difficulty -->
                  <div class="col-md-6">
                    <label class="form-label">Difficulty</label>

                    <select v-model="trekStore.editingTrek.difficulty" class="form-select">
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
                      v-model="trekStore.editingTrek.duration"
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
                      v-model="trekStore.editingTrek.totalSlots"
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
                      v-model="trekStore.editingTrek.price"
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
                      v-model="trekStore.editingTrek.image_url"
                      type="url"
                      class="form-control"
                      placeholder="link to image"
                    />
                  </div>

                  <!-- Description -->
                  <div class="col-12">
                    <label class="form-label">Description</label>

                    <textarea
                      v-model="trekStore.editingTrek.description"
                      class="form-control"
                      rows="4"
                      placeholder="Write a brief description about the trek..."
                    ></textarea>
                  </div>

                  <!-- Start Date -->
                  <div class="col-md-6">
                    <label class="form-label">Starting Date</label>

                    <input
                      v-model="trekStore.editingTrek.starting_at"
                      type="date"
                      class="form-control"
                    />
                  </div>

                  <!-- End Date -->
                  <div class="col-md-6">
                    <label class="form-label">Ending Date</label>

                    <input
                      v-model="trekStore.editingTrek.ending_at"
                      type="date"
                      class="form-control"
                    />
                  </div>

                  <!-- Assigned Staff -->
                  <div class="col-md-6">
                    <label class="form-label">Assign Staff ID</label>

                    <input
                      v-model="trekStore.editingTrek.assigned_staff_id"
                      type="text"
                      placeholder="Staff Id"
                      class="form-control"
                    />
                  </div>

                  <!-- Status -->
                  <div class="col-md-6">
                    <label class="form-label">Status</label>

                    <select v-model="trekStore.editingTrek.status" class="form-select">
                      <option value="pending">Pending</option>
                      <option value="approved">Approved</option>
                    </select>

                    <small class="text-muted"> Keep Pending until every detail is verified. </small>
                  </div>


                </div>
              </form>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>

              <button
                type="button"
                class="btn btn-success"
                @click="handleSaveTrek"
              >
                <span
                  v-if="trekStore.savingTrek"
                  class="spinner-border spinner-border-sm me-1"
                ></span>
                Save Trek
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
