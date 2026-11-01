# 03 — Silence/pause editing, audio cleanup, timeline interchange, short-clip tools

Research date: 2026-11-01. Method: source code was cloned (read only, never executed) into
`/tmp/claude-0/-home-user-Learning-Repo0/3391813e-183a-5a64-8aab-0e6817637581/scratchpad/research/pkg-edit/`,
plus vendor docs, issue trackers and forums. The GitHub REST API was blocked in this session, so
repo activity comes from `git clone` and `git ls-remote` (commit and tag dates) and from public GitHub web pages.

Evidence labels:
- **VERIFIED-FROM-SOURCE (VFS):** I read it in the code or repo files at the commit named.
- **DOCUMENTED (DOC):** vendor or maintainer docs, a paper, or the official changelog says so.
- **INFERRED (INF):** my reasoning from the evidence. Not tested.
- **UNKNOWN (UNK):** no evidence found.

Target machine (given by the coordinator): Windows laptop, AMD Ryzen 7 5700U (8C/16T Zen 2, AVX2), 16 GB RAM,
AMD integrated GPU, **no CUDA**. Every speed figure below is weighted for CPU-only use.

---

## 0. Executive summary (decision-relevant)

1. **The current detector is a per-sample peak gate at −14 dBFS (VFS).** That makes it gain-dependent and asymmetric.
   It can delete quiet speech, and one click or cough can break up a real pause. Keep the approved profile, but add
   a **speech-inside-removal guard** that only reports and never edits. Use Silero VAD v6 (MIT, ONNX, CPU, about 1–3 min
   per 60-min lecture, INF) and optionally ASR word timestamps. Also add a **noise-floor-relative calibration
   check** for each recording. Details in §1.
2. **Interchange:** generating one **FCP7 XML** sequence (linked A/V, markers) and importing it once is structurally
   more robust than 300–900 QE-DOM ripple-extracts. QE is undocumented, ExtendScript support was documented only
   "through September 2026", and every extract is a separate stateful mutation. Generate the XML with your own
   small writer, or use auto-editor's writer. Do **not** use OTIO's `fcp_xml` adapter for this: it writes **no `<link>` elements**
   (VFS), so A/V would arrive unlinked. Premiere also imports `.otio` natively (DOC, with limits). auto-editor has
   a `premiere-otio` export (VFS). §3.
3. **auto-editor** (Unlicense, Nim, very active: 31.8.0 released 2026-10-29, commits 2026-10-31) is the strongest open tool.
   It ships a single unsigned Windows binary and writes Premiere FCP7 XML with `<link>` groups, `pproTicksIn/Out`
   and NTSC handling (VFS). Its `audio` method is also an **absolute peak per frame** (default 0.04 ≈ −28 dBFS), so it
   shares the gain-dependence problem. It has no VAD. It does have built-in whisper.cpp/Parakeet transcription and
   `--edit word/subtitle`. Use it as an XML writer or second opinion, not as a replacement detector. §2.
4. **Audio cleanup, conservative and CPU-friendly:** highpass 70–80 Hz → mild denoise (`afftdn` or
   DeepFilterNet3 with attenuation limit, or `arnndn` with mix < 1) → gentle compression or `speechnorm` → two-pass
   `loudnorm` to −16 LUFS / −1.5 dBTP. DeepFilterNet's binary runs about 0.19 RTF single-thread on a laptop i5 (DOC), so
   roughly 8–12 min for 60 min (INF). The project is **stale** (last release 2023-08-31, last commit 2024-09-25) and has
   Windows install issues. Its pre-built Rust `deep-filter` binary avoids Python. Demucs (about 1.5× real time on CPU, DOC)
   and Resemble Enhance (deepspeed dependency, built for GPUs) are **not suitable** here. Adobe Podcast is cloud
   upload. Premiere's Enhance Speech is local (DOC 2023) but cannot be scripted in a batch. §4.
5. **Captions/fillers for Egyptian Arabic:** Premiere's own Speech-to-Text reportedly does **not support Arabic**
   (DOC-community). Use whisper-family models locally. Whisper tends to drop fillers. CrisperWhisper 2.0 is
   multilingual verbatim, but its **weights carry a non-commercial licence** (VFS README), which blocks use on a monetised channel
   without a paid licence. §2.5.
6. **Shorts/highlights:** ClipsAI is abandoned (last commit 2024-01-17) and uses an **English-only** embedder
   (`all-roberta-large-v1`, VFS). Better options for this user: LLM selection over a timestamped Arabic transcript, plus a fixed
   crop layout, because the webcam is baked in. §5.

---

## 1. Coordinator's questions: the current silencedetect profile

Current frozen profile: `silencedetect=noise=0.2` (= 20·log10(0.20) = **−13.98 dBFS**), `d=0.6`, a 0.2 s buffer on each side,
and inward frame snapping.

