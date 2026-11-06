'use strict';
// Stage 1 offline tests: synthetic data only, no network, no browser. Node.js 18+.
const assert = require('node:assert/strict'), fs = require('node:fs'), os = require('node:os'), path = require('node:path'), b = require('./bank.cjs');
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'question-synthetic-')), journal = path.join(dir, 'journal.jsonl');
const fixture = JSON.parse(fs.readFileSync(path.join(__dirname, '../assets/example.json'), 'utf8'));
const four = [{ label: 'A', text: 'Alpha text' }, { label: 'B', text: 'Bravo text' }, { label: 'C', text: 'Charlie text' }, { label: 'D', text: 'Delta text' }];
const q = (n, extra = {}) => ({ ...fixture, position: n, stem: 'Synthetic stem ' + n, ...extra });
const withKey = (n, extra = {}) => q(n, { choices: four, answer: 'C', answerExplicit: true, ...extra });

// --- journal: replay, conflicts, order
assert(b.ingest(journal, q(2))); assert(b.ingest(journal, q(1))); assert(!b.ingest(journal, q(1)));
assert.throws(() => b.ingest(journal, q(1, { stem: 'changed' })), /Conflicting/);
assert.deepEqual(b.recover(journal).records.map(x => x.position), [2, 1]);

// --- no AI / supplements, ever
const rows = Array.from({ length: 13 }, (_, i) => q(i + 1));
assert.throws(() => b.build(rows, { supplements: 'x.json' }), /never adds/);
assert.throws(() => b.build(rows, { supplementRecords: [{}] }), /never adds/);

// --- grouping + deterministic shuffle
const grouped = rows.map((x, i) => ({ ...x, group: i < 4 ? 'passage' : null, passage: i < 4 ? 'Shared synthetic passage' : null }));
const g1 = b.build(grouped, { seed: 8 }), g2 = b.build(grouped, { seed: 8 });
assert.deepEqual(g1.mapping, g2.mapping); assert.equal(new Set(g1.mapping.map(x => x.position)).size, 13);
const posOrder = g1.mapping.map(x => x.position), at = [1, 2, 3, 4].map(p => posOrder.indexOf(p));
assert.equal(Math.max(...at) - Math.min(...at), 3, 'passage group must stay contiguous');
assert.notDeepEqual(b.build(rows, { seed: 8 }).mapping.map(x => x.position), b.build(rows, { seed: 9 }).mapping.map(x => x.position));
assert.deepEqual(b.build(rows, { shuffle: false }).mapping.map(x => x.position), rows.map(x => x.position));

