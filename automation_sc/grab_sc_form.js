// Dump visible form fields from the current SoundCloud edit page using an existing Chrome session.
// Requires Chrome launched with --remote-debugging-port=9222 and an open SoundCloud track edit tab.
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const ctx = browser.contexts()[0];
  const page = ctx.pages().find(p => p.url().includes('soundcloud.com')) || ctx.pages()[0];
  await page.bringToFront();
  await page.waitForLoadState('domcontentloaded');

  const fields = await page.evaluate(() => {
    const res = [];
    const nodes = document.querySelectorAll('input, textarea, select');
    for (const el of nodes) {
      const labels = [];
      if (el.labels) labels.push(...Array.from(el.labels).map(l => l.innerText.trim()).filter(Boolean));
      const aria = el.getAttribute('aria-label') || '';
      const placeholder = el.getAttribute('placeholder') || '';
      const name = el.getAttribute('name') || '';
      const id = el.id || '';
      const type = el.tagName.toLowerCase();
      let value = '';
      if (el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement) value = el.value;
      if (el instanceof HTMLSelectElement) value = el.value || (el.selectedOptions[0]?.value || '');
      res.push({ type, name, id, aria, placeholder, labels, value });
    }
    return res;
  });

  console.log(JSON.stringify({ url: page.url(), count: fields.length, fields }, null, 2));
  await browser.close();
})();
