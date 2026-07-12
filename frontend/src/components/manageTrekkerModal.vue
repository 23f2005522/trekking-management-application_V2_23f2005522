<script setup>
import { ref, watch } from 'vue'
import { userTrekkerStore } from '@/stores/admin/trekkerStore'
import { useFlashStore } from '@/stores/flashStore'

const trekkerStore = userTrekkerStore()
const flashStore = useFlashStore()

const selectedStatus = ref('reactivate')
const reason = ref('')

const setDefaultAction = (trekker) => {
  if (!trekker) {
    selectedStatus.value = 'reactivate'
    reason.value = ''
    return
  }

  if (trekker.is_blacklisted) {
    selectedStatus.value = 'deblacklist'
  } else if (!trekker.is_active) {
    selectedStatus.value = 'reactivate'
  } else {
    selectedStatus.value = 'deactivate'
  }

  reason.value = trekker.blacklisted_reason || ''
}

watch(
  () => trekkerStore.selectedTrekker,
  (trekker) => setDefaultAction(trekker),
  { immediate: true }
)

const getStatusLabel = (trekker) => {
  if (trekker.is_blacklisted) return 'Blacklisted'
  if (!trekker.is_active) return 'Deactivated'
  return 'Active'
}

const getStatusBadgeClass = (trekker) => {
  if (trekker.is_blacklisted) return 'bg-dark'
  if (!trekker.is_active) return 'bg-secondary'
  return 'bg-success'
}

const handleSave = async () => {
  const trekker = trekkerStore.selectedTrekker
  if (!trekker) return

  if (
    trekker.is_blacklisted &&
    (selectedStatus.value === 'reactivate' || selectedStatus.value === 'deactivate')
  ) {
    flashStore.show(
      'Cannot reactivate or deactivate a blacklisted trekker. Remove blacklist first.',
      'error'
    )
    return
  }

  try {
    const data = await trekkerStore.handleEditTrekker(trekker.user_id, selectedStatus.value, reason.value)
    flashStore.show(data?.message || 'Trekker updated successfully.', 'success')
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to update trekker status.', 'error')
  }
}
</script>

<template>
  <div
    class="modal fade"
    id="manageTrekkerModal"
    tabindex="-1"
    aria-hidden="true"
    data-bs-backdrop="static"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header bg-success text-white">
          <h5 class="modal-title">Manage Trekker</h5>
          <button class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body" v-if="trekkerStore.selectedTrekker">
          <div class="card bg-light mb-4">
            <div class="card-body">
              <h5>{{ trekkerStore.selectedTrekker.username }}</h5>
              <p class="text-muted mb-2">{{ trekkerStore.selectedTrekker.email }}</p>
              <span class="badge" :class="getStatusBadgeClass(trekkerStore.selectedTrekker)">
                Current: {{ getStatusLabel(trekkerStore.selectedTrekker) }}
              </span>
            </div>
          </div>

          <label class="fw-semibold mb-2">Change Status</label>

          <div
            v-if="trekkerStore.selectedTrekker.is_blacklisted"
            class="alert alert-warning py-2 small mb-3"
          >
            This trekker is blacklisted. Remove blacklist first before reactivating.
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              value="reactivate"
              v-model="selectedStatus"
              :disabled="trekkerStore.selectedTrekker.is_blacklisted"
            />
            <label
              class="form-check-label text-success"
              :class="{ 'text-muted': trekkerStore.selectedTrekker.is_blacklisted }"
            >
              Activate / Reactivate
            </label>
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              value="deactivate"
              v-model="selectedStatus"
              :disabled="trekkerStore.selectedTrekker.is_blacklisted"
            />
            <label
              class="form-check-label text-warning"
              :class="{ 'text-muted': trekkerStore.selectedTrekker.is_blacklisted }"
            >
              Deactivate
            </label>
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              value="blacklist"
              v-model="selectedStatus"
            />
            <label class="form-check-label text-danger">Blacklist</label>
          </div>

          <div class="form-check mb-4">
            <input
              class="form-check-input"
              type="radio"
              value="deblacklist"
              v-model="selectedStatus"
            />
            <label class="form-check-label">Remove Blacklist</label>
          </div>

          <label class="fw-semibold">Reason (Optional)</label>
          <textarea
            rows="4"
            class="form-control"
            v-model="reason"
            placeholder="Reason for status change..."
          ></textarea>
        </div>

        <div v-else class="modal-body text-center text-muted">Select a trekker.</div>

        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button class="btn btn-success" @click="handleSave">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
