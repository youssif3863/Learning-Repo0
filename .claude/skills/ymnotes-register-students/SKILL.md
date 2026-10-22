---
name: ymnotes-register-students
description: Register paid YMnotes students on e-teaching.site from the "[YMnotes]" emails in the ymnotes3864@gmail.com Gmail (full package → Medicine + Surgery lectures for 5 months; Mid Questions → Mid-Module Exam Questions for 2 weeks), label each handled thread "ymnotes-registered", and report. Use when asked to register / add / process YMnotes students or registration emails, and in the scheduled daily run. Parameter: window (hours of mail to scan, default 25).
---

# YMnotes student registration

Reads `[YMnotes]` registration emails, adds each student to the right group(s) of the lecturer's
course on https://e-teaching.site, labels the Gmail thread, and ends with a short report.
The procedure is the same by hand or on the schedule. **`window`** = hours of mail to scan
(default **25**: the schedule runs daily and the label prevents double work).
Site details, lessons learned and troubleshooting are in `REFERENCE.md`. Read it **only** if
something fails or the site changed.

## Requirements (if one is missing: stop, report exactly which, and tell the user how to fix it)

| # | Needed | Where it is set | Fix |
|---|--------|-----------------|-----|
| 1 | `SKILL.md`, `REFERENCE.md`, `drive.js` at `.claude/skills/ymnotes-register-students/` | repo **youssif3863/Learning-Repo0**, branch `main` (scheduled runs clone `main`) | re-add the folder and merge to `main` |
| 2 | Allow rule `Bash(node .claude/skills/ymnotes-register-students/drive.js:*)` | repo `.claude/settings.json` → `permissions.allow` | the user adds it on GitHub (the agent may not edit its own permissions) |
| 3 | `ETEACHING_EMAIL`, `ETEACHING_PASSWORD` (lecturer login) | claude.ai → the cloud **environment's** environment variables | user sets them there; never in chat |
| 4 | **Gmail** connector (ymnotes3864@gmail.com) | claude.ai → Customize → Connectors, **and** attached to the scheduled task | `mcp__Gmail__*` tools must load via ToolSearch |
| 5 | Repo attached to the session/scheduled task | scheduled task settings → Repository | — |
| 6 | Network access to `e-teaching.site` | environment network policy | — |
| 7 | Chromium `/opt/pw-browsers/chromium` + global npm `playwright` | pre-installed in the Claude Code cloud image | — |
| 8 | Optional: **n8n** connector (read-only log checks) | scheduled task connectors | the run still works without it |

Not needed: the Playwright MCP. It can't log in safely, and `drive.js` does all browser work.
Run `drive.js` from the **repo copy** at the path above. A personal copy of this skill elsewhere
won't match the allow rule (2) and will be blocked in Auto mode.

## Hard rules

- **Credentials:** never print, echo, log, test, screenshot, write or summarize `ETEACHING_EMAIL` /
  `ETEACHING_PASSWORD`. Never ask for them in chat. Only `drive.js` reads them.
- **Gmail:** read and label only. Never send, reply, forward, draft, trash, delete or mark spam.
  Never read mail older than the window.
- **n8n:** read-only. Only `search_workflows`, `search_workflow_executions`, `get_workflow_execution`,
  `get_workflow_details`. Never update, publish, unpublish, execute, archive or test a workflow.
- **Site:** only Add Student → "Save & Clear this Page", through `drive.js register`. Never Delete,
  add groups, or change course/group settings.
- **Never guess.** Missing or odd fields, unclear plan, not found, any error → leave unlabeled and report.
- **Never register a code twice.** `drive.js` dedupes on the site itself ("Already registered" plus
  the green group cards), not only by the Gmail label.

## Procedure (normal day: 3–6 tool calls)

1. **One Gmail search.** `cutoff=$(( $(date -u +%s) - window*3600 ))`, then
   `mcp__Gmail__search_threads` with query `subject:"[YMnotes]" after:<cutoff> -label:ymnotes-registered`
   and `pageSize: 50` (page through if `nextPageToken`). If there are none: reply
   **"No new YMnotes emails in the last <window> h."** and stop. Don't open the browser.
2. **Classify from subject + snippet.** Snippets carry the labeled fields in order. Call
   `get_thread` (`messageFormat: PLAIN_TEXT`) **only** when a field you need is cut off. Read
   fields by label: code = `Student Code` / `E-Teaching App Student Code`; amount = `Paid` (ACCEPTED)
   or `Amount Paid` (MANUAL REVIEW); plus `Course`.
   - Subject `REJECTED` → **Skipped** (no label).
   - `ACCEPTED` / `MANUAL REVIEW REQUIRED` → plan:

   | Course field | Amount paid | Plan |
   |---|---|---|
   | `Digestive` | > 400 EGP, or blank | `full` (Medicine + Surgery lectures, 5 months) |
   | contains `Mid Questions` | ≤ 400 EGP (≈ 80), or blank | `questions` (Mid-Module Exam Questions, 14 days) |
   | `Digestive` | ≤ 400 | unclear (amount doesn't fit) |
   | contains `Mid Questions` | > 400 | unclear (amount doesn't fit) |
   | `Final` questions, a new course, or a new email format | any | unclear (no rule yet) |

   - Several emails with one code → one entry. Keep all its thread ids and its email type.
   - Optional, for an unclear email only (blank or odd field): if the n8n tools exist, look up
     that registration in workflow **`J3tPverV4M8GmATX`** ("YMnotes Enhanced Course Submission (3-Layer
     Verification) _Published"). Use `search_workflow_executions` with `startedAfter` = cutoff, then
     `get_workflow_execution` with `includeData: true, truncateData: 1`. Use it **only** to
     confirm a field the email itself shows. If it doesn't settle the question, leave the entry unclear.
3. **One driver call for everyone** (one login, about 2 min + 40 s per student), run from the repo root
   exactly like this, with no pipes or prefixes and a 600000 ms timeout:
   `node .claude/skills/ymnotes-register-students/drive.js register '[{"code":"94599","plan":"full"},{"code":"12345","plan":"questions"}]'`
   Pass only `full` / `questions` entries. Unclear ones never go to the site. Output is one
   `RESULT {...}` line per student:
   - `registered`: saved and re-verified on the site.
   - `already`: already in the plan's groups. No change.
   - `unclear`: e.g. already in other groups, so the shared course expiry would change. Left for the user.
   - `failed`: not found, page error, save not confirmed.
   - Exit code **3** = login failed: **do not retry** (risk of locking the account). Report it.
   - `--dry-run` fills the form without saving (manual testing only).
4. **Label.** `mcp__Gmail__label_thread` with `ymnotes-registered` on **all** threads of codes that came
   back `registered` or `already`. Get the id from `list_labels` (it was `Label_1`), and create the
   label if it's missing. Never label unclear, failed or REJECTED threads.
5. **Report** (short; no credentials, student emails or phone numbers):
   ```
   YMnotes registration — <date, Cairo>, window <window> h
   Registered: <code> <name> — Medicine + Surgery until <date> | Mid-Module Questions until <date>
   Registered as MANUAL REVIEW (check payment): <code> <name> — <amount> <method>, reason: <reason>
   Already registered (labeled): <code> <name> — until <date>
   Skipped: <code> — REJECTED: <reason>
   Failed / unclear (left unlabeled): <code> — <why>
   ```
   Leave out empty sections. Registered MANUAL REVIEW students always get their own section.
