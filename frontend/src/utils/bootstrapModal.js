import { Modal } from 'bootstrap'

export const cleanupModalArtifacts = () => {
  document.querySelectorAll('.modal-backdrop').forEach((backdrop) => backdrop.remove())
  document.body.classList.remove('modal-open')
  document.body.style.removeProperty('padding-right')
}

export const hideBootstrapModal = (modalId) => {
  const modalElement = document.getElementById(modalId)
  if (!modalElement) {
    cleanupModalArtifacts()
    return
  }

  const modalInstance = Modal.getOrCreateInstance(modalElement)
  modalInstance.hide()

  window.setTimeout(() => {
    cleanupModalArtifacts()
  }, 200)
}

export const registerModalCleanup = (modalId) => {
  const modalElement = document.getElementById(modalId)
  if (!modalElement) return () => {}

  const handleHidden = () => cleanupModalArtifacts()
  modalElement.addEventListener('hidden.bs.modal', handleHidden)

  return () => {
    modalElement.removeEventListener('hidden.bs.modal', handleHidden)
  }
}