(() => {
  const qs = (selector, root = document) => root.querySelector(selector);
  const qsa = (selector, root = document) => [...root.querySelectorAll(selector)];

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  };

  const csrfToken = () =>
    qs('#csrf-form input[name="csrfmiddlewaretoken"]')?.value || getCookie('csrftoken');

  const ensureFeedbackNode = () => {
    let node = qs('#pv-action-feedback');
    if (!node) {
      node = document.createElement('p');
      node.id = 'pv-action-feedback';
      node.className = 'pv-action-feedback';
      node.setAttribute('aria-live', 'polite');
      const mountTarget = qs('#main-wrapper .container') || qs('#main-wrapper');
      mountTarget?.prepend(node);
    }
    return node;
  };

  const announce = (text, isError = false) => {
    const node = ensureFeedbackNode();
    if (!node) return;
    node.textContent = text;
    node.classList.toggle('is-error', Boolean(isError));
    node.classList.add('is-visible');
    window.setTimeout(() => node.classList.remove('is-visible'), 2600);
  };

  const setBusyState = (button, isBusy) => {
    if (!button) return;
    if (isBusy) {
      button.dataset.originalText = button.textContent;
      button.disabled = true;
      button.classList.add('is-loading');
      button.textContent = button.dataset.loadingText || '...';
      return;
    }

    button.disabled = false;
    button.classList.remove('is-loading');
    if (button.dataset.originalText) {
      button.textContent = button.dataset.originalText;
      delete button.dataset.originalText;
    }
  };

  const ensureFieldError = (field) => {
    let errorNode = field.parentElement?.querySelector('.error-text.client-error');
    if (!errorNode && field.parentElement) {
      errorNode = document.createElement('small');
      errorNode.className = 'error-text client-error';
      field.parentElement.appendChild(errorNode);
    }
    return errorNode;
  };

  const clearFieldError = (field) => {
    field.classList.remove('is-invalid');
    const node = field.parentElement?.querySelector('.error-text.client-error');
    if (node) node.remove();
  };

  const showFieldError = (field, message) => {
    field.classList.add('is-invalid');
    const node = ensureFieldError(field);
    if (node) node.textContent = message;
  };

  const todayIso = () => new Date().toISOString().slice(0, 10);

  const validateForm = (form) => {
    let isValid = true;
    const fields = qsa('input,textarea,select', form);
    fields.forEach((field) => clearFieldError(field));

    fields.forEach((field) => {
      if (field.disabled || field.type === 'hidden') return;

      const value = typeof field.value === 'string' ? field.value.trim() : field.value;
      if (field.required && !value) {
        showFieldError(field, 'This field is required.');
        isValid = false;
        return;
      }

      if (field.type === 'email' && value) {
        const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
        if (!emailOk) {
          showFieldError(field, 'Enter a valid email address.');
          isValid = false;
        }
      }

      if (field.name === 'score_min' && value) {
        const parsed = Number(value);
        if (!Number.isFinite(parsed) || parsed < 0) {
          showFieldError(field, 'Min score must be zero or higher.');
          isValid = false;
        }
      }

      if (field.name === 'created_after' && value) {
        if (String(value) > todayIso()) {
          showFieldError(field, 'Date cannot be in the future.');
          isValid = false;
        }
      }

      if (field.name === 'reason' && value && value.length < 3) {
        showFieldError(field, 'Reason must be at least 3 characters.');
        isValid = false;
      }
    });

    const pass1 = qs('input[name="password1"]', form);
    const pass2 = qs('input[name="password2"]', form);
    if (pass1 && pass2 && pass1.value && pass2.value && pass1.value !== pass2.value) {
      showFieldError(pass2, 'Passwords do not match.');
      isValid = false;
    }

    return isValid;
  };

  const ensureConfirmDialog = () => {
    let dialog = qs('#pv-confirm-dialog');
    if (dialog) return dialog;

    dialog = document.createElement('dialog');
    dialog.id = 'pv-confirm-dialog';
    dialog.className = 'pv-confirm-dialog';
    dialog.innerHTML = `
      <form method="dialog" class="pv-confirm-dialog-form">
        <p class="pv-confirm-dialog-text"></p>
        <div class="pv-confirm-dialog-actions">
          <button value="cancel" class="button style2" type="submit">Cancel</button>
          <button value="ok" class="button style3" type="submit">Confirm</button>
        </div>
      </form>
    `;
    document.body.appendChild(dialog);
    return dialog;
  };

  const askConfirm = (message) =>
    new Promise((resolve) => {
      const dialog = ensureConfirmDialog();
      const textNode = qs('.pv-confirm-dialog-text', dialog);
      if (textNode) textNode.textContent = message || 'Are you sure?';

      const closeHandler = () => {
        dialog.removeEventListener('close', closeHandler);
        resolve(dialog.returnValue === 'ok');
      };

      dialog.addEventListener('close', closeHandler);
      dialog.showModal();
    });

  document.body.classList.add('js-ready');

  const themePickers = qsa('[data-theme-picker]');
  const themes = new Set(['template', 'dark']);
  const applyTheme = (name) => {
    const theme = themes.has(name) ? name : 'template';
    const classes = [...document.body.classList].filter((item) => item.startsWith('theme-'));
    classes.forEach((item) => document.body.classList.remove(item));
    document.body.classList.add(`theme-${theme}`);
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    themePickers.forEach((picker) => {
      picker.value = theme;
    });
  };

  if (themePickers.length) {
    applyTheme(localStorage.getItem('theme') || 'template');
    themePickers.forEach((picker) => {
      picker.addEventListener('change', () => applyTheme(picker.value));
    });
  }

  qsa('.flash').forEach((flashNode, index) => {
    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'flash-dismiss';
    closeBtn.textContent = 'x';
    closeBtn.setAttribute('aria-label', 'Dismiss message');
    closeBtn.addEventListener('click', () => flashNode.remove());
    flashNode.appendChild(closeBtn);
    window.setTimeout(() => flashNode.remove(), 3200 + index * 250);
  });

  qsa('form[data-submit-lock]').forEach((form) => {
    form.addEventListener('submit', () => {
      const buttons = qsa('button[type="submit"]', form);
      buttons.forEach((button) => {
        if (button.disabled) return;
        setBusyState(button, true);
      });
    });
  });

  qsa('form[data-client-validate]').forEach((form) => {
    form.setAttribute('novalidate', 'novalidate');
    qsa('input,textarea,select', form).forEach((field) => {
      field.addEventListener('input', () => clearFieldError(field));
      field.addEventListener('change', () => clearFieldError(field));
    });

    form.addEventListener('submit', (event) => {
      if (validateForm(form)) return;
      event.preventDefault();
      qsa('button[type="submit"]', form).forEach((button) => setBusyState(button, false));
      announce('Please fix highlighted fields.', true);
    });
  });

  qsa('form[data-confirm-message]').forEach((form) => {
    form.addEventListener('submit', async (event) => {
      if (form.dataset.confirmed === '1') {
        delete form.dataset.confirmed;
        return;
      }

      event.preventDefault();
      const confirmed = await askConfirm(form.dataset.confirmMessage);
      if (!confirmed) {
        qsa('button[type="submit"]', form).forEach((button) => setBusyState(button, false));
        return;
      }

      form.dataset.confirmed = '1';
      if (typeof form.requestSubmit === 'function') {
        form.requestSubmit();
      } else {
        form.submit();
      }
    });
  });

  qsa('[data-logout-link]').forEach((logoutLink) => {
    logoutLink.addEventListener('click', (event) => {
      event.preventDefault();
      const logoutForm = qs('#logout-form');
      if (!logoutForm) return;
      if (typeof logoutForm.requestSubmit === 'function') {
        logoutForm.requestSubmit();
      } else {
        logoutForm.submit();
      }
    });
  });

  const searchInput = qs('#live-search-input');
  const searchResults = qs('#live-search-results');
  if (searchInput && searchResults) {
    let timer;
    let activeIndex = -1;
    let requestToken = 0;

    const setActive = (nextIndex) => {
      const items = qsa('li', searchResults);
      items.forEach((item, index) => {
        item.classList.toggle('is-active', index === nextIndex);
      });
      activeIndex = nextIndex;
    };

    const clearResults = () => {
      searchResults.innerHTML = '';
      activeIndex = -1;
    };

    const renderResults = (results) => {
      clearResults();
      const fragment = document.createDocumentFragment();
      results.forEach((item) => {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.href =
          typeof item.url === 'string' && item.url.startsWith('/') ? item.url : '#';
        link.textContent = typeof item.title === 'string' ? item.title : '';
        if (item.subtitle) {
          const sub = document.createElement('small');
          sub.textContent = String(item.subtitle);
          link.appendChild(sub);
        }
        li.appendChild(link);
        fragment.appendChild(li);
      });
      searchResults.appendChild(fragment);
    };

    const fetchResults = async () => {
      const q = searchInput.value.trim();
      if (!q) {
        clearResults();
        return;
      }

      requestToken += 1;
      const currentToken = requestToken;
      searchResults.setAttribute('aria-busy', 'true');

      let response;
      try {
        response = await fetch(`/search/live/?q=${encodeURIComponent(q)}`);
      } catch {
        searchResults.setAttribute('aria-busy', 'false');
        clearResults();
        return;
      }

      if (!response.ok || currentToken !== requestToken) {
        searchResults.setAttribute('aria-busy', 'false');
        clearResults();
        return;
      }

      let payload;
      try {
        payload = await response.json();
      } catch {
        searchResults.setAttribute('aria-busy', 'false');
        clearResults();
        return;
      }

      if (currentToken !== requestToken) {
        searchResults.setAttribute('aria-busy', 'false');
        return;
      }

      renderResults(Array.isArray(payload.results) ? payload.results : []);
      searchResults.setAttribute('aria-busy', 'false');
    };

    searchInput.addEventListener('input', () => {
      window.clearTimeout(timer);
      timer = window.setTimeout(fetchResults, 300);
    });

    searchInput.addEventListener('keydown', (event) => {
      const items = qsa('li a', searchResults);
      if (!items.length) return;

      if (event.key === 'ArrowDown') {
        event.preventDefault();
        setActive((activeIndex + 1) % items.length);
      } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        setActive((activeIndex - 1 + items.length) % items.length);
      } else if (event.key === 'Enter' && activeIndex >= 0) {
        event.preventDefault();
        items[activeIndex].click();
      } else if (event.key === 'Escape') {
        clearResults();
      }
    });

    document.addEventListener('click', (event) => {
      if (searchInput.contains(event.target) || searchResults.contains(event.target)) return;
      clearResults();
    });
  }

  const filterForm = qs('#thread-filter-form') || qs('#search-filter-form');
  if (filterForm) {
    filterForm.addEventListener('change', () => {
      const params = new URLSearchParams(new FormData(filterForm));
      history.replaceState({}, '', `?${params.toString()}`);
    });
  }

  qsa('[data-bookmark-toggle]').forEach((bookmarkBtn) => {
    bookmarkBtn.dataset.loadingText = bookmarkBtn.dataset.loadingText || 'Saving...';
    bookmarkBtn.addEventListener('click', async () => {
      const slug = bookmarkBtn.dataset.slug;
      if (!slug) return;
      const labelOn = bookmarkBtn.dataset.labelOn || 'Bookmarked';
      const labelOff = bookmarkBtn.dataset.labelOff || 'Save';
      setBusyState(bookmarkBtn, true);
      let response;
      try {
        response = await fetch(`/bookmarks/toggle/${slug}/`, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken() },
        });
      } catch {
        setBusyState(bookmarkBtn, false);
        announce('Bookmark request failed.', true);
        return;
      }
      if (!response.ok) {
        setBusyState(bookmarkBtn, false);
        announce('Bookmark request failed.', true);
        return;
      }
      const payload = await response.json();
      setBusyState(bookmarkBtn, false);
      bookmarkBtn.textContent = payload.is_bookmarked ? labelOn : labelOff;
      announce(payload.is_bookmarked ? 'Saved to bookmarks.' : 'Removed from bookmarks.');
    });
  });

  const rateBtn = qs('#ajax-rate-btn');
  if (rateBtn) {
    rateBtn.dataset.loadingText = rateBtn.dataset.loadingText || 'Saving...';
    rateBtn.addEventListener('click', async () => {
      const ratingSel = qs('#ajax-rating');
      const threadSlug = ratingSel?.dataset.threadSlug;
      if (!threadSlug || !ratingSel) return;

      setBusyState(rateBtn, true);
      const payload = new URLSearchParams();
      payload.set('rating', ratingSel.value);

      let response;
      try {
        response = await fetch(`/bookmarks/rate/${threadSlug}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken(),
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: payload,
        });
      } catch {
        setBusyState(rateBtn, false);
        announce('Rating request failed.', true);
        return;
      }

      if (!response.ok) {
        setBusyState(rateBtn, false);
        announce('Rating request failed.', true);
        return;
      }

      const data = await response.json();
      const avgTarget = qs('#thread-average-rating');
      const badgeTarget = qs('#thread-rating-badge');
      if (avgTarget && typeof data.average === 'number') avgTarget.textContent = data.average.toFixed(1);
      if (badgeTarget) badgeTarget.textContent = data.badge;
      setBusyState(rateBtn, false);
      announce('Rating updated.');
    });
  }

  qsa('[data-vote-target]').forEach((voteBtn) => {
    voteBtn.dataset.loadingText = voteBtn.dataset.loadingText || 'Voting...';
    voteBtn.addEventListener('click', async () => {
      const targetType = voteBtn.dataset.voteTarget;
      const targetId = voteBtn.dataset.targetId;
      const value = voteBtn.dataset.value;
      if (!targetType || !targetId || !value) return;

      setBusyState(voteBtn, true);
      const payload = new URLSearchParams();
      payload.set('target_type', targetType);
      payload.set('target_id', targetId);
      payload.set('value', value);

      let response;
      try {
        response = await fetch('/votes/toggle/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken(),
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: payload,
        });
      } catch {
        setBusyState(voteBtn, false);
        announce('Vote request failed.', true);
        return;
      }

      if (!response.ok) {
        setBusyState(voteBtn, false);
        announce('Vote request failed.', true);
        return;
      }

      const data = await response.json();
      const scoreEl = qs('#thread-score');
      if (targetType === 'thread' && scoreEl && typeof data.score === 'number') {
        scoreEl.textContent = data.score;
      }
      setBusyState(voteBtn, false);
      announce('Vote saved.');
    });
  });

  qsa('.pv-zf-nav-trigger').forEach((trigger) => {
    const li = trigger.closest('li');
    if (!li) return;

    const setExpanded = (value) => {
      trigger.setAttribute('aria-expanded', value ? 'true' : 'false');
    };

    setExpanded(false);
    li.addEventListener('mouseenter', () => setExpanded(true));
    li.addEventListener('mouseleave', () => setExpanded(false));
    trigger.addEventListener('focus', () => setExpanded(true));
    li.addEventListener('focusout', (event) => {
      if (!li.contains(event.relatedTarget)) setExpanded(false);
    });
    trigger.addEventListener('click', (event) => {
      const expanded = trigger.getAttribute('aria-expanded') === 'true';
      setExpanded(!expanded);
      event.preventDefault();
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key.toLowerCase() === 'k' && (event.ctrlKey || event.metaKey)) {
      event.preventDefault();
      searchInput?.focus();
    }
    if (event.key === 'Escape') {
      qsa('.flash').forEach((flash) => flash.remove());
    }
  });
})();
