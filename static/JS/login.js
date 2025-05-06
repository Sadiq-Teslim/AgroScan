document.getElementById("login-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("login-username").value.trim();
  const password = document.getElementById("login-password").value.trim();
  const status = document.getElementById("login-status");

  try {
    const response = await fetch(loginUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (response.ok) {
      status.textContent = `✅ ${data.success}`;
      status.className = "text-green-600";
      localStorage.setItem("agroscanUser", JSON.stringify(data));
      window.location.href = "{% url 'home' %}";
    } else {
      status.textContent = `❌ ${data.error || "Login failed."}`;
      status.className = "text-red-600";
    }
  } catch (err) {
    console.error(err);
    status.textContent = "❌ Error during login.";
    status.className = "text-red-600";
  }
});