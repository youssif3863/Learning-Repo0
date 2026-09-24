// Render an HTML file to an A4 PDF with the pre-installed Chromium (print CSS).
// usage: node render.cjs input.html output.pdf
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
(async () => {
  const [, , input, output] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: output, preferCSSPageSize: true, printBackground: true,
                   displayHeaderFooter: false, tagged: true, outline: false });
  await browser.close();
})();
