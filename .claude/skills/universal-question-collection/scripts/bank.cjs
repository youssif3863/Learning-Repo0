'use strict';
// Stage 1 utility. Offline only. Node.js 18+, standard library.
// Never contacts a website, never controls a browser and NEVER generates or adds questions.
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const unavailable = 'Not displayed by the source.';
const LABELS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const hash = x => crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex');
const key = q => JSON.stringify([q.exam, q.position]);

// ---------------------------------------------------------------- record contract
function validate(q) {
  if (!q || typeof q.exam !== 'string' || !q.exam.trim() || !Number.isInteger(q.position) || q.position < 1 ||
      typeof q.stem !== 'string' || !q.stem.trim()) throw Error('Invalid occurrence identity or stem');
  if (!Array.isArray(q.choices) || !q.choices.length || q.choices.some(c => typeof c.label !== 'string' || typeof c.text !== 'string'))
    throw Error('Invalid ordered choices');
  if (new Set(q.choices.map(c => c.label)).size !== q.choices.length) throw Error('Duplicate choice labels');
  for (const k of ['answer', 'explanation']) if (q[k] !== null && typeof q[k] !== 'string') throw Error('Missing or invalid ' + k);
  if (typeof q.answerExplicit !== 'boolean' || q.answer !== null && !q.answerExplicit) throw Error('Answer is not explicitly identified by source');
  for (const p of q.images || []) if (typeof p !== 'string' || /^(?:[a-z]+:|[\\/])|(?:^|[\\/])\.\.(?:[\\/]|$)/i.test(p)) throw Error('Unsafe image path');
  return q;
}

function recover(file) {
  const records = [], seen = new Map(); let torn = false;
  if (!fs.existsSync(file)) return { records, torn };
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  for (let i = 0; i < lines.length; i++) {
    if (!lines[i].trim()) continue; let q;
    try { q = JSON.parse(lines[i]); } catch (e) { if (i === lines.length - 1) { torn = true; break; } throw Error('Malformed journal line ' + (i + 1)); }
    validate(q); const k = key(q);
    if (seen.has(k)) { if (seen.get(k) !== hash(q)) throw Error('Conflicting source occurrence ' + k); continue; }
    seen.set(k, hash(q)); records.push(q);
  }
  return { records, torn };
}

