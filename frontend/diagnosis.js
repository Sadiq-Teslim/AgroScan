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

// Guest Mode Handling
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
  
  // Setup form submission handler
  document.getElementById('diagnoseForm').addEventListener('submit', async function(e) {
      e.preventDefault();
      
      const fileInput = document.getElementById('imageInput');
      if (!fileInput.files[0]) {
          showMessage('Please select an image first', 'error');
          return;
      }
      
      const formData = new FormData();
      formData.append('file', fileInput.files[0]);
      
      // Show loading state
      document.getElementById('result').innerHTML = '<p>Analyzing image...</p>';
      
      try {
          const response = await fetch('http://localhost:8080/api/diagnose', {
              method: 'POST',
              body: formData
          });
          
          const data = await response.json();
          
          if (data.error) {
              showMessage(data.error, 'error');
              return;
          }
          
          // Display results
          displayResults(data);
          
          // Save to history if user is logged in
          if (localStorage.getItem('user')) {
              saveToHistory(data, fileInput.files[0]);
          }
      } catch (error) {
          showMessage('Error connecting to the server. Please try again.', 'error');
      }
  });
})

// Create Lucide Icons
lucide.createIcons()

// Camera functionality
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

// Display diagnosis results
function displayResults(data) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <div class="bg-white p-4 rounded-lg shadow">
            <h2 class="text-xl font-bold text-green-700">Diagnosis Results</h2>
            <p class="mt-2"><strong>Identified Condition:</strong> ${data.class.replace(/_/g, ' ')}</p>
            <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%</p>
            <div class="mt-4">
                <h3 class="font-bold">Recommended Actions:</h3>
                <ul class="list-disc pl-5 mt-2">
                    ${getRecommendations(data.class)}
                </ul>
            </div>
        </div>
    `;
}

// Get disease-specific recommendations
function getRecommendations(condition) {
    // Map conditions to recommendations
    const recommendations = {
        "Pepper_bell_Bacterial_spot": "<li>Apply copper-based fungicides</li><li>Ensure proper spacing between plants</li><li>Remove infected leaves</li>",
        "Pepper_bell_healthy": "<li>Continue current care practices</li><li>Monitor regularly for signs of disease</li>",
        "Potato_Early_blight": "<li>Remove infected leaves</li><li>Apply fungicides containing chlorothalonil</li><li>Ensure good air circulation</li>",
        "Potato_Late_blight": "<li>Remove infected plants immediately</li><li>Apply copper-based fungicides</li><li>Avoid overhead irrigation</li>",
        "Potato_healthy": "<li>Continue current care practices</li><li>Monitor regularly for signs of disease</li>",
        "Tomato_Bacterial_spot": "<li>Remove infected leaves</li><li>Apply copper-based bactericides</li><li>Avoid overhead watering</li>",
        "Tomato_Early_blight": "<li>Remove lower infected leaves</li><li>Apply fungicides</li><li>Mulch around plants</li>",
        "Tomato_Late_blight": "<li>Remove infected plants immediately</li><li>Apply fungicides</li><li>Improve air circulation</li>",
        "Tomato_healthy": "<li>Continue current care practices</li><li>Monitor regularly for signs of disease</li>"
    };
    
    return recommendations[condition] || "<li>Consult with a local agricultural expert</li>";
}

// Show notification messages
function showMessage(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = type === 'error' 
        ? 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative' 
        : 'bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative';
    alertDiv.innerHTML = message;
    
    const container = document.querySelector('main');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Save diagnosis to history
function saveToHistory(data, imageFile) {
    // Convert image to data URL for storage
    const reader = new FileReader();
    reader.onload = function(e) {
        const history = JSON.parse(localStorage.getItem('diagnosisHistory') || '[]');
        history.push({
            date: new Date().toISOString(),
            class: data.class,
            confidence: data.confidence,
            imageUrl: e.target.result
        });
        localStorage.setItem('diagnosisHistory', JSON.stringify(history));
    };
    reader.readAsDataURL(imageFile);
}