/* ═══════════════════════════════════════════════════════════════
   NEXUS — main.js
   Interactions, Animations, Particle Systems
   ═══════════════════════════════════════════════════════════════ */

'use strict';

/* ─── UTILITIES ──────────────────────────────────────────────── */
const lerp = (a, b, t) => a + (b - a) * t;
const clamp = (v, min, max) => Math.min(Math.max(v, min), max);
const map = (v, a, b, c, d) => c + ((v - a) / (b - a)) * (d - c);
const raf = (fn) => requestAnimationFrame(fn);

/* ─── SYSTEM CLOCK ───────────────────────────────────────────── */
function initClock() {
  const el = document.getElementById('systemClock');
  if (!el) return;
  function tick() {
    const now = new Date();
    const h = String(now.getUTCHours()).padStart(2, '0');
    const m = String(now.getUTCMinutes()).padStart(2, '0');
    const s = String(now.getUTCSeconds()).padStart(2, '0');
    el.textContent = `${h}:${m}:${s} UTC`;
  }
  tick();
  setInterval(tick, 1000);
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
    cursor.style.top  = my + 'px';
  });

  // Smooth follower
  function animateFollower() {
    fx = lerp(fx, mx, 0.1);
    fy = lerp(fy, my, 0.1);
    follower.style.left = fx + 'px';
    follower.style.top  = fy + 'px';
    raf(animateFollower);
  }
  animateFollower();

  // Expand on interactive elements
  const interactives = 'a, button, .tilt-card, .nav-link, .panel-action, .fc-link, .orbital-module';
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

/* ─── MAGNETIC BUTTONS ───────────────────────────────────────── */
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

/* ─── NAVBAR ─────────────────────────────────────────────────── */
function initNav() {
  const nav = document.getElementById('navDock');
  if (!nav) return;

  let lastY = 0;
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    nav.classList.toggle('scrolled', y > 60);
    lastY = y;
  }, { passive: true });

  // Active section tracking
  const sections = document.querySelectorAll('section[id]');
  const links = document.querySelectorAll('.nav-link[data-section]');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        links.forEach(l => {
          l.classList.toggle('active', l.dataset.section === id);
        });
      }
    });
  }, { threshold: 0.4 });

  sections.forEach(s => observer.observe(s));

  // Smooth scroll
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const id = link.dataset.section;
      const target = document.getElementById(id);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
}

/* ─── HERO PARTICLE CANVAS ───────────────────────────────────── */
function initHeroCanvas() {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let W, H, particles, mouse = { x: -999, y: -999 };

  function resize() {
    W = canvas.width  = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
    createParticles();
  }

  function createParticles() {
    const count = Math.floor((W * H) / 9000);
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * W,
      y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      r: Math.random() * 1.5 + 0.4,
      color: Math.random() > 0.6
        ? `rgba(16,185,129,${Math.random() * 0.6 + 0.2})`
        : Math.random() > 0.5
          ? `rgba(6,182,212,${Math.random() * 0.4 + 0.1})`
          : `rgba(59,130,246,${Math.random() * 0.3 + 0.1})`,
      opacity: Math.random() * 0.8 + 0.2,
    }));
  }

  const CONNECTION_DIST = 120;
  const MOUSE_DIST = 150;

  function draw() {
    ctx.clearRect(0, 0, W, H);

    // Draw connections
    for (let i = 0; i < particles.length; i++) {
      const a = particles[i];
      for (let j = i + 1; j < particles.length; j++) {
        const b = particles[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONNECTION_DIST) {
          const alpha = (1 - dist / CONNECTION_DIST) * 0.12;
          ctx.strokeStyle = `rgba(16,185,129,${alpha})`;
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    // Draw particles
    particles.forEach(p => {
      // Mouse repulsion
      const dx = p.x - mouse.x;
      const dy = p.y - mouse.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < MOUSE_DIST) {
        const force = (1 - dist / MOUSE_DIST) * 1.5;
        p.vx += (dx / dist) * force * 0.02;
        p.vy += (dy / dist) * force * 0.02;
      }

      // Damping
      p.vx *= 0.98;
      p.vy *= 0.98;

      p.x += p.vx;
      p.y += p.vy;

      // Wrap
      if (p.x < 0) p.x = W;
      if (p.x > W) p.x = 0;
      if (p.y < 0) p.y = H;
      if (p.y > H) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.fill();
    });

    raf(draw);
  }

  window.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });

  window.addEventListener('resize', resize);
  resize();
  draw();
}

