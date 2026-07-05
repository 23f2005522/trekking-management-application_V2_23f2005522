<script setup>
import ManagaStaffModal from '@/components/managaStaffModal.vue'

const trekkers = [
  {
    user_id: 1,
    username: 'Anish Das',
    email: 'anish@gmail.com',
    status: 'active',
    is_active: true,
  },
  {
    user_id: 2,
    username: 'Rahul Sharma',
    email: 'rahul@gmail.com',
    status: 'active',
    is_active: true,
  },
  {
    user_id: 3,
    username: 'Priya Singh',
    email: 'priya@gmail.com',
    status: 'inactive',
    is_active: false,
  },
  {
    user_id: 4,
    username: 'Amit Kumar',
    email: 'amit@gmail.com',
    status: 'active',
    is_active: true,
  },
  {
    user_id: 5,
    username: 'Sneha Roy',
    email: 'sneha@gmail.com',
    status: 'inactive',
    is_active: false,
  },
]

const handleTrekkerSelection = (id) => {
  console.log("Selected Trekker:", id)
}
</script>

<template>
  <div class="col p-4">
    <ManagaStaffModal />

    <!-- Heading -->
    <h1 class="fw-bold">Manage Trekkers</h1>

    <p class="text-muted">
      Review trekker accounts and manage their access.
    </p>

    <hr />

    <!-- Search -->
    <div class="card shadow-sm mb-4 border-0">
      <div class="card-body">
        <div class="row align-items-center">

          <div class="col-md-8">
            <div class="input-group">
              <span class="input-group-text bg-white border-end-0">
                <i class="bi bi-search text-success"></i>
              </span>

              <input
                type="text"
                class="form-control border-start-0"
                placeholder="Search by trekker name, email or ID..."
              />
            </div>
          </div>

          <div class="col-md-4 text-end">
            <small class="text-muted">
              Showing
              <strong>{{ trekkers.length }}</strong>
              of
              <strong>{{ trekkers.length }}</strong>
              Trekkers
            </small>
          </div>

        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card shadow-sm border-0">
      <div class="table-responsive">

        <table class="table table-hover mb-0">

          <thead class="bg-success text-white">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Account Status</th>
              <th>Activity</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="trekker in trekkers"
              :key="trekker.user_id"
            >
              <td>{{ trekker.user_id }}</td>

              <td>{{ trekker.username }}</td>

              <td>{{ trekker.email }}</td>

              <td>
                <span
                  :class="{
                    'badge bg-success p-2': trekker.status === 'active',
                    'badge bg-danger p-2': trekker.status === 'inactive'
                  }"
                >
                  {{ trekker.status }}
                </span>
              </td>

              <td>
                <span
                  :class="{
                    'badge bg-success': trekker.is_active,
                    'badge bg-secondary': !trekker.is_active
                  }"
                >
                  {{ trekker.is_active ? "Active" : "Inactive" }}
                </span>
              </td>

              <td>
                <button
                  class="btn btn-primary btn-sm"
                  @click="handleTrekkerSelection(trekker.user_id)"
                  data-bs-toggle="modal"
                  data-bs-target="#manageStaffModal"
                >
                  <i class="bi bi-pencil"></i>
                </button>
              </td>

            </tr>

            <tr v-if="trekkers.length === 0">
              <td colspan="6" class="text-center text-muted py-4">
                No trekkers found.
              </td>
            </tr>

          </tbody>

        </table>

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