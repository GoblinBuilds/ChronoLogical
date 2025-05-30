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
