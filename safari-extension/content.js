(() => {
  if (window.top !== window || document.getElementById('halloween-decor-root')) return;

  const root = document.createElement('div');
  root.id = 'halloween-decor-root';
  root.setAttribute('aria-hidden', 'true');
  const shadow = root.attachShadow({ mode: 'closed' });
  const style = document.createElement('style');
  style.textContent = `
    :host { all: initial; position: fixed; inset: 0; z-index: 2147483647; pointer-events: none; }
    .web { position: fixed; top: 0; width: 136px; height: 136px; opacity: .74; filter: drop-shadow(0 2px 2px #2c162244); }
    .web svg, .skeleton svg { width: 100%; height: 100%; }
    .left { left: 0; } .right { right: 0; transform: scaleX(-1); }
    .skeleton { position: fixed; top: -116px; width: 76px; height: 102px; animation: fall var(--duration) cubic-bezier(.25,.55,.45,1) forwards; opacity: .94; }
    @keyframes fall { 0% { transform: translateY(-115px) rotate(-14deg); opacity: 0 } 11% { opacity: 1 } 70% { transform: translateY(var(--fall)) rotate(13deg); opacity: 1 } 88% { transform: translateY(var(--fall)) rotate(4deg); opacity: 1 } 100% { transform: translateY(calc(var(--fall) + 35px)) rotate(4deg); opacity: 0 } }
    @media (prefers-reduced-motion: reduce) { .skeleton { display: none } }
  `;
  shadow.append(style);
  document.documentElement.append(root);

  const webSVG = `<svg viewBox="0 0 140 140" xmlns="http://www.w3.org/2000/svg"><path d="M0 0 H139 M0 0 V139 M0 0 L139 139 M0 0 C45 20 95 20 139 0 M0 0 C20 45 20 95 0 139 M0 0 C54 65 92 105 139 139 M0 0 C68 42 105 83 139 139 M0 35 C24 24 42 22 70 24 M0 70 C28 45 50 40 91 43 M0 105 C39 66 72 58 113 66 M35 0 C24 22 24 42 24 70 M70 0 C45 28 40 50 43 91 M105 0 C66 39 58 72 66 113" fill="none" stroke="#d5b8a7" stroke-width="1.25" stroke-linecap="round"/></svg>`;
  const skeletonSVG = `<svg viewBox="0 0 80 108" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="#f7ebd6" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M40 41v43M20 53l20 10 20-10M24 65l16 8 16-8M25 78l15 7 15-7M40 83l-16 21M40 83l17 21M21 57L6 78M59 57l15 21"/></g><circle cx="40" cy="22" r="19" fill="#f7ebd6" stroke="#6a3e38" stroke-width="2"/><ellipse cx="32" cy="20" rx="4.5" ry="6" fill="#483039"/><ellipse cx="48" cy="20" rx="4.5" ry="6" fill="#483039"/><path d="M36 33h8M40 26l-2 5h4z" stroke="#483039" stroke-width="2" fill="none"/></svg>`;
  const cursorSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M4 3L7 27l6-7 6 8 4-3-6-8 10-1z" fill="#f9e6c5" stroke="#5a302c" stroke-width="2"/><circle cx="13" cy="13" r="2" fill="#e98842"/></svg>`;
  const cursorURL = `url("data:image/svg+xml,${encodeURIComponent(cursorSVG)}") 4 3, auto`;
  const cursorStyle = document.createElement('style');
  cursorStyle.id = 'halloween-decor-cursor';
  cursorStyle.textContent = `html, body, body *:not(input):not(textarea):not(select):not(option):not([contenteditable]):not([contenteditable] *) { cursor: ${cursorURL} !important; } input, textarea, select, option, [contenteditable], [contenteditable] * { cursor: text !important; }`;

  let settings = { webs: false, skeletons: false, cursor: false };
  let nextBurst = Date.now() + 8000;
  let burstTimer;

  function apply(next) {
    if (settings.webs !== next.webs) {
      shadow.querySelectorAll('.web').forEach(el => el.remove());
      if (next.webs) for (const side of ['left', 'right']) {
        const web = document.createElement('div'); web.className = `web ${side}`; web.innerHTML = webSVG; shadow.append(web);
      }
    }
    if (settings.cursor !== next.cursor) {
      if (next.cursor) document.documentElement.append(cursorStyle); else cursorStyle.remove();
    }
    if (settings.skeletons && !next.skeletons) shadow.querySelectorAll('.skeleton').forEach(el => el.remove());
    settings = next;
  }

  function burst() {
    if (!settings.skeletons || document.hidden || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const count = Math.random() < .5 ? 2 : 3;
    for (let i = 0; i < count; i++) {
      const skeleton = document.createElement('div');
      skeleton.className = 'skeleton';
      skeleton.innerHTML = skeletonSVG;
      skeleton.style.left = `${12 + Math.random() * 76}vw`;
      skeleton.style.setProperty('--fall', `${Math.max(160, innerHeight * (.48 + Math.random() * .28))}px`);
      skeleton.style.setProperty('--duration', `${3.3 + i * .35}s`);
      skeleton.addEventListener('animationend', () => skeleton.remove(), { once: true });
      shadow.append(skeleton);
    }
  }

  async function sync() {
    try {
      const data = await browser.runtime.sendMessage({ type: 'halloween-settings' });
      apply({ webs: !!data.webs, skeletons: !!data.skeletons, cursor: !!data.cursor });
    } catch { apply({ webs: false, skeletons: false, cursor: false }); }
  }
  sync(); setInterval(sync, 750);
  burstTimer = setInterval(() => {
    if (Date.now() >= nextBurst) { burst(); nextBurst = Date.now() + 90000 + Math.random() * 90000; }
  }, 1000);
})();
