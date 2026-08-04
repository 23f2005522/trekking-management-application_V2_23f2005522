<script setup>
import { ref, watch } from 'vue'
import { useStaffStore } from '@/stores/admin/staffStore'
import { useFlashStore } from '@/stores/flashStore'

const staffStore = useStaffStore()
const flashStore = useFlashStore()

const selectedStatus = ref('approved')
const reason = ref('')

const setDefaultAction = (staff) => {
  if (!staff) {
    selectedStatus.value = 'approved'
    reason.value = ''
    return
  }

  if (staff.status === 'blacklisted') {
    selectedStatus.value = 'blacklisted'
  } else if (staff.status === 'rejected') {
    selectedStatus.value = 'rejected'
  } else if (!staff.is_active && staff.status === 'approved') {
    selectedStatus.value = 'reactivate'
  } else if (staff.is_active && staff.status === 'approved') {
    selectedStatus.value = 'approved'
  } else {
    selectedStatus.value = staff.status
  }

  reason.value = staff.blacklisted_reason || ''
}

watch(
  () => staffStore.selectedStaff,
  (staff) => setDefaultAction(staff),
  { immediate: true }
)

const getAccessLabel = (staff) => {
  if (staff.status === 'blacklisted') return 'Blacklisted'
  if (!staff.is_active) return 'Deactivated'
  return 'Active'
}

const getAccessBadgeClass = (staff) => {
  if (staff.status === 'blacklisted') return 'bg-dark'
  if (!staff.is_active) return 'bg-secondary'
  return 'bg-success'
}

const handleSaveChanges = async () => {
  const staff = staffStore.selectedStaff
  if (!staff) return

  if (
    staff.status === 'blacklisted' &&
    (selectedStatus.value === 'reactivate' || selectedStatus.value === 'deactivate')
  ) {
    flashStore.show(
      'Cannot deactivate or reactivate a blacklisted staff member. Change profile status first.',
      'error'
    )
    return
  }

  if (
    selectedStatus.value === 'deactivate' &&
    staff.status !== 'approved'
  ) {
    flashStore.show('Only approved staff can be deactivated.', 'error')
    return
  }

  try {
    const data = await staffStore.handelEditStaff(selectedStatus.value, reason.value)
    flashStore.show(data?.message || 'Staff updated successfully.', 'success')
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to edit staff.', 'error')
  }
}
</script>

<template>
  <div class="modal fade" id="manageStaffModal" tabindex="-1" data-bs-backdrop="static">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header bg-success text-white">
          <h5 class="modal-title">Manage Staff</h5>

          <button class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body" v-if="staffStore.selectedStaff">
          <div class="card bg-light mb-4">
            <div class="card-body">
              <h5>
                {{ staffStore.selectedStaff.username }}
              </h5>

              <p class="text-muted mb-2">
                {{ staffStore.selectedStaff.email }}
              </p>

              <span
                class="badge me-2"
                :class="{
                  'bg-success': staffStore.selectedStaff.status === 'approved',
                  'bg-warning text-dark': staffStore.selectedStaff.status === 'pending',
                  'bg-danger': staffStore.selectedStaff.status === 'rejected',
                  'bg-dark': staffStore.selectedStaff.status === 'blacklisted',
                }"
              >
                Profile: {{ staffStore.selectedStaff.status }}
              </span>

              <span class="badge" :class="getAccessBadgeClass(staffStore.selectedStaff)">
                Access: {{ getAccessLabel(staffStore.selectedStaff) }}
              </span>
            </div>
          </div>

          <label class="fw-semibold mb-2">Profile Status</label>

          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              value="pending"
              v-model="selectedStatus"
            />
            <label class="form-check-label"> Pending </label>
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              value="approved"
              v-model="selectedStatus"
            />
            <label class="form-check-label text-success"> Approved </label>
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              value="rejected"
              v-model="selectedStatus"
            />
            <label class="form-check-label text-danger"> Rejected </label>
          </div>

          <div class="form-check mb-3">
            <input
              class="form-check-input"
              type="radio"
              value="blacklisted"
              v-model="selectedStatus"
            />
            <label class="form-check-label"> Blacklisted </label>
          </div>

          <label class="fw-semibold mb-2">Account Access</label>

          <div
            v-if="staffStore.selectedStaff.status === 'blacklisted'"
            class="alert alert-warning py-2 small mb-3"
          >
            Blacklisted staff must have profile status changed before account access updates.
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              value="reactivate"
              v-model="selectedStatus"
              :disabled="staffStore.selectedStaff.status !== 'approved'"
            />
            <label
              class="form-check-label text-success"
              :class="{ 'text-muted': staffStore.selectedStaff.status !== 'approved' }"
            >
              Activate / Reactivate
            </label>
          </div>

          <div class="form-check mb-3">
            <input
              class="form-check-input"
              type="radio"
              value="deactivate"
              v-model="selectedStatus"
              :disabled="staffStore.selectedStaff.status !== 'approved'"
            />
            <label
              class="form-check-label text-warning"
              :class="{ 'text-muted': staffStore.selectedStaff.status !== 'approved' }"
            >
              Deactivate (with reason)
            </label>
          </div>

          <label class="fw-semibold">Reason</label>

          <textarea
            rows="4"
            class="form-control"
            v-model="reason"
            placeholder="Reason for rejection, blacklist, or deactivation..."
          />
        </div>

        <div v-else class="modal-body text-center text-muted">Select a staff member.</div>

        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>

          <button class="btn btn-success" @click="handleSaveChanges">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
