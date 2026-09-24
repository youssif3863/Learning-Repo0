// Render handout.html to PDF with Chromium (print CSS; A4).
const path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [,, input, output] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: output, preferCSSPageSize: true, printBackground: true, displayHeaderFooter: false, tagged: true, outline: false });
  await browser.close();
})();
