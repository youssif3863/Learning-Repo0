---
name: etymology
description: Break a word into its meaningful parts and explain it in English and Arabic — part-by-part meanings, literal reconstruction, accepted Arabic term, short English and Arabic definitions, and what the word means in the user's own context (the book, handout, slide or conversation it came from). Use whenever the user says "Etymology", asks what a term's parts mean, why something is called what it is, what a prefix, suffix or combining form means (-itis, -ectomy, hepato-, dys-), wants medical terms from a lecture, slide, screenshot or list broken down, or asks in Arabic (أصل الكلمة، تفكيك المصطلح، معنى المقطع، ليه اسمها كده) — even without the word "etymology". Covers medical terminology and general vocabulary, eponyms, acronyms and Arabic words. Not for plain translation, spelling or pronunciation requests unless the user also wants the breakdown.
---

# Etymology — English & Arabic

Help the learner understand and remember a word by showing what each part means, what the parts say literally, what the word means today, and what it means *where the learner met it*. Most users are Arabic-speaking medical students reading English textbooks and lecture notes, so the answer should be short, bilingual and easy to scan. The user's requested depth, language and format always win over these defaults.

The learner wants the meaning, not a history lesson: skip origin languages (Greek, Latin, etc.) and historical commentary unless they ask. Use that knowledge silently to get the breakdown right.

## Workflow

1. **Pin the term and its sense.** If a spelling correction is clear, show it briefly and proceed. Ask one focused question only if illegibility or several plausible senses would make the answer useless.
2. **Look for the context before writing.** Check the conversation, uploaded files, book pages, handouts, slides and screenshots for where this word appears. If it appears there, read the surrounding sentence or section so you can say what the word means *in that passage* — this is often what the learner actually needs. Never pretend to have read something you have not seen, and never invent a context.
3. **Classify how the name was formed:** analyzable word, compound, eponym, acronym, fixed phrase, or Arabic word built on a root and pattern. Do not force a Greek/Latin breakdown on a word that isn't built that way.
4. **Split into meaningful parts, in original order.** Use real prefixes, roots/combining forms and suffixes; do not force every word into all three. A connecting vowel (the *-o-* in *gastr-o-enter-o-logy*) has no meaning of its own, so leave it out of the table.
5. **Reconstruct the literal sense** in English and natural Arabic.
6. **Define it now** in one short sentence each, English and Arabic. Give the accepted Arabic term in the heading — a translation alone is not a definition. For medical terms, use `references/medical-affixes.md` so Arabic equivalents stay consistent (e.g. *-otomy* بَضْع, *-ectomy* استئصال, *-ostomy* فَغْر).
7. **Add the context meaning** from step 2, if found.
8. **Add at most one short distinction** when it truly helps — a commonly confused term or a sibling word with a different ending. Skip it when there is nothing useful to say.

## Default response — one term

**[Term] — [accepted Arabic term]**

| Part | English meaning | المعنى بالعربية |
| --- | --- | --- |
| [component in original order] | [meaning] | [Arabic meaning] |

**Literally:** [English literal meaning] → «[Arabic literal meaning]».

**English definition:** [one short sentence].

**التعريف بالعربية:** [one short sentence].

**In context:** [only if the word appears in the user's material or conversation — one or two sentences naming the source and explaining what the word means there].

**Important distinction:** [optional, one line].

Keep it brief: about 70–130 words for one ordinary term, plus the context line. Omit any section with nothing useful in it rather than filling it. For an eponym or acronym, replace the table with the naming basis or the expansion. If a literal reconstruction does not apply, skip that line. No quizzes, history or clinical lectures unless asked.

### Worked example (no context available)

**Cholecystectomy — استئصال المرارة**

| Part | English meaning | المعنى بالعربية |
| --- | --- | --- |
| chole- | bile | صفراء |
| cyst- | bladder, sac | كيس / مثانة |
| -ectomy | surgical removal | استئصال |

**Literally:** removal of the bile sac → «استئصال كيس الصفراء».

**English definition:** Surgical removal of the gallbladder.

**التعريف بالعربية:** عملية جراحية لإزالة المرارة.

**Important distinction:** cholecyst*otomy* = cutting into the gallbladder (بَضْع) · cholecyst*ectomy* = removing it (استئصال) · cholecyst*ostomy* = making an opening in it (فَغْر).

### The same term with context

If the user had shared a surgery handout with the line "Laparoscopic cholecystectomy is the treatment of choice for symptomatic gallstones", the answer would add:

**In context:** In your surgery handout, it is the standard operation for gallstones that cause symptoms, done through small keyhole incisions (استئصال المرارة بالمنظار).

Other cases — an eponym, an acronym, a misleading literal meaning, an Arabic word — are in `references/examples.md`. Read it when the term is not a straightforward analyzable word.

## Several terms at once

When the user gives a list, a slide or a screenshot with **four or more** terms, use one compact table instead of a block per term:

| Term | Breakdown | Meaning | المصطلح العربي |
| --- | --- | --- | --- |
| hepatomegaly | hepat- (liver) + -megaly (enlargement) | enlarged liver | ضخامة الكبد |

Then add short notes only where a term needs one (a misleading literal meaning, a common confusion), and a one-line context note if the terms came from the user's material. When terms share a part, point it out once. With two or three terms, use the one-term format for each. For a quick follow-up ("and *-ostomy*?"), answer briefly in the same style.

## Arabic quality and layout

- Prefer standard Arabic medical terminology (the *Unified Medical Dictionary* / المعجم الطبي الموحد tradition) and clear Modern Standard Arabic. Add an Egyptian Arabic gloss only when it helps or is requested. Avoid awkward word-for-word calques.
- An established Arabic term beats the literal pattern: *anemia* is فقر الدم, not «انعدام الدم».
- Use diacritics only where a word would otherwise be misread (بَضْع "incision" vs بِضْع "a few").
- Mixed right-to-left and left-to-right text scrambles easily. Keep Arabic in its own labelled line or in the last table column. When an English term must appear inside an Arabic sentence, put it in parentheses after the Arabic: التهاب الكبد (hepatitis).

## Accuracy

A learner taught a false part will mis-read other words too, so:

- Never split a word from spelling resemblance alone, and never invent roots, meanings or named people.
- Keep literal meaning, accepted Arabic term, modern definition and context meaning distinct. If the literal meaning misleads, say so in one short clause (*-oma* means "mass", yet a hematoma is not a tumour).
- **Eponyms:** name the person; do not split surnames into roots. **Acronyms:** expand and translate the expansion. **Arabic words:** use the real root (جذر) and pattern (وزن), not a prefix/suffix model.
- If unsure about a part's meaning, check a reliable dictionary or medical terminology reference rather than guessing. Never imply a lookup happened when it did not. If something cannot be confirmed, say so briefly.
- Do not add pronunciation unless asked.

## Final self-check

Every part is genuine and in original order; connectors carry no meaning; English and Arabic definitions agree; Arabic terms are standard and render cleanly; context meaning is included when the word appears in the user's material; and the answer is short.
