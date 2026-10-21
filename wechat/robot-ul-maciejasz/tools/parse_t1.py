#!/usr/bin/env python3
"""从原文 PDF 第 2～10 页按列坐标解析表 1，输出 src/t1_raw.json。用法：python3 parse_t1.py <原文 PDF> <输出 json>"""
import sys, json
from collections import Counter
import pymupdf

doc = pymupdf.open(sys.argv[1])
HDR = ('System', 'name,ref', 'DOF', 'Supported', 'movements', 'Main', 'control inputs', 'Actuators', 'Type; field', 'application',
       'Stage of', 'additional info')
rows, sect = [], None
for n in range(1, 10):
    lines = []
    for b in doc[n].get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = ''.join(s['text'] for s in l['spans']).strip()
            if t: lines.append((l['bbox'], t, l['spans'][0]['font'], l['spans'][0]['size']))
    end = min([x[0][1] for x in lines if x[3] < 7.5 and x[0][1] > 100] + [770])
    body = [x for x in lines if 98 < x[0][1] < end and not (x[0][1] < 120 and x[1].startswith(HDR)) and not x[1].startswith('Table 1')]
    c = Counter(round(x[0][0]) for x in body)
    cs = []
    for k in sorted(k for k, v in c.items() if v >= 3):
        if not cs or k - cs[-1] > 6: cs.append(k)
    assert len(cs) == 7, (n + 1, cs)
    col = lambda x0: max(i for i, x in enumerate(cs) if x0 >= x - 4)
    starts = sorted({round(x[0][1]) for x in body if col(x[0][0]) == 1})
    secs = [(x[0][1], x[1]) for x in body if 'SemiBold' in x[2] and x[1].startswith('Systems')]
    page_rows = {y: {'c': [''] * 7, 'page': n + 1} for y in starts}
    for bb, t, fnt, _ in sorted(body, key=lambda x: (round(x[0][1]), x[0][0])):
        if 'SemiBold' in fnt and t.startswith('Systems'): continue
        ys = [y for y in starts if y <= bb[1] + 1]
        if not ys:  # 跨页续行，接到上一页最后一行
            r = rows[-1]
        else:
            r = page_rows[ys[-1]]
        i = col(bb[0]); r['c'][i] = (r['c'][i] + ('' if r['c'][i].endswith('-') else ' ') + t).strip()
    for y in starts:
        s = [t for sy, t in secs if sy < y]
        if s: sect = s[-1]
        page_rows[y]['sect'] = sect; rows.append(page_rows[y])
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
print(len(rows))
