<template>
  <!-- Toggle -->

  <button
    class="btn btn-success m-3"
    type="button"
    data-bs-toggle="offcanvas"
    data-bs-target="#trekkerSidebar"
  >
    <i class="bi bi-list"></i>
  </button>

  <!-- Sidebar -->

  <div class="offcanvas offcanvas-start text-bg-success py-4" tabindex="-1" id="trekkerSidebar">
    <div class="offcanvas-header border-bottom">
      <h5 class="offcanvas-title">
        <i class="bi bi-mountains me-2"></i>

        TrekMaster
      </h5>

      <button class="btn-close btn-close-white" data-bs-dismiss="offcanvas"></button>
    </div>

    <div class="offcanvas-body d-flex flex-column p-0">
      <ul class="nav nav-pills flex-column p-3 flex-grow-1">
        <li v-for="item in paths" :key="item.path" class="nav-item mb-2">
          <router-link
            :to="item.path"
            class="nav-link"
            :class="route.path === item.path ? 'bg-white text-success hover' : 'text-white'"
            
          >
            <i :class="[item.icon, 'me-2']"></i>
            {{ item.title }}
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

<script setup>
import logout from '@/utils/logout'
import { useRoute } from 'vue-router'

const route = useRoute()

const paths = [
  {
    title: 'Dashboard',
    path: '/trekker/dashboard',
    icon: 'bi bi-speedometer2',
  },
  {
    title: 'Browse Treks',
    path: '/trekker/treks',
    icon: 'bi bi-signpost-2',
  },
  {
    title: 'My Bookings',
    path: '/trekker/bookings',
    icon: 'bi bi-calendar-check',
  },
  {
    title: 'History',
    path: '/trekker/history',
    icon: 'bi bi-clock-history',
  },
  {
    title: 'Profile',
    path: '/trekker/profile',
    icon: 'bi bi-person-circle',
  },
]
</script>
