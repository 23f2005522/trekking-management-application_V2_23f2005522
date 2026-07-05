<script setup>
import { useStaffStore } from '@/stores/staffStore'

const staffStore = useStaffStore()
</script>

<template>
  <div class="modal fade" id="manageStaffModal" tabindex="-1">
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

              <p class="text-muted">
                {{ staffStore.selectedStaff.email }}
              </p>

              <span
                class="badge"
                :class="{
                  'bg-success': staffStore.selectedStaff.status === 'approved',
                  'bg-warning text-dark': staffStore.selectedStaff.status === 'pending',
                  'bg-danger': staffStore.selectedStaff.status === 'rejected',
                  'bg-dark': staffStore.selectedStaff.status === 'blacklisted',
                }"
              >
                Current :
                {{ staffStore.selectedStaff.status }}
              </span>
            </div>
          </div>

          <label class="fw-semibold mb-2"> Change Status </label>

          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              value="pending"
              v-model="staffStore.selectedStatus"
            />
            <label class="form-check-label"> Pending </label>
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              value="approved"
              v-model="staffStore.selectedStatus"
            />
            <label class="form-check-label text-success"> Approved </label>
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="radio"
              value="rejected"
              v-model="staffStore.selectedStatus"
            />
            <label class="form-check-label text-danger"> Rejected </label>
          </div>

          <div class="form-check mb-3">
            <input
              class="form-check-input"
              type="radio"
              value="blacklisted"
              v-model="staffStore.selectedStatus"
            />
            <label class="form-check-label"> Blacklisted </label>
          </div>

          <label class="fw-semibold"> Reason </label>

          <textarea rows="4" class="form-control" v-model="staffStore.reason" />
        </div>

        <div v-else class="modal-body text-center">Loading...</div>

        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>

          <button class="btn btn-success" @click="staffStore.handelEditStaff()">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>