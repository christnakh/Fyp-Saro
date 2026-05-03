/* ═══════════════════════════════════════════════════════════════
   Steel Waste Prediction System — Main JavaScript
   NEXUS design interactions + prediction form
   ═══════════════════════════════════════════════════════════════ */

'use strict';

const lerp = (a, b, t) => a + (b - a) * t;
const raf = (fn) => requestAnimationFrame(fn);

function prefersReducedMotion() {
  return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/** Non-blocking message; click to dismiss. */
function showToast(message, variant = 'info') {
  const stack = document.getElementById('toastStack');
  if (!stack || !message) return;
  const el = document.createElement('button');
  el.type = 'button';
  let extra = '';
  if (variant === 'error') extra = ' app-toast--error';
  if (variant === 'success') extra = ' app-toast--success';
  el.className = `app-toast${extra}`;
  el.setAttribute('aria-label', 'Dismiss notification');
  el.textContent = message;
  const dismiss = () => {
    el.remove();
  };
  el.addEventListener('click', dismiss);
  stack.appendChild(el);
  const ms = variant === 'error' ? 9000 : 4800;
  setTimeout(dismiss, ms);
}

function initBackToTop() {
  const btn = document.getElementById('backToTop');
  if (!btn) return;
  const toggle = () => {
    const y = window.scrollY || document.documentElement.scrollTop;
    if (y > 400) {
      btn.removeAttribute('hidden');
      requestAnimationFrame(() => btn.classList.add('is-visible'));
    } else {
      btn.classList.remove('is-visible');
      btn.setAttribute('hidden', '');
    }
  };
  window.addEventListener('scroll', toggle, { passive: true });
  toggle();
  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
  });
}

/** Count up hero metrics when the stats strip scrolls into view. */
function initStatCounters() {
  const root = document.getElementById('heroStats');
  if (!root) return;
  const items = root.querySelectorAll('[data-stat-item][data-count-to]');
  if (!items.length) return;

  const applyFinal = () => {
    items.forEach((item) => {
      const target = parseFloat(item.getAttribute('data-count-to'));
      const dec = parseInt(item.getAttribute('data-decimals') || '0', 10) || 0;
      const valEl = item.querySelector('.stat-value');
      if (!valEl || !Number.isFinite(target)) return;
      valEl.textContent = dec ? target.toFixed(dec) : String(Math.round(target));
    });
  };

  const animate = () => {
    items.forEach((item) => {
      const target = parseFloat(item.getAttribute('data-count-to'));
      const dec = parseInt(item.getAttribute('data-decimals') || '0', 10) || 0;
      const valEl = item.querySelector('.stat-value');
      if (!valEl || !Number.isFinite(target)) return;

      if (prefersReducedMotion()) {
        valEl.textContent = dec ? target.toFixed(dec) : String(Math.round(target));
        return;
      }

      const start = performance.now();
      const dur = 1000;
      const tick = (now) => {
        const t = Math.min(1, (now - start) / dur);
        const eased = 1 - (1 - t) * (1 - t);
        const cur = target * eased;
        valEl.textContent = dec ? cur.toFixed(dec) : String(Math.floor(cur));
        if (t < 1) {
          requestAnimationFrame(tick);
        } else {
          valEl.textContent = dec ? target.toFixed(dec) : String(Math.round(target));
        }
      };
      requestAnimationFrame(tick);
    });
  };

  if (prefersReducedMotion()) {
    applyFinal();
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          io.disconnect();
          animate();
        }
      });
    },
    { threshold: 0.2 }
  );
  io.observe(root);
}