### 1(a) How ffmpeg `silencedetect` computes its threshold — VFS

Source: `libavfilter/af_silencedetect.c` (FFmpeg master, fetched 2026-11-01:
https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_silencedetect.c).

- **Per-sample instantaneous amplitude. No RMS, no window, no hysteresis.** The macro tests each sample:
  `update(ctx, insamples, *p < noise && *p > -noise, ...)`. A sample counts as "silent" when |x| < noise.
- For integer formats, `noise` is scaled by `INT16_MAX` or `INT32_MAX` in `config_input`. Float formats compare directly.
  A `noise` of `-14dB` is converted to a linear ratio by the option parser, so 0.2 and −13.98 dB are equivalent.
- Silence begins only after `nb_samples_notify = duration × sample_rate × channels` **consecutive** silent samples.
  With the default `mono=0`, channels are interleaved into a single counter. **Any one sample on any channel at or above the
  threshold resets the counter** (`nb_null_samples = 0`) and, if silence was already running, ends it at that sample.
- `silence_start` is back-dated to the first silent sample of the run. `silence_end` is the first loud sample.

Consequences for this user (INF, from the code):
- **Gain dependence:** the decision depends on absolute peak level. Lower OBS mic gain, a different mic, or a voice that
  softens at sentence ends ("…يعني") can keep peaks under 0.2 for at least 0.6 s. That passage would be classified as silence and cut.
  Higher gain does the reverse and lets breaths and room noise count as "speech".
- **Fragile against transients:** one keyboard click, mouse click, desk knock or plosive that peaks above 0.2 splits a
  pause into two sub-0.6 s pieces. Neither piece is removed, so pauses next to clicks survive.
- **No smoothing:** speech has frequent low-amplitude samples (zero crossings) but rarely 0.6 s of *only*
  low-amplitude samples. The 0.6 s minimum is therefore what protects quiet speech, not the threshold.
- −14 dBFS is an unusually high gate. The default is 0.001 (−60 dB), and unsilence's default is −35 dB
  (VFS `unsilence/lib/detect_silence/DetectSilence.py:35`). It only works because the approved recordings are hot and fairly clean.

Alternatives inside ffmpeg:
- `silenceremove` supports `detection=avg|rms|peak|median|ptp|dev` with a `window` (default 20 ms, VFS
  `af_silenceremove.c` lines 142–149). It removes audio rather than reporting timestamps, so it is awkward as a planner input.
- Better: compute your own windowed RMS envelope from `ffmpeg -f f32le` PCM, or use `astats`/`ebur128` metadata. Then apply hysteresis
  (open threshold > close threshold) and minimum durations.

### 1(b) A non-destructive "speech-inside-removal" guard — feasible, recommended

Design (INF, built only from documented APIs):

1. Run **Silero VAD v6** (`pip install silero-vad[onnx-cpu]`, or call the ONNX model directly) on a 16 kHz mono extract:
   `get_speech_timestamps(wav, model, threshold=0.5, min_speech_duration_ms=250, min_silence_duration_ms=100, speech_pad_ms=30)`
   (these defaults are VFS in `src/silero_vad/utils_vad.py`). Output: a list of `{start,end}` sample offsets, which Claude writes as JSON.
2. For every planned removal range R = [a+buffer, b−buffer] after frame snapping, compute `speech_overlap_ms(R)`, the
   total intersection with VAD speech segments.
3. Rules. They report and never change the frozen profile automatically:
   - overlap ≥ 150 ms and the max VAD probability inside R ≥ 0.7 → **BLOCK**. Either shrink R to exclude the speech, or keep R
     entirely and list it for listening review.
   - 50–150 ms → **WARN** (often breath or lip noise. Silero is trained to reject non-speech noise, but breath handling is UNK).
   - the reverse check: kept segments with less than 5 % VAD speech over at least 2 s → **CANDIDATE CUT**, reported only. These catch
     fan noise or keyboard typing that is louder than −14 dBFS.
4. Optional second witness: **ASR word timestamps** (faster-whisper `word_timestamps=True`, or auto-editor
   `whisper --split-words --format json`). Any word whose midpoint lies inside R raises a BLOCK. Words are the strongest
   evidence of content loss, but Whisper timestamps can drift by about 100–300 ms (INF), so use word *midpoints* and a tolerance.

