
import axiosInstance from '@/utils/axioUtil'
import LoginView from '@/views/authView/loginView.vue'
import RegisterView from '@/views/authView/registerView.vue'
import HomeView from '@/views/homeview/homeView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const approuter = {
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Home route
    {
      path: '/',
      name: 'home',
      component: HomeView
    },

    // Authentication routes
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },

    // Admin route
    {
      path: '/admin',
      name: 'admin',
      component: () => import("@/views/adminView/adminView.vue"),
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        {
          path: 'dashboard',
          name: 'admindashboard',
          component: () => import("@/views/adminView/adminDashboardView.vue")
        }
        , 
        {
          path : "treks" , 
          name : "manageTreks" ,
          component: () => import("@/views/adminView/manageTrek.vue")
        }
        , 
        {
          path : "staff" ,
          name : "manageStaff" ,
          component: () => import("@/views/adminView/manageStaff.vue")
        }
        ,
        {
          path : "trekkers" ,
          name : "manageTrekkers" ,
          component: () => import("@/views/adminView/manageTrekkers.vue")
        }
        ,

      ]
    },


    // Staff route
    {
      path : '/staff/dashboard',
      name : 'staffdashboard',
      component : () => import("@/views/staffView/StaffView.vue"),
      meta: { requiresAuth: true, role: 'staff' }
    },


    // Trekker route
    {
      path : '/trekker/dashboard',
      name : 'trekkerdashboard',
      component : () => import("@/views/trekkerView/TrekkerView.vue"),
      meta: { requiresAuth: true, role: 'trekker' }
    },






    // wiledcard route for 404 Not Found
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import("@/views/404/notFoundView.vue")
    }

  ],
}
const router = createRouter(approuter)

// prototected routes
router.beforeEach(async (to) => {

    const token = localStorage.getItem("access_token")
    const role = localStorage.getItem("role")

    if (to.meta.requiresAuth && !token) {
        return { name: "login" }
    }

    if (token) {
        try {
            await axiosInstance.get("/auth/authme")
        } catch {
            localStorage.clear()
            return { name: "login" }
        }
    }

    if (to.meta.requiresAuth && role !== to.meta.role) {
        return { name: "login" }
    }

    return true
})

export default router
