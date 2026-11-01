# YMnotes Skills — Review & Recommendations for Every Custom Skill

**Review date:** 2026-11-01  
**Scope:** all **27 skills you installed** in your Claude account, plus the second copy of `ymnotes-register-students` stored in this repository. The 13 Anthropic built-in or example skills (docx, pdf, pptx, xlsx, docs, skill-creator, morning, deep-research, google-workspace, import-memory, built-in-browser, chrome-browser, computer-use) are excluded, because they are maintained by Anthropic, not you.  
**How it was done:**
- Seven parallel review agents (Opus, medium effort), each tracing SKILL.md into its scripts, references and tests.
- I consolidated and spot-checked their findings, and ran my own cross-skill metrics.
- `premiere-basic-video-workflow` had its own deep audit earlier today ([`premiere-skill-audit/`](premiere-skill-audit/)).
- Everything was **read-only**: no skill file was changed. The skills' own offline tests were run only on scratch copies, and nothing touched a browser, account, Gmail, YouTube, Drive or social platform.

## How to use this file

When you sit down to work on one skill, jump to its section in **Part 4** (use the table of contents below). Each section stands on its own:

1. **Identity**
2. **Purpose & triggering**
3. **How it actually works** — the traced execution path, with file and line references
4. **Strengths to keep**
5. **Findings** — with evidence and severity
6. **Recommendations** — prioritised, with draft text or code
7. **Quick wins** — under 30 minutes each
8. **Open questions**

Parts 1–3 are the cross-skill view: what to fix first, and the patterns that repeat across many skills.

**Evidence labels:**
- **V-SRC** — read in the code or files
- **V-RUN** — confirmed by running something offline on a copy
- **INF** — inferred

**Severity:**
- **High** — wrong or unsafe output, a security, privacy or integrity problem, or the skill is broken
- **Med** — a reliability or quality gap
- **Low** — polish

**Path shorthands used in Part 4:**

| Shorthand | Means |
|---|---|
| `SYN/`, `<S>/`, `<skills>/` | the synced skills folder: `~/.claude/skills/synced/<org>_<id>/` |
| `REPO/` | this repository (`Learning-Repo0/`) |
| `RS/` | `REPO/.claude/skills/ymnotes-register-students/` |
| `IX/` | `SYN/incision-block5-7-exams/` |
| no prefix | a path relative to the skill's own folder |

---

## Table of contents

