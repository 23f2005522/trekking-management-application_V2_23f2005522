<script setup>
</script>

<template>
  <div class="col p-4">

    <!-- Heading -->
    <div class="d-flex justify-content-between align-items-center mb-4">

      <div>
        <h1 class="fw-bold">Manage Treks</h1>

        <p class="text-muted mb-0">
          View, create and manage trekking events.
        </p>
      </div>

      <button class="btn btn-success d-flex align-items-center">
        <i class="bi bi-plus-lg me-2"></i>
        Add New Trek
      </button>

    </div>

    <!-- Search -->

    <div class="card shadow-sm mb-4">

      <div class="card-body">

        <div class="input-group">

          <input
            type="text"
            class="form-control"
            placeholder="Search treks..."
          />

          <button class="btn btn-outline-secondary">

            <i class="bi bi-search"></i>

          </button>

        </div>

      </div>

    </div>

    <!-- Treks Table -->

    <div class="card shadow-sm">

      <div class="table-responsive">

        <table class="table table-hover align-middle mb-0">

          <thead class="table-light">

            <tr>

              <th>ID</th>
              <th>Trek Name</th>
              <th>Location</th>
              <th>Difficulty</th>
              <th>Slots</th>
              <th>Status</th>
              <th>Actions</th>

            </tr>

          </thead>

          <tbody>

            <tr>

              <td>1</td>
              <td>Everest Base Camp</td>
              <td>Nepal</td>
              <td>Hard</td>
              <td>10</td>

              <td>

                <span class="badge bg-success">
                  Open
                </span>

              </td>

              <td>

                <button class="btn btn-outline-primary btn-sm me-2">

                  <i class="bi bi-pencil"></i>

                </button>

                <button class="btn btn-outline-danger btn-sm">

                  <i class="bi bi-trash"></i>

                </button>

              </td>

            </tr>

            <tr>

              <td>2</td>
              <td>Kedarkantha Trek</td>
              <td>Uttarakhand</td>
              <td>Easy</td>
              <td>15</td>

              <td>

                <span class="badge bg-success">
                  Open
                </span>

              </td>

              <td>

                <button class="btn btn-outline-primary btn-sm me-2">

                  <i class="bi bi-pencil"></i>

                </button>

                <button class="btn btn-outline-danger btn-sm">

                  <i class="bi bi-trash"></i>

                </button>

              </td>

            </tr>

            <tr>

              <td>3</td>
              <td>Hampta Pass</td>
              <td>Himachal Pradesh</td>
              <td>Moderate</td>
              <td>8</td>

              <td>

                <span class="badge bg-success">
                  Open
                </span>

              </td>

              <td>

                <button class="btn btn-outline-primary btn-sm me-2">

                  <i class="bi bi-pencil"></i>

                </button>

                <button class="btn btn-outline-danger btn-sm">

                  <i class="bi bi-trash"></i>

                </button>

              </td>

            </tr>

            <tr>

              <td>4</td>
              <td>Valley of Flowers</td>
              <td>Uttarakhand</td>
              <td>Easy</td>
              <td>20</td>

              <td>

                <span class="badge bg-danger">
                  Closed
                </span>

              </td>

              <td>

                <button class="btn btn-outline-primary btn-sm me-2">

                  <i class="bi bi-pencil"></i>

                </button>

                <button class="btn btn-outline-danger btn-sm">

                  <i class="bi bi-trash"></i>

                </button>

              </td>

            </tr>

            <tr>

              <td>5</td>
              <td>Roopkund Trek</td>
              <td>Uttarakhand</td>
              <td>Moderate</td>
              <td>12</td>

              <td>

                <span class="badge bg-success">
                  Open
                </span>

              </td>

              <td>

                <button class="btn btn-outline-primary btn-sm me-2">

                  <i class="bi bi-pencil"></i>

                </button>

                <button class="btn btn-outline-danger btn-sm">

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