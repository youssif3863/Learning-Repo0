# YMnotes Premiere Skill — Technical Audit and Integration Research

**Research date:** 2026-11-01  
**Audit target:** `premiere-basic-video-workflow` v1.1 (the uploaded `premiere-basic-video-workflow.skill_1.zip`, byte-identical to the synced Claude copy except three dotfiles), and its continuation `ymnotes-premiere-shorts` v6.  
**Scope:** analysis and recommendations only. Nothing was installed, no skill file was modified, Premiere was not touched, and no project was edited.

## How to read the evidence labels

| Label | Meaning |
|---|---|
| **[V-SRC]** | Verified by reading source code, a package tarball, a registry record or a primary vendor document |
| **[V-RUN]** | Verified by running a permitted, read-only check in the research container: the skill's own offline tests on a scratch copy, registry queries, grep |
| **[DOC]** | Documented by a credible source, not checked against code |
| **[INF]** | Inferred from verified facts |
| **[UNK]** | Unknown; Section 10 says how to settle it |

**Important limitation.** No computer was attached to this session, so I did **not** inspect your Windows workstation. Every environment fact below comes from the skill's own configuration and evidence files: `config/premiere-host-capabilities.json`, `evidence/*.md` and `config/workflow-defaults.json`. Those files record what earlier runs observed on your machine, but I could not confirm the current installed state. Section 10 lists the read-only commands that would confirm it.

The full research notes, with code excerpts and more than 110 source links, are in [`research/`](research/):

- `00-audit-notes.md` — my own audit notes
- `01-premiere-mcp-servers.md` — MCP servers and bridges
- `02-adobe-official-apis.md` — UXP, CEP, ExtendScript and native features
- `03-silence-audio-interchange.md` — silence and pause tools, audio cleanup, XML/OTIO interchange, Shorts tools
- `04-transcription-captions.md` — ASR, VAD and captions

---

## 1. Verdict

**Keep the current architecture: Claude Code → deterministic Node runner → `premiere-pro-mcp` CEP file bridge → ExtendScript, with the direct-cut QE engine.** Then harden it, upgrade its bridge in a controlled way, and add a local captions pipeline. Do not replace it now.

- **The core already works.** It is the one part of your workflow proven at production scale: 874 ripple cuts with frame delta 0, no gaps, no orphans and no generated subclips, plus a certified 63-minute lecture ([V-SRC] `evidence/CONTROLLED_FULL_TEST_2026-09-05.md`, `PRODUCTION_RELEASE.md`). No Premiere step uses mouse clicks or screen coordinates.
- **No alternative is better yet:**
  - UXP on your Premiere 26.3 has **no razor and no range extract or lift**. Razor APIs first appear as "New APIs Coming in 27.1 (Beta)" in Adobe's samples ([V-SRC] [AdobeDocs samples commit 8d75ef1](https://github.com/AdobeDocs/uxp-premiere-pro-samples/commit/8d75ef1e7d76d08818696e7c9545fa8913b2d8f8)).
  - The other Premiere MCP servers are no better than the one you use, and two have security or telemetry problems (§5).
  - XML/OTIO interchange is promising but unproven on your host.
- **The weaknesses are verifiable and fixable, mostly in verification code you already own** (§2.6):
  - The production runner disables the stale-timeline fingerprint guard.
  - The "re-verify after a Premiere or bridge update" safety rule is never actually enforced.
  - Frame rate is forced to an integer.
  - The edit gate tolerates one-frame errors and inspects only V1/A1.
  - Nothing checks that each cut landed in the right place, only that the total length is right.
- **Your bridge is 58 releases behind.** You run `premiere-pro-mcp` 1.14.1 (2026-08-28); the latest is 1.27.0 (2026-10-31) ([V-RUN] npm registry). The newer versions fix all seven bridge defects your skill had to route around. They also add an asynchronous Media Encoder export with job status, a working `delete_sequence`, a cross-process lock and idempotency keys ([V-SRC] tarball diff). But the package changes extremely fast — about 1,000 commits in two months, essentially one maintainer — so **pin an exact version and pilot it on a disposable project before production use.**
- **Your use case's biggest gaps are captions and audio cleanup.** Neither needs a new heavy tool:
  - faster-whisper is already installed and already bundles Silero VAD.
  - YouTube's `captions.insert` API can carry the captions without going through Premiere. Premiere cannot transcribe Arabic, and its Arabic caption rendering has a history of bugs.
