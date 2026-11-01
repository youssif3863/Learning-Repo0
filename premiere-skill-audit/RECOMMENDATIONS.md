# YMnotes Premiere Skill — All Recommendations

**Compiled:** 2026-11-01 · **Review reminder:** 2026-11-11  
**Applies to:** `premiere-basic-video-workflow` v1.1 and `ymnotes-premiere-shorts` v6, on Windows · Premiere Pro 26.3.2 · `premiere-pro-mcp` 1.14.1  
**Source:** consolidated from [`PREMIERE_SKILL_AUDIT_2026-11-01.md`](PREMIERE_SKILL_AUDIT_2026-11-01.md). Evidence, file and line references, and source links are in that report and in [`research/`](research/).

Everything here is a **proposal**. Nothing has been installed or changed.

---

## The decision in one paragraph

Keep the current architecture: Claude Code → `ymnotes-runner.mjs` → `premiere-pro-mcp` CEP bridge → ExtendScript, with your direct-cut QE engine. It is production-proven (874 cuts, frame delta 0) and uses no mouse or coordinate automation in Premiere. Make three moves:

1. **Harden** the verification you already own.
2. **Upgrade** the bridge to a **pinned** version, after a disposable pilot.
3. **Add** a local captions stage.

Do **not** switch to UXP, XML import or another MCP server yet. Plan a UXP migration for 2027–2028: Adobe disables CEP by default in **Dec 2028** and removes it from new versions from **Dec 2029**.

---

## Priority overview

| # | Recommendation | Tier | Effort | Risk | Install needed |
|---|---|---|---|---|---|
| R1 | Enforce the live host/version binding | Essential | Low | Low | No |
| R2 | Turn the stale-timeline fingerprint guard on | Essential | Low | Low | No |
| R3 | Exact rational frame rate + VFR preflight | Essential | Low–Med | Low | No |
| R4 | Per-segment, zero-tolerance edit verification on every track | Essential | Medium | Low | No |
| R5 | Explicit track targeting + multi-audio-stream preflight | Essential | Low | Low | No |
| R6 | Chunked cut loop, timeout sizing, correct failure classification, engine bug fixes | Essential | Medium | Medium | No |
| R7 | Run the speech-tail diagnostic in autopilot | Essential | Low | Low | No |
| R8 | Stronger export gate | Essential | Low | Low | No |
| R9 | Documentation consistency + remove the unofficial download link | Essential | Low | None | No |
| R10 | Upgrade `premiere-pro-mcp` to **exactly 1.27.0**, after a pilot | Essential | Medium | Medium | Yes (npm + CEP panel) |
| R11 | Local lecture captions → YouTube draft captions | Essential | Medium | Low–Med | No (one OAuth re-consent) |
| R12 | Silero VAD "speech-inside-cut" guard | Strongly recommended | Low–Med | Low | No |
| R13 | Shorts: `hotwords` instead of `initial_prompt`; re-verify `remove_from_timeline` | Strongly recommended | Low | Low | No |
| R14 | Optional post-export audio finishing (ffmpeg remux) | Optional | Medium | Medium | No |
| R15 | FCP7 XML build pilot (future replacement for QE extract) | Optional | Med–High | Medium | No |
| R16 | Premiere markers from chapter metadata | Optional | Low | Low | No (after R10) |
| R17 | UXP migration track (2027–2028) | Optional / strategic | High | Medium | Later |
| R18 | whisper.cpp Vulkan benchmark on the Ryzen 5700U iGPU | Optional | Low | Low | Benchmark only |
| R19 | Hold Premiere auto-updates until the pilot passes | Essential (operational) | Low | None | No |

**Suggested order:** R19 → R9 → R1–R8 (one hardening patch) → pilot (§Validation) → R10 → R11 + R12 → R13 → optional items.

---

## Essential

### R1 — Enforce the live host/version binding

- **Problem:** the skill claims a Premiere or bridge version change downgrades every capability to UNVERIFIED. In code, `capabilityState()` only does that when a `live` argument is passed, and no caller passes one (`scripts/lib/host-capabilities.mjs:30-60`; `build-final-from-plan.mjs:49`). An automatic Premiere update would keep trusting QE extract silently.
- **Change:** add a read-only host probe at S1 and again before S6. Stop before any mutation on a mismatch.

