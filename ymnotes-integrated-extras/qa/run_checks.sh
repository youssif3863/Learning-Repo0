#!/usr/bin/env bash
# Run every saved-file check on the finished PDF. Usage: bash qa/run_checks.sh
# Needs the YMnotes medical-book redesign skill (set YMNOTES_SKILL to its folder if it is not in the default place).
set -u
cd "$(dirname "$0")/.."
SKILL="${YMNOTES_SKILL:-/root/.claude/skills/synced/9e64779b-7e56-405a-bea8-e1a695a63aec_b53328e2-3aba-468f-bac9-89c120548dbd/ymnotes-medical-book-redesign}"
PDF=YMnotes-Digestive-System-Integrated-Teaching-Extras.pdf
echo "== 1. integration checks (qa/verify.py)"
python3 qa/verify.py; V=$?
echo "== 2. skill layout guard"
python3 "$SKILL/scripts/layout_guard.py" "$PDF" --out qa/layout-guard.json >/dev/null; L=$?
python3 -c "import json;print('layout guard:', json.load(open('qa/layout-guard.json'))['verdict'])"
echo "== 3. skill contents contract (declare -> snapshot before outline -> verify final)"
python3 - <<'PY'
import json
m = json.load(open("build/out/build-map.json"))
json.dump({str(n): m["destinations"][f"ch{n:02d}"]["folio"] for n in range(1, 41)}, open("build/out/toc-folios.json", "w"))
open("build/out/openers.txt", "w").write(",".join(f'{n}={m["destinations"][f"ch{n:02d}"]["physical_page"]}' for n in range(1, 41)))
PY
python3 "$SKILL/scripts/contents_contract.py" declare --structure source/chapters.json --subjects source/chapter-subjects.json \
        --toc-pages build/out/toc-folios.json --out qa/contents-entries.json
python3 "$SKILL/scripts/contents_contract.py" snapshot build/out/with-closing.pdf --out qa/nav-baseline.json
python3 "$SKILL/scripts/contents_contract.py" verify "$PDF" --declared qa/contents-entries.json --baseline qa/nav-baseline.json \
        --openers "$(cat build/out/openers.txt)" --out qa/contents-entry-map.json | tail -12
echo "(Known limitation: that gate identifies a chapter by its opening PAGE. Where several chapters open on one page"
echo " - the compact 'no additions' entries, or Part 1's header on Chapter 1's page - it counts their rows as duplicates."
echo " qa/verify.py checks the same entries by exact heading position instead.)"
exit $(( V || L ))