/** Warm the predict route after hover/focus on nav links (one-shot). */
function initNavPrefetch() {
  const predictUrl = document.body.getAttribute('data-predict-url');
  if (!predictUrl) return;
  let done;
  const inject = () => {
    if (done) return;
    done = true;
    const l = document.createElement('link');
    l.rel = 'prefetch';
    l.href = predictUrl;
    document.head.appendChild(l);
  };
  document.querySelectorAll('a[href]').forEach((a) => {
    try {
      const u = new URL(a.href, window.location.origin);
      if (!u.pathname.includes('predict')) return;
    } catch {
      return;
    }
    a.addEventListener('mouseenter', inject, { once: true });
    a.addEventListener('focus', inject, { once: true });
  });
}

/* ─── CUSTOM CURSOR ──────────────────────────────────────────── */
function initCursor() {
  const cursor = document.getElementById('cursor');
  const follower = document.getElementById('cursorFollower');
  if (!cursor || !follower) return;

  let mx = 0, my = 0;
  let fx = 0, fy = 0;

  document.addEventListener('mousemove', (e) => {
    mx = e.clientX;
    my = e.clientY;
    cursor.style.left = mx + 'px';
    cursor.style.top = my + 'px';
  });

  function animateFollower() {
    fx = lerp(fx, mx, 0.1);
    fy = lerp(fy, my, 0.1);
    follower.style.left = fx + 'px';
    follower.style.top = fy + 'px';
    raf(animateFollower);
  }
  animateFollower();

  const interactives = 'a, button, .tilt-card, .nav-link, .fc-link, .btn-primary, .btn-ghost, .btn-secondary, .btn-predict, .back-to-top, .app-toast';
  document.querySelectorAll(interactives).forEach(el => {
    el.addEventListener('mouseenter', () => {
      cursor.classList.add('expanded');
      follower.classList.add('expanded');
    });
    el.addEventListener('mouseleave', () => {
      cursor.classList.remove('expanded');
      follower.classList.remove('expanded');
    });
  });

  document.addEventListener('mouseleave', () => {
    cursor.style.opacity = '0';
    follower.style.opacity = '0';
  });
  document.addEventListener('mouseenter', () => {
    cursor.style.opacity = '1';
    follower.style.opacity = '1';
  });
}

/* ─── MAGNETIC BUTTONS / LINKS ────────────────────────────────── */
function initMagnetic() {
  document.querySelectorAll('.magnetic').forEach(el => {
    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = e.clientX - cx;
      const dy = e.clientY - cy;
      const strength = 0.35;
      el.style.transform = `translate(${dx * strength}px, ${dy * strength}px)`;
    });
    el.addEventListener('mouseleave', () => {
      el.style.transition = 'transform 0.5s cubic-bezier(0.16,1,0.3,1)';
      el.style.transform = 'translate(0, 0)';
      setTimeout(() => { el.style.transition = ''; }, 500);
    });
  });
}

/* ─── NAV DOCK SCROLL STATE ───────────────────────────────────── */
function initNav() {
  const nav = document.getElementById('navDock');
  if (!nav) return;

  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    nav.classList.toggle('scrolled', y > 60);
  }, { passive: true });
}

/* ─── SCROLL REVEAL ────────────────────────────────────────────── */
function initScrollReveal() {
  const elements = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const delay = el.dataset.delay || '0';
        setTimeout(() => el.classList.add('revealed'), parseInt(delay));
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

  elements.forEach(el => observer.observe(el));
}

/* ─── 3D TILT CARDS ───────────────────────────────────────────── */
function initTiltCards() {
  document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      const rotX = -y * 10;
      const rotY = x * 10;
      card.style.transform = `perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(1.02)`;
      card.style.transition = 'none';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      card.style.transition = 'transform 0.6s cubic-bezier(0.16,1,0.3,1)';
    });
  });
}

/* ─── PARAM HELP (?): structured multi-line tooltips ───────────── */
const PARAM_HELP_TIP_ID = 'paramHelpTooltip';

