function initialLogin() {
  const loginBtn = document.getElementById('loginBtn')
  window.location.href = 'login.html';
}

// Function to check if the user is a guest
    // Trigger modal when "Try It Now" is clicked
    document.getElementById('tryNowBtn').addEventListener('click', () => {
    document.getElementById('authModal').classList.remove('hidden');
  });

  // Continue as guest
  document.getElementById('guestBtn').addEventListener('click', () => {
    document.getElementById('authModal').classList.add('hidden');
    // window.location.href = 'diagnosis.html'; // or wherever you want to send them
  });

  // Redirect to sign up
  document.getElementById('signInBtn').addEventListener('click', () => {
    window.location.href = 'signup.html'; // change to your actual signup page
  });
  
  function redirectToDiagnosis() {
  // Close the SMS modal
  document.getElementById('smsModal').classList.add('hidden');
  // Redirect
  window.location.href = 'diagnosis.html';
  localStorage.setItem('isGuest', 'true')
}
function redirectToSignUp() {
  // Close the SMS modal
  document.getElementById('smsModal').classList.add('hidden');
  // Redirect
  window.location.href = 'signup.html';
}
  function showSMSModal() {
    document.getElementById('smsModal').classList.remove('hidden');
  }

  function closeSMSModal() {
    document.getElementById('smsModal').classList.add('hidden');
  }

  // document.getElementById("guestBtn").addEventListener("click", function () {
  //   localStorage.setItem("isGuest", "true");
  //   // Open the next modal OR redirect after user confirms
  // });

  // document.getElementById("signInBtn").addEventListener("click", function () {
  //   localStorage.setItem("isGuest", "false");
  //   // Redirect to sign in page
  // });
