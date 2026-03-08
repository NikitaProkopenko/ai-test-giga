'use strict';

const searchInput   = document.getElementById('searchInput');
const searchBox     = document.getElementById('searchBox');
const suggestionsEl = document.getElementById('suggestions');
const submitBtn     = document.getElementById('submitBtn');
const resultPanel   = document.getElementById('resultPanel');

// Sample suggestion pool (simulates autocomplete)
const SUGGESTION_POOL = [
  'как приготовить борщ',
  'как выучить JavaScript',
  'погода в Москве',
  'курс доллара сегодня',
  'что такое машинное обучение',
  'лучшие фильмы 2024',
  'рецепт пиццы',
  'как похудеть',
  'новости',
  'перевести текст',
  'python для начинающих',
  'история России',
  'как работает интернет',
  'youtube',
  'вконтакте',
];

let activeIndex = -1;
let currentSuggestions = [];

// ── Suggestions ──────────────────────────────────────────────

function getSuggestions(query) {
  if (!query.trim()) return [];
  const q = query.toLowerCase();
  return SUGGESTION_POOL
    .filter(s => s.startsWith(q) || s.includes(q))
    .slice(0, 8);
}

function renderSuggestions(items) {
  currentSuggestions = items;
  activeIndex = -1;

  if (!items.length) {
    hideSuggestions();
    return;
  }

  suggestionsEl.innerHTML = items.map((item, i) =>
    `<div class="suggestion-item" role="option" data-index="${i}">
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
      </svg>
      <span>${highlightMatch(item, searchInput.value)}</span>
    </div>`
  ).join('');

  suggestionsEl.classList.add('visible');

  // Merge search-box and suggestions visually
  searchBox.style.borderRadius = '24px 24px 0 0';
  searchBox.style.borderBottom = '1px solid #e4e4e4';
}

function highlightMatch(text, query) {
  if (!query.trim()) return text;
  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return text.replace(new RegExp(`(${escaped})`, 'gi'), '<strong>$1</strong>');
}

function hideSuggestions() {
  suggestionsEl.classList.remove('visible');
  suggestionsEl.innerHTML = '';
  currentSuggestions = [];
  activeIndex = -1;
  searchBox.style.borderRadius = '';
  searchBox.style.borderBottom = '';
}

// ── Keyboard navigation ───────────────────────────────────────

searchInput.addEventListener('keydown', (e) => {
  const items = suggestionsEl.querySelectorAll('.suggestion-item');
  if (!items.length) {
    if (e.key === 'Enter') doSearch();
    return;
  }

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    activeIndex = (activeIndex + 1) % items.length;
    updateActive(items);
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    activeIndex = (activeIndex - 1 + items.length) % items.length;
    updateActive(items);
  } else if (e.key === 'Enter') {
    e.preventDefault();
    if (activeIndex >= 0 && currentSuggestions[activeIndex]) {
      searchInput.value = currentSuggestions[activeIndex];
      hideSuggestions();
    }
    doSearch();
  } else if (e.key === 'Escape') {
    hideSuggestions();
  }
});

function updateActive(items) {
  items.forEach((el, i) => {
    el.classList.toggle('active', i === activeIndex);
  });
  if (activeIndex >= 0) {
    searchInput.value = currentSuggestions[activeIndex];
  }
}

// ── Input events ─────────────────────────────────────────────

searchInput.addEventListener('input', () => {
  const val = searchInput.value;
  renderSuggestions(getSuggestions(val));
});

searchInput.addEventListener('focus', () => {
  const val = searchInput.value;
  if (val) renderSuggestions(getSuggestions(val));
});

// Suggestion click
suggestionsEl.addEventListener('click', (e) => {
  const item = e.target.closest('.suggestion-item');
  if (!item) return;
  const idx = parseInt(item.dataset.index, 10);
  searchInput.value = currentSuggestions[idx];
  hideSuggestions();
  doSearch();
});

// Hide on outside click
document.addEventListener('click', (e) => {
  if (!searchBox.contains(e.target) && !suggestionsEl.contains(e.target)) {
    hideSuggestions();
  }
});

// ── Search action ─────────────────────────────────────────────

function doSearch() {
  const query = searchInput.value.trim();
  hideSuggestions();

  if (!query) {
    resultPanel.innerHTML = '';
    return;
  }

  // Animate the result panel
  resultPanel.style.opacity = '0';

  const encoded = encodeURIComponent(query);
  const fakeCount = Math.floor(Math.random() * 900_000_000) + 100_000_000;
  const countStr = fakeCount.toLocaleString('ru-RU');

  resultPanel.innerHTML = `
    <div class="result-query">Запрос: «${escapeHtml(query)}»</div>
    <div class="result-count">Найдено примерно ${countStr} результатов</div>
    <a class="result-link" href="https://www.google.com/search?q=${encoded}" target="_blank" rel="noopener noreferrer">
      Искать «${escapeHtml(query)}» в Google →
    </a>
  `;

  requestAnimationFrame(() => {
    resultPanel.style.transition = 'opacity 0.25s ease';
    resultPanel.style.opacity = '1';
  });
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

submitBtn.addEventListener('click', () => {
  addRipple(submitBtn);
  doSearch();
});

// ── "I'm Feeling Lucky" ───────────────────────────────────────

document.querySelector('.btn-lucky').addEventListener('click', function () {
  addRipple(this);
  const query = searchInput.value.trim();
  if (query) {
    window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}&btnI=1`, '_blank', 'noopener,noreferrer');
  } else {
    searchInput.focus();
  }
});

// ── Ripple helper ─────────────────────────────────────────────

function addRipple(btn) {
  const ripple = document.createElement('span');
  ripple.classList.add('ripple');
  const rect = btn.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  ripple.style.cssText = `width:${size}px;height:${size}px;left:${rect.width / 2 - size / 2}px;top:${rect.height / 2 - size / 2}px`;
  btn.appendChild(ripple);
  ripple.addEventListener('animationend', () => ripple.remove());
}

// ── Mic button (demo) ─────────────────────────────────────────

document.querySelector('.mic-btn').addEventListener('click', () => {
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    alert('Ваш браузер не поддерживает голосовой ввод.');
    return;
  }
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SR();
  recognition.lang = 'ru-RU';
  recognition.interimResults = false;
  recognition.onresult = (e) => {
    searchInput.value = e.results[0][0].transcript;
    renderSuggestions(getSuggestions(searchInput.value));
  };
  recognition.start();
});
