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

// function autoResizeFontToHeight(id, maxFontSize = 4, minFontSize = 2.5, step = 1) {
//   const el = document.getElementById(id);
//   if (!el) return;

//   const maxHeight = parseFloat(getComputedStyle(el).maxHeight);
//   el.style.fontSize = `${maxFontSize}em`;

//   // Use requestAnimationFrame to ensure layout is stable
//   requestAnimationFrame(() => {
//     while (el.scrollHeight > maxHeight && parseFloat(el.style.fontSize) > minFontSize) {
//       const currentSize = parseFloat(el.style.fontSize);
//       el.style.fontSize = `${currentSize - step}em`;
//     }
//   });
// }

document.addEventListener("DOMContentLoaded", () => {
  autoResizeFontToHeight("dynamic-question");

});

document.addEventListener("DOMContentLoaded", function () {
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

document.addEventListener('DOMContentLoaded', () => {
  const timeline = document.getElementById('timeline');
  const palette = document.getElementById('palette');

  Sortable.create(palette, {
    group: { name: 'shared', pull: 'clone', put: false },
    sort: false,
    animation: 150,
  });

  Sortable.create(timeline, {
    group: { name: 'shared', pull: false, put: true },
    animation: 150,
    onAdd(evt) {
      const el = evt.item;
      const questionId = el.getAttribute('data-qid');
      const date = el.getAttribute('data-date');
      const siblings = Array.from(timeline.children).map(e => e.getAttribute('data-qid'));

      fetch('/validate_drop', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question_id: questionId, timeline: siblings })
      })
      .then(res => res.json())
      .then(data => {
        if (!data.valid) {
          alert("Invalid placement! Unlocks cleared.");
          window.location.reload();
        } else {
          el.classList.remove('new');
          el.classList.add('correct');
          const yearElement = document.createElement('p');
          yearElement.className = 'date';
          yearElement.innerHTML = `<strong>${date}</strong>`;
          el.prepend(yearElement);

          if (data.win) {
            document.getElementById("winModal").style.display = "flex"; 
          } else {
            alert("Correct placement! Loading next question...");
            window.location.reload();
          }
        }
      });
    }
  });
});
