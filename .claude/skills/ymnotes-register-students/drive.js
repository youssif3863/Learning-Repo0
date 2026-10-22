// e-teaching.site driver for the ymnotes-register-students skill.
// Usage (from repo root): node .claude/skills/ymnotes-register-students/drive.js '<json steps>'
// Logs in as the lecturer with ETEACHING_EMAIL / ETEACHING_PASSWORD from the environment. The values are
// never printed, logged, screenshotted or written anywhere; every line of output is scrubbed of them.
//
// Why the login is done "blind": with Flutter semantics (accessibility) ON, the Password field is exposed
// as a disabled <input> and cannot be typed into. With semantics OFF, Flutter creates real, enabled inputs
// when its canvas is tapped. So: page A (semantics on) reads the button/field positions, page B (semantics
// off) taps those positions to log in, then turns semantics on to navigate by role/name.
//
// Steps (run in order after login, each followed by a short wait and a semantics re-enable):
//   {"click":"text","exact":true,"nth":0}   click element with this text
//   {"role":"button","name":"x","nth":0}    click element by ARIA role + name
//   {"fill":"label","text":"value"}         focus a textbox by label and type into it
//   {"type":"text"} {"key":"Enter"} {"scroll":600} {"wait":ms} {"snap":true}
//   {"clickAt":[x,y]}                       click a viewport position (for Flutter menus whose items share one node)
//   {"boxOf":"text"}                        log the bounding box of the first element containing this text
//   {"shot":"name.png"}                     screenshot into $ET_OUT (default: OS temp dir), never in the repo
// Exit code: 0 ok, 1 step/site error, 2 missing env, 3 login aborted or failed.
const os = require('os'), path = require('path');
// Playwright is installed globally in the cloud image; resolve it from the global node_modules.
const { chromium } = require(require.resolve('playwright', {
  paths: [path.join(path.dirname(process.execPath), '..', 'lib', 'node_modules'), '/opt/node-tools/node_modules'],
}));
const E = process.env.ETEACHING_EMAIL || '', P = process.env.ETEACHING_PASSWORD || '';
const OUT = process.env.ET_OUT || os.tmpdir();
const SITE = 'https://e-teaching.site';
const VIEWPORT = { width: 1280, height: 900 };
const scrub = s => { let o = String(s); for (const v of [E, P]) if (v) o = o.split(v).join('***'); return o; };
const log = (...a) => console.log(scrub(a.join(' ')));
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function a11y(page) {
  await page.evaluate(() => { const p = document.querySelector('flt-semantics-placeholder'); if (p) p.click(); });
  await sleep(1500);
}
async function open(browser) {
  const page = await (await browser.newContext({ viewport: VIEWPORT })).newPage();
  for (let i = 1; ; i++) { // the proxy occasionally resets the first connection; retrying here is safe (nothing typed yet)
    try { await page.goto(SITE, { waitUntil: 'domcontentloaded' }); break; }
    catch (e) { if (i >= 3) throw e; log('goto retry', i, e.message.split('\n')[0]); await sleep(5000); }
  }
  await sleep(14000); // "Checking your browser" page (~8s), then Flutter boot
  return page;
}
const centre = async l => { const b = await l.boundingBox(); if (!b) throw new Error('no box'); return [b.x + b.width / 2, b.y + b.height / 2]; };

// Page A: semantics on, read where the login controls are drawn.
async function learnPositions(browser) {
  const a = await open(browser); await a11y(a);
  const R = {};
  R.dash = await centre(a.getByRole('button', { name: 'Dashboard' })); await a.getByRole('button', { name: 'Dashboard' }).click(); await sleep(2500);
  R.withEmail = await centre(a.getByRole('button', { name: 'Sign In with Email' })); await a.getByRole('button', { name: 'Sign In with Email' }).click(); await sleep(2500);
  R.email = await centre(a.getByRole('textbox', { name: 'E-Mail Address' }));
  R.pw = await centre(a.locator('input[type=password]'));
  R.signin = await centre(a.getByRole('button', { name: 'SignIn' }));
  await a.context().close();
  return R;
}

