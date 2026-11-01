# 02 — Adobe official APIs for Premiere 26.x: UXP vs ExtendScript/QE vs native features

Research date: 2026-11-01. Target: **Premiere (Pro) 26.3.2 on Windows**. The product was renamed back to "Adobe Premiere" with 26.0 (Jan 2026, per Wikipedia; DOCUMENTED). Adobe docs now say "Premiere", not "Premiere Pro".

## Evidence labels

- **VERIFIED-FROM-SOURCE (V)**: I read the Adobe doc source or Adobe sample code myself. I cloned `AdobeDocs/uxp-premiere-pro` (HEAD `fe96210`, 2026-10-23), `AdobeDocs/uxp-premiere-pro-samples` (HEAD `e1c23e3`, 2026-10-29) and `docsforadobe/premiere-scripting-guide` (2026-10-05), and downloaded `Adobe-CEP/Samples` PProPanel `Premiere.jsx` and `ReadMe.md`.
- **DOCUMENTED (D)**: Adobe blog or community posts, posts by Adobe staff, or reputable secondary sources.
- **INFERRED (I)**: My reasoning from the sources above.
- **UNKNOWN (U)**: Not established. Test it on the machine.

## Where the sources live

| What | Rendered URL | Source I read |
|---|---|---|
| UXP changelog | https://developer.adobe.com/premiere-pro/uxp/changelog/ | `github.com/AdobeDocs/uxp-premiere-pro/blob/main/src/pages/changelog/index.md` |
| Premiere DOM reference | https://developer.adobe.com/premiere-pro/uxp/ppro-reference/ | `.../src/pages/ppro-reference/classes/*.md` |
| Sample panel | — | https://github.com/AdobeDocs/uxp-premiere-pro-samples/tree/main/sample-panels/premiere-api |
| ExtendScript guide (community, includes Adobe text) | https://ppro-scripting.docsforadobe.dev/ | `github.com/docsforadobe/premiere-scripting-guide` |
| CEP PProPanel | https://github.com/Adobe-CEP/Samples/tree/master/PProPanel | `ReadMe.md`, `jsx/PPRO/Premiere.jsx` |

**Caveat on the "Since" fields (V+I).** Some per-method "Since" values in the reference are unreliable. `Transcript.transcribeClipProjectItem` is labelled "Since 25.6". However, the changelog lists it as new in 26.5, and git history shows the docs first added it in commit `73868aa` ("documentation updates for 26.5", 2026-08-24). The sample panel also files it under "New APIs in 26.5 (Beta)". **For 26.3.2, trust the changelog and the sample panel's version sections over the per-method "Since" labels.**

---

## 1. Premiere UXP: timeline and API coverage

### 1.1 Timeline (V, changelog)

| Version | Status | Notable additions |
|---|---|---|
| 25.1/25.2 | Public **beta**, 2024-12-04 | UXP v8.x added "Support for UXP Plugins in Premiere Pro v25.1 (Beta)" |
| **25.6.0** | **GA** ("Official Release of UXP extensibility"), Nov 2025 | "APIs are approaching parity with what was previously possible via CEP and ExtendScript" |
| 26.2.0 | Release (Apr 2026) | **Hybrid (C++) UXP plugins officially supported**. `ProjectConverter.exportAsFinalCutProXML` and `exportAsOpenTimelineIO`, `SequenceSettings.get/setVideoFrameRate`, `Project.closeSequence` |
| **26.3.0** | Release (Jun 2026). **This is your API level.** | Breaking: `Sequence.setSelection` is now sync, and every `create*Action` must run inside `project.lockedAccess()`. New: track `createSetNameAction`, `ClipProjectItem.createSubClipAction`, `EncoderManager.launchEncoder/startBatchEncode/setEmbeddedXMPEnabled/setSidecarXMPEnabled`, `Marker.guid`, `ObjectMaskUtils`, `Project.createSequenceWithPresetPath`, `ProjectConverter.exportAAF`, `SourceMonitor.setPosition`, `Transcript.querySupportedLanguages/hasTranscript` |
| 26.5.0 | Docs list it as a release. The sample UI labels it "(Beta)". Its status is U. | `Transcript.transcribeClipProjectItem` (+ `isLanguagePackAvailable`), `WorkAreaUtils`, `MediaManager` (purge cache), `C2PAService`, sync `Media.getStart/getDuration`. Fixes: `Markers.getMarkers(filters)` used to throw, and `ClipProjectItem.createSetIn/OutPointAction` used to error |
| 27.0 (Beta) | Announced in the samples | `TickTime.timeToTimecode/timecodeToTime`, `MogrtText`/`MogrtComment` structured MOGRT params, `ClipProjectItem.type` |
| **27.1 (Beta)** | "New APIs Coming in 27.1 (Beta)" in the sample UI | **`SequenceEditor.createRazorTrackAction(mediaType, trackIndex, time, razorLinkedTrackItems, alignToMediaType)` and `createRazorAllTracksAction(mediaType, time, alignToMediaType)`**, component instance names, detach proxy, `isStill` |