function initParamHelpTooltips() {
  if (document.body.dataset.paramHelpTipsInit === '1') return;
  document.body.dataset.paramHelpTipsInit = '1';

  let tipEl = document.getElementById(PARAM_HELP_TIP_ID);
  if (!tipEl) {
    tipEl = document.createElement('div');
    tipEl.id = PARAM_HELP_TIP_ID;
    tipEl.className = 'param-help-floating-tip';
    tipEl.setAttribute('role', 'tooltip');
    tipEl.hidden = true;
    document.body.appendChild(tipEl);
  }

  let hideTimer = null;
  let activeBtn = null;

  const clearHideTimer = () => {
    if (hideTimer) {
      clearTimeout(hideTimer);
      hideTimer = null;
    }
  };

  const hideTip = () => {
    clearHideTimer();
    tipEl.classList.remove('is-visible');
    tipEl.hidden = true;
    tipEl.textContent = '';
    activeBtn = null;
  };

  const scheduleHide = () => {
    clearHideTimer();
    hideTimer = setTimeout(hideTip, 180);
  };

  const positionTip = (btn) => {
    const margin = 10;
    const r = btn.getBoundingClientRect();
    tipEl.style.maxWidth = `${Math.min(352, window.innerWidth - 2 * margin)}px`;
    const tw = tipEl.offsetWidth || 280;
    const th = tipEl.offsetHeight || 48;

    let left = r.left;
    let top = r.bottom + margin;
    left = Math.max(margin, Math.min(left, window.innerWidth - tw - margin));
    if (top + th > window.innerHeight - margin) {
      top = Math.max(margin, r.top - th - margin);
    }
    tipEl.style.left = `${left}px`;
    tipEl.style.top = `${top}px`;
  };

  const showTip = (btn) => {
    const raw = btn.getAttribute('data-help') || btn.getAttribute('title') || '';
    if (!raw.trim()) return;
    clearHideTimer();
    activeBtn = btn;
    tipEl.textContent = raw;
    tipEl.hidden = false;
    requestAnimationFrame(() => {
      positionTip(btn);
      tipEl.classList.add('is-visible');
    });
  };

  document.addEventListener('mouseover', (e) => {
    const btn = e.target && e.target.closest && e.target.closest('.param-help-btn');
    if (btn) showTip(btn);
  });

  document.addEventListener('mouseout', (e) => {
    const rel = e.relatedTarget;
    const btn = e.target && e.target.closest && e.target.closest('.param-help-btn');
    if (btn) {
      if (rel && (btn.contains(rel) || rel.closest(`#${PARAM_HELP_TIP_ID}`))) return;
      scheduleHide();
      return;
    }
    const fromTip = e.target && e.target.closest && e.target.closest(`#${PARAM_HELP_TIP_ID}`);
    if (fromTip) {
      if (rel && (fromTip.contains(rel) || rel.closest('.param-help-btn'))) return;
      scheduleHide();
    }
  });

  tipEl.addEventListener('pointerenter', clearHideTimer);
  tipEl.addEventListener('pointerleave', scheduleHide);

  document.addEventListener('focusin', (e) => {
    const btn = e.target && e.target.closest && e.target.closest('.param-help-btn');
    if (btn) showTip(btn);
  });
  document.addEventListener('focusout', (e) => {
    const btn = e.target && e.target.closest && e.target.closest('.param-help-btn');
    if (!btn) return;
    setTimeout(() => {
      const ae = document.activeElement;
      if (ae && tipEl.contains(ae)) return;
      if (ae === btn) return;
      hideTip();
    }, 0);
  });

  const reposition = () => {
    if (!tipEl.classList.contains('is-visible') || !activeBtn) return;
    positionTip(activeBtn);
  };
  window.addEventListener('scroll', reposition, true);
  window.addEventListener('resize', reposition);
}

