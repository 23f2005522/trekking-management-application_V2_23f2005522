<script setup>
import logout from '../../../utils/logout'
</script>

<template>
  <!-- Toggle Button -->

  <button class="btn btn-success m-3" data-bs-toggle="offcanvas" data-bs-target="#adminSidebar">
    <i class="bi bi-list"></i>
  </button>

  <!-- Sidebar -->

  <div class="offcanvas offcanvas-start text-bg-success py-4" id="adminSidebar">
    <div class="offcanvas-header border-bottom">
      <h5 class="offcanvas-title">
        <i class="bi bi-mountains me-2"></i>

        TrekMaster
      </h5>

      <button class="btn-close btn-close-white" data-bs-dismiss="offcanvas"></button>
    </div>

    <div class="offcanvas-body d-flex flex-column p-0">
      <ul class="nav nav-pills flex-column p-3 flex-grow-1">
        <li class="nav-item mb-2">
          <router-link to="/admin/dashboard" class="nav-link text-white">
            <i class="bi bi-speedometer2 me-2"></i>

            Dashboard
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link to="/admin/treks" class="nav-link text-white">
            <i class="bi bi-signpost-2 me-2"></i>

            Treks
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link to="/admin/staff" class="nav-link text-white">
            <i class="bi bi-person-workspace me-2"></i>

            Manage Staff
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link to="/admin/users" class="nav-link text-white">
            <i class="bi bi-people me-2"></i>

            Manage Users
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link to="/admin/bookings" class="nav-link text-white">
            <i class="bi bi-calendar-check me-2"></i>

            Bookings
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link to="/admin/search" class="nav-link text-white">
            <i class="bi bi-search me-2"></i>

            Search
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link to="/admin/reports" class="nav-link text-white">
            <i class="bi bi-bar-chart me-2"></i>

            Reports
          </router-link>
        </li>

        <li class="nav-item mb-2">
          <router-link to="/admin/settings" class="nav-link text-white">
            <i class="bi bi-gear me-2"></i>

            Settings
          </router-link>
        </li>

        <li class="nav-item mt-auto pt-3 border-top">
          <div @click="logout" class="nav-link text-danger">
            <i class="bi bi-box-arrow-right me-2"></i>

            Logout
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>


<style scoped>
.nav-link {
  color: white;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background: rgba(255,255,255,.15);
  color: white;
}

.nav-link.router-link-active {
  background: white;
  color: #198754 !important;
  font-weight: 600;
}
</style>