Why Silero (DOC, Silero's own wiki, so not independent: https://github.com/snakers4/silero-vad/wiki/Quality-Metrics):
multi-domain ROC-AUC is 0.97 for v6 against 0.73 for WebRTC VAD. On noisy sets (VoxConverse) it is 0.94 against 0.65. The wiki
calls WebRTC "pretty poor at separating speech from noise". The README claims training on 6000+ languages, under 1 ms per 30 ms chunk on
one CPU thread, MIT licence, latest tag v6.2.3 (2026-09-23), and commits as recent as 2026-10-22 (VFS git).
CPU cost for 60 min (INF): about 112k chunks × under 1 ms ≈ under 2 min single-thread, faster with ONNX/batching. That fits the 5700U easily.
Caveats: it runs at 16 kHz with about 32 ms resolution. Whispered or very soft speech may score below 0.5, so tune the
threshold down to 0.35–0.4 for the guard (a guard should err toward BLOCK).

Other VADs:
- `py-webrtcvad` (MIT): last commit 2021-02-15 (VFS) and no Windows wheels in the original package.
  Weak against noise (above). Not recommended.
- `pyannote.audio` segmentation: heavier. It needs PyTorch, and its models are gated on Hugging Face behind a token. Its strength is diarisation,
  which is unnecessary for one speaker. INF: overkill.
- ffmpeg 8's `whisper` filter has `vad_model`/`vad_threshold`/`vad_min_silence_duration` options (VFS
  `af_whisper.c` lines 486–499). It needs an ffmpeg build linked with whisper.cpp. Whether common Windows builds include it is UNK.

### 1(c) Noise-floor-relative thresholds

Recommended per-recording calibration (INF; standard practice, not a specific tool):
1. Compute the RMS in 50 ms windows over the whole file (ffmpeg PCM → numpy, or `auto-editor levels`).
2. Noise floor N = 10th percentile of window dBFS. Speech level S = 95th percentile.
3. Threshold T = N + max(6 dB, 0.35·(S−N)), with hysteresis: close at T, reopen at T+3 dB.
4. **Use it as a check on the frozen −14 dBFS profile first:** if (S − 14 dB) < 6 dB, or the frozen
   threshold sits below N+6 dB, flag the recording as "gain out of approved envelope" before cutting. Optionally run
   loudness normalisation before detection, which turns the absolute threshold into a relative one. The current pipeline
   already computes EBU R128 gain per source, so applying it *before* silencedetect is a cheap way to cut gain dependence. The approved
   profile would then need re-approval by ear.

---

## 2. Silence / pause / jump-cut tools

### 2.1 auto-editor — https://github.com/WyattBlue/auto-editor

| Item | Finding | Label |
|---|---|---|
| Language | **Nim** (`ae.nimble`: `requires "nim >= 2.2.2"`), with C/Swift/JS pieces. It is no longer Python | VFS |
| License | **Unlicense** (public domain). Release binaries "may be under various open source licenses" because they bundle FFmpeg and codecs | VFS LICENSE, README |
| Maintenance | Tags 31.0.0 (2026-06-17) … 31.7.0 (2026-10-02), **31.8.0 (2026-10-29)**. Commits on 2026-10-31. Very active, single main maintainer (bus-factor risk) | VFS git |
| Install (Windows) | Download the binary from GitHub Releases and rename it to `auto-editor.exe`. **Unsigned** ("Unknown developer" warning). No longer on pip. Building from source needs WSL | DOC https://auto-editor.com/installing |
| Where it runs | External CLI. Premiere is not touched until you import the XML | VFS |
| Methods | `audio` (threshold default 0.04, per stream/channel), `motion` (downscale+blur frame diff, with ROI x/y/w/h), `blackdetect`, `subtitle`/`regex`, `word`; combined with `or/and/xor/not` | VFS `src/editmethods.nim` |
| How `audio` works | "loudest sample in a timebase section, divided by the max value": an **absolute peak per frame** (1/30 s at 30 fps). Same gain dependence as silencedetect, but per 33 ms frame | VFS `editmethods.nim`, `analyze/audio.nim` |
| Margins | `--margin 0.2sec` default, asymmetric `0.3s,1.5sec` allowed | DOC README |
| Premiere export | `--export premiere` → FCP7 XML (`.xml`). `--export premiere-otio` → `.otio` | VFS `conductor.nim`, `exports/fcp7.nim`, `exports/otio.nim` |
| Linked A/V | Writes `<link><linkclipref>` groups tying each video clip to its aligned audio clips, with trackindex/clipindex; unique ids across tracks | VFS `fcp7.nim` lines 276–308, 588–712 |
| Frame rate / NTSC | `setTbNtsc`: 24000/1001→(24,TRUE), 30000/1001→(30,TRUE), 60000/1001→(60,TRUE); other non-integer rates are truncated with ntsc FALSE. 30 fps CFR → (30,FALSE) | VFS |
| Premiere-exact times | Writes `pproTicksIn/Out` (since 31.8.x) | VFS CHANGELOG, `fcp7.nim:161` |
| pathurl on Windows | `handlePath` = absolute path with `\`→`/`, **no `file://` prefix and no percent-encoding** | VFS `fcp7.nim:506–511` |
| Audio channels | Writes `channelcount`, `sourcetrack/trackindex`. Fix #1139 (May 2026): mono sources no longer exported one-sided | VFS; issue list |
| Transcription | `auto-editor whisper <file> <ggml model>` (whisper.cpp; Whisper or Parakeet models), `--format srt/json`, `--split-words` | VFS `skills/auto-editor-transcribe/SKILL.md`, `src/transcribe.nim` |
| Agent skills | Ships Claude-style `skills/` (export, transcribe, effects, transitions); `npx skills add WyattBlue/auto-editor` | VFS |
| Open Premiere issues | Searching "premiere" gives 70 results, **all closed or merged** at fetch time. History includes #449 "Premiere don't show the Cuts", #439 "voice channels are disabled", #440 lagging, #448 Resolve pathurl backslash (fixed). #857 fixed a major Premiere-export performance regression (Nov 2025) | DOC https://github.com/WyattBlue/auto-editor/issues?q=premiere |
| Security | Unsigned binary from GitHub. Verify checksums and pin the version. No network use except optional yt-dlp URLs and Apple speech | DOC/INF |