```js
// same pinned bridge path the engine already uses; no new tool, no unsafe-script capability
const probe = extractData(await sendCommand(buildToolScript(
  'return __result({ppro: app.version, build: app.build || null, ' +
  'qe: (function(){try{app.enableQE();return !!qe;}catch(e){return false;}})()});'), bridgeOptions));
const live = { premiere_version: probe.ppro, premiere_pro_mcp_version: mcp.serverInfo?.version, bridge: "cep" };
const check = hostMatches(live);
if (!check.matches) stop("HOST_CHANGED_PILOT_REQUIRED", check.mismatches);
assertWorkflowAllowed("qe_extract_direct_cut", "silence_removal", live);   // pass `live` everywhere
```

- **SKILL.md text:**
  > **Host binding is enforced, not remembered.** S1 reads the live Premiere and bridge versions. If either differs from `premiere-host-capabilities.json → host`, the runner stops with `HOST_CHANGED_PILOT_REQUIRED` before any mutation. Never edit the `host` block by hand to make a job proceed; only a passing disposable pilot may update it.
- **Done when:** a deliberately mismatched host block stops the pilot run with zero Premiere mutations.

### R2 — Turn the stale-timeline fingerprint guard on

- **Problem:** the runner never passes `--baseline-fingerprint`, so plans record `stale_state_check: "sequence_id_only"` (`ymnotes-runner.mjs:643-646`). The executor already has the full comparison logic, but it is never fed.
- **Change:** after duplicating WORK, capture a fingerprint of the WORK timeline and pass it to `compile-timeline-cut-plan.mjs`. Refuse to build if the plan's `stale_state_check` is not `fingerprint_and_sequence_id`.

```js
runScript("capture-timeline-fingerprint.mjs", ["--sequence-id", copy.id, "--out", ctx.art("work-baseline-fingerprint.json")]);
// compile args += ["--baseline-fingerprint", ctx.art("work-baseline-fingerprint.json")]
```

- **Done when:** nudging one WORK clip by 1 frame makes the build return `TIMELINE_STATE_CHANGED_REPLAN`, with no cuts executed.

### R3 — Exact rational frame rate + VFR preflight

- **Problem:** the runner passes `--fps-num Math.round(fps) --fps-den 1` (`ymnotes-runner.mjs:645`). A 29.97 fps sequence would be cut with 30 fps ticks, about 3.6 s of drift per hour, and this is detected only *after* all cuts. OBS variable frame rate is not checked.
- **Change:**

```js
const tpf = BigInt(settings.videoFrameRate.ticks);          // e.g. 8475667200 for 29.97
const g = gcd(254016000000n, tpf);
const fpsNum = 254016000000n / g, fpsDen = tpf / g;          // 30000/1001
// pass fpsNum/fpsDen everywhere; planner frame duration = fpsDen/fpsNum (rational, not 1/fps float)
// preflight: ffprobe r_frame_rate vs avg_frame_rate; > 0.1% apart ⇒ BLOCKER "VFR_SOURCE_TRANSCODE_REQUIRED"
```

- **Done when:** a 29.97 CFR test file passes R4's checks exactly, and a VFR file is blocked at preflight.

### R4 — Per-segment, zero-tolerance edit verification on every track

- **Problems:**
  - The edit gate's `near()` tolerates **one frame** (`verify-job-completion.mjs:51-58`), although SKILL.md says one frame fails.
  - Orphans are written as a literal `[]` (`ymnotes-runner.mjs:710`).
  - Links are sampled for only 3 clips.
  - Only V1/A1 are checked.
  - Only the *total* length is compared, never *where* each cut landed.
- **Change:** a read-only ExtendScript dump of **every** track. For each clip it records start/end/inPoint/outPoint ticks, media path, nodeId and linked items. Compare it with the layout expected from the keep plan at **exact tick equality**:

