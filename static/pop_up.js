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

// Shows the win modal immediately if the element with ID "showModalTrigger" is present
document.addEventListener("DOMContentLoaded", function () {
  if (document.getElementById("showModalTrigger")) {
    const modal = document.getElementById("winModal");
    modal.style.display = "flex";
  }
});

// Opens the highscores modal by setting its display style to 'flex'
function openHighscoresModal() {
    document.getElementById('highscores_modal').style.display = 'flex';
}

// Closes the highscores modal by setting its display style to 'none'
function closeHighscoresModal() {
    document.getElementById('highscores_modal').style.display = 'none';
}

function restoreLock() {
  fetch('/restore-lock', { method: 'POST' })
    .then(res => {
      if (res.ok) location.reload();
      else alert("Could not restore a lock.");
    });
}