/* ─── PREDICTION FORM (AJAX) ───────────────────────────────────── */
function initPredictionForm() {
  const form = document.getElementById('predictionForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const loadingEl = document.getElementById('loading');
    const resultCard = document.getElementById('resultCard');
    const submitBtn = document.getElementById('btnPredictSubmit');

    if (loadingEl) {
      loadingEl.style.display = 'block';
      loadingEl.setAttribute('aria-hidden', 'false');
    }
    if (resultCard) {
      resultCard.classList.remove('result-card--animate-in');
      resultCard.style.display = 'none';
    }
    form.classList.add('is-busy');
    if (submitBtn) submitBtn.disabled = true;

    const formData = new FormData(this);
    const action = form.getAttribute('action') || '/predict';

    fetch(action, {
      method: 'POST',
      body: formData
    })
      .then((response) => response.text())
      .then((html) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newResultCard = doc.getElementById('resultCard');

        if (newResultCard && resultCard) {
          resultCard.innerHTML = newResultCard.innerHTML;
          resultCard.style.display = 'block';
          void resultCard.offsetWidth;
          resultCard.classList.add('result-card--animate-in');
          initPredictionResults(resultCard);
          // #region agent log
          fetch('http://127.0.0.1:7490/ingest/a4c0d7fd-2a80-4f45-a716-f22a573d9972', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Debug-Session-Id': '593439' }, body: JSON.stringify({ sessionId: '593439', hypothesisId: 'H5', location: 'main.js:initPredictionForm', message: 'ajax_result_ready', data: { hasScenarioScript: !!resultCard.querySelector('#predictionScenarioData') }, timestamp: Date.now() }) }).catch(() => {});
          // #endregion
          resultCard.scrollIntoView({
            behavior: prefersReducedMotion() ? 'auto' : 'smooth',
            block: 'start',
          });
          showToast('Prediction ready — use interactive levers to explore what-if scenarios.', 'success');
        } else {
          showToast('Could not read results from the server. Try refreshing the page.', 'error');
        }
      })
      .catch((err) => {
        console.error('Error:', err);
        showToast('Network error while predicting. Check your connection and try again.', 'error');
      })
      .finally(() => {
        if (loadingEl) {
          loadingEl.style.display = 'none';
          loadingEl.setAttribute('aria-hidden', 'true');
        }
        form.classList.remove('is-busy');
        if (submitBtn) submitBtn.disabled = false;
      });
  });
}

function resetForm() {
  const form = document.getElementById('predictionForm');
  const resultCard = document.getElementById('resultCard');

  if (form) form.reset();
  if (resultCard) {
    resultCard.style.display = 'none';
    resultCard.classList.remove('result-card--animate-in');
  }

  window.scrollTo({ top: 0, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
}

/* ─── PREDICTION RESULTS: scenario sliders + live API refresh ───────── */
const CATEGORY_BADGE_CLASS = {
  Excellent: 'success',
  Good: 'info',
  Average: 'warning',
  Poor: 'warning',
  'Very Poor': 'danger'
};

const RELIABILITY_BADGE_CLASS = {
  high: 'success',
  medium: 'warning',
  low: 'danger'
};

function fmtMoney(n) {
  return `$${Math.round(n).toLocaleString('en-US')}`;
}

function fmtNum(n, d) {
  const p = 10 ** (d || 0);
  return (Math.round(n * p) / p).toString();
}

function debounce(fn, ms) {
  let t;
  return function (...args) {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, args), ms);
  };
}

/** Debounced call with `.flush()` to run immediately (e.g. on range release). */
function debounceFlush(fn, ms) {
  let t;
  let lastArgs;
  const debounced = function (...args) {
    lastArgs = args;
    clearTimeout(t);
    t = setTimeout(() => {
      t = null;
      fn.apply(null, lastArgs);
    }, ms);
  };
  debounced.flush = () => {
    clearTimeout(t);
    t = null;
    if (lastArgs) fn.apply(null, lastArgs);
  };
  debounced.cancel = () => {
    clearTimeout(t);
    t = null;
  };
  return debounced;
}

const INTEGER_MODEL_KEYS = new Set([
  'num_unique_required_lengths',
  'cutting_optimization_usage',
  'bim_integration_level',
  'design_revisions_per_month',
  'supervision_index_1to5',
  'material_control_level_1to3',
  'storage_handling_index_1to5',
  'offcut_reuse_policy_0to2',
  'change_orders_per_month',
  'lead_time_days',
  'order_frequency_per_month',
]);

