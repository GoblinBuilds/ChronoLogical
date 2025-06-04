document.addEventListener('DOMContentLoaded', () => {
  const timeline = document.getElementById('timeline');
  const palette = document.getElementById('palette');

  Sortable.create(palette, {
    group: { name: 'shared', pull: 'clone', put: false },
    sort: false,
    animation: 150
  });

  Sortable.create(timeline, {
    group: 'shared',
    animation: 150,
    onAdd: function (evt) {
      handleDrop(evt);
    }
  });
});

function handleDrop(evt) {
  const questionId = evt.item.dataset.qid;
  const timeline = document.getElementById('timeline');
  const timelineOrder = [...timeline.children].map(card => card.dataset.qid);
  sendDropData(questionId, timelineOrder);
}


function sendDropData(questionId, timelineOrder) {
  fetch('/validate_drop', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question_id: questionId,
      timeline: timelineOrder
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.valid) {
      updateTimeline(data.unlocked, data.locked);
      updateStats(data.score, data.lifeline_count, data.skips);
      updateHistory(data.history);
    } else {
        loseCards()
        updateHistory(data.history);
        // Optional: add animation before clearing
        document.querySelectorAll('.card.unlocked').forEach(card => {
          card.classList.add('lost');
        });

        // After animation, update DOM
        setTimeout(() => {
          updateTimeline(data.unlocked, data.locked);
        }, 500); // Matches your card loss animation duration
        updateStats(data.score, data.lifeline_count, data.skips);
      }

      if (data.next_question) {
        updatePaletteCard(data.next_question);
      }

      if (data.win) {
        document.getElementById("winModal").style.display = "flex";
      }

      if (data.song_embed_url) {
        const container = document.querySelector(".spotify-player");
        container.innerHTML = ''; // Clear old iframe

        const iframe = document.createElement("iframe");
        iframe.style.borderRadius = "12px";
        iframe.src = data.song_embed_url + "?t=" + new Date().getTime(); // Prevent caching
        iframe.width = "100%";
        iframe.height = "80";
        iframe.setAttribute("frameborder", "0");
        iframe.setAttribute("allowtransparency", "true");
        iframe.setAttribute("allow", "autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture");
        iframe.loading = "lazy";

        container.appendChild(iframe);
      }
  });
}

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
// script animates a numerical score count-up effect on page load
document.addEventListener("DOMContentLoaded", () => {
  const scoreEl = document.getElementById("score");
  const finalScore = parseInt(scoreEl.dataset.score);
  let current = 0;
  const duration = 1000; 
  const frameRate = 30;
  const steps = duration / frameRate;
  const increment = Math.ceil(Math.abs(finalScore) / steps);
  const padLength = 5;

  function formatScore(score, padLength = 5) {
    const absStr = Math.abs(score).toString().padStart(padLength, '0');
    return score < 0 ? `-${absStr}` : absStr;
  }

  const counter = setInterval(() => {
    if (finalScore >= 0) {
      current += increment;
      if (current >= finalScore) {
        current = finalScore;
        clearInterval(counter);
      }
    } else {
      current -= increment;
      if (current <= finalScore) {
        current = finalScore;
        clearInterval(counter);
      }
    }

    scoreEl.textContent = formatScore(current, padLength);
  }, frameRate);
});

fetch('/check_answer', {
  method: 'POST',
  body: JSON.stringify({
    question_id: qid,
    user_date: selectedDate
  }),
  headers: {
    'Content-Type': 'application/json'
  }
})

function updateTimeline(unlocked, locked) {
  const timeline = document.getElementById('timeline');
  timeline.innerHTML = '';

  const combined = [...locked, ...unlocked].sort((a, b) => parseInt(a.date) - parseInt(b.date))
  for (const card of combined) {
    const cardDiv = document.createElement('div');
    cardDiv.className = `card ${locked.some(l => l.question_id === card.question_id) ? 'correct' : 'unlocked'}`;
    cardDiv.dataset.id = card.date;
    cardDiv.dataset.qid = card.question_id;

    cardDiv.innerHTML = `
      <p class="date">${card.date}</p>
      <p class="answered_question">${card.category === "Music & Soundbites" ? "Spotify Track" : card.question}</p>
    `;
    timeline.appendChild(cardDiv);
  }
}

function updateStats(score, lifelines, skips) {
  document.getElementById('score').textContent = score.toString().padStart(5, '0');
  document.querySelector('.hover_info:nth-child(2) h3').innerHTML = `Skips: ${skips}`;
  document.querySelector('.hover_info:nth-child(3) h3').innerHTML = `Lock-ins: ${3 - lifelines}`;
}

function updateHistory(history) {
  const list = document.querySelector('#action_history_floating ul');
  list.innerHTML = '';
  [...history].reverse().forEach(line => {
    const li = document.createElement('li');
    li.textContent = line;
    list.appendChild(li);
  });
}

function updatePaletteCard(card) {
  const palette = document.getElementById('palette');
  palette.innerHTML = ''; 

  const cardDiv = document.createElement('div');
  cardDiv.className = 'card';
  cardDiv.dataset.id = card.date;
  cardDiv.dataset.qid = card.question_id;
  cardDiv.dataset.date = card.date;

  cardDiv.innerHTML = `
    <p class="answered_question">
      ${card.category === "Music & Soundbites" ? "Guess the year of the song!" : card.question}
    </p>
  `;

  palette.appendChild(cardDiv);

  Sortable.create(document.getElementById('palette'), {
  group: { name: 'shared', pull: 'clone', put: false },
  sort: false,
  animation: 150
});
}