```text
expected = []; t = 0
for rec in narrative_order:                       # rec1, intro, rec2..N, outro
  if fixed asset: expected += {media, srcIn: backup.inTicks, dur: backup.durTicks, tl: t}; t += dur
  else for keep in keep_plan[rec].keep_segments:
      srcIn = backup[rec].inTicks + keep.start_frame * tpf
      dur   = (keep.end_frame - keep.start_frame) * tpf
      expected += {media: rec.path, srcIn, dur, tl: t}; t += dur
assert len(V1) == len(A1) == len(expected)
for i: V1[i].start == expected[i].tl and V1[i].inPoint == expected[i].srcIn
       and V1[i].end - V1[i].start == expected[i].dur              # tolerance 0 ticks
       and A1[i] has identical start/end/in/out and is V1[i]'s link partner
all other tracks empty before branding (after branding: coverage-span check)
orphans = computed (never a literal) → must be 0
```

- **SKILL.md text** (replaces the overstated line):
  > The edit gate compares **every** FINAL clip with the keep plan at **exact tick equality** — timeline start, source in, duration and A/V link partner. A one-tick difference fails. Every track is enumerated; any clip outside V1/A1 before branding fails `UNEXPECTED_TRACK_CONTENT`.
- **Done when:** a synthetic structure with one clip shifted 1 frame **fails**, and a real pilot passes with 0 differences.

### R5 — Explicit track targeting + multi-audio-stream preflight

- **Problem:** the engine targets `V1`/`A1` but never untargets other tracks (`execute-timeline-cuts.mjs:709-720`), and nothing checks for a second audio stream (OBS multi-track). That could leave A2 out of sync.
- **Change:** in the engine, untarget **all** tracks, target exactly `plan.target_tracks`, read the state back, and abort with no cuts on a mismatch. At preflight, run `ffprobe -show_streams`; more than one audio stream gives `MULTI_AUDIO_STREAM_UNSUPPORTED` until a pilot proves the case.
- **Done when:** a two-audio-stream test file is blocked, and the targeting readback is recorded in `build-result.json`.

### R6 — Chunked cut loop, timeout sizing, correct classification, engine bug fixes

- **Problems:**
  - Cut time grows faster than cut count: 53 cuts took 4.3 s and 874 took 819 s.
  - The bridge's effective ceiling is 1,200 s with the default 300 s timeout, so lectures needing more than about 1,100 cuts, or a stalled panel heartbeat, time out.
  - A timeout exits as generic `BRIDGE_EXECUTION_FAILED` instead of `PARTIAL_EDIT_STATE_UNKNOWN`.
  - Minor bugs: the schema version is compared as a string; `last_successful_cut_id` reports the *failed* cut; NaN is turned into 0.
- **Change:**
  - Split the descending cut list into batches of about 100. Each batch is one ExtendScript call that returns the new sequence end ticks and clip count. Node checks that the duration decreased by exactly the batch's frames before sending the next batch.
  - Per-batch timeout = `max(120 s, 3 s × batch size)`.
  - A timeout or bad delta → `PARTIAL_EDIT_STATE_UNKNOWN` (exit 2), with `completed_batches`.
  - Recovery is unchanged: rebuild WORK from SOURCE_BACKUP, and never retry against a partial timeline.
  - Fix the three minor bugs.
- **Done when:** a synthetic plan of about 1,200 cuts completes with exact per-batch deltas, and a forced tiny timeout reports `PARTIAL_EDIT_STATE_UNKNOWN` with the batch index.

### R7 — Run the speech-tail diagnostic in autopilot

- **Problem:** `diagnose-speech-tails.mjs` exists but is never called by the runner, so no speech-clipping check runs unattended.
- **Change:** after a PASS build at S6, run it per recording and put the counts in `FINAL_REPORT.md` as **WARNING**. It does not become a gate.
- **Done when:** `FINAL_REPORT.md` shows the speech-tail counts for every recording.

### R8 — Stronger export gate

- **Problem:** `verify-export-file.mjs` checks only duration ±1.0 s, the streams and 3 decoded frames.
- **Change:** add these checks:
  1. Audio stream duration within 1 frame of the video stream.
  2. Full decode: `ffmpeg -v error -i out.mp4 -f null -` reports no errors.
  3. Integrated loudness and true peak from `ebur128`, reported only.
  4. `blackdetect` / `freezedetect` over the lecture spans: warn above 2 s.
- **Done when:** a test file with 3 s of black inserted produces a WARNING, and a clean export passes.

### R9 — Documentation consistency + remove the unofficial download link