function coerceApiField(key, v) {
  if (key === 'reinforcement_ratio_kg_per_m3') {
    const n = Number(v);
    return Number.isFinite(n) ? n : 120;
  }
  if (INTEGER_MODEL_KEYS.has(key)) {
    const n = parseInt(String(v), 10);
    return Number.isFinite(n) ? n : 0;
  }
  if (key === 'project_id') return v == null ? 'P0' : String(v);
  if (v == null || v === '') return '';
  return typeof v === 'string' ? v : String(v);
}

function buildApiPayload(currentObj, steelKg) {
  const out = {};
  Object.keys(currentObj).forEach((k) => {
    if (k === 'total_steel_kg') return;
    out[k] = coerceApiField(k, currentObj[k]);
  });
  let steel = Number(steelKg);
  if (!Number.isFinite(steel) || steel <= 0) steel = 100000;
  out.total_steel_kg = steel;
  return out;
}

function readTotalSteelKg(currentFallback) {
  const steelInput = document.getElementById('inputTotalSteelKg');
  if (steelInput && steelInput.value !== '') {
    const n = Number(steelInput.value);
    if (Number.isFinite(n) && n > 0) return n;
  }
  const f = Number(currentFallback);
  if (Number.isFinite(f) && f > 0) return f;
  return 100000;
}

function normalizeNumericRange(key, b, rawCur) {
  const isReinf = key === 'reinforcement_ratio_kg_per_m3';
  const step = isReinf ? 0.1 : 1;
  let min = Number(b.p5);
  let max = Number(b.p95);
  if (!Number.isFinite(min)) min = Number(b.min);
  if (!Number.isFinite(max)) max = Number(b.max);
  let cur = isReinf ? Number(rawCur) : Math.round(Number(rawCur));
  if (!Number.isFinite(cur)) cur = isReinf ? 120 : 0;
  if (!Number.isFinite(min) || !Number.isFinite(max) || max <= min) {
    const pad = isReinf ? 30 : 8;
    min = cur - pad;
    max = cur + pad;
  }
  if (cur < min) min = cur - (isReinf ? 2 : 2);
  if (cur > max) max = cur + (isReinf ? 2 : 2);
  if (max <= min) max = min + (isReinf ? 0.2 : 2);
  if (!isReinf) {
    min = Math.floor(min);
    max = Math.ceil(max);
    if (max <= min) max = min + 1;
  } else {
    min = Math.round(min * 10) / 10;
    max = Math.round(max * 10) / 10;
    if (max <= min) max = Math.round((min + 0.2) * 10) / 10;
  }
  return { min, max, step };
}

function clampSnapNumeric(key, v, min, max) {
  const isReinf = key === 'reinforcement_ratio_kg_per_m3';
  const n = isReinf ? Number(v) : Math.round(Number(v));
  if (!Number.isFinite(n)) return isReinf ? Math.min(max, Math.max(min, 120)) : Math.min(max, Math.max(min, 0));
  const c = Math.min(max, Math.max(min, n));
  return isReinf ? Math.round(c * 10) / 10 : c;
}

