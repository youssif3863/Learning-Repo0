# ymnotes-register-students — reference

Read this only when a run fails or the site changed. Learned in the supervised setup on 2026-10-22.

## Site map (lecturer account, English UI, Flutter web app)

- Login: Dashboard → **Sign In with Email** (never "Sign In with Gmail") → E-Mail Address + Password →
  **SignIn** → role screen → **Lecturer** → Home Page. No 2FA.
- Home → Categories → **Courses** → *Lecturer Courses*: `Digestive System_YMnotes` (Digestive System,
  Medicine, 2026/2027, First Term, Dr. Youssef Mohammed Hamdy), `Neurology`, `Endocrine_YMnotes`.
- `Digestive System_YMnotes` → *Course Info Page* → **Groups** tab. There are 4 groups:
  `Final Exam Questions`, `Mid-Module Exam Questions`, `Medicine | Lectures`, `Surgery | Lectures`.
- Floating button (bottom-right) → menu: **Add Student** / All Students / Add new Group / **Delete**.
- **Add Student** → *Students Services* page, breadcrumb `Digestive System > Medicine > 2026/2027 >
  Digestive System_YMnotes`:
  - **Student Code** box → yellow magnifier → card with name + city + **New Student** or
    **Already registered**, plus "Old Time to disconnect the Service" (the current expiry).
  - **Available Groups [ total / selected ]**: tap a card to toggle it. **Green = selected / member.**
  - **Service will enable until** → date picker (Previous/Next month, days named like
    `March 22, 2027`, Select year, Cancel, **OK**).
  - Bottom: **Save & Exit**, **Save & Clear this Page** (used: it stays on the page for the next student), Cancel.
- The expiry date is **one per student for the whole course**, not per group. Each group's
  "Valid until" (e.g. 2026/12/31) is only a default.

## Plans (edit `PLANS` in drive.js to change)

| Plan | Groups | Access |
|---|---|---|
| `full` (theory, > 400 EGP) | Medicine \| Lectures + Surgery \| Lectures | 5 months from today (Cairo), same day of month |
| `questions` (Mid Questions, ≈ 80 EGP) | Mid-Module Exam Questions | 14 days |
| (none yet) | Final Exam Questions | Ask the user for the email/price rule before adding a plan |

Mixed case: a student already in some groups who buys another plan comes back `unclear`. The
shared expiry date would have to change, so the user decides.

## Lessons learned (each cost several attempts)

1. Playwright **MCP** can't log in safely: typing needs the password in a tool call, and its code sandbox
   has no `process.env`. So everything goes through `drive.js` with the allow rule.
2. In **Auto** permission mode, ad-hoc scripts that read the credentials, and edits to
   `.claude/settings.json`, are blocked by the safety classifier. Only the allow-listed `drive.js` command
   runs. Don't work around a block: tell the user.
3. The first load shows "Checking your browser" (~8–12 s). Flutter hides its UI from automation until
   accessibility is on: click `flt-semantics-placeholder` via JS.
4. **With accessibility on, the Password field is a disabled `<input>`.** Typing goes nowhere, and SignIn
   then burns a failed login. Fix: read the control positions on a page with accessibility on, then log
   in on a **fresh page with accessibility off** by tapping those positions (real enabled inputs
   appear). Check both fields hold the expected number of characters **before** SignIn, then turn
   accessibility on.
5. Menu items share one accessibility node. Click "Add Student" at the top eighth of that node's box,
   far from "Delete" at the bottom.
6. Ctrl+A doesn't clear Flutter fields, and the semantics input doesn't expose its value: use End +
   15 × Backspace.
7. After a search the panel briefly empties or shows a spinner. Wait for the "New Student" / "Already
   registered" card. If the same name shows for a different code, it's a stale result and counts as failed.
8. Card color (green) isn't in the accessibility tree. `drive.js` screenshots a 10×10 patch of each
   card and decodes it in the browser.
9. Saving takes several seconds. Confirm by searching the code again ("Already registered" + the new date
   + green groups), not by trusting the click.
10. The proxy sometimes resets the first page load; `drive.js` retries page loads, but never the password submit.
11. Cost: never explore the site or use the MCP in a scheduled run, don't read full threads the snippet
    covers, use one `register` call per run, and skip the browser entirely when there's no mail.

## Troubleshooting with the step runner (manual sessions only)

`node .claude/skills/ymnotes-register-students/drive.js '<json steps>'` logs in, runs the steps and prints a
scrubbed accessibility snapshot. Steps: `{"role":"button","name":"x","nth":0}`, `{"click":"text"}`,
`{"fill":"label","text":"v"}`, `{"clickAt":[x,y]}`, `{"key":"Enter"}`, `{"shot":"f.png"}` (to `$ET_OUT`, default OS
temp; never on the login form), `{"snap":true}`, `{"wait":ms}`. Example: open the Add Student page:
`[{"role":"button","name":"Courses","wait":4000},{"role":"button","name":"Digestive System_YMnotes","wait":5000},{"role":"tab","name":"Groups","wait":5000},{"role":"button","nth":-1,"wait":3000},{"clickAt":[630,519],"wait":7000}]`.
Use `register ... --dry-run` to test a change without saving.

## Where the emails come from

n8n workflow `J3tPverV4M8GmATX` ("YMnotes Enhanced Course Submission (3-Layer Verification) _Published",
active): validates the form, dedupes and applies promos, runs an AI payment check, logs to Sheets, and emails
student + admin. ACCEPTED = all checks passed; MANUAL REVIEW = the payment proof needs a human; REJECTED =
failed validation. Read-only access only.
