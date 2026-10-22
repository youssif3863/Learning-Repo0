---
name: ymnotes-register-students
description: Register paid YMnotes students on e-teaching.site from the "[YMnotes]" emails in the ymnotes3864@gmail.com Gmail, then label each handled thread "ymnotes-registered" and report. Use when asked to register / add / process YMnotes students or registration emails, and in the scheduled daily run. Parameter: window (hours of mail to scan, default 25).
---

# YMnotes student registration

Reads `[YMnotes]` registration emails, adds the students to the lecturer's course on
https://e-teaching.site, labels the Gmail thread, and ends with a short report.
Works the same run by hand or from the schedule. **Parameter `window`** = hours of mail to
scan (default **25**; the schedule runs once a day, and the label prevents double work).

## Requirements (check first; if any is missing, stop and tell the user exactly what to fix)

| # | What | Where it lives | Check |
|---|------|----------------|-------|
| 1 | This skill: `SKILL.md` + `drive.js` | repo `youssif3863/Learning-Repo0`, **default branch** (scheduled sessions clone the default branch) | file exists |
| 2 | Permission rule `Bash(node .claude/skills/ymnotes-register-students/drive.js:*)` | repo `.claude/settings.json` → `permissions.allow` (the agent may not edit this file itself; the user adds it) | `grep drive.js .claude/settings.json` |
| 3 | `ETEACHING_EMAIL`, `ETEACHING_PASSWORD` | the **cloud environment's** environment variables (claude.ai environment settings) | `drive.js` exits with code 2 and says "missing" if empty — never test them any other way |
| 4 | Gmail connector for ymnotes3864@gmail.com | claude.ai connectors; the scheduled task must store connector `Gmail` | `mcp__Gmail__*` tools load via ToolSearch |
| 5 | Network access to `e-teaching.site` | environment network policy | `drive.js` reaches the login page |
| 6 | Chromium `/opt/pw-browsers/chromium` + global npm `playwright` | pre-installed in the Claude Code cloud image | `drive.js` starts |

Not required: the Playwright **MCP** in `.mcp.json`. It cannot log in safely (it would need the
password typed into a tool call, and its code sandbox has no `process.env`). `drive.js` does
all browser work.

## Hard rules

- **Credentials**: never print, echo, log, screenshot, write to a file, or test the values of
  `ETEACHING_EMAIL` / `ETEACHING_PASSWORD`, and never put them in a summary. Only `drive.js`
  reads them (its output is scrubbed). Never ask the user to paste them in chat.
- **Gmail**: read and label only. Never send, reply, forward, draft, trash, delete or mark spam.
  Never read mail older than the window.
- **Site**: only Add Student (Students Services) with "Save & Clear this Page". Never click
  Delete, Add new Group, or change course/group settings. Never "Sign In with Gmail".
- **Never guess.** Missing or malformed code, unclear plan, student not found, any site error →
  leave the email unlabeled and list it under "Failed / unclear".
