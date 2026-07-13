<script setup>
import { Offcanvas } from 'bootstrap'
import logout from '../../utils/logout'
import { useRoute } from 'vue-router'
import { useFlashStore } from '@/stores/flashStore'

const route = useRoute()
const flashStore = useFlashStore()

const finishClose = (sidebar) => {
  sidebar.classList.remove('show')
  document.querySelectorAll('.offcanvas-backdrop').forEach((el) => el.remove())
  document.body.classList.remove('offcanvas-open')
  document.body.style.removeProperty('padding-right')
  document.body.style.removeProperty('overflow')
}

const closeSidebar = () => {
  const sidebar = document.getElementById('staffSidebar')
  if (!sidebar) return

  const instance = Offcanvas.getInstance(sidebar)
  if (instance) {
    sidebar.addEventListener('hidden.bs.offcanvas', () => finishClose(sidebar), { once: true })
    instance.hide()
  } else {
    finishClose(sidebar)
  }
}

const handleLogout = async () => {
  closeSidebar()
  const result = await logout()
  if (!result.success) {
    flashStore.show(result.message, 'error')
  }
  flashStore.show('Logged out successfully', 'success')
}

const paths = [
  {
    title: 'Dashboard',
    path: '/staff/dashboard',
    icon: 'bi bi-speedometer2',
  },
  {
    title: 'My Treks',
    path: '/staff/my-treks',
    icon: 'bi bi-signpost-2',
  },
  {
    title: 'Participants',
    path: '/staff/participants',
    icon: 'bi bi-people',
  },
  {
    title: 'Profile',
    path: '/staff/profile',
    icon: 'bi bi-person-circle',
  },
]
</script>

<template>
  <button 
    class="btn btn-success sidebar-toggle" 
    type="button"
    data-bs-toggle="offcanvas" 
    data-bs-target="#staffSidebar"
  >
    <i class="bi bi-list"></i>
  </button>

  <div class="offcanvas offcanvas-start text-bg-success py-4" tabindex="-1" id="staffSidebar">
    <div class="offcanvas-header border-bottom">
      <h5 class="offcanvas-title">
        <i class="bi bi-mountains me-2"></i>
        TrekMaster Staff
      </h5>
      <button class="btn-close btn-close-white" data-bs-dismiss="offcanvas"></button>
    </div>

    <div class="offcanvas-body d-flex flex-column p-0">
      <ul class="nav nav-pills flex-column p-3 flex-grow-1">
        <li v-for="item in paths" :key="item.path" class="nav-item mb-2">
          <router-link 
            :to="item.path" 
            class="nav-link"
            :class="route.path === item.path ? 'bg-white text-success fw-bold active-glow' : 'text-white'"
            @click="closeSidebar"
          >
            <i :class="[item.icon, 'me-2']"></i>
            {{ item.title }}
          </router-link>
        </li>

        <li class="nav-item mt-auto pt-3 border-top">
          <div @click="handleLogout" class="nav-link text-danger logout-btn">
            <i class="bi bi-box-arrow-right me-2"></i>
            Logout
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.sidebar-toggle {
  margin: 1rem 0.25rem;
  padding: 0.5rem 0.65rem;
}

.nav-link {
  transition: all 0.2s ease;
}

.nav-link:not(.bg-white):hover {
  background: rgba(255, 255, 255, 0.15);
  color: white !important;
}

.active-glow {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.logout-btn {
  cursor: pointer;
}

.logout-btn:hover {
  background: rgba(220, 53, 69, 0.1);
}
</style>
