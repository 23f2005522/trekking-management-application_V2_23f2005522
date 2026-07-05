<script setup>
import { reactive } from 'vue'
import router from '@/router'
import axiosInstance from '../../utils/axioUtil'
import { useFlashStore } from '@/stores/flashStore'


const flashStore = useFlashStore()
const formData = reactive({
  email: '',
  password: '',
  role: 'trekker',
})

const handelLogin = async (e) => {
  e.preventDefault()
  try {
    const { data } = await axiosInstance.post('/auth/login', formData)
    console.log('Login successful:', data)
    // stting token in local storage
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('role', data.role)
    localStorage.setItem('username', data.username)

    // set the user in the userStore
    console.log(data)

    // Redirect based on role
    const routeMap = {
      trekker: '/trekker/dashboard',
      staff: '/staff/dashboard',
      admin: '/admin/dashboard',
    }

    router.push(routeMap[data.role] || '/')

    return data

  } catch (error) {
    flashStore.show(error?.response?.data?.message || 'Login failed', 'error')
  }
}
</script>

<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-5">
        <div class="card shadow-lg border-0 rounded-4">
          <div class="card-body p-5">
            <h2 class="text-center mb-4">Trekking Management System</h2>

            <p class="text-center text-muted mb-4">Login to continue</p>

            <form>
              <!-- Email -->
              <div class="mb-3">
                <label class="form-label"> Email </label>

                <input
                  type="email"
                  class="form-control"
                  placeholder="Enter your email"
                  v-model="formData.email"
                />
              </div>

              <!-- Password -->
              <div class="mb-4">
                <label class="form-label"> Password </label>

                <input
                  type="password"
                  class="form-control"
                  placeholder="Enter your password"
                  v-model="formData.password"
                />
              </div>

              <!-- Role -->
              <div class="mb-4">
                <label class="form-label fw-bold"> Choose your role </label>

                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="role"
                    id="trekker"
                    value="trekker"
                    v-model="formData.role"
                  />

                  <label class="form-check-label" for="trekker"> Trekker </label>
                </div>

                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="role"
                    id="staff"
                    value="staff"
                    v-model="formData.role"
                  />

                  <label class="form-check-label" for="staff"> Trek Staff </label>
                </div>

                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="role"
                    id="admin"
                    value="admin"
                    v-model="formData.role"
                  />

                  <label class="form-check-label" for="admin"> Admin </label>
                </div>
              </div>

              <!-- Login Button -->

              <button @click="handelLogin" type="submit" class="btn btn-success w-100 py-2">
                Login
              </button>
            </form>

            <hr />

            <p class="text-center mb-0">
              Don't have an account?

              <router-link to="/register"> Register Here </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  max-width: 520px;
  margin: auto;
}
</style>
