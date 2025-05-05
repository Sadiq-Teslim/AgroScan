const toggleBtn = document.getElementById("toggleBtn");
    const sidebar = document.getElementById("sidebar");
    const closeBtn = document.getElementById("closeSidebar");

    toggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("-translate-x-full");
    });

    closeBtn.addEventListener("click", () => {
      sidebar.classList.add("-translate-x-full");
    });
    lucide.createIcons();

    function logout() {
      window.location.href = "login.html";
    }