/* ─── WAVE CANVAS (mini panel) ───────────────────────────────── */
function initWaveCanvas() {
  const canvas = document.getElementById('waveCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let t = 0;

  function draw() {
    const W = canvas.width;
    const H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    // Grid lines
    ctx.strokeStyle = 'rgba(16,185,129,0.05)';
    ctx.lineWidth = 1;
    for (let x = 0; x < W; x += 40) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    for (let y = 0; y < H; y += 30) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }

    // Wave 1
    const grad1 = ctx.createLinearGradient(0, 0, W, 0);
    grad1.addColorStop(0, 'rgba(16,185,129,0)');
    grad1.addColorStop(0.3, 'rgba(16,185,129,0.8)');
    grad1.addColorStop(0.7, 'rgba(6,182,212,0.6)');
    grad1.addColorStop(1, 'rgba(16,185,129,0)');

    ctx.beginPath();
    ctx.strokeStyle = grad1;
    ctx.lineWidth = 2;
    for (let x = 0; x <= W; x++) {
      const y = H / 2
        + Math.sin((x / W) * Math.PI * 4 + t) * 20
        + Math.sin((x / W) * Math.PI * 7 + t * 1.3) * 10
        + Math.sin((x / W) * Math.PI * 2 + t * 0.7) * 8;
      x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Fill beneath
    ctx.beginPath();
    for (let x = 0; x <= W; x++) {
      const y = H / 2
        + Math.sin((x / W) * Math.PI * 4 + t) * 20
        + Math.sin((x / W) * Math.PI * 7 + t * 1.3) * 10
        + Math.sin((x / W) * Math.PI * 2 + t * 0.7) * 8;
      x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.closePath();
    const fillGrad = ctx.createLinearGradient(0, H / 2, 0, H);
    fillGrad.addColorStop(0, 'rgba(16,185,129,0.08)');
    fillGrad.addColorStop(1, 'rgba(16,185,129,0)');
    ctx.fillStyle = fillGrad;
    ctx.fill();

    t += 0.018;
    raf(draw);
  }

  draw();
}

/* ─── CTA CANVAS (ambient) ───────────────────────────────────── */
function initCtaCanvas() {
  const canvas = document.getElementById('ctaCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let t = 0;

  function resize() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  }

  function draw() {
    const W = canvas.width;
    const H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    // Concentric glow rings
    for (let i = 0; i < 4; i++) {
      const r = (150 + i * 100) + Math.sin(t + i) * 20;
      const alpha = (0.06 - i * 0.012) * (1 + Math.sin(t * 0.5 + i) * 0.3);
      const grad = ctx.createRadialGradient(W / 2, H / 2, r * 0.7, W / 2, H / 2, r);
      grad.addColorStop(0, `rgba(16,185,129,0)`);
      grad.addColorStop(0.8, `rgba(16,185,129,${alpha})`);
      grad.addColorStop(1, `rgba(16,185,129,0)`);
      ctx.beginPath();
      ctx.arc(W / 2, H / 2, r, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(16,185,129,${alpha * 1.5})`;
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    t += 0.01;
    raf(draw);
  }

  window.addEventListener('resize', resize);
  resize();
  draw();
}

/* ─── SCROLL REVEAL ──────────────────────────────────────────── */
function initScrollReveal() {
  const elements = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const delay = el.dataset.delay || '0';
        setTimeout(() => {
          el.classList.add('revealed');
        }, parseInt(delay));
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

  elements.forEach(el => observer.observe(el));
}

/* ─── COUNTER ANIMATION ──────────────────────────────────────── */
function initCounters() {
  const counters = document.querySelectorAll('.stat-value[data-count]');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseFloat(el.dataset.count);
      const isFloat = String(target).includes('.');
      const duration = 1800;
      const start = performance.now();

      function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const value = target * eased;
        el.textContent = isFloat ? value.toFixed(1) : Math.round(value);
        if (progress < 1) raf(update);
      }

      raf(update);
      observer.unobserve(el);
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}

/* ─── 3D TILT CARDS ──────────────────────────────────────────── */
function initTiltCards() {
  document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width  - 0.5;
      const y = (e.clientY - rect.top)  / rect.height - 0.5;
      const rotX = -y * 10;
      const rotY =  x * 10;
      card.style.transform = `perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(1.02)`;
      card.style.transition = 'none';

      // Shine effect
      const shine = card.querySelector('.card-shine');
      if (shine) {
        shine.style.background = `radial-gradient(circle at ${(x+0.5)*100}% ${(y+0.5)*100}%, rgba(255,255,255,0.06), transparent 60%)`;
      }
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      card.style.transition = 'transform 0.6s cubic-bezier(0.16,1,0.3,1)';
    });
  });
}

/* ─── ORBITAL MODULES POSITIONING ───────────────────────────── */
function initOrbit() {
  const container = document.getElementById('featuresOrbit');
  if (!container) return;

  const modules = container.querySelectorAll('.orbital-module');
  const cx = container.offsetWidth / 2;
  const cy = container.offsetHeight / 2;
  const radius = 175;

  modules.forEach(module => {
    const angle = parseFloat(module.dataset.angle || 0);
    const rad = (angle - 90) * (Math.PI / 180);
    const x = cx + Math.cos(rad) * radius - 28;
    const y = cy + Math.sin(rad) * radius - 28;
    module.style.transform = `translate(${x - cx}px, ${y - cy}px)`;
  });

  // Slow animation orbit
  let t = 0;
  function animateOrbit() {
    modules.forEach((module, i) => {
      const baseAngle = parseFloat(module.dataset.angle || 0);
      const wobble = Math.sin(t * 0.8 + i) * 3;
      const rad = (baseAngle - 90 + wobble) * (Math.PI / 180);
      const x = cx + Math.cos(rad) * radius - 28;
      const y = cy + Math.sin(rad) * radius - 28;
      module.style.left = x + 'px';
      module.style.top  = y + 'px';
      module.style.transform = '';
    });
    t += 0.01;
    raf(animateOrbit);
  }
  animateOrbit();
}

/* ─── TIME SELECTOR (dashboard) ─────────────────────────────── */
function initTimeSelector() {
  document.querySelectorAll('.time-selector').forEach(selector => {
    selector.querySelectorAll('.time-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        selector.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        // Animate bars with random data
        const bars = selector.closest('.panel').querySelectorAll('.bar');
        bars.forEach(bar => {
          const h = Math.round(40 + Math.random() * 55);
          bar.style.setProperty('--h', h + '%');
          bar.classList.remove('active-bar');
        });
        // Randomly pick active bar
        const activeIdx = Math.floor(Math.random() * bars.length);
        bars[activeIdx].classList.add('active-bar');
        bars[activeIdx].style.setProperty('--h', (80 + Math.random() * 18) + '%');
      });
    });
  });
}

/* ─── PARALLAX ───────────────────────────────────────────────── */
function initParallax() {
  const hero = document.querySelector('.hero');
  if (!hero) return;

  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    const heroCanvas = document.getElementById('heroCanvas');
    const heroContent = hero.querySelector('.hero-content');
    if (heroCanvas) heroCanvas.style.transform = `translateY(${y * 0.3}px)`;
    if (heroContent) heroContent.style.transform = `translateY(${y * 0.15}px)`;
  }, { passive: true });
}

/* ─── PAGE TRANSITION ────────────────────────────────────────── */
function initTransition() {
  const overlay = document.getElementById('pageTransition');
  if (!overlay) return;

  // Intro reveal
  overlay.style.transform = 'scaleX(1)';
  overlay.style.transformOrigin = 'right';
  overlay.style.transition = 'transform 0.8s cubic-bezier(0.16,1,0.3,1) 0.1s';
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      overlay.style.transform = 'scaleX(0)';
    });
  });
}

/* ─── ENTER BUTTON ───────────────────────────────────────────── */
function initEnterButton() {
  const btn = document.getElementById('enterBtn');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const dashboard = document.getElementById('dashboard');
    if (dashboard) dashboard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
}

/* ─── RING CHART ANIMATION ───────────────────────────────────── */
function initRingCharts() {
  const rings = document.querySelectorAll('.ring-fill');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const ring = entry.target;
      const finalOffset = parseFloat(ring.getAttribute('stroke-dashoffset') || '0');
      ring.style.strokeDashoffset = '314';
      ring.style.transition = 'stroke-dashoffset 0s';
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          ring.style.transition = 'stroke-dashoffset 1.8s cubic-bezier(0.16,1,0.3,1) 0.3s';
          ring.style.strokeDashoffset = finalOffset;
        });
      });
      observer.unobserve(ring);
    });
  }, { threshold: 0.5 });

  rings.forEach(r => observer.observe(r));
}

/* ─── FEATURE CARD HOVER RIPPLE ──────────────────────────────── */
function initFeatureCardRipples() {
  document.querySelectorAll('.feature-card, .panel').forEach(card => {
    card.addEventListener('click', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const ripple = document.createElement('div');
      ripple.style.cssText = `
        position: absolute;
        left: ${x}px; top: ${y}px;
        width: 0; height: 0;
        background: radial-gradient(circle, rgba(16,185,129,0.2), transparent 70%);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        pointer-events: none;
        animation: rippleExpand 0.6s ease-out forwards;
        z-index: 0;
      `;
      card.style.position = 'relative';
      card.style.overflow = 'hidden';
      card.appendChild(ripple);
      setTimeout(() => ripple.remove(), 700);
    });
  });

  // Add keyframes dynamically
  if (!document.getElementById('rippleStyles')) {
    const style = document.createElement('style');
    style.id = 'rippleStyles';
    style.textContent = `
      @keyframes rippleExpand {
        to { width: 400px; height: 400px; opacity: 0; }
      }
    `;
    document.head.appendChild(style);
  }
}

/* ─── AMBIENT BACKGROUND GLOW FOLLOW ────────────────────────── */
function initAmbientGlow() {
  const sections = ['dashboard', 'features'];
  sections.forEach(id => {
    const section = document.getElementById(id);
    if (!section) return;
    section.addEventListener('mousemove', (e) => {
      const rect = section.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      section.style.setProperty('--glow-x', x + 'px');
      section.style.setProperty('--glow-y', y + 'px');
    });
  });
}

/* ─── TYPING EFFECT (hero eyebrow) ──────────────────────────── */
function initTypingEffect() {
  const el = document.querySelector('.eyebrow-text');
  if (!el) return;
  const text = el.textContent;
  el.textContent = '';
  el.style.opacity = '1';
  let i = 0;
  function type() {
    if (i < text.length) {
      el.textContent += text[i++];
      setTimeout(type, 50);
    }
  }
  setTimeout(type, 800);
}

/* ─── SECTION BACKGROUND PULSE ───────────────────────────────── */
function initSectionGlow() {
  // Add radial glow that follows the mouse per section
  const style = document.createElement('style');
  style.textContent = `
    #dashboard {
      background-image: radial-gradient(
        circle 600px at var(--glow-x, 50%) var(--glow-y, 50%),
        rgba(16,185,129,0.025),
        transparent
      );
    }
    #features {
      background-image: radial-gradient(
        circle 600px at var(--glow-x, 50%) var(--glow-y, 50%),
        rgba(6,182,212,0.025),
        transparent
      );
    }
  `;
  document.head.appendChild(style);
}

/* ─── SCROLL PROGRESS BAR ────────────────────────────────────── */
function initScrollProgress() {
  const bar = document.createElement('div');
  bar.style.cssText = `
    position: fixed; top: 0; left: 0; height: 2px; width: 0%;
    background: linear-gradient(90deg, #10b981, #06b6d4);
    z-index: 9995; pointer-events: none;
    transition: width 0.1s linear;
    box-shadow: 0 0 10px rgba(16,185,129,0.5);
  `;
  document.body.appendChild(bar);

  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docH = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (scrollTop / docH * 100) + '%';
  }, { passive: true });
}

/* ─── INIT ───────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initTransition();
  initClock();
  initCursor();
  initMagnetic();
  initNav();
  initScrollReveal();
  initCounters();
  initTiltCards();
  initParallax();
  initEnterButton();
  initTimeSelector();
  initFeatureCardRipples();
  initAmbientGlow();
  initSectionGlow();
  initScrollProgress();
  initTypingEffect();
  initRingCharts();

  // Canvas inits — deferred so layout is complete
  requestAnimationFrame(() => {
    initHeroCanvas();
    initWaveCanvas();
    initCtaCanvas();
    initOrbit();
  });
});
