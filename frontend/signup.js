// Initialize or fetch existing users array from localStorage
  const users = JSON.parse(localStorage.getItem("agroscanUsers")) || [
    { name: "John Doe", email: "j@g.com", password: "j2" },
    { name: "Amina Yusuf", email: "amina@agroscan.com", password: "amina456" },
    { name: "Chidi Okoro", email: "chidi@agroscan.com", password: "chidi789" },
    { name: "Fatima Bello", email: "fatima@agroscan.com", password: "fatima321" },
    { name: "Ibrahim Musa", email: "ibrahim@agroscan.com", password: "ibrahim654" }
  ];

  // Handle form submission
  document.getElementById("signupForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim().toLowerCase();
    const password = document.getElementById("password").value;

    // Check if user already exists
    const exists = users.some(u => u.email === email);
    if (exists) {
      alert("🚫 An account with this email already exists.");
      return;
    }

    // Add the new user to the array
    const newUser = { name, email, password };
    users.push(newUser);

    // Save updated user array to localStorage
    localStorage.setItem("agroscanUsers", JSON.stringify(users));
    localStorage.setItem("agroscanUser", JSON.stringify(newUser)); // Log them in

    // Redirect to diagnosis or login
    alert("✅ Account created successfully!");
    window.location.href = "diagnosis.html";
  });