function initPredictionResults(resultCard) {
  if (!resultCard) return;
  const script = resultCard.querySelector('#predictionScenarioData');
  if (!script) return;

  let ctx;
  try {
    ctx = JSON.parse(script.textContent);
  } catch (e) {
    console.warn('prediction scenario JSON parse failed', e);
    // #region agent log
    fetch('http://127.0.0.1:7490/ingest/a4c0d7fd-2a80-4f45-a716-f22a573d9972', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Debug-Session-Id': '593439' }, body: JSON.stringify({ sessionId: '593439', hypothesisId: 'H3', location: 'main.js:initPredictionResults', message: 'json_parse_failed', data: { err: String(e && e.message) }, timestamp: Date.now() }) }).catch(() => {});
    // #endregion
    return;
  }

  const keys = ctx.scenarioFeatureKeys || [];
  // #region agent log
  fetch('http://127.0.0.1:7490/ingest/a4c0d7fd-2a80-4f45-a716-f22a573d9972', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Debug-Session-Id': '593439' }, body: JSON.stringify({ sessionId: '593439', hypothesisId: 'H3', location: 'main.js:initPredictionResults', message: 'scenario_ctx', data: { scenarioKeys: keys.length, hasBounds: !!ctx.bounds }, timestamp: Date.now() }) }).catch(() => {});
  // #endregion
  if (!keys.length) {
    // #region agent log
    fetch('http://127.0.0.1:7490/ingest/a4c0d7fd-2a80-4f45-a716-f22a573d9972', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Debug-Session-Id': '593439' }, body: JSON.stringify({ sessionId: '593439', hypothesisId: 'H3', location: 'main.js:initPredictionResults', message: 'early_exit_no_scenario_keys', data: {}, timestamp: Date.now() }) }).catch(() => {});
    // #endregion
    return;
  }

  const baseline = { ...ctx.apiPayloadBaseline };
  let current = { ...baseline };
  const box = resultCard.querySelector('#scenarioControls');
  const btnReset = resultCard.querySelector('#btnScenarioReset');
  if (!box) return;

  let scenarioAbort = null;
  let scenarioReqGen = 0;

  function setScenarioError(msg) {
    const el = resultCard.querySelector('#scenarioApiError');
    if (!el) return;
    if (!msg) {
      el.textContent = '';
      el.hidden = true;
      return;
    }
    el.textContent = msg;
    el.hidden = false;
  }

  function buildControls() {
    box.innerHTML = '';
    keys.forEach((key) => {
      const b = ctx.bounds[key] || {};
      const display = (ctx.displayNames && ctx.displayNames[key]) || key;
      const help = (ctx.helps && ctx.helps[key]) || '';
      const row = document.createElement('div');
      row.className = 'scenario-row';
      const lab = document.createElement('label');
      lab.appendChild(document.createTextNode(`${display} `));
      const hb = document.createElement('button');
      hb.type = 'button';
      hb.className = 'param-help-btn';
      if (help) hb.setAttribute('data-help', help);
      hb.setAttribute('aria-label', 'Help');
      hb.textContent = '?';
      lab.appendChild(hb);
      row.appendChild(lab);

      if (b.type === 'categorical' && Array.isArray(b.values) && b.values.length) {
        const sel = document.createElement('select');
        sel.className = 'form-select form-select-sm';
        sel.dataset.featureKey = key;
        const vals = b.values.map((v) => String(v));
        let curS = String(current[key] == null ? '' : current[key]);
        if (!vals.includes(curS)) {
          const o0 = document.createElement('option');
          o0.value = curS;
          o0.textContent = `${curS} (submitted)`;
          sel.appendChild(o0);
        }
        b.values.forEach((v) => {
          const o = document.createElement('option');
          o.value = String(v);
          o.textContent = String(v);
          sel.appendChild(o);
        });
        sel.value = vals.includes(curS) ? curS : sel.options[0] ? sel.options[0].value : curS;
        current[key] = sel.value;
        sel.addEventListener('change', () => {
          current[key] = sel.value;
          scheduleRefresh();
        });
        row.appendChild(sel);
      } else {
        const { min, max, step } = normalizeNumericRange(key, b, current[key]);
        const rng = document.createElement('input');
        rng.type = 'range';
        rng.className = 'form-range';
        rng.dataset.featureKey = key;
        rng.min = String(min);
        rng.max = String(max);
        rng.step = String(step);
        current[key] = clampSnapNumeric(key, current[key], min, max);
        rng.value = String(current[key]);
        const cap = document.createElement('div');
        cap.className = 'small text-muted';
        cap.textContent = `Value: ${rng.value}`;
        const syncFromRange = () => {
          const v = clampSnapNumeric(key, rng.value, min, max);
          current[key] = v;
          rng.value = String(v);
          cap.textContent = `Value: ${v}`;
        };
        rng.addEventListener('input', () => {
          syncFromRange();
          scheduleRefresh();
        });
        rng.addEventListener('change', () => {
          syncFromRange();
          scheduleRefresh.flush();
        });
        row.appendChild(rng);
        row.appendChild(cap);
      }
      box.appendChild(row);
    });
  }

  function applyGauge(g) {
    if (!g) return;
    const m = resultCard.querySelector('#gaugeMarker');
    if (m) m.style.left = `${g.marker_pct}%`;
    const t10 = resultCard.querySelector('.gauge-tick-p10');
    const t90 = resultCard.querySelector('.gauge-tick-p90');
    if (t10 && g.p10_pct != null) t10.style.left = `${g.p10_pct}%`;
    if (t90 && g.p90_pct != null) t90.style.left = `${g.p90_pct}%`;
  }

  function applyApi(data) {
    if (!data || !data.success) {
      setScenarioError((data && data.error) || 'Prediction update failed.');
      return;
    }
    setScenarioError('');
    const pred = data.predicted_waste_percentage;
    const elE = resultCard.querySelector('#valExpected');
    if (elE) elE.innerHTML = `${fmtNum(pred, 2)}<span class="pct-sym">%</span>`;
    const iv = data.prediction_intervals_available;
    const p10 = data.p10;
    const p90 = data.p90;
    const v10 = resultCard.querySelector('#valP10');
    const v90 = resultCard.querySelector('#valP90');
    if (v10) {
      if (iv) v10.innerHTML = `${fmtNum(p10, 2)}<span class="pct-sym">%</span>`;
      else v10.textContent = '—';
    }
    if (v90) {
      if (iv) v90.innerHTML = `${fmtNum(p90, 2)}<span class="pct-sym">%</span>`;
      else v90.textContent = '—';
    }
    applyGauge(data.gauge);

    const imp = data.cost_co2_impact;
    const wc = resultCard.querySelector('#lineWasteCost');
    const wk = resultCard.querySelector('#lineWasteKg');
    const wco2 = resultCard.querySelector('#lineWasteCo2');
    if (wc) wc.textContent = fmtMoney(imp.waste_cost_usd);
    if (wk) wk.textContent = `${Math.round(imp.waste_kg).toLocaleString('en-US')}`;
    if (wco2) wco2.textContent = `${Math.round(imp.waste_co2_kg).toLocaleString('en-US')} kg CO₂`;

    const ts = resultCard.querySelector('#lineTotalSteel');
    if (ts && imp.total_steel_kg != null) {
      ts.textContent = Math.round(imp.total_steel_kg).toLocaleString('en-US');
    }

    const cap = resultCard.querySelector('#gaugeScaleCaption');
    if (cap && data.gauge) {
      const lo = fmtNum(data.gauge.gauge_lo, 1);
      const hi = fmtNum(data.gauge.gauge_hi, 1);
      cap.textContent = `Scale: ${lo}% → ${hi}% (neighbor-based band when available)`;
    }

    const interp = resultCard.querySelector('#interpretationText');
    if (interp && data.interpretation) interp.textContent = data.interpretation;

    const cat = data.waste_category;
    const badge = resultCard.querySelector('#categoryBadge');
    if (badge) {
      badge.textContent = cat;
      const col = CATEGORY_BADGE_CLASS[cat] || 'secondary';
      badge.className = `badge bg-${col} me-1`;
    }

    const rel = data.reliability;
    if (rel) {
      const rb = resultCard.querySelector('#reliabilityBadge');
      const rs = resultCard.querySelector('#reliabilityScoreText');
      const rm = resultCard.querySelector('#reliabilityMessage');
      const lvl = (rel.reliability_level || '').toLowerCase();
      const col = data.reliability_badge_color || RELIABILITY_BADGE_CLASS[lvl] || 'secondary';
      if (rb) {
        rb.textContent = (data.reliability_level_display || lvl.toUpperCase() || '');
        rb.className = `badge bg-${col} me-1`;
      }
      if (rs) {
        const pct =
          data.reliability_score_display ||
          (typeof rel.reliability_score === 'number'
            ? `${Math.round(rel.reliability_score * 100)}%`
            : '');
        rs.textContent = `${pct} similarity index`;
      }
      if (rm) rm.textContent = rel.message || '';
      const activeLvl = (
        data.reliability_level_display ||
        (rel.reliability_level || '').toUpperCase()
      ).trim();
      resultCard.querySelectorAll('.reliability-band').forEach((b) => {
        b.classList.remove('reliability-band--active');
      });
      const map = { HIGH: '.reliability-band--high', MEDIUM: '.reliability-band--medium', LOW: '.reliability-band--low' };
      const sel = map[activeLvl];
      if (sel) resultCard.querySelector(sel)?.classList.add('reliability-band--active');
    }
  }

  const runPredict = () => {
    const myGen = ++scenarioReqGen;
    resultCard.classList.add('result-card--scenario-updating');
    if (scenarioAbort) scenarioAbort.abort();
    scenarioAbort = new AbortController();
    const ac = scenarioAbort;
    setScenarioError('');
    const steel = readTotalSteelKg(current.total_steel_kg);
    current.total_steel_kg = steel;
    const payload = buildApiPayload(current, steel);
    // #region agent log
    fetch('http://127.0.0.1:7490/ingest/a4c0d7fd-2a80-4f45-a716-f22a573d9972', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Debug-Session-Id': '593439' }, body: JSON.stringify({ sessionId: '593439', hypothesisId: 'H4', location: 'main.js:runPredict', message: 'scenario_api_fetch', data: { gen: myGen, payloadKeys: Object.keys(payload).length }, timestamp: Date.now() }) }).catch(() => {});
    // #endregion
    fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: ac.signal,
    })
      .then(async (r) => {
        const data = await r.json().catch(() => ({}));
        if (ac.signal.aborted) return null;
        if (!r.ok) throw new Error(data.error || data.message || `HTTP ${r.status}`);
        return data;
      })
      .then((data) => {
        if (data == null || ac.signal.aborted) return;
        applyApi(data);
      })
      .catch((err) => {
        if (err.name === 'AbortError') return;
        setScenarioError(err.message || 'Network error while updating prediction.');
      })
      .finally(() => {
        if (myGen === scenarioReqGen) {
          resultCard.classList.remove('result-card--scenario-updating');
        }
      });
  };

  const scheduleRefresh = debounceFlush(runPredict, 65);

  if (btnReset) {
    btnReset.addEventListener('click', () => {
      current = { ...baseline };
      buildControls();
      scheduleRefresh.flush();
    });
  }

  buildControls();
}

/** SSR gauge ticks/marker use data-left-pct to avoid Jinja inside style="" (invalid for CSS tooling). */
function initGaugePositionsFromData(root = document) {
  root.querySelectorAll('[data-left-pct]').forEach((el) => {
    const raw = el.getAttribute('data-left-pct');
    if (raw == null || raw === '') return;
    const n = parseFloat(raw);
    if (!Number.isFinite(n)) return;
    el.style.left = `${n}%`;
  });
}

/* ─── INIT ───────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initCursor();
  initMagnetic();
  initNav();
  initScrollReveal();
  initTiltCards();
  initBackToTop();
  initStatCounters();
  initNavPrefetch();
  initParamHelpTooltips();
  initPredictionForm();
  initGaugePositionsFromData();
  const rc = document.getElementById('resultCard');
  if (rc && rc.querySelector('#predictionScenarioData')) {
    initPredictionResults(rc);
  }
});
