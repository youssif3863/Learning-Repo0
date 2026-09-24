// Render out/handout.html to PDF with the pre-installed Chromium.
// Running header/footer are Chromium print templates (the skill's Vivliostyle
// renderer is not installed in this environment; see the completion report).
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
(async () => {
  const out = process.argv[2];
  const which = process.argv[3] || 'handout';
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'out', which + '.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const f = "font-family: Archivo, 'YM Display', sans-serif;";
  await page.pdf({
    path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: which !== 'cover', outline: true, tagged: true,
    headerTemplate: `<div style="width:100%;margin:0 17mm 0 20mm;padding-top:9mm;${f}font-size:6.8pt;letter-spacing:.14em;color:#66756C;display:flex;justify-content:space-between;border-bottom:0.3pt solid #D4DDD7;padding-bottom:1.6mm">
      <span style="color:#1A5B31;font-weight:700;letter-spacing:.06em">YMnotes</span><span>DIGESTIVE SYSTEM · ADDITIONAL TEACHING POINTS · PART 1</span></div>`,
    footerTemplate: `<div style="width:100%;margin:0 17mm 0 20mm;padding-bottom:7mm;${f}font-size:6.8pt;letter-spacing:.14em;color:#66756C;display:flex;justify-content:space-between;align-items:center">
      <span><span style="display:inline-block;width:9mm;height:1.6pt;background:#1A5B31;vertical-align:middle;margin-right:2mm"></span>YMNOTES MEDICAL · DIGESTIVE SYSTEM</span>
      <span style="background:#1A5B31;color:#fff;font-weight:700;padding:1mm 2.2mm;border-radius:1mm;letter-spacing:.04em;font-size:8pt;-webkit-print-color-adjust:exact" class="pageNumber"></span></div>`,
    margin: which === 'cover' ? { top: 0, bottom: 0, left: 0, right: 0 } : { top: '22mm', bottom: '19mm', left: '20mm', right: '17mm' },
  });
  await browser.close();
})();