- **Problems:**
  - SKILL.md/`job-state.mjs` number stages S0–S15 while the runner uses S1–S17.
  - SKILL.md says Shorts makes "two" Shorts; v6 makes four.
  - SKILL.md links Premiere downloads to `filecr.com`, an unofficial redistribution site. That is a malware risk, and a non-genuine install can lose Creative Cloud services: updates, Speech-to-Text packs, Enhance Speech, UXP updates.
- **Change:**
  - Add a mapping table between the two stage numberings, or retire the manual numbering.
  - Correct the Shorts count.
  - Replace the download section with: *"Install Premiere Pro only from Adobe Creative Cloud."*
  - Also note that intro/outro MP4s are not in the package (git-ignored/LFS), so tests on a clean copy fail.
- **Done when:** no stage name in SKILL.md is missing from the runner or the mapping, and no unofficial link remains.

### R10 — Upgrade `premiere-pro-mcp` to exactly 1.27.0, after a pilot

- **Why:** 1.14.1 is 58 releases old. 1.27.0 (2026-10-31, MIT) fixes all seven bridge defects your host matrix routes around, and adds:
  - **asynchronous Media Encoder export** — `export_sequence_job_start` + `get_export_job_status` — so Premiere's script engine no longer freezes for the whole encode, and there are no more 480 s timeouts;
  - `export_sequence` with `timeout_minutes` and `range: "in_to_out"`, replacing the ignored `work_area_only`;
  - working `delete_sequence`, `export_frame`, linked `remove_from_timeline`, a validated `apply_edit_plan` and `add_to_timeline_batch`;
  - a cross-process **host lease** (one writer at a time), idempotency keys and progress heartbeats.
- **Cautions:**
  - Very high churn: about 1,000 commits in two months, one maintainer.
  - Not live-tested by the maintainer on 26.3.2.
  - Your engine imports bridge internals. 1.27.0 keeps the files but adds a temp-folder privacy check, the lease (`HOST_LEASE_BUSY`), a 32-command queue limit, a 1 MiB response cap, and a panel-version match (`CEP_SCHEMA_INCOMPATIBLE`).
  - Do **not** adopt `ripple_remove_timeline_ranges` as the cut engine yet: it appeared in 1.20.0 and got a stack-overrun fix on 2026-10-31. First compare it against your engine in the pilot.
- **Change in the skill after upgrading:**
  - Export goes through `export_sequence_job_start` + `get_export_job_status`.
  - Re-test each UNSAFE/UNAVAILABLE matrix entry individually before marking it SAFE.
  - Hash `dist/bridge/file-bridge.js` at preflight, so a silent package change is caught.
- **Done when:** validation tests V8 and V9 pass (below).

### R11 — Local lecture captions → YouTube draft captions

- **Why:** captions are your biggest missing workflow.
  - Premiere cannot transcribe Arabic: no Arabic in Adobe's transcript schema or Speech-to-Text languages.
  - Its Arabic caption rendering has a history of reversed or unjoined text.
  - You already have faster-whisper 1.2.1, which bundles Silero VAD.
- **Change:** new optional stage **S12b CAPTIONS**, enabled by `config.captions.enabled`, which acts as the standing "FULL authorization".

```python
model = WhisperModel(MODEL, device="cpu", compute_type="int8", download_root=CACHE, local_files_only=True)
pipe  = BatchedInferencePipeline(model)
segments, info = pipe.transcribe(final_mp4, language="ar", batch_size=8, word_timestamps=True,
        vad_filter=True,
        initial_prompt=STYLE_PROMPT,              # Arabic sentence containing Latin-script English terms
        hotwords=" ".join(GLOSSARY + lecture_terms),
        append_punctuations="\"'.。,，!！?？:：”)]}、،؟")
# → glossary post-correction per word (timestamps preserved)
# → line breaking: ≤ 42 chars × 2 lines, ≤ 20 chars/second
# → captions.srt + captions.vtt in FINAL time (never through the raw-source mapper)
# → ONE Claude review pass over text only (fix ASR spelling, keep English terms in Latin script)
# → YouTube captions.insert, isDraft=true by default
```

- **Requirements:**
  - Add the scope `https://www.googleapis.com/auth/youtube.force-ssl` to `youtube-upload.mjs` (today it is `youtube.upload` + `youtube.readonly`), then re-consent once.
  - Each `captions.insert` call costs 400 quota units.
