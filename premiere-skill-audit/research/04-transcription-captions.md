# 04 — Local transcription, alignment, VAD and captioning for YMnotes

Research date: 2026-11-01. Nothing was installed or run on a user machine. Package sources were downloaded to
`/tmp/claude-0/-home-user-Learning-Repo0/3391813e-183a-5a64-8aab-0e6817637581/scratchpad/research/pkg-asr/` and read only (no downloaded code was run).

Evidence labels:
- **VERIFIED-FROM-SOURCE (VFS)**: read in the downloaded code or files.
- **DOCUMENTED (DOC)**: stated in official docs, a README, a model card or a release note.
- **INFERRED (INF)**: my reasoning from the evidence.
- **UNKNOWN (UNK)**: not established.

Sources read locally:
- faster-whisper 1.2.1 wheel (PyPI)
- whisperX 3.8.6 sdist
- stable-ts 2.19.1 sdist
- silero-vad 6.2.3 sdist
- whisper.cpp git HEAD `482279b` (2026-10-30). Header version 1.9.5; latest tag v1.9.5.
- ctc-forced-aligner git HEAD (2026-09-07)
- Adobe's Premiere transcript JSON schema (`PremierePro_transcript_format_spec.json`)

---

## 0. Known facts about the workstation (from the coordinator, taken from the skill's own benchmark of 2026-09-03)

| Item | Value |
|---|---|
| CPU | AMD Ryzen 7 5700U (Zen 2, 8 cores / 16 threads, AVX2, no AVX-512) |
| RAM | 15.3 GiB |
| GPU | AMD Radeon **integrated** graphics (Vega 8 class, GCN 5). **No NVIDIA** (cuda_device_count=0). No NPU: the Ryzen AI NPU only exists from the 7040 series onward (INF). |
| OS / Python | Windows, Python 3.12.10 |
| Current stack | faster-whisper 1.2.1 + CTranslate2 4.8.2, `large-v3-turbo`, CPU int8 |
| Measured speed | real-time factor (RTF) about 1.01: a 60 min lecture takes about 61 min |
| Measured quality | Arabic is usable. English medical terms often come out as **Arabic-script phonetic spellings**, which is poor for captions. |
| Shorts skill | already passes `--prompt-terms` (initial_prompt) |

