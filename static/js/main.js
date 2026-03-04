/* ═══════════════════════════════════════════════════════════════
   Steel Waste Prediction System — Main JavaScript
   NEXUS design interactions + prediction form
   ═══════════════════════════════════════════════════════════════ */

'use strict';

const lerp = (a, b, t) => a + (b - a) * t;
const raf = (fn) => requestAnimationFrame(fn);

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

  const interactives = 'a, button, .tilt-card, .nav-link, .fc-link, .btn-primary, .btn-ghost, .btn-secondary, .btn-predict';
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

/* ─── PREDICTION FORM (AJAX) ───────────────────────────────────── */
function initPredictionForm() {
  const form = document.getElementById('predictionForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const loadingEl = document.getElementById('loading');
    const resultCard = document.getElementById('resultCard');

    if (loadingEl) loadingEl.style.display = 'block';
    if (resultCard) resultCard.style.display = 'none';

    const formData = new FormData(this);
    const action = form.getAttribute('action') || '/predict';

    fetch(action, {
      method: 'POST',
      body: formData
    })
      .then(response => response.text())
      .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newResultCard = doc.getElementById('resultCard');

        if (newResultCard && resultCard) {
          if (loadingEl) loadingEl.style.display = 'none';
          resultCard.innerHTML = newResultCard.innerHTML;
          resultCard.style.display = 'block';
          resultCard.scrollIntoView({ behavior: 'smooth' });
        }
      })
      .catch(err => {
        console.error('Error:', err);
        if (loadingEl) loadingEl.style.display = 'none';
        alert('Error making prediction. Please try again.');
      });
  });
}

function resetForm() {
  const form = document.getElementById('predictionForm');
  const resultCard = document.getElementById('resultCard');

  if (form) form.reset();
  if (resultCard) resultCard.style.display = 'none';

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ─── INIT ───────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initCursor();
  initMagnetic();
  initNav();
  initScrollReveal();
  initTiltCards();
  initPredictionForm();
});