- **Model A/B:** `large-v3-turbo` against `mohammedaly22/whisper-large-v3-turbo-egyptian-code-switching` (MIT; one-time CTranslate2 conversion; no published WER).
- **Speed:** about 1× real time today; batched mode is roughly 2× faster in faster-whisper's own CPU benchmark. Benchmark on your machine.
- **Privacy:** audio stays local. Only transcript text goes to Claude (review step) and caption text to YouTube.
- **Done when:** validation test V12 passes.

### R19 — Hold Premiere auto-updates until the pilot passes

- **Why:** every capability verdict is bound to 26.3.2. The bridge changelog reports that 26.5.2 ignores scripted work-area changes.
- **Change:** Creative Cloud → Apps → Premiere Pro → turn auto-update off. Test any new Premiere version in a disposable project first.

---

## Strongly recommended

### R12 — Silero VAD "speech-inside-cut" guard

- **Problem:** the frozen silence profile is an absolute −13.98 dBFS threshold. ffmpeg `silencedetect` tests each sample against it, with no RMS and no hysteresis, so results depend on mic gain.
- **Change:** new stage **S4b VAD_GUARD**. It reports only, and never changes `config.silence_profile`.

```python
from faster_whisper.audio import decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps
audio  = decode_audio(recording, sampling_rate=16000)
speech = get_speech_timestamps(audio, VadOptions(threshold=0.5, min_silence_duration_ms=100, speech_pad_ms=30))
for r in removals_for(recording):
    ov = overlap_seconds(r, speech)
    if ov >= 0.150: warn("SPEECH_IN_REMOVAL", r, ov)          # owner may promote to BLOCK after calibration
    elif ov >= 0.050: warn("SPEECH_EDGE_IN_REMOVAL", r, ov)
# also: noise floor (p10 of 50 ms RMS) and speech level (p95) vs calibration; > 6 dB off ⇒ WARN "GAIN_OUT_OF_CALIBRATION"
```

- **Calibration:** calibrate the thresholds on Digestive 04/05 with the owner listening. Estimated under 2 min per 60-minute recording on CPU.
- **Done when:** validation test V11 passes.

### R13 — Shorts transcription and track-cleanup fixes

- **Problems:**
  - `--prompt-terms` is passed as `initial_prompt`, which faster-whisper slides out of context after the first windows.
  - Shorts calls `remove_from_timeline`, which your host matrix marks UNSAFE for linked A/V.
- **Change:**
  - Pass the glossary as `hotwords`, which is re-sent every window.
  - Add `،` and `؟` to `append_punctuations`.
  - Consider `large-v3` for 60 s Short windows, where speed is irrelevant.
  - After R10, re-verify `remove_from_timeline` and record the verdict in the matrix.
- **Done when:** English terms appear in Latin script more often in a Shorts A/B comparison, and the matrix entry is updated from a real test.

---

## Optional enhancements

### R14 — Post-export audio finishing (ffmpeg remux)

- **What:** process only the delivered export, never the timeline or the silence-detection input.

```text
ffmpeg -i final.mp4 -af "highpass=f=75,afftdn=nr=10:nf=-45,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=200,loudnorm=I=-16:TP=-1.5:LRA=11:<measured values from pass 1>:linear=true" -c:v copy -c:a aac -b:a 320k final.clean.mp4
```

- **Details:**
  - Use two-pass `loudnorm`, then re-run the export gate on the new file.
  - Alternatives to `afftdn`: `arnndn` (mix 0.8), or DeepFilterNet3 with attenuation limited to about 15 dB. DeepFilterNet has been stale since 2023.
  - Avoid `agate`, Demucs, Resemble Enhance and cloud enhancers.
- **Gate:** this is a versioned change under `PRODUCTION_RELEASE.md`, enabled only after a blind A/B listening pass.

### R15 — FCP7 XML build pilot

- **What:** write `scripts/build-final-xml.mjs`, which emits FCP7 `xmeml` for the narrative, with:
  - `timebase 30` / `ntsc FALSE`;
  - percent-encoded `file://localhost/C:/…` paths;
  - a `<link>` group per V/A clipitem;
  - Premiere ticks.