- Never add a student twice. Dedupe by **student code** (the site's "Already registered" check),
  not only by the Gmail label.

## Procedure (cheap path — ~6 tool calls on a normal day)

1. **Search Gmail once** (no thread reads yet):
   `cutoff=$(( $(date -u +%s) - window*3600 ))` (25 h = 90000 s), then
   `mcp__Gmail__search_threads` query `subject:"[YMnotes]" after:<cutoff> -label:ymnotes-registered`,
   `pageSize` 50 (page through if `nextPageToken`). If there are no threads: reply
   **"No new YMnotes emails in the last <window> h."** and stop.
2. **Classify from subject + snippet.** Snippets carry the labelled fields in order
   (`Student Code` / `E-Teaching App Student Code`, `Course`, `Paid` / `Amount Paid`).
   Call `mcp__Gmail__get_thread` (`messageFormat: PLAIN_TEXT`) **only** when a field you need
   is cut off or absent from the snippet. Read fields by their label, never by position.
   - Subject `REJECTED` → skip (no label, list under Skipped with the Reason).
   - `ACCEPTED` and `MANUAL REVIEW REQUIRED` → decide the plan:

   | Course field | Amount | Plan |
   |---|---|---|
   | `Digestive` | > 400 EGP | `full` |
   | `Digestive` | blank | `full` (Course is unambiguous) |
   | `Digestive` | ≤ 400 | unclear |
   | contains `Mid Questions` (e.g. `Digestive Mid Questions`, ~80 EGP) | ≤ 400 or blank | `questions` |
   | contains `Mid Questions` | > 400 | unclear |
   | anything else / new format | — | unclear |

   - Several emails with the same code → one entry; remember all their thread ids.
   - Keep the email type (ACCEPTED vs MANUAL REVIEW) for the report.
3. **Register all students in ONE call** (one login for the whole batch, ~2 min + ~40 s/student):
   ```
   node .claude/skills/ymnotes-register-students/drive.js register '[{"code":"94599","plan":"full"},{"code":"24679","plan":"questions"}]'
   ```
   Run it from the repo root, exactly in this form (the permission rule matches the prefix).
   Do not pipe or prefix it with variables. Use a 600000 ms timeout. Output: one
   `RESULT {...}` line per student, with `status` set to one of:
   - `registered`: added and re-checked on the site (shows "Already registered" with the new date).
   - `already`: the site already had them in all plan groups. No change.
   - `unclear`: bad code, no site target for the plan, or registered in only some groups.
   - `failed`: student not found, page didn't load, save not confirmed, etc.
   Add `--dry-run` to fill the form without saving (for testing).
   - Exit code 3 = login failed: do **not** retry (avoid locking the account). Report it.
4. **Label**: for every code with status `registered` or `already`, label **all** its thread ids
   with `ymnotes-registered` (`mcp__Gmail__label_thread`, label id from `list_labels`; currently
   `Label_1`. Create the label if it's missing). Never label `failed`/`unclear`/REJECTED.
5. **Report** (short, no credentials, no student emails or phone numbers):
   ```
   YMnotes registration — <date Cairo>, window <window> h
   Registered: 94599 mohamed alaa eldin — full package (Medicine + Surgery) until 2027/3/22
   Registered (MANUAL REVIEW — check payment): 94599 … — 500 EGP InstaPay, reason: …
   Already registered (labelled): 85890 kirolos Ayman — until 2027/1/31
   Skipped: 66229 REJECTED — O6U Student Code is required
   Failed / unclear (left unlabelled): 24679 — Mid Questions: no matching course on site yet
   ```
   MANUAL REVIEW students that were registered always go in their own section.

## Site facts (learned in the supervised test, 2026-10-22)

- Login: Dashboard → "Sign In with Email" → E-Mail Address + Password → "SignIn" → role
  screen → **Lecturer**. No 2FA.
- Lecturer courses: **Digestive System_YMnotes** (Digestive System, Medicine 2026/2027, First Term),
  Neurology, Endocrine_YMnotes. "Surgery" and "Medicine" are **groups** inside
  Digestive System_YMnotes: **`Medicine | Lectures`** and **`Surgery | Lectures`**.
- Full package = both groups, **access ≈ 5 months** from today (Cairo), e.g. registered
  2026-10-22 → 2027/3/22. Questions plan = 14 days, but **no Mid Questions course/group exists
  yet**. `drive.js` (`PLANS.questions = null`) reports these as unclear until the user says where
  they go. When they do, set `PLANS.questions = { groups: [...], days: 14 }` (and the course, if different).
- Add Student flow (what `drive.js register` does): Courses → Digestive System_YMnotes →
  Groups tab → bottom-right floating button → **Add Student** → "Students Services" page
  (breadcrumb ends `Digestive System_YMnotes`) → type code in **Student Code** → yellow
  magnifier → student card shows name + **"New Student"** or **"Already registered"** (with
  "Old Time to disconnect the Service" = current expiry) → tap both group cards (turn green,
  **Available Groups [2/2]**) → **Service will enable until** → date picker (Next/Previous month,
  day buttons named like `March 22, 2027`) → **OK** → **Save & Clear this Page**.
- The group's own "Valid until" (2026/12/31) is only the default for new students. The per-student
  "Service will enable until" date is what counts.

## Lessons learned (why drive.js looks the way it does)

- Flutter hides its UI until accessibility is on: click `flt-semantics-placeholder` (off-screen)
  via JS after the ~8–12 s "Checking your browser" page.
- With accessibility ON the **Password field is a disabled input**, so typing fails (and pressing
  SignIn then burns a failed login). The fix is to read control positions with accessibility on,
  log in on a **fresh page with accessibility OFF** by tapping those positions (real inputs appear),
  check both fields hold the right number of characters **before** SignIn, then turn accessibility on.
- The floating menu's items (Add Student / All Students / Add new Group / **Delete**) share one
  accessibility node, so click "Add Student" by position (630, 519 at 1280×900). Delete is far below.
- Ctrl+A doesn't clear Flutter text fields; use End + Backspaces. The semantics input doesn't
  expose its typed value.
- After a search the student panel briefly empties or shows a spinner. Wait for the
  "New Student"/"Already registered" card, not for "Not Available".
- Save takes several seconds (spinner). Confirm by searching the code again ("Already registered" +
  new date) and don't trust the click alone.
- The proxy sometimes resets the first connection to the site; `drive.js` retries page loads
  (never the password submit).
- In Auto permission mode, ad-hoc scripts that read the credentials and edits to
  `.claude/settings.json` are blocked. Only the allow-listed `drive.js` command runs. Don't try
  to work around a block: tell the user.
- Cost: never explore the site during a scheduled run. Never use the Playwright MCP for this.
  Never read full threads that the snippet already covers. Do one `drive.js register` call per run.

## Exploring / fixing the site flow (manual sessions only)

`node .claude/skills/ymnotes-register-students/drive.js '<json steps>'` logs in and runs steps
(`role`/`name`, `click` text, `fill`, `clickAt`, `shot`, `snap`, `boxOf`; see the file header),
then prints a scrubbed accessibility snapshot. Screenshots go to `$ET_OUT` (default OS temp dir)
and must never show the login form. Use it only when the site changed and `register` fails.
