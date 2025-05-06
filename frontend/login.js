const users = [
  { name: "John Doe", email: "j@g.com", password: "j2", number: "07063569494" },
  { name: "Amina Yusuf", email: "amina@gmail.com", password: "amina456" },
  { name: "Chidi Okoro", email: "chidi@agroscan.com", password: "chidi789" },
  { name: "Fatima Bello", email: "fatima@agroscan.com", password: "fatima321" },
  { name: "Ibrahim Musa", email: "ibrahim@agroscan.com", password: "ibrahim654" },
  { name: "Sadiq Teslim", email: "sadiqadetola08@gmail.com", password: "Bamidele@08" },

];
function login(event) {
  event.preventDefault(); // Prevent form submission
  const email = document.getElementById("email").value.trim().toLowerCase();
  const password = document.getElementById("password").value.trim();
  const number = document.getElementById("number").value.trim();
  const user = users.find(u => u.email.toLowerCase() === email && u.password === password);

  const status = document.getElementById("login-status");

  if (user) {
    status.textContent = `Welcome, ${user.name}!`;
    status.className = "text-green-600";
    
    // Simulate a session or redirect
    localStorage.setItem("agroscanUser", JSON.stringify(user));
    // window.location.href = "dashboard.html";
    localStorage.setItem('isGuest', 'false')
    window.location.href = "diagnosis.html";
  } else {
    status.textContent = "❌ Invalid email or password";
    status.className = "text-red-600";
  }
}