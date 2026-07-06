<script setup>
const history = [
  {
    id: 1,
    trekName: 'Roopkund Trek',
    trekDates: '10 Apr - 16 Apr 2026',
    completedOn: '16 Apr 2026',
    status: 'Completed',
  },
  {
    id: 2,
    trekName: 'Kedarkantha Trek',
    trekDates: '15 Jan - 20 Jan 2026',
    completedOn: '20 Jan 2026',
    status: 'Completed',
  },
  {
    id: 3,
    trekName: 'Kuari Pass',
    trekDates: '05 Jan - 10 Jan 2026',
    completedOn: '10 Jan 2026',
    status: 'Completed',
  },
]
</script>

<template>
  <div>
    <h2 class="fw-bold mb-4">Trekking History</h2>

    <div class="card shadow-sm">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th>Trek Name</th>
              <th>Trek Dates</th>
              <th>Completed On</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in history" :key="item.id">
              <td>{{ item.trekName }}</td>
              <td>{{ item.trekDates }}</td>
              <td>{{ item.completedOn }}</td>
              <td>
                <span class="badge bg-success">{{ item.status }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="alert alert-primary d-flex align-items-center gap-2 mt-5" role="alert">
      <i class="bi bi-info-circle"></i>
      <span>History shows all your completed and cancelled treks.</span>
    </div>
  </div>
</template>
