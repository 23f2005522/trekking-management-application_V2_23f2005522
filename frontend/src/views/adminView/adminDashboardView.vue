<script setup>
import AdminSidebar from './adminSidebar.vue'
</script>

<template>
  <div class="container-fluid">

    <div class="row">

      <!-- Sidebar -->
      <div class="col-auto p-0">
        <AdminSidebar />
      </div>

      <!-- Main Content -->
      <div class="col p-4">

        <h1 class="fw-bold">
          Dashboard
        </h1>

        <p class="text-muted">
          Welcome back, Admin!
          Here's what's happening with your trekking platform.
        </p>

        <!-- Statistics -->

        <div class="row g-4 mt-2">

          <div class="col-md-6 col-lg-3">

            <div class="card shadow-sm">

              <div class="card-body">

                <div class="d-flex justify-content-between">

                  <div>

                    <h6 class="text-muted">
                      Total Treks
                    </h6>

                    <h1 class="text-success fw-bold">
                      15
                    </h1>

                    <small class="text-success">
                      +3 this month
                    </small>

                  </div>

                  <i class="bi bi-signpost-2 fs-1 text-success"></i>

                </div>

              </div>

            </div>

          </div>

          <div class="col-md-6 col-lg-3">

            <div class="card shadow-sm">

              <div class="card-body">

                <div class="d-flex justify-content-between">

                  <div>

                    <h6 class="text-muted">
                      Total Users
                    </h6>

                    <h1 class="text-success fw-bold">
                      248
                    </h1>

                    <small class="text-success">
                      +15 this month
                    </small>

                  </div>

                  <i class="bi bi-person fs-1 text-success"></i>

                </div>

              </div>

            </div>

          </div>

          <div class="col-md-6 col-lg-3">

            <div class="card shadow-sm">

              <div class="card-body">

                <div class="d-flex justify-content-between">

                  <div>

                    <h6 class="text-muted">
                      Total Staff
                    </h6>

                    <h1 class="text-success fw-bold">
                      18
                    </h1>

                    <small class="text-success">
                      +2 this month
                    </small>

                  </div>

                  <i class="bi bi-people fs-1 text-success"></i>

                </div>

              </div>

            </div>

          </div>

          <div class="col-md-6 col-lg-3">

            <div class="card shadow-sm">

              <div class="card-body">

                <div class="d-flex justify-content-between">

                  <div>

                    <h6 class="text-muted">
                      Total Bookings
                    </h6>

                    <h1 class="text-success fw-bold">
                      540
                    </h1>

                    <small class="text-success">
                      +20 this month
                    </small>

                  </div>

                  <i class="bi bi-calendar-check fs-1 text-success"></i>

                </div>

              </div>

            </div>

          </div>

        </div>

        <!-- Recent Bookings -->

        <div class="card shadow-sm mt-5">

          <div class="card-header bg-white">

            <h4 class="mb-0">
              Recent Bookings
            </h4>

          </div>

          <div class="table-responsive">

            <table class="table table-hover align-middle mb-0">

              <thead class="table-light">

                <tr>

                  <th>Booking ID</th>
                  <th>User</th>
                  <th>Trek</th>
                  <th>Date</th>
                  <th>Status</th>

                </tr>

              </thead>

              <tbody>

                <tr>

                  <td>#101</td>
                  <td>Rahul</td>
                  <td>Everest Base Camp</td>
                  <td>10 Jul 2026</td>

                  <td>
                    <span class="badge bg-warning text-dark">
                      Booked
                    </span>
                  </td>

                </tr>

                <tr>

                  <td>#102</td>
                  <td>Priya</td>
                  <td>Kedarkantha</td>
                  <td>12 Jul 2026</td>

                  <td>
                    <span class="badge bg-success">
                      Completed
                    </span>
                  </td>

                </tr>

                <tr>

                  <td>#103</td>
                  <td>Arjun</td>
                  <td>Valley of Flowers</td>
                  <td>15 Jul 2026</td>

                  <td>
                    <span class="badge bg-danger">
                      Cancelled
                    </span>
                  </td>

                </tr>

              </tbody>

            </table>

          </div>

          <div class="card-footer bg-white text-end">

            <router-link
              to="/admin/bookings"
              class="text-success text-decoration-none fw-semibold">

              View All Bookings

              <i class="bi bi-arrow-right"></i>

            </router-link>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<style scoped>

.card{
    border-radius:15px;
}

</style>