// Page B: semantics off, tap positions and type. Verifies field lengths before submitting.
async function login(browser) {
  const R = await learnPositions(browser);
  const b = await open(browser); await sleep(4000);
  const tap = async ([x, y]) => { await b.mouse.move(x - 5, y - 5); await sleep(150); await b.mouse.move(x, y); await sleep(150); await b.mouse.down(); await sleep(120); await b.mouse.up(); };
  const focused = t => b.evaluate(t => { const x = document.activeElement; return !!x && x.tagName === 'INPUT' && x.type === t && !x.disabled; }, t);
  await tap(R.dash); await sleep(3500);
  await tap(R.withEmail); await sleep(3500);
  await tap(R.email); await sleep(1500);
  if (!(await focused('text'))) return { ok: false, why: 'email field did not take focus' };
  await b.keyboard.type(E, { delay: 25 }); await sleep(800);
  await tap(R.pw); await sleep(1500);
  if (!(await focused('password'))) return { ok: false, why: 'password field did not take focus' };
  await b.keyboard.type(P, { delay: 25 }); await sleep(800);
  const lens = await b.evaluate(() => ({ t: (document.querySelector('input[type=text]') || {}).value?.length, p: (document.querySelector('input[type=password]') || {}).value?.length }));
  if (lens.t !== E.length || lens.p !== P.length) return { ok: false, why: 'field contents did not match expected lengths; not submitted' };
  await tap(R.signin); await sleep(9000);
  await a11y(b);
  // Role-selection screen after sign-in: choose Lecturer.
  const lecturer = b.getByText('Lecturer', { exact: true });
  if (await lecturer.count()) { log('ROLE screen: choosing Lecturer'); await lecturer.first().click(); await sleep(6000); await a11y(b); }
  if (await b.getByRole('button', { name: 'SignIn' }).count()) return { ok: false, why: 'still on the sign-in form after submitting (wrong credentials or site error)', page: b };
  return { ok: true, page: b };
}

