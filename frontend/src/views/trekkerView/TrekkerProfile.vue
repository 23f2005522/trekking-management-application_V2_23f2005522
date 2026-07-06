<template>
  <div>
    <h2 class="fw-bold mb-4">Profile</h2>

    <div class="card shadow-sm">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-6">
            <label class="form-label">Username</label>
            <input type="text" class="form-control" value="Amit Sharma" />
          </div>

          <div class="col-md-6">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" value="amit@example.com" />
          </div>

          <div class="col-md-6">
            <label class="form-label">Phone</label>
            <input type="text" class="form-control" value="9876543210" />
          </div>

          <div class="col-md-6">
            <label class="form-label">Role</label>
            <input type="text" class="form-control" value="Trekker" disabled />
          </div>

          <div class="col-12">
            <button class="btn btn-success">Save Profile</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
