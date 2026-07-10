<script setup>
import AddTrekModal from '@/components/addTrekModal.vue'
import DeleteTrekModal from '@/components/deleteTrekModal.vue'
import EditTrekModal from '@/components/editTrekModal.vue'
import { useTrekStore } from '@/stores/admin/trekStore'
import { onMounted, ref } from 'vue'
const trekStore = useTrekStore()

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

onMounted(() => {
  trekStore.fetchTreks()
})

const selectedTrekID = ref(null)
const handleEdit = (id) => {
  selectedTrekID.value = id
}

const selectedTrekForDelete = ref(null)
const handleDelete = (id) => {
  selectedTrekForDelete.value = id
  console.log('Selected trek for deletion:', selectedTrekForDelete.value)
}
</script>

<template>
  <div>
    <!-- ModalS -->
    <AddTrekModal />
    <EditTrekModal :trekId="selectedTrekID" />
    <DeleteTrekModal :trekId="selectedTrekForDelete" />

    <!-- Heading -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h1 class="fw-bold">Manage Treks</h1>

        <p class="text-muted mb-0">View, create and manage trekking events.</p>
      </div>

      <!-- Modal Button -->
      <button
        class="btn btn-success d-flex align-items-center"
        data-bs-toggle="modal"
        data-bs-target="#addNewTrekModal"
      >
        <i class="bi bi-plus-lg me-2"></i>

        Add New Trek
      </button>
    </div>

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
                v-model="trekStore.treksearchQuery"
                type="text"
                class="form-control border-start-0"
                placeholder="Search by trek name, location, difficulty or status..."
              />
            </div>
          </div>

          <div class="col-md-4 text-end">
            <small class="text-muted">
              Showing

              <strong>{{ trekStore.filteredTreks.length }}</strong>

              of

              <strong>{{ trekStore.treks.length }}</strong>

              treks
            </small>
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->

    <div class="card shadow-sm">
      <div class="table-responsive">
        <table class="table table-hover table-striped align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Trek Name</th>
              <th>Location</th>
              <th>Difficulty</th>
              <th>Total Slots</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="trek in trekStore.filteredTreks" :key="trek.id">
              <td>{{ trek.id }}</td>
              <td>{{ trek.name }}</td>
              <td>{{ trek.location }}</td>
              <td>{{ trek.difficulty }}</td>
              <td>{{ trek.availableSlots }}</td>

              <td>
                <span :class="['badge text-uppercase', getStatusBadgeClass(trek.status)]">
                  {{ trek.status }}
                </span>
              </td>

              <td>
                <button
                  class="btn btn-outline-primary btn-sm me-2"
                  data-bs-toggle="modal"
                  data-bs-target="#editTrekModal"
                  @click="handleEdit(trek.id)"
                >
                  <i class="bi bi-pencil"></i>
                </button>

                <button
                  type="button"
                  class="btn btn-danger"
                  data-bs-toggle="modal"
                  data-bs-target="#deleteTrekModal"
                  @click="handleDelete(trek.id)"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </td>

              
              
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<!-- 


<button >
  Launch demo modal
</button>




-->

<style scoped>
.card {
  border-radius: 15px;
}

.table td,
.table th {
  vertical-align: middle;
}

.btn-sm {
  width: 36px;
  height: 36px;
}
</style>