Sources: changelog (above). Razor examples are in samples commit `8d75ef1` (2026-10-06): https://github.com/AdobeDocs/uxp-premiere-pro-samples/commit/8d75ef1e7d76d08818696e7c9545fa8913b2d8f8 (V). The calls carry `@ts-expect-error - not typed yet!`, so they are pre-release.

### 1.2 Programming model (V)

- **Entry point:** `const ppro = require("premierepro")`, then `await ppro.Project.getActiveProject()` and `project.getActiveSequence()`. Most getters are async and return Promises.
- **Mutations:** a mutation is never a direct setter. You build `Action` objects with `create*Action(...)` and commit them with `project.executeTransaction(cb(compoundAction), "Undo label")`. That gives **one undo step per transaction** (`project.md`).
- **Locking:** since 26.3, Actions **must** be created inside `project.lockedAccess(() => {...})`, which takes a read/upgrade lock so project state cannot change during the callback. Adobe ships `@adobe/eslint-plugin-premierepro` to catch violations (changelog 26.3).
- **Selections:** `TrackItemSelection.createEmptySelection(cb)` gives a selection object that is valid only inside the callback, so no async code belongs in that callback (`trackitemselection.md`).
- There is no `CompoundAction` constructor to call yourself. The `compoundAction` argument exposes `addAction()`.

### 1.3 Coverage by area in 26.3 (V unless noted; class file names refer to `ppro-reference/classes/`)

**Project, sequence and tracks**

- `Project.open/createProject/save/saveAs/close`, `getSequences/getActiveSequence/setActiveSequence/openSequence/createSequence/createSequenceFromMedia/createSequenceWithPresetPath(26.3)/deleteSequence/importSequences/importFiles(filePaths, suppressUI, targetBin, asNumberedStills)/importAEComps`.
- `Sequence.getVideoTrack(i)/getAudioTrack(i)/getCaptionTrack(i)`, track counts, `getSelection/setSelection/clearSelection`, `getPlayerPosition/setPlayerPosition`, `getInPoint/getOutPoint`, **`createSetInPointAction/createSetOutPointAction`**, `createSetZeroPointAction`, `createCloneAction`, `createSubsequence`, `getSettings/createSetSettingsAction`, `getTimebase`, `getFrameSize`.
- `SequenceSettings` has setters for frame rect, frame rate (26.2), PAR, audio sample rate, codecs and so on. Use `setVideoFrameRect` plus `createSetSettingsAction` to make a 1080×1920 vertical sequence. The sample ships `Social Media Portrait 9x16 30 fps.sqpreset` for `createSequenceWithPresetPath`.
- Tracks: `getTrackItems(TrackItemType, includeEmpty)`, `isMuted/setMute`, and `createSetNameAction` (26.3). **No API exists to add or delete tracks.** Inserting at a track index above the track count creates a new track (`createInsertProjectItemAction` docs).

**Track items** (`videocliptrackitem.md`, `audiocliptrackitem.md`)

- Getters: start/end/in/out/duration, speed, project item, `getComponentChain`, `getTrackIndex`.
- Actions: `createMoveAction(TickTime)`, `createSetStartAction`, `createSetEndAction`, `createSetInPointAction` and `createSetOutPointAction` (source-relative), `createSetDisabledAction`, `createSetNameAction`, and add/remove video transition.
- **No action moves a clip vertically to another track.** Clone with a vertical offset, then remove the original.
- **Community-reported semantics (D, not Adobe):** `createMoveAction` behaves as a slide, and `createSetInPointAction` can shift the clip's start. Wrap these in tests. Source: https://community.adobe.com/questions-729/uxp-premiere-pro-how-to-slip-edit-a-videocliptrackitem-razor-blade-equivalent-1624762

**Edits** (`SequenceEditor`, `sequenceeditor.md`)

- `createInsertProjectItemAction(projectItem, time, vIdx, aIdx, limitShift)` performs an insert edit.
- `createOverwriteItemAction(projectItem, time, vIdx, aIdx)` performs an overwrite edit.
- `createCloneTrackItemAction(trackItem, timeOffset, vOffset, aOffset, alignToVideo, isInsert)`.
- **`createRemoveItemsAction(trackItemSelection, ripple: boolean, mediaType, shiftOverLapping)` deletes whole track items, with ripple when `ripple=true`.** The sample uses it as "ripple delete": https://github.com/AdobeDocs/uxp-premiere-pro-samples/blob/main/sample-panels/premiere-api/src/sequenceEditor.ts
- `insertMogrtFromPath(path, time, vIdx, aIdx)`, `insertMogrtFromLibrary`, `getInstalledMogrtPath`.
- **Missing in 26.3:**
  - No razor or split. Razor arrives in 27.1 Beta.
  - No range-based extract or lift on sequence in/out (the QE `extract` equivalent).
  - No ripple-delete of a time range that crosses clip boundaries.
  - No "add edit" command.

**Markers** (`markers.md`, `marker.md`)