What follows for this machine:
- Every CUDA-only path is irrelevant: faster-whisper GPU, WhisperX GPU, the NeMo models, and Qwen3-ASR with vLLM.
- The only GPU route is **Vulkan** through whisper.cpp/ggml. CTranslate2 has no Vulkan backend, and no ROCm backend on Windows (INF, from CTranslate2's CUDA-only GPU requirements in the faster-whisper README).

---

## 1. Executive decision summary

1. **Keep faster-whisper as the engine. Change how it is called.**
   - It is already installed. It is MIT-licensed. It bundles Silero VAD v6 as ONNX, so no torch is needed (VFS).
   - `BatchedInferencePipeline` with `compute_type="int8"` is the cheapest speed-up available on CPU. The README's CPU table shows int8 going from 1m42s sequential to 51s with `batch_size=8`, about 2x (DOC, small model, i7-12700K).
   - Expect roughly 1.5–2.5x on the 5700U, so a 60 min lecture would take about 25–40 min (INF; this must be benchmarked on the machine).
   - Caveats (VFS):
     - Batched mode forces `condition_on_previous_text=False` and ignores `hallucination_silence_threshold` (transcribe.py line 546–547).
     - It applies `initial_prompt` **to every 30 s chunk**, which helps the English-term problem (lines 182–191).
     - Open issues: "BatchedInferencePipeline segments are much larger than normal model" and a punctuation-merge bug (DOC, issue list).
2. **The English-in-Latin-script problem is the main quality issue. No local switch fixes it fully.** Options, best first:
   - (a) A **code-switched style prompt**. Write Arabic sentences that contain the lecture's English terms in Latin script, and pass them as `initial_prompt` (per chunk in batched mode) and/or `hotwords` (prepended to every window, VFS). Whisper copies the style of its prompt (DOC, OpenAI prompting guide). Effect size UNK; test it on 3–5 minutes of a lecture.
   - (b) **Post-correction against a glossary.** Map Arabic-script transliterations (e.g. "كود" to "code") to the Latin terms from the lecture's glossary. Do it word by word so the word timestamps survive. Claude Code can do this step, but the transcript text then goes to Anthropic's cloud (the same exposure as the current metadata step).
   - (c) A **fine-tuned code-switching Whisper**: `mohammedaly22/whisper-large-v3-turbo-egyptian-code-switching`.
     - MIT, safetensors, May 2026. Same turbo size, so roughly the same CPU speed.
     - Trained so that English words stay in English.
     - **No WER is published.** It was trained on only 12k samples (DOC).
     - It must be converted once with `ct2-transformers-converter` (needs transformers and torch in a separate venv) or `convert-h5-to-ggml.py` for whisper.cpp.
     - Worth an A/B test on one lecture.
   - Do **not** set `language="en"`; it translates. Do **not** rely on `multilingual=True`: there is an open issue, "multilingual=True silently returns translated text unless condition_on_previous_text=False" (DOC, Aug 2026).
3. **whisper.cpp with Vulkan on the Radeon iGPU is plausible but unproven for Vega 8.**
   - Since PR #3492 (merged 2025-11-01, in v1.8.3+), whisper.cpp selects `GGML_BACKEND_DEVICE_TYPE_IGPU` devices (VFS, `src/whisper.cpp` lines 1314 and 1384).
   - The PR author claims "3–4x better RTF" on a Radeon 680M (RDNA2) and on Intel Arc iGPUs, with no absolute timings (DOC).
   - No Vega 8 / 5700U benchmark was found (UNK).
   - **There is no official Windows Vulkan binary.** The release workflow builds only CPU, OpenBLAS, CUDA 11.8/12.4 and arm64 zips (VFS, `.github/workflows/release.yml`). Options are to build it yourself (VS Build Tools + Vulkan SDK + `cmake -DGGML_VULKAN=1`) or to trust a third-party zip (supply-chain risk).
   - Worth one hour of `whisper-bench` on the real machine before committing to it.
4. **Arabic word timestamps.**
   - Whisper's cross-attention DTW (faster-whisper `word_timestamps=True`; whisper.cpp `-dtw large.v3.turbo`) works on any script. Accuracy for Arabic has never been published (UNK). The general literature puts it at roughly 100–300 ms tolerance (DOC, arXiv 2505.15646 notes evaluations use tolerances above 200 ms).
   - Wav2vec2 forced alignment (WhisperX) uses an **Arabic-only vocabulary** (`jonatasgrosman/wav2vec2-large-xlsr-53-arabic`). Latin-script English words are mapped to a "wildcard" emission column in v3.8 (VFS), so they get only loose timing.
   - The MMS-based `ctc-forced-aligner` romanizes both scripts (uroman) and handles mixed text, but its default model is **CC-BY-NC-4.0** (VFS, HF API). That is a licence risk for a monetised channel.
   - For 30–60 s Shorts, faster-whisper word timestamps plus a short manual or Claude review is the pragmatic route.
5. **Premiere cannot transcribe Arabic.** Adobe's own transcript JSON schema lists 29 language codes and **no Arabic**; unsupported languages must use `"??-??"` (VFS). Speech to Text runs on-device (DOC, since 22.2), but that does not help here.
6. **Captions for long lectures: upload the SRT/VTT straight to YouTube.** That means the YouTube Data API `captions.insert` (DOC). Premiere's Arabic RTL caption rendering has a long history of reversed or disjointed text (DOC, community threads 2018–2025), so it is better avoided.
   - ExtendScript `Sequence.createCaptionTrack(projectItem, startAtTime, [captionFormat])` does exist (DOC) if a caption track inside Premiere is ever needed.
   - The new "Import Static Transcript" JSON route in Premiere has no scripting API ("not yet", Adobe, Aug 2025).
7. **Shorts karaoke: burning in with ffmpeg + libass is a robust alternative to Premiere text.**
   - libass has required HarfBuzz unconditionally since 0.15.0 (DOC, Changelog), so Arabic letters join correctly.
   - The ffmpeg `subtitles`/`ass` filter has `shaping=complex` (VFS, `vf_subtitles.c`).
   - Use one ASS event per word-highlight state, not `\kf` sweeps. Karaoke fill follows logical order, so it sweeps the wrong way for RTL (DOC, Subtitle Edit PR #12274).
8. **stable-ts is archived** (2026-05-30, "Development … indefinitely paused", DOC). Use it as a reference only. Port its regroup ideas instead of depending on it.

---

## 2. Comparison table: transcription engines

| Candidate | Version / date | License | Windows CPU | AMD iGPU (this machine) | Word timestamps | VAD | Install complexity | Local? |
|---|---|---|---|---|---|---|---|---|
| **faster-whisper** (SYSTRAN) https://github.com/SYSTRAN/faster-whisper | 1.2.1 (2025-10-31, PyPI). No release in 12 months. 5 open issues (DOC) | MIT | Yes (CTranslate2 wheels, int8/AVX2) | **No** (CUDA only) | Yes, cross-attention DTW (`find_alignment`, `median_filter_width=7`) VFS | Silero v6 ONNX bundled (`assets/silero_vad_v6.onnx`) VFS | Low (already installed). Deps: ctranslate2, onnxruntime, av, tokenizers, huggingface-hub (VFS METADATA) | Yes after the model download |
| **whisper.cpp** (ggml-org) https://github.com/ggml-org/whisper.cpp | v1.9.5 (Oct 2026) | MIT | Yes (official `whisper-bin-x64.zip`, BLAS zip) | **Yes via Vulkan, self-built or third-party** | `-ml 1 -sow` segment splitting, plus `-dtw large.v3.turbo` token DTW; `-ojf` JSON with token times (VFS) | Built-in Silero (`--vad -vm ggml-silero-v6.2.0.bin`) VFS | Medium (Vulkan needs VS Build Tools + Vulkan SDK) | Yes |
| **WhisperX** (m-bain) https://github.com/m-bain/whisperX | 3.8.6 (2026-05-25). 178 open issues (DOC) | BSD-2 | Yes (`--device cpu --compute_type int8`) | No | wav2vec2 CTC alignment. Arabic model exists; Latin words become wildcards (VFS) | pyannote (default, bundled weights) or Silero via `torch.hub` (VFS) | **High**: torch~=2.8, torchaudio, torchcodec, pyannote 4, transformers, nltk (VFS pyproject) | Yes (diarization needs an HF token, which is not needed here) |
| **stable-ts** (jianfch) https://github.com/jianfch/stable-ts | 2.19.1 (2025-08-16). **Archived 2026-05-30** | MIT | Yes | No | Stabilised Whisper timestamps, `align`, `refine` | Loudness mask by default. Silero via `torch.hub.load('snakers4/silero-vad:master')` (VFS) | Medium-high (torch + openai-whisper ≤20250625) | Yes, but VAD fetches remote code |
| **Qwen3-ASR** https://github.com/QwenLM/Qwen3-ASR | 0.6B/1.7B, 2026-01-29 | Apache-2.0 | Transformers backend is possible but slow (INF) | No | ForcedAligner covers 11 languages, **Arabic not included** (DOC) | – | High (GPU-oriented, vLLM recommended) | Yes |
| **Meta Omnilingual ASR** https://github.com/facebookresearch/omnilingual-asr | 0.2.0 (2025-12) | Apache-2.0 | UNK (fairseq2 stack, historically Linux/macOS, INF) | No | CTC/LLM, no word timestamps documented (UNK) | – | High | Yes. Lists `arz_Arab` (third-party doc) |
| **NVIDIA conformer/fastconformer Arabic (NeMo)** https://huggingface.co/nvidia/stt_ar_fastconformer_hybrid_large_pcd_v1.0 | 2025-10 | CC-BY-4.0 | NeMo on Windows is not well supported (INF) | No | CTC timestamps | – | High | Yes. Arabic script only, so English terms are lost (INF) |
| Premiere Speech to Text | Premiere 26.x | proprietary | on-device (DOC) | – | yes | – | – | Local, but **no Arabic** (VFS schema) |

### 2.1 Speed numbers that exist (all DOC unless noted)

| Source | Hardware | Model / config | Audio | Time |
|---|---|---|---|---|
| faster-whisper README | i7-12700K 8 threads | small, fp32 / int8 / int8 batch 8 | 13 min | 2m37s / 1m42s / **51s** |
| same | same | whisper.cpp fp32 / OpenVINO | 13 min | 2m05s / 1m45s |
| same | RTX 3070 Ti | large-v2 fp16 / batch 8 | 13 min | 1m03s / 17s |
| skill benchmark (coordinator) | Ryzen 7 5700U | large-v3-turbo int8, sequential | 60 min | ~61 min (RTF 1.01) |
| whisper.cpp PR #3492 | Radeon 680M / Arc iGPU | Vulkan iGPU vs CPU | – | "3–4x better RTF" (no absolute numbers) |
| maroonmed.com blog (2026-02) | RX 9070 XT (discrete) | whisper.cpp 1.8.3 Vulkan, large | 40–45 min episodes | ~7.5–8x realtime |

Projected for the 5700U (INF, needs measuring):
- faster-whisper turbo int8 **batched** (batch 8, `cpu_threads=8`): about 25–40 min per 60 min lecture. Batched uses more RAM: in the README, 3.6 GB vs 1.5 GB for small, so turbo should still fit in 15 GB.
- large-v3 (32 decoder layers vs 4 in turbo) on CPU: likely RTF 2–4. That is not viable for full lectures, but fine for 60 s Shorts.
- whisper.cpp Vulkan on Vega 8: unknown. Vega 8 has roughly 1.8 TFLOPS FP32, which suggests the encoder could beat 8 Zen 2 cores by a modest factor (INF).

---

## 3. faster-whisper in detail (current engine)

**Code facts (VFS, `faster_whisper/transcribe.py` 1.2.1):**
- `WhisperModel(model, device="auto", compute_type="default", cpu_threads=0, local_files_only=False)`. The model aliases include `large-v3`, `large-v3-turbo`/`turbo` (mapped to `mobiuslabsgmbh/faster-whisper-large-v3-turbo`, which now redirects on HF to `dropbox-dash/faster-whisper-large-v3-turbo`), `distil-large-v3`, and `distil-large-v3.5`.
- **Distil models are English-only** (DOC, distil-large-v3.5 card: "Distil-Whisper English family"). They are useless for Arabic.
- Sequential `WhisperModel.transcribe` defaults: `beam_size=5`, `condition_on_previous_text=True`, `vad_filter=False`, `word_timestamps=False`, `hallucination_silence_threshold=None`, `hotwords=None`, `multilingual=False`.
- `BatchedInferencePipeline.transcribe` defaults: `vad_filter=True`, `batch_size=8`, `without_timestamps=True`. It hard-codes `condition_on_previous_text=False` and `hallucination_silence_threshold=None` (lines 546–547).
  - If VAD is off and `clip_timestamps` is not given, it raises an error for audio longer than 30 s.
  - **Prompting:** in batched mode, `initial_prompt` is encoded and passed as `previous_tokens` to *every* batch (lines 182–191). `hotwords` goes through `get_prompt`.
- `get_prompt` (lines 1532–1565): `hotwords` are prepended after `<|startofprev|>` in **every window** (sequential mode too), truncated to `max_length//2` (about 223 tokens) together with the previous text.
  - In sequential mode, `initial_prompt` is only "previous text" and scrolls out after the first window or two. With `condition_on_previous_text=False` it applies to the first window only (`prompt_reset_since`, lines 1141, 1373–1383).
  - **So the existing `--prompt-terms` (initial_prompt) only affects the start of a sequential run. Use `hotwords` or batched mode to keep the terms active all the way through.**
- Word timestamps (`add_word_timestamps` / `find_alignment`): DTW over the alignment heads stored in the CT2 `config.json`. The turbo conversion includes 6 alignment heads (VFS, HF `config.json`).
  - **Arabic punctuation detail:** `append_punctuations` defaults to `"\"'.。,，!！?？:：”)]}、"`. It does **not** include `،` (U+060C) or `؟` (U+061F). Arabic punctuation may therefore come out as separate zero-length "words" instead of merging into the previous word (VFS defaults; effect INF). Pass `append_punctuations` with `،؛؟` added.
- VAD (`vad.py`): Silero ONNX through onnxruntime. `VadOptions` defaults: threshold 0.5, `min_silence_duration_ms=2000`, `speech_pad_ms=400`, `min_speech_duration_ms=0`. `get_speech_timestamps(audio, VadOptions(...))` returns sample indices and **can be called on its own for pause detection** (see section 6).
- Model files: CTranslate2 `model.bin`. This is not a pickle format, so there is no `torch.load` risk (INF from format). Downloads come from the Hugging Face Hub. Pin `revision` and use `local_files_only=True` after caching.

**Open issues relevant here (DOC, https://github.com/SYSTRAN/faster-whisper/issues, 5 open):**
- "multilingual=True silently returns translated text unless condition_on_previous_text=False" (2026-08-16)
- "BatchedInferencePipeline segments are much larger than normal model" (2025-11-16). Batched segments can run up to about 30 s, so caption segmentation must come from word timestamps.
- "Phantom hearing is prone to occur during multilingual transcription" (2025-07-16). This is a hallucination issue.
- "[FIX INCLUDED] BatchedInferencePipeline.transcribe does not seem to use append_punctuations and prepend_punctuations properly" (2025-02-20)
- "Missing ending of transcription" (2023)

Closed Arabic-tagged issue #954, "Poor output quality and speed when using batched inference" (closed 2024-10), shows that batched quality is worth A/B testing.

**Hallucination in silence:**
- Mitigations: `vad_filter=True` (on by default in batched mode); `hallucination_silence_threshold` (sequential mode only, needs `word_timestamps=True`); `condition_on_previous_text=False`; `compression_ratio_threshold=2.4` and `no_speech_threshold=0.6` (defaults).
- Lectures have long pauses (slides, writing on the board). VAD gating plus a lower `min_silence_duration_ms` (e.g. 500–700 ms) is the main defence (INF).

**How Claude Code would call it:** keep the existing venv. Add `batched` and `hotwords` flags to the existing script, and write JSON shaped like this:
`{segments:[{start,end,text,avg_logprob,no_speech_prob,words:[{start,end,word,probability}]}], info:{language,duration}}`.
Word `probability` is useful for flagging low-confidence words for review.

Suggested call pattern for this machine (INF, needs a benchmark):
```python
from faster_whisper import WhisperModel, BatchedInferencePipeline
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=8, local_files_only=True)
p = BatchedInferencePipeline(m)
segs, info = p.transcribe(wav, language="ar", batch_size=8, word_timestamps=True,
    initial_prompt=CODE_SWITCH_STYLE_PROMPT,  # applied to every chunk in batched mode
    hotwords=" ".join(GLOSSARY_TERMS[:40]),
    vad_parameters={"min_silence_duration_ms": 600, "speech_pad_ms": 200},
    append_punctuations="\"'.。,，!！?？:：”)]}、،؛؟")
```

---

## 4. whisper.cpp in detail (the only GPU path on this machine)

- **Version:** v1.9.5 (GitHub releases page shows 06 Oct; v1.9.4 on 11 Sep). Header `CMakeLists.txt` says 1.9.5 (VFS). MIT.
- **Windows binaries (VFS, `.github/workflows/release.yml`):**
  - `whisper-bin-x64.zip` / `whisper-bin-Win32.zip` (CPU), `whisper-blas-bin-x64.zip` (OpenBLAS)
  - `whisper-bin-win-cuda-12.4.0-x64.zip` / `-11.8.0-x64.zip`
  - arm64 CPU, Adreno OpenCL, and CUDA arm64 builds
  - **No Vulkan build for Windows.** The only official Vulkan artefact is the Linux Docker image `main-vulkan` (DOC README).
  - Third-party Windows Vulkan zips exist, e.g. `CryptoKey98/whispercpp-vulkan-runtime` (1.8.5) and `jerryshell/whisper.cpp-windows-vulkan-bin`. They are unvetted, so prefer building from source.
- **Vulkan build:** `cmake -B build -DGGML_VULKAN=1 && cmake --build build -j --config Release` (DOC README). It needs the Vulkan SDK and MSVC.
- **iGPU selection:** `whisper_backend_init_gpu()` now accepts `GGML_BACKEND_DEVICE_TYPE_IGPU` (VFS, lines 1314/1384, from PR #3492). `-dev N` picks the device and `-ng` forces CPU (VFS `cli.cpp`).
  - One user with an Intel Iris Xe reported the iGPU was not picked up on 1.8.3; the author suspected drivers (DOC, PR thread).
  - A Chinese tool (pyvideotrans) says its latest version dropped AMD-GPU-on-Windows support (DOC, ambiguous).
- **Useful CLI flags (VFS, `examples/cli/cli.cpp`):**
  - `-l ar`
  - `--prompt` and `--carry-initial-prompt` (always prepend the prompt, the equivalent of faster-whisper `hotwords`)
  - `-ml/--max-len`, `-sow/--split-on-word`, `-wt/--word-thold`
  - `-dtw large.v3.turbo` (DTW presets for tiny…large.v3.turbo)
  - `-osrt -ovtt -oj -ojf`
  - `--vad -vm <ggml-silero-v6.2.0.bin> -vt -vspd -vsd`
  - `-fa` (flash attention), `-sns` (suppress non-speech tokens)
- **Word-level timestamps:** `-ml 1` gives per-token segments (README example, "experimental"). For Arabic, add `-sow` so subword tokens are not split mid-word. `-dtw` adds `t_dtw` per token in `-ojf` JSON (VFS). Accuracy for Arabic is UNK.
- **Models:**
  - `download-ggml-model.sh` offers `large-v3-turbo`, `large-v3-turbo-q5_0` and `large-v3-turbo-q8_0` (VFS).
  - Fine-tuned HF models convert with `models/convert-h5-to-ggml.py` (VFS file exists).
  - ggml `.bin` is a custom binary format, not a pickle (INF).
- **Speed evidence:**
  - README benchmark on an i7-12700K: small model on CPU, whisper.cpp fp32 2m05s vs faster-whisper int8 batched 51s. **On CPU, faster-whisper batched int8 is faster.**
  - The case for whisper.cpp here rests entirely on Vulkan offload to the iGPU.
- **How Claude Code would call it:**
  - `whisper-cli.exe -m ggml-large-v3-turbo-q8_0.bin -f lecture16k.wav -l ar --carry-initial-prompt --prompt "<style prompt>" --vad -vm ggml-silero-v6.2.0.bin -ojf -of out`
  - Then parse `out.json`.
  - Benchmark first with `whisper-bench -m … -t 8` on CPU vs Vulkan.

---

## 5. Model choice for Egyptian Arabic + English medical code-switching

### 5.1 Published numbers

**Open Universal Arabic ASR Leaderboard** (Wang et al., arXiv 2412.13788, Dec 2024; https://arxiv.org/html/2412.13788v1; HF Space `elmresearchcenter/open_universal_arabic_asr_leaderboard`). WER/CER in %:

| Model | Avg WER | CV-18 | MGB-2 | SADA (all) | **SADA Egyptian subset WER** |
|---|---|---|---|---|---|
| nvidia/conformer-ctc-large-ar (LM) | **25.71** | 8.80 | 17.20 | 44.52 | **40.97** |
| openai/whisper-large-v3 | 29.87 | 17.83 | 16.26 | 55.96 | 59.28 |
| facebook/seamless-m4t-v2-large | 32.55 | 21.70 | 20.23 | 62.52 | 72.98 |
| openai/whisper-large-v3-turbo | 33.30 | 25.73 | 17.75 | 60.36 | 63.01 |
| openai/whisper-large-v2 | 34.04 | 21.77 | 25.17 | 57.46 | 48.44 |
| openai/whisper-medium | 39.60 | 28.07 | 29.32 | 67.71 | 55.79 |
| facebook/mms-1b-all | 47.86 | 26.52 | 39.16 | 77.48 | 81.94 |
| jonatasgrosman/wav2vec2-large-xlsr (WhisperX's Arabic aligner) | 54.63 | 23.00 | 56.29 | 86.82 | 89.79 |

Reading of this table (INF):
- turbo is about 3.4 WER points worse than large-v3 on average.
- On Egyptian TV speech (SADA), all Whisper models are poor in absolute terms (WER 48–63).
- None of these test sets is code-switched medical lecture speech.
- WER also penalises English words written in Arabic script (and the reverse) inconsistently.

**Code-switched / medical Egyptian:**
- **Clinera ASR Benchmark** (JMIR preprint 96222, March 2026; https://preprints.jmir.org/preprint/96222; full text could not be fetched).
  - 683 Egyptian Arabic–English code-switched medical utterances.
  - Systems: Whisper-large-v3, Whisper-medium, SeamlessM4T v2, Wav2Vec2-large-AR, ArAzn-Whisper-small, ElevenLabs Scribe v1.
  - Best: **ElevenLabs Scribe v1** (cloud), WER 27.8%, medical-term weighted F1 60.5%.
  - "General-purpose multilingual models … almost entirely fail[ed] to recognize medical terms" (DOC via search snippet; exact Whisper numbers UNK).
  - **This is the closest public benchmark to YMnotes content and confirms the observed failure mode.**
- **ArzEn corpus** (LREC 2020, https://aclanthology.org/2020.lrec-1.523). Best hybrid system 30.6% WER (arXiv 2108.12881).
- **ArzEn-LLM** (arXiv 2406.18120) released `ahmedheakl/arazn-whisper-small` (Apache-2.0) and `-medium` (MIT).
- **Perle ASR Code-Switch benchmark** (arXiv 2605.19069, May 2026; https://benchmarklist.com/benchmarks/asr_code_switch_benchmark/). Commercial APIs only. ElevenLabs Scribe v2 has 13.2% mean WER across 4 pairs. The Egyptian-pair breakdown is not on the summary page.

### 5.2 Candidate local models

| Model | Size | Licence | Arabic/English code-switching | Published Egyptian WER | CPU fit | Notes |
|---|---|---|---|---|---|---|
| `large-v3-turbo` (current) | 809M | MIT | Transliterates English into Arabic script (observed, plus model card example) | SADA-Eg 63.0 | RTF ~1 seq | Baseline |
| `large-v3` | 1.55B | MIT | same | SADA-Eg 59.3 | RTF ~2–4 (INF) | Better for Shorts only |
| **`mohammedaly22/whisper-large-v3-turbo-egyptian-code-switching`** https://huggingface.co/mohammedaly22/whisper-large-v3-turbo-egyptian-code-switching | 809M | MIT (training data `MohamedRashad/arabic-english-code-switching` is tagged GPL) | **Designed to keep English in Latin script.** Card example: "code", "Replit", "Agent" | **none published** | same as turbo | Decoder-only fine-tune, 12,180 training samples, safetensors. Needs CT2/ggml conversion. Medical vocabulary untested. |
| `oddadmix/whisper-large-v3-arabic-dialectal-v2` | 1.55B | Apache-2.0 | dialect-focused, code-switching not claimed | Egyptian WER 27.05 / CER 13.4 on its own 200-clip split (`dialect_wer.json`, VFS) | slow | Self-reported in-domain split |
| `MohamedRashad/Arabic-Whisper-CodeSwitching-Edition` | large-v2 | **GPL-3.0** | yes | UNK | slow | Licence is copyleft |
| `ahmedheakl/arazn-whisper-small/medium` | 244M/769M | Apache/MIT | yes (ArzEn) | in Clinera benchmark, numbers UNK | fast | Small model, so lower accuracy (INF) |
| `distil-large-v3/3.5` | – | MIT | **English only** | – | – | Not usable |
| NVIDIA Parakeet / Canary (public) | – | CC-BY-4.0 | **No Arabic** (Canary-1b-v2 covers EU25; Parakeet v3 is European) (DOC, NeMo checkpoint list) | – | – | Not usable. A Riva Parakeet-CTC-1.1B EMEA model with Arabic is NGC-gated (enterprise). |
| `nvidia/stt_ar_fastconformer_hybrid_large_pcd_v1.0` | ~115M | CC-BY-4.0 | Arabic script only | conformer-ctc-large-ar is best on OUAAL Egyptian (41.0) | NeMo, poor on Windows | Would lose English terms entirely (INF) |
| Qwen3-ASR-1.7B/0.6B | 1.7B | Apache-2.0 | Arabic listed, no dialect info; aligner has no Arabic | UNK | GPU-oriented | Not a fit for a CPU-only Windows machine |
| Meta Omnilingual ASR | 300M–7B | Apache-2.0 | `arz_Arab` (third-party listing) | UNK | UNK on Windows | Too immature to adopt here |
| SeamlessM4T v2 | 2.3B | CC-BY-NC-4.0 (INF, Meta licence) | – | SADA-Eg 73.0 | slow | Worse than Whisper |
| MMS-1b-all | 1B | CC-BY-NC-4.0 | – | SADA-Eg 81.9 | – | Worse |

### 5.3 Keeping English terms in Latin script: what actually works

1. **Style prompt** (no install).
   - Mechanism (VFS): in batched mode `initial_prompt` goes to every chunk, and `hotwords` goes to every window in both modes.
   - Content: 1–3 Egyptian Arabic sentences written exactly as the captions should look, with Latin-script English terms, e.g. "النهارده هنتكلم عن heart failure، وال ejection fraction، وإزاي نستخدم ACE inhibitors و beta blockers." Then add the lecture glossary.
   - Whisper follows the prompt's style and spelling. The model only uses the last ~224 tokens (DOC, OpenAI Whisper prompting guide https://cookbook.openai.com/examples/whisper_prompting_guide).
   - Risks: prompt words can be "hallucinated" into silent stretches (INF, known Whisper behaviour). Keep VAD on.
2. **Fine-tuned code-switching turbo** (one-time conversion; see the table).
3. **Glossary post-correction:**
   - Build a per-lecture glossary from the slide titles and topic (Claude already generates metadata).
   - Map Arabic-script transliterations to the Latin term. Fuzzy matching on a romanised form (e.g. uroman / simple Arabic-to-Latin) can be done locally. Claude can review flagged spans.
   - Replace one-to-one at word level so the timestamps survive. When one English term spans two Arabic tokens, merge their start and end times.
4. **Do not** use `language="en"` or rely on `multilingual=True` (it translates; see the open issue).

---

## 6. VAD (pause detection better than amplitude thresholds)

| VAD | Version | Licence | Runtime | Notes |
|---|---|---|---|---|
| **Silero VAD** https://github.com/snakers4/silero-vad | 6.2.3 (PyPI 2026-09-23) | MIT (VFS classifier) | ONNX (several opsets, half precision, OpenVINO variants) or TorchScript; 16 kHz, 512-sample windows (VFS) | The pip package **hard-requires torch** (VFS PKG-INFO). **But faster-whisper already ships `silero_vad_v6.onnx` and runs it with onnxruntime** (VFS). Use `faster_whisper.vad.get_speech_timestamps(decode_audio(path), VadOptions(threshold=0.5, min_silence_duration_ms=300, speech_pad_ms=100))`: no new install, fully local. whisper.cpp also has a ggml port (`ggml-silero-v6.2.0.bin`). |
| pyannote segmentation (via pyannote.audio 4.0.7, 2026-06-30) | – | MIT code, gated HF models (`pyannote/segmentation-3.0`, `speaker-diarization-community-1` CC-BY-4.0, gated "auto") (HF API) | torch | Heavy. WhisperX bundles its own segmentation weights (`assets/pytorch_model.bin`, pickle) so VAD needs no token (VFS). Overkill for a single speaker. |
| webrtcvad | `webrtcvad` 2.0.10 (2017, unmaintained); `webrtcvad-wheels` 2.0.14.post1 (2026-10) | MIT | C extension, 10/20/30 ms frames | GMM-based, more false positives on noise/music than neural VADs (INF/common knowledge) |
| TEN VAD https://github.com/TEN-framework/ten-vad | 1.0.6.9 (PyPI 2026-10-09) | **Apache-2.0 *with additional conditions*** (VFS LICENSE): no deployment that "competes with Agora's offerings" | native lib + ONNX | Claims lower latency than Silero. Licence is not plain OSS; avoid unless needed. |

Recommendation (INF):
- For silence trimming and Shorts cut points, use the Silero ONNX already inside faster-whisper, with `min_silence_duration_ms` set to the editing threshold (e.g. 350–700 ms) and `speech_pad_ms` of 80–150.
- It returns sample offsets, so divide by 16000 for seconds.
- This is much more robust to breaths, keyboard noise and room tone than amplitude gating.

---

## 7. Alignment and word-timestamp accuracy for Arabic

| Method | Arabic support | Code-switched (Latin inside Arabic) | Evidence |
|---|---|---|---|
| faster-whisper `word_timestamps=True` (cross-attention DTW) | Any script | Yes (same decoder) | VFS. Accuracy UNK for Arabic; generally ±100–300 ms (DOC, arXiv 2505.15646 / CrisperWhisper 2408.16589). |
| whisper.cpp `-dtw` / `-ml 1 -sow` | Any script | Yes | VFS. Marked "experimental" in the README. |
| WhisperX wav2vec2 CTC | `"ar": "jonatasgrosman/wav2vec2-large-xlsr-53-arabic"` (VFS `alignment.py` line 46) | **Latin chars are not in the vocabulary, so they map to a wildcard column (max non-blank score per frame)** (VFS lines 183, 272–281) | English medical terms get weak timing. Arabic is not in `PUNKT_LANGUAGES`, so sentence splitting falls back to English punkt (VFS). The aligner model is `pytorch_model.bin` (pickle) only (HF API). |
| ctc-forced-aligner (MahmoudAshraf97) https://github.com/MahmoudAshraf97/ctc-forced-aligner | MMS-300m-1130 with uroman romanisation | **Yes**: both scripts are romanised | VFS. BSD-2 code, but **model is CC-BY-NC-4.0** (HF API). Compiles a pybind11 C++ extension, so it needs MSVC on Windows. Deps: torch, torchcodec, transformers, uroman. |
| stable-ts `align` / `refine` | Any (Whisper-based) | Yes | VFS. Archived. Default regroup splits on `. 。 ? ？ , ，` only, **not `، ؟`** (VFS `result.py` "da" algorithm), so custom regroup strings are needed for Arabic. |
| Qwen3-ForcedAligner | **No Arabic** (11 languages) | – | DOC |

Practical recommendation (INF):
- Long-lecture captions do not need word precision. Segment-level SRT from faster-whisper words regrouped to 42 chars / 2 lines / ≤20 CPS is enough.
- For Shorts karaoke (30–60 s), run `large-v3` or the code-switch turbo with `word_timestamps=True` on the short clip only. Snap word boundaries to Silero speech edges, then clamp each word's minimum duration to about 120 ms.
- This is cheap on CPU because the clip is under 60 s.

---

## 8. Caption production

### 8.1 Segmentation rules

From the Netflix Arabic Timed Text Style Guide (DOC, https://partnerhelp.netflixstudios.com/hc/en-us/articles/215517947):
- **42 characters per line**, at most **2 lines**
- Reading speed **≤20 CPS** for adult content (17 CPS for children's content)
- No space before `، ؟ !`; use the single-character ellipsis "…"

For vertical Shorts, use 1 line of 2–5 words, or about 20–25 characters at 1080 px width (INF, typical karaoke style).

Tools:
- stable-ts regroup syntax (`sg`, `sp`, `sl`, `cm`, `mg`) is a good design model. Reimplementing about 60 lines of regrouping in the existing script avoids depending on an archived package (INF).
- WhisperX `--max_line_width/--max_line_count/--highlight_words` exist (VFS), but bring the heavy stack with them.
- Subtitle Edit (https://github.com/SubtitleEdit/subtitleedit) has a command-line converter and an RTL karaoke fix (PR #12274) (DOC). It is a Windows GUI app first. **INF**: useful for manual QA, not needed in the pipeline.

**RTL text hygiene:**
- In mixed Arabic/English lines, trailing neutral punctuation can jump to the wrong side. Insert U+200F (RLM) at line ends or around Latin runs (DOC, RightSub BiDi guide).
- Use Arabic punctuation `، ؟`.

### 8.2 Long lectures: where the captions should go

- **Recommended: sidecar SRT/VTT uploaded with the YouTube Data API `captions.insert`** (https://developers.google.com/youtube/v3/docs/captions/insert). It is local generation plus the same OAuth the skill already uses for uploads. No Premiere step, no RTL rendering risk, and viewers can turn captions off.
- **Premiere caption tracks:**
  - Manual: drag the SRT onto the timeline, or Captions panel > Import.
  - Scripted: ExtendScript `app.project.importFiles([srt])` then `seq.createCaptionTrack(projectItem, 0, Sequence.CAPTION_FORMAT_SUBTITLE)` (DOC, https://ppro-scripting.docsforadobe.dev/sequence/sequence/; returns boolean).
  - An Adobe employee (2023) said there are no other caption APIs. UXP can read caption tracks but write access is limited (DOC, forum threads). The version that introduced createCaptionTrack is UNK, and it is untested on 26.3.2 (UNK).
- **Premiere Arabic rendering:**
  - Long-standing reports of reversed or disconnected Arabic in captions and SRT imports (DOC, community threads 2018–2025).
  - Fixes: per-track "South Asian and Middle Eastern" text engine (pre-22.1.1); automatic since the 22.1.1 Universal Text Engine; RTL paragraph direction in Essential Graphics.
  - A mid-2025 user still reported unfixed RTL bugs. 2026 status is UNK. **Treat Premiere as risky for Arabic captions; test before automating.**
- **Premiere "Import Static Transcript" (JSON):**
  - Beta announced 2025-08-18. Adobe schema `https://schemas.adobe.com/transcript/v1.0.0`.
  - VFS from the attached spec: required `language`, `segments[{start,duration,language,speaker(uuid),words[{text,start,duration,confidence,eos,tags,type}]}]`, `speakers[{id,name}]`.
  - **The language enum has 29 codes and no Arabic; use `"??-??"`.**
  - No ExtendScript/UXP import API ("not yet", Adobe staff, 2025-08-19).
  - Could give Text-Based Editing on Arabic lectures (a manual import), but nothing more.

### 8.3 Shorts: burned-in karaoke

- **ffmpeg + libass:**
  - libass ≥0.15.0 "Require[s] HarfBuzz unconditionally" (DOC, https://raw.githubusercontent.com/libass/libass/master/Changelog). Latest libass is 0.17.5.
  - ffmpeg `subtitles=file.ass:shaping=complex` (VFS, `vf_subtitles.c` options auto/simple/complex).
  - Arabic joining is handled by HarfBuzz and bidi by FriBidi (DOC).
  - Common Windows full builds (gyan.dev, BtbN) include libass (INF; check with `ffmpeg -filters | findstr subtitles`).
- **Karaoke on RTL:**
  - `\k/\kf` timing follows logical order, so the highlight sweeps visually left-to-right on Arabic (DOC, Subtitle Edit PR #12274).
  - Safer pattern: **one Dialogue event per word-state**, i.e. the whole line re-emitted with the active word coloured via `{\c&H..&}` override tags. Word-level timing then comes straight from the JSON.
  - Mixed English words in a line need an RLM to keep the order stable (INF).
- **Alternative inside Premiere:** keep the existing MOGRT/Essential Graphics karaoke, but generate per-word text from the corrected JSON. The RTL-direction caveat above applies.

---

## 9. Premiere's own Speech to Text

| Question | Answer | Label |
|---|---|---|
| Local or cloud? | On-device since Premiere 22.2 (Feb 2022). Language packs are downloaded once. | DOC (https://www.adobe.com/uk/products/premiere/speech-to-text.html; Adobe community) |
| Arabic? | **No.** The schema's 29-code enum has no `ar-*`. Jan 2026 feature request "Speech to text in Arabic not supported in Premiere Pro 26". Caption translation also lacks Arabic (Oct 2025). | VFS (schema) + DOC (https://community.adobe.com/feature-requests-730/speech-to-text-in-arabic-not-supported-in-premiere-pro-26-1621281) |
| Scriptable? | No public API to start transcription or import transcripts (forum; "not yet"). | DOC |
| Better than Whisper for YMnotes? | Not applicable: no Arabic. | – |

---

## 10. Privacy: what is fully local

| Option | Local after setup? | Network at runtime | Notes |
|---|---|---|---|
| faster-whisper | **Yes** | Only the first model download from HF. Set `local_files_only=True` / `HF_HUB_OFFLINE=1`. | CT2 model, no pickle |
| whisper.cpp | **Yes** | None (download ggml models manually) | Build from source to avoid third-party binaries |
| WhisperX | Mostly | First downloads: HF aligner, NLTK `punkt_tab` (auto `nltk.download` on miss, VFS); **Silero via `torch.hub.load` from GitHub** if `--vad_method silero` (VFS); diarization needs an HF token | Pickle weights (`pytorch_model.bin`) for pyannote VAD and the Arabic aligner. Use torch ≥2.6 `weights_only` defaults (INF). |
| stable-ts | Mostly | `vad=True` runs `torch.hub.load('snakers4/silero-vad:master')`, **fetching and executing remote code from a moving branch** (VFS) | Archived; avoid |
| ctc-forced-aligner | Yes after downloads | HF model download | NC licence |
| Premiere Speech to Text | Yes | – | No Arabic |
| Claude post-correction / metadata | **No**: text goes to Anthropic | – | Transcript text only, not audio |
| ElevenLabs Scribe and other cloud ASR | No | audio uploaded | Best published code-switch WER, but not local |

---

## 11. Security notes (supply chain)

- **HF downloads:** pin `revision=<commit>` for every model. Prefer safetensors or CT2/ggml formats. Note:
  - `jonatasgrosman/wav2vec2-large-xlsr-53-arabic` ships only `pytorch_model.bin` (pickle) plus flax (VFS HF API).
  - `MahmoudAshraf/mms-300m-1130-forced-aligner` ships both safetensors and `.bin`.
  - The code-switch turbo ships safetensors.
- **`torch.hub.load` in WhisperX (silero option) and stable-ts (vad=True)** executes `hubconf.py` from GitHub at runtime (VFS). Avoid it, or pre-populate the hub cache from a pinned commit.
- **Third-party whisper.cpp Vulkan zips:** unsigned binaries from individuals. Build locally.
- **TEN VAD licence:** field-of-use restriction (VFS).
- Model conversion (`ct2-transformers-converter`) loads transformers weights. Do it once in an isolated venv from safetensors.

---

## 12. Recommended plan for this skill (INF unless noted)

1. **Benchmark, half a day, on the user's machine.**
   - faster-whisper turbo int8: sequential vs `BatchedInferencePipeline` (batch 4/8/16, `cpu_threads=8`) on a fixed 10 min excerpt. Record RTF and peak RAM.
   - whisper.cpp CPU vs Vulkan (`whisper-bench`, then a 10 min `whisper-cli` run) if a Vulkan build is acceptable.
2. **Fix the terminology** (largest quality gain). Add a code-switched style prompt plus `hotwords` from the per-lecture glossary. Use batched mode so the prompt applies everywhere. A/B test against the fine-tuned `mohammedaly22/...-egyptian-code-switching` converted to CT2 int8.
3. **Glossary post-correction pass** with word-level replacement that preserves timestamps. Flag words with `probability < 0.5` for Claude/human review.
4. **Lecture captions:** regroup words to ≤42 chars × 2 lines, ≤20 CPS, with Arabic punctuation and RLM hygiene. Write SRT/VTT and upload with YouTube `captions.insert`. Skip Premiere.
5. **Shorts:** re-transcribe each 30–60 s clip with `large-v3` (or the code-switch model) and `word_timestamps=True`. Snap to Silero edges, apply the glossary, then render karaoke with libass (one event per word state) or feed the existing Premiere MOGRT.
6. **Pause detection for editing:** replace amplitude thresholds with `faster_whisper.vad.get_speech_timestamps` (Silero ONNX, already installed).

---

## 13. Source URLs

- faster-whisper: https://github.com/SYSTRAN/faster-whisper ; https://pypi.org/project/faster-whisper/ (1.2.1, 2025-10-31) ; issues https://github.com/SYSTRAN/faster-whisper/issues
- CTranslate2: https://pypi.org/project/ctranslate2/ (4.8.4, 2026-10-25)
- whisper.cpp: https://github.com/ggml-org/whisper.cpp ; releases https://github.com/ggml-org/whisper.cpp/releases ; iGPU PR https://github.com/ggml-org/whisper.cpp/pull/3492 ; v1.8.3 https://github.com/ggml-org/whisper.cpp/releases/tag/v1.8.3
- Vulkan on Windows (third-party): https://www.maroonmed.com/subtitle-edit-and-whisper-cpp-stt-on-amd-and-other-non-nvidia-gpus-with-vulkan/ ; https://github.com/DomoticX/whisper.cpp-windows-vulkan ; https://github.com/CryptoKey98/whispercpp-vulkan-runtime/releases
- WhisperX: https://github.com/m-bain/whisperX ; https://pypi.org/project/whisperx/ (3.8.6)
- stable-ts: https://github.com/jianfch/stable-ts (archived 2026-05-30)
- ctc-forced-aligner: https://github.com/MahmoudAshraf97/ctc-forced-aligner ; model https://huggingface.co/MahmoudAshraf/mms-300m-1130-forced-aligner
- Silero VAD: https://github.com/snakers4/silero-vad ; https://pypi.org/project/silero-vad/ (6.2.3)
- TEN VAD: https://github.com/TEN-framework/ten-vad (LICENSE)
- pyannote: https://pypi.org/project/pyannote.audio/ (4.0.7) ; https://huggingface.co/pyannote/speaker-diarization-community-1
- OUAAL paper: https://arxiv.org/abs/2412.13788 ; https://arxiv.org/html/2412.13788v1 ; leaderboard https://huggingface.co/spaces/elmresearchcenter/open_universal_arabic_asr_leaderboard
- Clinera benchmark: https://preprints.jmir.org/preprint/96222
- ArzEn: https://aclanthology.org/2020.lrec-1.523 ; https://arxiv.org/abs/2108.12881 ; ArzEn-LLM https://huggingface.co/papers/2406.18120
- Code-switch benchmark: https://benchmarklist.com/benchmarks/asr_code_switch_benchmark/ (arXiv 2605.19069)
- Models: https://huggingface.co/mohammedaly22/whisper-large-v3-turbo-egyptian-code-switching ; https://huggingface.co/oddadmix/whisper-large-v3-arabic-dialectal-v2 ; https://huggingface.co/MohamedRashad/Arabic-Whisper-CodeSwitching-Edition ; https://huggingface.co/ahmedheakl/arazn-whisper-small ; https://huggingface.co/nvidia/stt_ar_fastconformer_hybrid_large_pcd_v1.0 ; https://huggingface.co/distil-whisper/distil-large-v3.5 ; https://huggingface.co/dropbox-dash/faster-whisper-large-v3-turbo
- Qwen3-ASR: https://github.com/QwenLM/Qwen3-ASR ; arXiv 2601.21337
- Omnilingual ASR: https://github.com/facebookresearch/omnilingual-asr ; https://huggingface.co/facebook/omniASR-LLM-7B
- NeMo checkpoints (no Arabic Parakeet/Canary): https://docs.nvidia.com/nemo/speech/3.0.0/asr/asr_checkpoints.html
- OpenAI Whisper prompting guide: https://cookbook.openai.com/examples/whisper_prompting_guide
- Word timestamp literature: https://arxiv.org/pdf/2505.15646 ; https://arxiv.org/pdf/2408.16589
- Netflix Arabic TTSG: https://partnerhelp.netflixstudios.com/hc/en-us/articles/215517947
- Premiere ExtendScript Sequence: https://ppro-scripting.docsforadobe.dev/sequence/sequence/
- Premiere transcript import beta + spec: https://community.adobe.com/t5/premiere-pro-beta-discussions/now-in-beta-import-your-own-transcript/m-p/15543866
- Premiere Arabic STT request (2026): https://community.adobe.com/feature-requests-730/speech-to-text-in-arabic-not-supported-in-premiere-pro-26-1621281
- Premiere Arabic caption RTL threads: https://community.adobe.com/t5/premiere-pro-discussions/arabic-characters-not-joining-correctly-in-the-new-captioning-tool/td-p/11908308 ; https://community.adobe.com/t5/premiere-pro-discussions/srt-import-with-right-to-left-language-e-g-hebrew-arabic-text-is-reversed/m-p/15179344
- Premiere STT offline: https://www.adobe.com/uk/products/premiere/speech-to-text.html
- libass Changelog: https://raw.githubusercontent.com/libass/libass/master/Changelog ; ffmpeg vf_subtitles: https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_subtitles.c
- Subtitle Edit RTL karaoke PR: https://github.com/SubtitleEdit/subtitleedit/pull/12274 ; RTL punctuation guide https://github.com/omerninyo/RightSub/wiki/BiDi-and-Plex-Guide
- YouTube captions.insert: https://developers.google.com/youtube/v3/docs/captions/insert
