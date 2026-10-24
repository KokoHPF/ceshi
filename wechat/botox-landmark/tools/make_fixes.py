# 生成 fixes.json：把 OCR 拆开的多行标注合并成一个框
import json, sys
G = {  # 图: [(序号组, 英文键)]
 'x23.jpg': [([0, 1], 'superior angle'), ([3, 4], 'lateral acromion'), ([5, 6], 'deltoid tubercle'), ([7, 8, 9], 'root of scapular spine')],
 'x51.jpg': [([2, 4], 'root of scapular spine'), ([3, 5], 'mid-posterior glenoid rim')],
 'x86.jpg': [([0, 1], 'inferior angle'), ([6, 7], 'inferior angle'), ([2, 4], 'root of scapular spine'), ([3, 5], 'root of scapular spine')],
 'x158.jpg': [([1, 2, 4, 5, 7], 'predicted supraspinatus target'), ([9, 11, 12, 14, 15], 'predicted infraspinatus target'), ([10, 13], 'deltoid tubercle'), ([17, 18], 'root of scapular spine')],
 'x131.jpg': [([3, 6], 'distance (mm)')],
 'x148.jpg': [([5, 7], 'distance (mm)'), ([22, 24], 'distance (mm)'), ([37, 40], 'distance (mm)')],
}
F = {'x63.jpg': {'text': {'1': 'Med', '2': 'Lat', '8': 'Inf'}, 'extra': [[445, 1678, 497, 1704, 'Lat']]}}
for img, gs in G.items():
    rows = json.load(open(img + '.ocr.json')); f = F.setdefault(img, {})
    for idx, key in gs:
        bs = [rows[i] for i in idx]
        f.setdefault('skip', []).extend(idx)
        f.setdefault('extra', []).append([min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs), key])
json.dump(F, open('fixes.json', 'w'), ensure_ascii=False, indent=1)