- Use auto-editor's `fcp7.nim` as a reference.
- **Do not** use OpenTimelineIO's FCP7 adapter: it writes no `<link>`, so A/V would import unlinked.
- **Test:** import into a disposable project and compare against the direct-cut FINAL using R4's per-segment dump.
- **Why:** atomic, linear-time, a supported import, no QE. A path off both QE and, later, CEP.
- **Adopt only if:** three lectures match exactly.

### R16 — Premiere markers from chapter metadata

After R10, write chapter markers into FINAL from `youtube-metadata.json`, so chapters are visible in the project. This works through ExtendScript markers now, or UXP markers later.

### R17 — UXP migration track (2027–2028)

- **Trigger:** Adobe's razor APIs reach general availability; they are "coming in 27.1 (beta)" now.
- **Hard limit:** CEP is disabled by default in Dec 2028.
- **Plan:**
  - Use `premiere-pro-mcp`'s UXP channel (token-authenticated, 127.0.0.1:7777) or a small own UXP panel that connects out to a local server. UXP plugins cannot host servers without a hybrid C++ add-on.
  - Put edits inside `executeTransaction`, so each change is one undo step.
  - Use `EncoderManager` progress events.
- **Re-evaluate:** Q2 2027.

### R18 — whisper.cpp Vulkan benchmark

whisper.cpp can use integrated GPUs since PR #3492. There is no official Windows Vulkan build, so build one with `-DGGML_VULKAN=1` and run `whisper-bench` on the Ryzen 5700U's Vega 8. Switch only if it clearly beats faster-whisper batched int8 on CPU.

---

## Do NOT do (rejected, with reasons)

- Replace the cut engine with `ripple_remove_timeline_ranges` now — too new, unproven on your host.
- Rewrite on UXP now — no razor or range extract in 26.3; no headless plugins until 2027.
- Use the hetpatel-11 Premiere MCP — telemetry on by default; its binary name collides with yours.
- Use mikechambers adb-mcp — its proxy listens on all network interfaces with no authentication.
- Use pymiere — unmaintained, GPL, unauthenticated local HTTP.
- Use the Adobe "Adobe for creativity" connector for editing — it does not edit desktop Premiere projects.
- Use Premiere Speech-to-Text, text-based "delete pauses" or auto-captions for these lectures — no Arabic.
- Use Premiere caption tracks for Arabic lecture captions — known RTL rendering bugs; YouTube captions are simpler.
- Use OpenTimelineIO's FCP7 adapter as the XML writer — no `<link>` elements.
- Use WhisperX or stable-ts — WhisperX's Arabic aligner can't time English words; stable-ts was archived in May 2026.
- Use non-commercially licensed models (ctc-forced-aligner default model, CrisperWhisper weights, TEN VAD) — risky on a monetized channel.
- Use Demucs or Resemble Enhance — too slow on CPU; generative.
- Use cloud tools (Descript, Gling, OpusClip, Adobe Podcast, FireCut) — footage leaves the machine, recurring cost, not scriptable.
- Use commercial jump-cut tools — no better than the current detector and not CLI-scriptable.

---

## Installation steps (for later — do not run before the hardening patch and pilot)

1. **Freeze the baseline:**
   - record the Premiere version (*Help → About*) and `npm ls -g premiere-pro-mcp`;
   - turn off Premiere auto-update;
   - copy the production repo and tag it `v1.1-pre-audit`.
2. **Hardening patch (R1–R9):** implement it on a branch, run `node tests/run-tests.mjs`, then the pilot.
3. **Bridge upgrade (R10):**
   1. Quit Premiere completely.
   2. `npm install -g premiere-pro-mcp@1.27.0` — an exact version, never `@latest`.
   3. `premiere-pro-mcp --install-cep` — reinstalls the matching panel. This sets `HKCU\Software\Adobe\CSXS.9–14\PlayerDebugMode=1`, which persists.
   4. Make sure the panel's temp folder equals `PREMIERE_TEMP_DIR` (`C:\Users\hp\AppData\Local\Temp\premiere-mcp-bridge`) and is private to your user.
   5. Keep `PREMIERE_MCP_CAPABILITIES` at the default. Do **not** enable `unsafe-script` for Claude's MCP server.
   6. Update `premiere-host-capabilities.json → host` only after the pilot passes.
   7. Rollback: `npm install -g premiere-pro-mcp@1.14.1`, then `premiere-pro-mcp --install-cep`.
