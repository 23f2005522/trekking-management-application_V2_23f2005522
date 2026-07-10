<script setup>
import { computed, ref, watch } from 'vue'
import { Modal } from 'bootstrap'
import { storeToRefs } from 'pinia'
import { userStaffStore } from '@/stores/staff/staffStore'

const emit = defineEmits(['updated'])

const props = defineProps({
  trekId: {
    type: [Number, String],
    default: null,
  },
  modalId: {
    type: String,
    default: 'staffManageTrekModal',
  },
})

const staffStore = userStaffStore()
const { managingTrek, loadingManagingTrek, savingTrekStatus } = storeToRefs(staffStore)

const selectedStatus = ref('open')

const trek = computed(() => managingTrek.value)
const loadingTrek = computed(() => loadingManagingTrek.value)
const savingStatus = computed(() => savingTrekStatus.value)

const canMarkCompleted = computed(() => trek.value?.status === 'ongoing')

const getStatusBadgeClass = (status) => {
  const normalizedStatus = String(status || '').toLowerCase()

  const statusClassMap = {
    open: 'bg-success',
    pending: 'bg-danger',
    ongoing: 'bg-warning text-dark',
    closed: 'bg-secondary',
    completed: 'bg-primary',
    approved: 'bg-info text-dark',
  }

  return statusClassMap[normalizedStatus] || 'bg-secondary'
}

watch(
  () => props.trekId,
  async (trekId) => {
    if (!trekId) {
      await staffStore.fetchTrekById(null)
      selectedStatus.value = 'open'
      return
    }

    try {
      const loadedTrek = await staffStore.fetchTrekById(trekId)
      selectedStatus.value = loadedTrek?.status || 'open'
    } catch {
      selectedStatus.value = 'open'
    }
  },
  { immediate: true }
)

const saveTrekStatus = async () => {
  if (!props.trekId) return

  try {
    const updatedTrek = await staffStore.updateTrekStatus(props.trekId, selectedStatus.value)
    selectedStatus.value = updatedTrek?.status || selectedStatus.value
    emit('updated', updatedTrek)
    const modalEl = document.getElementById(props.modalId)
    if (modalEl) Modal.getOrCreateInstance(modalEl).hide()
  } catch {
    // staffStore already shows flash on failure
  }
}
</script>

<template>
  <div class="modal fade" :id="modalId" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content staff-modal">
        <div class="modal-header staff-modal-header">
          <div>
            <h5 class="modal-title fw-semibold mb-1">
              Manage Trek
            </h5>

            <small class="text-white-50">
              Preview trek details and current assignment state
            </small>
          </div>

          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <div class="modal-body p-4" v-if="trek">
          <div class="row g-4">
            <div class="col-md-7">
              <div class="detail-card mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <div class="detail-label mb-0">Trek Name</div>
                  <span :class="['badge text-uppercase', getStatusBadgeClass(selectedStatus)]">
                    {{ selectedStatus }}
                  </span>
                </div>
                <div class="detail-value">{{ trek.name }}</div>
              </div>

              <div class="detail-card mb-3">
                <div class="detail-label">Location</div>
                <div class="detail-value">{{ trek.location }}</div>
              </div>

              <div class="detail-card mb-3">
                <div class="detail-label">Difficulty</div>
                <div class="detail-value text-capitalize">{{ trek.difficulty }}</div>
              </div>
            </div>

            <div class="col-md-5">
              <div class="detail-card mb-3">
                <div class="detail-label">Duration</div>
                <div class="detail-value">{{ trek.duration }} Days</div>
              </div>

              <div class="detail-card mb-3">
                <div class="detail-label">Start Date</div>
                <div class="detail-value">{{ trek.starting_date }}</div>
              </div>

              <div class="detail-card mb-3">
                <div class="detail-label">End Date</div>
                <div class="detail-value">{{ trek.ending_date }}</div>
              </div>
            </div>
          </div>

          <div class="stats-strip mt-4">
            <div class="stat-box">
              <span class="stat-label">Total Slots</span>
              <span class="stat-value text-primary">{{ trek.total_slots }}</span>
            </div>

            <div class="stat-box">
              <span class="stat-label">Available Slots</span>
              <span class="stat-value text-success">{{ trek.available_slots }}</span>
            </div>

            <div class="stat-box">
              <span class="stat-label">Booked</span>
              <span class="stat-value text-danger">{{ trek.total_participants }}</span>
            </div>
          </div>

          <div class="mt-4 pt-3 border-top">
            <label class="form-label fw-semibold mb-2">Trek Status</label>
            <select v-model="selectedStatus" class="form-select form-select-lg status-select">
              <option value="open">Open</option>
              <option value="ongoing">Ongoing</option>
              <option value="closed">Closed</option>
              <option value="completed" :disabled="!canMarkCompleted">Completed</option>
            </select>
            <small v-if="!canMarkCompleted" class="text-muted">
              Mark trek as ongoing before completing it.
            </small>
          </div>
        </div>

        <div v-else-if="loadingTrek" class="modal-body text-center py-5">
          Loading trek details...
        </div>

        <div v-else class="modal-body text-center py-5 text-muted">
          Select a trek to view details.
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            Close
          </button>

          <button type="button" class="btn btn-success" :disabled="savingStatus" @click="saveTrekStatus">
            {{ savingStatus ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.staff-modal {
  border: 0;
  border-radius: 18px;
  overflow: hidden;
}

.staff-modal-header {
  background: linear-gradient(135deg, #198754, #146c43);
  color: #fff;
  padding: 1.1rem 1.25rem;
}

.detail-card {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  padding: 0.85rem 1rem;
}

.detail-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #6c757d;
  margin-bottom: 0.3rem;
}

.detail-value {
  font-size: 1rem;
  font-weight: 500;
  color: #212529;
}

.stats-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.stat-box {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  padding: 0.9rem 1rem;
}

.stat-label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #6c757d;
  margin-bottom: 0.35rem;
}

.stat-value {
  display: block;
  font-size: 1.4rem;
  font-weight: 700;
  line-height: 1;
}

.status-select {
  border-color: #ced4da;
}

.status-select:focus {
  border-color: #198754;
  box-shadow: 0 0 0 0.2rem rgba(25, 135, 84, 0.15);
}

@media (max-width: 767.98px) {
  .stats-strip {
    grid-template-columns: 1fr;
  }
}
</style>
