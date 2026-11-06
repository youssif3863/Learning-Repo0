// Usage: node render.js <input.html> <output.pdf>
// Renders an HTML file to PDF with Chromium (Playwright) and prints, per .page element, the content bottom (pt).
const { chromium } = require('playwright');
(async () => {
  const [, , input, output] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + input, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const bottoms = await page.evaluate(() => [...document.querySelectorAll('.page')].map(p => {
    const c = p.querySelector('.content'); if (!c) return 0;
    return Math.round((c.getBoundingClientRect().bottom - p.getBoundingClientRect().top) * 0.75);
  }));
  console.log('PAGE_BOTTOMS ' + JSON.stringify(bottoms));
  await page.pdf({ path: output, preferCSSPageSize: true, printBackground: true });
  await browser.close();
})();