- `Markers.getMarkers(sequenceOrClipProjectItem)`, then `createAddMarkerAction(name, markerType, start, duration, comments)`, `createMoveMarkerAction`, `createRemoveMarkerAction`.
- On `Marker`: `createSetNameAction/SetCommentsAction/SetDurationAction/SetTypeAction/SetColorByIndexAction`, plus getters (`getUrl`, `getTarget` and others). `guid` was added in 26.3.
- Types: Comment, Chapter, WebLink and FLVCuePoint. **Filtering with `getMarkers(filters)` was broken before 26.5.** In 26.3, filter in JS instead.

**Captions**

- `Sequence.getCaptionTrack/getCaptionTrackCount`, and `CaptionTrack.getTrackItems/isMuted/setMute/createSetNameAction`.
- **No API creates a caption track, imports an SRT onto a caption track, generates captions from a transcript, or edits caption text or style.** I grepped the whole reference: no `srt`, `subtitle` or `createCaptionTrack`.
- (I/U) `project.importFiles([".srt"])` probably imports a caption project item. Whether an overwrite of that item onto a sequence creates a caption track is untested.

**Transcripts** (`transcript.md`, `textsegments.md`)

- In 26.3: `exportToJSON(clipProjectItem)`, `importFromJSON(json)` returning `TextSegments`, **`createImportTextSegmentsAction(textSegments, clipProjectItem)`**, `hasTranscript` (26.3) and `querySupportedLanguages` (26.3).
- `transcribeClipProjectItem(item, {language})` is **26.5+**. In 26.3 you cannot start Speech-to-Text programmatically (I, from the changelog and git history).
- The JSON schema is `assets/transcript_format_spec.json` in the samples, `$id https://schemas.adobe.com/transcript/v1.0.0`. It contains `language`, then `segments[]{start, duration, language, speaker, words[]{start, duration, text, confidence, eos, tags, type}}`, then `speakers[]{id(uuid), name}`, with times in float seconds.
- **The `LanguageCode` enum contains no Arabic code.** It lists en-us, en-gb, zh-hk, cmn-hans/hant, es-es, de-de, fr-fr, ja-jp, pt-pt/br, ko-kr, it-it, ru-ru, hi-in, nb-no, sv-se, nl-nl, da-dk, id-id, th-th, vi-vn, ms-my, tr-tr, pl-pl, fil-ph, te-in, ml-in, pa-in, plus `"??-??"` for unknown (V).
- **No API reads or edits text-based-editing selections, pauses or fillers.**

**Effects and params** (`componentparam.md`, `videocomponentchain.md`, `videofilterfactory.md`, `audiofilterfactory.md`, `keyframe.md`)

- Chain: `trackItem.getComponentChain()`, then `getComponentAtIndex(i)` (index 0/1 are the intrinsics: Opacity and Motion in the video chain), then `component.getMatchName()/getDisplayName()/getParam(i)`.
- Param: `createKeyframe(value)`, `createSetValueAction(keyframe, ...)`, `createSetTimeVaryingAction`, `createAddKeyframeAction/createRemoveKeyframeAction/createRemoveKeyframeRangeAction`, `createSetInterpolationAtKeyframeAction`, `getValueAtTime`, `getKeyframeListAsTickTimes`. `PointF` is used for Position.
- Add effects with `VideoFilterFactory.createComponent(matchName)` or `AudioFilterFactory.createComponentByDisplayName("Vocal Enhancer", trackItem)` (sample), then `chain.createInsertComponentAction/createAppendComponentAction/createRemoveComponentAction`.
- **Motion position, scale and opacity writes are supported (V, sample `keyframe.ts`).**
- (I) The audio Volume "Level" keyframes should work the same way through `AudioComponentChain`. U: test it.

**Audio**

- Available: effects through `AudioFilterFactory` (any display name the effects list exposes) and track mute.
- **No API for the Essential Sound panel** (Enhance Speech, Auto-Ducking, loudness auto-match, Remix) in UXP or ExtendScript. I grepped for "enhance", "duck", "remix" and "loudness": nothing (V).
- (U) Whether "Enhance Speech" appears in `AudioFilterFactory.getDisplayNames()`. Test it.

**Export** (`encodermanager.md`, `exporter.md`)

- `EncoderManager.getManager()`, then:
  - `exportSequence(sequence, ExportType.IMMEDIATELY | QUEUE_TO_AME | QUEUE_TO_APP, outputFile, presetFile(.epr), exportFull)`
  - `encodeFile(...)` and `encodeProjectItem(item, out, preset, workArea 0/1/2, ...)`
  - `isAMEInstalled`, `getExportFileExtension`
  - in 26.3: `launchEncoder`, `startBatchEncode`, XMP toggles
- **Events:** `EncoderManager.EVENT_RENDER_QUEUE / PROGRESS {jobID, progressAmount 0..1} / COMPLETE / ERROR {jobID, inErrorNumber} / CANCEL`, registered with `ppro.EventManager.addEventListener(encoder, ...)`. There is also the global `OperationCompleteEvent.EXPORT_MEDIA_COMPLETE` (sample `eventManager.ts`).
- `Exporter.exportSequenceFrame(seq, time, name, folder, w, h)` writes stills.

**Interchange out**

