# 01 — Premiere Pro MCP servers: audit of `premiere-pro-mcp` 1.14.1 and the alternatives

Research date: 2026-11-01. Source code was downloaded into
`/tmp/claude-0/-home-user-Learning-Repo0/3391813e-183a-5a64-8aab-0e6817637581/scratchpad/research/pkg-mcp/` and read with grep, sed and cat. None of it was executed.

- `pkg-mcp/v1141/package/`: the npm tarball of premiere-pro-mcp@1.14.1
- `pkg-mcp/v1270/package/`: the npm tarball of premiere-pro-mcp@1.27.0 (the latest)
- `pkg-mcp/repo-ppmcp/`: a git clone of the upstream repo with history only (`--filter=blob:none --no-checkout`)
- `pkg-mcp/alts/*`: shallow clones of the alternative projects

Labels used throughout:
- **[SRC]**: VERIFIED-FROM-SOURCE. I read the code or the registry JSON.
- **[DOC]**: DOCUMENTED. The claim comes from a README, CHANGELOG or web page only.
- **[INF]**: INFERRED.
- **[UNK]**: UNKNOWN.

Line references point into the extracted tarballs.

---

## 0. Bottom line

1. The package is `premiere-pro-mcp`, published by npm user `kavykun` from the GitHub repo `leancoderkavy/premiere-pro-mcp` under the MIT licence. It is very actively developed. **1.14.1 (2026-08-28) is 58 releases behind**: the latest is **1.27.0 (2026-10-31)**. [SRC: https://registry.npmjs.org/premiere-pro-mcp]
2. **Every one of the seven defects the skill found traces to specific code in 1.14.1**, and 1.15–1.27 fixed or reworked six of them. The seventh (apply_edit_plan has no source in/out) is now rejected loudly instead of ignored, and other tools cover ranged edits. See §3.
3. **The ~480 s export timeout is arithmetic, not chance.** `export_sequence` passes `timeoutMs: 120000`, and the bridge's hard cap is `max(timeoutMs*4, 120000)` = 480 000 ms. [SRC]
4. **1.14.1 `export_sequence` calls `seq.exportAsMediaDirect()`**, which renders inside Premiere and blocks the ExtendScript engine for the whole encode, even though the tool says "using Adobe Media Encoder". In 1.27.0 it is still exportAsMediaDirect, but with a configurable timeout (default 15 min, up to 240 min) and ffprobe verification. 1.25.0 added a true asynchronous AME path: `export_sequence_job_start` (which uses `app.encoder.encodeSequence`) plus `get_export_job_status`. [SRC]
5. **Upgrade risk for the user's engine:** deep imports of `dist/bridge/file-bridge.js` and `dist/bridge/script-builder.js` still resolve in 1.27.0. There is no `exports` map, `sendCommand(script: string, {tempDir, timeoutMs})` is unchanged, and `buildToolScript` and `escapeForExtendScript` still exist. Three caveats:
   - `buildToolScript` takes a **string**, not `lines[]`, in both versions.
   - 1.27.0 adds a cross-process host lease, a Windows ACL check on the bridge directory, and a CEP-panel schema check.
   - The CEP panel must be reinstalled after the upgrade.

   See §2.6.
6. **Recommendation:** upgrade to 1.27.x rather than replace it. Pin the exact version, reinstall the CEP panel, and run a smoke test. No alternative is clearly better.
   - `adobe-premiere-pro-mcp` (hetpatel-11) uses the same CEP file-bridge design, has fewer tools, and **sends telemetry by default**.
   - `adb-mcp` is a UXP proof of concept with 26 Premiere tools and **an unauthenticated proxy on all network interfaces**.
   - `ayushozha/AdobePremiereProMCP` is not on npm and runs a four-language stack.
   - pymiere is unmaintained and tested only up to Premiere 23.1.
   - Adobe has no official MCP server for desktop Premiere. Its hosted "Adobe for creativity" Claude connector (2026-04-28) does not edit Premiere projects. [DOC]

---

## 1. Package identity (npm)

| Field | Value | Label / source |
|---|---|---|
| name | `premiere-pro-mcp` | [SRC] registry |
| latest | **1.27.0** (2026-10-31T08:48Z) | [SRC] `dist-tags` |
| user's version | 1.14.1 (2026-08-28T04:13Z) | [SRC] `time` |
| author field | "MCP for Adobe Premiere Pro contributors" | [SRC] |
| npm maintainer | `kavykun` <kavyrattana@gmail.com> | [SRC] |
| repository | `git+https://github.com/leancoderkavy/premiere-pro-mcp.git` | [SRC] |
| homepage | https://premiere-pro-mcp.com/ | [SRC] |
| licence | MIT | [SRC] |
| provenance | npm SLSA provenance attestation on 1.14.1 (`dist.attestations`) | [SRC] |
| downloads | 5,981 in the week of 2026-10-23..29; 18,170 in the month to 2026-10-29 | [SRC] https://api.npmjs.org/downloads/point/last-week/premiere-pro-mcp |
| engines | node >= 20.19.0 | [SRC] |
| deps in 1.14.1 | `@modelcontextprotocol/sdk ^1.30.0`, `ws ^8.21.1`, `zod ^4.4.3`, `posthog-node ^5.46.1` | [SRC] |
| deps in 1.27.0 | `@modelcontextprotocol/server ^2.0.0`, `@modelcontextprotocol/node ^2.1.0`, `ws ^8.22.0`, `zod`, `jose ^6.2.10`, `posthog-node 5.57.2`, `@posthog/core`, `@posthog/types` | [SRC] |
| install scripts | **none** (no preinstall, install or postinstall in either version) | [SRC] package.json |
| tarball size | 1.14.1: 206 files, 2.46 MB unpacked. 1.27.0: 583 files, 9.5 MB | [SRC] |

**Version history.** There are 76 versions in all [SRC]:
- 1.0.0 on 2026-02-27, then a lull from March to July.
- About weekly releases from mid-July, with several per day in late August.
- After 1.14.1: 1.14.2–1.14.9, 1.15.0–1.15.2, 1.16.0–1.16.4, 1.17.0, 1.18.0–1.18.6, 1.19.0–1.19.1, 1.20.0, 1.21.0, 1.22.0, 1.23.0, 1.24.0–1.24.4, 1.25.0 (10-24), 1.26.0 (10-27), and 1.27.0 (10-31).

**What changed since 1.14.1** (from `v1270/package/CHANGELOG.md` [DOC], with spot checks in source [SRC]):
- 1.14.2: moved to MCP TypeScript SDK v2. It "replaced false-success responses for structural edits … deletion … with verified outcomes or explicit fail-closed errors".
- 1.15.2: fixed the QE still-export signature. The call `(path,w,h)` returned false, so every frame export fell through to the AME fallback. Also fixed macOS preset discovery.
- 1.16.1: insert tools (`add_to_timeline`, `add_to_timeline_batch`, `apply_edit_plan` insert) now handle sync lock. A mid-clip insert is treated as split plus insert and verified.
- 1.18.3: `export_sequence` fails when Premiere rejects the render or writes no file. `get_work_area` and `set_work_area` units were fixed.
- 1.19.0:
  - `export_sequence` gained ranges (`in_to_out`), overwrite refusal and written-file verification.
  - `work_area` now fails closed.
  - `add_to_timeline_batch` re-reads placements after later inserts.
  - `remove_from_timeline` and edit plans ripple through sync-locked ripple, so there are no more stray audio clips.
  - apply_edit_plan tokens are random and single-use.
- 1.20.0: new `ripple_remove_timeline_ranges`, a multi-range ripple cut with a preview token. This is exactly the skill's cut loop.
- 1.21.0: `set_work_area` notes that "Premiere 26.5.2 ignores the CEP work-area point setters".
- 1.23.0: when AME is absent, the default export preset no longer comes from IngestPresets (a 1024×540 proxy). Premiere's own `MediaIO/systempresets` is searched instead.
- 1.25.0:
  - New **`export_sequence_job_start` and `get_export_job_status`** (asynchronous AME).
  - MCP progress notifications every 10 s.
  - New `get_bridge_telemetry` blocking diagnosis.
  - `delete_sequence` guards nested sequences.
  - New `idempotency_key` on mutating tools.
- 1.26.0 and 1.27.0: bounded QE batches to avoid "InternalError: Stack overrun" in `ripple_remove_timeline_ranges`; `create_subclip` frame snapping; new `unnest_sequence_uxp`.

---

## 2. Architecture, from source (1.14.1 unless noted)

### 2.1 Transport: a CEP file bridge (primary)

**Node side** (`dist/bridge/file-bridge.js`) [SRC]:
- Temp dir is `options.tempDir || PREMIERE_TEMP_DIR || join(os.tmpdir(), "premiere-mcp-bridge")`. On Windows the default is `%TEMP%\premiere-mcp-bridge`.
- To send a command, it writes `cmd_<uuid>.jsx.staged`, then calls `renameSync` to produce `cmd_<uuid>.jsx`, so the panel never sees a partial file.
- It then polls for `res_<uuid>.json`, using `fs.watch` plus a 250 ms fallback timer.
- Each command file is prefixed with a bootstrap line that runs `$.evalFile("<tempDir>/helpers_<md5>.jsx")` when that helpers version is not yet loaded. The helpers file (about 14 KB) is written once.
- `cleanupTempDir()` deletes stale `cmd_`, `res_` and `busy_` files when the server starts.

**CEP side** (`cep-plugin/main.js`, `CSXS/manifest.xml`) [SRC]:
- Bundle `com.mcp.premiere.bridge`, with two extensions: a visible **panel** and a **headless** one that starts on `ApplicationActivate`.
- Host `PPRO` version 14.0+, CSXS 9.0, `--enable-nodejs`, `--allow-file-access-from-files`.
- `setInterval(processCommands, 200)` lists files matching `cmd_*.jsx` in sorted order.
- Each file is claimed by an **atomic rename** to `cmd_….jsx.<ENGINE_ID>.claimed`, so the panel and headless engines cannot both run it. The claimed file is read and deleted, then passed to `cs.evalScript(script, cb)`.
- The result string is parsed as JSON. Non-JSON is wrapped as `{success:true,data}`, and an empty result becomes a `success:false` error. The result is written to `res_<id>.json` atomically (staged, then renamed).
- While evalScript is in flight, the panel writes `busy_<id>.json` every 2 s.
- **The panel's temp dir comes from its own text field or localStorage. Its default is `os.tmpdir()` inside CEP plus `premiere-mcp-bridge`.** The panel never reads `PREMIERE_TEMP_DIR`, so a custom `PREMIERE_TEMP_DIR` only works if the panel field is set to the same path. Upstream issue #294 covered exactly this mismatch. [SRC/DOC]

**Installation** (`scripts/install-cep.ps1`) [SRC]:
- Copies to `%APPDATA%\Adobe\CEP\extensions\MCPBridgeCEP`. It prefers the signed `artifacts/MCPBridgeCEP.zxp`; both tarballs contain one with `META-INF/signatures.xml`.
- **Unconditionally sets `HKCU\SOFTWARE\Adobe\CSXS.9` … `CSXS.14` → `PlayerDebugMode`="1" (REG_SZ)**. The loop sits outside the signed/unsigned branch. The uninstaller leaves these keys in place.
- Run with `premiere-pro-mcp --install-cep`. **Yes, it requires installing a CEP extension and sets PlayerDebugMode.**

**Other details** [SRC]:
- `cep-plugin/.debug` declares a CEP remote-debug port `8088` for the panel. Whether CEP opens it depends on PlayerDebugMode and the .debug file being present [INF].
- The panel makes an outbound HTTPS call on load to `api.github.com/repos/leancoderkavy/premiere-pro-mcp/releases/latest` to check for updates. In 1.26.0 this moved to npm `/latest`. [SRC/DOC]

### 2.2 UXP path (optional)
- `dist/bridge/uxp-websocket-bridge.js` [SRC]: when `PREMIERE_UXP_TOKEN` (at least 16 characters) is set, the MCP server **listens on `127.0.0.1:7777`** (`PREMIERE_UXP_PORT`) at path `/uxp`.
  - The connection must carry `?token=` matching the token; comparison uses `timingSafeEqual`.
  - The server rejects anything that is not loopback and does **not** fall back to CEP once a UXP command has been sent.
- The UXP plugin (`uxp-plugin/manifest.json`, id `com.ppmcp.premiere.uxp`, Premiere **minVersion 25.6.0**, `network.domains: "all"`, `localFileSystem: request`) connects as a WebSocket **client**. [SRC]
  - It must be loaded through UXP Developer Tool or a `.ccx` package. DISTRIBUTION.md says a CCX is built by CI and that Marketplace distribution needs an Adobe-issued ID. [DOC]
- `*_uxp` tools are registered only when the connected panel's `hello.commands[cmd].supported === true`. That is what "authenticated UXP host advertises support" means. [SRC]

### 2.3 HTTP mode (not used by stdio clients)
- `dist/http-server.js` runs only through `npm run start:http`. It is not the default bin.
- It **binds 0.0.0.0:3000** and requires the `MCP_AUTH_TOKEN` bearer token ("REQUIRED", fail-closed). [SRC]
- In 1.27.0 the bind address can be changed with `MCP_HTTP_HOST`, but the default is still `0.0.0.0`. [SRC]

### 2.4 Script execution tools and the capability gate
- `execute_extendscript` (`dist/tools/scripting.js`) takes `{code, timeout_ms?}`. It wraps the code in an IIFE with `try/catch → __error` and sends it with `sendRawCommand`.
  - **Arbitrary ExtendScript is allowed**: no pattern blocking, only a 500 KB size limit.
  - `evaluate_expression` interpolates `${args.expression}` directly. [SRC]
- Both tools are in `UNSAFE_TOOL_NAMES` and need the **`unsafe-script` capability**. The default profile is `inspect,edit,export,filesystem`.
  - To expose these tools the user must set something like `PREMIERE_MCP_CAPABILITIES=inspect,edit,export,filesystem,unsafe-script`. [SRC `dist/security/capabilities.js`]
- `sendCommand` (used by the regular tools and by the user's engine) **rejects** scripts containing `eval(`, `new Function(` or `System.callSystem(`. `sendRawCommand` does not. The same rule holds in 1.27.0. [SRC]
- An arbitrary-code surface exists regardless of capabilities: anything that can write `cmd_*.jsx` into the bridge directory gets ExtendScript execution as the logged-in user. ExtendScript has file I/O and `system.callSystem`. 1.14.1 checks ownership only on POSIX and skips Windows (`if (process.platform === "win32") return;`). 1.22.0+ adds a Windows ACL check. [SRC/INF]

### 2.5 Timeouts [SRC]
- Default `DEFAULT_TIMEOUT_MS = 30000`, overridable with `PREMIERE_TIMEOUT_MS` or a per-call `timeoutMs`. `execute_extendscript` accepts `timeout_ms`.
- **Soft deadline, then hard cap.** At `timeoutMs` the bridge looks at `busy_<id>.json`:
  - If the file is fresh (mtime under 6 s in 1.14.1, under 10 s in 1.27.0), it keeps waiting up to `hardCapMs = max(timeoutMs*4, 120000)`.
  - Otherwise it fails with "Command timed out … Is the CEP plugin running?". If a busy file was ever seen, the message is instead "Premiere accepted the script but did not finish … modal dialog …".
- Per-tool overrides in 1.14.1: `export_sequence` uses 120 000 ms, giving a **480 s** hard cap. `export_frame` uses 60 000 ms, giving 240 s.
- In 1.27.0, `export_sequence` takes `timeout_minutes` (default 15, from 1 to 240), so the hard cap is 60 min by default.

### 2.6 Answers to the coordinator's priority questions about the engine

**(1) Will the engine's deep imports survive an upgrade?**
- Neither version has an `exports` field and both are `"type": "module"`. `dist/bridge/file-bridge.js` and `dist/bridge/script-builder.js` exist in both. [SRC]
- `sendCommand(script: string, options?: {tempDir?, timeoutMs?})` has the same name and shape in 1.27.0. 1.27.0 adds optional fields: `mutationOnTimeout`, `hostLabel`, `helpers`, `failFastOnUnreadyHeartbeat`, `mutating`, and others. [SRC `file-bridge.d.ts`]
- `buildToolScript` is exported in both as `buildToolScript = buildScript` and marked `@deprecated`. `escapeForExtendScript` is unchanged. [SRC]
- **Signature mismatch:** the declared signature is `buildScript(code: string): string`, and the body interpolates `${code}`. **If the engine passes `lines[]`, JavaScript turns the array into a comma-joined string** (`"a;,b;"`), which is a syntax error unless the engine joins the lines itself. The engine must already join them, or it is relying on single-element arrays. [SRC + INF]
- In 1.27.0, `buildScript` also prepends optional guards when the server has an expected project path or target. Those come from server-side state (`expectedProjectPath()` / `expectedHostTarget()`), and their source was not traced in a standalone import [UNK, likely empty].
- New behaviours in 1.27.0 `sendCommand` that the engine will hit [SRC]:
  1. `validateScript` still blocks `eval(` / `new Function(` / `System.callSystem(`.
  2. `ensurePrivateBridgeDirectory()` on Windows spawns PowerShell to check the bridge directory's ACL, waiting up to 30 s. It **throws** if the directory is not owned by the current user, if an untrusted identity has write access, if an ancestor is replaceable, or if the path is a symlink or junction. A custom `tempDir` must pass these checks.
  3. A **cross-process host lease** (lock dir `<tempDir>/.host-owner-lease`, holding `owner.json` with the pid). Engine and MCP-server commands are serialized, and lease acquisition gives up after `timeoutMs` with `HOST_LEASE_BUSY`.
  4. An in-process scheduler queue (`MAX_QUEUED_BRIDGE_COMMANDS = 32`).
  5. Mutating commands are refused when the panel heartbeat advertises an incompatible command schema (`CEP_SCHEMA_INCOMPATIBLE`) or when `<tempDir>/.host-recovery.json` exists (`HOST_RECOVERY_REQUIRED`).
     - The engine's raw calls are non-mutating unless `mutating` or `mutationOnTimeout` is passed, so they skip these gates.
     - But an engine crash that abandons the lease can create a recovery record, and that record then blocks the MCP server's own mutating tools until `acknowledge_operation_recovery` is run. [INF from `host-lease.js`]
  6. The response size is capped at 1 MiB (`MAX_BRIDGE_RESPONSE_BYTES`).
- Net: the imports will resolve and calls will work if the engine passes a string to `buildToolScript`, and if the bridge directory passes the ACL check (the default `%TEMP%\premiere-mcp-bridge` should). **Pin the exact version** (`premiere-pro-mcp@1.27.0`). Internal modules are not a public API, and they change almost weekly.

**(2) What happens when `timeoutMs` fires?**
- The Node side resolves `{success:false,…}`. Its `finally` block unlinks `cmd_`, `res_`, `busy_` and `.staged` files for that id. [SRC]
- If the panel has not claimed the command yet, the unlink removes it and it never runs. 1.27.0 does this explicitly with `cancelQueuedBehindLivePanel` (rename to `.cancelled`), reporting `not_applied` versus `claim_race`. [SRC]
- If the panel has already claimed it, **the ExtendScript keeps running inside Premiere**. Neither version has any cancel path: CSInterface.evalScript offers none, and the code never attempts one. [SRC for absence; INF for the CEP limitation]
- When the script finishes, the panel writes `res_<id>.json`. Nobody reads it, and it stays an orphan until the next server start runs `cleanupTempDir`.
- UUID ids mean a late result **cannot be mixed up with a later request**. [SRC]

**The 874-cut, 819 s loop.** With `timeoutMs: 300000` the hard cap is `max(1 200 000, 120 000)` = **1 200 s**, so an 819 s script succeeds as long as `busy_<id>.json` keeps refreshing.
- The 1.27.0 panel source warns that a host call blocking CEP's event loop "also stalls the heartbeat". If that happens, 1.14.1 gives up at the 300 s soft deadline (the busy file goes stale after 6 s) while the loop continues in Premiere. 1.27.0 reports "stuck" after 10 s of stale heartbeat. [SRC + INF]
- If the engine saw a timeout around 300 s, a stalled heartbeat is the likely cause. If it saw around 1 200 s, it hit the hard cap. [INF]

**(2b) Is a second command queued or run concurrently?**
- **1.14.1:** the Node side has no queue. The panel calls `processOneCommand` for **every** `cmd_*.jsx` it finds each 200 ms tick, so several `evalScript` calls are dispatched at once. Premiere's ExtendScript engine is single-threaded, so they run one after another in the host [INF].
  - Each queued command's busy timer starts at dispatch, so a command waiting behind a long one shows a fresh busy file. Its timeout therefore stretches toward the hard cap instead of failing fast. [SRC]
- **1.27.0:** the panel holds a `commandInFlight` flag and dispatches strictly one at a time. The Node side adds the scheduler queue and the cross-process lease. [SRC `cep-plugin/main.js` ~l.315]

**(3) Pickup, naming, locking and modal dialogs.** [SRC]
- Pickup is a 200 ms poll in both the panel and the headless engine.
- Naming: `cmd_<uuid>.jsx`, `res_<uuid>.json`, `busy_<uuid>.json`, `helpers_<md5>.jsx`. In 1.27.0 a `.headless.jsx` suffix routes a command to the headless engine, and the panel publishes `bridge-heartbeat.json` every second.
- Locking is by atomic rename on claim. The panel publishes responses by staged rename. Stale files are cleaned at server start; there is no per-request reuse risk.
- A modal dialog blocks evalScript, so no response arrives. The busy file stays fresh (if CEP's event loop is not blocked) and the bridge waits until the hard cap, then returns the "modal dialog" error.
- In 1.27.0, `get_bridge_telemetry` reports `blocking.state` (`likely_blocked_by_dialog`, `stuck`, and so on) without sending a command.

**(4) Progress and asynchronous jobs.**
- 1.14.1 has only the internal busy-file heartbeat. There are no MCP progress notifications and no asynchronous job tool. [SRC: grep finds no progress in `server.js`]
- 1.25.0+ adds [SRC]:
  - MCP `notifications/progress` every 10 s while the busy file is fresh, when the request has a progressToken (`HOST_HEARTBEAT_INTERVAL_MS`).
  - `get_bridge_telemetry`.
  - `export_sequence_job_start` and `get_export_job_status`.
  - `get_last_operations`.
  - `idempotency_key`.

**(5) What does `export_sequence` call?** See §3.6.
- In 1.14.1 it is `seq.exportAsMediaDirect(outputPath, presetPath, ENCODE_ENTIRE|ENCODE_WORKAREA)`. That is a direct, synchronous render that **blocks the ExtendScript engine for the whole encode** [SRC; the blocking is per Adobe's docs, DOC]. The return value is ignored.
- `app.encoder.encodeSequence` (AME queue) appears only in `add_to_render_queue` and `encode_*` in 1.14.1, and in `export_sequence_job_start` in 1.27.0. QE is used only for stills. [SRC]
- "AME still encoding" after a timeout probably came from a separately queued AME job, such as `add_to_render_queue` or `start_batch_encode` [INF].

### 2.7 Tool counts [SRC]
- I counted tool definitions as `^        <name>: {` followed by a `description:` line in `dist/tools/*.js`.
- **1.14.1: 369 definitions.** The package description says 319 core; `--help` says 317 in the default profile. The rest are UXP or unsafe-gated.
- **1.27.0: 522 definitions.** The description says 444 core; `--help` says 442 in the default profile. 153 tools are new and none were removed.
- `PREMIERE_MCP_TOOL_PACKS` (full, essential, inspection, delivery, captions) reduces what is advertised.
- Coverage includes captions (`captions.js`; `create_caption_track`, `read_sequence_captions`), markers, effects, transitions, keyframes, audio (`add_audio_keyframes`, `setup_ducking`, `detect_silence` via `execFile("ffmpeg", …)` with no shell), transcripts (`*_transcript_uxp`, which need UXP; 1.27.0 adds `transcribe_clip_uxp` and `import_transcript_uxp`), MOGRT and After Effects (1.27.0), and interchange formats (FCPXML, AAF, OMF, EDL).

### 2.8 Telemetry and security summary [SRC]
- PostHog telemetry is **off unless `POSTHOG_API_KEY` is set**, in both 1.14.1 and 1.27.0 (`dist/telemetry.js`). No key is hardcoded (grep for `phc_` found nothing).
- Network listeners:
  - None in default stdio mode.
  - UXP WebSocket on 127.0.0.1:7777, only when `PREMIERE_UXP_TOKEN` is set.
  - HTTP on 0.0.0.0:3000, only in `start:http` mode, with a bearer token.
- Outbound connections: the CEP panel's update check (GitHub, later npm). In 1.27.0, `--check-update` and `--update` query the npm registry only when you run those flags. [SRC `dist/update.js`]
- Files written:
  - `%TEMP%\premiere-mcp-bridge\*`.
  - `%APPDATA%\Adobe\CEP\extensions\MCPBridgeCEP`.
  - HKCU `CSXS.9`–`14` PlayerDebugMode.
  - In 1.27.0, token and lease state in the bridge directory.
- Arbitrary code: `execute_extendscript` and `evaluate_expression` when `unsafe-script` is enabled, plus anything that can write to the bridge directory, plus the CEP debug port.

---

## 3. The skill's seven defects, explained from source

### 3.1 apply_edit_plan inserts the whole clip and still returns applied:true
1.14.1 `dist/tools/edit-plans.js` [SRC]:
```js
// validateEditPlan: insert_clip checks only item_id, start_seconds, video/audio_track_index
mutations.push(`seq.insertClip(item${index}, __secondsToTicks(${operation.start_seconds}).toString(), ${operation.video_track_index ?? 0}, ${operation.audio_track_index ?? 0}); results.push({index:${index}, type:"insert_clip", applied:true});`);
...
return buildToolScript(`... return __result({applied:true, operations:results});`);
```
- The operation schema has **no source in/out**. The `plan` parameter is `{type:"object"}` with no properties, so `in_seconds` and `out_seconds` are **silently ignored**.
- `insertClip` places the project item's full range, or its current source In/Out marks.
- `applied:true` is hard-coded, with no readback.

1.27.0 [SRC]:
- `OPERATION_KEYS.insert_clip = ["type","item_id","start_seconds","video_track_index","audio_track_index"]`, and unknown keys now **throw** ("operation N has unknown key(s) …").
- Inserts go through `__insertClipHonoringSyncLock` with readback (`verified:true`).
- There is still **no ranged insert in edit plans**. Ranged edits instead use:
  - `create_subclip` (verified with frame snapping in 1.27.0) followed by an insert;
  - `trim_clip` after the insert;
  - `overwrite_clip`;
  - `ripple_remove_timeline_ranges`, which removes ranges from a timeline already laid out;
  - `create_silence_cut_source_stringout_uxp` (Premiere 26.3+, UXP).

### 3.2 add_to_timeline_batch leaves 1-frame fragments while reporting verified:true
1.14.1 `dist/tools/competitor-gaps.js` [SRC]:
- Each placement checks only two things: some new track item has the matching `projectItem`, and `|actualStart - requested| <= 1 frame`.
- It counts `addedCount` but **never fails when more than one item appears on a track**. A split remnant is exactly such an extra item.
- The single-clip `add_to_timeline`, by contrast, fails when `afterVideoCount > beforeVideoCount + 1` ("residual frame fragment").
- Start times go through `Math.round(seconds*254016000000)` without snapping to the sequence frame. A start that is off-frame, or within one frame of an existing cut, splits the neighbouring clip and leaves a sub-frame or one-frame piece that still passes the tolerance check [INF].
- Clips are sorted ascending and inserted with ripple semantics, so a later insert can split earlier ones. Nothing re-reads earlier placements.

Fixes: 1.16.1 split-plus-insert handling and 1.19.0 final re-read ("If a later insert moves or splits an earlier clip, the result reports … `committed_unverified`") [DOC, confirmed in 1.27.0 source by `finalReadback` and `driftedPlacements`]. 1.20.0 adds timebase snapping for UXP inserts [DOC]. CEP-side frame snapping for batch inserts was not confirmed [UNK].

### 3.3 remove_from_timeline leaves linked audio behind
1.14.1 `dist/tools/timeline.js` [SRC]:
```js
var clip = result.clip;
clip.remove(${args.ripple ? "true" : "false"}, ${args.ripple ? "true" : "false"});
```
- This removes one TrackItem only. Linked partners are never looked up.
- The changelog for 1.19.0 adds that `TrackItem.remove(true, …)` "never rippled and left gaps and stray audio while reporting success". [DOC]

1.27.0 [SRC]: `__removeClipAndPartners(result, include_linked !== false)` with linked partners included by default. Ripple goes through the verified sync-locked `rippleDeleteScriptBody`, and there is a readback that every removed id is gone.

### 3.4 delete_sequence fails
1.14.1 `dist/tools/sequence.js` [SRC]:
- It loops over **`project.rootItem.children` only**, so a sequence inside a bin is never found ("Sequence not found").
- It matches by `item.name === seq.name`, so duplicate names can pick the wrong sequence.
- It calls `project.deleteSequence(seq)` and ignores the return value.

1.27.0 [SRC]: resolves the sequence through `__findSequence` (id or name) anywhere in the project, checks nested usage (`confirm_remove_from_sequences`), checks `accepted === false`, and **reads back** that the sequence is gone.

### 3.5 export_frame fails ("no still presets")
1.14.1 `__exportStillFrame` in `dist/bridge/script-builder.js` [SRC]:
- Path 1 calls QE `qeSeq.exportFramePNG(outputPath, w, h)`. **That is the wrong signature.** The 1.15.2 changelog says QE takes `(timecodeString, pathWithoutExtension)`, and the old call "returned false without writing a file, so every frame export fell through to the Media Encoder fallback" [DOC, consistent with source].
- Path 2, the fallback, calls `__findStillPreset()`. It searches only:
  - `C:\Program Files\Adobe\Adobe Media Encoder*\MediaIO\systempresets`;
  - `C:\Program Files\Adobe\Adobe Premiere Pro*\Settings\IngestPresets`;
  - `Documents\Adobe\Adobe Media Encoder\*\Presets`.

  It does **not** search Premiere's own `MediaIO\systempresets`. Without AME, or with a non-default install path, it reports "AME: no PNG still preset found on disk".
- Fixed by 1.15.2 (QE signature) and 1.23.0 (Premiere `MediaIO/systempresets` fallback). 1.20.0 also improved `export_frame_uxp`. [DOC + SRC in 1.27.0 lines ~1659–1680]
- The `C:\Program Files\Adobe` root is still hard-coded in 1.27.0. [SRC]

### 3.6 export_sequence ignores work_area_only
1.14.1 [SRC]: `seq.exportAsMediaDirect(outputPath, presetPath, args.work_area_only ? app.encoder.ENCODE_WORKAREA : app.encoder.ENCODE_ENTIRE)` and then `return __result({ exported: true, … })`. There is no check of the work-area state and no check of the result.
- If the work-area bar is disabled or unset, Premiere encodes the whole sequence. The 1.19.0 changelog: "Unset or full-sequence work areas previously still called ENCODE_WORKAREA and could write the entire timeline as a verified work-area export." [DOC]
- 1.21.0 adds that **Premiere 26.5.2 ignores the CEP work-area point setters**, so the work area cannot be set reliably through ExtendScript. [DOC]

1.27.0 [SRC]: a `range` enum (`entire`, `in_to_out`, `work_area`). `work_area` fails closed unless the work area is enabled and covers part of the sequence. **Use `range: "in_to_out"`** after `set_sequence_in_out_points` (or `seq.setInPoint` / `setOutPoint`), which is reliable. Output is verified by file size and an ffprobe duration check to within one frame.

### 3.7 export_sequence times out at ~480 s while the encode continues
1.14.1 [SRC]: `sendCommand(script, { ...bridgeOptions, timeoutMs: 120000 })`, and the hard cap `Math.max(120000*4, 120000)` = **480 000 ms**. exportAsMediaDirect is synchronous inside the ExtendScript engine, so for long sequences the call simply outlives the cap. The render keeps going and the late result file is discarded.

1.27.0 [SRC]: `timeout_minutes` (default 15, maximum 240), plus `export_sequence_job_start` and `get_export_job_status`. These queue an AME job with `app.encoder.encodeSequence`, bind encoder events into `$.global.__premiereMcpAmeExportJobsV1`, and later verify the output by AME completion event, two stable file-size checks and ffprobe duration. Requirements: a saved project, an explicit `.epr` preset (not "Same as Project"), a new output path, and at most 32 jobs per process. Jobs are lost if the server restarts (`server_restarted`).

---

## 4. GitHub repository: leancoderkavy/premiere-pro-mcp

- https://github.com/leancoderkavy/premiere-pro-mcp: **470 stars, 84 forks, 1 open issue, 7 open PRs**, MIT. The page lists v1.25.0 as the latest GitHub release (npm has 1.27.0). [DOC, from the repo page fetched 2026-11-01]
- Issues: **175 in total, 174 closed**. The only open one is #911, "[Windows][Claude Desktop] v1.25.0 MCPB fails server/discover, while npm stdio works", opened 2026-10-25. [DOC, from the issues page]
- Issues that match the skill's defects (all closed) [DOC]:
  - #9 "capture_frame / export_frame fail on Premiere Pro 2026 AND 2025" (closed 2026-07-21)
  - #189 AME preset scan misses presets
  - #237 "Structural-edit tools report success without changes" (08-28)
  - #240 "Project-panel delete and nesting tools don't perform their operations" (08-28)
  - #238 Media Encoder export ignores absolute output path
  - #294 server and panel use different bridge directories
  - #562 insert_from_source ignores sync lock
  - #581 1.16.x fails to start on Windows (ACL check under AppData; fixed)
  - #687 "All render/export paths fail on Premiere 26.5.2 (Windows, scripted session)" (10-02)
  - #713 and #729 import_media / relink_media hang and wedge the CEP bridge
  - #728 apply_edit_plan token replayable
  - #841 export_sequence without preset_path picks a proxy preset (10-09)
  - #880 "Workflow gaps from long-form episode edits … doubled edits after client timeouts" (10-24)
  - #925 ripple_remove_timeline_ranges Stack overrun (10-31)
- Commit activity, from my clone of git history [SRC: `pkg-mcp/repo-ppmcp`, `git log`]:
  - About 1,370 commits.
  - By month: 7 in 2026-02, 10 in 03, 1 in 05, 109 in 07, 217 in 08, **614 in 09**, **416 in 10**.
  - By author: leancoderk 995, Kavy Rattana 148, Daniel Jesusegun 131, dependabot 31, "Cursor Agent" 23, copilot-swe-agent 12, cursor[bot] 7, plus about 9 small contributors.
  - HEAD is `c2370d7`, 2026-10-31, "Merge pull request #940 from leancoderkavy/release/v1.27.0".
  - In practice it is one maintainer, Kavy Rattana, with heavy AI-agent-assisted development and a very high rate of change.
- Quality signals:
  - The CHANGELOG is unusually candid. Many entries say "tested with a mocked bridge only; not yet verified in a live Premiere host".
  - Many fixes are reported from live testing on 25.2.3 and 26.5.1/26.5.2, mostly on macOS. Windows-specific live verification is thinner. [DOC]
  - The user's 26.3.2 is not named in any live test matrix I saw [UNK].

---

## 5. Other Premiere Pro MCP servers and bridges

### 5.1 Comparison table

| Project | Distribution | Transport (verified) | Tools | Last activity | Licence | Stars | Premiere 25/26 | Notes |
|---|---|---|---|---|---|---|---|---|
| **leancoderkavy/premiere-pro-mcp** (the user's) | npm `premiere-pro-mcp` | CEP panel + file bridge (`cmd_*.jsx`/`res_*.json`, 200 ms poll); optional UXP over token-authenticated WebSocket on 127.0.0.1:7777 [SRC] | 369 (1.14.1) / 522 (1.27.0) definitions [SRC] | 1.27.0 on 2026-10-31 [SRC] | MIT | 470 [DOC] | CEP host 14.0+; UXP 25.6+ [SRC]; live-tested 25.2.3 and 26.5.x [DOC] | 6k downloads a week; telemetry opt-in; asynchronous export added in 1.25 |
| **hetpatel-11/Adobe_Premiere_Pro_MCP** https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP | npm `adobe-premiere-pro-mcp` 1.2.11 (2026-10-24), 4,638 downloads a week [SRC] | CEP panel + file bridge (`command-<uuid>.json` / `response-<uuid>.json`, staged rename, `bridge-heartbeat.json`; the command carries `timeoutMs` for a panel watchdog that defaults to 45 s) [SRC `src/bridge/index.ts` l.1159-1215] | 283 (115 + 168). Only 5 are advertised by default; the rest go through `search_tools` / `invoke_tool`, or `PREMIERE_MCP_TOOLSET=full` [DOC KNOWN_ISSUES.md] | 2026-10-24 [SRC git] | MIT | 799, 150 forks, 21 open PRs [DOC] | CEP manifest `PPRO [14.0,99.9]`, CSXS 10 [SRC]; live-verified on 26.0.2 [DOC]; UXP "experimental" [DOC] | **Telemetry ON by default** to `https://adobe-premiere-mcp-telemetry.hetkp8044.workers.dev/v1/event` (opt out with `PREMIERE_MCP_TELEMETRY=0` or `DO_NOT_TRACK=1`); payload allowlist includes tool, success, duration, error_detail [SRC `src/utils/telemetry.ts`]. Export uses `app.encoder.encodeSequence` (AME queue) [SRC l.2111]. Has `execute_extendscript`. **Its bin is also named `premiere-pro-mcp`, which collides with the user's package if both are installed globally** [SRC package.json] |
| **mikechambers/adb-mcp** https://github.com/mikechambers/adb-mcp | source only (Python MCP via `uv`; Node proxy; UXP plugin) | Python MCP ↔ Socket.IO **proxy on port 3001** ↔ UXP plugin (Premiere `minVersion 25.6.0`) [SRC] | **26 Premiere tools** (`mcp/pr-mcp.py`): import, create sequence, add media, set start/end times, close gaps, a few effects, transitions, export_sequence, export_frame [SRC] | 2026-07-08; most work in 2025 [SRC git] | MIT | 735 [DOC] | 25.6+ (UXP) [SRC] | Self-described "proof of concept", single sequence [DOC]. **The proxy calls `server.listen(3001)` with no host and no auth, so it binds all interfaces** [SRC `adb-proxy-socket/proxy.js`]. Export uses UXP `EncoderManager.exportSequence(…, IMMEDIATELY, …)` [SRC]. 15 open issues, none Premiere-specific [DOC] |
| **ayushozha/AdobePremiereProMCP** https://github.com/ayushozha/AdobePremiereProMCP | source only; `@premierpro/mcp-server` **is not on npm** [SRC registry 404] | Go orchestrator + Rust media engine + Python intelligence + TS bridge (gRPC on 127.0.0.1:50054); the CEP panel hosts a **WebSocket server on 127.0.0.1:9801 with token auth** (`cep-panel/src/panel.js` l.423-470) [SRC]; also a UXP panel | Claims 1,066 schemas / 935 host commands; default "standard" profile of 74 [DOC] | 2026-10-05 [SRC git] | MIT | 135, 5 open issues [DOC] | Manifest 14.0+; only 26.5.2 macOS has tested workflows [DOC] | Has both `encodeSequence` and `exportAsMediaDirect` paths [SRC]. Heavy multi-runtime install. NickCocoa fork exists [DOC] |
| **IsaiahDupree/premiere-pro-mcp** https://github.com/isaiahdupree/premiere-pro-mcp | source; package name `premiere-pro-mcp` v1.1.1 in package.json [SRC] | Same file-bridge design and file layout as leancoderkavy 1.1.x (`src/bridge/file-bridge.ts`, `cep-plugin/main.js`, `fly.toml`) [SRC]; **INF: a derivative or fork of the user's package at about 1.1.1** | "300 tools, 30 modules" [DOC] | 2026-03-27 [SRC git] | [UNK] | [UNK] | [UNK] | Stale; no reason to prefer it |
| **MauricePutinas/premiere-pro-mcp-claude-code** https://github.com/MauricePutinas/premiere-pro-mcp-claude-code | source + .mcpb | CEP extension runs an **HTTP server on 127.0.0.1** (`client/main.js` l.223-234) [SRC]; host `PPRO [25.0,99.9]` [SRC] | 59 tools [DOC commit message] | One commit, 2026-06-21 [SRC] | [UNK] | [UNK] | 25.x | Single-drop project with Remotion intros; unmaintained |
| **matrayu/adobe-mcp** https://github.com/matrayu/adobe-mcp | source (Python) | Reuses the adb-mcp style socket client/proxy (`adobe_mcp/shared` socket_client) [SRC] | 19 Premiere tools [SRC count of `@mcp.tool`] | 2026-01-17 [SRC] | [UNK] | [UNK] | UXP (inherited) | Derivative of adb-mcp [INF] |
| **qmasingarbe/pymiere** https://github.com/qmasingarbe/pymiere | PyPI `pymiere` 1.4.1 (2023-05-10) [SRC] | Python → **unauthenticated HTTP POST to 127.0.0.1:3000** "Pymiere Link" CEP panel, which evals `to_eval` [SRC `pymiere/core.py` l.13, l.97] | Full ExtendScript object wrapper (not MCP) | Last commit 2025-03-05 [SRC] | GPL-3.0 | 473, 21 issues [DOC] | Tested up to 23.1 (2023); README: "Pymiere is not maintained anymore" [DOC] | Not an MCP server; useful only as a reference |
| **Adobe "Adobe for creativity" connector** https://blog.adobe.com/en/publish/2026/04/28/adobe-for-creativity-connector | Hosted remote MCP in Claude (launched 2026-04-28) | Cloud APIs (Express/Firefly class) [DOC] | "50+ tools" across Creative Cloud [DOC] | — | proprietary | — | Does not drive desktop Premiere projects; reviewers describe resize/reframe-class video operations [DOC: petapixel.com 2026-04-28; mindstudio.ai] | Not a substitute. An Adobe community feature request for an official Premiere MCP is still open [DOC: community.adobe.com/feature-requests-730/…-1644303] |

Other names found but not inspected: NickCocoa/AdobePremiereProMCP (a fork of ayushozha) [DOC]; the LobeHub listing `ppmcp-premiere-pro-mcp` points to the leancoderkavy package [DOC]; "premiere-remote" and similar returned nothing significant [UNK].

### 5.2 How the alternatives compare on the skill's pain points
- **Asynchronous or long export:** the user's 1.27.0 (`export_sequence_job_start`) and hetpatel (encodeSequence returns a jobID; job-status tooling not inspected [UNK]) both queue AME jobs. adb-mcp uses UXP `EncoderManager.exportSequence` with `IMMEDIATELY` [SRC]; whether that call blocks is [UNK].
- **Ripple multi-range cutting** (the skill's ExtendScript loop): only the user's package (≥1.20) has a dedicated, verified tool, `ripple_remove_timeline_ranges`. It takes up to 50 ranges per call, batches QE razors in groups of 8 from 1.27.0, relinks A/V and reads back the result [SRC/DOC].
- **Verification honesty:** in the source I read, leancoderkavy 1.27.0 has the most systematic readback contract (`verified`, `committed_unverified`, `mutationOutcome`). hetpatel also has heartbeat handling and writes long comments about false-success fixes [SRC].
- **Same failure modes:** hetpatel shares the CEP file-bridge model, so it has the same "a modal dialog blocks everything" and "evalScript cannot be cancelled" limits [SRC/INF].

---

## 6. Recommendations

1. **Upgrade to `premiere-pro-mcp@1.27.0` and pin it exactly.** Then:
   - Fully quit Premiere and run `premiere-pro-mcp --install-cep`. Connector changes require reinstalling the panel, and a mismatched panel makes mutating tools refuse with `CEP_SCHEMA_INCOMPATIBLE`.
   - Make sure the panel's temp-dir field matches `PREMIERE_TEMP_DIR`.
   - Run `premiere-pro-mcp --doctor` and `verify_premiere_connection`.
2. **Change the skill's tool usage:**
   - `export_sequence` → `export_sequence_job_start` + `get_export_job_status` for full-length renders, or `export_sequence` with `timeout_minutes`. Use `range: "in_to_out"` instead of `work_area_only`.
   - The ExtendScript cut loop → `ripple_remove_timeline_ranges` (preview, then apply with the token; 50 ranges per call, so chunk the 874 cuts). Alternatively keep the raw loop but send it in chunks well under the hard cap.
   - Ranged inserts → `create_subclip` then insert, or insert then `trim_clip`. Do not put in/out fields in `apply_edit_plan`.
   - Re-test `delete_sequence`, `export_frame` and `remove_from_timeline`. All were fixed per the source.
3. **For the engine's direct imports:**
   - Pass a string to `buildToolScript`.
   - Expect `HOST_LEASE_BUSY` when the MCP server is mid-command.
   - Choose `timeoutMs` knowing that the real wait ceiling is `max(4×timeoutMs, 120 s)` while the busy heartbeat stays fresh.
   - Treat a timeout as "outcome unknown". The script may still be running in Premiere.
   - Consider a pre-flight `get_bridge_telemetry`-style check of `busy_*` and heartbeat files before resending.
4. **Do not switch to hetpatel's package** unless its search_tools/invoke_tool model fits better. If you do, set `PREMIERE_MCP_TELEMETRY=0`, and remember that its bin name collides with this package's. Do not use adb-mcp's proxy on an untrusted network.
5. **Security hygiene:**
   - Keep `unsafe-script` enabled only if the skill needs `execute_extendscript`.
   - Know that PlayerDebugMode stays enabled for CSXS 9–14 after uninstall.
   - Keep the bridge directory private. 1.27.0 enforces this on Windows.
