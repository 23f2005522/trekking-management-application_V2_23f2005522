<script setup>
import { reactive } from 'vue'
import axiosInstance from '../../utils/axioUtil'
import { useFlashStore } from '@/stores/flashStore'
import router from '@/router'

const flashStore = useFlashStore()

const formData = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  role: 'trekker',
})

const handelRegister = async () => {
  try {
    if (formData.password !== formData.confirmPassword) {
      flashStore.show('Passwords do not match. Please try again.', 'error')
      return
    }

    const { data } = await axiosInstance.post('/auth/register', formData)
    console.log('Registration successful:', data)
    flashStore.show(data?.message || 'Registration successful! Please login.', 'success')
    router.push('/login')
  } catch (error) {
    
    flashStore.show(
      error.response?.data?.message || 'Registration failed. Please try again.',
      'error',
    )
    // console.error('Registration failed:', error)
  }
}
</script>

<template>
  <div class="container py-3">
    <div class="row justify-content-center">
      <div class="col-md-7 col-lg-6">
        <div class="card shadow-lg border-0 rounded-4">
          <div class="card-body p-5">
            <h2 class="text-center mb-2">Trekking Management System</h2>

            <p class="text-center text-muted mb-4">Create a trekker account</p>

            <form @submit.prevent="handelRegister">
              <!-- Username -->
              <div class="mb-3">
                <label class="form-label"> Username </label>

                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter your username"
                  v-model="formData.username"
                />
              </div>

              <!-- Email -->
              <div class="mb-3">
                <label class="form-label"> Email Address </label>

                <input
                  type="email"
                  class="form-control"
                  placeholder="Enter your email"
                  v-model="formData.email"
                />
              </div>

              <!-- Phone -->
              <div class="mb-3">
                <label class="form-label"> Phone Number </label>

                <input
                  type="tel"
                  class="form-control"
                  placeholder="Enter your phone number"
                  v-model="formData.phone"
                />
              </div>

              <!-- Password -->
              <div class="mb-3">
                <label class="form-label"> Password </label>

                <input
                  type="password"
                  class="form-control"
                  placeholder="Enter your password"
                  v-model="formData.password"
                />
              </div>

              <!-- Confirm Password -->
              <div class="mb-4">
                <label class="form-label"> Confirm Password </label>

                <input
                  type="password"
                  class="form-control"
                  placeholder="Re-enter your password"
                  v-model="formData.confirmPassword"
                />
              </div>

              <!-- Register Button -->
              <button type="submit" class="btn btn-success w-100 py-2">
                Register
              </button>
            </form>

            <hr />

            <p class="text-center mb-0">
              Already have an account?

              <router-link to="/login"> Login Here </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  max-width: 600px;
  margin: auto;
}
</style>