- `ProjectConverter.exportAsFinalCutProXML` (26.2), `exportAsOpenTimelineIO` (26.2) and `exportAAF` (26.3).
- **No import functions specific to XML, OTIO or AAF.** Import goes through `importFiles` (I).

**Other**

- `Metadata` (project/XMP get and set, schema).
- `SequenceUtils.performSceneEditDetectionOnSelection(clipOperation, selection)`, the **scene edit detection API**.
- `ClipProjectItem` in/out, subclip (26.3), proxies, interpretation, offline, relink.
- `SourceMonitor`.
- `EventManager`: project, sequence, track changed, export, import and generative-extend-complete events.
- **No Auto Reframe API in UXP.** ExtendScript has one; see §3.

### 1.4 Plugin sandbox: network, files, external control (V unless noted)

- **Network** (`plugins/concepts/manifest/index.md`, `resources/recipes/network/index.md`):
  - `requiredPermissions.network.domains` takes a list or `"all"`. `fetch`, XHR and **WebSocket** are available globally.
  - **"UXP supports WebSocket clients only. Plugins can connect to WebSocket servers, but cannot host or accept incoming connections."**
  - Adobe recommends https because "macOS restricts http://".
  - (I) The pattern is an external process that runs a localhost WebSocket or HTTP server, with the Premiere panel connecting out as a client. Whether `ws://localhost:PORT` or `ws://127.0.0.1` must be listed explicitly is U; `"all"` should cover it.
- **Files:** `localFileSystem` takes `"plugin" | "request" | "fullAccess"`. `fullAccess` allows `file:/C:/...` absolute paths. The UXP `fs` module is available.
- **Processes:** `shell.openPath(path)` and `shell.openExternal(url)` each need user consent. Per Adobe's recipe they can run a script file, but "it's not possible to pass any parameters, nor to capture the output". There is no `child_process`.
- **Hybrid C++ plugins** (26.2+): native `.uxpaddon` code, built with the SDK from the Adobe Developer Console. (I) Native code can open server sockets. Adobe staff (forum user `bbb_999`, 2026-06-25) says external-app communication via UXP is possible "using a Hybrid UXP plugin": https://forums.creativeclouddeveloper.com/t/invisible-uxp-for-bridge-automations/11990 (D)
- **No external or headless scripting:**
  - The UXP feature table says Premiere Pro supports UXP plugins from 25.1 and **UXP Scripting "-"** (`uxp-api/versions3-p.md`). There is no `.psjs` equivalent. The same table also shows Hybrid as "-", which is stale.
  - Adobe staff: "Support for invisible UXP plugins won't be available until next year" (June 2026, so 2027) (D, same thread).
  - So the panel must be open, or at least loaded, for a bridge to work.
  - UDT (UXP Developer Tool) loads and debugs plugins. It is not an automation channel.

---

## 2. ExtendScript, CEP and QE: status and timeline

**Superseding schedule: Adobe Developer Blog, Sept 2026** (D, Adobe primary): https://blog.developer.adobe.com/en/publish/2026/09/investing-in-the-future-of-creative-cloud-extensibility-uxp-comes-to-our-flagship-applications

- Premiere: "GA UXP plugins + Hybrid plugins available."
- **Premiere stops accepting new CEP submissions in December 2027.**
- **CEP is disabled by default in December 2028.** "users can easily turn it back on."
- **"Starting December 2029, CEP will no longer be included in these apps"**, that is, CEP retires at the end of 2029.
- Existing Marketplace CEP plugins keep working and can be updated until then.
- **"ExtendScripts are not affected by this transition."**

**Older statement, now superseded** (V): The PProPanel ReadMe (Nov 2025) said: "the plan is to support both CEP and UXP for a calendar year, after which we will remove support for CEP extensibility." That would have meant late 2026. The Sept 2026 blog replaces it with the 2027–2029 schedule. https://github.com/Adobe-CEP/Samples/blob/master/PProPanel/ReadMe.md

