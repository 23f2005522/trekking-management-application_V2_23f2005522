<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { userStaffStore } from '@/stores/staff/staffStore'

const staffStore = userStaffStore()
const { assignedTreks, updatingSlotsId } = storeToRefs(staffStore)

const getStatusBadgeClass = (status) => {
  const normalizedStatus = String(status || '').toLowerCase()

  const statusClassMap = {
    open: 'bg-success',
    ongoing: 'bg-warning text-dark',
    pending: 'bg-danger',
    closed: 'bg-secondary',
    completed: 'bg-primary',
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

const updateAvailableSlots = async (trek) => {
  try {
    await staffStore.updateTrekSlots(trek.id, trek.available_slots)
  } catch {
    // staffStore already shows flash on failure
  }
}

onMounted(async () => {
  try {
    await staffStore.fetchDashboardData()
  } catch {
    // staffStore already shows flash on failure
  }
})
</script>

<template>
  <div class="py-4">
    <div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-4">
      <div>
        <h1 class="fw-bold mb-1">My Treks</h1>
        <p class="text-muted mb-0">Live trek cards loaded from the staff API.</p>
      </div>

      <div class="badge bg-light text-success border border-success-subtle px-3 py-2 rounded-pill">
        <i class="bi bi-signpost-2 me-1"></i>
        {{ assignedTreks.length }} Assigned Treks
      </div>
    </div>

    <div class="row g-4">
      <div v-for="trek in assignedTreks" :key="trek.id" class="col-12 col-xl-6">
        <div class="card shadow-sm trek-card h-100 border-0">
          <div class="card-header trek-card-header bg-white border-0 pb-0">
            <div class="d-flex justify-content-between align-items-start gap-3">
              <div>
                <h4 class="mb-1 fw-semibold">{{ trek.name }}</h4>
                <p class="text-muted mb-0">{{ trek.location }} · {{ trek.difficulty }}</p>
              </div>

              <span :class="['badge text-uppercase px-3 py-2', getStatusBadgeClass(trek.status)]">
                {{ trek.status }}
              </span>
            </div>
          </div>

          <div class="card-body pt-3">
            <div class="row g-3">
              <div class="col-md-6">
                <div class="info-box">
                  <small class="text-muted d-block">Time</small>
                  <strong>{{ formatDisplayDate(trek.starting_date) }} - {{ formatDisplayDate(trek.ending_date) }}</strong>
                </div>
              </div>

              <div class="col-md-6">
                <div class="info-box">
                  <small class="text-muted d-block">Difficulty</small>
                  <strong>{{ trek.difficulty }}</strong>
                </div>
              </div>

              <div class="col-4">
                <div class="info-box">
                  <small class="text-muted d-block">Total Slots</small>
                  <strong class="text-primary">{{ trek.total_slots }}</strong>
                </div>
              </div>

              <div class="col-4">
                <div class="info-box">
                  <small class="text-muted d-block">Available Slots</small>
                  <strong class="text-success">{{ trek.available_slots }}</strong>
                </div>
              </div>

              <div class="col-4">
                <div class="info-box">
                  <small class="text-muted d-block">Booked Slots (participants)</small>
                  <strong class="text-danger">{{ trek.total_participants }}</strong>
                </div>
              </div>

              <div class="col-12">
                <div class="info-box">
                  <small class="text-muted d-block mb-2">Update Available Slots</small>
                  <div class="d-flex gap-2 flex-wrap align-items-center">
                    <input
                      v-model.number="trek.available_slots"
                      type="number"
                      min="0"
                      :max="trek.total_slots"
                      class="form-control form-control-sm"
                      style="max-width: 120px;"
                    />

                    <button
                      class="btn btn-primary btn-sm"
                      :disabled="updatingSlotsId === trek.id"
                      @click="updateAvailableSlots(trek)"
                    >
                      {{ updatingSlotsId === trek.id ? 'Saving...' : 'Update Slots' }}
                    </button>
                  </div>
                </div>
              </div>

              <div class="col-12 d-flex justify-content-between align-items-center flex-wrap gap-2 mt-2">
                <div></div>

                <button
                  class="btn btn-outline-success px-4"
                  @click="$router.push({ name: 'staffParticipants', query: { trekId: trek.id } })"
                >
                  View Participants
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trek-card {
  border-radius: 18px;
  overflow: hidden;
}

.trek-card-header {
  padding: 1.25rem 1.25rem 0.25rem;
}

.info-box {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  padding: 0.85rem 1rem;
  min-height: 72px;
}
</style>