- **The CEP clock.** Adobe's developer blog (September 2026) says:
  - Premiere stops accepting new CEP submissions in **December 2027**.
  - CEP becomes **disabled by default in December 2028**.
  - CEP is **removed from new versions from December 2029**. "ExtendScripts are not affected by this transition" ([V-SRC] [Adobe Developer Blog](https://blog.developer.adobe.com/en/publish/2026/09/investing-in-the-future-of-creative-cloud-extensibility-uxp-comes-to-our-flagship-applications)).
  - Your bridge is CEP-hosted, so plan a UXP migration in 2027–2028, once Adobe's razor APIs are generally available. Not now.

**Strongest recommended approach, in order:**

1. A no-install hardening patch to the gates and engine (P0).
2. A pinned, piloted upgrade to `premiere-pro-mcp` 1.27.0, using its asynchronous export (P1).
3. A local captions stage: faster-whisper with hotwords, glossary correction and Silero VAD, then YouTube `captions.insert` (P1).
4. A Silero VAD "speech-inside-cut" guard as a non-destructive cross-check on the frozen silence profile (P1).
5. An optional post-export audio-cleanup remux, behind a listening pass (P2).
6. An XML/OTIO interchange pilot and a UXP migration track as the long-term exit from CEP and QE (P2/P3).

---

## 2. Audit of the current skill

### 2.1 What was inspected

- All 131 files of the uploaded skill.
- The Shorts skill: 23 files, including `scripts/ymnotes-shorts.mjs` (1,065 lines).
- The full execution path, read end to end:
  `scripts/ymnotes-runner.mjs` (1,407 lines) → `scripts/build-final-from-plan.mjs` → `engine/direct-cut/execute-timeline-cuts.mjs` → `scripts/lib/mcp-client.mjs` → `premiere-pro-mcp` `dist/bridge/file-bridge.js`.
- The bridge files in the 1.14.1 and 1.27.0 npm tarballs, read but not executed.
- The gates: `scripts/verify-job-completion.mjs`, `scripts/verify-export-file.mjs`, `scripts/lib/host-capabilities.mjs`.
- The evidence history.
- The skill's own four test suites, run on a scratch copy.

### 2.2 Environment (from the skill's own records; not live-inspected)

| Item | Value | Source |
|---|---|---|
| OS | Windows (`win32`) | [V-SRC] `config/premiere-host-capabilities.json` → `host.platform` |
| Premiere Pro | **26.3.2** (Premiere Pro 2026), observed 2026-09-04 | same file |
| Bridge | `premiere-pro-mcp` **1.14.1**, CEP panel + file bridge, temp dir `C:\Users\hp\AppData\Local\Temp\premiere-mcp-bridge` | same file; `config/workflow-defaults.json` → `environment` |
| CPU / GPU / RAM | AMD Ryzen 7 5700U (8C/16T), AMD Radeon integrated graphics, **no NVIDIA/CUDA**, 15.3 GiB RAM | [V-SRC] `evidence/LOCAL_TRANSCRIPTION_BENCHMARK.md` |
| Python | 3.12.10 venv `C:\Users\hp\.codex\venvs\premiere-transcription` | same |
| ASR | faster-whisper 1.2.1, CTranslate2 4.8.2, `large-v3-turbo` int8 on CPU, real-time factor ≈ 1.01 (60 min ≈ 61 min). SCAN mode used `small` | same; `evidence/CONTROLLED_FULL_TEST_2026-09-05.md` |
| Node / ffmpeg | Node ≥ 20 (bridge 1.27 needs ≥ 20.19); ffmpeg/ffprobe from a WinGet build (an npm `ffmpeg` shim earlier on PATH caused false failures) | [V-SRC] `evidence/AUTOPILOT_HARDENING_2026-09-29.md`; npm `engines` |
| Shorts Python deps | opencv-python-headless, numpy, pillow, arabic-reshaper, python-bidi; YuNet face ONNX | [V-SRC] `ymnotes-premiere-shorts/requirements-shorts.txt` |
| Other agents | Codex reads the same repo through a junction. Claude Code uses the `premiere` MCP server and `graphify-premiere` | [V-SRC] `README.md` |
| Production repo | `D:\Github3863\…\Adobe premiere Skill` (local git, no remote) | [V-SRC] `SKILL.md`, `PRODUCTION_RELEASE.md` |
| Other Premiere plugins | **[UNK]** — needs a look at the CEP extensions folder and Premiere's plugin manager (§10) |

### 2.3 How Claude Code actually talks to Premiere (traced)

```text
Claude Code ──(ad-hoc MCP tools)──► `premiere` MCP server (premiere-pro-mcp, stdio)
                                         │
Claude Code ──(one Bash call)──► node scripts/ymnotes-runner.mjs (detached, lock + state)
                                         │ spawns its own stdio premiere-pro-mcp
                                         │   via scripts/lib/mcp-client.mjs (hard-coded default
                                         │   C:/Users/hp/AppData/Roaming/npm/node_modules/premiere-pro-mcp/dist/index.js)
                                         │
                                         ├─► build-final-from-plan.mjs ─► engine/direct-cut/execute-timeline-cuts.mjs
                                         │        imports premiere-pro-mcp PRIVATE internals:
                                         │        dist/bridge/file-bridge.js (sendCommand)
                                         │        dist/bridge/script-builder.js (buildToolScript)
                                         ▼
                 %TEMP%\premiere-mcp-bridge\cmd_<uuid>.jsx  ──►  CEP panel inside Premiere
                 (panel polls every 200 ms, renames the file,     evalScript(ExtendScript, incl. QE DOM)
                  writes busy_<id>.json heartbeats)           ◄──  res_<uuid>.json
```

[V-SRC] `scripts/lib/mcp-client.mjs:16-60`, `engine/direct-cut/execute-timeline-cuts.mjs:398-423`; bridge mechanics from `premiere-pro-mcp` 1.14.1 `dist/bridge/file-bridge.js` (research/01).

**Consequences:**

1. Up to three writers can address one panel: Claude's MCP server, the runner's MCP child, and the engine's direct `sendCommand`. Only the skill's own `autopilot.lock` and a "do not issue MCP calls" instruction keep them apart. In 1.14.1 the panel starts every waiting command at once and Premiere runs them in turn. 1.27.0 adds a real cross-process lease ([V-SRC]).
2. The engine depends on undocumented internal files of a package that releases almost daily. The files still exist in 1.27.0, but 1.27.0 adds a temp-folder privacy check run through PowerShell, a host lease (`HOST_LEASE_BUSY`), a 32-command queue limit, a 1 MiB response cap, and a panel-version match that refuses edits on mismatch ([V-SRC] research/01 §"engine imports").
3. On timeout, 1.14.1 keeps waiting while the panel refreshes its busy marker, up to `max(4 × timeoutMs, 120 s)`. That is **1,200 s** for the engine's 300 s default. A script the panel has already started cannot be cancelled ([V-SRC] `file-bridge.js` `pollForResponse`, `hardCapMs`).

### 2.4 Execution path by runner stage

| Runner stage | What runs | Premiere interface | Verification in code |
|---|---|---|---|
| S1_PREFLIGHT | ffprobe sources, disk, MCP `verify_premiere_connection`, YouTube token | MCP | PASS/WARN/BLOCKER table |
| S2_PROJECT_BACKUP | copies `.prproj` files | none | file copy |
| S3_PREMIERE_PREP | `get_full_project_overview`, `open_project`/`create_project`, `import_media` (missing only, matched by normalized path), `create_sequence_from_clips` → SOURCE_BACKUP | MCP | order, V1/A1 count, contiguity and frame sum, using `Math.round(seconds × fps)` |
| S4_DETECTION | MCP `detect_silence` per recording (ffmpeg `silencedetect` at −13.98 dB, 0.6 s) | MCP shells out to ffmpeg | cached per profile |
| S5_CUT_PLAN | `plan-silence-keep-segments.mjs` | none | planner checks |
| S6_EDIT | `duplicate_sequence` → rename WORK → `compile-timeline-cut-plan.mjs` → `build-final-from-plan.mjs` → **one ExtendScript loop**: `seq.setInPoint/OutPoint(ticks)` + `qeSeq.extract()`, descending | raw ExtendScript + **QE DOM** (unsupported) | project-item count before/after; total frames; V1 vs A1 clip **count** |
| S7_BRANDING | `apply-branding.mjs`: `add_to_timeline` + `set_clip_properties_batch` + `set_clip_anchor_point`, read back through `get_effect_properties` | MCP | normalized-unit adapter, coverage spans |
| S8_EDIT_QC | `get_sequence_structure`, `get_timeline_gaps`, `get_clip_links` ×3, then `verify-job-completion.mjs --stage edit` | MCP | see §2.6 for the limits |
| S9_SAVE | relink temporary paths, `save_project` | MCP | mtime check |
| S10_EXPORT | validate preset (SHA-256 pinned) → `export_sequence` (1.14.1 = `seq.exportAsMediaDirect`, which blocks Premiere's script engine for the whole encode) → bridge timeout treated as "still encoding" → poll the output file | MCP | file growth and stability |
| S11_EXPORT_QC | `verify-export-file.mjs`, `verify-branding-frames.mjs` | ffprobe/ffmpeg only | duration ±1.0 s, streams, 3 decoded frames, region-ink and edge-correlation branding detector |
| S12–S16 | SCAN transcription, metadata, YouTube resumable upload, e-teaching (Chrome) | none / browser | validators, API readback |
| S17 (Shorts) | `ymnotes-shorts.mjs`: `create_sequence_from_preset`, `overwrite_clip`, `add_keyframe`, `set_effect_property`, `remove_from_timeline`, `export_sequence` | MCP, hundreds of calls per Short (in Node, not agent turns) | structure counts, blackdetect/freezedetect |

[V-SRC] `scripts/ymnotes-runner.mjs:409-1050`; `ymnotes-premiere-shorts/scripts/ymnotes-shorts.mjs:315-660`.

### 2.5 YMnotes workflow coverage

| Workflow | Status today | Evidence |
|---|---|---|
| Long multi-file recordings → assembly with intro/outro | **Supported, production-proven** | §2.4; Digestive 04/05 runs |
| Silence/pause removal | **Supported, production-proven**, but the detector is an absolute amplitude threshold (gain-dependent, §2.6 #11) and no speech check runs in autopilot | `config.silence_profile`; runner has no call to `diagnose-speech-tails.mjs` |
| Webcam overlay | **Not handled by the lecture skill.** The webcam is an OBS picture-in-picture baked into the recording. The Shorts skill detects the PiP layout per frame (edge step plus YuNet) and recomposes vertically | `ymnotes-premiere-shorts/scripts/shorts/probe-layout.py` |
| Audio cleanup | **Not supported.** Only optional loudness gain matching, disabled by default (`config.loudness.enabled=false`). No noise reduction, EQ, compression or limiting | `PRODUCTION_RELEASE.md` "NOT ACTIVE" table |
| Captions (lecture) | **Not supported.** FULL transcription exists but produces no SRT/VTT and uploads no captions | `scripts/transcribe-final-video.py`; no caption code |
| Captions (Shorts) | **Supported as PNG images** (Pillow + arabic-reshaper + bidi), placed as stills, with a keyframed "karaoke" fill | `ymnotes-shorts.mjs:441-560` |
| Graphics | One PNG signature on V3 with verified normalized transforms; Shorts layered graphics | `apply-branding.mjs`; Shorts |
| Markers / chapters in Premiere | **Not supported.** Chapters exist only in YouTube metadata | no marker calls |
| Export | **Supported**, canonical preset pinned by SHA-256; bridge timeout handled by polling | §2.4 |
| Short clips | **Supported** (Shorts v6: four per lecture) | Shorts SKILL.md |

### 2.6 Verified weaknesses, defects and overstated claims

Severity reflects impact on correctness of a delivered lecture.

| # | Finding | Evidence | Severity |
|---|---|---|---|
| 1 | **The stale-timeline fingerprint guard is off in production.** The runner never passes `--baseline-fingerprint`, so the plan records `stale_state_check: "sequence_id_only"`. Only the sequence ID protects against cutting a modified WORK timeline | [V-SRC] `ymnotes-runner.mjs:643-646`; `compile-timeline-cut-plan.mjs:193-210` | High |
| 2 | **"A version change downgrades verdicts to UNVERIFIED" is documented but never enforced.** `capabilityState()` degrades only when a `live` argument is passed, and no caller passes one. Nothing reads `app.version` or the bridge version. A Creative Cloud auto-update to 26.5 (where scripted work-area changes are reportedly ignored — research/01) would still route through "VERSION_VALIDATED" QE extract | [V-SRC] `scripts/lib/host-capabilities.mjs:30-60`; callers `build-final-from-plan.mjs:49`, `upload-route.mjs:32` | High |
| 3 | **Frame rate is forced to an integer over 1.** The runner passes `--fps-num Math.round(sb.fps) --fps-den 1`. A 29.97 (30000/1001) sequence would be compiled with 30 fps ticks (8,467,200,000 instead of 8,475,667,200 per frame), so cut positions drift about 0.1 %, roughly 3.6 s per hour. This is caught only *after* all cuts, as a frame-delta failure. Adobe recommends converting OBS variable-frame-rate footage to constant frame rate ([DOC] [Adobe VFR FAQ](https://community.adobe.com/t5/premiere-pro/faq-variable-frame-rate-vfr-video/td-p/10348229)), and the preflight doesn't check for it | [V-SRC] `ymnotes-runner.mjs:395, 645`; tick values [V-SRC] research/02 §7 | Medium–High (latent today at 30 fps) |
| 4 | **The edit gate tolerates one frame.** `near()` defaults to one frame of tolerance for V1/A1 start/end matching and for contiguity. SKILL.md says "Any orphan, gap, or one-frame A/V mismatch fails the edit" — but a one-frame offset or gap passes these checks | [V-SRC] `verify-job-completion.mjs:51-58, 91-106`; `SKILL.md:108` | Medium |
| 5 | **Orphans are never computed in autopilot.** S8 writes `orphans: []` as a literal. Clip links are sampled for only 3 of hundreds of clips | [V-SRC] `ymnotes-runner.mjs:694, 710` | Medium |
| 6 | **Only V1/A1 are cut and checked.** The engine targets `["V1","A1"]` and never untargets other tracks. The gate inspects only V1/A1. A recording with a second audio stream (OBS multi-track), or a stray targeted or sync-locked track, is never checked. How QE extract treats untargeted sync-locked tracks is [UNK] | [V-SRC] `compile-timeline-cut-plan.mjs:53-54`; engine `:709-720`; gate `:84-130` | Medium |
| 7 | **Correctness is checked as a total, not per cut.** The gates compare total frames and V1/A1 alignment, never each FINAL clip's source in/out against the keep plan. A set of cuts in the wrong positions with the right total length would pass | [V-SRC] `build-final-from-plan.mjs:183-209`; `verify-job-completion.mjs:139-158` | Medium–High |
| 8 | **Timeouts on very long cut loops.** Cut time grows faster than cut count (53 cuts 4.3 s; 874 cuts 819 s). The effective bridge ceiling is 1,200 s at the default, so a lecture with more than about 1,100 cuts, or a panel whose heartbeat stalls, would time out. A timeout then exits as `BRIDGE_EXECUTION_FAILED` (exit 1), not `PARTIAL_EDIT_STATE_UNKNOWN`, while Premiere is still cutting | [V-SRC] engine `:772-779`, `build-final-from-plan.mjs:138-176`; timing [V-SRC] `CONTROLLED_FULL_TEST`; ceiling [V-SRC] bridge source | Medium |
| 9 | Minor engine bugs: the schema version is compared as a string (`'10.0.0' < '2.1.0'` is true); `last_successful_cut_id` returns the *failed* cut's ID; the header says "Target ALL tracks" but the code targets V1/A1; NaN in bridge JSON is silently turned into 0 | [V-SRC] engine `:183, 815, 28-29, 434` | Low |
| 10 | **The only speech-clipping detector never runs unattended.** `diagnose-speech-tails.mjs` is not called by the runner | [V-RUN] grep of `ymnotes-runner.mjs` | Medium |
| 11 | **The silence threshold is an absolute −13.98 dBFS** (20 % amplitude, carried over from Filmora). `silencedetect` compares *each sample* against it, across interleaved channels, with no RMS and no hysteresis ([V-SRC] [`af_silencedetect.c`](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_silencedetect.c), research/03). So the edit depends on mic gain, and it is the 0.6 s minimum that actually protects quiet speech | [V-SRC] `config.silence_profile` | Medium (approved by ear; frozen) |
| 12 | **Two divergent state machines.** SKILL.md/`job-state.mjs` use S0–S15 (S7_FINAL …); the runner uses S1_PREFLIGHT–S17_SHORTS. SKILL.md also says the Shorts skill makes "two" Shorts, while v6 makes four | [V-SRC] `SKILL.md:69-101, 533-541`; runner handlers | Low (confusing during manual repair) |
| 13 | **The package is not self-contained.** The intro/outro MP4s are git-ignored / LFS and absent from the zip, so tests fail on a clean copy | [V-RUN] §2.7 | Low |
| 14 | **The export gate is thin for long lectures.** It checks duration ±1.0 s, the streams and 3 decoded frames. It does not compare audio and video stream durations, run a full decode, report loudness, or detect black/frozen frames (Shorts already uses `blackdetect`/`freezedetect`) | [V-SRC] `verify-export-file.mjs`; `config.export` | Medium |
| 15 | **Shorts uses `remove_from_timeline`,** which the host matrix marks UNSAFE for linked A/V (fixed upstream in 1.19.0). Its `--prompt-terms` goes into faster-whisper's `initial_prompt`, which slides out of context after the first windows; `hotwords` is re-sent every window | [V-SRC] `ymnotes-shorts.mjs:459-460`; faster-whisper `transcribe.py:1141-1187, 1542-1548` | Low–Medium |
| 16 | **Unofficial install source.** SKILL.md's "Download links" section points Premiere downloads to `filecr.com`, an unofficial redistribution site. Such installers carry a malware risk. A non-genuine install may also lack Creative Cloud services (updates, Speech-to-Text language packs, Enhance Speech, UXP updates) that several recommendations below assume. Install only from Adobe / Creative Cloud | [V-SRC] `SKILL.md:463` | High (security) |

**Strengths to preserve** (verified):

- SOURCE_BACKUP is immutable and a duplicated WORK sequence is the only thing cut.
- Exact BigInt tick math in the compiler.
- Descending cut order.
- A zero-generated-subclip invariant, checked against the project-item count.
- The branding adapter's normalized-unit conversion, plus region-based verification on the delivered MP4.
- The preset pinned by SHA-256.
- Export resume that never re-issues an export.
- A YouTube channel guard and duplicate guard.
- A resumable runner with a lock.
- A metadata validator.
- An explicit host-capability matrix with two dimensions: does it work on this host, and is it allowed for this job.

### 2.7 Test results (offline suites, scratch copy; no media or Premiere)

| Suite | Clean copy | With synthetic intro/outro stand-ins |
|---|---|---|
| `tests/run-tests.mjs` (aggregate) | 343 pass / 3 fail | **702 pass / 2 fail** |
| `tests/hardening-v2.mjs` | 131 / 0 | 131 / 0 |
| `tests/hardening-v3.mjs` | 358 / 1 (missing intro/outro asset) | 359 / 0 |
| `tests/autopilot.mjs` | 109 / 0 | 109 / 0 |

[V-RUN] Node 22.23.4 on Linux. The two remaining failures ("resume returns the same next state", "changed recordings invalidate silence + plan") are a **Linux-only artifact**: `normalizePath()` lowercases paths, and re-stat'ing the lowercased path fails on a case-sensitive filesystem. They are not a Windows defect, but they would break the skill if it were ever run on macOS or Linux with case-sensitive paths.

---

## 3. Comparison of serious candidates

"Adds" means capability beyond the current skill. "Data leaves machine" means footage or transcripts leave your computer.

| Candidate | What / how | Where installed | Win + PPro 26.3 | Interface type | Maintenance (2026-11-01) | License | Data leaves machine | Adds | Main risks |
|---|---|---|---|---|---|---|---|---|---|
| **`premiere-pro-mcp` 1.27.0** ([npm](https://www.npmjs.com/package/premiere-pro-mcp), [GitHub](https://github.com/leancoderkavy/premiere-pro-mcp)) | Same CEP file bridge you use; 522 tool definitions; optional UXP channel (token, 127.0.0.1:7777) | Both: npm global plus a CEP panel; sets `PlayerDebugMode` for CSXS 9–14, left in place on uninstall | CEP host 14.0+, UXP 25.6+ [V-SRC]; live-tested by the maintainer on 25.2.3 and 26.5.x, **not 26.3.2** [DOC] | Supported ExtendScript + unsupported QE (stills, razor batching) + optional UXP | 1.27.0 on 2026-10-31; 72 versions; 1 of 175 issues open; very high churn [V-RUN/V-SRC] | MIT | No (telemetry only if `POSTHOG_API_KEY` set) [V-SRC] | Asynchronous AME export (`export_sequence_job_start` / `get_export_job_status`); `export_sequence` `timeout_minutes` and `range:"in_to_out"`; fixes for `add_to_timeline_batch`, `remove_from_timeline`, `delete_sequence`, `export_frame`, `apply_edit_plan` validation; `ripple_remove_timeline_ranges`; idempotency keys; host lease | Breaking internal changes for your engine; churn; new tools are days old (`ripple_remove_timeline_ranges` stack-overrun fix landed 2026-10-31) |
| **Hardened in-house direct-cut engine** (yours) | One ExtendScript evaluation: setIn/OutPoint + `qeSeq.extract()` | Already installed | Proven on 26.3.2 | Unsupported QE DOM ("100% unsupported", Adobe engineer, [Dec 2025](https://community.adobe.com/feature-requests-730/request-for-timeline-editing-api-support-clip-track-movement-flattening-1621168)) | Yours | Yours | No | Already works; hardening adds checks | QE is unsupported; CEP retires Dec 2028/2029 |
| **faster-whisper** (+ bundled Silero VAD) ([GitHub](https://github.com/SYSTRAN/faster-whisper)) | CTranslate2 Whisper; word timestamps; `hotwords`; `BatchedInferencePipeline`; `faster_whisper.vad.get_speech_timestamps` (Silero, ONNX, no torch) | External; **already installed** (1.2.1) | Yes (CPU int8) | n/a (external) | Active; 1.2.1 on PyPI | MIT | No, once models are cached (`local_files_only=True`) | Lecture SRT/VTT, a speech-inside-cut guard, better term retention through `hotwords`, roughly 2× CPU speed with batching [DOC] | Arabic accuracy (turbo Egyptian WER 63.0 on the [OUA leaderboard](https://huggingface.co/spaces/elmresearchcenter/open_universal_arabic_asr_leaderboard)); English terms rendered in Arabic script |
| **Silero VAD v6** ([GitHub](https://github.com/snakers4/silero-vad)) | Neural voice-activity detection, 30 ms frames | External; already inside faster-whisper | Yes, CPU | n/a | v6.2.3, 2026-09-23 | MIT | No | Speech-presence check independent of gain | Breath and filler handling [UNK]; vendor's own metrics |
| **YouTube Data API `captions.insert`** ([docs](https://developers.google.com/youtube/v3/docs/captions/insert)) | Upload SRT/VTT as a caption track (draft or published) | External (your uploader) | n/a | Supported Google API | Stable | Google ToS | The caption text goes to YouTube (the video already does) | Lecture captions without Premiere | Needs the `youtube.force-ssl` scope (you currently consent to `youtube.upload` + `youtube.readonly`) [V-SRC] `youtube-upload.mjs:42-43`; 400 quota units per call |
| **auto-editor 31.8.0** ([GitHub](https://github.com/WyattBlue/auto-editor)) | Nim CLI; per-frame audio peak threshold; writes Premiere FCP7 XML with `<link>` groups and Premiere ticks | External single binary (unsigned) | Yes | XML interchange (supported import) | Very active (2026-10-29/31), one maintainer | Unlicense | No | A second-opinion detector and a reference XML writer | Also an absolute threshold (default about −28 dBFS); unsigned binary; no pip |
| **FCP7 XML / OTIO import into Premiere** | Generate the whole FINAL narrative externally; one atomic import | Nothing to install (own writer) or OpenTimelineIO (Python) | FCP7 XML imports natively; OTIO import/export "[Now Released]" ([Adobe](https://community.adobe.com/announcements-732/now-released-otio-import-and-export-311699)) | Supported import | OTIO v0.18.1 (2025-11-08) | Apache-2.0 (OTIO) | No | Linear-time builds; no QE; an exit path from CEP once UXP can import | OTIO's FCP7 adapter **writes no `<link>`** (A/V would import unlinked) [V-SRC research/03]; path encoding; fidelity on your host [UNK] |
| **Adobe UXP (Premiere 26.3)** ([docs](https://developer.adobe.com/premiere-pro/uxp/)) | Official JS plugin API; `executeTransaction` (undoable); markers; `EncoderManager` with progress events; transcript JSON import | Inside Premiere (panel; no headless plugins until 2027 [DOC]) | GA since 25.6 | Supported | Active; razor coming in 27.1 (beta) | Adobe | No | Long-term supported path; markers; export progress | **No razor/extract in 26.3**; no caption-track API; plugins cannot host servers without a hybrid C++ add-on [V-SRC research/02] |
| **whisper.cpp (Vulkan)** ([GitHub](https://github.com/ggml-org/whisper.cpp)) | ggml Whisper; integrated GPUs selectable since [PR #3492](https://github.com/ggml-org/whisper.cpp/pull/3492) | External | Needs a self-built Vulkan binary (no official Windows Vulkan zip) | n/a | Active (v1.9.x) | MIT | No | Possible iGPU speed-up ("3–4×" on a 680M/Arc, not your Vega 8) [DOC] | Unproven on a 5700U; slower than faster-whisper batched on CPU [DOC] |
| **ffmpeg audio chain** (`highpass`, `afftdn`/`arnndn`, `acompressor`, two-pass `loudnorm`) | Deterministic filters | External; already installed | Yes | n/a | ffmpeg | LGPL/GPL | No | Conservative lecture voice cleanup | Must not feed silence detection; needs approval by ear |
| **DeepFilterNet3** ([GitHub](https://github.com/Rikorose/DeepFilterNet)) | Neural speech denoiser, 48 kHz | External binary | Yes (prebuilt `deep-filter`) | n/a | **Stale**: last release 2023-08-31 | MIT/Apache | No | Stronger noise reduction than `afftdn` | Windows/PyPI issues; large-file reports; artifacts on speech |
| **hetpatel-11 `adobe-premiere-pro-mcp` 1.2.11** ([GitHub](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP)) | Same file-bridge design, 283 tools, AME queue export | Both | CEP 14.0+, verified on 26.0.2 [DOC] | ExtendScript + QE | Active | MIT | **Telemetry on by default** to the author's Cloudflare endpoint [V-SRC] | Little beyond 1.27.0 | Its bin name `premiere-pro-mcp` **collides** with yours |
| **mikechambers `adb-mcp`** ([GitHub](https://github.com/mikechambers/adb-mcp)) | UXP proof of concept, 26 Premiere tools | Both (Python MCP + Node proxy + UXP plugin) | 25.6+ | UXP | Mostly 2025 | MIT | No | A UXP reference design | **Proxy listens on :3001 on all interfaces, no auth** [V-SRC] |

---

## 4. Ranked shortlist

1. **The hardening patch to your own engine and gates (no install).** It closes verified defects #1–#10 and #14, raises confidence on every future run, and is a prerequisite for safely trying anything else. Cost: code and tests only.
2. **`premiere-pro-mcp` pinned at 1.27.0, piloted.** It removes the most fragile workarounds:
   - export blocking Premiere's script engine for the whole encode, plus 480 s bridge timeouts — replaced by an asynchronous job with status;
   - `delete_sequence` unavailable — the cause of the "ZZ_DISCARDED_" parking workaround;
   - `export_frame` unavailable — leaving no visual check before export;
   - unsafe `remove_from_timeline`, used by Shorts;
   - three uncoordinated writers — replaced by a host lease.
   It is ranked below the patch because it has not been tested on your host.
3. **A local captions stage** with faster-whisper (installed), `hotwords` plus a glossary, Silero VAD and YouTube `captions.insert`. This is the largest *new* capability for your use case, with no new runtime. Deliver captions as draft tracks first.
4. **The Silero VAD speech-inside-cut guard,** run through faster-whisper's bundled VAD. It is the independent cross-check the frozen amplitude profile lacks (#10, #11), and it reports without changing the approved edit.
5. **A post-export ffmpeg audio-cleanup remux** (optional, after a listening pass). It meets the "audio cleanup" need without touching the frozen timeline or the silence detection.
6. **An FCP7-XML build pilot** (your own writer, using auto-editor's `fcp7.nim` as a reference), as the planned successor to QE extract. It gives linear-time, atomic builds and an exit from QE.
7. **A UXP migration track** for 2027–2028, keyed to Adobe's razor APIs reaching general availability and the CEP disable date (Dec 2028).

## 5. Rejected alternatives

| Alternative | Why rejected |
|---|---|
| Replacing the cut engine with `ripple_remove_timeline_ranges` now | Introduced in 1.20.0, with a stack-overrun fix on 2026-10-31. It still uses QE internally, takes 50 ranges per call (so 874 cuts need chunking), and has no track record on your host. Re-evaluate after a pilot shows per-segment equivalence with your engine |
| Rewriting on UXP now | 26.3 has no razor or range extract; razor is 27.1 beta. UXP plugins cannot host a server without a hybrid C++ add-on. Headless plugins arrive in 2027 [DOC] |
| hetpatel-11 Premiere MCP | Telemetry on by default; binary-name collision; no capability beyond 1.27.0 |
| mikechambers adb-mcp / matrayu adobe-mcp | Proof of concept; 26 tools; unauthenticated proxy on all interfaces |
| ayushozha AdobePremiereProMCP | Not on npm; Go + Rust + Python + TS toolchain; tested only on 26.5.2 macOS |
| pymiere | GPL-3.0; "not maintained anymore"; tested up to 23.1; unauthenticated localhost HTTP eval |
| Adobe "Adobe for creativity" Claude connector | Cloud Express/Firefly-class operations; does not edit desktop Premiere projects [DOC] |
| Premiere Speech-to-Text / text-based "delete pauses" / auto captions | **No Arabic** in Adobe's transcript schema or STT languages ([feature request, v26](https://community.adobe.com/feature-requests-730/speech-to-text-in-arabic-not-supported-in-premiere-pro-26-1621281)); no API for pause deletion or auto-captioning [V-SRC research/02] |
| Premiere caption tracks for Arabic lecture captions | Repeated reports of reversed or unjoined Arabic ([2021](https://community.adobe.com/t5/premiere-pro-discussions/arabic-characters-not-joining-correctly-in-the-new-captioning-tool/td-p/11908308), [2025](https://community.adobe.com/t5/premiere-pro-discussions/srt-import-with-right-to-left-language-e-g-hebrew-arabic-text-is-reversed/m-p/15179344)); YouTube captions are simpler and searchable |
| Enhance Speech / Essential Sound automation | Local, but **no scripting API** [V-SRC research/02]; GUI-only, clip by clip |
| OpenTimelineIO's FCP7 adapter as the XML writer | Writes no `<link>` elements, so A/V would import unlinked [V-SRC research/03] |
| WhisperX, stable-ts | WhisperX's Arabic aligner can't time English words; its VAD downloads code at runtime. stable-ts was archived 2026-05-30 [V-SRC research/04] |
| ctc-forced-aligner default model, CrisperWhisper weights, TEN VAD | Non-commercial or restrictive licences — a risk for a monetized channel |
| Demucs, Resemble Enhance | Too slow on CPU (~90 min per lecture); generative (can alter speech); unclear weight licences |
| Cloud tools (Descript, Gling, OpusClip, Adobe Podcast, FireCut, ElevenLabs Scribe) | Footage or audio leaves the machine and recurring cost; not cleanly scriptable. Scribe was the best system on the [Clinera Egyptian medical benchmark](https://preprints.jmir.org/preprint/96222) (27.8 % WER) — revisit only if you accept cloud transcripts |
| ClipsAI | Abandoned (2024-01); English-only embeddings |
| Commercial jump-cut tools (AutoCut, TimeBolt, Recut) | No better than the current detector, not CLI-scriptable, and a licence to buy |
| OBS Source Record (separate webcam recording) | Mixed stability and sync reports ([forum](https://obsproject.com/forum/resources/source-record.1285)); the baked-in PiP is already handled by the Shorts layout detector |

---

## 6. Proposed architecture

```text
                               ┌────────────────────────────────────────────────────┐
 Claude Code (judgement only)  │ ymnotes-runner.mjs  (one detached process, lock,   │
  · exit-code handling ───────►│ state, resume)                                     │
  · metadata / caption review  │                                                    │
                               │  NEW S1b HOST_BINDING ── reads app.version + bridge│
                               │        version; mismatch ⇒ STOP (pilot required)   │
                               │  S4  silence (unchanged frozen profile)            │
                               │  NEW S4b VAD_GUARD ── faster_whisper.vad (Silero)  │
                               │        report speech-inside-removal (WARN/BLOCK)   │
                               │  S6  direct cuts (hardened engine, chunked,        │
                               │        fingerprint ON, rational fps, all tracks)   │
                               │  S8  edit gate: per-segment source in/out, 0-tick  │
                               │        tolerance, every track, full link audit     │
                               │  S10 export: export_sequence_job_start + status    │
                               │  S11 export gate + A/V stream parity, full decode, │
                               │        loudness report, black/freeze detect        │
                               │  NEW S11b AUDIO_FINISH (optional): ffmpeg chain,   │
                               │        remux video copy, re-verify                 │
                               │  NEW S12b CAPTIONS (optional): faster-whisper      │
                               │        FULL(+hotwords) → glossary fix → SRT/VTT    │
                               │        → Claude text review → captions.insert      │
                               └──────────────┬───────────────────────┬─────────────┘
                                              │ one client, one lease  │ local CLIs
                                              ▼                        ▼
                        premiere-pro-mcp (PINNED, e.g. 1.27.0)   ffmpeg · ffprobe · Python venv
                        file bridge ─► CEP panel ─► ExtendScript   (faster-whisper, Silero ONNX)
                                              │
                                              ▼
                                    Adobe Premiere Pro 26.3.2 (updates held until pilot passes)
                                              │
                               Future (2027–28): UXP plugin channel / XML import replaces QE
```

**Communication rules:**

1. All Premiere traffic goes through **one** bridge client per process, and the 1.27 host lease serializes processes.
2. The engine stops importing bridge internals once a pinned public tool proves equivalent. Until then it imports them only from the **pinned** version, and checks a hash of `file-bridge.js` at preflight.
3. Every mutation is followed by a structural read compared **per segment** with the plan.
4. Footage never leaves the machine. Transcript text goes to Anthropic only in the optional Claude review step, and caption text goes to YouTube, which already receives the video.

---

## 7. Prioritized improvement plan

| ID | Change | Fixes / opportunity | Benefit | Complexity | Compatibility | Risk |
|---|---|---|---|---|---|---|
| **P0-1** | Enforce host binding (new stage S1b) | #2 | Stops silent trust after a Premiere or bridge update | Low | All | Low |
| **P0-2** | Turn the fingerprint guard on in the runner | #1 | Refuses to cut a changed WORK timeline | Low | All | Low |
| **P0-3** | Exact rational frame rate end to end, plus a VFR preflight | #3 | Correct ticks at 29.97/59.94; early refusal of VFR | Low–Med | All | Low |
| **P0-4** | Per-segment, zero-tolerance edit verification on every track | #4, #5, #6, #7 | Proves *where* cuts landed, not only how much was removed | Medium | All | Low (read-only) |
| **P0-5** | Explicit track targeting plus a multi-stream preflight | #6 | No A2 desync | Low | All | Low |
| **P0-6** | Chunked cut loop, timeout sizing, correct classification | #8, #9 | No spurious failures on long lectures; progress | Medium | All | Medium (touches the engine — pilot) |
| **P0-7** | Run the speech-tail diagnostic in autopilot (warning) | #10 | The existing detector actually runs | Low | All | Low |
| **P0-8** | Stronger export gate | #14 | Catches A/V-length mismatch, corrupt mid-file, black/frozen frames | Low | All | Low |
| **P0-9** | Documentation consistency; remove the unofficial download link | #12, #16 | Fewer wrong manual repairs; security | Low | All | None |
| **P1-1** | Pinned `premiere-pro-mcp` upgrade (pilot first) | §2.3; host matrix entries | Async export, delete, export_frame, lease, idempotency | Medium | Win + 26.3.2 [UNK until pilot] | Medium |
| **P1-2** | Captions stage (S12b) | §2.5 captions gap | Lecture captions | Medium | Existing venv | Low–Med (accuracy) |
| **P1-3** | VAD guard (S4b) | #11 | Gain-independent speech check | Low–Med | Existing venv | Low |
| **P1-4** | Shorts: `hotwords` instead of `initial_prompt`; re-verify `remove_from_timeline` after the upgrade | #15 | Better term spelling; safer track cleanup | Low | Existing | Low |
| **P2-1** | Post-export audio finishing remux (S11b) | §2.5 audio gap | Cleaner voice, consistent loudness | Medium | ffmpeg | Medium (needs approval by ear) |
| **P2-2** | FCP7 XML build pilot | QE dependency; superlinear timing | Atomic, linear, supported import | Med–High | Win + 26.3.2 [UNK] | Medium |
| **P2-3** | Markers / chapter markers in Premiere from metadata | §2.5 | Chapters visible in the project | Low (after P1-1) | ExtendScript or UXP | Low |
| **P3-1** | UXP migration track | CEP retirement Dec 2028/2029 | Long-term support | High | 27.x | Medium |
| **P3-2** | whisper.cpp Vulkan benchmark on the 5700U | ASR speed | Possibly 2–4× faster | Low (benchmark) | Needs a self-built binary | Low |

**Essential:** P0-1 to P0-9, P1-1, P1-2. **Optional enhancements:** P1-3, P1-4, P2-x, P3-x. (P1-3 is cheap and strongly recommended.)

### 7.1 Draft changes (proposals only — not applied)

**P0-1 Host binding.** Add `scripts/lib/host-probe.mjs` and call it at S1 and again at the start of S6:

```js
// read-only probe through the same pinned bridge path the engine already uses
// (sendCommand + buildToolScript); no new MCP tool and no unsafe-script capability required
const probe = extractData(await sendCommand(buildToolScript(
  'return __result({ppro: app.version, build: app.build || null, ' +
  'qe: (function(){try{app.enableQE();return !!qe;}catch(e){return false;}})()});'), bridgeOptions));
const live = { premiere_version: probe.ppro, premiere_pro_mcp_version: mcp.serverInfo?.version, bridge: "cep" };
const check = hostMatches(live);              // existing function, finally given live data
if (!check.matches) stop("HOST_CHANGED_PILOT_REQUIRED", check.mismatches,
  "Run the disposable-project pilot (validation plan §9) and update premiere-host-capabilities.json.host");
assertWorkflowAllowed("qe_extract_direct_cut", "silence_removal", live);   // pass live everywhere
```

Draft SKILL.md text:
> **Host binding is enforced, not remembered.** S1 reads the live Premiere and bridge versions. If either differs from `premiere-host-capabilities.json → host`, the runner stops with `HOST_CHANGED_PILOT_REQUIRED` before any mutation. Never edit the `host` block by hand to make a job proceed; only a passing disposable pilot may update it.

**P0-2 Fingerprint.** In `ymnotes-runner.mjs` S6, before compiling:

```js
const fp = runScript("capture-timeline-fingerprint.mjs", ["--sequence-id", copy.id, "--out", ctx.art("work-baseline-fingerprint.json")]);
// then add: "--baseline-fingerprint", ctx.art("work-baseline-fingerprint.json")
// and fail the compile if plan.execution_readiness.stale_state_check !== "fingerprint_and_sequence_id"
```

The executor already contains the comparison logic (`buildLiveFingerprintPayload`). It only needs to be fed.

**P0-3 Rational frame rate.**

```js
// from get_sequence_settings: videoFrameRate.ticks (e.g. 8475667200)
const tpf = BigInt(settings.videoFrameRate.ticks);
const g = gcd(254016000000n, tpf);
const fpsNum = 254016000000n / g, fpsDen = tpf / g;      // 30000/1001 for 29.97
// pass --fps-num fpsNum --fps-den fpsDen ; planner frame_duration = fpsDen/fpsNum (rational)
// preflight: ffprobe r_frame_rate vs avg_frame_rate; mismatch > 0.1% ⇒ BLOCKER "VFR_SOURCE_TRANSCODE_REQUIRED"
```

**P0-4 Per-segment verification.** Add a read-only ExtendScript dump. It uses the same `clipData()` the engine already uses in its stale check, and returns, for **every** track, each clip's `start/end/inPoint/outPoint` ticks, media path, nodeId and linked-item count. Then compare against the expected FINAL layout derived from the keep plan:

```text
expected = []
t = 0
for rec in narrative_order:            # rec1, intro, rec2..N, outro
  if rec is fixed asset: expected.push({media: rec.path, srcIn: backup[rec].inTicks, dur: backup[rec].durTicks, tl: t}); t += dur
  else for keep in keep_plan[rec].keep_segments:
         srcIn = backup[rec].inTicks + keep.start_frame * tpf
         dur   = (keep.end_frame - keep.start_frame) * tpf
         expected.push({media: rec.path, srcIn, dur, tl: t}); t += dur
assert V1.length == A1.length == expected.length
for i: assert V1[i].start == expected[i].tl && V1[i].inPoint == expected[i].srcIn
          && V1[i].end - V1[i].start == expected[i].dur            # exact ticks, tolerance 0
          && A1[i] has identical start/end/inPoint/outPoint && linkedItems(V1[i]) includes A1[i]
for every other track: assert empty, except branding tracks after S7 (checked by coverage spans)
orphans = clips on any narrative track lacking a linked partner  → must be 0 (computed, never a literal)
```

Draft SKILL.md replacement for the overstated line:
> The edit gate compares **every** FINAL clip with the keep plan at **exact tick equality**: timeline start, source in, duration and A/V link partner. A one-tick difference fails. Every track is enumerated; any clip outside V1/A1 before branding fails `UNEXPECTED_TRACK_CONTENT`.

**P0-5 Track targeting.** In the engine script, before the loop: untarget **all** video and audio tracks, then target exactly `plan.target_tracks`. Read the targeting state back and abort with no cuts if it differs. At preflight, `ffprobe -show_streams` every recording; more than one audio stream means `MULTI_AUDIO_STREAM_UNSUPPORTED` until a pilot proves the multi-track case.

**P0-6 Chunked loop.** Split the descending cut list into batches of about 100. Each batch is one ExtendScript evaluation that performs the batch, then returns the new sequence end ticks and the clip count. Node checks the duration decreased by exactly the batch's frames before sending the next batch. Batches remain descending, so earlier coordinates stay valid.

- Timeout per batch: `max(120 s, 3 s × batch size)`.
- A timeout or bad delta at batch *k* is classified as `PARTIAL_EDIT_STATE_UNKNOWN` (exit 2), with `completed_batches = k-1`.
- Recovery is unchanged: rebuild WORK from SOURCE_BACKUP.
- Also fix #9: compare schema versions numerically, and report `last_successful_cut_id` from the last executed index.

**P0-7.** In S6, after a PASS build, run `diagnose-speech-tails.mjs` for each recording and record the counts in `FINAL_REPORT.md` as WARNING. No gate change, keeping the documented rule.

**P0-8 Export gate additions** (`verify-export-file.mjs`):

- Audio stream duration within 1 frame of video stream duration.
- `ffmpeg -v error -i out.mp4 -f null -` returns no decode errors. About 2–5 min for a 60-min 1080p file on your CPU [INF].
- `ebur128` integrated loudness and true peak, reported only.
- `blackdetect` / `freezedetect` over the lecture spans: warn on runs longer than 2 s.

**P1-2 Captions stage (S12b, off unless `config.captions.enabled`).** It respects the skill's "FULL needs authorization" rule by making that authorization a standing configuration choice.

```python
model = WhisperModel(MODEL, device="cpu", compute_type="int8", download_root=CACHE, local_files_only=True)
pipe  = BatchedInferencePipeline(model)
segments, info = pipe.transcribe(final_mp4, language="ar", batch_size=8, word_timestamps=True,
        vad_filter=True,
        initial_prompt=STYLE_PROMPT,            # Arabic sentence with Latin-script terms (style example)
        hotwords=" ".join(GLOSSARY + lecture_terms),
        append_punctuations="\"'.。,，!！?？:：”)]}、،؟")
# → glossary post-correction per word (keeps timestamps) → line breaking: ≤42 chars × 2 lines, ≤20 cps
# → captions.srt / captions.vtt in FINAL time (already FINAL time; never through the raw mapper)
# → Claude review: ONE pass over text only (fix ASR spelling, keep English terms Latin) → validator
# → youtube captions.insert (isDraft=true by default; language "ar"; name "Arabic + English terms")
```

- **Speed:** about 1× real time today; batched mode is roughly 2× faster in faster-whisper's own CPU benchmark [DOC]. Benchmark on your machine.
- **Model A/B:** `large-v3-turbo` against [`whisper-large-v3-turbo-egyptian-code-switching`](https://huggingface.co/mohammedaly22/whisper-large-v3-turbo-egyptian-code-switching) (MIT; needs a one-time CTranslate2 conversion; no published WER).
- **Scope:** the uploader needs the `youtube.force-ssl` scope — **a one-time re-consent**.

**P1-3 VAD guard (S4b).**

```python
from faster_whisper.audio import decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps
audio = decode_audio(recording, sampling_rate=16000)
speech = get_speech_timestamps(audio, VadOptions(threshold=0.5, min_silence_duration_ms=100, speech_pad_ms=30))
for r in removals_for(recording):                       # from keep-plan complement, source seconds
    ov = overlap_seconds(r, speech)
    if ov >= 0.150: block_or_warn("SPEECH_IN_REMOVAL", r, ov)   # default WARN; owner may promote
    elif ov >= 0.050: warn("SPEECH_EDGE_IN_REMOVAL", r, ov)
# also record noise-floor (p10 of 50 ms RMS) and speech level (p95) vs calibration; >6 dB off ⇒ WARN "GAIN_OUT_OF_CALIBRATION"
```

The thresholds are provisional; calibrate them on Digestive 04/05 with the owner listening. Never change `config.silence_profile` automatically. Estimated under 2 min per 60-min recording on CPU [INF].

**P2-1 Audio finishing (S11b, off by default).** Process only the delivered export:

```text
ffmpeg -i final.mp4 -af "highpass=f=75,afftdn=nr=10:nf=-45,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=200,loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=..:measured_TP=..:measured_LRA=..:measured_thresh=..:offset=..:linear=true"
       -c:v copy -c:a aac -b:a 320k final.clean.mp4
```

- Use two-pass `loudnorm`: measure first, then apply in linear mode.
- Then re-run `verify-export-file.mjs` on the new file, and verify the audio and video durations and a sync probe.
- The timeline and silence detection stay untouched.
- Turning it on is a versioned change under `PRODUCTION_RELEASE.md`, with an A/B listening pass.

**P2-2 XML pilot.**

- Write `scripts/build-final-xml.mjs`: FCP7 `xmeml` for the narrative only, `timebase 30 / ntsc FALSE`, percent-encoded `file://localhost/C:/…` paths, a `<link>` group per V/A clipitem, and Premiere ticks.
- Import it through `app.project.importFiles([xml])` / `app.openFCPXML()` into a disposable project.
- Compare the imported sequence **per segment** with the direct-cut FINAL, using the P0-4 dump.
- Adopt only after three lectures match exactly.

---

## 8. Prerequisites and installation steps (for later review only — do not run yet)

**Prerequisites:**

- Genuine Adobe Premiere Pro 2026 from Creative Cloud.
- Node ≥ 20.19.
- The existing faster-whisper venv.
- ffmpeg/ffprobe pinned in `config/local.json`.
- A Google OAuth client able to add the `youtube.force-ssl` scope.

**A. Freeze the baseline.**

1. In Premiere: *Help → About* — record the version. In Creative Cloud → Apps → Premiere → turn **auto-update off** until the pilot (§9) passes.
2. `npm ls -g premiere-pro-mcp` — record it (expected 1.14.1).
3. Copy the production repo folder. Tag it `v1.1-pre-audit` in its local git.

**B. Hardening patch (P0).** Implement it on a branch of the production repo. Run `node tests/run-tests.mjs` (expected: all pass on Windows), then run the §9 pilot before merging.

**C. Bridge upgrade (P1-1), only after B passes.**

1. Quit Premiere completely.
2. `npm install -g premiere-pro-mcp@1.27.0` — an exact version, never `@latest`.
3. `premiere-pro-mcp --install-cep` — reinstalls the matching panel. A mismatched panel refuses edits with `CEP_SCHEMA_INCOMPATIBLE` [V-SRC]. Note that this sets `HKCU\Software\Adobe\CSXS.9–14\PlayerDebugMode=1`, which persists.
4. Make sure the panel's temp-folder setting equals `PREMIERE_TEMP_DIR` (`C:\Users\hp\AppData\Local\Temp\premiere-mcp-bridge`) and that the folder is private to your user, because 1.27 enforces this.
5. Keep `PREMIERE_MCP_CAPABILITIES` at the default `inspect,edit,export,filesystem`. Do **not** enable `unsafe-script` for Claude's MCP server; the engine talks to the bridge directly.
6. Update `config/premiere-host-capabilities.json → host` **only after** the §9 pilot passes. Re-verify the UNSAFE/UNAVAILABLE entries (`add_to_timeline_batch`, `remove_from_timeline`, `delete_sequence`, `export_frame`, `work_area_only`) individually.
7. Rollback: `npm install -g premiere-pro-mcp@1.14.1`, then `premiere-pro-mcp --install-cep`.

**D. Captions (P1-2).**

1. No new Python package is needed; faster-whisper 1.2.1 is installed.
2. Optional A/B model: download once, then convert with `ct2-transformers-converter --model mohammedaly22/whisper-large-v3-turbo-egyptian-code-switching --output_dir <cache>\egy-cs-turbo-ct2 --quantization int8` (that converter needs `transformers` in a separate venv).
3. Add `youtube.force-ssl` to `youtube-upload.mjs` scopes and run `node scripts/ymnotes-runner.mjs authorize` once to re-consent.

**E. VAD guard (P1-3).** Nothing to install; it uses `faster_whisper.vad`.

**F. Optional:** whisper.cpp Vulkan. Build it with VS Build Tools + Vulkan SDK, `cmake -DGGML_VULKAN=1`, then run `whisper-bench`. No official Windows Vulkan binary exists [V-SRC research/04].

---

## 9. Validation plan (disposable test project)

**Setup:**

- A copy of one past lecture's recordings (e.g. Digestive 05) in `D:\YMnotes_Pilot\`.
- A new empty `Pilot.prproj`.
- A test YouTube upload in TEST mode, so it is PRIVATE with a prefixed title.
- Never the production project or channel visibility.
- Record every result in `pilot-results.json`.

| # | Test | Pass criterion | Fail criterion |
|---|---|---|---|
| V1 | Host probe | Reports Premiere 26.3.2 and the expected bridge version; a deliberate mismatch (edit the host block in the pilot copy) stops before any mutation with `HOST_CHANGED_PILOT_REQUIRED` | Any mutation happens on a mismatch |
| V2 | Fingerprint guard | Plan has `stale_state_check = fingerprint_and_sequence_id`. After manually nudging one WORK clip by 1 frame, the build returns `TIMELINE_STATE_CHANGED_REPLAN` and the project item count is unchanged | Cuts run on a modified WORK |
| V3 | Direct cuts, 30 fps | Per-segment dump equals the expected layout at 0-tick tolerance on every V1/A1 clip; orphans computed = 0; other tracks empty; project items before = after; SOURCE_BACKUP node IDs and ticks unchanged | Any tick difference, orphan, or SOURCE_BACKUP change |
| V4 | Negative test of the gate | Feed the gate a synthetic structure with one clip shifted 1 frame and one A1 clip offset 1 frame | Both must FAIL. PASS = defect not fixed |
| V5 | 29.97 fps | A short 29.97 CFR test recording compiles with 30000/1001 and passes V3 criteria; a VFR test file is blocked at preflight | Drift or VFR accepted |
| V6 | Multi-audio-stream file | A recording with two audio streams is blocked (`MULTI_AUDIO_STREAM_UNSUPPORTED`). Then run a separate explicit test of how QE extract treats untargeted, sync-locked A2, and record the result | Silent acceptance |
| V7 | Long loop | A synthetic plan with about 1,200 removals on a duplicated long sequence completes in batches; each batch's duration delta is exact; total delta 0; a forced timeout (tiny per-batch timeout) is reported as `PARTIAL_EDIT_STATE_UNKNOWN` with the batch index | Reported as generic FAIL, or a retry against the partial timeline |
| V8 | Bridge 1.27.0 equivalence | Same plan through the 1.14.1 build and the 1.27.0 build gives identical per-segment dumps; `delete_sequence` deletes a disposable sequence in a bin; `export_frame` writes a PNG; `remove_from_timeline` on a linked clip removes both A and V | Any mismatch keeps the entry UNSAFE |
| V9 | Async export | `export_sequence_job_start` → `get_export_job_status` reaches complete; the file passes `verify-export-file.mjs`; Premiere stays responsive to a read-only probe during the encode | Blocking, duplicate encode, or a failed gate |
| V10 | Export gate additions | Audio/video duration parity within 1 frame; full decode with 0 errors; loudness reported; a test file with 3 s of black inserted produces a WARNING | Missed defect |
| V11 | VAD guard | On Digestive 04/05: report produced in under 5 min per recording; every removal flagged ≥150 ms, checked by ear, is genuinely speech in at least 80 % of sampled cases (owner listening sample of 20) | Mostly false positives |
| V12 | Captions | SRT/VTT valid (no overlaps, ≤42 chars per line, ≤2 lines, ≤20 cps); Arabic renders correctly in YouTube's player; ≥90 % of a 30-term glossary appears in Latin script after correction; uploaded as a **draft** track to the PRIVATE test video; readback shows the track | RTL breakage, missing terms, publish without draft |
| V13 | Audio finishing (optional) | Integrated loudness −16 ±1 LUFS, true peak ≤ −1.5 dBTP, audio/video duration parity, blind A/B preferred by the owner | Audible artifacts, or the owner prefers the original |
| V14 | Regression | `node tests/run-tests.mjs` all green on Windows; a full runner pass on the pilot lecture ends `EDIT: PASS`, `EXPORT: PASS` with no new warnings beyond the expected VAD report | Any red gate |

---

## 10. Remaining uncertainties and how to resolve them

| Uncertainty | Why it matters | How to resolve |
|---|---|---|
| Current installed versions on your PC | Everything is bound to 26.3.2 + 1.14.1 as of September 2026 | Read-only: Premiere *Help → About*; `npm ls -g premiere-pro-mcp`; `node -v`; `ffmpeg -version`; list `%APPDATA%\Adobe\CEP\extensions` and `C:\Program Files (x86)\Common Files\Adobe\CEP\extensions`; `reg query HKCU\Software\Adobe\CSXS.12 /v PlayerDebugMode` |
| Whether your Premiere is a genuine Creative Cloud install | Affects updates, Speech-to-Text packs, Enhance Speech, UXP updates; malware risk | Check Creative Cloud desktop → Apps shows Premiere with your account |
| 1.27.0 behaviour on 26.3.2 | The maintainer's live tests cover 25.2.3 and 26.5.x | Validation V8–V9 |
| QE extract with untargeted sync-locked tracks | Possible A2 desync | V6 |
| Superlinear extract cost beyond 874 cuts | Long-lecture timing | V7 |
| `ripple_remove_timeline_ranges` equivalence | Could retire the private-import engine | Add to V8: same plan in 50-range chunks, compare dumps |
| FCP7 XML import fidelity (links, Arabic/encoded paths, about 1,800 clipitems) | Successor architecture | P2-2 pilot |
| Premiere's behaviour with OTIO linked A/V | Alternative interchange | Import an auto-editor `premiere-otio` export in the pilot project |
| Accuracy of Egyptian-Arabic/English-term ASR (turbo vs code-switching model) | Caption quality | V12 with a hand-checked 5-minute reference |
| Silero VAD on breaths and lecture room noise | Guard false positives | V11 |
| whisper.cpp Vulkan speed on Vega 8 | Faster captions | P3-2 benchmark |
| Whether 26.5 changes scripted in/out or extract behaviour | Auto-update risk | Keep updates off; pilot 26.5 in a disposable project before upgrading |
| Adobe's UXP razor GA date (27.1 beta now) | Migration timing | Watch the [UXP changelog](https://developer.adobe.com/premiere-pro/uxp/changelog/); re-evaluate in Q2 2027 |

---

## 11. What should I install or change first, why, and what would it let the skill do that it cannot reliably do now?

**Change first (no install): apply the P0 hardening patch.** That means:

- turn the fingerprint guard on;
- enforce the live Premiere and bridge version binding;
- use the exact rational frame rate;
- verify every cut **per segment at zero-tick tolerance on every track**;
- size, chunk and correctly classify the cut loop's timeouts;
- run the speech-tail check.

**Why:** today the skill can prove *how much* it removed, but not *where* the cuts landed. It cannot notice that Premiere or its bridge changed under it, and it disables its own stale-timeline guard in autopilot. Each of these is a silent-wrong-result path in code you already own, and fixing them needs no new software.

**What it unlocks:** a self-checking edit. Each lecture's timeline is proven to equal the approved cut plan clip by clip, and the skill refuses to cut after an unexpected update or a changed timeline. It also handles 29.97 or long recordings safely.

**Install first: `premiere-pro-mcp` pinned at exactly 1.27.0**, reinstalling its CEP panel, validated on a disposable project before production.

**Why:** it replaces the most fragile workarounds:

- an export that freezes Premiere's script engine and times out at about 480 s, replaced by an asynchronous Media Encoder job with real status;
- no way to delete a wrong sequence;
- no frame grab before export;
- unsafe linked-clip removal in Shorts;
- three uncoordinated writers on one bridge, replaced by a host lease.

**The capability that follows:** with both in place, the cheapest large new capability is **local lecture captions**. faster-whisper is already installed: add `hotwords`, a glossary and Silero VAD, then upload with YouTube `captions.insert` as drafts. It needs no new runtime, only a one-time `youtube.force-ssl` re-consent.

---

### Key sources (all accessed 2026-11-01)

- Adobe Developer Blog, CEP → UXP schedule: https://blog.developer.adobe.com/en/publish/2026/09/investing-in-the-future-of-creative-cloud-extensibility-uxp-comes-to-our-flagship-applications
- Premiere UXP reference and changelog: https://developer.adobe.com/premiere-pro/uxp/ppro-reference/ · https://developer.adobe.com/premiere-pro/uxp/changelog/
- Adobe UXP samples (razor "coming in 27.1"): https://github.com/AdobeDocs/uxp-premiere-pro-samples/commit/8d75ef1e7d76d08818696e7c9545fa8913b2d8f8
- Premiere ExtendScript guide (community-maintained, Adobe wording): https://ppro-scripting.docsforadobe.dev/
- QE DOM unsupported (Adobe engineer): https://community.adobe.com/feature-requests-730/request-for-timeline-editing-api-support-clip-track-movement-flattening-1621168
- OTIO import/export released in Premiere: https://community.adobe.com/announcements-732/now-released-otio-import-and-export-311699
- No Arabic Speech-to-Text (v26): https://community.adobe.com/feature-requests-730/speech-to-text-in-arabic-not-supported-in-premiere-pro-26-1621281
- `premiere-pro-mcp`: https://www.npmjs.com/package/premiere-pro-mcp · https://github.com/leancoderkavy/premiere-pro-mcp
- hetpatel-11 MCP: https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP · adb-mcp: https://github.com/mikechambers/adb-mcp · pymiere: https://github.com/qmasingarbe/pymiere
- ffmpeg silencedetect source: https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_silencedetect.c
- auto-editor: https://github.com/WyattBlue/auto-editor · OpenTimelineIO: https://github.com/AcademySoftwareFoundation/OpenTimelineIO · otio-fcp-adapter: https://github.com/OpenTimelineIO/otio-fcp-adapter
- faster-whisper: https://github.com/SYSTRAN/faster-whisper · Silero VAD: https://github.com/snakers4/silero-vad · whisper.cpp: https://github.com/ggml-org/whisper.cpp (iGPU PR #3492)
- Open Universal Arabic ASR leaderboard: https://huggingface.co/spaces/elmresearchcenter/open_universal_arabic_asr_leaderboard · Clinera benchmark: https://preprints.jmir.org/preprint/96222
- Egyptian code-switching Whisper: https://huggingface.co/mohammedaly22/whisper-large-v3-turbo-egyptian-code-switching
- YouTube captions.insert: https://developers.google.com/youtube/v3/docs/captions/insert
- DeepFilterNet: https://github.com/Rikorose/DeepFilterNet
- Adobe VFR FAQ: https://community.adobe.com/t5/premiere-pro/faq-variable-frame-rate-vfr-video/td-p/10348229
- Arabic caption issues in Premiere: https://community.adobe.com/t5/premiere-pro-discussions/arabic-characters-not-joining-correctly-in-the-new-captioning-tool/td-p/11908308 · https://community.adobe.com/t5/premiere-pro-discussions/srt-import-with-right-to-left-language-e-g-hebrew-arabic-text-is-reversed/m-p/15179344
- OBS Source Record: https://obsproject.com/forum/resources/source-record.1285

The detailed per-area findings, code excerpts and the remaining source links are in [`research/`](research/).