**ExtendScript** (V, docsforadobe index, which carries Adobe's wording):

- "ExtendScript-based integrations are still supported, and Adobe currently has no plan or schedule for removing ExtendScript, which will not be removed as part of any CEP removal."
- From the 23.0 changelog: "No further changes or improvements to Premiere Pro's ExtendScript API are planned."
- How-to: "Executing scripts from within CEP panels is the recommended approach." Command-line execution is "not recommended".
- **Practical implication (I):** in Premiere, ExtendScript has no File > Scripts host. Your CEP-hosted ExtendScript bridge therefore depends on CEP:
  - It keeps working through 26.x and 2027.
  - It needs a user toggle from Dec 2028.
  - It is gone from new versions from Dec 2029.
  - The CEP-only bridge is the piece with a known end date. The blog does not say how ExtendScript would run in Premiere without CEP (U).

**QE DOM** (D, Adobe engineer Bruce Bullis):

- "The QE DOM is 100% unsupported, and not recommended."
- "in UXP, there is no such thing as QE DOM."
- "the plan is to expose some (but definitely not ALL) QE DOM functions, in the UXP API."
- Sources: Feb 2025, https://community.adobe.com/questions-729/extendscript-unsupported-undoc-commands-are-hidden-behind-40-is-there-a-way-to-get-them-for-free-1416569. Dec 2025: "there have been zero changes to QE DOM APIs, and no such changes are planned or scheduled… will also remain 100% unsupported", https://community.adobe.com/feature-requests-730/request-for-timeline-editing-api-support-clip-track-movement-flattening-1621168.
- `app.enableQE()` itself is documented in the guide: "Enables Premiere Pro's QE DOM" (V).
- Adobe's own PProPanel still calls `qe.project.getActiveSequence()`, `qe.project.newSequence`, `qe.source.player.*` and `qe.project.deletePreviewFiles` (V, `Premiere.jsx` lines 409–415, 640–643, 720–721, 1312).
- The QE razor and extract methods themselves are **not documented anywhere by Adobe** (U). Their behaviour is only known empirically.

**Razor and split in UXP** (D): An Adobe reply (`bbb_999`, 2025-09-14) said there was no razor API for the 1.0 release, which prioritised parity with "CEP+ExtendScript APIs (not including QE DOM)": https://forums.creativeclouddeveloper.com/t/premiere-pro-uxp-dom-eta-for-programmatic-split-razor-on-timeline/11375. Razor now appears in the 27.1 Beta samples (V, §1.1).

**Known ExtendScript/CEP breakage in 25/26** (D, user reports):

- On clean installs of 25.6.2, CEP `evalScript` did not respond. An Adobe rep called it a known bug, worked around by closing the Adobe Stock panel: https://community.adobe.com/questions-729/critical-premiere-scripting-engine-does-not-respond-to-cep-evalscript-calls-1621640
- In June 2026 a user reported a CEP bridge "silently broken" after an update. Adobe said: "Your report is the first we've heard" and that nothing changed for hidden CEP panels in 26.3 (thread above).
- Old: `app.encoder` broken on Mac 14.3.1–15, fixed in 22+ (V, guide).
- I found no Adobe-confirmed list of 26.x ExtendScript regressions (U).

---

## 3. Native features relevant to lecture editing in 26.x

| Feature | Local or cloud | Arabic | Automatable? |
|---|---|---|---|
| **Speech to Text / transcription** | Local, with downloadable language packs. "with 22.2 and later you can use Speech to Text offline" (D, adobe.com product page). The 2026 model "supports 18 languages" (D, Adobe CM, Mar 2026, https://community.adobe.com/announcements-732/announcing-improvements-in-transcription-accuracy-and-speed-1555432) | **No** (D: Jan 2026 request "Speech to Text in Arabic not supported in Premiere Pro 26", https://community.adobe.com/feature-requests-730/speech-to-text-in-arabic-not-supported-in-premiere-pro-26-1621281. V: no `ar-*` in the transcript-JSON enum) | Trigger in UXP from **26.5** (`transcribeClipProjectItem`). In 26.3, only check, export or import. **External transcripts (e.g. Whisper Arabic) can be imported** with `Transcript.importFromJSON` + `createImportTextSegmentsAction` (V). UI equivalent: Text panel > … > Import > Import Static Transcript (D, https://community.adobe.com/announcements-732/now-in-beta-import-your-own-transcript-311910). Whether `"??-??"` with Arabic text renders correctly for TBE or captions is **U** |
| **Auto captions** (from transcript; single-word captions added in 26.3, D) | Local | Only via an imported transcript (U) | **No API** to generate captions in UXP or ExtendScript. ExtendScript `Sequence.createCaptionTrack(projectItem(.srt), startSeconds, format)` builds a caption track from an imported SRT (V, guide). UXP has no equivalent in 26.3 (V) |
| **Caption translation** | Cloud (25.2+) | Arabic not supported per a Community Expert (D) | No API |
| **Text-based editing "delete pauses"** | Local | Depends on the transcript | **Not scriptable.** No API touches TBE selection or pauses (V by absence). UI-only: Pauses filter, Delete (Extract/Lift). Minimum pause is about 0.1 s; a 26.2 regression was reported (D, https://community.adobe.com/questions-729/removing-pauses-using-text-based-editing-still-leaves-a-lot-of-room-1558021) |
| **Enhance Speech** | **Local** in Premiere: "optimized to perform locally… no internet connection required", downloaded as an add-on (D, https://community.adobe.com/announcements-732/now-released-enhance-speech-in-premiere-pro-313485) | Not officially listed; staff say no translation capability. Language-agnostic behaviour is U | No Essential Sound API. Enumerate the `AudioFilterFactory` display names to check (U) |
| Auto-Ducking, Remix, loudness auto-match | Local | n/a | No API (V by absence) |
| **Scene Edit Detection** | Local | n/a | **Yes.** UXP `SequenceUtils.performSceneEditDetectionOnSelection` and ExtendScript `Sequence.performSceneEditDetectionOnSelection` (V) |
| **Auto Reframe** (vertical shorts) | Local (Sensei) | n/a | **ExtendScript only:** `Sequence.autoReframeSequence(num, den, 'slower'/'default'/'faster', newName, useNested)` returns a new sequence (V, guide, since 14.0). **No UXP equivalent in 26.3** (V by absence) |
| Generative Extend | Cloud (Firefly, credits), GA 25.2 (D) | n/a | No trigger API. Only `OperationCompleteEvent.GENERATIVE_EXTEND_COMPLETE` (V) |
| Media Intelligence search | 25.2+ (D) | n/a | No API |
| AI Assistant (Window > Assistant) | **Public beta** since 2026-06-23. Firefly and partner models; "optimized for English" (D, https://community.adobe.com/announcements-727/meet-your-new-assistant-editor-ai-assistant-in-premiere-pro-is-now-in-public-beta-1629317) | Partial | No API or MCP. Organises bins, transcribes, adds markers, builds stringouts. No silence removal is listed |
| **MOGRT import** | Local | n/a | UXP `SequenceEditor.insertMogrtFromPath/FromLibrary` (V). ExtendScript `Sequence.importMGT/importMGTFromLibrary` + `TrackItem.getMGTComponent()` (V). Structured MOGRT text editing in UXP arrives in 27.0 (`MogrtText`, V); in 26.3 editing it through params is U |
| **Adobe Media Encoder** | Local | n/a | Queue from Premiere: UXP `EncoderManager` (V) or ExtendScript `app.encoder.encodeSequence/startBatch` with `bind('onEncoderJobProgress'...)` (V, PProPanel). AME watch folders are a native UI feature (D, general knowledge). An AME UXP **public beta** is "live now" per the Sept 2026 blog (D) |

---

## 4. Interchange

| Format | Import into Premiere | Export | Notes |
|---|---|---|---|
| **FCP7 XML (xmeml)** | **Yes**, File > Import (D, helpx migration page via search) | UI, ExtendScript `exportAsFinalCutProXML`, UXP `ProjectConverter.exportAsFinalCutProXML` (26.2, V) | (I, from long practice) Survives: clips, source in/out, tracks, A/V links (`<link>`), sequence and clip markers, speed, Basic Motion scale/position/rotation, opacity, audio levels and keyframes, cross dissolves. Lost: captions, most effects. **The best fit for a "build the cut list outside, import once" silence-removal strategy.** U: test on 26.3.2 |
| **FCPXML (FCP X)** | **No native import**. Adobe recommends Intelligent Assistance XtoCC (D, helpx "migrate from Final Cut Pro X") | — | Not usable |
| **AAF** | Yes (D) | ExtendScript `Project.exportAAF`, UXP `exportAAF` (26.3, V) | Audio-post oriented |
| **EDL (CMX3600)** | Yes (D, long-standing) | ExtendScript `exportTimeline`/UI | One video track; no effects or markers |
| **OTIO** | **Yes.** The Adobe announcement is titled "[Now Released] OTIO Import and Export" (D, https://community.adobe.com/announcements-732/now-released-otio-import-and-export-311699). Remotion's docs say File > Import works in 25.6+ (D) | UXP `exportAsOpenTimelineIO` (26.2, V) | Supported: clip names, cut list, source in/out, timecode and fps, multiple tracks and names, linear speed, sequence markers (name, color, duration), clip markers on round-trip. Not mentioned: effects, transitions, captions. Adobe staff (Feb 2025): "We're not there yet" for full release quality |

---

## 5. Frame-accurate time

- **ExtendScript:** "there are 254016000000 ticks per second". `Time.ticks` is a **String**, `Time.seconds` a number, and `getFormatted()` gives timecode (V, `other/time.md`). Several setters accept seconds (e.g. `Sequence.setInPoint(time)` takes "Integer or Time object… time in seconds") (V).
- **UXP `TickTime`:**
  - Constructors: `createWithTicks(string)`, `createWithSeconds(number)`, `createWithFrameAndFrameRate(frame, FrameRate)`.
  - Properties: `ticks` (string), `ticksNumber`, `seconds`.
  - Math: `add/subtract/multiply/divide/equals/alignToFrame/alignToNearestFrame`, plus `TIME_ZERO` and `TIME_INVALID`.
  - `FrameRate.createWithValue()` and `.ticksPerFrame`. `Sequence.getTimebase()` returns ticks per frame.
  - Timecode conversion arrives in 27.0.
  - Adobe's sample warns that `createWithSeconds(oldEnd.seconds - 1.0)` "is not the best approach for precise TickTime calculation". Use ticks or frame math instead (V, `sequence.ts`).
- **Exact ticks per frame (I, computed):**

  | Rate | Ticks per frame |
  |---|---|
  | 23.976 | 10594584000 |
  | 24 | 10584000000 |
  | 25 | 10160640000 |
  | **29.97** | **8475667200** |
  | 30 | 8467200000 |
  | 59.94 | 4237833600 |
  | 60 | 4233600000 |

  All are integers, and a 48 kHz sample is 5292000 ticks. So **do all cut math in integer ticks (BigInt)**, snapped to `ticksPerFrame` multiples, never in float seconds. **Drop-frame affects only the timecode label, not ticks.** Avoid parsing DF timecode yourself until `timecodeToTime` arrives (27.0).
- **OBS VFR** (D, Adobe community FAQ, https://community.adobe.com/t5/premiere-pro/faq-variable-frame-rate-vfr-video/td-p/10348229):
  - Premiere flags "Variable Frame Rate Detected" in clip Properties.
  - Adobe recommends transcoding VFR to CFR before proxy, consolidate or transcode workflows, and mentions "Preserve Audio Sync".
  - OBS users report drift of about 2 frames on long recordings.
  - (I) For long lectures, record CFR in OBS or transcode to CFR before computing silence ranges. Silence detection on audio (sample-accurate) then has to map onto a CFR video timebase.

---

## 6. Official Adobe MCP / AI-agent integration

- **No official Adobe MCP server for desktop Premiere exists (D).** An Adobe-community request from 2026-09-28 asks for one and has no Adobe reply: https://community.adobe.com/feature-requests-730/official-model-context-protocol-mcp-server-for-premiere-pro-1644303
- The **"Adobe for creativity" Claude connector** (2026-04-28; adobe.com/adobe-connectors.html names Premiere among the apps, D) appears to run cloud/Express-level operations such as reframing and resizing. It does not control a local Premiere timeline. That is per secondary analysis (https://www.mindstudio.ai/blog/claude-mcp-adobe-vs-photoshop-premiere-what-it-does), and Adobe's page gives no Premiere tool list. Status is I/U.
- The **in-app AI Assistant** is beta, UI-only and exposes no API (D).
- Third-party Premiere MCP servers (e.g. leancoderkavy/premiere-pro-mcp) use CEP/ExtendScript/QE bridges. They are not Adobe products (D).

---

## 7. Capability matrix (for your 26.3.2)

✅ supported · ⚠️ partial or workaround · ❌ none · β = beta or later version only

| Operation | ExtendScript (+QE) via CEP | UXP 26.3 | Native UI feature | Sources |
|---|---|---|---|---|
| Open project, sequences, tracks, clips | ✅ | ✅ | — | `project.md`, `sequence.md` |
| Insert / overwrite edit | ✅ `insertClip`/`overwriteClip` | ✅ `createInsertProjectItemAction`/`createOverwriteItemAction` | ✅ | `sequenceeditor.md` |
| Move / trim track item | ✅ `TrackItem.move`, start/end/in/out props | ✅ `createMove/SetStart/SetEnd/SetIn/SetOutPointAction` (semantics quirky, D) | ✅ | `videocliptrackitem.md` |
| **Ripple delete whole clips** | ✅ `TrackItem.remove(inRipple, alignToVideo)` | ✅ **`createRemoveItemsAction(sel, ripple=true, …)`** | ✅ | `sequenceeditor.md`, sample `sequenceEditor.ts` |
| **Razor / split at time** | ⚠️ QE only (undocumented, unsupported) | ❌ in 26.3 · β **27.1** `createRazorTrackAction`/`createRazorAllTracksAction` | ✅ Add Edit | samples commit `8d75ef1` |
| **Extract / lift a time range (in→out)** | ⚠️ QE only (undocumented) | ❌. Emulate by rebuilding (overwrite source segments with in/out), clone+trim, or wait for razor + `createRemoveItemsAction` | ✅ Extract/Lift | I |
| Silence removal end to end | ⚠️ QE razor + remove | ⚠️ Rebuild the sequence from a cut list: `ClipProjectItem.createSetInOutPointsAction` + `createOverwriteItemAction` per kept segment, or subclips (26.3), **or import FCP7 XML/OTIO** | ⚠️ TBE "Delete pauses" (UI only, transcript-dependent) | I |
| Sequence in/out | ✅ `setInPoint/setOutPoint` | ✅ `Sequence.createSetInPointAction/createSetOutPointAction` | ✅ | `sequence.md` |
| Work area | ✅ | β 26.5 `WorkAreaUtils` | ✅ | changelog |
| Markers: create / read / edit / move / remove | ✅ `markers.createMarker` etc. | ✅ (filter arg buggy until 26.5) | ✅ | `markers.md`, `marker.md`, sample `markers.ts` |
| **Caption track from SRT** | ✅ `Sequence.createCaptionTrack(item, t, fmt)` | ❌ (U: `importFiles` + overwrite) | ✅ Import captions | guide `sequence.md`; UXP grep |
| Caption text/style edit | ❌ | ❌ | ✅ | — |
| Auto captions from transcript | ❌ | ❌ | ✅ (single-word in 26.3) | — |
| Start transcription | ❌ | ❌ in 26.3 · β 26.5 `transcribeClipProjectItem` | ✅ (no Arabic) | `transcript.md`, changelog |
| Import external transcript JSON | ❌ | ✅ `importFromJSON` + `createImportTextSegmentsAction` (no Arabic code; `"??-??"` U) | ✅ (Import Static Transcript) | sample `transcript.ts`, `transcript_format_spec.json` |
| Export transcript JSON | ❌ | ✅ `exportToJSON` | ✅ | `transcript.md` |
| TBE delete pauses / fillers | ❌ | ❌ | ✅ UI | — |
| Motion position / scale / opacity | ✅ `components[].properties[].setValue` | ✅ `ComponentParam.createSetValueAction` / keyframes | ✅ | `componentparam.md`, sample `keyframe.ts` |
| Add / remove effects | ⚠️ QE (`addVideoEffect`) | ✅ `VideoFilterFactory`/`AudioFilterFactory` + chain actions | ✅ | `videofilterfactory.md` |
| Audio volume keyframes | ✅ | ✅ (I) via Volume component params | ✅ | I |
| Enhance Speech / Essential Sound / Auto-Duck | ❌ | ❌ (U: filter list) | ✅ (Enhance Speech local) | grep |
| MOGRT insert | ✅ `importMGT` | ✅ `insertMogrtFromPath` | ✅ | `sequenceeditor.md` |
| MOGRT text edit | ✅ `getMGTComponent()` | ⚠️ U in 26.3 · β 27.0 `MogrtText` | ✅ | `mogrttext.md` |
| Auto Reframe | ✅ `autoReframeSequence` | ❌ | ✅ | guide `sequence.md` |
| Scene edit detection | ✅ | ✅ | ✅ | `sequenceutils.md` |
| New vertical sequence | ✅ (preset / QE `newSequence`) | ✅ `createSequenceWithPresetPath` (26.3) + `SequenceSettings.setVideoFrameRect` | ✅ | `project.md`, `sequencesettings.md` |
| Nest / subsequence | ✅ `createSubsequence` | ✅ `Sequence.createSubsequence` | ✅ | `sequence.md` |
| Export in-app (direct) | ✅ `exportAsMediaDirect(out, epr, workArea)` | ✅ `exportSequence(seq, IMMEDIATELY, out, epr, exportFull)` | ✅ | `encodermanager.md` |
| Queue to AME + progress | ✅ `app.encoder.encodeSequence` + `bind('onEncoderJobProgress')` | ✅ `QUEUE_TO_AME` + `EVENT_RENDER_PROGRESS {jobID, progressAmount}` | ✅ | sample `eventManager.ts`, `Premiere.jsx` L648–652 |
| Export frame | ⚠️ QE `exportFramePNG` | ✅ `Exporter.exportSequenceFrame` | ✅ | `exporter.md` |
| Import media | ✅ | ✅ `importFiles` | ✅ | `project.md` |
| Export FCP XML / OTIO / AAF | ✅ XML/AAF/OMF | ✅ XML+OTIO (26.2), AAF (26.3) | ✅ | `projectconverter.md` |
| Metadata (XMP / project) | ✅ | ✅ | ✅ | `metadata.md` |
| Undo grouping | ❌ (each call is a separate undo) | ✅ `executeTransaction(cb, label)` = one undo step | — | `project.md` |
| External control from another process | ✅ CEP panel (Node.js enabled, can host a server) | ⚠️ Panel as WebSocket/HTTP **client** only; a hybrid C++ addon is needed to host. Not headless (invisible plugins "next year") | — | network recipe; forum 11990 |

---

## 8. Claims you asked me to check

| Claim | Verdict |
|---|---|
| "UXP in Premiere has no ripple delete / extract equivalent" | **Partly false.** Ripple delete of whole track items exists: `SequenceEditor.createRemoveItemsAction(selection, ripple=true, mediaType, shiftOverlapping)`, since 25.6 (V). There is **no range extract/lift and no razor in 26.3** (V). Razor is coming in **27.1 Beta** (V, samples). |
| "UXP can create markers" | **True** (V): `Markers.createAddMarkerAction(name, type, start, duration, comments)` inside `executeTransaction`. |
| "UXP can export via EncoderManager with progress events" | **True for AME-queued jobs** (V): `EVENT_RENDER_PROGRESS` with `progressAmount` 0–1, plus QUEUE/COMPLETE/ERROR/CANCEL. For `ExportType.IMMEDIATELY`, the docs do not say whether progress events fire (U). `EXPORT_MEDIA_COMPLETE` exists globally. |
| "UXP can import captions" | **False in 26.3** (V by full-reference grep): no caption-track creation or SRT import API. Transcript JSON import **is** supported. ExtendScript `createCaptionTrack` does exist. |
| "CEP will be removed in a specific year" | **True** (D, Adobe Developer Blog, Sept 2026): Premiere stops accepting new CEP submissions Dec 2027, disables CEP by default Dec 2028, and drops CEP from new versions Dec 2029. ExtendScript is "not affected" and Adobe has "no plan or schedule for removing ExtendScript". The older "one calendar year" plan from Nov 2025 is superseded. |

## 9. Open questions to test on 26.3.2 (U)

1. Do `ExportType.IMMEDIATELY` exports emit any progress event?
2. Does `importFiles(['x.srt'])` followed by an overwrite onto the sequence produce a caption track?
3. Does importing transcript JSON with `language: "??-??"` and Arabic words work for TBE and caption generation?
4. `AudioFilterFactory.getDisplayNames()`: is Enhance Speech, or a loudness effect, exposed?
5. Exact behaviour of `createSetInPointAction` and `createMoveAction` on a trimmed clip (community reports a slide rather than a slip).
6. Whether the manifest must list `ws://localhost:<port>` explicitly, or whether `"all"` is needed.
7. Whether 26.5 is a public release yet (the docs say release; the samples say Beta).