How Claude Code would call it:
`auto-editor lecture.mp4 --edit audio:-14dB --margin 0.2s --export premiere:name="L07" -o L07.xml`,
or `--export v3 -o L07.v3` to get a JSON timeline Claude can parse and diff against its own planner.
`auto-editor levels lecture.mp4` dumps per-frame loudness for calibration.
Added capability: a tested Premiere XML writer with links and ticks, a motion method (possibly useful with an ROI on the slide area
to keep pauses while slides change, INF), and built-in transcription.
Limitations: no VAD and no RMS mode, so it is no smarter than the current detector. It is a different implementation, so a parity risk exists against the
approved-by-ear profile. Releases are frequent, so pin a version. A single maintainer.

### 2.2 Other open-source cutters

| Tool | URL | Mechanism (VFS) | Maint. | Verdict |
|---|---|---|---|---|
| jumpcutter | https://github.com/carykh/jumpcutter | Per-frame max abs amplitude **normalised by the file's max** (`--silent_threshold 0.03` of peak); renders a new video | last commit 2021-04-27 | Abandoned. Renders only, no XML. Reject |
| unsilence | https://github.com/lagmoellertim/unsilence | Wraps ffmpeg `silencedetect` (default −35 dB, 0.5 s); renders, with optional speed-up of silent parts instead of cutting | last commit 2023-01-16, tag 1.0.9 | Stale. Same detector as now. Reject |
| Silero-VAD-based scripts | various small repos | VAD → ffmpeg concat | mostly hobby | Build the guard yourself (§1b) instead |
| auto-editor | above | peak/frame + motion | very active | Best open option |

### 2.3 Commercial tools (brief)

