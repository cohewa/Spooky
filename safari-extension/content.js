(() => {
  if (document.getElementById('halloween-decor-root')) return;

  const root = document.createElement('div');
  root.id = 'halloween-decor-root';
  root.setAttribute('aria-hidden', 'true');
  const shadow = root.attachShadow({ mode: 'closed' });
  const style = document.createElement('style');
  style.textContent = `
    :host { all: initial; position: fixed !important; inset: 0 !important; z-index: 2147483647 !important; pointer-events: none !important; }
    .candy-cursor { position: fixed; left: 0; top: 0; width: 40px; height: 42px; transform: translate(-20%, 9px); display: none; image-rendering: pixelated; }
    .candy-cursor.visible { display: block; }
  `;
  shadow.append(style);
  const candyCursor = document.createElement('img');
  candyCursor.className = 'candy-cursor';
  candyCursor.src = browser.runtime.getURL('candy-cursor.png');
  candyCursor.alt = '';
  candyCursor.draggable = false;
  shadow.append(candyCursor);
  document.documentElement.append(root);

  const cursorStyle = document.createElement('style');
  cursorStyle.id = 'halloween-decor-cursor';
  cursorStyle.textContent = `html, body, html *, body * { cursor: none !important; }`;

  let settings = { cursor: false };

  function moveCursor(event) {
    if (!settings.cursor) return;
    candyCursor.style.left = `${event.clientX}px`;
    candyCursor.style.top = `${event.clientY}px`;
    candyCursor.classList.add('visible');
  }

  document.addEventListener('pointermove', moveCursor, true);
  document.addEventListener('pointerover', moveCursor, true);
  document.addEventListener('pointerout', event => {
    if (!event.relatedTarget) candyCursor.classList.remove('visible');
  }, true);

  function apply(next) {
    if (settings.cursor !== next.cursor) {
      if (next.cursor) {
        document.documentElement.append(cursorStyle);
      } else {
        cursorStyle.remove();
        candyCursor.classList.remove('visible');
      }
    }
    settings = next;
  }

  async function sync() {
    try {
      const data = await browser.runtime.sendMessage({ type: 'halloween-settings' });
      apply({ cursor: !!data.cursor });
    } catch { apply({ cursor: false }); }
  }
  sync(); setInterval(sync, 750);
})();