// --- option shuffling, relabelling, answer remapping
const parseStudy = md => md.split('\n---\n\n').filter(x => x.includes('## Question')).map(block => {
  const id = block.match(/<!-- id: ([^;]+?)[ ;]/)[1]; const opts = [...block.matchAll(/^([A-Z])\. (.*?)\s*$/gm)].map(m => ({ label: m[1], text: m[2] }));
  return { id, opts, answer: block.match(/\*\*Source answer:\*\* (.*)/)[1].trim() };
});
const keyed = Array.from({ length: 40 }, (_, i) => withKey(i + 1));
const st = b.build(keyed, { seed: 5 }), parsed = parseStudy(st.study);
assert.equal(parsed.length, 40); let moved = 0;
for (const p of parsed) {
  assert.deepEqual(p.opts.map(o => o.label), ['A', 'B', 'C', 'D'], 'options relabelled in order');
  assert.equal(p.opts.find(o => o.label === p.answer).text, 'Charlie text', 'answer follows its option text');
  if (p.opts[0].text !== 'Alpha text') moved++;
}
assert(moved > 10, 'options actually shuffled'); assert.equal(st.optionsShuffled, 40);
assert(!/^#+\s*(?:Question\s*)?\d/m.test(st.study) && !/Question \d/.test(st.study), 'study file is not numbered');
// multi-answer and text answers
const multi = b.remapAnswer(withKey(1, { answer: 'A, C' }), [2, 0, 3, 1]); assert.deepEqual(multi, { ok: true, answer: 'A, B' });
assert.deepEqual(b.remapAnswer(withKey(1, { answer: 'Delta text' }), [3, 2, 1, 0]), { ok: true, answer: 'A' });
assert.equal(b.remapAnswer(withKey(1, { answer: 'unrelated prose' }), [0, 1, 2, 3]).ok, false);
const noKey = b.build([withKey(1, { answer: null, answerExplicit: false })], { seed: 1 }); assert(noKey.study.includes('Not displayed by the source.'));
// position-dependent questions stay in source order
const aota = withKey(1, { choices: [...four.slice(0, 3), { label: 'D', text: 'All of the above' }], answer: 'D' });
const both = withKey(2, { choices: [...four, { label: 'E', text: 'A and C' }], answer: 'E' });
const stemRef = withKey(3, { stem: 'Which of statements A to C is right (option B)?' });
const explRef = withKey(4, { explanation: 'Option B is wrong because...' });
const bad = withKey(5, { answer: 'free text answer' });
const keep = b.build([aota, both, stemRef, explRef, bad], { seed: 3 });
assert.equal(Object.values(keep.optionsKept).reduce((a, c) => a + c, 0), 5); assert.equal(keep.optionsShuffled, 0);
for (const m of keep.mapping) { const o = m.optionOrderBySourceLabel.split(','); assert.deepEqual(o, [...o].sort(), 'kept questions keep source order'); assert(m.optionsKeptInSourceOrder); }
assert(parseStudy(keep.study).every(p => p.opts[0].text === 'Alpha text'));
assert.equal(b.build(keyed, { seed: 5, shuffleOptions: false }).optionsShuffled, 0);

// --- validation guards
assert.throws(() => b.validate(q(3, { images: ['../secret.png'] })), /Unsafe/); assert.throws(() => b.validate(q(3, { answer: 'A', answerExplicit: false })), /explicitly/);

// --- export: source files immutable, study file separate, audit, protected output
b.ingest(journal, q(3, { stem: 'Repeated synthetic stem' })); b.ingest(journal, q(4, { stem: 'Repeated synthetic stem' }));
b.ingest(journal, withKey(6, { stem: 'Keyed synthetic stem' }));
const report = b.exportBank(journal, path.join(dir, 'export'), { expected: { [fixture.exam]: 7 }, date: '2026-01-01', sourceLocation: 'Synthetic' });
assert.equal(report.duplicates.length, 1); assert(report.issues.some(x => x.includes('missing position 5')) || report.issues.some(x => x.includes('count')));
const exp = path.join(dir, 'export'); for (const f of ['exam_1.md', 'questions_shuffled.md', 'collection_audit.md']) assert(fs.existsSync(path.join(exp, f)), f);
assert(!fs.existsSync(path.join(exp, 'study.md')));
const src = fs.readFileSync(path.join(exp, 'exam_1.md'), 'utf8'); assert(src.indexOf('Synthetic stem 2') < src.indexOf('Synthetic stem 1') === false, 'source file in source order');
assert(/Exam index: e1 = /.test(fs.readFileSync(path.join(exp, 'questions_shuffled.md'), 'utf8')));
assert(report.shuffle.optionsShuffled >= 1 && report.mapping.length === 5);
assert.throws(() => b.exportBank(journal, exp), /already exists/);
assert.throws(() => b.exportBank(journal, path.join(dir, 'x2'), { supplements: 'a.json' }), /never adds/);

// --- torn-tail recovery, copied assets
fs.appendFileSync(journal, '{"exam":'); assert(b.recover(journal).torn); assert.equal(b.recover(journal).records.length, 5); assert.throws(() => b.ingest(journal, q(9)), /Torn/);
const repaired = path.join(dir, 'repaired.jsonl'); for (const row of b.recover(journal).records) b.ingest(repaired, row); assert.equal(b.recover(repaired).records.length, 5);
const image = path.join(dir, 'assets', 'synthetic.txt'); fs.mkdirSync(path.dirname(image)); fs.writeFileSync(image, 'synthetic asset');
b.ingest(repaired, q(7, { images: ['assets/synthetic.txt'] })); b.exportBank(repaired, path.join(dir, 'images')); assert(fs.existsSync(path.join(dir, 'images/assets/synthetic.txt')));
console.log('PASS (Stage 1): replay, conflicts, recovery, no-AI guard, group + option shuffling, answer remapping, position-dependent options, unnumbered output, exports, copied assets. Workspace: ' + dir);
