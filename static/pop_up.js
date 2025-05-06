function openPopup() {
    document.getElementById('myModal').style.display = 'block';
  }

  function closePopup() {
    document.getElementById('myModal').style.display = 'none';
  }

  function toggleMenu() {
    var menu = document.getElementById("dropdown_menu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}