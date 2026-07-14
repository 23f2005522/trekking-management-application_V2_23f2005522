<script setup>
import { onMounted } from 'vue'
import Loader from '@/components/Loader.vue'
import { useStaffStore } from '@/stores/admin/staffStore'
import { useFlashStore } from '@/stores/flashStore'
import ManagaStaffModal from '@/components/managaStaffModal.vue'
import CreateStaffModal from '@/components/createStaffModal.vue'

const staffStore = useStaffStore()
const flashStore = useFlashStore()

onMounted(async () => {
  try {
    await staffStore.fetchStaffs()
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to fetch staff.', 'error')
  }
})




</script>

<template>
  <div>
    <!-- modals -->
    <ManagaStaffModal />
    <CreateStaffModal />

    <!-- Heading -->

    <div class="d-flex justify-content-between align-items-start mb-2">
      <div>
        <h1 class="fw-bold mb-1">Manage Staff</h1>
        <p class="text-muted mb-0">Create staff accounts and manage approval status.</p>
      </div>

      <button
        class="btn btn-success"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#createStaffModal"
      >
        <i class="bi bi-person-plus me-1"></i>
        Add Staff
      </button>
    </div>

    <hr />

    <div>
      <!-- search  -->
      <div class="card shadow-sm mb-4 border-0">
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-md-8">
              <div class="input-group">
                <span class="input-group-text bg-white border-end-0">
                  <i class="bi bi-search text-success"></i>
                </span>

                <input
                  v-model="staffStore.staffsearchQuery"
                  type="text"
                  class="form-control border-start-0"
                  placeholder="Search by staff name, email, status or Staff ID..."
                />
              </div>
            </div>

            <div class="col-md-4 text-end">
              <small class="text-muted">
                Showing

                <strong>{{ staffStore.filteredStaffs?.length ?? 0 }}</strong>

                of

                <strong>{{ staffStore.allStaffs?.length ?? 0 }}</strong>

                Staffs
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- all staffs -->
      <div class="card shadow-sm border-0">
        <div v-if="staffStore.loadingStaffs" class="d-flex justify-content-center align-items-center p-5">
          <Loader />
        </div>

        <div v-else class="table-responsive p-3">
          <table class="table table-hover mb-0">
            <thead class="bg-success text-white">
              <tr>
                <th scope="col">UserID</th>
                <th scope="col">StaffID</th>
                <th scope="col">Name</th>
                <th scope="col">PhoneNumber</th>
                <th scope="col">Email</th>
                <th scope="col">Status</th>
                <th scope="col">Actions</th>
                <th scope="col">Edit Staff</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="staff in staffStore.filteredStaffs" :key="staff.user_id">
                <td>{{ staff.user_id }}</td>
                <td>{{ staff.staff_id }}</td>
                <td>{{ staff.username }}</td>
                <td>{{ staff.phone }}</td>
                <td>{{ staff.email }}</td>
                <td>
                  <span
                    :class="{
                      'badge bg-success': staff.status === 'approved',
                      'badge bg-warning': staff.status === 'pending',
                      'badge bg-danger': staff.status === 'rejected',
                      'badge bg-dark': staff.status === 'blacklisted',
                      'p-2': true,
                    }"
                  >
                    {{ staff.status }}
                  </span>
                </td>

                <td>
                  <!-- Actions -->
                  <div
                    :class="{
                      'badge bg-success': staff.is_active,
                      'badge bg-secondary': !staff.is_active,
                    }"
                  >
                    {{ staff.is_active ? 'Active' : 'Inactive' }}
                  </div>
                </td>

                <td>
                  <!-- Actions -->
                  <button
                    type="button"
                    class="btn btn-primary"
                    data-bs-toggle="modal"
                    data-bs-target="#manageStaffModal"
                    @click="staffStore.selectedStaffId = staff.user_id"
                  >
                    <i class="bi bi-pencil"></i>
                  </button>
                </td>
              </tr>

              <!-- No Staffs Found -->
              <tr v-if="staffStore.filteredStaffs.length === 0">
                <td colspan="8" class="text-center text-muted py-4">No staffs found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  border-radius: 15px;
}

.table td,
.table th {
  vertical-align: middle;
}

.badge {
  padding: 8px 12px;
}
</style>
