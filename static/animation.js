function validateDrop(questionId, timelineIds) {
  fetch('/validate_drop', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question_id: questionId,
      timeline: timelineIds
    })
  })
  .then(res => res.json())
  .then(data => {
    if (!data.valid) {
      loseCards(); 
    } else {
      console.log('Correct placement');
    }
  });
}

function loseCards() {
  const cards = document.querySelectorAll('.card.unlocked');

  cards.forEach(card => {
    const x = (Math.random() - 0.5) * 200;
    const y = (Math.random() - 0.5) * 160;
    const angle = (Math.random() - 0.5) * 40;

    card.style.setProperty('--x', `${x}px`);
    card.style.setProperty('--y', `${y}px`);
    card.style.setProperty('--angle', `${angle}deg`);

    card.classList.add('lost');
  });
}
