function openModal() {
  document.getElementById('modalOverlay').style.display = 'flex';
}

function closeModal() {
  document.getElementById('modalOverlay').style.display = 'none';
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

function autoResizeFontToHeight(id, maxFontSize = 4, minFontSize = 2.5, step = 1) {
  const el = document.getElementById(id);
  if (!el) return;

  const maxHeight = parseFloat(getComputedStyle(el).maxHeight);
  el.style.fontSize = `${maxFontSize}em`;

  // Use requestAnimationFrame to ensure layout is stable
  requestAnimationFrame(() => {
    while (el.scrollHeight > maxHeight && parseFloat(el.style.fontSize) > minFontSize) {
      const currentSize = parseFloat(el.style.fontSize);
      el.style.fontSize = `${currentSize - step}em`;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  autoResizeFontToHeight("dynamic-question");
});