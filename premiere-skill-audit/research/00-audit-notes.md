# Audit notes (own verification) — 2026-11-01

Audit target: uploaded premiere-basic-video-workflow.skill_1.zip == synced skill copy (diff: only .gitattributes/.gitignore/.graphifyignore extra in zip). 131 files, 4.4 MB. Shorts skill (ymnotes-premiere-shorts v6) read from synced copy.

## Environment (from skill evidence/config — not live-inspected; no computer attached)
- win32, Premiere Pro 26.3.2 (host-capabilities.json observed 2026-09-04), premiere-pro-mcp 1.14.1, CEP file-bridge, PREMIERE_TEMP_DIR C:\Users\hp\AppData\Local\Temp\premiere-mcp-bridge
- AMD Ryzen 7 5700U, 15.3 GiB RAM, AMD Radeon iGPU, no CUDA (LOCAL_TRANSCRIPTION_BENCHMARK 2026-09-03)
- Python 3.12.10 venv C:\Users\hp\.codex\venvs\premiere-transcription; faster-whisper 1.2.1 / CTranslate2 4.8.2; large-v3-turbo CPU int8 RTF≈1.01; SCAN used model `small` in controlled test
- Node (process.execPath), ffmpeg/ffprobe (WinGet build; npm shim earlier on PATH)
- Codex also uses the skill via junction; Claude Code uses `premiere` MCP server + graphify-premiere
- Shorts: opencv-python-headless, numpy, pillow, arabic-reshaper, python-bidi; YuNet ONNX face model

## Communication path (verified from source)
- Agent ad-hoc: Claude Code MCP server `premiere` (premiere-pro-mcp) -> file bridge -> CEP panel -> ExtendScript.
- Runner/scripts: scripts/lib/mcp-client.mjs spawns its own stdio premiere-pro-mcp (hardcoded default C:/Users/hp/AppData/Roaming/npm/node_modules/premiere-pro-mcp/dist/index.js), protocol 2024-11-05, 120 s default timeout (runner uses 600 s).
- Cut engine: engine/direct-cut/execute-timeline-cuts.mjs imports premiere-pro-mcp PRIVATE internals dist/bridge/file-bridge.js (sendCommand) and dist/bridge/script-builder.js (buildToolScript, escapeForExtendScript) and sends raw ExtendScript with app.enableQE(), seq.setInPoint/OutPoint(ticks), qeSeq.extract(). Default timeout 300000 ms; build-final-from-plan does not pass --timeout-ms.
- No mouse/coordinate automation in any Premiere step. UI automation only: e-teaching.site (Flutter canvas, screenshot+coordinates via Claude in Chrome) and Shorts Stage B social uploads (Chrome).

