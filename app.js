'use strict';

const input     = document.getElementById('userInput');
const submitBtn = document.getElementById('submitBtn');
const output    = document.getElementById('output');

function showTyping() {
  output.innerHTML = '<div class="typing"><span></span><span></span><span></span></div>';
}

function showText(text) {
  output.textContent = text;
}

function showPlaceholder() {
  output.innerHTML = '<span class="placeholder">Ответ появится здесь...</span>';
}

async function handleSubmit() {
  const query = input.value.trim();
  if (!query) return;

  submitBtn.disabled = true;
  showTyping();

  try {
    // Simulate an async response (replace with your actual API call)
    await new Promise(r => setTimeout(r, 800));
    showText(`Вы написали: «${query}»`);
  } catch (err) {
    showText('Произошла ошибка. Попробуйте ещё раз.');
  } finally {
    submitBtn.disabled = false;
    input.focus();
  }
}

submitBtn.addEventListener('click', handleSubmit);

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') handleSubmit();
});

// Clear placeholder on first focus if it's still showing
input.addEventListener('focus', () => {
  if (output.querySelector('.placeholder')) {
    showPlaceholder();
  }
}, { once: true });
