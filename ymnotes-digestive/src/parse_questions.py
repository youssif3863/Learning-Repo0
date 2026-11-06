import re, json, sys
src = sys.argv[1]; out = sys.argv[2]
lines = [l.rstrip() for l in open(src, encoding='utf-8')]
skip = {"DIGESTIVE / MID-MODULE", "youtube.com/@ymnotes"}
SRC = re.compile(r'^(Digestive System|Hernia book|General oncology|Diaphragm anatomy)\b.*')
OPT = re.compile(r'^([A-E])\. (.*)$')
GRP = re.compile(r'^Group ([A-Z]{1,2})$')
LABELS = {"Microbiology", "Parasitology", "Extra"}
qs = []; cur = None; group = None; label = None; state = None
for l in lines:
    s = l.strip()
    if not s or s in skip or re.fullmatch(r'\d{1,3}', s): continue
    m = GRP.match(s)
    if m: group = m.group(1); cur = None; state = 'new'; continue
    if s in LABELS: label = s; cur = None; state = 'new'; continue
    if SRC.match(s):
        cur['src'].append(s); state = 'src'; continue
    m = OPT.match(s)
    if m and cur is not None and state in ('opt','q') and m.group(1) == "ABCDE"[len(cur['opts'])]:
        cur['opts'].append(m.group(2)); state = 'opt'; continue
    if state in ('new','src') or cur is None:
        cur = dict(group=group, label=label, q=s, opts=[], src=[]); qs.append(cur); state = 'q'; continue
    if state == 'q': cur['q'] += ' ' + s
    elif state == 'opt': cur['opts'][-1] += ' ' + s
for i, q in enumerate(qs, 1): q['id'] = i
json.dump(qs, open(out, 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(qs), 'questions'); print(Counter(len(q['opts']) for q in qs)); print(Counter(q['label'] for q in qs))
bad = [q['id'] for q in qs if len(q['opts']) < 4 or not q['src']]; print('suspicious', bad)
