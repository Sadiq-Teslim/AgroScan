// Toggle Script
const toggleBtn = document.getElementById('toggleBtn')
const sidebar = document.getElementById('sidebar')
const closeBtn = document.getElementById('closeSidebar')

const mainContentWrapper = document.getElementById('mainContentWrapper');

toggleBtn.addEventListener('click', () => {
  sidebar.classList.toggle('-translate-x-full')
  mainContentWrapper.classList.add('flex', 'flex-1')
})

closeBtn.addEventListener('click', () => {
  sidebar.classList.add('-translate-x-full')
})
window.addEventListener('DOMContentLoaded', () => {
  const isGuest = localStorage.getItem('isGuest')

  if (isGuest === 'true') {
    // Hide sidebar
    const sidebar = document.getElementById('sidebar')
    if (sidebar) sidebar.style.display = 'none'
    // Make the footer fixed
    const footer = document.getElementById('footer')
    if (footer) footer.classList.add('ml-0', 'bottom-0', 'w-full')
    // Hide Menu Button
    const toggleBtn = document.getElementById('toggleBtn')
    if (toggleBtn) toggleBtn.style.display = 'none'
    // Adjust body layout
    const body = document.body
    if (body) body.classList.remove('flex')
    if (body) body.classList.add('flex-col')
    // Optional: adjust main content width to full if sidebar is gone
    const mainContent = document.getElementById('mainContent')
    if (mainContent) mainContent.classList.remove('ml-64') // Tailwind class if used
  }

  if (isGuest === 'false') {
    // Show sidebar
    const sidebar = document.getElementById('sidebar')
    if (sidebar) sidebar.style.display = 'block'
    // Show Menu Button
    const toggleBtn = document.getElementById('toggleBtn')
    if (toggleBtn) toggleBtn.style.display = 'block'
    // Adjust body layout
    // const body = document.body;
    // if (body) body.classList.remove("flex-col");
    // if (body) body.classList.add("flex");
    // Hide guest content
    const guestContent = document.getElementById('guestContent')
    if (guestContent) guestContent.style.display = 'none'
  }
})

lucide.createIcons()
function openCamera () {
  const videoElement = document.createElement('video')
  const canvasElement = document.createElement('canvas')
  const context = canvasElement.getContext('2d')

  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then(stream => {
      videoElement.srcObject = stream
      videoElement.play()

      const captureButton = document.createElement('button')
      captureButton.textContent = 'Capture'
      captureButton.className =
        'bg-green-600 text-white px-4 py-2 rounded-lg mt-4'

      document.body.appendChild(videoElement)
      document.body.appendChild(captureButton)

      captureButton.addEventListener('click', () => {
        canvasElement.width = videoElement.videoWidth
        canvasElement.height = videoElement.videoHeight
        context.drawImage(videoElement, 0, 0)
        const imageData = canvasElement.toDataURL('image/png')

        // Stop the video stream
        stream.getTracks().forEach(track => track.stop())

        // Remove video and button elements
        videoElement.remove()
        captureButton.remove()

        // Replace "no file chosen" with the image
        const fileInputLabel = document.querySelector('label[for="fileInput"]')
        if (fileInputLabel) {
          const imgPreview = document.createElement('img')
          imgPreview.src = imageData
          imgPreview.alt = 'Captured Image'
          imgPreview.className = 'w-32 h-32 object-cover mt-4'
          
          // Clear existing content and append the image
          fileInputLabel.innerHTML = ''
          fileInputLabel.appendChild(imgPreview)
        }

        // You can now use the captured image data
        console.log(imageData)
      })
    })
    .catch(error => {
      console.error('Error accessing the camera:', error)
    })
}

const mainContentWrapper = document.getElementById('mainContentWrapper');
// if (toggleBtn && sidebar && mainContentWrapper) {
//   toggleBtn.addEventListener('click', () => {
//     if (sidebar.classList.contains('-translate-x-full')) {
//       mainContentWrapper.classList.add('flex', 'flex-1')
//     } else {
//       mainContentWrapper.classList.remove('flex', 'flex-1')
//     }
//   })
// }