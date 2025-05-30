// Opens the modal by setting its display style to 'flex'
function openModal() {
  document.getElementById('modal_overlay').style.display = 'flex';
}

// Closes the modal by setting its display style to 'none'
function closeModal() {
  document.getElementById('modal_overlay').style.display = 'none';
}

// Enable clicking outside the modal to close it
document.addEventListener('DOMContentLoaded', () => {
  const modalOverlay = document.getElementById('modal_overlay');
  const modalBox = modalOverlay.querySelector('.modal');

  modalOverlay.addEventListener('click', (event) => {
    // Only close if clicking directly on the overlay (not inside modal box)
    if (!modalBox.contains(event.target)) {
      closeModal();
    }
  });
});

// // Toggles the visibility of the dropdown menu
// function toggleMenu() {
//   var menu = document.getElementById("dropdown_menu");
//   menu.style.display = menu.style.display === "block" ? "none" : "block";
// }

// Removes the flash message if the user clicks outside of it
function dismissFlash(event) {
  const flashes = document.querySelector('.flashes');
  if (!flashes.contains(event.target)) {
    document.getElementById('flash-overlay').remove();
  }
}

// Removes the flash overlay from the DOM if it exists
function removeFlash() {
  const overlay = document.getElementById('flash-overlay');
  if (overlay) {
    overlay.remove();
  }
}

// Automatically remove the flash overlay after 5 seconds
setTimeout(() => {
  const overlay = document.getElementById('flash-overlay');
  if (overlay) overlay.remove();
}, 5000);

/*
// Automatically resizes the font size of an element to fit within its maximum height
function autoResizeFontToHeight(id, maxFontSize = 4, minFontSize = 2.5, step = 1) {
  const el = document.getElementById(id);
  if (!el) return;

  const maxHeight = parseFloat(getComputedStyle(el).maxHeight);
  el.style.fontSize = `${maxFontSize}em`;

  // Use requestAnimationFrame to ensure layout is stable before measuring
  requestAnimationFrame(() => {
    while (el.scrollHeight > maxHeight && parseFloat(el.style.fontSize) > minFontSize) {
      const currentSize = parseFloat(el.style.fontSize);
      el.style.fontSize = `${currentSize - step}em`;
    }
  });
}
*/

// document.addEventListener("DOMContentLoaded", () => {
//   autoResizeFontToHeight("dynamic-question");
// });

/*
document.addEventListener("DOMContentLoaded", function () {
  // Adds a click animation to the lock icon when the lock button is clicked
  const lockButton = document.querySelector('button[name="action"][value="lock"]');
  const lockIcon = document.getElementById("lockIcon");

  if (lockButton && lockIcon) {
    lockButton.addEventListener("click", function () {
      // Reset animation
      lockIcon.classList.remove("animate");
      void lockIcon.offsetWidth; // Trigger reflow
      lockIcon.classList.add("animate");
    });
  }
});
*/

// Shows the win modal immediately if the element with ID "showModalTrigger" is present
document.addEventListener("DOMContentLoaded", function () {
  if (document.getElementById("showModalTrigger")) {
    const modal = document.getElementById("winModal");
    modal.style.display = "block";
  }
});

