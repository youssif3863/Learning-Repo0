# Browser loop and recovery

State sequence: discover → inspect consequences → capture → persist → navigate → observe → reconcile.

- Capture one question's rendered details in one pass. A loading placeholder is not a blank question. Use supported readiness waits; if unavailable, a bounded wait followed by a fresh observation. One failed observation does not justify a refresh.
- Before every click inspect the fresh control: a Next button may turn into Finish on the last question. Identical labels can have different effects. Stop at the final question without submitting.
- Prefer Next for source order; use numbered navigation when Next fails normally. Do not select random answers to enable navigation. For review pages containing multiple questions, preserve their visible ordering and dependent passages.
- Save each occurrence keyed by exam and original position or visible identifier. A replay of the same key and content is idempotent; changed content at that key is a conflict to inspect, not silently overwrite. Identical content at different source positions remains separate.
- On interruption, recover records from the journal; compare current exam/position with the last saved question. If it already exists, verify its identity once and continue. Do not assume the page remained unchanged across turns.
- If a question fails to render after a bounded wait and one normal alternative navigation, mark its position as missing, save a checkpoint, and continue other permitted content. Never count a missing placeholder as captured.
- On access denial, rate limit, CAPTCHA or explicit collection restriction, stop site actions and save. Do not repeatedly refresh, use cached URLs to evade the gate, or change identities. User-restored access must be confirmed by the live tool before resuming.
- A locked list can coexist with an already open accessible exam. Do not infer why. Finish only permitted work; after the user restores access resume the next incomplete exam, preserving completed files.

Keep the audit's latest checkpoint explicit: exam, last confirmed source position, saved count, next intended position, missing positions and blocker. Historical checkpoints must not contradict current status. A wait interval is a claim about actions you initiate, not the site's background requests.