- [Part 1 — Overview table](#part-1--overview-table)
- [Part 2 — Do these first](#part-2--do-these-first)
- [Part 3 — Patterns across skills](#part-3--patterns-across-skills)
- [Part 4 — Skill-by-skill](#part-4--skill-by-skill)
  - **A. Video production:** [premiere-basic-video-workflow](#premiere-basic-video-workflow) · [ymnotes-premiere-shorts](#ymnotes-premiere-shorts) · [filmora-basic-video-workflow](#filmora-basic-video-workflow)
  - **B. Books & question banks:** [ymnotes-medical-book-redesign](#ymnotes-medical-book-redesign) · [ymnotes-questions](#ymnotes-questions)
  - **C. Teaching content & distribution:** [ymnotes-batch-messages](#ymnotes-batch-messages) · [ymnotes-youtube-video-finder](#ymnotes-youtube-video-finder) · [ymnotes-video-visuals](#ymnotes-video-visuals) · [ymnotes-qr](#ymnotes-qr) · [medical-visual-board](#medical-visual-board) · [etymology](#etymology)
  - **D. Operations automation:** [ymnotes-register-students](#ymnotes-register-students) · [incision-block5-7-exams](#incision-block5-7-exams)
  - **E. Developer tools:** [codex-delegate](#codex-delegate) · [graphify](#graphify)
  - **F. Community workflow skills (Matt Pocock's set):** [grill-me](#grill-me) · [handoff](#handoff) · [retro](#retro) · [teach](#teach) · [writing-for-agents](#writing-for-agents)
  - **G. Vendor skills:** [n8n official skills](#n8n-official-skills)
- [Appendix — Metrics](#appendix--metrics)

---

## Part 1 — Overview table

Health:
- 🟢 **Good** — keep, polish
- 🟡 **Fair** — fix the listed issues
- 🟠 **Needs work** — High issues affect normal use
- 🔴 **Broken / retire**

| Skill | Group | Health | Findings H/M/L | Offline tests (run on a copy) | The one thing to do first |
|---|---|---|---|---|---|
| premiere-basic-video-workflow | A | 🟡 Good core, verification gaps | see its audit (16 findings) | 702/704 pass (2 Linux-only path-case artifacts) | Hardening patch R1–R9 in `premiere-skill-audit/RECOMMENDATIONS.md` |
| ymnotes-premiere-shorts | A | 🟡 | 2 / 9 / 10 | 220 pass, 4 skipped | Make the QC gate able to FAIL; one owner approval per lecture before public posting |
| filmora-basic-video-workflow | A | 🔴 Retire | 1 / 7 / 5 | 25 pass | Turn off automatic invocation; archive once Premiere is proven (≈5 runs or 2026-12-31) |
| ymnotes-medical-book-redesign | B | 🟢 Strong, 2 High | 2 / 5 / 9 | 293 OK, 3 skipped | Stop scanned pages with a hidden OCR text layer passing as native text; resolve the clinical-update contradiction |
| ymnotes-questions | B | 🟠 | 4 / 6 / 7 | 34/35 (1 fails because sync drops `.gitignore`) | Fix answer text leaking into student PDFs and headings merging into questions |
| ymnotes-batch-messages | C | 🟡 | 2 / 5 / 6 | script ran offline OK | Fix the rule-breaking example; warn before the data expires (2027-01-21) |
| ymnotes-youtube-video-finder | C | 🟢 | 0 / 2 / 5 | no tests | Add Claude-specific verification steps; check the YMnotes catalogue first |
| ymnotes-video-visuals | C | 🟠 Not portable | 1 / 5 / 3 | no tests | Re-route image generation to Claude tools (Canva connector or graphics rendered in code) |
| ymnotes-qr | C | 🟡 | 1 / 5 / 4 | not run (deps absent) | Block non-public material from the "anyone with the link" folder |
| medical-visual-board | C | 🟠 Not portable | 1 / 4 / 3 | 14 scenarios, never run | Map its routes to Claude tools; run the scenarios |
| etymology | C | 🟢 | 0 / 2 / 6 | no evals | Fix one broken heading reference; halve the 854-character description |
| ymnotes-register-students | D | 🟠 Security | 2 / 6 / 8 | expiry function OK | Verify sender and authenticity; never auto-register MANUAL REVIEW; keep one copy |
| incision-block5-7-exams | D | 🔴 Retire | 5 / 3 / 3 | none | Disable now (academic integrity, credentials); replace with a tutoring-only skill if wanted |
| codex-delegate | E | 🟡 | 1 / 6 / 7 | doctor ran against a mock setup | Make doctor list available models and stop the permanent NEEDS-SETUP state |
| graphify | E | 🟡 | 1 / 7 / 6 | 13 pass (not the documented commands) | Fix the documented query commands (wrong argument order) |
| grill-me | F | 🔴 Broken | 1 / 1 / 1 | — | Install the upstream `grilling` skill (5 min) |
| handoff | F | 🟢 | 0 / 2 / 3 | — | Print the saved path; warn that `/tmp` is lost in cloud sessions |
| retro | F | 🟢 | 0 / 1 / 4 | — | Say where session logs live |
| teach | F | 🟢 | 0 / 2 / 4 | — | Check before writing into a git repo or a non-empty folder |
| writing-for-agents | F | 🟢 | 0 / 1 / 4 | — | Resolve its conflicting advice with skill-creator on descriptions |
| n8n official skills (7) | G | 🟡 | 4 / 4 / 3 (combined) | — | Scope their broad triggers to n8n work; install the full set or keep a core four |

---

## Part 2 — Do these first

Ordered by risk. These are the items where something wrong or unsafe can happen today.

1. **incision-block5-7-exams — disable it now.**
   - The skill takes **graded exams and certification inside other students' accounts**: per-student ledgers, "switching students", parallel operators, and a WhatsApp "your exams are done, change your password" message. It can also make the "I have studied…" attestation for the student.
   - That is likely academic misconduct and a breach of the platform's terms, and it certifies clinical procedures the student may not be competent in.
   - Remove it, or at minimum set `disable-model-invocation: true` and `allow_implicit_invocation: false`. Delete `references/whatsapp.md` and the plain-text activation codes. Stop receiving student passwords and tell affected students to change theirs.
   - If you want something in its place, build a tutoring/practice skill with **no browser or account access**. This review deliberately gives no advice on making exam-taking more effective.
2. **ymnotes-register-students — close the free-registration hole.**
   - The Gmail query selects on subject only. There is no `from:` check and no check that the email really came from your payment workflow, so a spoofed, forwarded or edited email can register someone.
   - Emails marked "MANUAL REVIEW" are registered automatically.
   - Add a sender and authenticity check. Hold MANUAL REVIEW cases for you to approve.
   - Keep **one** copy: the repo copy is the source of truth for scheduled runs, so delete or regenerate the synced copy. Both load today.
3. **ymnotes-qr — guard the public folder.**
   - Every file inherits "anyone with the link", and nothing stops paid, exam or student material from being uploaded there.
   - Add a content and folder allow-list check and an explicit confirmation step.
4. **ymnotes-premiere-shorts — let QC fail, and look before posting.**
   - The QC gate can only return PASS or WARN, so black frames, silence or a truncated export still go out publicly to up to 12 posts per lecture.
   - Add FAIL states, plus one owner review of the four Shorts (QC frames plus captions) before Stage B.
5. **ymnotes-questions — fix fidelity before the next release.** Reproduced on synthetic PDFs:
   - an indented "Answer: B" line merges into choice B **and is printed**;
   - unnumbered banks merge headings into the first question;
   - bold or colour answer keys are silently dropped;
   - "E. coli", "7.4" and "3-4 weeks" halt extraction.
6. **grill-me — 5-minute fix.** It hands off to a `grilling` skill that was never installed. Install upstream `productivity/grilling`, or paste its body in.
7. **ymnotes-batch-messages — before 2027-01-21:**
   - its semester data ends then, and it degrades silently;
   - its only worked example breaks three of its own hard rules (greeting, du'a, automated-message alert).
8. **Remove unofficial download links.** Both video skills (`premiere-basic-video-workflow` SKILL.md "Download links", `filmora-basic-video-workflow`) point to unofficial software sites. That is a malware and licensing risk. Point to official vendor installers only.
9. **ymnotes-medical-book-redesign:**
   - scanned pages with an invisible OCR text layer pass as native text, so OCR errors in doses would pass the fidelity check;
   - the skill both forbids and instructs "CORRECTED" clinical changes. Decide which rule wins.
10. **n8n skills — stop them hijacking non-n8n work.**
    - Triggers like "error", "API", "scheduled", "publish", "JavaScript" and "deploy" overlap with YMnotes runner and publishing work.
    - Add a CLAUDE.md line limiting them to n8n tasks, and file upstream issues.

---

## Part 3 — Patterns across skills

These issues repeat across skills. Fixing the pattern once, with a convention or a shared check, is cheaper than fixing each skill separately.

| # | Pattern | Where it appears | Recommendation |
|---|---|---|---|
| X1 | **Written for ChatGPT, not Claude.** The skill assumes built-in image generation or image search, ChatGPT tool names, or "Use when ChatGPT needs…" | ymnotes-video-visuals, medical-visual-board, ymnotes-youtube-video-finder; `agents/openai.yaml` in many skills; incision model presets | Add a short **"Tools by host"** section to each: Claude Code / claude.ai / ChatGPT. Claude routes: the **Canva connector** (`generate-image`, already connected), **graphics rendered in code** (HTML/SVG → PNG with Playwright, which gives pixel-exact webcam-safe zones), WebFetch / a browser for pages, and `Read` to inspect downloaded images. Remove "ChatGPT" from descriptions |
| X2 | **Gates that cannot fail.** A skipped check counted as passed, or a gate that only warns | Shorts QC (PASS/WARN only); book (skipped QA counts as pass); questions (visual review not tied to the built PDF); premiere (one-frame tolerance, orphans written as a literal); register (MANUAL REVIEW auto-registered) | Adopt a portfolio rule: **every gate has a FAIL state; SKIPPED ≠ PASS; a reviewer record names whether it was a self-review.** Add one negative test per gate (feed it a known-bad input; it must fail) |
| X3 | **Duplicate or drifting copies.** Synced caches versus production repos | register-students (repo vs synced; both load); premiere and Shorts (production code on `D:\` differs from the synced copy; the synced runner lacks the `shorts` command) | Name one source of truth per skill in its SKILL.md. Run synced copies only for reading, or regenerate them from the source repo. Add a version stamp the runtime checks |
| X4 | **The sync drops dotfiles** (`.gitignore`, `.gitattributes`) | questions packager check fails; premiere intro/outro assets excluded | Don't make runtime checks depend on dotfiles; ship non-dot equivalents or make the check tolerant |
| X5 | **Expiring data and version time bombs** | batch-messages (2027-01-21); codex model names; graphify pinned to 0.9.55+ (PyPI 0.9.100); book's page renderer (Vivliostyle) is unpinned (`npx --yes`); questions' reportlab/svglib upper limits are stale; premiere bridge 1.14.1 | Every skill with dated data or pinned tools gets an `expires`/`validated_on` field and a startup check that **warns before** expiry. Pin renderers to exact versions |
| X6 | **Public-action authority.** Standing permissions for public or consequential actions | Shorts (12 public posts per lecture, no look first); register (unattended daily run); YouTube uploads (UNLISTED by default) | Keep standing permission for *routine* steps. Require a one-line owner confirmation for each *public batch* (e.g., per lecture), with a dry-run summary |
| X7 | **Personal data and tracking.** Student names, codes and credentials in transcripts; public folders; share-tracking codes in links | register (names in reports, an example student code), incision (codes, credentials), QR (public folder), questions and book (`si=` tracking parameter in YouTube links in `brand.json`) | Report student codes only, not names; scrub snapshots; replace example codes with `00000`; remove `si=` parameters from published links |
| X8 | **Descriptions and triggers** | Long descriptions: Shorts 877 characters, etymology 854. Missing "use when": QR, questions. Broad triggers: n8n pack, incision. The register repo copy's description is invalid YAML | Keep descriptions to about 300–450 characters, built as *what it does + "Use when…" + "Not for…"*. Your 27 installed skills cost about 9.9k characters of descriptions **in every session** (about 19k with built-ins); trimming the five longest saves about 1.5k |
| X9 | **No tests or evals for most small skills; medical accuracy unevaluated** | etymology, medical-visual-board (scenarios exist but never run), video-visuals, finder, QR, batch-messages, register, community skills | Use `skill-creator`'s eval workflow: 5–10 fixed prompts per skill with expected properties, re-run after edits. For the medical skills, add a "known-answer" set (e.g., 20 terms with verified breakdowns) |
| X10 | **Missing dependencies** | grill-me → `grilling`; n8n skills → 8 sibling skills not installed (about 146 references); Shorts → production files not packaged | When installing from a collection, install its dependency closure. Add a startup "dependencies present?" check |
| X11 | **Medical-content authority is inconsistent** | book (forbids clinical updates, yet autopilot says "CORRECTED"); questions (answer leakage); Shorts (`medical_check` only checked for "TODO") | One shared YMnotes medical-fidelity policy file, referenced by every medical skill: *source-faithful by default; clinical corrections only with explicit owner approval and a cited source; never publish answer keys accidentally* |
| X12 | **Unofficial software download links** | premiere, filmora | Official vendor sources only |

---

## Part 4 — Skill-by-skill


### A. Video production

#### premiere-basic-video-workflow
**Identity:** v1.1 autopilot (frozen baseline v1.0, 2026-09-05) · in-house · 128 files / 4.4 MB · synced 2026-10-26 · entry: `node scripts/ymnotes-runner.mjs start|resume|status`, run from the **production repo on `D:\`**, never from the synced cache.

**Purpose & triggering:**
- It assembles OBS lecture recordings in Premiere Pro, removes silence, brands, verifies, exports, writes metadata, uploads to YouTube (UNLISTED) and publishes on e-teaching.site, unattended.
- The description is accurate.
- Overlap: `filmora-basic-video-workflow` (the legacy path, now superseded) and `ymnotes-premiere-shorts` (its continuation).

**Full audit:** this skill was audited in depth separately:
- [`premiere-skill-audit/PREMIERE_SKILL_AUDIT_2026-11-01.md`](premiere-skill-audit/PREMIERE_SKILL_AUDIT_2026-11-01.md) — evidence, comparison of candidates, architecture, validation plan;
- [`premiere-skill-audit/RECOMMENDATIONS.md`](premiere-skill-audit/RECOMMENDATIONS.md) — R1–R19, with draft code and pass/fail checks.

Only the summary is repeated here.

**How it actually works:**
1. Claude Code runs `ymnotes-runner.mjs`, which spawns the `premiere-pro-mcp` 1.14.1 bridge.
2. The bridge writes files into a temp folder, and a panel inside Premiere runs them as ExtendScript.
3. Silence cuts run in ONE ExtendScript loop using the undocumented, unsupported QE DOM (`qeSeq.extract()`), on a duplicated WORK sequence; SOURCE_BACKUP stays untouched.
4. Gates (ffprobe/ffmpeg) check the edit and the export.
5. There is no mouse or coordinate automation in Premiere. The e-teaching step is Chrome automation.

**Strengths to keep:**
- Production-proven: 874 cuts with frame delta 0.
- Zero generated subclips.
- BigInt tick maths.
- A branding adapter for normalized coordinates, with region verification on the delivered MP4.
- The preset pinned by SHA-256.
- Export resume without re-issuing.
- A YouTube channel guard and duplicate guard.
- A resumable runner with a lock.

**Top findings** (details and line numbers in the audit):

| # | Finding | Severity |
|---|---|---|
| P1 | The stale-timeline fingerprint guard is disabled in autopilot (`ymnotes-runner.mjs:643-646`) | High |
| P2 | The "re-verify after a version change" rule is never enforced (`host-capabilities.mjs` gets no `live` argument) | High |
| P3 | Frame rate is forced to integer/1 (29.97 would drift about 3.6 s per hour) | Med–High |
| P4 | The edit gate tolerates one frame; orphans are written as a literal `[]`; only V1/A1 are checked; no per-segment position check | Med–High |
| P5 | Long cut loops can exceed the bridge's ceiling (about 1,200 s) and be misclassified | Med |
| P6 | The speech-tail diagnostic never runs in autopilot; the −14 dBFS absolute silence threshold depends on mic gain | Med |
| P7 | Thin export gate (no A/V parity check, no full decode, no black or frozen-frame detection) | Med |
| P8 | Unofficial Premiere download link in SKILL.md | High (security) |
| P9 | Bridge 1.14.1 is 58 releases behind 1.27.0, which fixes seven known defects | Med |
| P10 | No lecture captions; no audio cleanup | Opportunity |

**Recommendations:**
1. Hardening patch R1–R9 (no install).
2. A pinned `premiere-pro-mcp@1.27.0`, after a disposable pilot (R10).
3. Local captions → YouTube draft captions (R11).
4. A Silero VAD speech-inside-cut guard (R12).
5. Hold Premiere auto-updates (R19).
6. Optional: audio finishing (R14), an XML build pilot (R15), and a UXP migration track before CEP is disabled by default in Dec 2028 (R17).

**Quick wins:**
- Turn off Premiere auto-update.
- Remove the unofficial download link.
- Fix SKILL.md's "two Shorts" (now four) and add the stage-numbering map.

**Open questions:** see audit §10: the currently installed versions, 1.27.0 behaviour on 26.3.2, and QE extract with sync-locked tracks.

[↑ back to contents](#table-of-contents)

---

#### ymnotes-premiere-shorts

**Identity:**
- Version: v6 (SKILL.md title).
- Source: claude.ai plugin `plugin_019Vfg7RRov2XyjvTrmipT3K`. The real production code lives in `D:\Github3863\…\Adobe premiere Skill` (SKILL.md:13).
- Size: 22 files, 892 KB, of which the YuNet ONNX is 232 KB and the `.epr` preset is 323 KB.
- Last updated: 2026-10-29 (manifest `updatedAt`).
- Entry points:
  - `node scripts/ymnotes-shorts.mjs run|status "<lecture>" [--social-only]`.
  - Through the production runner: `node scripts/ymnotes-runner.mjs shorts "<lecture>"`.
  - Agent-driven Stage B, which follows `references/SOCIAL_UPLOAD.md`.

**Purpose & triggering:** The skill takes the verified FINAL export of a Premiere lecture and does the following:
1. Transcribes about 9 candidate windows.
2. Drafts 4 ranked 30–60 s spans with timed captions. The model reviews this draft at exit 12.
3. Builds each Short in a separate Premiere project from PNG stills, keyframes and generated SFX.
4. Exports, runs QC, and uploads each Short UNLISTED to YouTube (Stage A).
5. Writes a `social-request.json` so the agent can post each Short publicly to Facebook, Instagram and TikTok through Claude in Chrome (Stage B), with durable receipts.

Description verdict:
- Accurate, but long (about 900 characters, always loaded). It carries implementation detail that belongs in the body: "frame-exact", "karaoke", "small 1080p copies", "durable receipts".
- No harmful overlap. It is clearly the second half of `premiere-basic-video-workflow`.
- The words "Reels/TikToks" are good triggers.
- It cannot serve Filmora lectures: it needs Premiere's `export-verification.json` and `final-structure.json`.

**How it actually works:**
1. `run()` (scripts/ymnotes-shorts.mjs:957) first checks public text on any existing plan (:962-965).
2. `prerequisites` (:120) needs a PASS `export-verification.json` and `final-structure.json`, and loads the course ledger, filtering it by export fingerprint (:137).
3. `candidates` (:145) calls `candidateWindows` (shorts-core.mjs:47). It uses topic-map anchors with an even-spread fallback and skips the opening.
4. `transcribe` (:156) calls `transcribe-windows.py`, which caches per window and runs faster-whisper int8 on CPU (transcribe-windows.py:82-87).
5. `loadPlan` (:230) does the following:
   - If no plan exists: `writeDraft` → `draftPlan` (draft-plan.mjs:154; span scoring :62-78, diversity pass :183-190), then exit 12 with `shorts-request.json`.
   - Otherwise: `validatePlan` (shorts-core.mjs:144) checks count, TODOs, duration, content range, 120 s gap, text limits and links.
6. The per-Short loop (:984-1013) runs these steps, with one retry:
   - `probeLayout`: `probe-layout.py`, a PIP-edge heuristic plus YuNet face detection with per-frame refinement.
   - `renderGraphics`: `render-graphics.py`, PIL plus arabic-reshaper and bidi, with SFX synthesised in numpy.
   - `buildShort` (:353-616): 14 video tracks, ranged `overwrite_clip` placements, `remove_from_timeline` of the carrier and extra audio, keyframes, then a structure check (:582-605).
   - `exportShort`: polls file size (:618-647).
   - `qcShort`: ffprobe plus black, freeze, volume and silence detection, and 3 PNG frames (:649-681).
7. `youtubeStageRun` (:711) calls `uploadShort` (:684). This shells out to `youtube-upload.mjs`, which is **not in this package**. It retries once with backoff, then reads the result back.
8. `socialStep` (:751) does the following:
   - Re-checks public text.
   - Gates on Stage A (`youtubeStage`, publish-orchestrator.mjs:22).
   - Reads receipts from 4 locations (social-receipts.mjs:47).
   - Runs `ensureSocialCopy` (social-copy.mjs:98): two-pass x264 under 9.5 MB.
   - Writes `posts[]` and `batches[]` (`stageBBatches`, publish-orchestrator.mjs:35).
9. The agent then posts through Chrome following SOCIAL_UPLOAD.md §2/§3/§3b/§3c and writes receipts by hand (§4). A rerun mirrors those receipts and updates the ledger and the report (:909-955).

**Strengths to keep:**
- The model reviews a deterministic draft instead of writing from scratch. TODO fields are a hard validator failure (draft-plan.mjs:229, shorts-core.mjs:155-156). This is a good shape for the "one judgement" step.
- Public-text link ban:
  - It is enforced at three points: an early check (:962), at validation, and before Stage B (:761).
  - The caption cleaner strips links again as a second line of defence (shorts-core.mjs:342-365).
  - Medical abbreviations such as H.pylori are kept on purpose.
- Idempotency is well layered:
  - Key = sha256(export fingerprint | frame range) (shorts-core.mjs:109).
  - Stage B does not start until Stage A is recorded (:765).
  - An ambiguous publish is never retried automatically (publish-orchestrator.mjs:64-66, :82).
  - A corrupt or unreadable receipt **blocks** reposting instead of allowing it (:787-791).
  - "Strongest receipt wins" merging never downgrades a PASS (social-receipts.mjs:37-44).
- Social copy:
  - It never substitutes the master.
  - Size, streams and duration are verified by ffprobe, the output is hashed, and the cache is keyed to the master fingerprint and the recipe (social-copy.mjs:20-42, :127-137).
- Assets:
  - The face model is vendored with its source, MIT licence and SHA-256 recorded (assets/models/README.md). The hash matched on check: `8f2383e4…52fa4`.
  - SFX are synthesised locally (render-graphics.py:387-420), so there is no music-copyright exposure.
- Clear human boundaries:
  - Stop at sign-in, 2FA, CAPTCHA or new terms (SKILL.md:137-138, SOCIAL_UPLOAD.md §5).
  - TikTok's "automatic content checks" prompt is declined as an account-setting change (SOCIAL_UPLOAD.md:160-161).
  - The reason for the TikTok browser route is honest: there is no audited Content Posting app (:143-148).
- Tests: the offline suite is real. 220 passed, 0 failed and 4 skipped, including a CLI integration test with stubbed libraries (V-RUN).
- Failures stay contained: one Short failing does not stop the others, and the lecture's own status is never touched.

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| S1 | **The QC gate is advisory only.** `qcShort` returns PASS or WARN, never FAIL. Black runs, freezes, long silence, wrong fps, wrong duration or near-inaudible audio only add a warning. The Short is still uploaded to YouTube, and it reaches public Stage B because WARN is accepted. Only the social copy separately re-checks 1080×1920 and duration. | scripts/ymnotes-shorts.mjs:677, :679, :712, :802, :866; social-copy.mjs:115 | V-SRC | High |
| S2 | **Nobody reviews content before it goes public, and nothing checks medical accuracy.** Standing authorisation is reused "do not ask again for each Reel". The 3 QC frames are produced but SKILL.md never tells the agent to look at them before Stage B. `medical_check` is free text that is only checked for TODO. Twelve irreversible public posts per lecture, with medical claims, rely on the model's own review. Facebook Reels cannot be edited from the web afterwards. | SKILL.md:26-28, :129-133; ymnotes-shorts.mjs:670-676; shorts-core.mjs:155-156; SOCIAL_UPLOAD.md:93-98 | V-SRC | High |
| S3 | **A re-export of the lecture brings back duplicate public posts.** The key includes the export fingerprint, so a re-export changes every key and old receipts no longer settle. The ledger's "already clipped" ranges are also filtered by the same fingerprint, so the same moments get picked again. The test suite asserts this behaviour on purpose. The only safeguard is the agent's live-profile check, and on Facebook that is a visual thumbnail comparison. | shorts-core.mjs:109; ymnotes-shorts.mjs:137; tests/shorts.mjs:219; SOCIAL_UPLOAD.md:56-59 | V-SRC + V-RUN (keys `1f243b793f` vs `478024ab91` for the same range) | Med-High |
| S4 | **Receipts are written by hand and the URL is not checked against the platform.** The agent writes the JSON into 2 files and upserts a combined file itself. `receiptSettles` accepts any `https://` URL, so a TikTok URL in a Facebook receipt settles that post. | SOCIAL_UPLOAD.md:233-269; shorts-core.mjs:372-377 | V-RUN | Med |
| S5 | **Burned-in text corrections after export are silently ignored.** A caption, header or callout fix to an exported and QC'd Short with the same key is skipped as "already exported — not rebuilt". Graphics are re-rendered, but the MP4 is not, so the typo stays in the pixels. | ymnotes-shorts.mjs:990-993, :262-264 | V-SRC | Med |
| S6 | **Partial failure exits 0.** `done ? COMPLETE : FAILED` returns 0 even when only 1 of 4 Shorts exported (status PARTIAL). The SKILL.md exit table treats 0 as "processing complete". | ymnotes-shorts.mjs:1022-1027; SKILL.md:50 | V-SRC | Med |
| S7 | **Export completion is decided by 5 s of stable file size.** A pause while Premiere is writing ends the poll early. The truncated file then only gets a QC WARN (see S1). | ymnotes-shorts.mjs:636-643 | V-SRC | Med |
| S8 | **Layout silently degrades when the face model fails to load.** `make_face_detector` swallows the error, and every non-PIP frame then becomes `cam`: a 52 %-centre crop of a slide. The runner never checks `face_detector: null`. | probe-layout.py:45-48, :99, :165 | V-SRC | Med |
| S9 | **The "frame-exact" claim rests on OpenCV seeking.** It uses `CAP_PROP_POS_FRAMES` on H.264, which can land on the wrong frame with some backends. The crop is also static, using the median face x: no tracking within a segment. A large face on a slide (over 16 % of height) is classified as `cam`. | probe-layout.py:86-89, :97, :154-155 | INF | Low-Med |
| S10 | **The package is not self-contained, and the synced runner is stale.** It imports `scripts/lib/{workflow-config,autopilot,mcp-client}.mjs` and calls `youtube-upload.mjs`, none of which are in the package. The synced `premiere-basic-video-workflow/scripts/ymnotes-runner.mjs` has **no `shorts` command and no S17**, so SKILL.md:33 fails from synced copies. It only works from the D:\ production repository. | ymnotes-shorts.mjs:32-34, :694; SKILL.md:11-13, :33; grep of the sibling runner found 0 "shorts" hits | V-SRC | Med |
| S11 | **Browser automation and platform terms.** Meta, Instagram and TikTok terms restrict automated interaction. Posting by an agent-driven browser, three platforms in parallel, at 12 posts per lecture, risks account flags. An official route exists for Facebook and Instagram that the docs don't mention: the Graph API Reels publishing, usable in development mode for accounts with roles on the app. | SKILL.md:90-93; SOCIAL_UPLOAD.md:201-228 | INF (check current terms) | Med |
| S12 | **Concurrency adds risk for little gain.** The three-tab parallel flow means typing a caption or clicking Post in the wrong tab is possible. SOCIAL_UPLOAD contradicts itself: "Work in **one selected task tab**" (§0) versus "three dedicated task tabs" (§3c). §0 still says "the two named accounts". | SOCIAL_UPLOAD.md:33, :35, :208-217 | V-SRC | Med |
| S13 | **The small social copy lowers public quality.** It is 1080×1920 at about 1.13 Mbps for a 60 s Short (`74000/60-100`), compared with a 10 Mbps master. The text-heavy graphics then get re-encoded again by each platform. The cap exists only because the Chrome `file_upload` tool limit is about 10 MB. | social-copy.mjs:7, :11-17; SOCIAL_UPLOAD.md:23-25 | V-SRC/INF | Low-Med |
| S14 | **An ad-hoc public-copy path for legacy Shorts.** For legacy CTA masters, the agent is told to build its own ffmpeg overlay copy ("precedent Digestive 18"). That copy bypasses `ensureSocialCopy` validation and the copy cache. | SOCIAL_UPLOAD.md:194-199 | V-SRC | Low-Med |
| S15 | **The link check covers YouTube domains only.** A shortener or other URL in burned-in header, captions or callouts passes, for example `bit.ly/abc`. Social captions are cleaned, but the burned-in pixels are not. | shorts-core.mjs:122 | V-RUN | Low |
| S16 | **Caption rules contradict each other.** The playbook says "≤ 64 chars, ≤ 3.8 s" in one place, "≤ 38 chars, 0.9–2.6 s" in another, and "1.2–4.5 s, two lines max" in a third. SKILL.md says one line ≤ 38. | SHORTS_PLAYBOOK.md:46-47, :70, :80; SKILL.md:73 | V-SRC | Low |
| S17 | **Broken and stale references.** `CONFIG_PATCH.md` does not exist. A comment still says "three in v4". The "Runner" paragraph repeats "master export/QC" twice. SKILL.md carries v5/v6 changelogs. | SKILL.md:22, :116, :140-156; draft-plan.mjs:6; SHORTS_PLAYBOOK.md:146 | V-SRC | Low |
| S18 | **The export preset is fixed at 30p.** The sequence fps must match the lecture fps. If the preset and the source differ, QC `fps_matches` only warns (see S1). | assets/export-presets/…30p…epr; ymnotes-shorts.mjs:665 | INF | Low |
| S19 | **The drafter rewards English-term density.** `edu = 3 + 1.5·terms` favours jargon-dense spans. There is at most one candidate per window, so roughly 9 spans compete for 4 picks. Duplicate concepts are only caught by exact string match within the plan, not against the course ledger. | draft-plan.mjs:72, :157-177; shorts-core.mjs:225 | V-SRC/INF | Low |
| S20 | **Personal data.** The owner's personal name appears in public-page instructions. It is a public page, so this is noted only. | SKILL.md:103; SOCIAL_UPLOAD.md:75 | V-SRC | Low |
| S21 | **The Python helpers have no tests.** There are no tests for probe-layout, render-graphics or transcribe-windows. `cv2` is not installed in the review container, so these could not be run. | tests/*; requirements-shorts.txt | V-RUN | Low |

**Recommendations:**

1. **Make QC a real gate** (fixes S1, S7, S18). Effort: S.
   - Split the checks into blocking and advisory:
     - Blocking: `video_stream`, `size_1080x1920`, `fps_matches`, `audio_stream`, `duration`, `duration_30_60`, `no_black`, `audible`.
     - Advisory: `no_freeze` and `no_long_silence`, because slides can legitimately freeze.
   - Draft code:

     ```js
     const BLOCKING = new Set(["video_stream","size_1080x1920","fps_matches","audio_stream","duration","duration_30_60","no_black","audible"]);
     const status = checks.some(c => c.status==="FAIL" && BLOCKING.has(c.id)) ? "FAIL" : checks.every(c=>c.status==="PASS") ? "PASS" : "WARN";
     // in run(): if (rec.qc === "FAIL") { rec.exported = false; throw new Error("QC FAIL: …") }  → retried once, then warning; never uploaded
     ```

   - Change export completion to stable size for 3 consecutive polls *and* `ffprobe` duration within tolerance before returning.

2. **Add one owner approval per lecture before anything public** (fixes S2). Effort: M.
   - After Stage A, the runner writes `<lecture>/Shorts/PUBLISH_REVIEW.md`. Per Short it contains: the YouTube unlisted link, 3 QC frames, the captions, `medical_check`, and the platform captions.
   - Stage B `posts[]` stay empty until `shorts/publish-approval.json` exists, holding `{approved_by:"owner", at, keys:[…]}` that matches the current keys.
   - SKILL.md text: *"Stage B starts only after the owner approves PUBLISH_REVIEW.md for these exact keys (one approval per lecture, not per post). Show the owner the review file and the unlisted YouTube links; never write publish-approval.json yourself."*
   - This replaces the stored, dated authorisation lines as the trust boundary for public medical content.

3. **Separate content identity from export identity** (fixes S3). Effort: M.
   - Add `content_key = sha256(job_name | round(start_s,1) | round(end_s,1) | normalized title)`. Check receipts and the ledger by `key` **or** `content_key`.
   - Don't filter `usedRanges` by fingerprint (:137). Compare by job and time overlap instead.
   - On a match with a different key, write a BLOCKED entry: *"posted earlier from a previous export; reconcile, do not repost"*.
   - Update tests/shorts.mjs:219 to expect "blocked" instead of "pending".

4. **Write receipts with a CLI, and check the platform URL** (fixes S4). Effort: S.
   - Add a subcommand: `node scripts/ymnotes-shorts.mjs receipt "<lecture>" --short short-2 --platform instagram --status PASS --url <u> [--note …]`. It calls `persistSocialReceipt` with all paths.
   - In `receiptSettles`, require the platform's domain:

     ```js
     const HOST = { facebook:/^https:\/\/(www\.)?facebook\.com\/(reel|.*\/videos)\//, instagram:/^https:\/\/www\.instagram\.com\/reel\//, tiktok:/^https:\/\/www\.tiktok\.com\/@[^/]+\/video\/\d+/ };
     ```

   - SOCIAL_UPLOAD §4 then becomes one line: *"After each confirmed post run the receipt command; never hand-edit receipt files."*

5. **Treat a burned-in text change as a rebuild** (fixes S5). Effort: S.
   - Store `render_hash = sha256(JSON(spec without out_dir))` in the record. If it differs from the exported one and the Short has no public receipts, rebuild and re-export.
   - If public posts already exist, block with "burned-in text changed after publication; owner decision".

6. **Honest exit codes** (fixes S6). Effort: S. Return a distinct code (for example 13, PARTIAL) when `0 < done < shorts.length`, and add it to the SKILL.md exit table.

7. **Make layout fail loudly** (fixes S8, S9). Effort: S.
   - `probe-layout.py` exits 2 if `--model` was given but the detector failed to load.
   - Use frame-accurate decoding: read sequentially from the bracket start instead of a per-frame `set(POS_FRAMES)`, or pre-extract with ffmpeg `-ss` before `-i` plus `select`.
   - Add a test with a synthetic 2-scene clip.

8. **Make the package self-describing** (fixes S10, S17). Effort: S.
   - Add a "Requires" block at the top of SKILL.md: *"Runs only inside the production repository (D:\…\Adobe premiere Skill) which supplies scripts/lib/*, scripts/youtube-upload.mjs and the `shorts` runner command; the claude.ai copy is reference only."*
   - Re-sync `premiere-basic-video-workflow` so its runner has S17.
   - Remove `CONFIG_PATCH.md` mentions or ship the file.
   - Move the v5/v6 changelogs to `CHANGELOG.md`.

9. **Run Stage B one platform at a time, or move Facebook and Instagram to the official API** (fixes S11, S12, S13). Effort: S (docs) / L (API).
   - Short term: keep the uploads concurrent, but type captions and click Post one tab at a time. Before typing, check that the tab URL matches the platform host.
   - Fix §0 ("three task tabs; three named accounts").
   - Medium term: a Graph API adapter for `runStageB(adapters.facebook/instagram)`, which already exists as a hook. This removes the 9.5 MB copy, the browser automation risk under the terms of service, and the visual duplicate check.

10. **Script the legacy-CTA copy** (fixes S14). Effort: M. Add a `--legacy-cta-overlay` option to `ensureSocialCopy` with the documented geometry, so the result goes through the same validation and cache.

11. **Widen the link check** (fixes S15). Effort: S. Reuse the caption cleaner's URL regex in `publicTextFailures` for burned-in fields, allowing only the medical abbreviations already listed.

12. **Make one source of truth for caption rules** (fixes S16). Effort: S. Keep only the v3 one-line rule (≤ 38 chars, 0.9–2.6 s) in the playbook. Delete :46-47 and :80, and point SKILL.md to the playbook.

13. **Trim the description** (context cost). Effort: S. Draft:
    > "Make and publish the four YMnotes teaching Shorts of a finished Premiere lecture: after premiere-basic-video-workflow exits 12 at S17_SHORTS, or when asked for YMnotes Shorts/Reels/TikToks. Edits in Premiere, uploads UNLISTED to YouTube, then posts to the YMnotes Facebook, Instagram and TikTok via Claude in Chrome. Use --social-only for existing Shorts. Not for raw OBS recordings or Filmora lectures."

**Quick wins (<30 min):**
- Change the `qcShort` status to FAIL on blocking checks (Rec 1, first half).
- Add domain regexes to `receiptSettles` and update 3 tests.
- Exit code 13 for PARTIAL.
- Make probe-layout exit non-zero when the detector fails.
- Fix SOCIAL_UPLOAD §0: one tab → three tabs, two accounts → three.
- Delete SHORTS_PLAYBOOK.md:46-47 and :80, the `CONFIG_PATCH.md` references, and the "three in v4" comment.
- Add one SKILL.md line before Stage B: *"Open each `<id>_qc_*.png` and the unlisted YouTube link; stop if a frame shows a black, cropped-slide or garbled caption."*

**Open questions:**
- Has a lecture ever been re-exported after Shorts were posted? If so, check the live profiles for duplicates now (S3).
- Does the owner want the per-lecture approval gate, or does a written standing authorisation for public medical content remain the policy (S2)?
- Are the Facebook page and the Instagram account linked as an Instagram Business or Creator account, which the Graph API route requires?
- What is the current Claude in Chrome `file_upload` size cap? If it is above 10 MB, raise `SOCIAL_MAX_BYTES`.
- Is every lecture 30 fps? Otherwise the 30p preset and the sequence preset need per-fps variants.

[↑ back to contents](#table-of-contents)

---

#### filmora-basic-video-workflow

**Identity:**
- Version: `3.0.0-candidate.1` (SKILL.md:5). It was never promoted from "candidate".
- Source: claude.ai plugin `plugin_01DC5LCW7qVfP5xk76GYB8Dc`, from the "Astra Filmora engineering 2026-09-08" mission (qa/baseline.json).
- Size: 23 files, 304 KB. About 108 KB of that is historical reference docs.
- Last updated: 2026-09-09 (manifest).
- Entry points:
  - SKILL.md, a Computer-Use runbook.
  - Helpers: `scripts/job.py preflight|init|begin|commit|pass|status`, `scripts/media.py verify|transcribe`, `scripts/metadata.py`.
  - `agents/openai.yaml` for Codex/ChatGPT.

**Purpose & triggering:** The skill drives Wondershare Filmora 13 through Windows Computer Use (screenshots and semantic clicks). It assembles the latest 4 OBS recordings with an intro and outro, runs Filmora's Silence Detection per source, repairs gaps, adds two signature PNG overlays, exports MP4, verifies the file with ffprobe/ffmpeg, writes evidence-based metadata, and uploads UNLISTED through YouTube Studio in a named Chrome profile.

Description verdict:
- Accurate, and it front-loads "Wondershare Filmora".
- It **overlaps** with `premiere-basic-video-workflow`. Both claim "the standard YMnotes workflow" for OBS recordings. A request without an editor named ("edit today's lecture") can fire either one.
- The Premiere description already excludes Filmora, but not the other way round.

**How it actually works:**
1. `job.py preflight` (scripts/job.py:55) snapshots `D:/OBS Studio Captures` twice, checks the files are stable, sorts by the OBS filename timestamp (:15-37), and writes the manifest. `init`, `begin` and `commit` then form a self-attested intent/receipt ledger (:85-125).
2. The agent performs SKILL.md §2–§7 by sight:
   - Import in batches.
   - "Insert Media to End" per item (:76-83).
   - A Silence Detection dialog at 25 %, 0.5 s, 0.1 s, then Shift+Delete on the gaps (:89-98).
   - Overlays: "Add to new track", type the transform values, then **drag** the right edge to the end of V1 (:104-111).
   - Export dialog checks (:117-122).
3. `media.py verify` (scripts/media.py:18-47) checks stability, resolution, fps, duration against the *agent-observed* V1 duration, and decodes 3 frames and a 1 s audio sample.
4. CONTENT_EVIDENCE.md plus `media.transcribe` (faster-whisper 1.2.1) produce the content map. `metadata.py` calls `core.metadata_check` and `publication_check` (core.py:81-140).
5. The YouTube upload is done by hand in Chrome (references/YOUTUBE.md). The agent fills an "observed" JSON (:33-49) and `metadata.py --observed --final` compares it.

**Strengths to keep:**
- Strong safety rules:
  - Never modify the source files.
  - Stop at overwrite, login, payment or upgrade dialogs (SKILL.md:31-32).
  - UNLISTED only, with a hard stop when the channel or profile can't be proved (YOUTUBE.md:3-10).
  - The docs are honest that "Receipts record observations, not proof" (SKILL.md:155, RUNTIME.md:42).
- A good idempotency design for a UI tool:
  - Record intent before side effects.
  - A RECONCILE state on interruption.
  - "A started/uncertain upload cannot be automatically reset" (RUNTIME.md:44).
  - The upload intent is recorded *before* file selection (YOUTUBE.md:21).
- Semantic targets rather than coordinates. "Coordinates are temporary hints only" (VIDEO_EDITING_AUTOMATION_SOP.md:30). No unproven UI macros were promoted (qa/ENGINEERING.md:18).
- The helpers are stdlib-only, with strict JSON (duplicate keys and NaN are rejected) and writes that never overwrite.
- Tests: 25 unit tests pass (V-RUN). The real-ffmpeg `media.py verify` passed on a synthetic 1080p25 file and correctly blocked a duration mismatch (V-RUN). That closes the gap qa/validation.json lists as "ffprobe integration not run".
- Clear progressive disclosure. History is excluded from normal runs (SKILL.md:183-192).

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| F1 | **Superseded by the Premiere path.** `premiere-basic-video-workflow` is unattended and API-based, with an upload API and 874 cuts verified in production. Its own SKILL.md says "Never reuse Filmora X/Y values" and its description excludes Filmora. The Shorts pipeline only accepts Premiere artifacts. Filmora has not changed since 2026-09-09 and is still a "candidate". | SKILL.md:5; manifest updatedAt; premiere-basic-video-workflow/SKILL.md:3, :292; ymnotes-shorts.mjs:120-125 | V-SRC | High (redundancy) |
| F2 | **Description overlap and always-on context cost** for a skill that should now be a fallback. Both skills describe the same OBS→YMnotes job. | SKILL.md:3; premiere-basic SKILL.md:3 | V-SRC | Med |
| F3 | **No version pinning or guard.** It is validated only on Filmora 13.0.60.5095, but nothing reads the installed version. Preflight doesn't check it, and on any other version the instruction is to "verify changed labels". Filmora auto-updates, and versions 14 and 15 move the panels. | SKILL.md:12; ACTION_SEQUENCE.json:9-10; scripts/job.py:55-84; OPTIMIZATION_REPORT.md:142 | V-SRC | Med |
| F4 | **The UI automation is fragile by nature.** A 4-source lecture takes roughly 60+ vision-and-click steps. These include a pixel drag of each overlay's right edge to V1's exclusive end ("neither one frame short nor extending"), typing transform values, selecting a gap until a "white outlined block with an X" appears, and checking dialog values. The Duration-dialog alternative is "not yet pilot-validated". Recovery is one undo and one retry, then stop, and before S8 the ledger cannot rebuild a lost timeline. | SKILL.md:95, :104-111, :155, :169-170 | V-SRC/INF | Med |
| F5 | **The file gate is circular.** `verify` compares the export with the "observed final V1 duration" that the same agent read from the Filmora UI. Nothing independently confirms that silence was removed (no expected-duration bound against the source totals), that the overlays are present, or that there are no black or silent stretches. Branding is checked "visually" only. | SKILL.md:123; RUNTIME.md:70-72; scripts/media.py:18-47 | V-SRC + V-RUN | Med |
| F6 | **The stage gates are self-attested.** `job.py pass` accepts any receipt with `"verified": true` written by the agent. The docs admit this is "bookkeeping, not a proof engine". | RUNTIME.md:31-42; scripts/job.py:102-125 | V-SRC | Med |
| F7 | **The YouTube upload goes through the browser UI** even though a tested API uploader exists in the Premiere path (resumable upload, readback, duplicate guard). The browser route has "no idempotency key" and depends on proving the Chrome profile. | YOUTUBE.md:9-10, :21; premiere-basic scripts/youtube-upload.mjs | V-SRC | Med |
| F8 | **Install provenance.** The user's stored "Filmora and other programs" link points to an unofficial redistribution site. That is a malware and licensing risk, and an unlicensed Filmora watermarks exports. This extends prior-audit R9 to Filmora. | premiere-basic-video-workflow/SKILL.md:464 | INF | Med |
| F9 | **A stray user note ships in the package root** (`edits to skill.txt`, with the Studio upload URL). It is listed in the QA baseline as a package file. | `edits to skill.txt`:1; qa/baseline.json | V-SRC | Low |
| F10 | **Sediment.** About 108 KB of historical documents (forensic 42 KB, master spec 23 KB, blueprint 24 KB, optimization 10 KB) can contradict the runtime. SKILL.md:192 has to rank them. SKILL.md itself grew from 11.3 KB to 16.6 KB. | references/*; qa/validation.json; qa/ENGINEERING.md:95 | V-SRC | Low |
| F11 | **Hardcoded Windows paths.** The OBS folder and the brand folder are written into SKILL.md and the example config. | SKILL.md:40-41; config/machine.example.json:2-4 | V-SRC | Low |
| F12 | **The helpers break under `python -I`.** `media.py` and `job.py` import the sibling `core`, which fails with ModuleNotFoundError under isolated mode. Isolated mode is the convention the Shorts runner uses and the safe way to run code near untrusted media. | scripts/media.py:10 | V-RUN | Low |
| F13 | **`qa/package.py` can't be run without the original ZIP.** The "standard validator" was unavailable, and real speech and ffprobe integration are marked "not run". | qa/package.py:50; qa/validation.json | V-RUN | Low |

**Recommendations:**

1. **Retire it in stages: first make it user-invoked, then archive** (fixes F1, F2, F10). Effort: S.
   - Now: add `disable-model-invocation: true` to the frontmatter and change the description to the human-facing line *"Fallback: legacy Filmora 13 UI workflow for YMnotes lectures (use only if Premiere is unavailable)."* This removes the always-on context cost and the triggering overlap.
   - After roughly 5 more successful Premiere and Shorts lectures (or by 2026-12-31): archive the skill outside the synced set and keep a zip.
   - Delete the historical documents from the live package either way.

2. **If it is kept as a fallback, add a version guard** (fixes F3). Effort: S.
   - In `job.py preflight`, read the Filmora version from the installed exe (Windows: PowerShell `(Get-Item "<Filmora.exe>").VersionInfo.ProductVersion`) or require `filmora_version` in config.
   - `require(version == "13.0.60.5095" or config.get("allow_unvalidated_version"), "Filmora version drift: run a disposable pilot first")`.
   - Tell the user to switch off Filmora auto-update.

3. **Reuse the Premiere uploader** (fixes F7). Effort: M. Replace YOUTUBE.md with *"Upload with the production `scripts/youtube-upload.mjs --video <mp4> --package <metadata.json> --visibility UNLISTED`, then `--verify-video`."* This removes the Chrome-profile proof and the browser duplicate risk.

4. **Make the file gate independent** (fixes F5). Effort: S.
   - Add `--sources-total` to `media.py verify`, with an `expected_max = sources_total + intro + outro` bound. Fail if the duration is ≥ 98 % of that, which means silence removal didn't happen.
   - Add `blackdetect` and `silencedetect` as in the Shorts `qcShort`.
   - Extract frames at 2 s, intro mid, middle and end-2 s into JOB for the visual receipt.

5. **Housekeeping** (fixes F9, F11, F12). Effort: S.
   - Delete `edits to skill.txt`.
   - Add `sys.path.insert(0, str(Path(__file__).parent))` to each script so they run under `-I`.
   - Keep the D:\ paths only in `machine.example.json`.

6. **Install from the vendor only** (fixes F8). Effort: S. Replace the stored link with the official Wondershare download and licence, or remove it when the skill is retired.

**Quick wins (<30 min):**
- Add `disable-model-invocation: true` and the fallback description.
- Delete `edits to skill.txt`.
- Add the `sys.path` fix to `media.py`, `job.py` and `metadata.py`.
- Add one SKILL.md line under Purpose: *"Before any action, read Help > About; if not 13.0.60.5095, stop and report version drift."*

**Open questions:**
- Is Filmora still installed and licensed, and has it been used since the Premiere runner went into production? If not, archive now.
- Does any machine lack Premiere, so that a Filmora fallback is really needed?
- Should Filmora-produced lectures ever get Shorts? Today they can't: the Shorts skill needs Premiere artifacts.

[↑ back to contents](#table-of-contents)

---


### B. Books & question banks

#### ymnotes-medical-book-redesign
**Identity:** v1.9.0 (SKILL_MANIFEST.json:3; manifest `state` reads "CANDIDATE_RUNTIME_UPDATE_NOT_INSTALLED", line 121) · in-house YMnotes, based on 1.8.1, no outside upstream · 197 files / 8.3 MB (3.0 MB of it is assets/brand/ymnotes-closing-page.pdf; 89 scripts, about 31.6k lines including tests and references) · last updated 2026-10-30 (manifest `date`, VALIDATION.md:3) · entry points: `scripts/ymnotes_book.py` (doctor/inspect/init/extract/structure/editorial/master/build/prototype/sync-design/qa/release/autopilot/finish/status), `scripts/compose.py range`, `scripts/pipeline_state.py status|plan|run`.

**Purpose & triggering:** The skill turns a native-text medical PDF (optionally with a DOCX master) into a redesigned, print-first YMnotes book. It does this through a frozen source, a verified block stream, a Markdown master, Pandoc → Vivliostyle composition, about 30 QA gates and a hash-bound release with a reviewer ledger. It deliberately keeps clinical content source-faithful. The description leads with strong words ("Rebuild or redesign YMnotes medical books… print-first… PDF QA") and lists useful negative branches (ordinary PDF reading, medical advice, image generation). It triggers about right. It overlaps a little with `ymnotes-questions` (a book with end-of-chapter MCQs, or the phrase "rebuild … PDF") and with the generic `pdf` skill ("redesign this handout PDF"). Verdict: good. The description could add one disambiguating clause for question banks.

**How it actually works:**
1. `ymnotes_book.py doctor` (ymnotes_book.py:141) checks the Python modules, pandoc/node/npx and brand assets. If Vivliostyle is not installed it runs `npx --yes @vivliostyle/cli --version` (ymnotes_book.py:192), which can download the latest CLI.
2. `inspect` → `init` freeze ORIGINAL/original-book.pdf and plant DESIGN/ (styles) and templates. `design_system_state` is stamped from the manifest (ymnotes_book.py:351-356).
3. `extract`/`build`: `source_preflight` (ymnotes_book.py:459) calls `source_mode.inspect`, which calls a page "native" if `get_text()` is non-empty (source_mode.py:7). Then `extract_blocks.py` and `verify_extraction.py` run, cached through `pipeline_state.cached_stage` with the "verified-extraction" receipt (ymnotes_book.py:611-613). An existing blocks.json is re-proved, never re-extracted (595-607).
4. Master: `build_markdown.py` + `verify_markdown.py`, cached as "verified-master" (ymnotes_book.py:624-627). Then `compose.py book` → Pandoc → Vivliostyle, resolved by `ymnotes_paths.renderer_cmd` (local node_modules → global → `npx --yes @vivliostyle/cli`, ymnotes_paths.py:145-169). Then `append_final_page.py` and `set_page_labels.py` (ymnotes_book.py:637-643).
5. `qa` → `run_qa.py` runs about 30 gates, each judged by the tool's last verdict line (run_qa.py:100-125). Examples are layout_guard (151), verify_extraction/markdown, contents_contract (242), render_completeness (266), figure, furniture and cover gates, and fixture self-tests. It writes QA/reports/book-receipt.json with status QA-PASSED or CANDIDATE.
6. `release` → `release.py` refuses unless the design state is FROZEN (release.py:44). It reruns verify_pdf, final_page and furniture, then `release_guard.validate` (receipt hash, inputs fingerprint, transcript hash, and `review_evidence.validate_review`: packet hash, pixel hashes, non-empty `reviewer`/`reviewed_at`, all sampled pages reviewed; review_evidence.py:143-178). It checks the naming policy and delivery profiles, and writes additively with `open("xb")`.
7. `autopilot` (ymnotes_book.py:754) chains all of these. It calls build with `no_verify=True` (817) and sends medical claims to "agent phase" assessment (843-896).

**Strengths to keep:**
- Real, enforced fidelity architecture: an immutable blocks.json, a token and high-risk-token census (verify_extraction.py:9 compares numbers, doses, units and signs), separate `author_intent` and `medical_verification`, a CONTESTED state that must not overwrite (audit_corrections.py:98-113), and positive/negative correction fixtures that QA reruns every time.
- Release gating that is actually bound to evidence: QA receipt, PDF sha, input fingerprints, transcript sha, review-packet pixel hashes and additive writes (release_guard.py:23-40, release.py:117-125). It is hard to release a stale or unreviewed PDF by accident.
- Navigation contract checked per chapter on the final saved PDF (internal GoTo, folio = page label, unrelated links preserved), with 37 tests.
- Portability is clean: no hard-coded machine paths anywhere in runtime code. `reproduction_script.py` and `audit_publication_safety.py:75` actively detect drive letters and user dirs, and the project is resolved by `--project` / `$YMNOTES_PROJECT`.
- Test suite (V-RUN): **293 tests OK, 3 skipped** in 137 s on Linux / Python 3.13 / PyMuPDF 2.0 / pypdf 6.21. That is newer than the tested Windows / PyMuPDF 1.28 toolchain and still green. The skips are 2 env-gated real-book regressions and 1 PowerShell portability test.
- A good routing table in SKILL.md ("Read only what the current operation needs") and a clear WORKING → CANDIDATE → QA-PASSED → RELEASED vocabulary.
- One-writer lock and hash-keyed resumable DAG (pipeline_state.py:78-141). Scanned PDFs are refused with a clear message.

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | The scan detector is fooled by any text layer. A scanned page with an invisible OCR layer (render mode 3), or a full-page image with only a printed folio, is classed `native` / `native_extraction_safe: True`. The extraction census then compares the OCR layer with itself, so OCR errors in doses or numbers pass as "verified". SKILL.md:24-26 promises "the bundled native pipeline refuses scans". | source_mode.py:7-11; ymnotes_book.py:465-469; reproduced on synthetic `ocrscan.pdf` and `scan_with_folio.pdf` | V-RUN | High |
| 2 | Policy contradiction on clinical changes. SKILL.md and autonomy.md say clinical updating needs separate authorization, but autopilot/finish and editorial_autopilot tell the running agent to check "authoritative references" and set `CORRECTED` to overrule the author. `audit_corrections` accepts CORRECTED with only a `references` field: there is no authorization flag. | SKILL.md:41-45; references/autonomy.md "Clinical updating…"; ymnotes_book.py:855-866; editorial_autopilot.py:26-27,498-502; audit_corrections.py:106-108 | V-SRC | High |
| 3 | A gate that SKIPs counts as passing. When `want == PASS`, `verdict_of` returns True for SKIP. So a missing `BUILD/contents-entries.json` makes the contents contract SKIP and QA still reaches QA-PASSED. That contradicts "contents_contract.py verify is release-blocking". The same applies to cover, figure-groups, figure-completeness and structure-integrity SKIPs. | run_qa.py:119-121; contents_contract.py:800-807; tests/test_contents_contract.py:420-424; SKILL.md:58-60 | V-SRC | Med |
| 4 | The renderer is not pinned, although the docs say it is. Doctor and the build fall back to `npx --yes @vivliostyle/cli` with no version, so the latest CLI is fetched silently (npm latest is 11.4.0; VALIDATION records 11.2.0). Pagination can drift between builds and invalidate review packets. README and the operating guide say "pinned". | ymnotes_book.py:192; ymnotes_paths.py:166-167; README.md:30; operating-guide.md:12; `npm view` = 11.4.0 | V-SRC / V-RUN | Med |
| 5 | The reviewer attestation can be self-written. `validate_review` only checks that `reviewer` and `reviewed_at` are non-empty and that the page lists match. Any agent can write the ledger. autonomy.md allows labelled self-review, but no field records whether a review is "self" or "independent", and release does not show it. | review_evidence.py:149; release.py:154 (`evidence`) | V-SRC | Med |
| 6 | `computed_guard.cjs` (the print-CSS visibility/overflow preflight) is listed in SKILL.md as a check but is not wired into run_qa, release or doctor. Doctor does not check for puppeteer-core either. It runs only if someone remembers to run it. | SKILL.md:124; grep: no caller in scripts/*.py; run_qa.py:148-296 | V-SRC | Med |
| 7 | `--release-anyway` is dead or misleading. The help text promises to "publish even though QA reported unmet expectations", but release.py → `release_guard.validate` raises on a non-QA-PASSED receipt (an uncaught ValueError and traceback). The flag also clashes with "Do not bypass a failed gate". | ymnotes_book.py:826,1079-1082,914; release_guard.py:28-29; SKILL.md:70 | V-SRC | Low |
| 8 | Autopilot's docstring promises "Source in, release-ready book out", but release always refuses a fresh project: the design state is CANDIDATE from init, and there is no review ledger. Autopilot also builds with `no_verify=True`, so it writes no extraction or master checkpoint receipts. | ymnotes_book.py:755-757,817; release.py:44-47; VALIDATION.md:1 "(CANDIDATE)" | V-SRC | Low |
| 9 | Stale or inconsistent status metadata. README says "Revision 1.8.0" as the current text while the manifest says 1.9.0. The manifest says "NOT_INSTALLED" although the skill is installed and synced. The SKILL.md hash in the manifest no longer matches, because the sync rewrote the frontmatter with LF inside an otherwise CRLF file. The manifest lists a `.gitignore` that is not shipped. | README.md:6; SKILL_MANIFEST.json:121,154; `file SKILL.md` = mixed CRLF/LF (lines 1-4 LF) | V-RUN | Low |
| 10 | Orphan or sediment references. `troubleshooting.md` (11.9 KB) and `editions.md` are reached from nowhere. `qa-and-release.md` (27.5 KB, the largest reference) is not in the SKILL.md routing table and overlaps release-contract.md and verification.md. `design-system.md` is referenced only from code. | grep of `*.md` pointers; SKILL.md:75-95 | V-SRC | Low |
| 11 | Stale usage strings: 34 docstrings tell the reader to run `python tools/X.py`, but the scripts live in `scripts/` and expect project context. | run_qa.py:10-12; release.py:11-12; 20+ scripts | V-SRC | Low |
| 12 | SKILL.md costs about 3.2k tokens. The 40-line "Deterministic tools" catalogue (SKILL.md:105-145) and the 12-line contents-index paragraph (50-61) are reference that only some branches need. Under the user's rubric they belong behind a pointer. The body also leans on prohibitions ("Never…", "Do not…" about 15 times). | SKILL.md:36-70,105-145; writing-for-agents "Progressive disclosure", "Negation" | V-SRC | Low |
| 13 | The print-quality checks cover geometry, not press readiness. There is a font floor of 5.5 pt, overprint and bounds checks, Type3 detection, a figure ppi check only where `dpi_basis` is declared, and QR decoding. There is no check that every font is embedded, no image effective-ppi check for ungrouped figures, and no colour, bleed or PDF/X check. That fits office or print-shop A4 if the claim is kept modest. | layout_guard.py:135,176-177; audit_figure_groups.py:200-204 | V-SRC | Low |
| 14 | The test suite never runs the real renderer. Composition tests use `tests/fixtures/fake_renderer.py`, and the end-to-end real-book proofs are manual and on Windows (VALIDATION.md). Pagination or layout regressions from a Vivliostyle or Chromium update are not caught automatically. | tests/test_render_transaction.py; tests/fixtures/fake_renderer.py; test_external_regression.py:33-41 (env-gated) | V-RUN | Med |
| 15 | Privacy, minor: brand QR destination URLs carry a YouTube share-tracking `si=` parameter. This is not a secret, but it is a sharer identifier printed into every book's QR code. No credentials or tokens were found. Fonts are OFL with licences bundled. | assets/brand/brand.json:39; assets/brand/qr-destinations.json:10 | V-SRC | Low |
| 16 | `doctor` itself can touch the network (`npx --yes …`). This reviewer ran doctor once; it resolved from the npm cache. "No remote service is needed" (README.md:36) is true only when the renderer is preinstalled. | ymnotes_book.py:191-199 | V-RUN | Low |

**Recommendations:**
1. **Harden scan detection** → fixes #1 → in `source_mode.inspect`, count only *visible* text. Treat a page as a scan when an image covers more than 80% of it and visible text is below a threshold, and flag invisible text (span flags or `render_mode==3` via `page.get_texttrace()`) as an `ocr_layer`. Draft:
   ```python
   vis = [s for s in page.get_texttrace() if s.get("type") != 3 and s.get("opacity",1) > 0]  # type 3 = invisible
   chars = sum(len(s["chars"]) for s in vis)
   img_cover = sum(r.get_area() for r in (fitz.Rect(i["bbox"]) & page.rect for i in page.get_image_info())) / page.rect.get_area()
   if img_cover > .8 and chars < 200: scan.append(n)           # scan, possibly with folio
   if any(s.get("type")==3 for s in page.get_texttrace()): ocr.append(n)
   "native_extraction_safe": not scan and not ocr
   ```
   Add 2 tests using the synthetic PDFs from this review. Effort: S–M.
2. **Make clinical correction an explicit, authorized branch** → fixes #2 → `audit_corrections.py`: refuse `status == "CORRECTED"` unless `SOURCE/book.json` (or corrections.json) has `"clinical_update_authorized": {"by": "...", "when": "...", "scope": "..."}`. Change the agent_phase text (ymnotes_book.py:861-863) to: "set CONFIRMED or CONTESTED; CORRECTED is available only when the project records `clinical_update_authorized` (a separate task the author requested)." Mirror this in editorial_autopilot.py:498-502 and editorial-correction.md:113. Effort: S.
3. **Make SKIP fail for release-blocking gates** → fixes #3 → in run_qa, add a `REQUIRED` expectation, used for the contents contract and for the cover gate when front matter exists. Draft: `if "SKIP" in last: return want not in (FAIL, REQUIRED), last`. Have `init` and `sync-design` always declare `BUILD/contents-entries.json`. Effort: S.
4. **Pin the renderer** → fixes #4 and #16 → put `RENDERER_PACKAGE = "@vivliostyle/cli@11.2.0"` (or read `renderer_version` from SKILL_MANIFEST/`requires`) in ymnotes_paths.py:142. In doctor, use `npx --no-install` and report "not installed: npm i -D @vivliostyle/cli@11.2.0" instead of fetching. Record the resolved version in the QA receipt and refuse release if it changed. Effort: S.
5. **Record what kind of review happened** → fixes #5 → require `review_kind ∈ {self, author, independent}` in the review ledger (review_evidence.py:149), copy it into the release manifest, and print it in the release summary. Effort: S.
6. **Wire in computed_guard or demote it** → fixes #6 → either add a run_qa check, skipped with REVIEW when node, puppeteer-core or Chrome is absent, plus a doctor row for puppeteer-core, or move the computed_guard line out of the SKILL.md tool list into release-contract.md as an optional manual step. Effort: S–M.
7. **Remove `--release-anyway`** → fixes #7 and #8 → delete the flag and its hint text, and change the autopilot docstring to "Source in, QA'd CANDIDATE out; release needs a frozen design and a review ledger." Effort: S.
8. **Slim SKILL.md** → fixes #12 → move the tool catalogue (SKILL.md:105-145) to `references/tools.md`, leaving one line: "Measurement tools and what each proves: [tools](references/tools.md)." Shorten the contents paragraph to 3 lines plus its existing pointer. Rephrase prohibitions as targets where possible ("Publish source medicine verbatim; record ambiguity in the exception log"). That saves about 1.5k tokens on every activation. Effort: S.
9. **Clear out reference sediment** → fixes #10 and #11 → route `troubleshooting.md` from the table ("A gate or tool fails unexpectedly"). Merge or delete `qa-and-release.md` and `editions.md` against release-contract, verification and edition-reconciliation. Run `sed -i 's#python tools/#python scripts/#'` over the docstrings. Effort: M.
10. **Add one real-render smoke test** → fixes #14 → an opt-in test (`YMNOTES_RENDER_SMOKE=1`) that builds `tests/fixtures/synthetic_book.py` through the real pinned Vivliostyle and runs `run_qa.py book`, asserting QA-PASSED and a stable page count. Effort: M.
11. **Refresh metadata after each sync** → fixes #9 → regenerate the manifest hashes, normalise SKILL.md to one line-ending style, update README's "current revision" to 1.9.0, and change the manifest `state` to CANDIDATE_INSTALLED. Effort: S.
12. **Print-readiness additions (optional)** → fixes #13 → in layout_guard, fail on any font with an empty `ext` (not embedded) and warn on images under 200 effective ppi. State in SKILL.md: "print-first = office/print-shop A4; no PDF/X or bleed". Effort: S.
13. **Remove the `si=` share parameter** from both QR destination URLs and regenerate the QR SVGs → fixes #15. Effort: S.

**Quick wins (<30 min):**
- Remove the unused `--release-anyway` flag and its hint text (#7).
- Pin `@vivliostyle/cli@11.2.0` in ymnotes_paths.py:142 and in doctor (#4).
- Treat SKIP as failure for the contents contract in run_qa.py:119 (#3).
- Update README's revision line and the manifest state, and regenerate the SKILL.md hash (#9).
- Add `troubleshooting.md` to the SKILL.md routing table (#10).
- Change the `python tools/` usage strings to `python scripts/` (#11).
- Strip `?si=…` from the YouTube URL in brand.json and qr-destinations.json (#15).

**Open questions:**
- Is clinical correction (`CORRECTED`) ever meant to happen inside a redesign job, or always in a separate, user-authorized task? Recommendation 2 depends on the answer.
- Should a self-review by the agent ever be enough to release a student-facing book, or must the author (YMnotes) review personally?
- Do any of your source books arrive as scanned PDFs with OCR text layers (for example older handouts)? If so, #1 is urgent before the next build.
- Is the Telegram handle `ymnotesoffcial` (spelt without the second "i") the real channel name? It is printed in QR artwork (brand.json:47).
- Which print path do you use (home or office printer, a print shop, or PDF-only distribution)? The answer decides whether the PDF/X, bleed and embedding checks in #13 matter.
- The manifest describes an "editable copy" with `_development` evidence that the portable package excludes. Is the synced copy the canonical one, or is a Windows master copy the source of truth? That affects where fixes should be made.

[↑ back to contents](#table-of-contents)

---

#### ymnotes-questions
**Identity:** v0.4.0 (SKILL_MANIFEST.json:3, runtime.py:11) · synced claude.ai plugin skill, no upstream (marketplace manifest.json:289-292, `updatedAt` 2026-09-09) · 66 files / 2.7 MB (about 2.1 MB is 8 OFL fonts) · entry points: `scripts/ymnotes_questions.py` (CLI: doctor/inspect/init/extract/status/build/prepare-review/qa, plus organize/release/autopilot stubs that exit 3), `scripts/package_skill.py` (validate/zip), `agents/openai.yaml` (Codex/ChatGPT interface stub)

**Purpose & triggering:** It freezes a contiguous page range of one native-text PDF, copies MCQs line by line (stem, then A–H choices) into a hash-bound MASTER JSON, and renders an A4 YMnotes-branded question-bank PDF. It then prepares PNGs for an attested visual review, and a 10-gate QA run reports the result. It never generates answers and never publishes. Verdict on the description: it is accurate but jargon-heavy ("candidates", "hash-bound review preparation"). It leaves out the words the user actually types ("question bank", "MCQs from pages X–Y", "Mid questions", Arabic "بنك أسئلة"). It does not say that answers are not included, which a question-bank user would expect to know. A third of it is a negative list of unavailable features. There is mild overlap with `ymnotes-medical-book-redesign` ("source-faithful print-first publications, structured extraction, PDF QA") and with the generic `pdf` skill. The "MCQ/question bank" leading word separates them well enough once it comes first in the description.

**How it actually works:**
1. `doctor` (ymnotes_questions.py:87-109) checks that the 5 modules can be imported and that pdftoppm/pdftotext/tesseract are on PATH. Those 3 tools are listed but no code uses them. Version caps are not checked.
2. `init --pages a-b` (ymnotes_questions.py:112-162): checks signatures (55-75), stages a new workspace in a temp dir, then renames it into place (119-125). `freeze_pdf_range` writes the page subset and selection.json (pdf_native.py:31-53). Templates, tokens, brand assets and fonts are copied in (156-160). `validate_project` refuses any folder under a SKILL.md (runtime.py:66-71).
3. `extract` runs under a writer lock (runtime.py:147-162; pdf_native.py:125-288):
   - Each page: `page_visuals` stops the run on any image, table, curve, line or rect except a full-page white background (85-96, 177-178).
   - Text lines come from `extract_text_lines(x_tol=2,y_tol=3, return_chars=False)` (70-77). Font and colour information is discarded.
   - Segmentation: a line with more than one `\d+|[A-H]` marker stops the run (202-204). `CHOICE_RE` matches uppercase consecutive labels (205-219). A line indented more than 12 pt and close below a choice joins that choice (227-236). Any other unnumbered line opens or extends a stem (246-259).
   - `fidelity_errors` requires every native line to be used once and in order, and each stem/choice to be rebuilt exactly from its spans (contracts.py:26-70).
4. `build` (render_questions.py:52-396):
   - `native_preflight` re-extracts the PDF and compares text, geometry, annotations and visuals (contracts.py:73-116). Unsupported glyphs are rejected (247-253).
   - Stems with soft wraps are joined with spaces (21-40). "not/except" is bolded in negative stems (43-49).
   - The DP page planner (page_composition.py:21-69) packs whole questions. The PDF and its sidecar are created exclusively, then latest-build.json is written (385-391).
5. `prepare-review` (pilot_qa.py:66-96) rasterises the pages with pdfplumber and writes an unreviewed checklist. `qa` = structural `qa()` (contracts.py:225-270) plus `audit_project` with 10 gates (pilot_qa.py:126-255). Visual review is accepted when status, reviewer, notes, checks and PNG hashes are filled in (34-63).

**Strengths to keep:**
- A real fidelity design: every native line must be consumed exactly once, in order, and re-verified against the frozen PDF before every build (contracts.py:68, 94). Tampering tests cover number, label, span and text.
- It refuses to answer, correct, shrink or reorder. When in doubt it stops instead of guessing. Writes are atomic, the writer lock is exclusive, init is staged then renamed, and candidates/sidecars are never overwritten (runtime.py:88-114).
- Provenance is honest: build input, runtime and schema hashes make old reviews stale automatically (runtime.py:131-144). `prepare-review` always starts at `not_run`, and every result says `production_release_eligible: false`.
- Imports are lazy, so `doctor` works without dependencies. There are no absolute machine paths in code, paths are portable and checked for symlinks/junctions, and there are no network or model calls.
- Licensing is clean: OFL notices sit beside each font, and brand-asset hashes are recorded and tested (borrowed-assets.json).
- SKILL.md is small (38 lines, 4.5 KB), with a task→reference routing table. The test suite is fast (35 tests, about 7 s).

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | **Answer text gets published into the student PDF.** A line indented more than 12 pt right under the last choice (for example "Answer: B" or an explanation) is joined silently into that choice and rendered. Every QA gate except visual review still passed. | pdf_native.py:227-236; probe: `[["B","Second\nAnswer: B"]]`, built PDF shows "B Second Answer: B" | V-RUN | High |
| 2 | **Headings are silently merged into the next question.** With unnumbered questions, any line before the first stem (chapter title, "Choose the best answer") becomes part of the stem and is published. This breaks SKILL.md:25 "never silently merge questions". | pdf_native.py:246-259; probe: stem `"Chapter 5 Review Questions\nWhich is correct?"` → PDF Q01 | V-RUN | High |
| 3 | **Answer keys are lost without warning.** Answers marked by bold or colour are dropped silently because `return_chars=False` discards font data. Answers in /FreeText or /Ink annotations are set aside as "excluded". No answer layer exists, so a bank cannot carry a key, and the user is never told one existed. | pdf_native.py:72, 107-121; data-contracts.md:12; probe `bold_answer` built with no warning | V-RUN | High |
| 4 | **The marker check rejects ordinary medical text.** "E. coli", "7.4", "3-4 weeks" and "vitamin B-12" all count as a second marker, so extraction stops. Most real medical MCQ PDFs will fail at extract. | pdf_native.py:202-204; probes `E_coli_in_stem`, `decimal_value`, `range_hyphen` → STOP | V-RUN | High |
| 5 | Real-world layouts are almost all blocked, with no way to declare exclusions. Running headers, footers and page numbers break the rule that every line belongs to a question. Any ruling line or underline counts as a vector and blocks. Lowercase `a)` choices stop the run. No mechanism exists to declare a header/footer band as excluded, although the schema has an `excluded` detection disposition. | pdf_native.py:94-96, 177, 9; contracts.py:68-69; contracts.py:216-217; probe `lowercase_choices` → STOP | V-RUN / INF (footer) | Med |
| 6 | Soft-wrap reflow corrupts hyphenated words. "hyper-\ntension" is rendered as "hyper- tension". The `rendered_content` gate collapses whitespace, so it cannot catch this. | render_questions.py:38-40; pilot_qa.py:184; probe `hyphen_wrap` | V-RUN | Med |
| 7 | One test fails in the installed copy. `package_skill.files()` requires `.gitignore`, and the synced skill has none (sync drops dotfiles), so `test_packaging_and_extraction_structure` and `package_skill.py --check` fail. Result: 34/35 pass with the locked dependencies, and the same with the latest reportlab 5.1.0 and svglib 2.3.2. | package_skill.py:14-15, 24-25; test_pipeline.py:295-300 | V-RUN | Med |
| 8 | The visual-review gate does not tie the PNGs to the candidate. Any valid PNGs whose hashes match their own files, with the right page count, pass. It never checks them against the `QA/review-<hash>/visual-review.json` that prepare-review wrote. "Binds both candidate and PNG hashes" overstates this. | pilot_qa.py:41-56; SKILL.md:30; qa-and-publication.md:14 | V-SRC | Med |
| 9 | No install route for the agent. SKILL.md and agent-operation.md say "requirements installed", but only README.md:5-12 gives install commands, and only in PowerShell. The Claude app and cloud have no bootstrap. `doctor` reports reportlab 5.0.1 as PRESENT even though requirements say `<5`. | agent-operation.md:5; README.md:5-14; ymnotes_questions.py:96-99 | V-RUN | Med |
| 10 | Dead publication-safety pattern. `\\.py\\b` inside a raw string matches a backslash followed by "py" and a backslash, so it never matches ".py". `TODO` with `re.I` is a substring match and false-matches words such as "mastodon". | pilot_qa.py:188 (verified with re test) | V-RUN | Low |
| 11 | Dead code and duplication: `source_canonical` and `output_flat` are computed but never compared, which looks like a check that does not run. Also: unused `examples_root` (`--development-workspace` refers to an `examples/` folder that is not shipped), unused `fx, fy`, three copies of `digest`, duplicated CHOICE/NUMBER regexes, and logo/QR geometry computed twice. | pilot_qa.py:160-161, 171, 15-20, 11-12; ymnotes_questions.py:131, 205-206; render_questions.py:163-167 vs 195-202, 231; pdf_native.py:13-18 | V-SRC | Low |
| 12 | Reference sediment. 5 stub "routing" files have no inbound links: design.md, layout-refinements.md, question-design-system.md, foundation-audit.md, reliability-pass.md. The same "Full-page, unstroked white rectangles…" paragraph appears verbatim in 3 places. verification.md and README describe the developer's own environment ("organized Astra workspace", 3,034-file rehash, Gitleaks), which the runtime agent does not need. | references/*.md; SKILL.md:38 = agent-operation.md:64 = qa-and-publication.md:24; README.md:18-23; verification.md:14-16 | V-SRC | Low |
| 13 | The description misses user trigger words and the "no answers" fact. Its last sentence is a negative list, against the rubric's "front-load leading word / prompt the positive". | SKILL.md:3 | V-SRC | Med |
| 14 | Contextual bolding of "not/except" applies to every match in the whole stem, not just the instruction. In a long case such as "…did not respond… Which is NOT…" both are bolded. | render_questions.py:47-48 | V-SRC | Low |
| 15 | Personal or tracking data: the YouTube destination URL carries an `si=` share-tracking parameter. The Telegram handle spelling should be confirmed. No secrets or tokens were found. | templates/brand.json:28, :35 | V-SRC | Low |
| 16 | Unused config. Bank title, numbering and watermark settings in project.json are ignored. The PDF title and footer are hardcoded ("YMnotes Question Bank", "Medical questions"), so per-module banks cannot be titled. This is honestly documented. | render_questions.py:211, 229, 331; agent-operation.md:60 | V-SRC | Low |
| 17 | Version caps are stale. `reportlab<5` and `svglib<2`, but reportlab 5.1.0 and svglib 2.3.2 are current and the suite passes on them (apart from #7). | requirements.txt; PyPI check 2026-11-01 | V-RUN | Low |

**Recommendations:**
1. **Stop on text after the last choice instead of merging it** (#1). In pdf_native.py:227-236, allow a continuation line only if it lines up with the hanging indent of the choice text. Stop on answer or explanation prefixes. Draft:
   ```python
   ANSWER_RE = re.compile(r"^\s*(answer|ans\.?|key|correct|explanation|rationale)\b", re.I)
   if ANSWER_RE.match(line["text"]):
       raise ValueError(f"Answer/explanation line on source page {source_page}; answer layer unsupported - review source")
   text_x = anchor + label_width_estimate          # x of choice text after "B."
   hanging = abs(line["x0"] - text_x) <= 3
   if same_page and close_line and hanging and not numbered_next: ...join...
   ```
   Add a regression test that copies the `indented_answer_line` probe. Effort S.
2. **Require an explicit start for each question** (#2). At pdf_native.py:246, when `current is None and not numbered`, raise "Unnumbered text before a question: heading, instruction or unnumbered bank requires review". Add an opt-in `--unnumbered` init flag recorded in selection.json for genuinely unnumbered banks, and still stop on a stem of more than one line before choice A. Effort S.
3. **Make the marker check reject only real inline markers** (#4). Replace the regex at pdf_native.py:202 with a check based on character gaps. Set `return_chars=True` and count a marker only at line start, or after a horizontal gap of at least 3× the space width, followed by a space and then an uppercase letter or digit. Whitelist `[A-H]\. [a-z]` (genus abbreviations) and `\d[.-]\d` (decimals, ranges). Add tests for "E. coli", "7.4", "3-4 weeks" and "B-12". Effort M.
4. **Add an answer-key path that only uses the source** (#3). Phase 1 (S): with `return_chars=True`, if the chars of one choice differ in fontname weight or `non_stroking_color` from its siblings, stop with "Source emphasises choice X (possible answer key)". Do the same if FreeText/Ink annotations exist, so nothing is lost silently. Phase 2 (M): add an optional `answers` layer to question-bank.schema.json: `{question_id, label, evidence: "bold"|"annotation"|"answer_line", spans}`. Fill it only from explicit source evidence, never by inference. Render a separate answer-key page, and add a QA gate that every recorded answer label exists among the question's choices. Effort S→M.
5. **Declared exclusion bands for headers, footers and decorative rules** (#5). Add an init option `--exclude-band top=36,bottom=40` (pt), stored in selection.json. Lines inside a band become `detections` with disposition `excluded` and reason "declared running header/footer". `fidelity_errors` then counts used + excluded = all blocks. Treat horizontal `page.lines` entirely inside a band, or not touching any text bbox, as decorative and record them as excluded. Effort M.
6. **Stop reflowing hyphenated wraps** (#6). In `_soft_wrap_stem`, return `raw, False` if any line except the last ends with "-". Make the `rendered_content` comparison check the reflowed display text against expected display text, not whitespace-collapsed raw text. Effort S.
7. **Fix packaging and the failing test** (#7). In package_skill.py:14 move `.gitignore` to an optional set (`OPTIONAL_ROOT_FILES = {".gitignore"}`, skipped if missing). Effort S.
8. **Tie review PNGs to prepare-review** (#8). In `visual_evidence_valid`, load `QA/review-<candidate_sha[:16]>/visual-review.json` and require `visual["rendered_pages"] == prepared["rendered_pages"]`, with every path under that directory and `visual["dpi"] == prepared["dpi"]`. Effort S.
9. **Install bootstrap in agent-operation.md** (#9, #17). Add one platform-neutral block:
   `python -m venv .venv && <venv-python> -m pip install -r requirements-lock.txt` (Windows `.venv\Scripts\python.exe`, POSIX `.venv/bin/python`). Add a sentence telling the agent to pass the absolute script path. Make `doctor` compare installed versions with requirements.txt using `packaging.specifiers`, or a simple major-version check. Raise the caps to `reportlab>=4.4,<6` and `svglib>=1.6,<3` after re-running the suite. Effort S.
10. **Rewrite the description** (#13). Draft:
    `description: Build YMnotes MCQ question-bank PDFs from a page range of a native-text PDF, copying every stem and choice word-for-word (no answers added or corrected), or review/redesign those question pages. Use for "make a question bank from pages X–Y", "extract the MCQs from this PDF", re-laying out an existing bank, or visual QA of a built bank. Scanned pages, images, DOCX, figures and tables stop the run.`
    Effort S.
11. **Prune sediment** (#11, #12). Delete the 5 orphan reference stubs. Keep the white-background paragraph only in agent-operation.md. Move the developer-environment sections of verification.md and README.md:18-23 to the dev `history/` folder. Remove the dead variables, import `digest` and the regexes from one module, and fix pilot_qa.py:188 to `r"\.py\b"` and `\bTODO\b` (#10). Effort S.
12. **Scope "not/except" emphasis to the interrogative clause** (#14). Bold only the first match after the last sentence boundary in the stem. Effort S.
13. **Strip the tracking parameter** (#15). Use `https://youtube.com/@ymnotes` in brand.json. The QR SVG must be regenerated only if it encodes the `si=` URL. Effort S.
14. **Unavailable features: what each would take** (from the description):
    - **Production release (S–M):** implement `release`. Require a passing qa-report and a fresh visual review, plus an explicit `--confirm` flag. Copy the candidate into `RELEASE/` with a release manifest. Hand off to `ymnotes-qr` for Drive/QR, as an instruction rather than a runtime dependency.
    - **OCR / image pages (L):** add an `ocr` adapter (ocrmypdf/tesseract or Claude vision) that writes normalized blocks with `method: "ocr"` and a confidence value; the schema already supports both. Because native re-verification is impossible, freeze the OCR output as the truth artifact. Require agreement from two engines or a per-line human or vision check, and keep the `partial`/issues path for low-confidence spans.
    - **DOCX (M–L):** python-docx paragraph walk. The key gotcha is that Word auto-numbering ("1.", "A.") is not in the text. It must be resolved from `numbering.xml` (`w:numPr`) to recover numbers and labels. Pagination stays null, as data-contracts.md already specifies.
    - **Figures (L):** take bboxes from `page.images`, render crops at 300 dpi via pypdfium2 (already in the lock), and store hashes. Propose owners by proximity and "Figure N" references. Record the reviewer's decision in a JSON file (the schema already has `ownership.candidates/decision_evidence`). Render the figure inside the question block with its aspect ratio preserved. This must come after #5 so that decorative graphics no longer block everything.

**Quick wins (<30 min):**
- Make `.gitignore` optional in package_skill.py:14 → the suite goes 35/35 (#7).
- Fix `\\.py\\b` → `\.py\b`, and `TODO` → `\bTODO\b` (pilot_qa.py:188).
- Stop reflowing stems with a line ending in "-" (render_questions.py:38).
- Stop on `Answer|Ans|Key|Explanation` lines (pdf_native.py, before line 221).
- Delete the 5 orphan reference stubs and the 2 duplicate white-background paragraphs.
- Remove the dead variables (`source_canonical`, `output_flat`, `examples_root`, `fx, fy`).
- Replace the description with draft 10 above.
- Strip `?si=…` from templates/brand.json:28.

**Open questions:**
- Do the user's real source PDFs carry answers (bold, coloured, "Answer:" lines, end-of-chapter keys)? Should the bank PDF contain a key (#3/rec 4)?
- Are typical sources numbered, with uppercase A–E choices and no running headers? If not, the skill may never have succeeded on a real PDF (#4/#5). Has it been run on a real one since v0.4.0?
- Is `t.me/ymnotesoffcial` (brand.json:35) the correct handle, or a typo for "official"?
- Should titled banks (module name, "Mid Questions") be supported? That needs project.json `title` to drive the PDF title and header (#16).
- Is `agents/openai.yaml` still used, given the related "Support Claude Code and ChatGPT Work" pattern in other skills?
- Who is the intended "reviewer" for the visual gate: the agent inspecting PNGs, or the user? That decides whether rec 8 is enough, or whether a user confirmation step is also wanted.

[↑ back to contents](#table-of-contents)

---


### C. Teaching content & distribution

#### ymnotes-batch-messages
**Identity:** no version · local/custom (no upstream) · 13 files / ~344 KB (raw PDF text 140 KB, `videos.json` 100 KB) · data stamped `_checked: 2026-10-19` (`references/videos.json:3`, `references/semester.json:155`) · entry points: `SKILL.md`, `scripts/where_are_we.py`

**Purpose & triggering:** Produces the weekly Egyptian-Arabic WhatsApp/Telegram message for one O6U batch (levels 1-4). It links individual YMnotes videos chosen for the current teaching week and the next exam. The description is strong. It front-loads the deliverable, covers Arabic triggers (دفعة, رسالة الأسبوع, سنة أولى…) and the "which videos fit a batch now" branch. Its weak point is that it hardcodes "first-semester 2026-2027", so it will under-trigger or mislead after January 2027. There is mild overlap with `ymnotes-youtube-video-finder` on "which video fits X". This skill uses only the owner's own catalogue, while the finder searches all of YouTube. Neither description names the other to disambiguate. No overlap with `medical-visual-board` or `etymology`.

**How it actually works:**
1. `SKILL.md:25-26`: map the batch to a level, then run `where_are_we.py --level N --date`.
2. `where_are_we.py:19-20`: load both JSON files at import. `week_of()` (`:31-42`) computes the week from `week1_start` (2026-09-19) and the 13 teaching weeks, then the `after_teaching` windows.
3. `report()` (`:60-120`): list exams with countdowns. Pull the week topics from `levelN-weeks.md` with a regex on `Wk N` (`:45-49`).
4. Exam suggestions (`:91-109`) cover exams ≤14 days away (or the next one). Phase is "mid" when the exam text contains "mid", otherwise "final". Practical means OSPE/OSCE. Then come videos whose `weeks` contain this week or next week (`:110-115`).
5. `search()` (`:123-130`): substring search in the catalogue. It skips excluded playlists only.
6. The agent picks 4-8 videos and writes the message to the house style (`SKILL.md:55-64`). The mandatory `Alert:` line is at `SKILL.md:52,63`.

**Strengths to keep:**
- A deterministic script does date math and exam countdowns, so the model does none of it.
- Hard guardrails are explicit and motivated: no playlists, no invented IDs, excluded series, "never send yourself", and the mandatory automated-message line with its reason given (`SKILL.md:46-53`).
- The data was validated (V-RUN). Every curated ID in `levels` exists in the `catalogue`. No curated video is in an excluded playlist or on the excluded list. No duplicates. All `type`/`for` values are valid.
- The "Keeping the data fresh" section gives a clear maintenance recipe (`SKILL.md:66-70`).
- The house style captures the owner's standing preferences (دكاترة, du'a naming Allah).

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | The only worked example breaks three hard rules: the greeting is "يا دفعة سنة تانية" (rule: always دكاترة), the closing "ربنا يوفقكم…" does not name Allah, and the mandatory `Alert: This is an automated message ❤️` line is missing. Examples steer more strongly than rules, and the owner posts without review. | `references/example-year2-nrs.md:6,36-37` vs `SKILL.md:52,58,63` | V-SRC | High |
| 2 | The semester data expires. After 2027-01-21 the script prints "after the teaching weeks" with no exams and no suggestions, and gives no warning that the data is stale. The description still says 2026-2027. The second semester (~Feb 2027) cannot be served. | `semester.json` `after_teaching` ends 2027-01-21; run with `--date 2027-02-20` gave an empty suggestion block; `SKILL.md:3,10` | V-RUN | High |
| 3 | During the final-exam weeks the script suggests nothing. MSS/ERS/PED end-modules are undated, so no exam matches and no teaching week matches. The SKILL tells the agent to pick `for: final` by hand, which is exactly the busiest period. | run `--level 2 --date 2026-12-20` showed an empty VIDEO SUGGESTIONS block; `SKILL.md:40` | V-RUN | Med |
| 4 | The week digests have gaps. `level1-weeks.md` has no Wk 8 (7-12/11), although the raw PDF has it (`raw/level1-schedule.txt:1933`). `level3-weeks.md` has no Wk 7. "Next week" topics silently disappear for those weeks. | `level1-weeks.md:71-74`; `grep Wk` on level3 | V-RUN | Med |
| 5 | Coverage gaps reach the output. Level 1 IBF and IMB have zero mapped videos, and level 4 HVD and SM 408 have zero (from week 10). Today's level-1 run returns one video against a 4-8 target. | validation script; run `--level 1 --date 2026-11-01` | V-RUN | Med |
| 6 | Phase misclassification. Any exam without "mid" is labelled "final", so "IBS OSPE (Gp 1-10)" prints "IBS final + practical". It is cosmetic for written matching, but it misleads the agent's reading. | `where_are_we.py:96`; run output | V-RUN | Low |
| 7 | `search()` ignores `excluded_videos`. Today that does no harm because the Solo Team ad is not in the catalogue, but it is a latent guardrail hole. | `where_are_we.py:123-130` | V-SRC | Low |
| 8 | Four curated entries use `module: "Skill lab"`, which is not a module in `semester.json`. They can never match an exam and they show in week lists without a module context. | `videos.json` level 2 `1OOsmbwPeyw`; level 3 `TES_cHGKyZ8`, `ll-pJYA_kwQ`, `ypn94qz6KKg` | V-RUN | Low |
| 9 | Ended modules still surface. CAD practical videos appear in level-4 week 7, although CAD ran weeks 1-5. `weeks` matching ignores `module_weeks`. This may be intentional (skill lab timing), but it is undocumented. | run `--level 4 --date 2026-11-01`; `semester.json` CAD [1,5] | V-RUN | Low |
| 10 | Context cost of the "code can't run" fallback (`SKILL.md:34`). Hand-reading `videos.json` (100 KB) plus the raw schedules (140 KB) is about 60-70k tokens. The raw text is a fallback that is rarely needed, but it ships in the skill. | file sizes | INF | Med |
| 11 | `dt.date.today()` uses the container time zone (UTC in cloud). Cairo is UTC+2, so between 22:00 and 24:00 Cairo time the week or countdown can be off by a day. | `where_are_we.py:144` | INF | Low |
| 12 | There are no tests or data validator. Integrity (IDs in catalogue, not excluded, modules valid, weeks 1-14) is checked only by the model "before handing over" (`SKILL.md:52`). | none present | V-SRC | Med |
| 13 | Tool dependencies. Running the script needs a shell: Claude Code, or the claude.ai code sandbox (paths relative to the skill dir). Refreshing data needs logged-out YouTube fetches and Claude in Chrome (`SKILL.md:68`), which are not available in plain claude.ai. | `SKILL.md:26,68` | INF | Low |
| 14 | Privacy is fine. Group numbers (Gp 1-20) are cohort scheduling, not student data. No names, phones or secrets were found (grep). | grep scan | V-SRC | n/a |

**Recommendations:**
1. **Fix the example** → #1. Rewrite `references/example-year2-nrs.md` lines 6 and 36-37 to: `السلام عليكم يا دكاترة 👋` … `ربنا يوفقكم ويجعله ميد سهل عليكم بإذن الله ✅` / `— YMnotes` / *(blank)* / `Alert: This is an automated message ❤️`. Keep the "wrong batch" apology line as the demo of the "owns up" rule. Add one line to "Why it works": "ends with the Alert line." → S
2. **Add a staleness gate** → #2. In `report()`:
   ```python
   last = d(SEM["semester"]["after_teaching"][-1]["to"])
   if today > last:
       sys.exit("STALE DATA: semester.json covers up to %s. Ask the user for the new semester PDFs; do not write a message." % last)
   ```
   In `SKILL.md`, change the description to "…using the bundled O6U semester schedules (currently first semester 2026-2027; the script refuses dates outside it)". → S
3. **Add a finals mode** → #3. When `label` starts with "Final exams", print each running module's `for: final` and `summary` videos, plus the undated end-modules from `L["notes"]`. Pseudocode: `if n > teaching_weeks: for m in L["modules"]: rows = [e for e in entries if e["module"]==m and (e["for"]=="final" or e["type"] in ("summary","past-exam"))]`. → M
4. **Add `scripts/validate_data.py`** → #4, #5, #8, #12. Check: every `levels` ID is in the `catalogue` and not excluded; `module` is in that level's modules or in an allowed set `{"Skill lab"}`; weeks are 1-14; every week 1-13 has a heading in `levelN-weeks.md`; report modules with zero videos. Add a step to "Keeping the data fresh": "run `validate_data.py` after every edit". Regenerate the missing L1 Wk 8 and L3 Wk 7 blocks from the raw text. → M
5. **Fix the phase heuristic and the search guardrail** → #6, #7. `phase = "mid" if re.search(r"mid", what, re.I) else ("final" if re.search(r"end", what, re.I) else "practical-only")`. In `search()`, add `if v["id"] in VID["excluded_videos"]: continue`. → S
6. **Move the raw schedules out of the default path** → #10. Keep `references/raw/` but replace the fallback sentence with: "If code can't run, read only `semester.json` and the one `levelN-weeks.md`; open `raw/` only to repair a missing week." → S
7. **Use Cairo time** → #11. `today = dt.datetime.now(zoneinfo.ZoneInfo("Africa/Cairo")).date()`. → S

**Quick wins (<30 min):** Rec 1 (example), Rec 2 (stale gate and description), Rec 5, Rec 7, and the fallback-wording change in Rec 6.

**Open questions:**
- Is CAD practical surfacing in week 7 intentional (skill-lab rotation)?
- Will the owner supply the second-semester PDFs before February 2027? Is a `semester-2026-2027-s2.json` with a selector preferred over overwriting?
- Should "Skill lab" become a pseudo-module per level in `semester.json`?

[↑ back to contents](#table-of-contents)

---

#### ymnotes-youtube-video-finder
**Identity:** no version · authored for ChatGPT/Codex (`agents/openai.yaml` products chatgpt/codex/api/atlas) · 7 files / ~15 KB · last updated unknown · entry point: `SKILL.md` (4 references, no scripts)

**Purpose & triggering:** Finds the YouTube video(s) that best fit a topic, page range, handout or screenshot. It ranks by verified concept coverage, not popularity, separately for English and Arabic. The description is good. It covers the branches (topic, page range, screenshot, language, contextual follow-ups) and states negative scope (thumbnails, production, account management). Its negations ("Do not trigger for…") partly overlap with `ymnotes-video-visuals` and the Premiere skills, which is useful disambiguation. It overlaps with `ymnotes-batch-messages` on "which video fits", and should say it is for any channel, while batch messages handles YMnotes' own videos for a دفعة.

**How it actually works:**
1. Build a concept checklist from the source material (`SKILL.md:10-19`, `references/source-matching.md`).
2. Search with `site:youtube.com/watch` query variants, at most 2 refinement rounds (`SKILL.md:21-31`, `references/search-playbook.md:3-13`).
3. Rank with the confirmed/partial/unknown rubric and an optional weighted percentage (`references/evaluation-rubric.md:15-21`).
4. Format the answer (`references/output-template.md`).
Everything is instructions. There is no code and no API.

**Strengths to keep:**
- Calibrated evidence language (fit vs confidence; "unknown" vs "not covered") and the ban on fake "87% match" scores (`SKILL.md:41-45`; `evaluation-rubric.md:15-19`).
- Printed-page vs viewer-index handling, including the YMnotes GIT handout's green box (`SKILL.md:14`).
- The spoken-language rule: "English speaker" means spoken English, and titles do not prove language (`SKILL.md:17`, `search-playbook.md:15`).
- Prompt-injection hygiene: retrieved pages are data (`SKILL.md:31`).
- A stopping rule with a budget (`search-playbook.md:13`).
- No paid API or account is required.

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | The skill is ChatGPT-specific. `agents/openai.yaml` and the scope paragraph talk about "ChatGPT mode", Android, and personal skills, which is irrelevant or confusing for Claude. | `SKILL.md:62`; `agents/openai.yaml:10-14` | V-SRC | Low |
| 2 | Verification depends on tools Claude may not have. Claude Code `WebFetch` of youtube.com watch pages returns JS-heavy HTML, so chapters and description sit in `ytInitialData` and may be stripped. claude.ai web fetch is similar. Neither has native transcript access. The skill handles absence gracefully (`SKILL.md:29-31`) but gives no concrete Claude route, for example the playlist-page `ytInitialData` approach that `ymnotes-batch-messages` already uses (`ymnotes-batch-messages/SKILL.md:68`) or the YouTube oEmbed endpoint for title and channel. | `SKILL.md:23-31` | INF | Med |
| 3 | It does not know the YMnotes catalogue. For a YMnotes creator, the owner's own videos (`ymnotes-batch-messages/references/videos.json`) are a natural first candidate set, but the skill says "Do not hardcode favorite channels as winners", and nothing tells it to at least check YMnotes. | `search-playbook.md:11` | INF | Med |
| 4 | Context cost: the SKILL body is ~7.8 KB (~2k tokens), with many hedge sentences that are probably no-ops for Claude ("Keep the response brief", "Answer in the user's conversational language", "Do not invent IDs"). There is room to prune by ~30%. | `SKILL.md:8,28,58` | INF | Low |
| 5 | Heavy negation steering ("Do not…", "Never…" ~20 times). The rubric flags this as a variance risk. | `SKILL.md` throughout | V-SRC | Low |
| 6 | There are no evals or test prompts for a skill whose value is ranking judgement. | none present | V-SRC | Low |
| 7 | `assets/icon.svg` and `agents/openai.yaml` are unused by Claude. They cost no context, but they are dead weight for this platform. | files | V-SRC | Low |

**Recommendations:**
1. **Add a Claude tool route** → #2. In "Search and inspect", add: "In Claude: `WebSearch` with `allowed_domains:["youtube.com"]`; confirm title and channel with `https://www.youtube.com/oembed?url=<watch-url>&format=json`; for chapters, fetch the watch page and read the `ytInitialPlayerResponse.videoDetails.shortDescription`. If WebFetch strips it, label confidence 'title/snippet only'." → S
2. **Check YMnotes first** → #3. Add a line: "When the topic matches an O6U module, also check `ymnotes-batch-messages/references/videos.json` (search by title) and include a YMnotes video if it is a genuine fit; rank it by the same rubric." → S
3. **Make it portable** → #1, #7. Replace `SKILL.md:62` with "Never claim that this skill watches videos, retrieves transcripts it was not given, or changes a YouTube account." Keep `openai.yaml` only if the skill is shared with ChatGPT. → S
4. **Prune and turn negations positive** → #4, #5. For example, turn "Do not claim an exhaustive… best" into "Say 'closest match I found'". Remove the generic no-ops. → M
5. **Add 3-5 eval prompts** (`evals/`): page-range GIT handout, "Arabic only, under 15 min", and a contextual follow-up, "now investigations". → M

**Quick wins (<30 min):** Recs 1-3.

**Open questions:**
- Should YMnotes' own videos get priority or only equal consideration?
- Is the skill still shared with ChatGPT (keep `openai.yaml`) or is it Claude-only now?

[↑ back to contents](#table-of-contents)

---

#### ymnotes-video-visuals
**Identity:** no version · authored for ChatGPT image generation (`agents/openai.yaml` products chatgpt/codex/api/atlas) · 7 files / ~14 KB · last updated unknown · entry point: `SKILL.md` (3 references, 1 unreferenced SVG guide)

**Purpose & triggering:** Produces one YMnotes-branded 16:9 intro/start image that doubles as a thumbnail, and keeps the bottom-right webcam area clear. Input can be a topic, a screenshot, a book chapter, or a mix. The description wastes words and is mis-addressed. "Use when ChatGPT needs to generate…" names another product, and the description repeats body detail (mainly English, polished, webcam). It also lacks the user's real trigger words ("thumbnail", "صورة البداية", "intro image", "cover for the video"). Overlap: `medical-visual-board` makes study boards (multi-image), not video frames, so they overlap only in "medical visual". The descriptions should cross-exclude. No overlap with `etymology` or `ymnotes-qr`.

**How it actually works:** Instructions only.
1. Identify the input mode (`SKILL.md:51-57`).
2. Distil 1 concept and 2-4 subthemes (`:59-68`).
3. Pick an archetype (`references/visual-system.md:15-88`).
4. Set the text hierarchy (`:75-82`).
5. "Generate", self-check, do one repair pass (`:84-93`).
6. If image generation is unavailable, output a prompt (`:154-155`).
There is no generation tool named, no code and no render step.

**Strengths to keep:**
- A concrete, measurable webcam-safe zone (right 22-28% × bottom 22-28%) with a list of what may and may not go there (`SKILL.md:35-47`, `visual-system.md:121-135`).
- A clear text hierarchy (3-8-word title, max 2-4 labels) and a micro-copy bank.
- The archetype menu encourages variety without losing the brand.
- "Never use or invent the user's face" (`SKILL.md:27`).
- A graceful fallback to a production-grade prompt (`SKILL.md:155`).

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | The skill is not portable to Claude as written. It assumes native image generation (ChatGPT). Claude has no built-in raster image generation, so in most Claude surfaces it silently drops to the "prompt only" fallback. In this environment a Canva connector exists (`mcp__Canva__generate-image`, which supports `aspectRatio: LANDSCAPE_16_9`), but the skill never mentions it. Code-rendered SVG/HTML-to-PNG (Claude Code, claude.ai sandbox) is another unmentioned route that would let the webcam zone be enforced exactly. | `SKILL.md:3,12,154-155`; Canva tool schema | V-SRC / INF | High |
| 2 | The description is mis-addressed and bloated ("ChatGPT needs to…", style adjectives). It has no thumbnail/Arabic trigger words, so it risks under-triggering in Claude. | `SKILL.md:3` | V-SRC | Med |
| 3 | The self-check cannot be verified. "Mentally check… bottom-right preserved" cannot actually be checked for a generated raster. Generative models routinely ignore "keep corner empty". There is no step to view the result, measure the zone, or overlay `assets/webcam-safe-area.svg`. | `SKILL.md:84-93` | INF | Med |
| 4 | `assets/webcam-safe-area.svg` is never referenced, so the agent will not find it. | `SKILL.md` (no mention); `assets/webcam-safe-area.svg:4` | V-SRC | Low |
| 5 | Medically wrong example. For "Cranial Nerve Examination" the anchors given are "motor testing, sensory testing, reflexes, gait/coordination". That is the general neurological exam, not CN I-XII. It could seed wrong subthemes on a branded image. | `references/input-modes.md:11-13` | V-SRC | Med |
| 6 | Duplication: the webcam rules appear in 3 places, the branding forms in 2, and the micro-copy in 2. That costs maintenance and tokens. | `SKILL.md:35-47`, `visual-system.md:107-135`, `output-patterns.md:36-44,62-70` | V-SRC | Low |
| 7 | No brand colours or logo are specified. "YMnotes feel consistent" is undefined, while `ymnotes-qr` defines the brand palette (green `#0B5A34`, orange `#EA6014`, teal `#007A87`). Outputs will drift. | `visual-system.md:98-105` vs `ymnotes-qr/SKILL.md:93` | V-SRC | Med |
| 8 | Medical accuracy is unguarded. There is no instruction to verify anatomical labels or terms on the image (generators misspell and mislabel anatomy). | `SKILL.md:107-122` | INF | Med |
| 9 | There are no tests or examples of good outputs. | none present | V-SRC | Low |

**Recommendations:**
1. **Add a Claude generation path** → #1, #3. Replace "Core behavior" with:
   ```
   Pick the first available route:
   A) Canva connector: mcp__Canva__generate-image {prompt, aspectRatio:"LANDSCAPE_16_9"}; then view the result.
   B) Code render (Claude Code / sandbox): compose an HTML/SVG 1920x1080 frame (title, hero art, brand strip),
      render to PNG (playwright or cairosvg), with the webcam zone x>=1440, y>=810 kept empty by construction.
   C) Neither: give one production prompt (output-patterns.md skeleton) and say no image tool is available.
   After A or B, look at the image and confirm: the title is legible at 320 px wide, the bottom-right 25% x 25% is empty, and the anatomy labels are spelled correctly. Do one repair pass at most.
   ```
   → M
2. **Rewrite the description** → #2. "Create one YMnotes-branded 16:9 lecture intro image or YouTube thumbnail from a topic, chapter, or screenshot of notes, keeping the bottom-right clear for the webcam. Use for 'thumbnail', 'intro/start image', 'صورة البداية', 'cover for the video'. Not for multi-image study boards (medical-visual-board)." → S
3. **Fix the CN example** → #5. Use anchors such as "CN I-XII, eye movements (III/IV/VI), facial sensation & motor (V/VII), bulbar (IX-XII)". → S
4. **Add brand tokens** → #7. In `visual-system.md`: "Brand: green #0B5A34, orange #EA6014, teal #007A87; 'YMnotes' wordmark top-left." Ask the owner to confirm. → S
5. **Deduplicate** → #6. Keep the webcam rules only in `SKILL.md`, and the archetypes and micro-copy only in references. Reference `assets/webcam-safe-area.svg` from the self-check (#4). → S
6. **Add a label accuracy check** → #8. "Every anatomical label or term on the image must be spelled and placed correctly; when unsure, drop the label." → S

**Quick wins (<30 min):** Recs 2-6.

**Open questions:**
- Which image route does the owner actually use in Claude: the Canva connector, code rendering, or a ChatGPT hand-off?
- Is there an official YMnotes logo file that should ship in `assets/`?
- Exact webcam box geometry in OBS/Premiere: is it 350×220 at (1200,650) on a 1600×900 canvas, as the SVG implies?

[↑ back to contents](#table-of-contents)

---

#### ymnotes-qr
**Identity:** no version · local/custom; the script originated in the GitHub repo `youssif3863/ymnotes-files` (`scripts/ymnotes_qr.py:2-9,29-31`) · 2 files / ~21 KB · last updated unknown · entry points: `SKILL.md`, `scripts/ymnotes_qr.py qr`

**Purpose & triggering:** Uploads a student file to a public "YMnotes Files" Drive folder (per-subject subfolders). It builds a `/file/d/<id>/view` link, checks that the link opens without sign-in, and renders a branded, decode-checked QR card for use in videos. The description is too thin for model invocation. It has no "Use when" branches (QR for a video, share handout with students, replace a file behind an existing QR, re-title a card) and no Arabic triggers. No overlap with the other three skills, except that it shares brand colours with video-visuals (which lacks them).

**How it actually works:**
1. `get_file_permissions` on the root folder must show `anyone` (`SKILL.md:30-31`).
2. `search_files` / `create_file` for the subject folder (`:32-34`).
3. `create_file` with `base64Content` and `disableConversionToGoogleType` (`:35-39`). The parameter names match the current Drive connector schema (verified against tool schema).
4. Build the link (`:40-41`).
5. Verify in the built-in browser, not curl (`:42-47`).
6. `pip install segno pillow opencv-python-headless`, then `ymnotes_qr.py qr` (`:48-55`). `make_card()` builds an ECC-H QR, a 22% centre badge, the title (≤3 lines) and the subtitle (`ymnotes_qr.py:116-158`). `check_decodes()` resizes to 300/450/700 px and passes on 2 of 3 decodes (`:161-170`).
7. Deliver with `SendUserFile` (`SKILL.md:56-59`).

**Strengths to keep:**
- Clear invariants: "the link never breaks / the QR always scans" (`SKILL.md:12`).
- A correct "Manage versions → Upload new version" procedure keeps the file ID. The connector's `update_file` limits are stated accurately (`SKILL.md:61-67`).
- The connector limit is stated honestly: `share_file` cannot set "anyone with link", so that is a one-time manual setup (`SKILL.md:79-85`). This matches the `share_file` schema (user, group or chat space only).
- The automated decode check at phone-like sizes, with ECC-H and a badge sized within the recovery budget.
- "Never type the user's password" (`SKILL.md:85`).

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | Personal data hardcoded in the skill: the owner's personal Google account email and the public folder ID/URL. Anyone who receives the skill bundle gets the folder link and can browse every published file. Values withheld. | `SKILL.md:15,16-17,46,64,66,81`; GitHub owner `scripts/ymnotes_qr.py:29` | V-SRC | Med |
| 2 | Public folder risk. The root folder is mandated "Anyone with the link: Viewer" and every file inherits that. Any file mistakenly placed there (paid e-teaching.site material, student lists, exam questions) becomes public, and the folder itself can be browsed. There is no rule on what must never be uploaded, and no per-upload check. | `SKILL.md:19-21,30-31,73-76` | V-SRC / INF | High |
| 3 | Stale script and docs. The script's docstring and 3 of 4 subcommands (`add`, `verify`, `render`, plus `catalog.json`/README/GitHub Pages logic, ~60% of the file) describe the retired GitHub workflow. The SKILL uses only `qr`. The README text it renders even points to `.claude/skills/ymnotes-qr/` in that repo. This misleads an agent that reads `--help`. | `scripts/ymnotes_qr.py:2-9,29-31,99-113,174-312`; `SKILL.md:87-90` | V-SRC | Med |
| 4 | `cmd_qr` exits 0 even when `decodes:false`, so a caller that checks exit codes misses the failure. `check_decodes` also crashes if `cv2.imread` returns `None`. | `scripts/ymnotes_qr.py:315-318,163-167` | V-SRC | Low |
| 5 | Surface-specific tools. `SendUserFile`, the built-in browser `navigate`/`get_page_text`, and "Claude in Chrome" (`SKILL.md:42-47,56,64`) exist only in some Claude surfaces (desktop/Cowork). claude.ai web has none of them, and `pip install` needs network in the sandbox. No fallback is given for "no browser": the step just says "if it fails, fix sharing". | `SKILL.md:42-56` | INF | Med |
| 6 | The verification assumption is fragile. "Built-in browser is not signed in to Google" is assumed, not checked. If it is signed in as the owner, the public-access test gives a false pass. | `SKILL.md:44-47` | INF | Med |
| 7 | Arabic titles: `font()` falls back to DejaVu, and Arabic shaping needs Pillow built with libraqm. Here `raqm=True` (V-RUN), but on hosts without fribidi/raqm Arabic titles render as disconnected, left-to-right glyphs. `wrap()` also measures LTR. The decode check does not catch bad text. | `scripts/ymnotes_qr.py:60-96` | INF | Low |
| 8 | The size limit is vague ("files up to a few MB"). There is no number, and no size check before base64-encoding into a tool call. A large PDF can blow the context and fail mid-call. | `SKILL.md:37-39` | V-SRC | Low |
| 9 | The description gives no trigger branches (see Purpose). | `SKILL.md:3` | V-SRC | Med |
| 10 | No tests. The QR script was not executed here because segno/opencv are not installed and installing them needs network, which the rules forbid. Rendering and decoding are unverified in this review. | env check | V-RUN (deps absent) | Low |

**Recommendations:**
1. **Guard what goes public** → #2. Add a "Before upload" step: "This folder is public. Upload only material meant for anyone (free handouts, figures). Stop and ask if the file is paid course content, exam questions, or contains student names, phones or IDs. After upload, run `get_file_permissions` on the file and confirm the roles are owner plus `anyone:reader` only." Consider a per-file model instead (`inheritedPermissionsDisabled` folders, with only the file set public through the Drive UI) if browsable-folder exposure matters. → S
2. **Move the identifiers out of the body** → #1. Put the account and folder ID in `references/config.md` (or an env/config file) and have the steps read "the configured root folder". Do not embed the folder URL; the ID is enough for the API. → S
3. **Trim the script to the `qr` command** → #3, #4. Delete `add`/`verify`/`render`/catalog code (keep them in git history) and fix the docstring to "Make a YMnotes-branded QR card for a URL and check it decodes". Add `if img is None: sys.exit(...)` and `sys.exit(0 if ok else 2)` in `cmd_qr`. → S
4. **Add surface fallbacks** → #5, #6. Step 5: "If no unsigned browser is available, ask the user to open the link in a private/incognito window and confirm it opens; do not mark it verified yourself." Step 7: "If `SendUserFile` is unavailable, save the PNG and give its path (Claude Code), or attach it (claude.ai)." Before trusting the browser test, check it is not signed in by loading `accounts.google.com` and seeing a sign-in prompt. → S
5. **Rewrite the description** → #9. "Publish a YMnotes student file to the public YMnotes Files Google Drive folder and return a branded QR card with its title. Use when the user wants a QR code for a handout/image to show in a video, to share a file with students by QR, to replace the file behind an existing QR, or to re-title a QR card (باركود، QR للملف)." → S
6. **Set a hard size limit** → #8. "If the file is over 10 MB, do not base64 it; use the Drive website or ask the user." (Agree the number with the owner.) → S
7. **Add an offline smoke test and an Arabic check** → #7, #10. Add `scripts/test_qr.py`: render a card for a dummy URL with an English and an Arabic title, assert `decodes`, and save the PNG for a visual check; print `PIL.features.check('raqm')` and warn if it is false. → S

**Quick wins (<30 min):** Recs 1, 2, 4, 5, 6, plus the two-line exit-code fix from Rec 3.

**Open questions:**
- Has anything non-public ever been placed in the YMnotes Files folder? A one-time audit of its contents is advisable.
- Is a browsable public folder intended (a student "library"), or is per-file link sharing enough?
- In which Claude surface is this skill usually run? That decides the browser and `SendUserFile` fallbacks.
- Should the brand palette here become the shared source of truth for `ymnotes-video-visuals`?

[↑ back to contents](#table-of-contents)

---

#### medical-visual-board
**Identity:** no version · user-authored, evidently written for ChatGPT (openai.yaml, "native gallery", "search-results carousel") · 5 files, about 30 KB · manifest updatedAt 2026-09-09 · entry point: SKILL.md (model-invoked); evaluations/scenarios.md (manual)

**Purpose & triggering:** Builds "Pinterest-style" boards from supplied notes or concept lists: a short title plus one medically meaningful image per concept, or one combined comparison canvas. It controls counts, order, provenance and revisions. The description is accurate and has good negative scope (not explanations, diagnosis, slides). It says nothing about the image capabilities it depends on. Overlap: `ymnotes-video-visuals` also produces medical images, but only one branded 16:9 intro/thumbnail. The boundary is clear in substance, but both descriptions say "medical … visuals from notes/screenshots", so a request like "make a visual from this chapter" could fire either. `ymnotes-medical-book-redesign` (figures in books) is a weaker overlap.

**How it actually works:** Prompt only. Lock the output contract (counts, order, language, revision targets) SKILL.md:10-19 → bound concepts to the supplied source; external sources may verify depiction but not add topics :21-29 → per-asset scratch row :31 → route: real image for clinical/radiology/histology, sourced or generated diagram for anatomy/mechanism :33-45 → capability check :47-53 → visual accuracy gate: inspect the actual pixels, laterality, provenance, watermark :55-64 → present title+image, attribution, no placeholders :66-72 → revision rules :74-76 → final check :78-80. References: visual-decisions.md (modality table, source ranking, licence checks), comparison-illustrations.md (generation prompt pattern, inspect/repair).

**Image tools needed, and availability in Claude:**
| Capability the skill assumes | Where used | Available in Claude? |
|---|---|---|
| Image **search** that returns viewable image results (a "carousel") | :39, :71; visual-decisions.md:159-163 | **No native image search.** Claude WebSearch returns text results and URLs, and WebFetch turns pages into markdown, so it cannot see images. In Claude Code, a workaround is curl-download the image file → `Read` it (Claude can view local images), or a Playwright screenshot. (INF/V-SRC from tool descriptions) |
| Image **generation** / editing | :40-45; comparison-illustrations.md:103-124 | **No native generation in Claude.** In this account it is only reachable through the **Canva MCP** (`generate-image`, `edit-design`, `merge-designs`), which is not mentioned anywhere in the skill. (V-SRC: tool list) |
| Image **viewing / inspection** | :53, :57 | **Yes** for user uploads (chat) and for local files via `Read` (Claude Code). |
| One-canvas **composition** of real images | :41, :50 | Not native. Possible via Python/Pillow in Claude Code, an HTML artifact, or Canva `merge-designs`/`create-design`. |
| **Delivery** of images inline ("native gallery", embedded image) | :69-71 | claude.ai chat does not render arbitrary external image URLs in markdown. An HTML artifact can display a gallery, but external hotlinks may be blocked by CSP; embedding as data: URIs or uploaded assets is the safer route. (INF) |

**Strengths to keep:**
- Unusually rigorous contract handling: an exact-N-assets definition, one-canvas means one asset, and the newest correction wins only on conflicting points (:14-19).
- Medical safeguards are strong and specific: source bounds membership; external sources verify but cannot add diagnoses (:25); patient vs viewer laterality (:60; comparison-illustrations.md:95,109); no synthetic radiograph presented as real (:45); unresolved defects never marked passed (:64).
- Privacy rules for patient uploads (:29, comparison-illustrations.md:111).
- Licence and watermark discipline (visual-decisions.md:162).
- 14 well-designed adversarial scenarios with withheld pass criteria (evaluations/scenarios.md).
- Honest capability fallback: "Prompts, search links, and placeholders are not a completed visual board" (:52).

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | The skill is written for ChatGPT's image toolset (image search carousel, built-in generation, native gallery). In Claude, two of its three routes (search with viewing, generation) have no native tool, so most boards fall to the "Neither" branch → a limitation message. | SKILL.md:39-41,47-52,69-71; agents/openai.yaml | V-SRC + INF | High |
| 2 | The only generation path in this account (Canva MCP) and the Claude Code inspection path (download → `Read`) are not mentioned, so the model is unlikely to find them. | SKILL.md:47-53 | V-SRC | Med |
| 3 | Evaluations are manual prose. Nothing records that they were run, there are no results, and no harness exists. "Do not report different named models as tested unless they actually ran" (scenarios.md:7) suggests no runs are logged. | evaluations/scenarios.md:3-7 | V-SRC | Med |
| 4 | Trigger overlap with `ymnotes-video-visuals` on "medical visual from notes/screenshot". Neither description names the other. | SKILL.md:3; ymnotes-video-visuals/SKILL.md:3 | V-SRC | Low |
| 5 | Heavy context: the SKILL.md body is about 10.7 KB (about 2.7k tokens), with long, abstract, dense sentences. Several lines are no-ops for a careful model, e.g. "Keep varied visuals harmonious and uncluttered" (:69). | SKILL.md | V-SRC | Low |
| 6 | Licence and reuse verification is demanded (visual-decisions.md:162) but no practical route is given (e.g., Wikimedia Commons / Open-i / NIH image-licence fields). In practice the model may stall or over-claim. | visual-decisions.md:157-165 | INF | Med |
| 7 | The description doesn't say what it needs. A Claude user asking for a board gets no early signal that generation is missing until mid-run. | SKILL.md:3, :47 | INF | Low |
| 8 | Medical-accuracy verification depends on "reliable verification material" with no named sources. For a medical creator this is the key safeguard. | SKILL.md:60; visual-decisions.md:155 | V-SRC | Med |

**Recommendations:**
1. Add a "Claude tool map" section → (#1, #2) draft for SKILL.md after :47:
   ```
   ## Tools in Claude
   - Find real images: WebSearch for pages → download candidate image (curl -L -o) → Read the file to inspect pixels. Prefer Wikimedia Commons, Open-i (openi.nlm.nih.gov), Radiopaedia (check licence), PubMed Central OA figures.
   - Generate a schematic: Canva MCP generate-image (label it "Illustration").
   - One canvas from real images: Python Pillow grid in Claude Code, or Canva merge/create-design.
   - Deliver: an HTML artifact gallery with images embedded (data: URI or uploaded assets), title above each, source link beside it.
   ```
   → M
2. Run the 14 scenarios once in Claude and log the results → (#3) add `evaluations/results-YYYY-MM-DD.md` with case | model | pass/fail | note. → M
3. Name verification sources → (#6, #8) add to visual-decisions.md: "Verify anatomy and appearance against at least one of: Radiopaedia, DermNet, StatPearls/NCBI Bookshelf, Gray's/Netter (if the user supplies them); licence from the image page's own licence field (CC-BY etc.)." → S
4. Disambiguate from ymnotes-video-visuals → (#4) append to the description: "For a single branded 16:9 intro/thumbnail, use ymnotes-video-visuals." and add the reverse line there. → S
5. Prune no-ops and compress → (#5) target about 7 KB. Merge the capability bullets (:49-53) into the new tool map. → M

**Quick wins (<30 min):** add the cross-pointer to ymnotes-video-visuals (#4); add the named source list (#8); add a one-line "Needs: image viewing; real-image download or Canva generation" note to the body's capability section (#7).

**Open questions:**
- Is this skill mainly used in ChatGPT (where its tools exist) or in Claude? If ChatGPT only, consider making it user-invoked in Claude to save context load.
- Is the Canva MCP an acceptable generator for medical schematics (accuracy and branding)?
- Where should boards be delivered in Claude: artifact, Google Drive folder (as with ymnotes-qr), or local files?

[↑ back to contents](#table-of-contents)

---

#### etymology
**Identity:** no version · user-authored (no upstream) · 4 files, about 21 KB (SKILL.md 7.9 KB, references/medical-affixes.md 10 KB, references/examples.md 2.7 KB, agents/openai.yaml) · manifest updatedAt 2026-10-23 · entry point: SKILL.md (model-invoked); `agents/openai.yaml` for Codex/ChatGPT

**Purpose & triggering:** Breaks a word into its morphemes and gives English and Arabic part meanings, a literal reconstruction, the accepted Arabic term, short definitions, and a "what it means in *your* material" line. The audience is Arabic-speaking medical students. The description is accurate and has good bilingual trigger phrases (أصل الكلمة، ليه اسمها كده). It also sets negative boundaries (plain translation, spelling, pronunciation). At 854 characters it is the longest description of the four, and it restates output-format detail ("part-by-part meanings, literal reconstruction, accepted Arabic term…") that the body already carries. I found no real overlap with other skills. The nearest neighbours are `ymnotes-medical-book-redesign` and `ymnotes-questions`, and neither does morphology.

**How it actually works:** All of it is prompt, with no code. Workflow SKILL.md:12-21 (pin term → look for context in uploads → classify formation → split → literal → define using `references/medical-affixes.md` → context line → one distinction) → output template :23-41 → multi-term table rule at 4+ terms :69-77 → Arabic layout rules :79-84 → accuracy rules :86-94 → self-check :96-98. Non-standard cases point to `references/examples.md` (:67).

**Strengths to keep:**
- The context step (:15) is the real differentiator, and it has an explicit honesty guard ("never pretend to have read something you have not seen").
- Concrete accuracy rules: no splitting on resemblance alone, eponyms not split, Arabic words analysed by root and pattern (جذر/وزن), and misleading literal meanings flagged (:90-92).
- A curated Arabic glossary that fixes the most-confused surgical trio (بَضْع / استئصال / فَغْر) and states that an established whole-term translation beats an affix calque (medical-affixes.md:5).
- RTL/LTR layout guidance (:84) is a real, non-obvious gotcha worth caching.
- Tight length budget (70–130 words), so output stays scannable.

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | Broken internal cross-reference: the affix file points to a heading "Accuracy and verification" in SKILL.md, but SKILL.md's heading is "## Accuracy". | references/medical-affixes.md:6; SKILL.md:86 | V-SRC | Low |
| 2 | Nothing tests medical or Arabic accuracy: no evals, no golden set. The glossary is the only safeguard, and a reviewer has not signed it off (no source/date line). A wrong affix propagates into every word that uses it (the skill's own warning, :88). | whole skill; medical-affixes.md:3 | V-SRC | Med |
| 3 | The "check a reliable dictionary" instruction has no named source or tool. In Claude it would need WebSearch/WebFetch, so in practice the model falls back on memory. | SKILL.md:93 | INF | Med |
| 4 | Description is long (854 chars, always loaded) and repeats body content. The rubric says to cut identity the body already carries. | SKILL.md:3 | V-SRC | Low |
| 5 | Some glossary entries are loose or contestable: `-osis` → "داء / تَفَعُّل" (تفعّل is a morphological pattern, not a gloss); `-trophy` → "ضخامة / ضمور" (lists two opposite outcomes as the meaning of a part that means "nourishment"); `pan-` example "قلة الكريات الشاملة" (the more usual form is قلة الكريات الشاملة/نقص الكريات الشامل; acceptable but worth checking against المعجم الطبي الموحد). | medical-affixes.md: rows -osis, -trophy, pan- | V-SRC (content judgement) | Low |
| 6 | Contradiction: the body says to skip origin languages (:10), yet every glossary row carries a Greek/Latin "Origin" column. This is harmless (it is used "silently") but costs tokens each time the file loads. | SKILL.md:10; medical-affixes.md tables | V-SRC | Low |
| 7 | The Codex-oriented `agents/openai.yaml` ships in a Claude skill. It is harmless but dead weight for Claude. | agents/openai.yaml | V-SRC | Low |
| 8 | The skill has a lot of negation ("No quizzes, history…", "Do not add pronunciation", "Never split…"). Most of it is legitimate guardrails, but :94 ("Do not add pronunciation unless asked") is a probable no-op, because the template has no pronunciation slot. | SKILL.md:41,94 | V-SRC | Low |

**Recommendations:**
1. Add a 10-case golden eval file (`evaluations/cases.md`) → so that accuracy is checked, not assumed (#2). Draft rows: `cholecystectomy` (trio distinction), `anemia` (established term beats literal), `hematoma` (-oma ≠ tumour), `Bell's palsy` (eponym), `CABG` (acronym), `صُداع` (root/pattern), `ileum vs ilium`, `myelitis vs myositis`, a 5-term slide list (table mode), a term present in an uploaded handout (context line). For each, record the expected Arabic term and the parts. Re-run whenever the glossary changes. → M
2. Fix the cross-reference → (#1) change medical-affixes.md:6 to `(see "Accuracy" in SKILL.md)`. → S
3. Name the verification source → (#3) replace SKILL.md:93 with: "If unsure about a part, verify with WebSearch (e.g., Merriam-Webster Medical, Dorland's, or المعجم الطبي الموحد at emro.who.int/umd) and say "verified" only if you opened a source." → S
4. Trim the description → (#4) draft: `Break a word (medical or general, English or Arabic) into its meaningful parts and explain it in English and Arabic, including what it means in the user's own material. Use when the user says "Etymology", asks what a prefix/suffix/root means (-itis, hepato-), why something is called what it is, wants terms from a slide/list broken down, or asks أصل الكلمة / تفكيك المصطلح / ليه اسمها كده. Not for plain translation, spelling or pronunciation.` (about 430 chars). → S
5. Add a provenance line to the glossary and review flagged rows → (#5) "Reviewed against المعجم الطبي الموحد, <date>, by <name>", and fix -osis/-trophy glosses (e.g., -trophy → "تغذية (→ حجم الخلية)"). → S
6. Optional: drop the Origin column, or move it to the end → (#6). → S

**Quick wins (<30 min):** fix the heading reference (#1); shorten the description (#4); delete line :94 (#8); add a "Reviewed:" line to medical-affixes.md.

**Open questions:**
- Is the skill also used in ChatGPT/Codex (hence openai.yaml)? If so, keep the file. If not, drop it.
- Should Egyptian-Arabic glosses be the default for YMnotes audiences (currently opt-in, :81)?

[↑ back to contents](#table-of-contents)

---


### D. Operations automation

#### ymnotes-register-students

**Identity:** no version field · two copies: the synced plugin copy (`SYN/ymnotes-register-students`, manifest `updatedAt` 2026-10-22T12:30Z, `backingPluginId plugin_012if…`) and the repo copy (`RS/`, last commit `1abd5aa`, 2026-10-22 15:13 +0300, PR #13) · 3 files, 32 KB (SKILL.md 7.3 KB, REFERENCE.md 5.6 KB, drive.js 19 KB) · entry points: SKILL.md procedure, `node .claude/skills/ymnotes-register-students/drive.js register '<json>' [--dry-run]`, and the step-runner mode (`drive.js '<steps>'`) for troubleshooting.

**Copy diff (asked):** the copies have the same content. `diff` shows a single difference: SKILL.md:3 is a quoted YAML string in the synced copy and a plain scalar in the repo copy. REFERENCE.md and drive.js are byte-identical.
- **Which is newer:** the synced copy was uploaded about 17 minutes after the last repo commit (15:13 +0300 is 12:13Z, and the upload was 12:30Z). It is a re-serialised export of the same commit, so neither copy is newer in substance. File mtimes are only sync and checkout times (2026-11-01).
- **Which is better:** the synced copy, slightly. The repo copy's frontmatter is **not valid strict YAML**: `yaml.safe_load` fails with "mapping values are not allowed here" because `Parameter: window` puts a `: ` inside a plain scalar (V-RUN). Claude Code's lenient loader still lists the skill, but other hosts or validators may not.
- **Drift risk:** both copies load in this session, as `ymnotes-register-students` and `anthropic-skills:ymnotes-register-students`. That means two identical descriptions in context and an ambiguous choice of which one to invoke.
- **Recommended single source of truth:** the repo copy, because the allow rule (`REPO/.claude/settings.json:5`) and the scheduled runs (`RS/SKILL.md:19,29-30`) depend on the repo path.

**Purpose & triggering:** The skill reads `[YMnotes]` registration emails from the last N hours (default 25). It classifies each one as a `full` or `questions` plan from the subject and snippet, then registers all students in one headless Playwright run on the e-teaching.site Flutter app. Finally it labels the handled threads and writes a short report. The description is accurate, specific and carries the trigger words ("register / add / process YMnotes students", "scheduled daily run"). It does overclaim that the students are **paid**: the skill never verifies payment (see F1). It overlaps with nothing except its own duplicate plugin copy.

**How it actually works:**
1. Gmail search: `subject:"[YMnotes]" after:<epoch> -label:ymnotes-registered` (`RS/SKILL.md:48-51`). If there are no results, it stops before opening the browser.
2. The plan comes from the subject (REJECTED / ACCEPTED / MANUAL REVIEW) and the Course and Amount fields (`SKILL.md:52-66`). An optional read-only n8n lookup is allowed for unclear emails only (`:68-72`).
3. One `drive.js register` call. `login()` reads the control positions on page A with semantics on (`drive.js:49-59`), then taps those positions on page B with semantics off. It checks the field lengths before SignIn (`:62-84`). `openAddStudent` handles the menu: it finds the menu node's box, with a fixed fallback point (`:120-132`).
4. `registerOne` validates the code with `^\d{4,7}$` (`:180`). It searches (`:133-143`) and guards against stale results (`:187`). It detects the green group cards from 10×10 screenshot patches (`:146-164`) and checks for an existing registration ("already") or a mixed case that comes back "unclear" (`:192-201`). It then selects the groups, verifies them, picks the date (`:165-176`), saves (`:211`) and verifies by searching again (`:215-219`).
5. Exception path: if the page is no longer Add Student, it logs in again on a fresh context (`:230-239`). Exit codes are 0 / 1 / 2 / 3, and code 3 means "do not retry" (`SKILL.md:82`).
6. It labels threads whose codes came back `registered` or `already` (`SKILL.md:84-86`) and writes the report (`:87-96`).

**Strengths to keep:**
- Credential discipline. The values live only in environment variables and every output line is scrubbed (`drive.js:25,29-30`). The field lengths are checked before submitting, so a mistyped login cannot burn a failed attempt (`:75-76`), and the password submit is never retried (`REFERENCE.md:60`).
- Idempotency comes from the site, not only from the Gmail label: "Already registered" plus the green groups (`drive.js:192-195`). Every save is re-verified on the site (`:215-219`). Mixed or shared-expiry cases are handed to the owner instead of changed (`:196-198`).
- The skill takes no action when it is unsure: unclear, failed and REJECTED threads stay unlabeled (`SKILL.md:42,86`), and the authority boundaries are tight: Gmail is read-and-label only, n8n is read-only, and the site action is limited to Add Student (`SKILL.md:32-44`).
- It is economical. There is no browser when there is no mail, one login per run, and SKILL.md and REFERENCE.md are split so the runtime file stays small (`SKILL.md:12-13,46`).
- Lessons learned are captured with their cause (`REFERENCE.md:36-62`). The requirements table gives a fix for each item (`SKILL.md:15-26`).
- The expiry calculation is correct. Clamping at month ends works (30 Sep → 28 Feb; 31 Aug → 31 Jan), the year rolls over, the 14-day plan works, and the Cairo date is used (V-RUN).

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| F1 | **A spoofed or edited email can give free access.** The only selector is the subject. There is no `from:` filter and no check that the message came from the n8n sender or the expected Gmail account, and SPF/DKIM are not checked. Classification uses subject keywords plus fields in the body. Gmail ignores punctuation in `subject:` searches, so `[YMnotes]` matches any subject containing "YMnotes", including `Fwd:` and `Re:` copies. n8n also emails the *student* (`REFERENCE.md:76-77`), so students know the format exactly. | `SKILL.md:49,56-57`; `REFERENCE.md:76-77` | V-SRC (punctuation behaviour INF) | High |
| F2 | **MANUAL REVIEW is registered automatically.** The upstream meaning is "the payment proof needs a human", yet the skill registers the student and only flags it in the report. This contradicts the description's "paid students". | `SKILL.md:57,91,96`; `REFERENCE.md:77` | V-SRC | High |
| F3 | **A blank amount defaults to the larger plan.** Blank amount + Digestive gives `full` (5 months), and blank + Mid Questions gives `questions`. A truncated or tampered email therefore grants the most valuable plan. | `SKILL.md:61-62` | V-SRC | Med |
| F4 | **Payment authenticity is fully delegated** to the n8n "AI payment check". The skill never checks the amount against the price, the method, or a transaction reference. | `REFERENCE.md:75-77`; `SKILL.md:52-55` | V-SRC | Med |
| F5 | **Leftovers silently disappear.** Unclear and failed threads stay unlabeled but drop out of the `after:<now-25h>` window the next day, so nothing re-surfaces them. A missed daily run also loses that day's mail. | `SKILL.md:10-11,48-49,86` | V-SRC/INF | Med |
| F6 | **Fragile UI constants.** These include the fixed magnifier click (1170,125), the fixed menu fallback (630,519) on a menu that also contains Delete, `getByRole('button').last()` for the floating button, a fixed 1280×900 viewport, a 30-point RGB green threshold, and many fixed sleeps (14 s boot). The page check at `:131` and the lack of any confirm click limit the damage if Delete is hit. | `drive.js:28,43,124,128,140,161` | V-SRC | Med |
| F7 | **Repeated logins.** Every exception that leaves the Add Student page triggers a full new login, with no per-run cap. A flaky site with N students could mean N logins, which risks lockout or rate-limits even though each submit is "fresh". | `drive.js:230-239` | V-SRC | Low-Med |
| F8 | **No result does not count as failed.** A crash in the top-level catch exits 1 with no RESULT lines for the remaining students. SKILL.md lists the statuses but never says that a code with no RESULT line counts as failed. Exit code is also 0 even when every student failed. | `drive.js:243,250`; `SKILL.md:76-83` | V-SRC | Low-Med |
| F9 | **No run lock.** A manual run and the scheduled run at the same time could both see "New Student" and save. The site dedupe only helps sequentially. | `SKILL.md:43-44`; `drive.js:200-211` | INF | Low |
| F10 | **Date format is assumed.** Dates are built without zero padding (`2027/4/1`) and matched as literal strings in the date button and the verification. If the site pads, a successful save is reported as failed. It would self-heal the next day as "already". | `drive.js:207,209,217` | INF | Low |
| F11 | **Personal data in output and transcripts.** The report prints student names, which are kept in the scheduled-session transcript. The step runner prints full accessibility snapshots, which may hold student names and cities. A concrete-looking student code appears as the example at the two cited lines; it may be a real student (value not repeated here). | `SKILL.md:89-94,75`; `drive.js:87,261,277,280,284` | V-SRC/INF | Low |
| F12 | **Invalid YAML in the repo copy**, plus a duplicate synced copy loaded in the same session (see copy diff above). | `RS/SKILL.md:3`; `SYN/manifest.json:217-221` | V-RUN | Med |
| F13 | **`.mcp.json` is unpinned and auto-approved.** It runs `npx @playwright/mcp@latest` with `--no-sandbox`, and `enableAllProjectMcpServers: true` approves it automatically. That fetches unpinned code into every session, including scheduled ones, even though the skill says the MCP is not needed and cannot log in safely. | `REPO/.mcp.json:4-11`; `REPO/.claude/settings.json:2`; `SKILL.md:28`; `REFERENCE.md:38-39` | V-SRC | Med |
| F14 | **No tests.** There is nothing for classification rules, `expiry()`, or parsing of the RESULT lines. `--dry-run` needs the live site. | (no test files in `RS/`) | V-SRC | Low |
| F15 | **Undocumented `dry-run-ok` status.** It is not in the SKILL.md status list, and the label `Label_1` is hard-coded (with a fallback). | `drive.js:89,210`; `SKILL.md:78-85` | V-SRC | Low |
| F16 | **The hard rules have no technical enforcement.** The scheduled task's Gmail connector exposes send, trash and forward tools; only the prose rules stop them. Whether the scheduled task restricts its tools could not be checked offline. | `SKILL.md:36,22` | INF | Low |

**Recommendations:**
1. **Authenticate the email before acting** → F1, F4.
   - Add `from:<n8n sender address>` to the query.
   - In step 2, require the sender header to equal that address and the subject to start with `[YMnotes] ` (no `Re:` or `Fwd:`).
   - Better still, have n8n include an HMAC token of `code|plan|amount|date`, computed with a secret held in the environment, and verify it in `drive.js`.

   Draft: `query: from:<n8n-sender> subject:"[YMnotes]" after:<cutoff> -label:ymnotes-registered` and "If the From header is not exactly <n8n-sender> or the subject starts with Re:/Fwd: → unclear (suspected forgery)."

   Effort S for the filter, M for the HMAC.
2. **Stop auto-registering MANUAL REVIEW** → F2. Make MANUAL REVIEW → `unclear` and leave it unlabeled. Report it under "Needs payment check". If the owner wants speed, add an opt-in `allow_manual=true` parameter that is only valid in manual sessions. Fix the description to "Register students that n8n ACCEPTED…". Effort S.
3. **A blank amount → unclear** → F3. Change table rows 1-2 to "> 400 EGP" and "≤ 400 EGP" with no "or blank". Effort S.
4. **Make leftovers durable** → F5.
   - Add the label `ymnotes-needs-review` to unclear and failed threads.
   - Run a second query each day for that label older than the window, and list those threads in the report as "Still pending (n days)".
   - Alternatively, widen the window to 7 days. The site dedupe makes that safe.

   Effort S.
5. **Single source of truth** → F12.
   - Keep `RS/` as the master. Quote the description, copying the synced copy's line 3 verbatim.
   - Then either delete the plugin copy, or regenerate it from the repo on each merge and add a `version:` line to both so drift is visible.

   Effort S.
6. **Pin or remove the Playwright MCP** → F13. Either delete `.mcp.json` and `enableAllProjectMcpServers`, or pin the package (`@playwright/mcp@<exact version>`) and set `enabledMcpjsonServers: []` for scheduled runs. Effort S.
7. **Harden the driver** → F6, F7, F8.
   - Cap re-logins at 1 per run.
   - Print `RESULT {code, status:"failed", detail:"not attempted (driver aborted)"}` for each remaining student in the top-level catch.
   - Exit 4 if any result is `failed`.
   - Derive the magnifier position from the Student Code textbox box (right edge plus an offset) instead of (1170,125).
   - If the menu node box is not found, throw instead of falling back to (630,519).
   - Add to SKILL.md step 3: "A code with no RESULT line = failed."

   Effort M.
8. **Add an offline test** → F14. Move `PLANS`, `expiry` and the classification table into a pure module and test it with `node --test`. Cover month-end clamping, DST, and the amount and course matrix, including blank and spoofed cases. Effort M.
9. **Add a run lock** → F9. Have drive.js create an exclusive lock file (`fs.openSync(lock,'wx')`) in the OS temp directory, or label threads `ymnotes-processing` before calling drive.js. Effort S.
10. **Reduce personal data** → F11. Report codes only, or the first name only. Scrub snapshot output in step-runner mode to headings and buttons only. Replace the example code with `00000`. Effort S.

**Quick wins (<30 min):**
- Quote the description in `RS/SKILL.md:3` (copy the synced line).
- Add `from:` to the Gmail query and the rule "Re:/Fwd: → unclear".
- Change MANUAL REVIEW → unclear and blank amount → unclear.
- Add the line "No RESULT line = failed" and document `dry-run-ok`.
- Replace the example code `<example student code>` in `SKILL.md:75` and `drive.js:87`.
- Pin or remove `@playwright/mcp@latest`.

**Open questions:**
- Which exact sender address does n8n use for the admin emails? Does the student copy have the same subject?
- Does the owner *want* MANUAL REVIEW students registered before a human checks the payment proof (a deliberate speed trade-off)?
- Is the daily scheduled task configured with only Gmail (plus optional n8n)? Does it restrict Gmail write tools? (Not checked; read-only rule.)
- Does e-teaching.site zero-pad dates (`2027/04/01`)?
- Should the plugin copy exist at all, given that the drive.js allow rule only matches the repo path?

[↑ back to contents](#table-of-contents)

---

#### incision-block5-7-exams

**Identity:** no version field · synced plugin skill (`SYN/manifest.json:78-81`, `updatedAt` 2026-10-24T12:31Z), sourced from user-supplied ZIP and update notes dated 2026-10-24 (`IX/references/block5/index.md:3`) · 27 files, about 150 KB:
- SKILL.md: 9.3 KB, 1,198 words
- references: 12 general and policy files, plus 15 course files (7 for Block 5, 7 for Block 7, and a Block 5 index) totalling about 12.2k words
- `agents/openai.yaml` and an icon

Entry points: SKILL.md (model-invoked). `agents/openai.yaml:4,14` sets `allow_implicit_invocation: true` for ChatGPT, Codex, API and Atlas.

**Purpose & triggering:** The skill drives a browser logged into an Incision Academy **student account** and takes the graded course tests of the "October 6 University – Block 5/7 Program". It answers questions from an embedded answer bank plus course text, targets at least 80%, and caps attempts at two. It ends with a report keyed by student code and offers an Arabic WhatsApp "your exams are done" message. The description accurately says what it does ("Run requested … exams", "student-account course completion"). It is, however, broad on triggers: "chest drain, respiratory, cardiovascular, limb examination, anesthesia…" could fire on ordinary medical-study requests. Implicit invocation is on. It does not overlap with other YMnotes skills.

**How it actually works (trace):**
1. **Start-up:** model-preset reminder, then browser choice, then verifying the logged-in student code and program. If the block is not yet open, it enters a block activation code (`SKILL.md:17-23`; `programs.md:5-12`).
2. **Load the policy files:** attempts, answer policy and progress, plus the active course's answer table (`SKILL.md:23-29`).
3. **For each course:** check attempt history (`attempts.md:7-18`). Open the test, read each question, match it against the bank (`answer-policy.md:15-20`; e.g. `block7/examination-of-the-elbow.md` "Question candidates" table). If an answer is missing, check the course text or "reason independently" (`answer-policy.md:22-30`). Select, press Next, Finish, and record the score (`SKILL.md:31-38`; `recovery.md`).
4. **After the sweep:** produce the report and ask the operator's permission for a second attempt. Never take a third attempt (`SKILL.md:40-45`; `progress.md:42-65`).
5. **Optional extras:** a WhatsApp completion draft for the student (`whatsapp.md`), and "learning" that adds newly answered questions to the bank (`learning.md`).

**Account ownership and academic-integrity assessment (factual):**
- **Whose account:** students' accounts, not the user's own. The skill is built for **multiple students and operators**:
  - ledgers keyed "by verified student code" (`attempts.md:24`);
  - "Switching students … start a separate ledger for the new student" (`programs.md:21-25`);
  - "attempts by other operators" (`SKILL.md:13`) and "other agents may own adjacent tabs" (`browser.md:10-12`);
  - "use split view" for parallel runs (`SKILL.md:21`);
  - default prompt "for student [code]" (`openai.yaml:4`).
- **Exam-taking on behalf of students:** the WhatsApp draft is addressed *to the student*. It tells them their 7 exams are complete with at least 80%, asks them to check their Outlook for the certificates, and says "you can change your account password now for your privacy" (`whatsapp.md:22-44`, `:39`, `:65`). That implies the student handed over their login credentials so the operator could complete the exams for them.
- **Answer bank:**
  - Block 7 files hold about 165 question → answer rows (`block7/*.md`), and Block 5 has per-course answer traces (`block5/index.md:3,20-24`).
  - The `learning.md` loop grows the bank from runs (`learning.md:1-19`).
- **Attestation:** the Block 5 course 1 "attestation" test asks the account holder to confirm "I have studied and understood the course content and would like to receive a certificate" (`block5/course1-subcutaneous-infiltration.md:12-14`).
- **Conclusion:** yes. The skill **automates graded assessment and certification that are meant to be completed by the enrolled student personally**, for students other than the user. It is not a study aid.
- **Risks:**
  - Academic misconduct ("contract cheating") under typical university rules (O6U program, `programs.md:16-17`).
  - A probable breach of Incision's terms (account sharing, automated access, someone else taking the assessment). This is INF, since the terms were not read.
  - Credential sharing.
  - Certificates that misrepresent competence in **clinical procedures** such as chest drain insertion and defibrillator use. That is a patient-safety concern, not just a policy one.
- **Safeguards present:** all of them are operational and none addresses integrity:
  - no storing of credentials (`SKILL.md:15`) and no bypassing of access controls (`answer-policy.md:28`; `browser.md:20`);
  - an attempt cap and retake consent (`attempts.md`);
  - no sending of WhatsApp messages without a separate request (`whatsapp.md:3`);
  - no student identities in the bank (`learning.md:19`);
  - an attestation guard that requires the student's own confirmation (`course1…md:14`). This is the only integrity-aware line.

  There is no check that the account belongs to the operator, no check that the institution permits this, and no practice-only mode.

**Strengths to keep (for any re-purposed version):**
- A careful honesty discipline: it separates verified, unverified and unknown results, never inflates a pass (`progress.md:30-40`), and keeps evidence grades (✔ / ✔c / ? / ✗?) on content (`answer-policy.md:3-13`).
- Good privacy hygiene: no credentials, cookies or student identities go into reusable files (`progress.md:3`; `learning.md:19`).
- The course-text summaries (e.g. the elbow "Supplied course notes") would be valid **study material** in a tutoring mode.
- It prefers DOM and text reads over screenshots and coordinates (`browser.md:14-18`). That makes it less fragile than canvas automation.

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| I1 | **It automates graded exams and certification in other students' accounts.** The design is multi-student and multi-operator, and the completion message is sent to the student. | `SKILL.md:3,13,19,22,44`; `programs.md:21-25`; `browser.md:10-12`; `whatsapp.md:22-44`; `openai.yaml:4` | V-SRC | High |
| I2 | **Credential sharing is implied.** The student is told to change their password after the run. | `whatsapp.md:39,65` | V-SRC | High |
| I3 | **An embedded answer bank grows with each run.** About 165 Block 7 Q→A rows plus the Block 5 traces. | `block7/*.md` (Question candidates tables); `block5/index.md:3,20`; `learning.md:1-19` | V-SRC | High |
| I4 | **A false attestation is possible** ("I have studied and understood…") on the student's behalf. Only a prose guard prevents it. | `block5/course1-subcutaneous-infiltration.md:12-14` | V-SRC | High |
| I5 | **Probable breach of the platform's terms and the institution's rules.** The skill uses university program activation codes, gets certificates issued, and mentions no check of what is permitted. | `programs.md:5-17`; `whatsapp.md:37,63` | INF | High |
| I6 | **Block activation codes are stored in plain text** (access tokens; values not repeated here). | `SKILL.md:22`; `programs.md:7,8,10`; `block5/index.md:6` | V-SRC | Med |
| I7 | **Implicit invocation is on, and the triggers are broad clinical topics.** It could fire on innocent study requests. | `SKILL.md:3`; `openai.yaml:14` | V-SRC | Med |
| I8 | **Personal-data handling.** Student codes, scores and login handoffs are kept in host checkpoints and transcripts. The skill relies on the host for privacy. | `progress.md:3-20`; `SKILL.md:19,22` | V-SRC | Med |
| I9 | **Context cost.** About 1.6k tokens for SKILL.md, plus about 3.7k for three always-loaded policy files, plus about 1.5k per course. The text is heavily negation-based (20 "never/do not" in SKILL.md and 87 in the references), against the rubric's "prompt the positive". | `SKILL.md` (whole); `references/*` | V-RUN (counts) | Low |
| I10 | **Unverifiable claims.** Model presets ("GPT 6 Luna", "GPT 6.1 Sol"), the Block 7 code is marked not live-tested, and the legacy ✔ marks "lack retained proof". | `SKILL.md:20,22`; `answer-policy.md:7`; `programs.md:8` | V-SRC | Low |
| I11 | **No tests or scripts.** The behaviour is unverifiable offline. | (no scripts in `IX/`) | V-SRC | Low |

**Recommendations** (deliberately not about exam effectiveness):
1. **Retire the exam-taking workflow** → I1-I5. Disable the skill now: remove it from the synced plugin, or at minimum set `allow_implicit_invocation: false` and `disable-model-invocation: true`. Stop using student credentials, delete `whatsapp.md`, and delete the stored activation codes. Effort S.
2. **If a replacement is wanted, rebuild it as a tutoring and practice skill** → I1, I3, I4. Name it something like `incision-block5-7-study`. It runs with **no browser and no account access**. It teaches from the course notes, quizzes the student with explanations, and the student takes the real test themselves.

   Draft description: "Tutor a student for Incision Academy Block 5/7 courses (chest drain, respiratory/CV/limb examination, local anaesthesia, postoperative care, Efficia/FT10/RapidVac) using course-note summaries and self-quiz questions with explanations. Never logs in to Incision or answers a live/graded test; the student takes assessments personally."

   Keep the "Supplied course notes" sections and evidence grades as teaching content. Drop the "Question candidates" answer tables that are keyed to live tests, or turn them into explained practice items not formatted for answer-matching. Remove `attempts.md`, `recovery.md`, `browser.md` and `programs.md`. Effort M.
3. **If the owner believes some use is legitimate** (e.g. their own account), verify Incision's terms and the O6U academic-integrity policy first. Restrict the skill to the owner's own account, and add a hard stop: "If the signed-in account is not the user's own, stop." The attestation must always be made by the person themselves. Effort S (gate) + owner research.
4. **Personal data cleanup** → I6, I8. Purge student codes and results from any checkpoints or transcripts the owner controls, and stop collecting other people's credentials. Effort S.
5. **If anything is kept, cut the context cost and rewrite the rules positively** → I9. Effort M.

**Quick wins (<30 min):**
- Set `allow_implicit_invocation: false` (`openai.yaml:14`) and add `disable-model-invocation: true` to the frontmatter, or remove the skill from the plugin.
- Delete `references/whatsapp.md` and the activation-code lines (`SKILL.md:22`, `programs.md:7-10`, `block5/index.md:6`).
- Stop the practice of receiving student passwords. Tell affected students to change theirs.

**Open questions:**
- Are the accounts the owner's own (one student, self-study) or customers' accounts? The evidence above says customers', and possibly a paid service. The owner should confirm.
- Does Incision Academy or O6U permit any third-party or automated completion? Neither the skill nor this review checked.
- Where are the run checkpoints with student codes and scores stored? Who can see them?
- Is there a related payment flow (similar to YMnotes registration) for this service? If so, it carries the same integrity issue.

[↑ back to contents](#table-of-contents)

---


### E. Developer tools

#### codex-delegate
**Identity:** 0.6.1-ymnotes · MIT, derived from amElnagdy/delegate-skills `codex-delegate` v0.5.0 (README.md:233-236) · 11 files, about 141 KB (relay.mjs 46 KB, doctor.mjs 21 KB, SKILL.md 13.5 KB, 6 references) · manifest updatedAt 2026-10-28 · entry points: SKILL.md (model-invoked, "use proactively"), `scripts/doctor.mjs` (check / plan / install / login / verify), `scripts/relay.mjs` (dispatch)

**Purpose & triggering:** Makes Claude the coordinator and the Codex CLI the implementer: write a brief, dispatch it via `relay.mjs`, verify the route from Codex's session log, re-run gates, and integrate. Parallel writers go in git worktrees. The description (195 chars) is compact, but it spends words on internal jargon ("Terra High default, Sol when warranted"). "Use proactively" makes it fire on almost any substantial coding task, which overlaps with Claude's own coding and with the official `/codex:rescue` plugin. The body handles that boundary (SKILL.md:181-188), but the description does not.

**Model names, checked:** "Terra" / "Sol" / "Astra" **are not nonsensical**. Web sources (third-party, not OpenAI's own docs) report `gpt-6.1-terra` (released about 2026-10-26), `gpt-6.1-sol`, and `gpt-6-astra` as Codex CLI model IDs, plus `gpt-6-luna`. The same sources position **Sol as the complex-coding model**, and Terra as cheaper and faster, aimed at writing, visual understanding and computer use. So the default route "Terra for normal coding" is a cost choice, not an obvious quality choice. One source also says Terra needs **Codex CLI ≥ 0.159.0**. npm `@openai/codex` latest is 0.166.0.

**Upstream currency:** The upstream's latest tag is **v0.5.0 (2026-08-16)**, which is the base this fork names. There are no GitHub Releases and I could not load the commit history (repo API access is blocked in this session), so post-tag changes on `main` are unverified. Upstream has since grown into an 18-implementer suite with `delegate-setup` / `lane.mjs` (which this fork's `--lane` still references).

**How it actually works:** SKILL.md:29-60 runs `doctor.mjs check` → `runChecks()` (doctor.mjs:147-192) probes node/git/npm/codex/`codex exec --help`/`codex login status`, reads `~/.codex/models_cache.json` (slugs only, :97-108) and the top-level `model` in config.toml (:110-119), and checks the plugin via `claude plugin list --json` (:131-145). It writes a READY cache in the OS temp dir (:269-273). Dispatch: `relay.mjs` parseArgs (:218-340) → applyRoute pins `-m` and `-c model_reasoning_effort` and blocks /astra/i (:159-174) → prepareRunDir snapshots `git status --porcelain` as baseline (:610-630) → spawn `codex exec --json -o final.txt -s workspace-write -m … -` with the brief on stdin (:557-587, :749-901) → watchdog/abort handlers → writeResult computes `newChanges` and `routeVerified` from the rollout `turn_context` records (:503-550, :632-678).

**Security posture:**
- **Sandbox:** default `workspace-write` (relay.mjs:234). `danger-full-access` is accepted with no guard or approval prompt (:133, :287), and SKILL.md never tells Claude when it is allowed.
- **Approvals:** no `-a/--ask-for-approval` is passed. This relies on `codex exec`'s non-interactive behaviour (no approval prompts), so the sandbox is the only boundary.
- **Network:** off by default. `--network-access` opts in and is correctly refused with read-only (:292-299). Web search (hosted) works even read-only (header :57-61). It is not disabled by default, so an "offline" run can still search.
- **Secrets:** briefs must not contain values (SKILL.md:194). `--clean-env` exists but is not the default, so Codex inherits the full environment, including any tokens in env vars.
- **Worktrees:** the junction trick shares the main tree's `node_modules` into each worktree (parallel-and-routing.md:46). A workspace-write Codex in the worktree can then write into the **main** `node_modules`, and that breaks "disjoint file sets". `git worktree remove --force` (:79) discards untracked files. This is mitigated by "only after patch applied".
- **Global installs:** `npm install -g @openai/codex` only after the user approves, with `--yes`, and only on a local host (doctor.mjs:275-292). Good.

**Strengths to keep:**
- Explicit routing on every run, with a read-back of the model actually used from Codex's session rollout (`routeVerified`, `astraUsed`). Mismatches are surfaced, not hidden.
- Doctor design: read-only `check`, `plan` before `install`, `--yes` gating, refusal off-host, a mock mode for testing, and no credential reading (only slugs from models_cache).
- The relay is robust: atomic result.json, a watchdog, abort-on-signal still writes a result, Windows `.cmd` shim and WindowsApps PATH handling, shell-safe token validation for everything that reaches cmd.exe (:134-141, :300-338).
- The review discipline in review-and-land.md (check test edits first; passing is necessary but not sufficient).
- Clear coexistence rules with the official plugin.

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | Once `models_cache.json` exists and lacks exactly `gpt-6.1-terra`+`high`, doctor reports **NEEDS-SETUP forever**, with an empty "models BLOCKED" line and no list of the models that *are* available. When the model is renamed or retired, the whole skill stops. | doctor.mjs:175-182, :213-215, :233; ran mock with `gpt-5.5-codex` cache → exit 1, "models BLOCKED" with no detail | V-RUN | High |
| 2 | Model IDs are hardcoded in 3 places (relay ROUTES, doctor POLICY, SKILL/README/setup/dispatch text) with no single source of truth. The dispatch reference also claims effort levels "`max`, `ultra` for the GPT-6.1 models in this account", which is account-specific and goes stale. | relay.mjs:147-152; doctor.mjs:31-36; SKILL.md:88-93; references/dispatch-and-poll.md:40 | V-SRC | Med |
| 3 | Routing premise may be inverted: public sources position Sol (not Terra) for complex coding and Terra for writing/vision/computer use. Defaulting all coding to Terra is a cost decision, and the skill doesn't say so. | SKILL.md:72,90; web sources | INF | Med |
| 4 | No minimum Codex CLI version check. Doctor only checks for the flags `--json`/`--output-last-message`/`resume`, but Terra reportedly needs ≥0.159.0. An older CLI passes doctor and then fails at dispatch. | doctor.mjs:155-156,170 | V-SRC + INF | Med |
| 5 | `newChanges` misses edits to files that were already dirty. It compares porcelain lines, so a file showing ` M foo` before and after (Codex edited it further) is not reported. SKILL.md:128-129 calls it "edits made by this run". | relay.mjs:650-652 | V-SRC | Med |
| 6 | The READY cache (12 h) is invalidated only by a change in Codex version. A logout, plan change, or loss of model access within 12 h still reports READY. The cache path is a fixed name in the shared temp dir (`codex-delegate-readiness.json`), so on a multi-user Linux host another user could plant it. | doctor.mjs:29-30, :256-267 | V-SRC | Low |
| 7 | `danger-full-access` is accepted with no policy in SKILL.md, the default environment is not clean, and web search is not disabled by default. Together these leave the sandbox posture entirely up to the model. | relay.mjs:133,234,416-419; SKILL.md:116-125 | V-SRC | Med |
| 8 | The worktree `node_modules` junction lets parallel writers mutate the shared main-tree `node_modules`, which defeats the isolation that parallel-and-routing.md promises. | references/parallel-and-routing.md:41-47 | INF | Med |
| 9 | Dead upstream feature: `--lane` requires `../../delegate-setup/scripts/lane.mjs`, which is not shipped. It is documented in the relay header and dispatch reference. | relay.mjs:29,176-181; dispatch-and-poll.md:37 | V-SRC | Low |
| 10 | `verify` crashes with a TypeError if the dry-run argv lacks `-m … -c model_reasoning_effort=…` (`.match()` returns null and then `.slice` is called). | doctor.mjs:355 | V-SRC | Low |
| 11 | Host detection: any host that isn't local Claude Code (e.g., the user's own terminal, or Codex/Cursor running the skill) with a blocking item becomes "unsupported" (exit 3), not "needs-setup", so a plain `node doctor.mjs check` from PowerShell sends the user the wrong signal. | doctor.mjs:87-91, :190 | V-SRC | Low |
| 12 | `checkPlugin` depends on `claude plugin list --json`. If that flag does not exist in the user's Claude Code version, it silently reports "unknown". This is acceptable, but the plugin install path then always blocks. | doctor.mjs:136-143, :298-301 | INF | Low |
| 13 | The description has a "use proactively" trigger with no cost cue. On a ChatGPT plan this can burn Codex quota on work Claude would do inline. The body's "do it inline" rules (:75) are not reflected in the description. | SKILL.md:3,20 | INF | Low |
| 14 | No automated tests ship with the skill, though `--mock` exists for them. Upstream's tests were not carried over. | scripts/doctor.mjs:13 | V-SRC | Low |
| 15 | Licence compliance is fine: the MIT notice is preserved and the derivation is stated. | LICENSE; README.md:231-236 | V-SRC | — |

Run evidence (copies only): `relay.mjs --dry-run` produced the expected argv; `--model gpt-6-astra` → exit 2 "Astra model" refusal; `--network-access --read-only` → exit 2; a real `doctor.mjs check --json` on this cloud host → `unsupported`, exit 3 (correct, since Codex is not installed).

**Recommendations:**
1. Make the model policy data, not code, and degrade gracefully → (#1, #2, #4) create `scripts/routes.json` `{ "terra": {"model":"gpt-6.1-terra","effort":"high"}, …, "minCodex":"0.159.0" }`, imported by both scripts. In doctor, when the default model is missing, list the available slugs and print `"set routes.json terra.model to one of: …, then re-run"`. Add `atLeast(codexVersion, POLICY.minCodex)` to the codexCli status. → M
2. Fix `newChanges` → (#5) pseudocode: before dispatch, record `git hash-object` for each dirty path (or `git stash create` → baseline tree SHA). After the run, report a path as changed if it is not in the baseline **or** its hash differs. Minimal version: `newChanges = touched.filter(l => !baseline.includes(l) || hashBefore[path(l)] !== hashNow(path(l)))`. → M
3. State a sandbox policy in SKILL.md §8 → (#7) draft: "Default `workspace-write`, offline. Use `--network-access` only for dependency installs or `gh`. Never pass `--sandbox danger-full-access` unless the user says so in this task. Pass `--web-search disabled` unless the brief needs docs. Use `--clean-env` when the repo's shell has tokens in its environment (n8n, Supabase, YouTube API keys)." Optionally make the relay refuse `danger-full-access` without `--allow-full-access`. → S
4. Re-examine the default route → (#3) decide deliberately: either `sol-medium` default with Terra for bounded scripts, or keep Terra and write the reason ("cost: Terra about half of Sol") into SKILL.md:72. → S
5. Replace the `node_modules` junction → (#8) for parallel writers, run `npm.cmd ci --prefer-offline` in each worktree as a pre-step (outside Codex), or brief the task as "do not modify node_modules" and check `git -C "$REPO" status node_modules` after the run. → S
6. Harden the cache → (#6) include `login` and `models` in the cache key (re-run `codex login status`, which is cheap). Put the cache under `os.homedir()/.cache/codex-delegate/` rather than shared tmp. → S
7. Remove the `--lane` code and docs, or ship lane.mjs → (#9). → S
8. Guard `verify` parsing → (#10) `const m = …match(...); routes[route] = m ? m.slice(1).join("/") : "error: unexpected argv"`. → S
9. Add `tests/doctor.mock.test.mjs` → (#14) cover ready, models-missing, api-key-blocked, cloud-unsupported and old-CLI using `--mock` (`node --test`). → M
10. Description → (#13) draft: `Delegate substantial, well-defined coding (features, refactors, test suites, scripts, debugging passes) to the OpenAI Codex CLI and verify the result; parallel worktrees; first-run setup/doctor. Use when asked to use Codex or delegate, or proactively for multi-file work worth more than writing a brief. Not for quick edits or code review.` → S

**Quick wins (<30 min):** null-guard in verify (#10); print the available model slugs when BLOCKED (#1, part); sandbox policy paragraph (#3); delete `--lane` docs (#9); add the reason for the Terra default (#4).

**Open questions:**
- Has `verify --live` ever been run on the Windows machine, and did `routeVerified` come back `true` with the real `turn_context` field names (`payload.model`/`payload.effort`)? This is unverifiable offline.
- Did upstream `main` change after v0.5.0 (relay fixes)? Diffing needs repo access, which was blocked in this session.
- Is the user's ChatGPT plan one where Terra is rolled out? Sources say the rollout is staged by plan.

[↑ back to contents](#table-of-contents)

---

#### graphify
**Identity:** SKILL "1.0.0" per CHANGELOG (2026-09-07) · unified derivative of Graphify-Labs/graphify (`v8` @ c9f9901877, Apache-2.0 + MIT), nyldn/skills (MIT), matt-riley/agent-skills (**GPL-3.0**) · 26 files, about 215 KB (build-workflow.md 30 KB, query.md 13 KB, 2 Python scripts 39 KB, 5 licence files 49 KB) · manifest updatedAt 2026-09-09 · entry points: SKILL.md (model-invoked; openai.yaml `allow_implicit_invocation: true`), `scripts/graphify_doctor.py`, `scripts/graphify_query_local.py`, `tests/test_graphify_skill.py`

**Purpose & triggering:** A "control plane" that makes agents consult a Graphify knowledge graph (`graphify-out/GRAPH_REPORT.md`, `graph.json`) before scanning files, then confirm in source files, and refresh the graph only when structure changes. It covers build, update, export, hooks, transcription and multi-repo merge through 12 references. The description is accurate, but it ends with a negation block ("Do NOT use for…"). It also triggers on "exploring unfamiliar repositories" even where no graph exists, which overlaps with Claude Code's own Explore behaviour. No other skill in the set overlaps. Upstream now ships its own official Claude skill (`graphify install` / `graphify claude install`), so having both installed would duplicate it.

**How it actually works:** SKILL.md §3 (:60-112): read durable state → locate `graphify-out/` → freshness via `needs_update` / `graphify check-update` / `python scripts/graphify_doctor.py . [--check]` → GRAPH_REPORT.md → queries via the local helper or the `graphify` CLI → open 1–3 files with "`view_file`" → act → `graphify update .` only when justified. Routing table :116-131 → references. Doctor (511 lines): subprocess probes of the graphify CLI and package version, graph.json metadata, git HEAD, `needs_update`, `.graphifyignore`, ~/.codex/config.toml `multi_agent`, and a project-wide `rglob` for Google-native files; `--check` exits 0 only if graph.json and the report exist and `needs_update` is absent (graphify_doctor.py:498-505). Query helper: a zero-dependency BFS/path/explain over `nodes` + `links|edges`.

**Upstream / version currency:** The skill pins "graphifyy v0.9.55+" (CHANGELOG; SOURCE.md:15). **PyPI `graphifyy` is now 0.9.100**, licence expression Apache-2.0 with LICENSE, LICENSE-MIT and NOTICE. That is 45 patch releases since the snapshot. Upstream still uses the `v8` branch, has no GitHub Releases, and now installs its own skill. The doctor already parses the CLI's "skill is from graphify X, package is Y" warning (:296-302), which is good.

**Licence compliance:** The Apache-2.0 LICENSE + NOTICE and MIT texts are preserved (licenses/). However, the skill **declares GPL-3.0-derived content** (SOURCE.md:31-34; provenance.md:36: negative gating text, openai.yaml conventions, build-workflow separation) and ships the GPL text, **yet the skill has no overall licence statement**. If the GPL-derived parts are copyrightable expression, redistributing the combined skill requires GPL-3.0 for the whole (Apache-2.0 and MIT are GPL-3-compatible, one-way). Personal use is unaffected. Sharing or publishing the skill (e.g., to students, or a public repo) is the trigger.

**Are the routing tests real?** **No.** ROUTING_TESTS.md is a hand-written table of 10 prompts with "Actual Routing Decision" and "PASS" filled in. There is no harness, no transcript, no model or date, and it cannot be re-run. The Python tests are real and pass (13/13, V-RUN), but they test the scripts and the frontmatter, **not** routing or the commands that SKILL.md documents.

**Strengths to keep:**
- Correct epistemic boundary: the graph says *where* to look and source files say *what is true*. It explicitly includes medical facts and config values (:34-37).
- A freshness decision matrix that avoids reflexive rebuilds (:135-145).
- A zero-dependency local query helper with sensible JSON output, plus a read-only doctor. Both work (V-RUN).
- Provenance recorded with commit SHAs. Licence texts preserved.
- Response standard: cite the graph source, its freshness, and the confirming file:line (:149-155).

**Findings:**

| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | **Documented local-query commands are broken.** SKILL.md uses `python scripts/graphify_query_local.py . stats`, but the CLI takes the action first and the project via `-p`. Running it as documented → `error: argument action: invalid choice: '.'`. All 5 examples are affected, plus the routing table row. | SKILL.md:92-96, :122; graphify_query_local.py argparse (`-p PROJECT`, action positional) | V-RUN | High |
| 2 | Script paths are relative to the skill (`python scripts/graphify_doctor.py .`) but are run from the project root, so they fail unless the agent substitutes the skill directory. | SKILL.md:80-82, :92-96, :126, :144 | V-SRC | Med |
| 3 | Tool names come from another agent (Antigravity/Gemini): `view_file`, `grep_search`, `list_dir`, `replace_file_content`. Claude's tools are Read/Grep/Glob/Edit. | SKILL.md:106; references/navigation.md:27,33,36,65,92; ROUTING_TESTS.md:34 | V-SRC | Med |
| 4 | ROUTING_TESTS.md presents unexecuted, self-graded results as "100% precision". That is an overstated claim. | ROUTING_TESTS.md:28-46 | V-SRC | Med |
| 5 | GPL-3.0-derived content with no top-level licence for the combined work. It is a distribution risk only. | SOURCE.md:31-34; references/provenance.md:36; licenses/matt-riley-LICENSE | V-SRC | Med (if shared) / Low (private) |
| 6 | Version stale: written for graphifyy 0.9.55+, current 0.9.100. Commands and flags in the references (e.g., `graphify claude install`, `check-update`, `extract`) are unverified against current. | SOURCE.md:15; CHANGELOG.md:16; PyPI | V-SRC + web | Med |
| 7 | False claim: "graphify_doctor.py copied verbatim without modification". The doctor references the fork-added `graphify_query_local.py` (local_query_helper_exists), so it was modified. | SOURCE.md:41 (provenance §2.4); graphify_doctor.py:314,355,410,445 | V-SRC | Low |
| 8 | Missing referenced artefacts: `.graphify_version` (CHANGELOG.md:21; provenance.md:36) and `references/research-notes.md` / `default-build-workflow.md` (SOURCE.md:26,34) are not in the skill. | file listing | V-SRC | Low |
| 9 | Hardcoded Windows paths from the author's build machine (`D:\Github3863\…`, `file:///D:/…`, `C:\Users\hp\.gemini\…`). | README.md:6; CHANGELOG.md:13-29; references/platform-notes.md:109 | V-SRC | Low |
| 10 | build-workflow Step 1 auto-installs `graphifyy` with no user confirmation, including `pip install … --break-system-packages` into system Python. That conflicts with the "ask before installing" norm in the user's other skills. | references/build-workflow.md:83-91 | V-SRC | Med |
| 11 | An over-absolute rule, "never run broad recursive grep … when a valid Graphify graph exists" (in shouty `[!CRITICAL]` form). It can block legitimate exact-string searches (error messages, config keys) that a graph cannot answer. | SKILL.md:38; navigation.md:27 | INF | Low |
| 12 | Context cost: the SKILL.md body is about 10.5 KB. The README duplicates SKILL.md content (README is never loaded, but it is duplicated maintenance). build-workflow.md is 30 KB / 558 lines when loaded. | wc output | V-SRC | Low |
| 13 | The doctor's `google_pointer_summary` does an unbounded `rglob("*")` over the project on every run, which is slow on big repos and media archives. It also reads `~/.codex/config.toml` (only for a `multi_agent` flag; nothing is leaked). | graphify_doctor.py:240-258, :262-271 | V-SRC | Low |
| 14 | The tests pass but would not catch #1: `TestGraphifyQueryLocal` calls the correct syntax (`action … -p dir`), not the SKILL.md syntax. | tests/test_graphify_skill.py:157 | V-RUN | Med |

**Recommendations:**
1. Fix the documented commands and anchor them to the skill directory → (#1, #2, #14) replace SKILL.md:80-96 with:
   ```bash
   python "<skill-dir>/scripts/graphify_doctor.py" .            # add --check for exit 0/1
   python "<skill-dir>/scripts/graphify_query_local.py" stats -p .
   python "<skill-dir>/scripts/graphify_query_local.py" query "authentication billing" -p .
   python "<skill-dir>/scripts/graphify_query_local.py" path AuthMiddleware StripeWebhook -p .
   python "<skill-dir>/scripts/graphify_query_local.py" explain DatabasePool -p .
   python "<skill-dir>/scripts/graphify_query_local.py" find BillingRouter -p .
   ```
   Then add a test that extracts every `graphify_query_local.py` line from SKILL.md and runs it against the synthetic graph. → S
2. Translate the tool names to Claude → (#3) `view_file` → Read, `grep_search` → Grep, `list_dir` → Glob, `replace_file_content` → Edit, in SKILL.md, navigation.md and ROUTING_TESTS.md. → S
3. Resolve the licence → (#5) either (a) rewrite the GPL-derived lines independently (the "Do NOT use" gating text and openai.yaml are short and easy to rewrite), remove matt-riley from SOURCE.md and licenses/, and declare `license: Apache-2.0 (see licenses/)`; or (b) add `license: GPL-3.0-or-later (combined work; see licenses/)` to the frontmatter. Option (a) is simpler if the skill may be shared. → S
4. Re-baseline against graphifyy 0.9.100 → (#6) run `graphify --help` and the subcommand helps on the user's machine, diff them against query.md/update.md/hooks.md/exports.md, and update `SOURCE.md` with the new commit and date. Consider whether upstream's official skill (`graphify claude install`) should replace most references, with this skill keeping only the control-plane policy. → M
5. Make the routing tests real, or relabel them → (#4) rename ROUTING_TESTS.md to "routing intent spec (not executed)", or run each prompt in a fresh Claude session with the skill installed and record the model, date and whether the skill loaded. → S/M
6. Gate installs → (#10) replace the build-workflow.md:83-91 auto-install with: "If graphify is missing, show `uv tool install graphifyy` (or `pipx install graphifyy`) and ask the user; never use `--break-system-packages`." → S
7. Soften the grep rule → (#11) "Prefer graph queries for structure; use Grep for exact strings (errors, keys, literals) the graph does not index." → S
8. Clean up provenance and paths → (#7, #8, #9) correct the "verbatim" claim, drop the missing-file references, and strip the `D:\` / `file:///` / `C:\Users\hp` paths. → S
9. Bound the doctor scan → (#13) skip `google_pointer_summary` unless a `--google` flag is passed, or cap the rglob at N files. → S

**Quick wins (<30 min):** fix the 6 command lines (#1/#2); rename the tool names (#3); relabel ROUTING_TESTS.md (#4); remove the hardcoded paths and the "verbatim" claim (#7, #9); add the install-confirmation sentence (#10).

**Open questions:**
- Is graphify actually installed on the Windows machine, and which version? That decides whether references need a re-baseline or a rewrite.
- Will this skill ever be shared (students, a GitHub repo)? That decides the urgency of the GPL question.
- Keep this unified skill, or switch to upstream's official skill plus a short local policy addendum?

[↑ back to contents](#table-of-contents)

---


### F. Community workflow skills (from mattpocock/skills, unmodified)

#### grill-me
**Identity:** no version field (upstream plugin v1.3.2) · `mattpocock/skills` `skills/productivity/grill-me` · 2 files / 294 B · synced 2026-10-30T23:15:54Z (manifest) · entry point: user types `/grill-me` (`disable-model-invocation: true`)

**Purpose & triggering:** A one-line shim that hands off to the model-invoked `grilling` skill, which runs a "relentless interview" in rounds over a design tree. Upstream deliberately splits it in two: a user-facing slash command, plus a model-invoked body other skills can reach. The human-facing description is fine. **Verdict: broken as installed**, because its only target is missing. It has no overlap with other installed skills.

**How it actually works:** `<S>/grill-me/SKILL.md:4` sets user-invoked → `:7` "Call the Skill tool with "grilling"" → the Skill tool finds no `grilling` (there is no `<S>/grilling/`, and it is absent from `manifest.json`'s 40 names) → the agent improvises or reports failure.

**Strengths to keep:**
- Correct upstream pattern: a thin user-invoked alias over a model-invoked body (matches `writing-for-agents/SKILL-MECHANICS.md:9-12`).
- Upstream `grilling` (round-based frontier questions, "yes accepts the recommendation", sub-agent fact finding) is high quality and fits planning n8n and runner changes.

**Findings:**
| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | Target skill `grilling` is not installed. Nothing named `grilling` exists in the synced folder or in `manifest.json`, so `/grill-me` does nothing useful. | `<S>/grill-me/SKILL.md:7`; `grep -ril grilling <S>` hits only that file; manifest names list | V-SRC | High |
| 2 | Cause: the skills were cherry-picked one per plugin rather than installed as the `mattpocock-skills` plugin, whose `plugin.json` lists `grilling` next to `grill-me`. | upstream `.claude-plugin/plugin.json` (skills list); distinct `backingPluginId` per skill in `manifest.json` | V-SRC | Med |
| 3 | grill-me does not appear in the session's skill listing (expected, because it is user-invoked), so the user must remember it by name. | session skill list; `SKILL.md:4` | V-RUN | Low |

**Recommendations:**
1. **Install `grilling`** → fixes #1/#2. Upload upstream `skills/productivity/grilling/SKILL.md` (30 lines, description of about 170 chars, roughly 45 tokens of always-loaded context) as its own skill named exactly `grilling`. Keep its frontmatter: `name: grilling`, `description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.` → **S**.
2. **Alternative if you want zero context load**: inline the body into grill-me and delete the indirection, i.e. replace `SKILL.md:7` with the full upstream `grilling` body (lines 6–30). Downside: no other skill (e.g. `teach`, a future planning skill) can reach it, and you diverge from upstream → **S**.
3. Optional: add `argument-hint: "What plan or decision should I grill you on?"` so the prompt shows in the slash menu → **S**.

**Quick wins (<30 min):** Recommendation 1. Then test it by typing `/grill-me plan the YMnotes Shorts schedule`.

**Open questions:**
- Did you mean to install the whole `mattpocock-skills` plugin? Installing it would also bring `grilling`, `to-questionnaire` and `wait-what`, but the engineering skills assume a GitHub issue tracker and `CODING_STANDARDS.md`.

[↑ back to contents](#table-of-contents)

---

#### handoff
**Identity:** no version field (upstream v1.3.2; temp-dir wording from upstream PR #1184, 2026-10-06) · `mattpocock/skills` `skills/productivity/handoff` · 2 files / 1.1 KB · synced 2026-10-30T23:16:18Z · entry point: `/handoff [focus of next session]`

**Purpose & triggering:** Compacts the current conversation into a handoff document for a fresh agent: it references existing artifacts rather than copying them, redacts secrets and PII, and lists the skills the next agent should load. It is user-invoked and the description is human-facing, which is appropriate. There is light overlap with Claude Code's built-in `/compact`. Handoff differs because it produces a portable file.

**How it actually works:** `SKILL.md:4` gives the argument hint → `:8` writes to `$TMPDIR` / `/tmp` / `%TEMP%`, explicitly not the workspace → `:10` adds a suggested-skills section → `:12` references specs/commits/URLs instead of duplicating them → `:14` redacts → `:16` tailors the document to the argument.

**Strengths to keep:**
- Short (about 230 tokens), with clear rules about duplication and redaction.
- The argument hint makes the next session's focus explicit.
- The OS temp-dir rule is now spelled out (upstream fix for issue #272).

**Findings:**
| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | In claude.ai cloud / Claude Code Remote sessions, `/tmp` lives in an ephemeral container that is released on archive. A "fresh agent" in another session cannot read the file, so the handoff is lost unless it is also echoed or published. | `SKILL.md:8` | INF | Med |
| 2 | No step tells the agent to **print the saved path** (or the content) at the end. Without it the user cannot find a file under macOS `$TMPDIR` (`/var/folders/…/T/`). | `SKILL.md:8` (no output step) | V-SRC | Med |
| 3 | On Windows, Claude Code runs Bash (Git Bash), where `%TEMP%` is not expanded. The variable there is `$TEMP` or `$TMP`, and `$TMPDIR` is usually unset, so the agent may fall back to `/tmp`, which maps to a Git-Bash-private directory. | `SKILL.md:8` | INF | Low |
| 4 | No filename convention, so repeated handoffs collide or are hard to find. | `SKILL.md:8` | V-SRC | Low |
| 5 | Redaction covers "PII". For YMnotes, that should explicitly include student names, emails and phone numbers from registration work. | `SKILL.md:14` | INF | Low |

**Recommendations:**
1. Add an output and location rule → #1, #2, #4. Draft to append after `:8`:
   > Name it `handoff-YYYYMMDD-HHMM-<slug>.md`. When the session's system prompt lists a scratchpad directory, save there instead. In a cloud or remote session, also paste the full document in your final reply. Always end by printing the absolute path.

   → **S**.
2. Windows clarity → #3: change `%TEMP%` to "`%TEMP%` on Windows (`$TEMP` in Git Bash)" → **S**.
3. Optional YMnotes redaction line → #5: "Redact student names, emails, phone numbers and e-teaching.site account data." → **S**.

Note: editing these locally diverges from upstream. Consider proposing #1/#2 upstream instead (issue on `mattpocock/skills`).

**Quick wins (<30 min):** Recommendations 1 and 2.

**Open questions:**
- Do you mainly run handoffs on your Windows/macOS machine or in claude.ai cloud sessions? The answer decides whether "paste in reply" should be the default.

[↑ back to contents](#table-of-contents)

---

#### retro
**Identity:** no version field (upstream v1.3.2) · `mattpocock/skills` `skills/engineering/retro` · 2 files / 4.5 KB · synced 2026-10-30T23:16:36Z · entry point: `/retro` (user-invoked; no argument hint although it accepts a session reference)

**Purpose & triggering:** A retrospective on a coding session that proposes improvements to the agent's *environment* in seven categories: navigation, automated checks, coding standards, AGENTS.md, tool economy, no-ops and information access. Results are ranked by severity. It is user-invoked with a human-facing description, which is appropriate. It depends on `writing-for-agents`, which is installed and model-invoked, so that call works. It is the natural companion for after a failed YMnotes runner or n8n session.

**How it actually works:** `SKILL.md:11` calls Skill `writing-for-agents` (resolvable; see `writing-for-agents/SKILL.md:1-4`, no `disable-model-invocation`) → `:13` reads session logs, defaulting to the current session → `:15-23` checks the seven categories → `:25` presents them by severity. Reference section `:29-44` covers the implementer/reviewer split and the file roles.

**Strengths to keep:**
- "Build the check, don't write the rule" for mechanical violations (`:19`), and "missing guardrail is a finding" (`:18`).
- The category list doubles as a checklist for your own skills audits.
- The cross-reference to `writing-for-agents` resolves.

**Findings:**
| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | "Search through session logs on this machine" gives no location. Claude Code keeps transcripts in `~/.claude/projects/<slug>/*.jsonl`, and remote sessions are read via `list_events`. Without that, the agent guesses. | `SKILL.md:13` | V-SRC | Med |
| 2 | It assumes Matt's conventions (`CODING_STANDARDS.md`, a reviewer agent, an implementation/review split). Your repos and runner probably lack these, so recommendations can push you to create scaffolding you don't use. | `SKILL.md:19,29-35,42` | INF | Low |
| 3 | It names `AGENTS.md` as the global file but not `CLAUDE.md`, the file Claude Code actually loads (line 41 mentions both). | `SKILL.md:20` vs `:41` | V-SRC | Low |
| 4 | It accepts a session argument (`:13`) but has no `argument-hint`. | frontmatter `:1-5` | V-SRC | Low |
| 5 | "Present to the user" has no completion criterion (e.g., each candidate with evidence plus a concrete change). That invites a vague list, which by `writing-for-agents/SKILL.md:47-52` is weak demand. | `SKILL.md:25` | V-SRC | Low |

**Recommendations:**
1. Add a log pointer → #1. After `:13` add:
   > Claude Code transcripts live in `~/.claude/projects/<project-slug>/<session-id>.jsonl` (Windows: `%USERPROFILE%\.claude\projects`). For a claude.ai remote session, use `list_events` on its session id.

   → **S**.
2. Add `argument-hint: "Which session? (blank = this one)"` → #4 → **S**.
3. Sharpen step 4 → #5:
   > For each candidate give: the evidence (transcript line or file:line), the category, and the exact file or check to add. Stop when every category has been checked and either yielded a candidate or a stated 'none'.

   → **S**.
4. Optionally (local fork) replace `CODING_STANDARDS.md` with "the repo's standards doc if it has one" → #2/#3. Prefer filing upstream → **S**.

**Quick wins (<30 min):** Recommendations 1 and 2.

**Open questions:**
- Do you want retro to cover non-code sessions too (Premiere/Filmora runner, browser automation)? If so, the "coding session" framing should be widened in a local fork.

[↑ back to contents](#table-of-contents)

---

#### teach
**Identity:** no version field (upstream v1.3.2; path anchoring and quiz-position fix from upstream PR #1183, 2026-10-07) · `mattpocock/skills` `skills/productivity/teach` · 6 files / 18.2 KB (SKILL.md 9.7 KB, about 2.4k tokens, plus 4 format files) · synced 2026-10-30T23:16:46Z · entry point: `/teach <topic>`

**Purpose & triggering:** A stateful, multi-session tutor. It builds a workspace in the current directory: a mission, resources, learning records, HTML lessons, a reusable asset library, reference sheets and notes. It is grounded in retrieval practice, spacing and the zone of proximal development. It is user-invoked with a human-facing description and an argument hint, which is good. There is conceptual overlap with your `medical-visual-board`, `etymology` and `ymnotes-youtube-video-finder` skills for medical topics, but no trigger conflict, because teach is user-invoked.

**How it actually works:** `SKILL.md:12` resolves workspace paths from the directory `/teach` ran in, and format files from the skill folder → `:14-20` define the files (`MISSION.md`, `reference/*.html`, `RESOURCES.md`, `learning-records/*.md`, `lessons/*.html`, `assets/*`, `NOTES.md`) → `:75` interviews for the mission first if it is missing → `:30` sets "never trust parametric knowledge", so it fills RESOURCES first → `:49-61` produce a numbered lesson HTML and try to open it via CLI (`:55`) → `:67` reuses `./assets/`. Format files: `MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md` (lazy-creates `./learning-records/`, `:3`). `GLOSSARY-FORMAT.md` is never linked from SKILL.md.

**Strengths to keep:**
- Strong pedagogy: the fluency vs storage-strength split, desirable difficulty, and the knowledge/skills/wisdom split (`:24-45`).
- Source-first stance (`:30,95`), which suits medical teaching. Pair it with your PubMed MCP.
- Quiz anti-cueing rule (`:110`), and lazy directory creation (LEARNING-RECORD-FORMAT `:3`).

**Findings:**
| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | **Writes into whatever directory you happen to be in.** Run inside a code repo (e.g. this `Learning-Repo0` or the runner repo), it creates `lessons/`, `assets/`, `reference/`, `MISSION.md`, `RESOURCES.md`, `NOTES.md` at the repo root. The generic names `assets/` and `reference/` can mix with existing project folders, and the files get swept into git commits. There is no "check the directory is empty or dedicated" step. | `SKILL.md:12,14-20,67` | V-SRC | Med |
| 2 | Glossary location is contradictory: SKILL.md puts glossaries in `./reference/*.html` (`:15,134-136`), while `GLOSSARY-FORMAT.md` and LEARNING-RECORD-FORMAT define a root `GLOSSARY.md`. `GLOSSARY-FORMAT.md` is orphaned, since SKILL.md never links it. | `SKILL.md:15,134-136`; `GLOSSARY-FORMAT.md:1-3`; `LEARNING-RECORD-FORMAT.md:41` | V-SRC | Med |
| 3 | Record IDs are inconsistent: files are `0001-slug.md`, but supersession uses `LR-NNNN`. | `SKILL.md:17`; `LEARNING-RECORD-FORMAT.md:21,46` | V-SRC | Low |
| 4 | "Open the lesson file … by running a CLI command" is OS-specific (`start` / `open` / `xdg-open`) and fails silently in cloud sessions, where there is no browser. The skill never says to fall back to printing the path or publishing an artifact. | `SKILL.md:55` | INF | Low |
| 5 | Lessons hard-code external links and assets, but there is no guidance for offline/print use, although reference docs "should print out well" (`:15`). Matters for students who print handouts. | `SKILL.md:15,57` | INF | Low |
| 6 | Wiki-link syntax `[[MISSION.md]]` / `[[GLOSSARY.md]]` in the format files is not a real link for Claude. It is harmless but inconsistent with the `[x](./x)` links elsewhere. | `LEARNING-RECORD-FORMAT.md:36,41` | V-SRC | Low |

**Recommendations:**
1. Add a workspace guard → #1. Insert after `SKILL.md:12`:
   > Before writing anything, check the current directory. If it is a git repository or already contains files not created by this skill, propose a dedicated folder (`./learn-<topic>/` or `~/learning/<topic>/`) and ask before writing.

   (Local fork; also worth an upstream issue.) → **S**.
2. Fix glossary → #2. Either add to the file list at `:20`: "`GLOSSARY.md`: canonical terminology. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md)", and change `:136` to "The glossary lives in `GLOSSARY.md`; an HTML print view may live in `./reference/`". Or delete `GLOSSARY-FORMAT.md`. File upstream → **S**.
3. Lesson opening fallback → #4: replace `:55` with
   > Open the lesson for the user (`start` on Windows, `open` on macOS, `xdg-open` on Linux). If no browser is available, print the absolute path.

   → **S**.
4. For medical use: add to NOTES or a local fork, "Prefer PubMed / guideline sources; cite with PMID/DOI" → **S**.

**Quick wins (<30 min):** Recommendation 1 (or simply always run `/teach` from a fresh folder), and recommendation 2.

**Open questions:**
- Do you plan to use teach for your own learning, or to generate student lessons? For students, its outputs overlap with `ymnotes-medical-book-redesign` and `medical-visual-board`, so a shared style asset may be wanted.

[↑ back to contents](#table-of-contents)

---

#### writing-for-agents
**Identity:** no version field (upstream v1.3.2) · `mattpocock/skills` `skills/productivity/writing-for-agents` · 3 files / 13.6 KB (SKILL.md 10.9 KB, about 2.7k tokens; SKILL-MECHANICS.md 2.6 KB) · synced 2026-10-30T23:16:57Z · entry point: **model-invoked** (description in context every turn); also called by `retro` (`retro/SKILL.md:11`)

**Purpose & triggering:** A style reference for any document an agent consumes. It covers context pointers, the two loads (context vs cognitive), the information hierarchy and progressive disclosure, completion criteria, leading words, negation, and pruning. SKILL-MECHANICS covers invocation choice and router skills. The description is short (about 110 chars) and well-targeted ("creating or editing skills, or modifying AGENTS.md or CLAUDE.md"). **Overlap:** it fires on exactly the same task as Anthropic's `skill-creator` ("create new skills, modify and improve existing skills"), and the two give partly opposing advice on descriptions (see #1).

**How it actually works:** The description triggers on skill/CLAUDE.md edits → `SKILL.md:8` points to `SKILL-MECHANICS.md` when the document is a skill → body sections `:10-81` are flat reference with no steps → MECHANICS `:5-14` gives the invocation decision and `:20-22` the router pattern. All internal links resolve (`SKILL.md:8,59`; `SKILL-MECHANICS.md:3`).

**Strengths to keep:**
- A precise vocabulary (context pointer, branch, completion criterion, sediment, no-op), useful for the whole skills review.
- The user-invoked vs model-invoked guidance (`SKILL-MECHANICS.md:9-12`) correctly explains why grill-me/handoff/retro/teach cost no context.
- The no-op test and the "delete the whole sentence" rule (`SKILL.md:81`).

**Findings:**
| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | It co-triggers with `skill-creator`, with conflicting guidance. writing-for-agents says "one trigger per branch; collapse synonyms; prune the pointer" (`SKILL.md:14-18`). skill-creator (and the n8n skills' style) favours long, "pushy" trigger lists. When you edit a YMnotes skill, both load and the agent gets mixed signals. | `SKILL.md:3,14-18`; skill-creator description in manifest | V-SRC | Med |
| 2 | It promises "frontmatter" coverage (`SKILL.md:8`), but MECHANICS covers only `description` and `disable-model-invocation`. Nothing on `argument-hint`, `allowed-tools`, `model`, the description length limit, or the fact that claude.ai-synced skills cannot ship hooks or scripts that run. | `SKILL.md:8`; `SKILL-MECHANICS.md:5-14` | V-SRC | Low |
| 3 | `SKILL-MECHANICS.md:10,14` says no other skill can reach a user-invoked skill. Upstream itself now reaches user-invoked skills "by relative path" (pending changeset `chief-of-staff-shared-wiki-procedures.md`), a legitimate workaround the doc doesn't mention. | `SKILL-MECHANICS.md:10,14`; upstream `.changeset/` | V-SRC | Low |
| 4 | All reference and no completion criterion. When used for an edit, nothing says what "done" looks like (e.g., "every line passed the no-op test"). This is its own rule (`SKILL.md:47-52`) unapplied. | `SKILL.md:6-81` | INF | Low |
| 5 | The description has no Arabic or "skill review" trigger. That is acceptable: you invoke it by name when auditing. | `SKILL.md:3` | INF | Low |

**Recommendations:**
1. Settle the co-trigger → #1. Choose a primary. Two options:
   - (a) Keep skill-creator for building and evals, and narrow writing-for-agents to wording: `description: Writing style for agent-read documents. Use when wording or pruning a skill body or description, CLAUDE.md, or AGENTS.md.`
   - (b) Add a line to your global CLAUDE.md: "When editing skills, follow writing-for-agents for wording; use skill-creator only for evals and packaging."

   → **S**.
2. Extend MECHANICS (local fork) → #2: add a short "Other frontmatter" section with `argument-hint` (shown in the slash menu), `allowed-tools`, and claude.ai sync limits (no hooks; other skills are reachable only via the Skill tool) → **S**.
3. Add a closing completion criterion → #4:
   > Done when every line of the edited document has passed the relevance and no-op tests and every pointer names its branches.

   → **S**.

**Quick wins (<30 min):** Recommendation 1(b), which costs one line in CLAUDE.md.

**Open questions:**
- Which philosophy do you want for the YMnotes skill descriptions: concise branch-per-trigger (Pocock) or exhaustive trigger lists (skill-creator/n8n)? The rest of the review should apply one consistently.

[↑ back to contents](#table-of-contents)

---


### G. Vendor skills (from n8n-io/skills, unmodified — do not edit locally)

#### n8n official skills

*Covers: using-n8n-skills-official, n8n-code-nodes-official, n8n-data-tables-official, n8n-debugging-official, n8n-error-handling-official, n8n-expressions-official, n8n-workflow-lifecycle-official*

**Identity:** `n8n-io/skills` (package v1.3.0, HEAD `27b6b9f`, 2026-10-17) · 7 of upstream's 15 skills, each synced as its own plugin (2026-10-31 09:38–09:40Z) · **byte-identical to upstream** (`diff -rq` empty for all 7) · 33 files / about 312 KB total · upstream `hooks/` (SessionStart + 3 PreToolUse + PostToolUse) **not synced** · entry point: all model-invoked

**Purpose & triggering:**
- `using-n8n-skills-official` is the router and tool cheat-sheet.
- The other six cover domain rules: Code-node avoidance, Data Tables, debugging, error branches and status codes, expressions/Luxon, and design → validate → test → publish.

Content quality is high and n8n-specific. **Verdict on descriptions:** `using-n8n` and `data-tables` are reasonably scoped. `error-handling`, `code-nodes`, `workflow-lifecycle` and `debugging` carry generic trigger words that will fire on non-n8n work.

**How it actually works:** All seven descriptions (2,523 chars, about 630 tokens) sit in context every turn → the router `using-n8n-skills-official/SKILL.md:14,24` orders "invoke the relevant skill before any n8n action … err on the side of loading too many" → each domain skill loads its SKILL.md and points to `references/*.md` → tool calls are made via `mcp__n8n__*`. Upstream's SessionStart hook would normally inject the router every session (`using-n8n…/SKILL.md:3`). The hook is absent here, so the router only loads when its description fires.

**Strengths to keep:**
- Excellent, specific guardrails, e.g. validate *and* re-fetch connections (`using-n8n…:15`, `workflow-lifecycle:34-51`); `test_workflow` side effects (`using-n8n…:59`); sequential fan-out (`workflow-lifecycle:54-60`); 4xx/5xx mapping (`error-handling:14-18`).
- The router's "surface drift" rule (`using-n8n…:8,203`).
- Data-table dedup and idempotency patterns, directly relevant to `ymnotes-register-students`-style flows if you move them to n8n.

**Tool-name currency (vs the live `mcp__n8n__*` server in this account, 59 tools):**
- All core names are **consistent**: `get_workflow_sdk_reference` (its section enum matches `using-n8n…:125` exactly), `validate_workflow` (takes `code`), `create_workflow_from_code`, `update_workflow` (op list, the group-op exception and max 100 all match `:131`), `execute_workflow` (`executionMode` required, matches `:143`), `test_workflow`, `prepare_workflow_pin_data`, the data-table, version-history and agent tools.
- **Referenced but absent:** `get_user_preferences`, `save_user_preference`, `update_user_preference`, `undo_user_preference` (`using-n8n…:30,52,90-104,199`). The skill itself says they sit behind a rollout flag and gives a fallback (`:95`). Each load spends tokens on them for nothing.
- **Live but never mentioned:** `get_instance_context` (the server's own instructions say to call it *before the first substantive answer*), `get_instance_activity`, `expand_instance_activity`, `get_node_usage`, `install_community_node`. The skills' protocol (`using-n8n…:193-203`) therefore omits the server's mandated first step.
- **Parameter drift:** the live `create_workflow_from_code` and `update_workflow` say "Always provide" `versionName`, and `get_workflow_details` has `detailLevel`. Neither appears anywhere in the 7 skills (grep count 0). `skillsUsed` is normalised to lowercase server-side, while the skills ask to keep the exact names (`using-n8n…:209`). That is harmless.

**Findings:**
| # | Finding | Evidence (file:line) | Label | Severity |
|---|---|---|---|---|
| 1 | **Dangling skill references.** 8 referenced skills are not installed: `n8n-node-configuration` (29 refs), `-subworkflows` (30), `-ai-nodes` (24), `-credentials-and-security` (23), `-agents` (18), `-loops` (12), `-binary-and-data` (7), `-extending-mcp` (3). The router's non-negotiable #3 and its "3-node webhook" default both point at missing skills, so the Skill tool will fail on them. | `using-n8n…/SKILL.md:16,24,29,44-57,70-80,173`; `workflow-lifecycle:62,74,126,176`; `expressions:79,207,308`; `data-tables:125,137`; `debugging:31,80`; `error-handling:81` | V-SRC | High |
| 2 | **Hooks missing.** The router claims "loaded by the SessionStart hook every session" and "PreToolUse hooks remind you". In claude.ai-synced skills there are no hooks, so the always-on protocol and the validate/create/update reminders never run. | `using-n8n…/SKILL.md:3,14`; upstream `hooks/hooks.json` | V-SRC | Med |
| 3 | **Trigger overreach, error-handling.** It fires on "API", "production", "error", "failure", "scheduled", "webhook", "try/catch", "any workflow that runs unattended". The YMnotes runner (exit codes, "error", checkpoint/resume), the scheduled daily `ymnotes-register-students` run, Render deploys, or Supabase errors can load about 3k tokens of n8n webhook/4xx rules. | `n8n-error-handling-official/SKILL.md:3` | V-SRC | High |
| 4 | **Trigger overreach, code-nodes.** It fires on "Code", "JavaScript", "Python", "transform data", "write a function". Any JS/Python work, e.g. editing `ymnotes-runner.mjs` or PDF scripts, can pull in "the Code node is a last resort" rules. | `n8n-code-nodes-official/SKILL.md:3` | V-SRC | High |
| 5 | **Trigger overreach, workflow-lifecycle.** It fires on "design", "organize", "structure", "ship", "deploy", "publish". "Publish" is core YMnotes vocabulary (YouTube, e-teaching.site, Shorts social publishing), and "design" covers book redesign and visual boards. A hijack loads about 4.9k tokens, plus references up to about 25k. | `n8n-workflow-lifecycle-official/SKILL.md:3` | V-SRC | High |
| 6 | **Trigger overreach, debugging.** "errors", "it's not working", "why is this happening", "any debugging context". It competes with every non-n8n debug task. | `n8n-debugging-official/SKILL.md:3` | V-SRC | Med |
| 7 | Lesser overreach: expressions ("DateTime", "format date", "any node-parameter assignment"); data-tables ("dedup", "idempotency", "lookup", "persistent state", which the register-students dedup logic shares). | `n8n-expressions-official/SKILL.md:3`; `n8n-data-tables-official/SKILL.md:3` | V-SRC | Low |
| 8 | **Context cost.** Always-on: 7 descriptions, about 630 tokens per turn. On a typical n8n build the router pulls 4+ skills (`using-n8n…:24`): router about 6.9k + lifecycle 4.9k + expressions 5.3k + error-handling 3.0k is about **20k tokens** before any reference. Loading all 7 SKILL.md files is about 29k tokens. Full packs with references are about 76k tokens (lifecycle refs alone about 20k, `REVIEW_CHECKLIST.md` 39 KB). | sizes: `wc -c` per file (chars/4) | V-SRC | Med |
| 9 | **Overlap.** (a) The expression → Edit Fields → Code decision tree appears in three places (`code-nodes:16-37`, `references/DECISION_TREE.md`, `expressions:369-379`). (b) "validate + get_workflow_details + test before publish" appears in `using-n8n…:15,43,202` and `workflow-lifecycle:23-51` plus `VALIDATION_CHECKLIST.md`. (c) "error" is shared by `debugging` and `error-handling`, so both load on one failure. (d) The router's 135-line tool table restates the MCP's own tool schemas, a cache that drifts (see #10/#11). | lines cited | V-SRC | Low |
| 10 | **Drift vs the live MCP.** Four preference tools are absent. Five live tools go unmentioned, including `get_instance_context`, which the n8n server instructions mandate first. `versionName` (live: "Always provide it") and `detailLevel` are never mentioned. | `using-n8n…:90-104,193-203`; live tool schemas | V-RUN | Med |
| 11 | **Rule 1 of the router demands a Skill call before *any* n8n action** and "even if you already read it" (`:36`). That causes repeated reloads of 5–7k-token skills within one session. | `using-n8n…/SKILL.md:14,36,61` | V-SRC | Low |

**Recommendations (vendor-maintained, so manage the pack rather than editing files):**
1. **Decide pack completeness first** → #1, #2. Either:
   - (a) **Install the full upstream set**: add the 8 missing skills, at about 8×80 more description tokens per turn. Since synced skills can't run hooks, add one line to global CLAUDE.md as the hook substitute: "For any n8n task, first call `get_instance_context`, then invoke `using-n8n-skills-official`."
   - (b) **Trim to a core subset.**

   Recommended: (a) if you build n8n workflows weekly, (b) otherwise → **S/M**.
2. **Keep subset (if b):** `using-n8n-skills-official`, `n8n-workflow-lifecycle-official`, `n8n-expressions-official`, `n8n-error-handling-official`. **Disable** `n8n-code-nodes-official` (its decision tree is already summarised in `expressions:369-379`), `n8n-data-tables-official` (re-enable when you use Data Tables) and `n8n-debugging-official` (its key steps are "re-fetch workflow / node types / execution", which the router covers). This saves about 280 description tokens per turn and removes the "Code/JavaScript" and "debugging" hijacks → #4, #6, #9 → **S**.
3. **Contain overreach without editing vendor files** → #3–#7. Add to global CLAUDE.md:
   > The n8n-*-official skills apply only when the task involves an n8n workflow, node, expression, Data Table or the `mcp__n8n__*` tools. Words like 'error', 'publish', 'deploy', 'scheduled', 'API', 'JavaScript' in YMnotes runner, video publishing, Render/Supabase or other work do not trigger them.

   → **S**.
4. **File upstream issues on `n8n-io/skills`** → #3–#7, #10:
   - (i) Scope every description with "in n8n" / "n8n workflow", e.g. `error-handling`: "Use when building or hardening an **n8n** workflow that is webhook-triggered, scheduled, or production-bound…". Drop bare "API", "error", "production", "scheduled", "Code", "JavaScript", "design", "publish", "deploy".
   - (ii) Add `get_instance_context` as protocol step 0 and mention `versionName` and `detailLevel`.
   - (iii) Note that hook-less installs (claude.ai skill sync) need a fallback for the SessionStart router.
   - (iv) Make the preference-tool section conditional on presence, or move it to a reference file.

   → **S** (writing issues).
5. **Monitor currency**: re-diff against `n8n-io/skills` monthly. It moved 2026-10-17, and the live MCP already exposes newer tools. Watch whether upstream adds `get_instance_context` → **S**.
6. If you keep the pack, tell sessions to load references on demand, not by default (e.g. read `REVIEW_CHECKLIST.md` only for audits), to cap the about 76k-token full load → #8, #11 → **S**.

**Quick wins (<30 min):**
- Add the CLAUDE.md scoping line (recommendation 3).
- Add the `get_instance_context`-first line (recommendation 1a).
- Disable `n8n-code-nodes-official` and `n8n-debugging-official` if you choose the subset.

**Open questions:**
- How often do you build or edit n8n workflows vs run the YMnotes runner and video work? That frequency decides between full pack and subset.
- Is the n8n instance n8n Cloud or self-hosted, and which version? The preference tools need 2.41/2.42+, and Gateway credits are Cloud-only (`using-n8n…:32,92`).
- Were the 8 missing skills deliberately excluded (e.g., to save context) or lost in a partial sync like `grilling`?

[↑ back to contents](#table-of-contents)

---


## Appendix — Metrics

Measured from the synced skill files on 2026-11-01. "Description" is what loads into **every** session's skill list. "Body" is what loads when the skill triggers. "Hard paths" counts machine-specific paths such as `C:\Users`, `D:\`, `/Users/`.

| Skill | Description chars | SKILL.md words | Files | Test/eval files | Hard paths | Manual-only (`disable-model-invocation`) |
|---|---|---|---|---|---|---|
| ymnotes-premiere-shorts | 877 | 1,308 | 22 | 6 | 1 | no |
| etymology | 854 | 1,140 | 4 | 0 | 0 | no |
| premiere-basic-video-workflow | 531 | 4,563 | 128 | 12 | 113 (machine-local config) | no |
| ymnotes-video-visuals | 518 | 787 | 7 | 0 | 0 | no |
| n8n-workflow-lifecycle-official | 510 | 2,835 | 9 | 0 | 0 | no |
| incision-block5-7-exams | 492 | 1,138 | 27 | 0 | 0 | no |
| ymnotes-youtube-video-finder | 492 | 1,016 | 7 | 0 | 0 | no |
| ymnotes-batch-messages | 481 | 987 | 13 | 0 | 0 | no |
| ymnotes-register-students | 457 | 1,005 | 3 | 0 | 0 | no |
| n8n-error-handling-official | 455 | 1,703 | 7 | 0 | 0 | no |
| graphify | 446 | 1,264 | 26 | 1 | 3 | no |
| medical-visual-board | 429 | 1,461 | 5 | 1 | 0 | no |
| filmora-basic-video-workflow | 393 | 2,271 | 23 | 1 | 32 | no |
| ymnotes-medical-book-redesign | 367 | 1,481 | 197 | 17 | 8 | no |
| ymnotes-questions | 366 | 516 | 66 | 4 (in `fixtures/test_*.py`) | 0 | no |
| n8n-code-nodes-official | 364 | 1,684 | 4 | 0 | 0 | no |
| n8n-data-tables-official | 319 | 1,639 | 4 | 0 | 0 | no |
| n8n-expressions-official | 305 | 3,029 | 1 | 0 | 0 | no |
| n8n-debugging-official | 289 | 1,628 | 3 | 0 | 0 | no |
| using-n8n-skills-official | 281 | 3,910 | 1 | 0 | 0 | no |
| codex-delegate | 193 | 1,871 | 11 | 0 | 2 | no |
| ymnotes-qr | 153 | 973 | 2 | 0 | 0 | no |
| writing-for-agents | 103 | 1,757 | 3 | 0 | 0 | no |
| handoff | 86 | 114 | 2 | 0 | 0 | yes |
| teach | 61 | 1,496 | 6 | 0 | 0 | yes |
| grill-me | 51 | 6 | 2 | 0 | 0 | yes |
| retro | 44 | 665 | 2 | 0 | 0 | yes |
| **Total (27 installed skills)** | **9,917** | | | | | |

The whole skill list, including the 13 Anthropic skills, is about 19,000 characters of descriptions in every session. `ymnotes-register-students` appears **twice**: the repo copy in `.claude/skills/` and the synced copy.

The per-skill sections in Part 4 are the full review notes. The Premiere deep audit, with its research appendices, lives in [`premiere-skill-audit/`](premiere-skill-audit/).
