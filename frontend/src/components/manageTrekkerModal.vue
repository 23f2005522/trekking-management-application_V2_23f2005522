<script setup>
import { ref, watch } from 'vue'
import { userTrekkerStore } from '@/stores/admin/trekkerStore'

const trekkerStore = userTrekkerStore()

const selectedStatus = ref(true)
const reason = ref('')

watch(
  () => trekkerStore.selectedTrekker,
  (trekker) => {
    if (!trekker) {
      selectedStatus.value = true
      reason.value = ''
      return
    }

    selectedStatus.value = trekker.is_active
    reason.value = trekker.blacklisted_reason || ''
  },
  { immediate: true }
)



</script>

<template>
  <div
    class="modal fade"
    id="manageTrekkerModal"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">

      <div class="modal-content">

        <!-- Header -->
        <div class="modal-header bg-success text-white">

          <h5 class="modal-title">
            Manage Trekker
          </h5>

          <button
            class="btn-close btn-close-white"
            data-bs-dismiss="modal"
          ></button>

        </div>

        <!-- Body -->
        <div
          class="modal-body"
          v-if="trekkerStore.selectedTrekker"
        >

          <div class="card bg-light mb-4">

            <div class="card-body">

              <h5>{{ trekkerStore.selectedTrekker.username }}</h5>

              <p class="text-muted mb-2">
                {{ trekkerStore.selectedTrekker.email }}
              </p>

              <span
                class="badge"
                :class="{
                  'bg-success': trekkerStore.selectedTrekker.is_active,
                  'bg-danger': !trekkerStore.selectedTrekker.is_active
                }"
              >
                Current :
                {{ trekkerStore.selectedTrekker.is_active ? 'Active' : 'Deactivated' }}
              </span>

            </div>

          </div>

          <!-- Status -->

          <label class="fw-semibold mb-2">
            Account Status
          </label>

          <div class="form-check">

            <input
              class="form-check-input"
              type="radio"
              :value="'deblacklist'"
              v-model="selectedStatus"
            >

            <label class="form-check-label text-success">
              Activate
            </label>

          </div>

          <div class="form-check mb-4">

            <input
              class="form-check-input"
              type="radio"
              :value="'blacklist'"
              v-model="selectedStatus"
            >

            <label class="form-check-label text-danger">
              Blacklist
            </label>

          </div>

          <!-- Reason -->

          <label class="fw-semibold">
            Reason (Optional)
          </label>

          <textarea
            rows="4"
            class="form-control"
            v-model="reason"
            placeholder="Reason for deactivation..."
          ></textarea>

        </div>

        <div
          v-else
          class="modal-body text-center"
        >
          Loading...
        </div>

        <!-- Footer -->

        <div class="modal-footer">

          <button
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>

          <button
            class="btn btn-success"
            @click="
              trekkerStore.handleEditTrekker(
                trekkerStore.selectedTrekker.user_id,
                selectedStatus,
                reason
              )
            "
          >
            Save Changes
          </button>

        </div>

      </div>

    </div>
  </div>
</template>