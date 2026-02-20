(() => {
  const qs = (s, root = document) => root.querySelector(s);
  const qsa = (s, root = document) => [...root.querySelectorAll(s)];

  const csrfToken = () =>
    qs('#csrf-form input[name="csrfmiddlewaretoken"]')?.value || getCookie('csrftoken');

  const themePickers = qsa('[data-theme-picker]');
  const themes = new Set(['default', 'dark', 'ocean', 'sunset', 'mono']);

  const applyTheme = (name) => {
    const theme = themes.has(name) ? name : 'default';
    const classes = [...document.body.classList].filter((c) => c.startsWith('theme-'));
    classes.forEach((c) => document.body.classList.remove(c));
    document.body.classList.add(`theme-${theme}`);
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    themePickers.forEach((picker) => {
      picker.value = theme;
    });
  };

  if (themePickers.length) {
    const stored = localStorage.getItem('theme') || 'default';
    applyTheme(stored);
    themePickers.forEach((picker) => {
      picker.addEventListener('change', () => applyTheme(picker.value));
    });
  }

  qsa('.flash').forEach((el, i) => setTimeout(() => el.remove(), 3200 + i * 250));

  const searchInput = qs('#live-search-input');
  const searchResults = qs('#live-search-results');
  if (searchInput && searchResults) {
    let timer;
    searchInput.addEventListener('input', () => {
      clearTimeout(timer);
      const q = searchInput.value.trim();
      timer = setTimeout(async () => {
        if (!q) {
          searchResults.innerHTML = '';
          return;
        }
        const res = await fetch(`/search/live/?q=${encodeURIComponent(q)}`);
        const data = await res.json();
        searchResults.innerHTML = data.results
          .map((m) => `<li><a href="/movies/${m.slug}/">${m.title}</a></li>`)
          .join('');
      }, 300);
    });
  }

  const filterForm = qs('#movie-filter-form');
  if (filterForm) {
    filterForm.addEventListener('change', () => {
      const params = new URLSearchParams(new FormData(filterForm));
      history.replaceState({}, '', `?${params.toString()}`);
    });
  }

  qsa('[data-favorite-toggle]').forEach((favoriteBtn) => {
    favoriteBtn.addEventListener('click', async () => {
      const slug = favoriteBtn.dataset.slug;
      const res = await fetch(`/favorites/toggle-ajax/${slug}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken() },
      });
      if (!res.ok) return;
      const data = await res.json();
      favoriteBtn.textContent = data.is_favorite ? 'In Favorites' : 'Toggle Favorite';
    });
  });

  const rateBtn = qs('#ajax-rate-btn');
  if (rateBtn) {
    rateBtn.addEventListener('click', async () => {
      const ratingSel = qs('#ajax-rating');
      const movieId = ratingSel?.dataset.movieId;
      if (!movieId) return;

      const payload = new URLSearchParams();
      payload.set('rating', ratingSel.value);

      const res = await fetch(`/reviews/ajax/rate/${movieId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken(),
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: payload,
      });
      if (!res.ok) return;
      const data = await res.json();
      alert(`Saved rating ${data.rating}. Avg: ${data.average}`);
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key.toLowerCase() === 'k' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      searchInput?.focus();
    }
  });

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  }
})();
