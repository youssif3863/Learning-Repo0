// e-teaching.site driver for the ymnotes-register-students skill.
// Usage (from repo root): node .claude/skills/ymnotes-register-students/drive.js '<json steps>'
// Logs in with ETEACHING_EMAIL / ETEACHING_PASSWORD from the environment. The values are never
// printed, logged, screenshotted or written anywhere; every line of output is scrubbed of them.
// Steps (run in order after login, each followed by a short wait and a re-enable of Flutter semantics):
//   {"click":"text","exact":true}           click first element with this text
//   {"role":"button","name":"x","nth":0}    click element by ARIA role + name
//   {"fill":"label","text":"value"}         focus a textbox by label and type into it
//   {"type":"text"} {"key":"Enter"} {"scroll":600} {"wait":ms} {"snap":true}
//   {"shot":"name.png"}                     screenshot into $ET_OUT (default: OS temp dir), never in the repo
const { chromium } = require('/node-tools/node_modules/playwright');
const os = require('os'), path = require('path');
const E = process.env.ETEACHING_EMAIL || '', P = process.env.ETEACHING_PASSWORD || '';
const OUT = process.env.ET_OUT || os.tmpdir();
const scrub = s => { let o = String(s); for (const v of [E, P]) if (v) o = o.split(v).join('***'); return o; };
const log = (...a) => console.log(scrub(a.join(' ')));
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function a11y(page) {
  await page.evaluate(() => { const p = document.querySelector('flt-semantics-placeholder'); if (p) p.click(); });
  await sleep(1500);
}
(async () => {
  if (!E || !P) { log('ERROR missing ETEACHING_EMAIL or ETEACHING_PASSWORD'); process.exit(2); }
  const steps = JSON.parse(process.argv[2] || '[]');
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true, args: ['--no-sandbox'] });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  let code = 0;
  try {
    await page.goto('https://e-teaching.site', { waitUntil: 'domcontentloaded' });
    await sleep(12000); await a11y(page); // "Checking your browser" page, then Flutter semantics
    await page.getByRole('button', { name: 'Dashboard' }).click(); await sleep(2000);
    await page.getByRole('button', { name: 'Sign In with Email' }).click(); await sleep(2000);
    await page.getByRole('textbox', { name: 'E-Mail Address' }).click(); await sleep(500);
    await page.keyboard.type(E, { delay: 20 }); await page.keyboard.press('Tab'); await sleep(500);
    await page.keyboard.type(P, { delay: 20 }); await sleep(300);
    await page.getByRole('button', { name: 'SignIn' }).click();
    await sleep(8000); await a11y(page);
    log('LOGIN done, url', page.url());
    for (const s of steps) {
      log('STEP', JSON.stringify(s));
      if (s.click) await page.getByText(s.click, { exact: !!s.exact }).nth(s.nth || 0).click();
      else if (s.role) await page.getByRole(s.role, { name: s.name, exact: !!s.exact }).nth(s.nth || 0).click();
      else if (s.fill) { await page.getByRole('textbox', { name: s.fill }).first().click(); await sleep(300); await page.keyboard.type(s.text, { delay: 20 }); }
      else if (s.type) await page.keyboard.type(s.type, { delay: 20 });
      else if (s.key) await page.keyboard.press(s.key);
      else if (s.scroll) await page.mouse.wheel(0, s.scroll);
      await sleep(s.wait || 2500); await a11y(page);
      if (s.shot) { await page.screenshot({ path: path.join(OUT, path.basename(s.shot)) }); log('SHOT', path.join(OUT, path.basename(s.shot))); }
      if (s.snap) log(await page.locator('body').ariaSnapshot());
    }
    log('FINAL url', page.url());
    log(await page.locator('body').ariaSnapshot());
  } catch (e) {
    code = 1;
    log('ERROR', e.message.split('\n')[0]);
    log(await page.locator('body').ariaSnapshot().catch(() => ''));
  }
  await browser.close();
  process.exit(code);
})();
