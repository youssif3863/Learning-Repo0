---
name: etymology
description: Explain where a word comes from and how its parts build its meaning, in English and Arabic — prefix/root/suffix breakdown, origin language, literal reconstruction, accepted Arabic translation, English and Arabic definitions, and contextual meaning. Use whenever the user says "Etymology", asks what a term's parts mean, why something is called what it is, what a prefix, suffix or combining form means (-itis, -ectomy, hepato-, dys-), wants medical terms from a lecture, slide, screenshot or list broken down, or asks in Arabic (أصل الكلمة، تفكيك المصطلح، معنى المقطع، ليه اسمها كده) — even without the word "etymology". Covers medical terminology and general vocabulary, eponyms, acronyms and Arabic words. Not for plain translation, spelling or pronunciation requests unless the user also wants the origin or breakdown.
---

# Etymology — English & Arabic

Help the learner understand and remember a word by separating four things that are easy to blur together: its historical origin, its meaningful structure, its literal sense, and its present-day use. Keep the answer concise, accurate and bilingual. The user's requested depth, language and format always win over these defaults.

Most users are Arabic-speaking learners (often medical students) who meet English/Greek/Latin terminology daily. The goal is durable understanding: once a learner truly knows that *-ectomy* means "cutting out", dozens of terms become self-explanatory. So a correct, transferable breakdown is worth more than an elaborate story.

## Workflow

1. **Pin the term and its sense.** Take it from the current sentence, image or discussion. Use available context without pretending to have read unseen sources. If a spelling correction is clear, show it briefly and proceed. Ask one focused question only if illegibility or several plausible senses would make the answer useless.
2. **Classify how the name was formed:** analyzable word, compound, borrowing, eponym, acronym, fixed phrase, or Arabic word built on a root and pattern. Do not assume Greek or Latin ancestry — many terms are eponyms, borrowings from Arabic, French or German, or modern coinages.
3. **Split into meaningful parts, in original order.** Distinguish prefixes, roots/combining forms and suffixes where they exist; do not force every word into all three. A connecting vowel (the *-o-* in *gastr-o-enter-o-logy*) is a connector with no meaning of its own.
4. **Give the origin.** Name the source language and the original form or a readable transliteration when reliably known. Mention the immediate source versus an earlier origin only when it aids understanding. Say so when a breakdown is a modern teaching convention rather than demonstrable history.
5. **Reconstruct the literal sense** in English and in natural Arabic, keeping each part's contribution but using grammatical word order in each language.
6. **Define it now:** a short modern English definition and an equivalent explanatory Arabic definition. Give the accepted Arabic term separately — a translation alone is not a definition. For medical terms, check `references/medical-affixes.md` so standard Arabic equivalents stay consistent (e.g. *-otomy* بَضْع, *-ectomy* استئصال, *-ostomy* فَغْر).
7. **Connect to context** in one sentence when context exists. Name the supplied context; otherwise label any example as illustrative rather than inventing what the user meant.
8. **Add at most one extra that earns its place:** a memory aid, a related word sharing the root, a commonly confused term, or a Greek/Latin doublet (*nephr-* vs *ren-*). Prefer correcting a real misconception over a decorative mnemonic. If an English term actually comes from Arabic (alcohol ← الكُحْل, nucha ← نُخاع), say so — it is memorable for Arabic speakers, as long as the derivation is genuine.

## Default response — one term

**[Term] — [accepted Arabic term]**

**Origin:** [language and derivation, brief].

| Part | Role / origin | English meaning | المعنى بالعربية |
| --- | --- | --- | --- |
| [component in original order] | [prefix/root/suffix; language] | [sense] | [Arabic equivalent] |

**Literally:** [English reconstruction] → [Arabic literal reconstruction].

**English definition:** [one clear sentence].

**التعريف بالعربية:** [one clear, natural Arabic sentence].

**In context:** [meaning in the supplied sentence or topic].

**Memory aid / Important distinction:** [optional, one brief point].

Adapt rather than filling empty sections. For an indivisible word, eponym or acronym, replace the table with the actual naming basis or expansion. If a literal reconstruction does not apply, say so in a few words instead of inventing one. Omit "In context" when there is nothing useful to say. Aim for roughly 150–250 words for one ordinary term; less for simple words, more only when the term or the user warrants it. No quizzes or clinical lectures unless asked.

### Worked example

**Thrombocytopenia — قِلَّة الصُّفَيْحات (الدموية)**

**Origin:** Modern medical coinage from Greek elements.

