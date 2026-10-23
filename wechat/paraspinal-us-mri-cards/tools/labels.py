"""原文图中英文标注 → 中文。ABBR 区分大小写（Rm/RM、RCPM/RCPm 含义不同），WORD 用小写、去空格和句点匹配。"""
ABBR = {
    'Trap': '斜方肌', 'LD': '背阔肌', 'Rm': '小菱形肌', 'RM': '大菱形肌', 'SP': '棘突', 'SS': '冈上肌', 'Scap': '肩胛骨',
    'LS': '肩胛提肌', 'LS1': '肩胛提肌1', 'LS2': '肩胛提肌2', 'LS3': '肩胛提肌3', 'LS4': '肩胛提肌4',
    'SPS': '上后锯肌', 'SPI': '下后锯肌', 'SA': '前锯肌', 'Inc': '肋间肌', 'Ilio': '髂肋肌', 'Hlio': '髂肋肌', 'ES': '竖脊肌',
    'DSA': '肩胛背动脉', 'DSN': '肩胛背神经', 'SAN': '副神经', 'SCM': '胸锁乳突肌',
    'SPCa': '头夹肌', 'SPCe': '颈夹肌', 'LCa': '头最长肌', 'Lca': '头最长肌', 'LC': '头最长肌', 'LCe': '颈最长肌', 'ICCe': '颈髂肋肌',
    'SSCa': '头半棘肌', 'SsCa': '头半棘肌', 'SSCe': '颈半棘肌', 'SSCaM': '头半棘肌内侧束', 'SSCaL': '头半棘肌外侧束', 'SSCal': '头半棘肌外侧束',
    'AP': '关节柱', 'CTJ': '肋横突关节', '1stCTJ': '第1肋横突关节', 'Mas': '乳突', 'DIG': '二腹肌',
    'OCS': '头上斜肌', 'OCI': '头下斜肌', 'OA': '枕动脉', 'GON': '枕大神经', 'TrSp': '横突棘肌', 'DCA': '颈深动脉',
    'RCPM': '头后大直肌', 'RCPm': '头后小直肌', 'SST': '胸半棘肌', 'ICT': '胸髂肋肌', 'LT': '胸最长肌', 'ICL': '腰髂肋肌',
    'RO': '回旋肌', 'F': '小关节', 'TP': '横突', 'QL': '腰方肌', 'PM': '腰大肌', 'IC': '髂嵴', 'M': '多裂肌',
    'VA': '椎动脉', 'C2DRG': 'C2背根神经节', 'C2SP': 'C2棘突', 'C1SP': 'C1棘突', 'SC': '脊髓',
    'C1TP': 'C1横突', 'C4TP': 'C4横突', 'C5TP': 'C5横突', 'L4TP': 'L4横突', 'C5R': 'C5神经根', 'L3/4F': 'L3/4小关节',
    'EO': '腹外斜肌', 'IO': '腹内斜肌', 'TVA': '腹横肌', 'LR': '外侧缝',
}
WORD = {
    'medial': '内侧', 'lateral': '外侧', 'cranial': '头侧', 'caudal': '尾侧', 'anterior': '前侧', 'posterior': '后侧',
    'caudal-medial': '尾内侧', 'cranial-lateral': '头外侧', 'anterior-lateral': '前外侧', 'posterior-medial': '后内侧',
    'caudal-posterior': '尾后侧', 'cranial-anterior': '头前侧', 'occiput': '枕骨', 'pleura': '胸膜', 'bowel': '肠管',
    'facet': '小关节', 'lamina': '椎板', 'rib': '肋骨', '1strib': '第1肋', '2ndrib': '第2肋', '3rdrib': '第3肋',
    '10thrib': '第10肋', '11thrib': '第11肋', '12thrib': '第12肋', 'multifidus': '多裂肌',
    'trapezius': '斜方肌', 'latissimusdorsi': '背阔肌', 'iliocostalisthoracis': '胸髂肋肌', 'longissimusthoracis': '胸最长肌',
    'spinalisthoracis': '胸棘肌', 'multifidusthoracis': '胸多裂肌', 'semipinalisthoracis': '胸半棘肌', 'semispinalisthoracis': '胸半棘肌',
    'rhomboidminor': '小菱形肌', 'rhomboidmajor': '大菱形肌', 'levatorscapulae': '肩胛提肌', 'serratusanterior': '前锯肌',
    'serratusposteriorsuperior': '上后锯肌', 'serratusposteriorinferior': '下后锯肌', 'sternocleidomastoid': '胸锁乳突肌',
    'stemocleidomastoid': '胸锁乳突肌', 'stermocleidomastoid': '胸锁乳突肌',
    'spleniuscapitis': '头夹肌', 'spleniuscervicis': '颈夹肌', 'longissimuscapitis': '头最长肌', 'tongissimuscapitis': '头最长肌',
    'longissimuscervicis': '颈最长肌', 'iliocostaliscervicis': '颈髂肋肌', 'semispinaliscapitis': '头半棘肌', 'semispinaliscervicis': '颈半棘肌',
    'obliquecapitisinferior': '头下斜肌', 'obliquecapitissuperior': '头上斜肌', 'rectuscapitisposteriormajor': '头后大直肌',
    'rectuscapitisposteriorminor': '头后小直肌', 'scalenusanterior': '前斜角肌', 'scalenusmedius': '中斜角肌', 'scalenusposterior': '后斜角肌',
    'interspinales': '棘间肌', 'multifidus&rotatores': '多裂肌和回旋肌', 'rotatorthoracis': '胸回旋肌', 'rotatoresthoracis': '胸回旋肌',
    'iliocostalislumborum': '腰髂肋肌', 'quadratuslumborum': '腰方肌', 'psoas': '腰大肌', 'psoasmajor': '腰大肌',
    'longissimusthoracislumbarpart': '胸最长肌（腰部）', 'longissimusthoracismlumbarpart': '胸最长肌（腰部）', 'multifidusrotatores': '多裂肌和回旋肌',
    'lliocostalislumborum': '腰髂肋肌', 'medial-posterior': '内后侧', 'lateral-anterior': '外前侧', 'vb': '椎体',
    'serratusposteriorinferior': '下后锯肌', 'obliquecapitissuperiorm': '头上斜肌',
}


def norm(t):
    return t.replace(' ', '').replace('.', '').replace(',', '').replace('，', '').replace('(', '').replace(')', '').lstrip('-')


def lookup(t):
    k = norm(t)
    if k in ABBR: return ABBR[k]
    lk = k.lower()
    for cand in (lk, lk[:-1] if lk.endswith('m') else None):
        if cand and cand in WORD: return WORD[cand]
    return None
