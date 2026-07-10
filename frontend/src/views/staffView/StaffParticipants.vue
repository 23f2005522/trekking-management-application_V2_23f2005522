<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { userStaffStore } from '@/stores/staff/staffStore'

const staffStore = userStaffStore()
const {
  assignedTreks,
  participantsTrek,
  participants,
  loadingParticipants,
} = storeToRefs(staffStore)

const selectedTrekId = ref(null)

const trek = computed(() => participantsTrek.value)

const selectedTrekName = computed(() => {
  return (
    trek.value?.name ||
    assignedTreks.value.find((t) => t.id === selectedTrekId.value)?.name ||
    'Select a trek'
  )
})

const getStatusBadgeClass = (status) => {
  const normalizedStatus = String(status || '').toLowerCase()

  const statusClassMap = {
    booked: 'bg-success',
    completed: 'bg-primary',
    canceled: 'bg-danger',
    open: 'bg-success',
    ongoing: 'bg-warning text-dark',
    pending: 'bg-danger',
    closed: 'bg-secondary',
    approved: 'bg-info text-dark',
  }

  return statusClassMap[normalizedStatus] || 'bg-secondary'
}

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

const togglePayment = async (participant) => {
  try {
    await staffStore.toggleParticipantPayment(selectedTrekId.value, participant.id)
  } catch {
    // staffStore already shows flash on failure
  }
}

const selectTrek = (trekId) => {
  selectedTrekId.value = trekId
}

watch(selectedTrekId, (trekId) => staffStore.fetchParticipants(trekId))

onMounted(async () => {
  try {
    await staffStore.fetchDashboardData()

    if (assignedTreks.value.length > 0) {
      selectTrek(assignedTreks.value[0].id)
    }
  } catch {
    // staffStore already shows flash on failure
  }
})
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-4">
      <div>
        <h1 class="fw-bold mb-1">Participants</h1>
        <p class="text-muted mb-0">View participants grouped by your assigned treks.</p>
      </div>

      <div class="badge bg-light text-success border border-success-subtle px-3 py-2 rounded-pill">
        <i class="bi bi-people me-1"></i>
        {{ participants.length }} Participants
      </div>
    </div>

    <div class="row g-4">
      <div class="col-12 col-lg-4 col-xl-3">
        <div class="trek-list-panel">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="fw-semibold mb-0">Assigned Treks</h5>
            <span class="badge bg-success">{{ assignedTreks.length }}</span>
          </div>

          <button
            v-for="assignedTrek in assignedTreks"
            :key="assignedTrek.id"
            type="button"
            :class="[
              'trek-list-item text-start w-100 mb-2',
              selectedTrekId === assignedTrek.id ? 'active' : '',
            ]"
            @click="selectTrek(assignedTrek.id)"
          >
            <span class="fw-semibold d-block">{{ assignedTrek.name }}</span>
            <small class="text-muted d-block">
              {{ assignedTrek.location }} - {{ formatDisplayDate(assignedTrek.starting_date) }}
            </small>
            <span :class="['badge mt-2 text-uppercase', getStatusBadgeClass(assignedTrek.status)]">
              {{ assignedTrek.status }}
            </span>
          </button>

          <div v-if="assignedTreks.length === 0" class="text-muted text-center py-4">
            No assigned treks found.
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-8 col-xl-9">
        <div class="participants-panel">
          <div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-3">
            <div>
              <h4 class="fw-semibold mb-1">
                {{ selectedTrekName }} (TrekID: {{ selectedTrekId }})
              </h4>
              <p v-if="trek" class="text-muted mb-0">
                {{ trek.location }} - {{ formatDisplayDate(trek.starting_date) }} to
                {{ formatDisplayDate(trek.ending_date) }}
              </p>
              <p v-else class="text-muted mb-0">Choose an assigned trek to see bookings.</p>
            </div>

            <div v-if="trek" class="d-flex gap-2 flex-wrap">
              <span class="badge bg-light text-dark border px-3 py-2">
                Total: {{ trek.total_participants }}
              </span>
              <span class="badge bg-light text-success border border-success-subtle px-3 py-2">
                Available: {{ trek.available_slots }}
              </span>
            </div>
          </div>

          <div v-if="loadingParticipants" class="text-center text-muted py-5">
            Loading participants...
          </div>

          <div v-else class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Booking Date</th>
                  <th>Booking Status</th>
                  <th>Payment Status</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="participant in participants" :key="participant.id">
                  <td>{{ participant.id }}</td>
                  <td>{{ participant.username }}</td>
                  <td>{{ participant.email }}</td>
                  <td>{{ participant.booking_date }}</td>
                  <td>
                    <span
                      :class="['badge text-uppercase', getStatusBadgeClass(participant.status)]"
                    >
                      {{ participant.status }}
                    </span>
                  </td>

                  <td>
                    <button
                      class="btn btn-sm"
                      :class="participant.payment_status === 'paid' ? 'btn-success' : 'btn-warning'"
                      @click="togglePayment(participant)"
                    >
                      <i
                        class="bi me-1"
                        :class="
                          participant.payment_status === 'paid' ? 'bi-check-circle' : 'bi-cash'
                        "
                      ></i>

                      {{ participant.payment_status }}
                    </button>
                  </td>
                </tr>

                <tr v-if="participants.length === 0">
                  <td colspan="5" class="text-center text-muted py-5">
                    No participants found for this trek.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trek-list-panel,
.participants-panel {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  box-shadow: 0 0.125rem 0.35rem rgba(33, 37, 41, 0.05);
  padding: 1rem;
}

.trek-list-item {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 0.85rem 1rem;
  transition:
    border-color 0.15s ease,
    background-color 0.15s ease;
}

.trek-list-item.active,
.trek-list-item:hover {
  background: #f0fff7;
  border-color: #198754;
}
</style>