function ingest(file, q) {
  validate(q); const s = recover(file);
  if (s.torn) throw Error('Torn final record: recover valid prefix to a new journal first');
  const old = s.records.find(r => key(r) === key(q));
  if (old) { if (hash(old) !== hash(q)) throw Error('Conflicting source occurrence'); return false; }
  fs.mkdirSync(path.dirname(path.resolve(file)), { recursive: true });
  const prefix = fs.existsSync(file) && fs.statSync(file).size && !fs.readFileSync(file, 'utf8').endsWith('\n') ? '\n' : '';
  const fd = fs.openSync(file, 'a'); try { fs.writeSync(fd, prefix + JSON.stringify(q) + '\n'); fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
  return true;
}

// ---------------------------------------------------------------- deterministic shuffling
function shuffled(a, seed) {
  let s = seed >>> 0; const rand = () => ((s = (Math.imul(s, 1664525) + 1013904223) >>> 0) / 4294967296);
  a = [...a]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rand() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a;
}
const qSeed = (q, seed) => ((seed >>> 0) ^ parseInt(hash([q.exam, q.position]).slice(0, 8), 16)) >>> 0;

// Options that only make sense in their original positions must never be reordered.
const POS_OPTION = [
  /\b(?:all|none|both|neither|either|any)\s+of\s+(?:the\s+)?(?:above|these|those|them|previous)\b/i,
  /\b(?:all|none)\s+(?:the\s+)?above\b/i,
  /\b(?:the\s+)?(?:above|previous|preceding)\s+(?:are|is|options?|choices?|statements?|answers?)\b/i,
  /^\s*(?:[Bb]oth\s+)?\(?[A-E]\)?(?:\s*(?:,|&|\+|and|or)\s*\(?[A-E]\)?)+\s*\.?\s*$/,
  /\b(?:[Oo]ptions?|[Cc]hoices?|[Aa]nswers?|[Ss]tatements?)\s+\(?[A-E]\)?(?![A-Za-z])/,
];
const POS_STEM = /\b(?:[Oo]ptions?|[Cc]hoices?|[Ss]tatements?)\s+\(?[A-E]\)?(?![A-Za-z])/;
const POS_EXPL = /\b(?:[Oo]ptions?|[Cc]hoices?|[Aa]nswers?)\s+\(?[A-E]\)?(?![A-Za-z])|(?:^|\s)\(?[A-E]\)\s|\b[Bb]oth [A-E]\b|\b[A-E]\s+(?:is|are)\s+(?:correct|incorrect|wrong|right|true|false)\b/;

function optionKeepReason(q) {
  if (q.choices.length < 2) return 'single option';
  if (q.choices.length > LABELS.length) return 'more than 26 options';
  if (q.choices.some(c => POS_OPTION.some(r => r.test(c.text)))) return 'position-dependent options (e.g. "all of the above", "A and C")';
  if (POS_STEM.test(q.stem) || (q.passage && POS_STEM.test(q.passage))) return 'stem refers to options by letter';
  if (q.explanation && POS_EXPL.test(q.explanation)) return 'source explanation refers to option letters';
  return null;
}

// Map the source answer onto the new labels. Returns {ok, answer}.
function remapAnswer(q, order) {
  if (q.answer === null || q.answer === undefined) return { ok: true, answer: null };
  const norm = s => s.trim().replace(/[().\s]/g, '').toUpperCase();
  const newLabel = oi => LABELS[order.indexOf(oi)];
  const labels = q.choices.map(c => norm(c.label));
  const toks = q.answer.split(/\s*(?:,|;|&|\+|\band\b)\s*/i).map(norm).filter(Boolean);
  if (toks.length && toks.every(t => labels.includes(t)))
    return { ok: true, answer: toks.map(t => newLabel(labels.indexOf(t))).sort().join(', ') };
  const lowered = q.answer.trim().toLowerCase();
  let i = q.choices.findIndex(c => c.text.trim().toLowerCase() === lowered);
  if (i >= 0) return { ok: true, answer: newLabel(i) };
  const m = q.answer.match(/^\s*\(?([A-Za-z0-9]{1,3})[.)]\s+(.*)$/);
  if (m) { i = labels.indexOf(norm(m[1])); if (i >= 0 && q.choices[i].text.trim().toLowerCase() === m[2].trim().toLowerCase()) return { ok: true, answer: newLabel(i) }; }
  return { ok: false };
}

// ---------------------------------------------------------------- Markdown rendering
const idOf = (q, examIndex) => `e${examIndex.get(q.exam)}-p${q.position}`;
function body(q, choices, answer, examIndex, extra = '') {
  const passage = q.passage ? q.passage.split('\n').map(l => '> ' + l).join('\n').replace(/^> /, '> **Passage** — ') + '\n\n' : '';
  const opts = choices.map(c => c.label + '. ' + String(c.text).replace(/\n/g, '  \n   ')).join('  \n');
  const images = (q.images || []).map(p => '![Source figure](' + p.replace(/\\/g, '/') + ')').join('\n');
  return `## Question\n\n<!-- id: ${idOf(q, examIndex)}${q.group ? '; group: ' + q.group : ''}${extra} -->\n\n${passage}${q.stem}\n\n${opts}\n\n${images ? images + '\n\n' : ''}` +
    `**Source answer:** ${answer ?? unavailable}\n\n**Source explanation:** ${q.explanation ?? unavailable}\n`;
}
// Source files: original order, original labels (immutable audit copies).
function render(q, examIndex) { return body(q, q.choices, q.answer, examIndex); }
// Study file: relabelled A, B, C… in the given order, answer remapped. No numbering.
function renderStudy(q, order, answer, examIndex) {
  const choices = order.map((oi, i) => ({ label: LABELS[i] ?? q.choices[oi].label, text: q.choices[oi].text }));
  return body(q, choices, answer, examIndex);
}

function build(records, cfg = {}) {
  if (cfg.supplements || cfg.supplementRecords) throw Error('Supplements are not supported: this skill never adds generated questions');
  const exams = new Map(); for (const q of records) { validate(q); if (!exams.has(q.exam)) exams.set(q.exam, []); exams.get(q.exam).push(q); }
  const examIndex = new Map([...exams.keys()].map((e, i) => [e, i + 1]));
  const sources = [], groups = [], groupMap = new Map();
  for (const [exam, rows] of exams) {
    rows.sort((a, b) => a.position - b.position); sources.push([exam, rows]);
    for (const q of rows) { const g = q.group ? JSON.stringify([exam, q.group]) : key(q); if (!groupMap.has(g)) { groupMap.set(g, []); groups.push(groupMap.get(g)); } groupMap.get(g).push(q); }
  }
  const seed = cfg.seed ?? 2026, ordered = cfg.shuffle === false ? groups : shuffled(groups, seed);
  const doOptions = cfg.shuffle !== false && cfg.shuffleOptions !== false;
  const study = [], mapping = [], kept = {}; let count = 0, optionsShuffled = 0;
  for (const group of ordered) for (const q of group) {
    let order = q.choices.map((_, i) => i), reason = doOptions ? optionKeepReason(q) : 'option shuffling disabled';
    if (doOptions && !reason) {
      order = shuffled(order, qSeed(q, seed));
      const r = remapAnswer(q, order);
      if (!r.ok) { reason = 'source answer could not be mapped to a label'; order = q.choices.map((_, i) => i); }
    }
    let answer = q.answer;
    if (reason) { kept[reason] = (kept[reason] || 0) + 1; if (q.choices.length <= LABELS.length) { const r = remapAnswer(q, order); if (r.ok) answer = r.answer; } }
    else { answer = remapAnswer(q, order).answer; optionsShuffled++; }
    study.push(renderStudy(q, order, answer, examIndex)); count++;
    mapping.push({ studyOrder: count, id: idOf(q, examIndex), exam: q.exam, position: q.position,
      optionOrderBySourceLabel: order.map(i => q.choices[i].label).join(','), optionsKeptInSourceOrder: reason });
  }
  return { sources, study: study.join('\n---\n\n'), mapping, examIndex, optionsShuffled, optionsKept: kept };
}

function exportBank(journal, out, cfg = {}) {
  const s = recover(journal); if (s.torn) throw Error('Repair torn final record before export');
  if (fs.existsSync(out)) throw Error('Output directory already exists');
  const b = build(s.records, cfg), issues = [], dups = new Map(), assetRoot = path.dirname(path.resolve(journal)), expected = cfg.expected || {};
  const missingExams = Object.keys(expected).filter(e => !b.sources.some(([title]) => title === e)); for (const e of missingExams) issues.push(`${e}: captured 0 / ${expected[e]}`);
  for (const [exam, rows] of b.sources) {
    if (expected[exam] !== undefined && expected[exam] !== rows.length) issues.push(`${exam}: count ${rows.length} / ${expected[exam]}`);
    const positions = new Set(rows.map(q => q.position)); const bound = expected[exam] ?? Math.max(...positions);
    for (let i = 1; i <= bound; i++) if (!positions.has(i)) issues.push(`${exam}: missing position ${i}`);
    for (const q of rows) {
      const h = hash([q.stem, q.passage ?? null, q.choices]); if (!dups.has(h)) dups.set(h, []); dups.get(h).push(key(q));
      for (const issue of q.issues || []) issues.push(key(q) + ': ' + issue);
      for (const image of q.images || []) {
        const p = path.resolve(assetRoot, image);
        if (!p.startsWith(assetRoot + path.sep) || !fs.existsSync(p) || !fs.statSync(p).isFile()) issues.push(key(q) + ': Required source image not captured: ' + image);
        else if (!fs.realpathSync(p).startsWith(fs.realpathSync(assetRoot) + path.sep)) throw Error('Asset symlink escapes root');
      }
    }
  }
  fs.mkdirSync(out, { recursive: true }); let index = 0;
  for (const [exam, rows] of b.sources) {
    const status = expected[exam] === undefined ? 'Listed count unknown' : expected[exam] === rows.length ? 'Count matched; consult audit' : 'Incomplete';
    fs.writeFileSync(path.join(out, `exam_${++index}.md`), `# ${exam}\n\nCapture date: ${cfg.date || 'Unspecified'}  \nSource location: ${cfg.sourceLocation || 'Unspecified'}  \nListed count: ${expected[exam] ?? 'Unknown'}  \nCaptured count: ${rows.length}  \nStatus: ${status}\n\n` + rows.map(q => render(q, b.examIndex)).join('\n---\n\n'));
  }
  for (const q of s.records) for (const image of q.images || []) {
    const p = path.resolve(assetRoot, image);
    if (fs.existsSync(p) && fs.statSync(p).isFile()) { const dest = path.join(out, image); fs.mkdirSync(path.dirname(dest), { recursive: true }); fs.copyFileSync(p, dest); }
  }
  const header = `# Shuffled question set\n\nCaptured: ${cfg.date || 'Unspecified'} · Source: ${cfg.sourceLocation || 'Unspecified'} · Questions: ${s.records.length}\n\n` +
    `Exam index: ${[...b.examIndex].map(([e, i]) => `e${i} = ${e}`).join('; ')}\n\n` +
    `<!-- Stage 1 output. Questions and options are shuffled and unnumbered; options are relabelled A, B, C...; source answers are remapped to the new labels. Stage 2 reads this file. -->\n\n---\n\n`;
  fs.writeFileSync(path.join(out, 'questions_shuffled.md'), header + b.study);
  const report = {
    captured: s.records.length, torn: s.torn, issues,
    unavailable: s.records.filter(q => q.answer === null || q.explanation === null).map(q => ({ exam: q.exam, position: q.position, answer: q.answer === null, explanation: q.explanation === null })),
    duplicates: [...dups.values()].filter(x => x.length > 1), provenance: s.records.map(q => ({ exam: q.exam, position: q.position })),
    shuffle: { questionsShuffled: cfg.shuffle !== false, optionsShuffled: b.optionsShuffled, optionsKeptInSourceOrder: b.optionsKept },
    mapping: b.mapping, lastSaved: s.records.at(-1) ? { exam: s.records.at(-1).exam, position: s.records.at(-1).position } : null,
  };
  fs.writeFileSync(path.join(out, 'collection_audit.md'), '# Collection audit\n\nReview all count, image, text and missing-field issues before claiming completion. Null answers/explanations were unavailable at the source. The mapping shows, for each shuffled question, the source option order.\n\n```json\n' + JSON.stringify(report, null, 2) + '\n```\n');
  return report;
}

module.exports = { validate, recover, ingest, build, exportBank, render, renderStudy, remapAnswer, optionKeepReason };
if (require.main === module) {
  try {
    const [cmd, file, arg, config] = process.argv.slice(2);
    if (cmd === 'ingest') console.log(ingest(file, JSON.parse(fs.readFileSync(arg, 'utf8'))) ? 'Saved' : 'Already saved');
    else if (cmd === 'recover') console.log(JSON.stringify(recover(file), null, 2));
    else if (cmd === 'export') console.log(JSON.stringify(exportBank(file, arg, config ? JSON.parse(fs.readFileSync(config, 'utf8')) : {}), null, 2));
    else throw Error('Usage: bank.cjs ingest JOURNAL RECORD | recover JOURNAL | export JOURNAL NEW_OUT [CONFIG]');
  } catch (e) { console.error(e.message); process.exitCode = 1; }
}
