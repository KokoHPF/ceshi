"""图中英文标注 → 中文"""
WORD = {'middletrapezius': '中斜方肌'}


def norm(t):
    return t.replace(' ', '').replace('.', '').lower()


def lookup(t):
    return WORD.get(norm(t))