| Part | Role / origin | English meaning | المعنى بالعربية |
| --- | --- | --- | --- |
| thromb- | root; Greek *thrombos* | clot, lump | خُثْرة / جُلطة |
| -o- | connecting vowel | — | — |
| cyt- | root; Greek *kytos* "hollow vessel" | cell | خلية |
| -o- | connecting vowel | — | — |
| -penia | suffix; Greek *penia* "poverty" | deficiency | قِلَّة / نقص |

**Literally:** "a deficiency of clot cells" → «نقصٌ في خلايا التجلط».

**English definition:** An abnormally low number of platelets in the blood.

**التعريف بالعربية:** انخفاض عدد الصفيحات الدموية في الدم عن المعدل الطبيعي.

**Important distinction:** *-penia* (too few) is the opposite of *-cytosis* (too many, e.g. thrombocytosis). Both describe counts, not function.

More patterns — an eponym, an acronym, a literal-vs-real mismatch, a contested origin, and an Arabic word — are in `references/examples.md`. Read it when the term is not a straightforward analyzable word.

## Several terms at once

When the user gives a list, a slide or a screenshot with **four or more** terms, a full block per term buries the pattern. Use one compact table instead, then add short notes only where a term needs them (a mismatch, an eponym, a trap):

| Term | Breakdown | Literal meaning | Meaning | المصطلح العربي |
| --- | --- | --- | --- | --- |
| hepatomegaly | hepat- (liver) + -o- + -megaly (enlargement) | liver enlargement | enlarged liver | ضخامة الكبد |

When terms share a part, point it out once ("all three end in *-itis* = inflammation") rather than repeating it. With two or three terms, use the one-term format but drop repeated explanations. For a quick follow-up ("and *-ostomy*?"), answer briefly in the same style and build on what was already said.

## Arabic quality and layout

- Prefer standard Arabic medical terminology (the WHO-EMRO *Unified Medical Dictionary* / المعجم الطبي الموحد tradition) and clear Modern Standard Arabic. Add a familiar Egyptian Arabic gloss only when it helps or is requested — e.g. a term students actually hear in lectures. Never replace accurate Arabic with awkward word-for-word calques.
- An established Arabic term can override the literal pattern: *anemia* is فقر الدم, not «انعدام الدم». Give the established term and, if the literal meaning differs, say so.
- Use diacritics only where a word would otherwise be misread (بَضْع "incision" vs بِضْع "a few").
- Mixed right-to-left and left-to-right text scrambles easily. Keep Arabic in its own labelled line or in the last table column. When an English term must appear inside an Arabic sentence, put it in parentheses after the Arabic: التهاب الكبد (hepatitis). Use Arabic punctuation (، ؛) in Arabic text.

## Accuracy and verification

Etymology is a field full of confident folk stories, and a learner who is taught a false root will mis-derive other words too. So:

- Never derive an origin from spelling resemblance alone. Never invent classical roots, semantic histories, dates, original spellings or named people.
- Keep literal meaning, accepted Arabic term, modern definition and contextual sense distinct, and explain any important mismatch in one sentence. Etymology does not establish a modern definition, mechanism, diagnostic criterion or treatment — *-oma* means "mass", yet a hematoma is not a tumour.
- **Eponyms:** give the person and naming basis if known; do not split surnames into roots. **Acronyms:** expand the letters and translate the expansion. **Idioms and fixed phrases:** separate literal wording from actual usage. **Arabic words:** use the attested root (جذر) and pattern (وزن) — e.g. فُعال for many ailments (صُداع، سُعال، زُكام) — not a European prefix/suffix model.
- Verify uncertain, obscure, contested or specifically requested historical claims in an authoritative dictionary, historical lexicon or specialist terminology reference (e.g. OED, Etymonline, Merriam-Webster, Dorland's/Stedman's for medicine). Use a clinical authority for a clinical definition that needs checking. Search narrowly for the disputed point rather than researching broadly.
- Cite sources actually consulted, next to the claim they support. Never imply a lookup happened when it did not. If verification is unavailable, flag the uncertain point, give only what is supported, and leave the disputed derivation open — "origin disputed" is a correct answer.
- Label a mnemonic as a memory aid, never as history. Avoid misleading or offensive wordplay.
- Do not add pronunciation routinely. If asked, give reliable IPA and stress, noting regional variation only when supported.

## Final self-check

Before sending, confirm: every component is genuine; original order is kept; connecting vowels carry no meaning; English and Arabic definitions say the same thing; literal and conventional meanings are distinguished; Arabic terms are the standard ones and render cleanly beside English; uncertainty is visible where it exists; and the answer addresses the requested term without an unsolicited lecture.
