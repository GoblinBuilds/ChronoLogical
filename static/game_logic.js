

// Enables drag-and-drop functionality using Sortable.js
document.addEventListener('DOMContentLoaded', () => {
  const timeline = document.getElementById('timeline');
  const palette = document.getElementById('palette');

  // Set up the palette as a source of draggable elements
  Sortable.create(palette, {
    group: { name: 'shared', pull: 'clone', put: false },
    sort: false,
    animation: 150,
  });

  // Set up the timeline to accept drops from the palette
  Sortable.create(timeline, {
    group: { name: 'shared', pull: false, put: true },
    animation: 150,
    onAdd(evt) {
      const el = evt.item;
      const questionId = el.getAttribute('data-qid');
      const date = el.getAttribute('data-date');
      const siblings = Array.from(timeline.children).map(e => e.getAttribute('data-qid'));

      // Validate the drop with the server
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
            // Show date and update element class
            el.classList.remove('new');
            el.classList.add('correct');
            const yearElement = document.createElement('p');
            yearElement.className = 'date';
            yearElement.innerHTML = `<strong>${date}</strong>`;
            el.prepend(yearElement);

            // Show win modal or reload based on result
            if (data.win) {
              document.getElementById("winModal").style.display = "flex";
            } else {
              window.location.reload();
            }
          }
        });
    }
  });
});

// Makes the action history panel draggable and saves its position using localstorage
document.addEventListener('DOMContentLoaded', () => {
  const panel = document.getElementById("action_history_floating");

  // Restore position from localStorage if available
  window.addEventListener("DOMContentLoaded", () => {
    const x = localStorage.getItem("historyPanelX");
    const y = localStorage.getItem("historyPanelY");
    if (x !== null && y !== null) {
      panel.style.transform = `translate(${x}px, ${y}px)`;
      panel.setAttribute("data-x", x);
      panel.setAttribute("data-y", y);
    }
  });

  // Enable dragging of the panel using interact.js
  interact('.draggable').draggable({
    allowFrom: '.drag-handle',
    listeners: {
      move(event) {
        const target = event.target;
        const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
        const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

        target.style.transform = `translate(${x}px, ${y}px)`;
        target.setAttribute('data-x', x);
        target.setAttribute('data-y', y);

        // Save the new position in localstorage
        localStorage.setItem("historyPanelX", x);
        localStorage.setItem("historyPanelY", y);
      }
    }
  });
});