| Tool | Where it runs | Pricing (approx., 3rd-party or vendor 2026; verify) | Footage leaves machine? | Premiere path |
|---|---|---|---|---|
| TimeBolt | Desktop app (Win/Mac) | Lifetime ~$247–$347; Pro ~$97/yr (sources conflict) | Reviewer says fully local (INF) | XML export (paid tier) |
| Recut | Desktop app (Win/Mac) | **$129 one-time** or $15/mo (DOC https://getrecut.com) | UNK (desktop app) | "Export an XML" (DOC) |
| AutoCut | Premiere/Resolve extension | Basic (Silences only) $6.6/mo or $79/yr; AI $14.9/mo (DOC https://www.autocut.com/en/pricing/) | UNK. AI features likely server-side (INF) | Inside Premiere |
| FireCut | Premiere/Resolve plugin | ~$10–$34/mo, 25 h audio/month cap (3rd-party) | Cap suggests server processing (INF) | Inside Premiere |
| Gling | Desktop app + cloud AI | ~$15–$40/mo, hour-metered (3rd-party) | Likely uploads (INF/UNK) | XML export (DOC gling.ai) |
| Descript | Desktop app + cloud | Hobbyist $16–24, Creator $24–35/user/mo; media-minute model since Sep 2025 (3rd-party) | **Yes**, cloud transcription and storage (DOC-general) | Timeline export (UNK detail) |

INF: none of these is scriptable by Claude Code as cleanly as a CLI. The extensions need GUI interaction. Arabic-specific
filler and pause handling is unverified for all of them.

### 2.4 Native Premiere option

Text-Based Editing can find pauses and filler words for deletion (DOC-community, Adobe announcement thread
https://community.adobe.com/announcements-732/now-in-beta-filler-words-and-other-text-based-editing-updates-in-premiere-pro-313483).
**Arabic is reportedly not supported by Premiere Speech-to-Text** (open feature request
https://community.adobe.com/t5/idea-premiere-pro/speech-to-text-in-arabic/idi-p/13515504). Not viable for Egyptian Arabic lectures (DOC-community).

### 2.5 Fillers ("umm", "يعني", "إيه") and breaths

- Whisper and faster-whisper (MIT) give word timestamps but are trained toward clean transcripts and often **omit fillers** (INF, widely reported).
  Egyptian Arabic plus English medical terms is a code-switching case; test accuracy before relying on it (UNK).
- **CrisperWhisper 2.0** (https://github.com/nyrahealth/CrisperWhisper, tags v2.0.3, commits 2026-09-22): verbatim
  mode transcribes `[um]`, `[uh]`, repetitions and cut-offs with word timestamps. It claims multilingual support (10-language benchmark, by the vendor).
  The **code is MIT, but the standard weights use the Nyra *non-commercial research* licence. Pro weights are commercial only** (VFS README §License).
  A monetised YouTube channel or paid-student platform is commercial use, so a licence is required. CPU speed of the large model on a 5700U: slow (INF). The CT2 runtime helps.
- Breaths: no reliable open breath detector was found (UNK). Practical options are VAD-negative gaps of 150–500 ms with
  energy above the noise floor, or high-pass energy bursts (INF). Recommend leaving breaths inside buffers (sounds natural) rather than cutting them.
- CPU ASR throughput on a 5700U (INF, benchmark before committing): faster-whisper `medium`/`large-v3-turbo` int8
  runs on the order of real time to a few times faster on 8 cores. `large-v3` is slower than real time. auto-editor's Parakeet backend is fast, but
  Parakeet v3 covers European languages and Arabic support is UNK.

---

## 3. Timeline interchange (OTIO / FCP7 XML) vs the ExtendScript QE loop

### 3.1 OpenTimelineIO core — https://github.com/AcademySoftwareFoundation/OpenTimelineIO

| Item | Finding | Label |
|---|---|---|
| Latest release | **v0.18.1 (2025-11-08)**, v0.18.0 (2025-11-06). Main branch active (commits 2026-10-30, bundle fixes) | VFS git |
| Python | `python_requires >3.9`; classifiers 3.9–3.15; "OS Independent"; wheels include Windows (DOC PyPI, INF) | VFS setup.py |
| License | Apache-2.0 | VFS |
| Adapters | Since 0.17 the core ships only otio_json/otiod/otioz. FCP7 XML, FCPXML, AAF and CMX are separate plugin packages | VFS `adapters/` dir |
| `url_from_filepath` | `urllib.parse.unquote(PurePath(p).as_uri())` → `file:///C:/My Folder/x.mp4`, **un-encoded** | VFS `url_utils.py` |

Adapter maintenance (VFS git):

| Adapter | Latest tag | Last commit | Status |
|---|---|---|---|
| otio-fcp-adapter (FCP7 XML) https://github.com/OpenTimelineIO/otio-fcp-adapter | v1.0.0 | 2026-04-08 | Lightly maintained |
| otio-fcpx-xml-adapter https://github.com/OpenTimelineIO/otio-fcpx-xml-adapter | v1.0.0 | 2024-06-25 | Dormant |
| otio-aaf-adapter https://github.com/OpenTimelineIO/otio-aaf-adapter | v2.0.0 | 2026-09-21 (dependabot) | Maintained |
| otio-cmx3600-adapter https://github.com/OpenTimelineIO/otio-cmx3600-adapter | v1.0.0 | 2025-12-12 | Lightly maintained |

**Critical finding — the fcp_xml adapter does not write linked A/V (VFS).** The only occurrence of "link" in
`src/otio_fcp_adapter/fcp_xml.py` is line 428, `default_ignore_keys = {"timecode", "rate", "link"}`. Links are dropped on
read and never emitted on write. The README feature matrix: markers ✔, audio tracks ✔, transitions ✖, effects ✖, speed ✖.
`_build_rate` writes `timebase=ceil(fps)` and `ntsc = FALSE if rate == fps else TRUE` (VFS line 1307–1323), which is fine for 30.0.
`pathurl` = `target_url` verbatim (line 1479), so you must supply a well-formed URL.
→ An OTIO → FCP7 XML → Premiere route gives **unlinked** video and audio clips (INF from code). Ripple and trim behaviour in
Premiere then differs from what the user expects. Not recommended without post-processing to inject `<link>` elements.

### 3.2 Premiere's native OTIO import

Adobe announced OTIO import/export in the Premiere beta in Oct 2024 ("Now Released" announcement
https://community.adobe.com/announcements-732/now-released-otio-import-and-export-311699). It carries clip names, placement, source in/out,
timecode, fps, multiple tracks, track names, linear speed and sequence markers. Known gaps: sequence settings from non-Premiere OTIO
"may not transfer automatically", OTIOZ/OTIOD are not supported, and a 2026 report says speed keyframes are not preserved (DOC-community). Adobe's release notes
list OTIO import/export, but which version made it GA could not be pinned (UNK; helpx returned 403). auto-editor's `premiere-otio`
exporter states "Premiere can import and export .otio files" (VFS `exports/otio.nim` header). Whether OTIO import keeps A/V **linked**
in Premiere is UNK. Test it.

### 3.3 FCP7 XML pitfalls (for any generator)

| Pitfall | Detail | Label |
|---|---|---|
| pathurl | Premiere itself writes `file://localhost/...` with percent-escapes (example in Adobe forum). auto-editor writes a bare `C:/...`. Unicode or Arabic filenames historically needed percent-escaping in FCP (Apple pro-apps-dev 2007). **Recommendation:** use ASCII-only media paths, or emit `file://localhost/C:/...` with RFC 3986 percent-encoding, and test both once | DOC/INF |
| timebase/ntsc | 30 fps CFR → `<timebase>30</timebase><ntsc>FALSE</ntsc>`. 29.97 → 30/TRUE. Confirm OBS output with ffprobe `r_frame_rate` vs `avg_frame_rate` (VFR guard) | VFS auto-editor / INF |
| Audio channel mapping | Stereo AAC from OBS: Premiere may show 2 mono tracks or 1 stereo track depending on `channelcount`/`sourcetrack`. auto-editor had bugs here (#439 disabled channels, #1139 one-sided mono) | DOC issues |
| Links | Must emit `<link>` for V and A clipitems (clipindex/trackindex) or clips import unlinked | VFS |
| Sequence settings | Premiere builds a sequence from XML `<format>/<samplecharacteristics>`. Verify 1920×1080, 30p, 48 kHz after import | INF |
| Precision | Frame-based in/out loses sub-frame audio precision. `pproTicksIn/Out` (254016000000 ticks/s) restores exactness | VFS auto-editor |
| Disabled or missing clips | Cause apparent "drift" in forum reports | DOC-community (Adobe forum threads) |
| Scripted import | ExtendScript `app.openFCPXML(path, projPath)` and `app.project.importFiles([xml])` are documented. An old (2017) report of errors exists | DOC https://ppro-scripting.docsforadobe.dev/application/application.html |

### 3.4 Is XML import more robust than the QE ripple-extract loop for 300–900 cuts? — Yes, with a validation step (INF)

| Criterion | QE DOM extract loop (current) | Generated FCP7 XML / OTIO |
|---|---|---|
| API status | QE DOM is **undocumented/unsupported**. ExtendScript documented "through September 2026" (DOC scripting guide); UXP GA in 25.6 (DOC changelog) | XML import is a long-standing user feature; OTIO import is newer |
| Number of state mutations | 300–900 ripple operations on a live sequence. A failure mid-way leaves a partial edit | 1 import of a pre-computed cut list. Atomic from the user's point of view |
| Determinism and verification | Must re-read the sequence after edits to verify | The XML is a file Claude can diff, lint and unit-test before import. After import, re-export the XML and compare clip in/out |
| Speed | O(N) extracts, each rippling all later clips (INF: minutes) | One import (INF: seconds to tens of seconds for ~1–2k clipitems; no benchmark found) |
| Frame accuracy | Depends on QE time-string handling | Exact frames plus ticks |
| Linked A/V | Preserved (operates on existing clips) | Only if the generator writes `<link>` (auto-editor yes, OTIO adapter **no**) |
| Branding and effects added later | Keeps the project | Imports as a new sequence. Do branding (intro/outro/overlays) **after** import via ExtendScript/UXP, or append in XML |
| Risks | Hangs and crashes, undocumented behaviour changes | Offline media (pathurl), channel mapping, sequence-preset mismatch, duplicate master clips/bins |

Recommendation (INF): keep the planner as the single source of truth, emit an FCP7 XML from its keep-list (own writer modelled on
auto-editor's `fcp7.nim`, or run auto-editor with `--edit` driven by a pre-computed v3 timeline), import it with `app.openFCPXML`/`importFiles`,
then run a verification pass (re-export or enumerate clips, then compare). Keep the QE loop as a fallback until parity is shown on 2–3 lectures.

---

## 4. Audio cleanup (local, scriptable)

### 4.1 Tool table (CPU = Ryzen 7 5700U, 60-min lecture)

| Tool | Local/cloud | License | Est. CPU time, 60 min | Quality evidence | Artifact risk on speech | Maint. |
|---|---|---|---|---|---|---|
| ffmpeg `highpass`, `lowpass` | local | LGPL/GPL | seconds | DSP basics | none at 70–80 Hz | active |
| ffmpeg `afftdn` (FFT denoise, nr/nf/tn noise tracking) | local | LGPL | ~1–2 min (INF) | stationary noise only | "watery"/musical noise if nr > ~12 dB | active |
| ffmpeg `arnndn` (RNNoise; `model=`, `mix=` −1..1) | local | BSD model + LGPL | ~1 min (INF, RNNoise is tiny) | general-purpose; needs a `.rnnn` model file (GregorR rnnoise-models) | can gate soft syllables. Use `mix=0.7–0.85` | ffmpeg active; xiph/rnnoise v0.2, last commit 2025-02-22 (VFS) |
| ffmpeg `agate` | local | LGPL | seconds | — | chops word tails. **Avoid** for lectures | — |
| ffmpeg `deesser` | local | LGPL | seconds | — | lisping if aggressive | — |
| ffmpeg `dynaudnorm` / `speechnorm` / `acompressor` / `compand` | local | LGPL | seconds–1 min | — | pumping or raised noise floor in pauses if aggressive | — |
| ffmpeg `loudnorm` two-pass (I, TP, LRA, `measured_*`, `linear=true`) | local | LGPL | 2 × decode pass | EBU R128 | none in linear mode | — |
| **DeepFilterNet3** https://github.com/Rikorose/DeepFilterNet | local | **MIT or Apache-2.0** | RTF 0.19 single-thread on i5-8250U (DOC paper https://arxiv.org/abs/2305.08227) → ~8–12 min (INF) | PESQ 3.17 VoiceBank+DEMAND (DOC paper) | over-suppression of soft consonants at full strength. Use `--atten-lim` (e.g., 12–18 dB) | **stale**: v0.5.6 2023-08-31, last commit 2024-09-25 (VFS). Open #704 PyPI/torchaudio-soundfile on Windows; #497 large-file failure on Windows (DOC issues) |
| Resemble Enhance https://github.com/resemble-ai/resemble-enhance | local | MIT | very slow on CPU (INF; CFM generative enhancer) | demo-level | **generative**: can hallucinate or alter timbre and words | last commit 2024-12-03; `deepspeed` in requirements (hard on Windows) (VFS) |
| Demucs v4 (vocals isolation) https://github.com/adefossez/demucs | local | MIT code; **weights licence unclear / possibly NC** (VFS README) | ~**1.5× duration** on CPU → ~90 min (DOC README) | music separation, not speech denoise | music-trained; phasey speech | maintained fork, commit 2026-10-26 |
| Adobe Podcast Enhance Speech (web) | **cloud upload** | proprietary | upload-bound | strong, popular | over-processed "studio" sound; v2 adds strength control | Free ~30 min/file, Premium ~$9.99/mo, 2 h/file (3rd-party, verify) |
| Premiere **Enhance Speech** (Essential Sound) | **local** ("performs locally… no internet connection required", DOC 2023 announcement https://community.adobe.com/announcements-732/now-released-enhance-speech-in-premiere-pro-313485) | bundled | per clip, GUI | good; has a Mix Amount slider | same family as Podcast; trained mainly on English per user claim (UNK) | Adobe |

Notes:
- The DeepFilterNet `deep-filter` pre-built binary needs **48 kHz WAV** input (VFS README line 46). Its Python package needs PyTorch.
  For 60-min files, split into 5–10 min chunks with 1 s overlap to avoid the large-file failure (INF from #497).
- RNNoise and DeepFilterNet both run at 48 kHz frames. Resample explicitly to avoid surprises.
- Arabic speech: none of the denoisers is language-specific (they model speech spectra), so risk is similar to English (INF).

### 4.2 Recommended conservative lecture voice chain (INF)

Process extracted audio (WAV 48 kHz) and re-attach it, or apply as clip-level replacement audio. Never denoise *before* silence detection
unless the detector is re-approved.

```
# pass 1 (measure)
ffmpeg -i in.wav -af "highpass=f=75,afftdn=nr=10:nf=-50:tn=1,acompressor=threshold=-24dB:ratio=2.5:attack=15:release=200:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json" -f null -
# pass 2 (apply, linear)
ffmpeg -i in.wav -af "highpass=f=75,afftdn=nr=10:nf=-50:tn=1,acompressor=...,loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=..:measured_TP=..:measured_LRA=..:measured_thresh=..:offset=..:linear=true" -ar 48000 out.wav
```
- If the room or fan noise is non-stationary, replace `afftdn` with `deep-filter --atten-lim 15` (DeepFilterNet3) or
  `arnndn=m=<model>.rnnn:mix=0.8`. A/B test 60 s excerpts by ear (the user's approval-by-ear process).
- Skip `agate`, Demucs and Resemble Enhance. Use `deesser` only if sibilance is audible.
- Read results: `loudnorm` prints JSON (Claude parses `input_i`, `output_i`, `target_offset`). Verify with
  `ffmpeg -af ebur128=peak=true` on the output.

---

## 5. Short-clip extraction / highlight detection

| Tool | URL | What it does (VFS) | Maint. | Fit for Egyptian-Arabic lectures |
|---|---|---|---|---|
| ClipsAI | https://github.com/ClipsAI/clipsai | whisperX transcription → TextTiling over **`all-roberta-large-v1`** sentence embeddings → clip boundaries (15–900 s); resize via pyannote diarisation + face detection (facenet-pytorch, mediapipe) + scenedetect | last commit **2024-01-17**, tag 0.2.1, MIT | **Poor**: English embedder; pyannote needs an HF token; heavy torch stack; abandoned |
| OpusClip | opus.pro | cloud highlight and reframe | commercial | **Cloud upload**; Arabic quality UNK; pricing UNK (subscription) |
| Premiere Auto Reframe | built in | local reframing | Adobe | Works, but tracks the dominant subject (INF) |
| OpenCV YuNet / MediaPipe face detection | opencv_zoo / google mediapipe (Apache-2.0) | per-frame face boxes on CPU | active | The webcam overlay is **baked in at a fixed position**, so face tracking finds the small webcam face. A **fixed crop template** (slide region + webcam region stacked 9:16) is simpler and deterministic (INF) |

Recommendation (INF): for highlights, have Claude rank segments from a timestamped transcript (whisper or faster-whisper JSON,
Arabic plus English terms) and cut with fixed layout templates. This matches the existing `ymnotes-premiere-shorts` skill's approach. Use
face detection only to verify the webcam box position once per recording.

---

## 6. Integration sketch for Claude Code (INF)

1. `ffmpeg -i lecture.mp4 -ac 1 -ar 16000 -f wav vad.wav` → `python -I vad_guard.py vad.wav plan.json > guard.json`
   (Silero ONNX). Claude reads `guard.json` (BLOCK/WARN/CANDIDATE lists) before running the edit step.
2. Calibration: an RMS percentile script prints `{noise_floor_db, speech_p95_db, margin_db, in_envelope: bool}`.
3. Edit: the planner keep-list → FCP7 XML (linked A/V, ticks, percent-encoded `file://localhost` pathurl) → ExtendScript
   `app.openFCPXML` → verify by enumerating clips. Fallback is the QE loop.
4. Audio: a two-pass loudnorm chain on the extracted WAV. Optional DeepFilterNet binary. Re-import as replacement audio.
5. Captions: faster-whisper or auto-editor whisper → SRT/JSON. Human review for Arabic medical terms.

---

## 7. Sources (primary)
- FFmpeg silencedetect source: https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_silencedetect.c ; silenceremove: …/af_silenceremove.c ; whisper filter: …/af_whisper.c ; arnndn: …/af_arnndn.c
- auto-editor repo, CHANGELOG, `src/exports/fcp7.nim`, `src/exports/otio.nim`, `src/editmethods.nim`: https://github.com/WyattBlue/auto-editor ; installing: https://auto-editor.com/installing ; issues: https://github.com/WyattBlue/auto-editor/issues?q=premiere
- OTIO: https://github.com/AcademySoftwareFoundation/OpenTimelineIO ; FCP adapter: https://github.com/OpenTimelineIO/otio-fcp-adapter
- Premiere OTIO: https://community.adobe.com/announcements-732/now-released-otio-import-and-export-311699
- Premiere scripting guide (openFCPXML; ExtendScript through Sept 2026): https://ppro-scripting.docsforadobe.dev/application/application.html ; UXP changelog: https://developer.adobe.com/premiere-pro/uxp/changelog
- Silero VAD: https://github.com/snakers4/silero-vad ; metrics: https://github.com/snakers4/silero-vad/wiki/Quality-Metrics
- DeepFilterNet: https://github.com/Rikorose/DeepFilterNet ; paper: https://arxiv.org/abs/2305.08227 ; Windows issues: https://github.com/Rikorose/DeepFilterNet/issues?q=is%3Aissue+windows
- RNNoise: https://github.com/xiph/rnnoise ; Demucs: https://github.com/adefossez/demucs ; Resemble Enhance: https://github.com/resemble-ai/resemble-enhance
- CrisperWhisper: https://github.com/nyrahealth/CrisperWhisper ; ClipsAI: https://github.com/ClipsAI/clipsai
- jumpcutter: https://github.com/carykh/jumpcutter ; unsilence: https://github.com/lagmoellertim/unsilence ; py-webrtcvad: https://github.com/wiseman/py-webrtcvad
- Premiere Arabic STT request: https://community.adobe.com/t5/idea-premiere-pro/speech-to-text-in-arabic/idi-p/13515504 ; Enhance Speech local: https://community.adobe.com/announcements-732/now-released-enhance-speech-in-premiere-pro-313485
- Commercial: https://getrecut.com ; https://www.autocut.com/en/pricing/ ; https://firecut.ai/pricing/premiere-pro ; https://www.gling.ai ; TimeBolt/Descript pricing via third-party pages (https://clipjury.pages.dev/reviews/timebolt, https://sonix.ai/resources/descript-pricing/), verify on the vendor sites.
