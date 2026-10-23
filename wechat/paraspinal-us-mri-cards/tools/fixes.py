"""逐图人工修正（键为图片 xref）"""
EXTRA = {}   # x: [[x0, y0, x1, y1, '英文'], ...]
SKIP = {}    # x: {OCR 序号, ...}
TEXT = {}    # x: {OCR 序号: '正确文字'}
SIZE = {}    # x: 字号倍数
ALIGN = {}   # x: {'英文': 'l'/'r'}