## Verified defects / overstated claims
1. Fingerprint stale-timeline guard disabled in production: runner calls compile-timeline-cut-plan.mjs without --baseline-fingerprint (ymnotes-runner.mjs:643-646) -> stale_state_check = "sequence_id_only".
2. Host version binding never enforced: host-capabilities.mjs only degrades to UNVERIFIED if a `live` arg is passed; no caller passes it (build-final-from-plan.mjs:49 assertWorkflowAllowed without live; upload-route.mjs:32). No script reads app.version or MCP serverInfo version for comparison. A Premiere auto-update silently keeps QE extract "VERSION_VALIDATED".
3. Frame rate forced to integer/1: runner passes --fps-num Math.round(sb.fps) --fps-den 1 (runner:645); fpsFromSettings = 254016000000/ticks. A 29.97 (30000/1001) sequence would be compiled as 30/1 -> ticks per frame 8467200000 vs true 8475667200 -> cumulative drift ~0.1% (≈3.6 s/hour) in cut positions; would surface only as a nonzero frame delta AFTER cuts were applied. 59.94 likewise. Planner input frame_duration_seconds = 1/fps (float).
4. Edit gate tolerance is ONE FRAME, not zero: verify-job-completion.mjs near() default tolerance = oneFrame (+1e-9) for A/V start/end and V1 contiguity. SKILL.md claims "Any orphan, gap, or one-frame A/V mismatch fails the edit" — a one-frame A/V offset or one-frame gap passes the V1/A1 span checks (frame-count total still exact).
5. Orphans not computed in runner path: S8_EDIT_QC writes `orphans: []` literal (runner:710); get_clip_links sampled for 3 clips only (first/middle/last) out of hundreds.
6. Only V1/A1 inspected. Extract targets only plan.target_tracks = [V1, A1] (config.narrative_order); other tracks are never explicitly untargeted. Gate checks only V1/A1. A recording with a second audio stream (OBS multi-track) or any other targeted/sync-locked track is unverified -> possible silent desync on A2.  (Premiere behaviour of untargeted sync-locked tracks under QE extract: UNKNOWN — test.)
7. Total-duration-only correctness: gate compares total frames + V1/A1 alignment; it never checks per-segment source in/out against the keep plan. A wrong-position cut set with the same total would pass (e.g., offset drift).
8. [CORRECTED after reading premiere-pro-mcp 1.14.1 file-bridge.js: while the CEP panel refreshes busy_<id>.json the bridge keeps waiting up to max(4 x timeoutMs, 120 s) = 1200 s for the 300 s default, so the 819 s run fit. Residual risk: loops > ~1200 s or a stalled busy marker.] Executor timeout misclassification: on bridge timeout executor exits 1 (BRIDGE_EXECUTION_FAILED) not 2; build-final then treats it as generic FAIL, reads inventory/structure (queued behind still-running ExtendScript). Controlled full test: 874 cuts took 819 s (> 300 s default). Real risk for long lectures. Recovery message would be wrong ("FAIL" vs "PARTIAL_EDIT_STATE_UNKNOWN").
9. Minor engine bugs: schema version compared as string ('10.0.0' < '2.1.0'); last_successful_cut_id returns the FAILED cut id; header comment says "Target ALL tracks" but code targets V1/A1; extractData replaces NaN with 0.
10. Speech-tail diagnostic never invoked by autopilot runner (grep: no call), so the only speech-clipping detector does not run in unattended production.
11. Silence threshold -13.98 dBFS (20% amplitude, Filmora heritage). Absolute, gain-dependent; diagnostic thresholds "calibrated against one recording".
12. Two divergent state machines: SKILL.md/job-state.mjs S0..S15 (S7_FINAL etc.) vs runner S1_PREFLIGHT..S17_SHORTS. SKILL.md says Shorts makes "two" Shorts; Shorts v6 makes four.
13. Package not self-contained: intro/outro MP4 excluded (.gitignore/LFS) -> run-tests.mjs 343/346 on clean copy; with synthetic stand-ins 702/704; remaining 2 failures = Linux case-sensitivity artifact (normalizePath lowercases paths, fingerprint re-stat fails) — not a Windows defect. hardening-v2 131/131, hardening-v3 359/359 (with stand-ins), autopilot 109/109.
14. export verification: duration ±1.0 s, streams, 3 decoded frames. No audio-vs-video stream duration check, no full decode, no loudness report, no black/freeze detect (Shorts has blackdetect/freezedetect).
15. Shorts uses remove_from_timeline (host-matrix UNSAFE for linked A/V) on carrier/SFX audio tracks; per-caption PNG stills + per-keyframe MCP calls (hundreds of bridge round trips); captions are images, not caption tracks.
16. SKILL.md "Download links": Premiere from filecr.com (unofficial redistribution site) — security + licensing concern; affects CC services (Speech to Text, Enhance Speech, updates).

## What works (verified by evidence + code)
- Assembly, SOURCE_BACKUP immutability, duplicate WORK, direct-cut silence removal (874 cuts, delta 0), branding with normalized-unit adapter + frame-region verification, canonical preset with SHA-256 pin, export polling across bridge timeout, metadata SCAN, YouTube resumable upload with channel guard, resumable runner with lock.
## Not supported at all
- Captions/subtitles for lectures; audio cleanup (noise reduction, EQ, compression, Enhance Speech); markers; chapter markers in Premiere; graphics beyond one PNG mark; webcam overlay manipulation (baked into OBS); multicam; J/L cuts; filler-word removal.
