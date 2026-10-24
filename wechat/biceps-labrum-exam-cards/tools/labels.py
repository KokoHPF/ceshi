"""图中英文标注 → 中文"""
ABBR = {'A': None, 'B': None}
WORD = {'examiner': '检查者', 'patient': '患者', 'uniformresistance': '均匀阻力', 'uniformdownwardforce': '均匀向下的力',
        'uniformdownward': '均匀向下的力', 'resistpronation': '抗旋前', 'resistsupination': '抗旋后'}


def norm(t):
    return t.replace(' ', '').replace('.', '').replace(',', '').lower()


def lookup(t):
    return WORD.get(norm(t))