4. **Captions (R11):**
   - nothing new to install;
   - add the `youtube.force-ssl` scope and run `node scripts/ymnotes-runner.mjs authorize` once;
   - optional model conversion: `ct2-transformers-converter --model mohammedaly22/whisper-large-v3-turbo-egyptian-code-switching --output_dir <cache>\egy-cs-turbo-ct2 --quantization int8`, in a separate venv with `transformers`.
5. **VAD guard (R12):** nothing to install; it uses `faster_whisper.vad`.

---

## Validation checklist (disposable pilot project only)

Use a copy of one past lecture in `D:\YMnotes_Pilot\`, a new empty `Pilot.prproj`, and TEST mode so any upload is PRIVATE.

- [ ] **V1** Host probe reports 26.3.2 + bridge version; a mismatched host block stops before any mutation.
- [ ] **V2** Fingerprint on; a 1-frame nudge to WORK gives `TIMELINE_STATE_CHANGED_REPLAN` and zero cuts.
- [ ] **V3** Per-segment dump equals the expected layout at **0 ticks**; orphans = 0 (computed); other tracks empty; project items unchanged; SOURCE_BACKUP unchanged.
- [ ] **V4** A synthetic 1-frame shift and a 1-frame A/V offset both **FAIL** the gate.
- [ ] **V5** A 29.97 CFR file compiles as 30000/1001 and passes V3; a VFR file is blocked.
- [ ] **V6** A two-audio-stream file is blocked. Also record how QE extract treats untargeted, sync-locked A2.
- [ ] **V7** About 1,200 synthetic cuts complete in batches with exact deltas; a forced timeout reports `PARTIAL_EDIT_STATE_UNKNOWN` + batch index.
- [ ] **V8** 1.14.1 and 1.27.0 builds give identical per-segment dumps; `delete_sequence` (in a bin), `export_frame` and linked `remove_from_timeline` work.
- [ ] **V9** The async export job completes, the file passes the export gate, and Premiere answers a read-only probe during the encode.
- [ ] **V10** Export gate: A/V parity within 1 frame; full decode clean; loudness reported; 3 s of black → WARNING.
- [ ] **V11** VAD guard: under 5 min per recording; at least 80 % of flagged removals (owner listening sample of 20) are genuine speech.
- [ ] **V12** Captions: valid SRT/VTT (no overlaps, ≤42 chars × 2 lines, ≤20 cps); Arabic renders correctly on YouTube; ≥90 % of a 30-term glossary in Latin script; uploaded as a **draft** to the PRIVATE test video.
- [ ] **V13** (Optional, R14) −16 ±1 LUFS, true peak ≤ −1.5 dBTP, A/V parity, owner prefers it in a blind A/B.
- [ ] **V14** `node tests/run-tests.mjs` all green on Windows; a full pilot run ends `EDIT: PASS`, `EXPORT: PASS`.

---

## Open questions to settle (read-only checks on your PC)

- **Current versions:**
  - Premiere *Help → About*;
  - `npm ls -g premiere-pro-mcp`, `node -v`, `ffmpeg -version`;
  - list `%APPDATA%\Adobe\CEP\extensions` and `C:\Program Files (x86)\Common Files\Adobe\CEP\extensions`;
  - `reg query HKCU\Software\Adobe\CSXS.12 /v PlayerDebugMode`.
- **Genuine Creative Cloud install?** Creative Cloud desktop → Apps should list Premiere under your account.
- **Still unknown, to be measured in the pilot:**
  - 1.27.0 behaviour on 26.3.2;
  - QE extract with sync-locked untargeted tracks;
  - extract timing beyond 874 cuts;
  - FCP7 XML / OTIO import fidelity;
  - Egyptian Arabic/English ASR accuracy;
  - Silero behaviour on breaths;
  - Vulkan speed on the Vega 8;
  - Adobe's UXP razor GA date.

---

## Review notes (fill in on 2026-11-11)

| Item | Decision (adopt / defer / reject) | Owner | Target date | Notes |
|---|---|---|---|---|
| Hardening patch R1–R9 | | | | |
| Bridge upgrade R10 | | | | |
| Captions R11 | | | | |
| VAD guard R12 | | | | |
| Shorts fixes R13 | | | | |
| Audio finishing R14 | | | | |
| XML pilot R15 | | | | |
| UXP track R17 | | | | |
