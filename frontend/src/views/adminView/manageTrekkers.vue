<script setup>
import ManageTrekkerModal from '@/components/manageTrekkerModal.vue'
import { useFlashStore } from '@/stores/flashStore'
import { userTrekkerStore } from '@/stores/admin/trekkerStore'
import { onMounted } from 'vue'



const TrekkerStore = userTrekkerStore()
const flashStore = useFlashStore()
onMounted(() => {
  try {
    TrekkerStore.fetchAllTrekkers()
    flashStore.show('Trekkers fetched successfully.', 'success')
  } catch (error) {
    flashStore.show('Error fetching trekkers.', 'danger')
  }
})

const handleTrekkerSelection = (id) => {
  console.log('Selected Trekker:', id)
  TrekkerStore.selectedTrekkerId = id
}

</script>

<template>
  <div>
    <ManageTrekkerModal/>

    <!-- Heading -->
    <h1 class="fw-bold">Manage Trekkers</h1>

    <p class="text-muted">Review trekker accounts and manage their access.</p>

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
                v-model="TrekkerStore.trekkersearchQuery"
                type="text"
                class="form-control border-start-0" 
                placeholder="Search by trekker name, email or ID..."
              />
            </div>
          </div>

          <div class="col-md-4 text-end">
            <small class="text-muted">
              Showing
              <strong>{{ TrekkerStore.filteredTrekkers.length }}</strong>
              of
              <strong>{{ TrekkerStore.allTrekkers.length }}</strong>
              Trekkers
            </small>
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="card shadow-sm border-0">


      <div v-if="TrekkerStore.filteredTrekkers.length <= 0" class="card-footer text-muted">

        No trekkers found.
      </div>

        <div class="table-responsive" v-else> 
        <table class="table table-hover mb-0">
          <thead class="bg-success text-white">
            <tr>
              <th>User ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone Number</th>
              <th>Account Status</th>
              <th>Activity</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="trekker in TrekkerStore.filteredTrekkers" :key="trekker.user_id">
              <td>{{ trekker.user_id }}</td>

              <td>{{ trekker.username }}</td>

              <td>{{ trekker.email }}</td>
              <td>{{ trekker.phone }}</td>

              <td>
                <span
                  :class="{
                    'badge bg-success p-2': trekker.is_blacklisted === false,
                    'badge bg-danger p-2': trekker.is_blacklisted === true,
                  }"
                >
                  {{ trekker.is_blacklisted ? 'Blacklisted' : "Active" }}
                </span>
              </td>

              <td>
                <span
                  :class="{
                    'badge bg-success': trekker.is_active,
                    'badge bg-secondary': !trekker.is_active,
                  }"
                >
                  {{ trekker.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>

              <td>
                <button
                  class="btn btn-primary btn-sm"
                  @click="handleTrekkerSelection(trekker.user_id)"
                  data-bs-toggle="modal"
                  data-bs-target="#manageTrekkerModal"
                >
                  <i class="bi bi-pencil"></i>
                </button>
              </td>
            </tr>

            <tr v-if="TrekkerStore.filteredTrekkers.length === 0">
              <td colspan="6" class="text-center text-muted py-4">No trekkers found.</td>
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
