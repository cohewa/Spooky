browser.runtime.onMessage.addListener((message) => {
  if (message?.type !== 'halloween-settings') return;
  return fetch('http://127.0.0.1:47831/settings', { cache: 'no-store' })
    .then(response => response.ok ? response.json() : {})
    .catch(() => ({}));
});
