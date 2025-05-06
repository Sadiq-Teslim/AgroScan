document.getElementById("signup-form").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const username = document.getElementById("signup-username").value.trim();
    const email = document.getElementById("signup-email").value.trim();
    const password = document.getElementById("signup-password").value.trim();
    const confirm_password = document.getElementById("confirm-password").value.trim();
    const status = document.getElementById("signup-status");
  
    if (!isPasswordStrong(password)) {
      status.textContent = "❌ Password must be 8+ chars, include a number and uppercase letter.";
      status.className = "text-red-600";
      return;
    }
    
    if (password != confirm_password) {
      status.textContent = "❌ Both passwords do not match!";
      return;
    }
  
    try {
        const response = await fetch(signupUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
          },
          body: JSON.stringify({ username, email, password })
        });
    
        const data = await response.json();
        if (response.ok) {
          status.textContent = "✅ Registration successful.";
          status.className = "text-green-600";
          window.location.href = "{% url 'home' %}"
        } else {
          status.textContent = `❌ ${data.error || "Sign up failed."}`;
          status.className = "text-red-600";
        }
      } catch (err) {
        console.error(err);
        status.textContent = "❌ Error during sign up.";
        status.className = "text-red-600";
      }
});