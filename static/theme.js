document.addEventListener("DOMContentLoaded", function () {
  const toggleSwitch = document.getElementById("themeToggleSwitch");

  // Load saved theme preference
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "light") {
    document.body.classList.add("light-mode");
    toggleSwitch.checked = true;
  }

  // Toggle theme and save preference
  toggleSwitch.addEventListener("change", () => {
    if (toggleSwitch.checked) {
      document.body.classList.add("light-mode");
      localStorage.setItem("theme", "light");
    } else {
      document.body.classList.remove("light-mode");
      localStorage.setItem("theme", "dark");
    }
  });
});
    function triggerCRTFlash() {
      const flash = document.getElementById("crt-flash");

      // Remove old animation
      flash.style.animation = "none";

      // Force reflow to restart animation
      void flash.offsetWidth;

      // Apply new animation
      flash.style.animation = "crt-flash-out 0.6s ease-out";
    }