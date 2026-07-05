<script setup>
import { onMounted, ref } from 'vue'
import { useStaffStore } from '@/stores/staffStore'
import ManagaStaffModal from '@/components/managaStaffModal.vue'

const staffStore = useStaffStore()

onMounted(() => {
  staffStore.allFetchStaffs()
})


const handelStaffSelection = (staffId) => {
  console.log("Selected Staff ID:", staffId)
  staffStore.selectedStaffId = staffId
}




</script>

<template>
  <div class="col p-4">
    <!-- modal -->
    <ManagaStaffModal />

    <!-- Heading -->

    <h1 class="fw-bold">Manage Staff</h1>
    <p class="text-muted">Review staff registration requests and manage staff accounts.</p>
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
                  placeholder="Search by staff name, email, status or ID..."
                />
              </div>
            </div>

            <div class="col-md-4 text-end">
              <small class="text-muted">
                Showing

                <strong>{{ staffStore.filteredStaffs.length || 0 }}</strong>

                of

                <strong>{{ staffStore.allStaffs.length || 0 }}</strong>

                Staffs
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- all staffs -->
      <div class="card shadow-sm border-0">
        <div
          v-if="staffStore.loadingStaffs === false"
          class="d-flex justify-content-center align-items-center p-5"
        >
          <table class="table table-hover mb-0">
            <thead class="bg-success text-white">
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Name</th>
                <th scope="col">PhoneNumber</th>
                <th scope="col">Email</th>
                <th scope="col">Status</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="staff in staffStore.filteredStaffs" :key="staff.user_id">
                <td>{{ staff.user_id }}</td>
                <td>{{ staff.username }}</td>
                <td>{{ staff.phone }}</td>
                <td>{{ staff.email }}</td>
                <td>
                  <span
                    :class="{
                      'badge bg-success': staff.status === 'approved',
                      'badge bg-warning': staff.status === 'pending',
                      'badge bg-danger': staff.status === 'rejected',
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
                    @click="handelStaffSelection(staff.user_id)"
                    class="btn btn-primary"
                    data-bs-toggle="modal"
                    data-bs-target="#manageStaffModal"
                  >
                    <i class="bi bi-pencil"></i>
                  </button>
                </td>
              </tr>

              <!-- No Staffs Found -->
              <tr v-if="staffStore.filteredStaffs.length === 0">
                <td colspan="5" class="text-center text-muted py-4">No staffs found.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="d-flex justify-content-center align-items-center p-5">
          Loading staffs...
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

.nav-tabs .nav-link {
  color: #198754;
}

.nav-tabs .nav-link.active {
  font-weight: 600;
}

.badge {
  padding: 8px 12px;
}
</style>
