<script setup>
import { onMounted, ref } from 'vue'
import Loader from '@/components/Loader.vue'
import StaffManageTrekModal from '@/components/staffManageTrekModal.vue'
import { userStaffStore } from '@/stores/staff/staffStore'
import { useFlashStore } from '@/stores/flashStore'

const staffStore = userStaffStore()
const flashStore = useFlashStore()
const selectedTrekId = ref(null)

const openManageModal = async (trek) => {
  selectedTrekId.value = trek.id
  try {
    await staffStore.fetchTrekById(trek.id)
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to load trek details.', 'error')
  }
}


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

// format date to display in the table
const formatDisplayDate = (dateString) => {
  if (!dateString) return '-'

  const date = new Date(dateString)

  if (Number.isNaN(date.getTime())) return dateString

  return new Intl.DateTimeFormat('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(date)
}

//fetch the dashboard data when the component is mounted
onMounted(async () => {
  try {
    await staffStore.fetchDashboardData()
  } catch (error) {
    flashStore.show(error.response?.data?.message || 'Failed to load dashboard data.', 'error')
  }
})


</script>

<template>
  <div>
    <h1 class="fw-bold">
      My Dashboard
    </h1>

    <p class="text-muted">
      Welcome back! {{ staffStore.staffProfile?.username }} Here's an overview of your assigned treks.
    </p>

    <div v-if="staffStore.loadingDashboard" class="d-flex justify-content-center align-items-center py-5">
      <Loader />
    </div>

    <template v-else>
    <div class="row g-4 mt-2">
          <!-- Assigned Treks -->
          <div class="col-md-6 col-lg-4">
            <div class="card shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="text-muted">
                      Assigned Treks
                    </h6>

                    <h1 class="fw-bold text-success">
                      {{ staffStore.dashboardStats.totalAssignedTreks }}
                    </h1>

                    <small class="text-success">
                      Active Assignments
                    </small>
                  </div>

                  <i class="bi bi-signpost-2 fs-1 text-success"></i>
                </div>
              </div>
            </div>
          </div>

          <!-- Participants -->
          <div class="col-md-6 col-lg-4">
            <div class="card shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="text-muted">
                      Participants
                    </h6>

                    <h1 class="fw-bold text-success">
                      {{ staffStore.dashboardStats.totalParticipants }}
                    </h1>

                    <small class="text-success">
                      Registered
                    </small>
                  </div>

                  <i class="bi bi-people fs-1 text-success"></i>
                </div>
              </div>
            </div>
          </div>

          <!-- Open Treks -->
          <div class="col-md-6 col-lg-4">
            <div class="card shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between">
                  <div>
                    <h6 class="text-muted">
                      Open Treks
                    </h6>

                    <h1 class="fw-bold text-success">
                      {{ staffStore.dashboardStats.activeAssignedTreks }}
                    </h1>

                    <small class="text-success">
                      Currently Running
                    </small>
                  </div>

                  <i class="bi bi-calendar-check fs-1 text-success"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Treks starting in 7 days -->
        <div class="card shadow-sm mt-4 border-0">
          <div class="card-header bg-white d-flex justify-content-between align-items-center">
            <h4 class="mb-0">
              <i class="bi bi-calendar-event text-primary me-2"></i>
              Treks Starting in 7 Days
            </h4>
            <span class="badge bg-primary">{{ staffStore.upcomingTreks.length }} upcoming</span>
          </div>

          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>Trek</th>
                  <th>Location</th>
                  <th>Start Date</th>
                  <th>Participants</th>
                  <th>Starts In</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="trek in staffStore.upcomingTreks" :key="trek.id">
                  <td class="fw-semibold">{{ trek.name }}</td>
                  <td>{{ trek.location }}</td>
                  <td>{{ formatDisplayDate(trek.starting_date) }}</td>
                  <td>{{ trek.total_participants }}</td>
                  <td>
                    <span class="badge bg-info text-dark">
                      {{ trek.days_until_start === 0 ? 'Today' : `${trek.days_until_start} day(s)` }}
                    </span>
                  </td>
                  <td>
                    <span :class="['badge text-uppercase', getStatusBadgeClass(trek.status)]">
                      {{ trek.status }}
                    </span>
                  </td>
                </tr>
                <tr v-if="staffStore.upcomingTreks.length === 0">
                  <td colspan="6" class="text-center text-muted py-4">
                    No treks starting in the next 7 days.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Assigned Treks Table -->
        <div class="card shadow-sm mt-5">
          <div class="card-header bg-white">
            <h4 class="mb-0">
              My Assigned Treks
            </h4>
          </div>

          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>Trek</th>
                  <th>Location</th>
                  <th>Participants</th>
                  <th>Slots</th>
                  <th>Time</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="trek in staffStore.assignedTreks" :key="trek.id">
                  <td>{{ trek.name }}</td>
                  <td>{{ trek.location }}</td>
                  <td>{{ trek.total_participants }}</td>
                  <td>{{ trek.available_slots }}</td>
                  <td>{{ formatDisplayDate(trek.starting_date) }} - {{ formatDisplayDate(trek.ending_date) }}</td>

                  <td>
                    <span :class="['badge text-uppercase', getStatusBadgeClass(trek.status)]">
                      {{ trek.status }}
                    </span>
                  </td>

                  <td>
                    <button
                      type="button"
                      class="btn btn-outline-success btn-sm"
                      data-bs-toggle="modal"
                      data-bs-target="#staffManageTrekModal"
                      @click="openManageModal(trek)"
                    >
                      Manage
                    </button>
                  </td>
                </tr>

                <tr v-if="staffStore.assignedTreks.length === 0">
                  <td colspan="7" class="text-center text-muted py-4">
                    No assigned treks found.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

    </template>

    <StaffManageTrekModal :trekId="selectedTrekId" />
  </div>
</template>