// ---------- register mode ----------
// node drive.js register '[{"code":"94599","plan":"full"},{"code":"12345","plan":"questions"}]' [--dry-run]
// Prints one line per student:
//   RESULT {"code","plan","status":"registered|already|dry-run-ok|failed|unclear","student","groups","until","detail"}
// All plans live in course Digestive System_YMnotes; a plan = which group cards to turn green + how long.
const PLANS = {
  // Full package (theory, paid > 400 EGP): Medicine + Surgery lecture groups, ~5 months.
  full: { groups: ['Medicine | Lectures', 'Surgery | Lectures'], months: 5 },
  // Mid questions only (course "Digestive Mid Questions", ~80 EGP): 2 weeks.
  questions: { groups: ['Mid-Module Exam Questions'], days: 14 },
  // The site also has a "Final Exam Questions" group. No email/price rule for it yet: add a plan here when the
  // user defines one (e.g. final_questions: { groups: ['Final Exam Questions'], days: 14 }).
};
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
function cairoToday() {
  const [y, m, d] = new Intl.DateTimeFormat('en-CA', { timeZone: 'Africa/Cairo' }).format(new Date()).split('-').map(Number);
  return { y, m, d };
}
function expiry(plan) {
  const t = cairoToday();
  if (plan.months) {
    const m0 = t.m - 1 + plan.months, y = t.y + Math.floor(m0 / 12), m = (m0 % 12) + 1;
    const last = new Date(Date.UTC(y, m, 0)).getUTCDate();
    return { y, m, d: Math.min(t.d, last) };
  }
  const dt = new Date(Date.UTC(t.y, t.m - 1, t.d + plan.days));
  return { y: dt.getUTCFullYear(), m: dt.getUTCMonth() + 1, d: dt.getUTCDate() };
}
const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const snapText = page => page.locator('body').ariaSnapshot().catch(() => '');
async function waitFor(page, re, ms) {
  for (const end = Date.now() + ms; Date.now() < end; await sleep(1000)) { await a11y(page); const s = await snapText(page); if (re.test(s)) return s; }
  return null;
}
async function openAddStudent(page) {
  await page.getByRole('button', { name: 'Courses' }).click(); await sleep(4000); await a11y(page);
  await page.getByRole('button', { name: 'Digestive System_YMnotes' }).click(); await sleep(5000); await a11y(page);
  await page.getByRole('tab', { name: 'Groups' }).click(); await sleep(5000); await a11y(page);
  await page.getByRole('button').last().click(); await sleep(3000); await a11y(page); // floating menu, bottom-right
  // The menu items (Add Student / All Students / Add new Group / Delete) share ONE semantics node, top to bottom.
  // Click inside the top eighth of that node = "Add Student"; "Delete" is the bottom quarter and is never near.
  const m = await page.getByRole('group', { name: /^Add Student/ }).first().boundingBox().catch(() => null);
  const [x, y] = m ? [m.x + m.width / 2, m.y + m.height / 8] : [630, 519];
  await page.mouse.click(x, y); await sleep(7000); await a11y(page);
  const s = await snapText(page);
  if (!/heading "Students Services"/.test(s) || !/Digestive System_YMnotes/.test(s)) throw new Error('Add Student page did not open');
}
async function search(page, code) {
  const box = page.getByRole('textbox', { name: 'Student Code' });
  await box.click(); await sleep(300);
  // Ctrl+A is unreliable in Flutter text fields, and the semantics <input> doesn't expose its value: End + Backspaces.
  await page.keyboard.press('End');
  for (let i = 0; i < 15; i++) await page.keyboard.press('Backspace');
  await page.keyboard.type(code, { delay: 20 }); await sleep(800);
  await page.mouse.click(1170, 125); // yellow magnifier search button
  await sleep(3000); // the info panel briefly empties/shows a spinner between students; don't read that as "not found"
  return (await waitFor(page, /img "[^"]*(New Student|Already registered)"/, 25000)) || '';
}
// Which group cards are green (= student is / will be in that group)? Colour is not in the accessibility tree,
// so sample a 10x10 patch inside each card's corner from a screenshot and decode it in the browser.
async function greenGroups(page) {
  const names = [...(await snapText(page)).matchAll(/button "(.+?) \[ \d+ \] Student"/g)].map(m => m[1]);
  const green = [];
  for (const name of names) {
    const b = await page.getByRole('button', { name: new RegExp('^' + esc(name) + ' \\[') }).first().boundingBox();
    if (!b) continue;
    const png = await page.screenshot({ clip: { x: b.x + 8, y: b.y + 8, width: 10, height: 10 } });
    const [r, g, bl] = await page.evaluate(async b64 => {
      const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
      const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
      const x = c.getContext('2d'); x.drawImage(img, 0, 0);
      const d = x.getImageData(0, 0, c.width, c.height).data; let s = [0, 0, 0];
      for (let i = 0; i < d.length; i += 4) { s[0] += d[i]; s[1] += d[i + 1]; s[2] += d[i + 2]; }
      return s.map(v => v / (d.length / 4));
    }, png.toString('base64'));
    if (g > r + 30 && g > bl + 30) green.push(name);
  }
  return { names, green };
}
async function pickDate(page, { y, m, d }) {
  await page.getByRole('button', { name: /Service will enable until/ }).click(); await sleep(2500); await a11y(page);
  for (let i = 0; i < 36; i++) {
    const hdr = (await snapText(page)).match(/Select year ([A-Za-z]+) (\d{4})/);
    if (!hdr) throw new Error('date picker header not found');
    const diff = (y - Number(hdr[2])) * 12 + (m - 1 - MONTHS.indexOf(hdr[1]));
    if (diff === 0) break;
    await page.getByRole('button', { name: diff > 0 ? 'Next month' : 'Previous month' }).click(); await sleep(900); await a11y(page);
  }
  await page.getByRole('button', { name: `${MONTHS[m - 1]} ${d}, ${y}` }).click(); await sleep(1200);
  await page.getByRole('button', { name: 'OK', exact: true }).click(); await sleep(2500); await a11y(page);
}
let last = {};
async function registerOne(page, { code, plan: planName }, dryRun) {
  code = String(code || '');
  if (!/^\d{4,7}$/.test(code)) return { status: 'unclear', detail: 'student code missing or malformed' };
  const plan = PLANS[planName];
  if (!plan) return { status: 'unclear', detail: `no site group configured for plan "${planName}"` };
  const s = await search(page, code);
  if (!s) return { status: 'failed', detail: 'student not found for this code (or search did not load in 28s)' };
  const who = (s.match(/img "([^"]*)(New Student|Already registered)"/) || [])[1]?.trim();
  // Guard against reading the previous student's panel when a search silently did not fire.
  if (who && last.who === who && last.code !== code) return { status: 'failed', student: who, detail: 'search showed the previous student again (stale result)' };
  last = { who, code };
  const { names, green } = await greenGroups(page);
  const missingGroups = plan.groups.filter(g => !names.includes(g));
  if (missingGroups.length) return { status: 'failed', student: who, detail: 'group(s) not on the site: ' + missingGroups.join(', ') };
  if (/Already registered/.test(s)) {
    const until = (s.match(/text: (\d{4}\/\d+\/\d+) Old Time/) || [])[1] || 'unknown';
    const need = plan.groups.filter(g => !green.includes(g));
    if (!need.length) return { status: 'already', student: who, groups: green, until, detail: 'already in the plan groups; not changed' };
    // In the course but not in this plan's groups (e.g. a full-package student now buying questions). The access
    // date is ONE per student for the whole course, so changing it could shorten/extend other access: leave to the user.
    return { status: 'unclear', student: who, groups: green, until, detail: `already in ${green.join(' + ') || 'no group'} until ${until}; needs ${need.join(' + ')} — shared course expiry, left for manual handling` };
  }
  if (!/New Student/.test(s)) return { status: 'failed', detail: 'student not found for this code' };
  if (green.length) return { status: 'unclear', student: who, groups: green, detail: 'new student but some groups already pre-selected; not changed' };
  for (const g of plan.groups) { await page.getByRole('button', { name: new RegExp('^' + esc(g) + ' \\[') }).first().click(); await sleep(1500); }
  await a11y(page);
  const sel = (await greenGroups(page)).green;
  if (sel.length !== plan.groups.length || plan.groups.some(g => !sel.includes(g)))
    return { status: 'failed', student: who, detail: `group selection is [${sel.join(', ')}] instead of [${plan.groups.join(', ')}]; not saved` };
  const t = expiry(plan), want = `${t.y}/${t.m}/${t.d}`;
  await pickDate(page, t);
  if (!(await snapText(page)).includes(`button "${want} Service will enable until"`)) return { status: 'failed', student: who, detail: 'expiry date did not set to ' + want + '; not saved' };
  if (dryRun) return { status: 'dry-run-ok', student: who, groups: plan.groups, until: want, detail: 'form filled, not saved' };
  await page.getByRole('button', { name: 'Save & Clear this Page' }).click();
  if (!(await waitFor(page, /Save & Clear this Page/, 45000))) return { status: 'failed', student: who, detail: 'save did not finish (check manually before retrying)' };
  await sleep(2000);
  last = {}; // the same student is searched again on purpose
  const v = await search(page, code); // verify on the site
  const vg = v ? (await greenGroups(page)).green : [];
  if (v && /Already registered/.test(v) && v.includes(`${want} Old Time`) && plan.groups.every(g => vg.includes(g)))
    return { status: 'registered', student: who, groups: plan.groups, until: want };
  return { status: 'failed', student: who, detail: `saved but verification did not show Already registered in ${plan.groups.join(' + ')} until ${want} (check manually, do not retry blindly)` };
}
async function registerMode(browser, list, dryRun) {
  let r = await login(browser);
  if (!r.ok) { log('LOGIN FAILED:', r.why); return 3; }
  let page = r.page, opened = false;
  for (const st of list) {
    let res;
    try {
      if (PLANS[st.plan] && !opened) { await openAddStudent(page); opened = true; }
      res = await registerOne(page, st, dryRun);
    } catch (e) {
      res = { status: 'failed', detail: e.message.split('\n')[0] };
      // Stay on the Add Student page if still there; otherwise log in again on a fresh page for the next student.
      if (!/heading "Students Services"/.test(await snapText(page))) {
        opened = false; last = {};
        await page.context().close().catch(() => {});
        r = await login(browser);
        if (!r.ok) { log('RESULT', JSON.stringify({ code: st.code, plan: st.plan, ...res })); log('LOGIN FAILED on retry:', r.why); return 3; }
        page = r.page;
      }
    }
    log('RESULT', JSON.stringify({ code: st.code, plan: st.plan, ...res }));
  }
  return 0;
}

(async () => {
  if (!E || !P) { log('ERROR missing ETEACHING_EMAIL or ETEACHING_PASSWORD'); process.exit(2); }
  if (process.argv[2] === 'register') {
    const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true, args: ['--no-sandbox'] });
    const code = await registerMode(browser, JSON.parse(process.argv[3] || '[]'), process.argv.includes('--dry-run')).catch(e => { log('ERROR', e.message.split('\n')[0]); return 1; });
    await browser.close(); process.exit(code);
  }
  const steps = JSON.parse(process.argv[2] || '[]');
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true, args: ['--no-sandbox'] });
  let code = 0, page;
  try {
    const r = await login(browser);
    page = r.page;
    if (!r.ok) {
      log('LOGIN FAILED:', r.why);
      if (page) log(await page.locator('body').ariaSnapshot().catch(() => ''));
      await browser.close(); process.exit(3);
    }
    log('LOGIN ok, url', page.url());
    for (const s of steps) {
      log('STEP', JSON.stringify(s));
      if (s.click) await page.getByText(s.click, { exact: !!s.exact }).nth(s.nth || 0).click();
      else if (s.role) await page.getByRole(s.role, { name: s.name, exact: !!s.exact }).nth(s.nth || 0).click();
      else if (s.fill) { await page.getByRole('textbox', { name: s.fill }).first().click(); await sleep(300); await page.keyboard.type(s.text, { delay: 20 }); }
      else if (s.type) await page.keyboard.type(s.type, { delay: 20 });
      else if (s.key) await page.keyboard.press(s.key);
      else if (s.scroll) await page.mouse.wheel(0, s.scroll);
      else if (s.clickAt) await page.mouse.click(s.clickAt[0], s.clickAt[1]);
      else if (s.boxOf) log('BOX', s.boxOf, JSON.stringify(await page.getByText(s.boxOf).first().boundingBox()));
      await sleep(s.wait || 2500); await a11y(page);
      if (s.shot) { await page.screenshot({ path: path.join(OUT, path.basename(s.shot)) }); log('SHOT', path.join(OUT, path.basename(s.shot))); }
      if (s.snap) log(await page.locator('body').ariaSnapshot());
    }
    log('FINAL url', page.url());
    log(await page.locator('body').ariaSnapshot());
  } catch (e) {
    code = 1;
    log('ERROR', e.message.split('\n')[0]);
    if (page) log(await page.locator('body').ariaSnapshot().catch(() => ''));
  }
  await browser.close();
  process.exit(code);
})();
