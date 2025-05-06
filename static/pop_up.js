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
function toggleMenu() {
  var menu = document.getElementById("dropdown_menu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}
function dismissFlash(event) {
  const flashes = document.querySelector('.flashes');
  if (!flashes.contains(event.target)) {
  document.getElementById('flash-overlay').remove();
  }
}
function removeFlash() {
  const overlay = document.getElementById('flash-overlay');
  if (overlay) {
      overlay.remove();
  }
}
setTimeout(() => {
  const overlay = document.getElementById('flash-overlay');
  if (overlay) overlay.remove();
}, 5000);