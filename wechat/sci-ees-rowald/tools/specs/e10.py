from common import STEPS
SPEC = STEPS + [
 (['LD - Latissimus dorsi', 'Dp-Deltoideus posterior', 'SA- Serratus anterior', 'ES-LowerErectorSpinae', 'QL-Quadratus Lumborum'],
  '背阔 - 背阔肌\n三角后 - 三角肌后束\n前锯 - 前锯肌\n竖脊 - 下段竖脊肌\n腰方 - 腰方肌', {'al': 'l', 'fs': 19}),
 (['T-Trapezius@702,588', 'Pm-Pectoralis major@721,599', 'SA-Serratus anterior@722,611', 'RA-Rectus abdominis@725,623', 'Obl - Obliques@706,634',
   'QL - Quadratus Lumborum@732,646', 'IL -Iliopsoas', 'S-Sartorius', 'RF- Rectus femoris', 'Vlat-Vastus lateralis', 'Vmed-Vastus medialis', 'GL - Gluteus'],
  '斜方 - 斜方肌\n胸大 - 胸大肌\n前锯 - 前锯肌\n腹直 - 腹直肌\n腹斜 - 腹斜肌\n腰方 - 腰方肌\n髂腰 - 髂腰肌\n缝匠 - 缝匠肌\n股直 - 股直肌\n股外 - 股外侧肌\n股内 - 股内侧肌\n臀 - 臀肌', {'al': 'l', 'fs': 19}),
 (['D -Deltoideus', 'T-Trapezius', 'SA-Serratus anterior', 'Pm-Pectoralis major', 'RA-Rectus abdominis', 'Obl - Obliques', 'QL - Quadratus Lumborum'],
  '三角 - 三角肌\n斜方 - 斜方肌\n前锯 - 前锯肌\n胸大 - 胸大肌\n腹直 - 腹直肌\n腹斜 - 腹斜肌\n腰方 - 腰方肌', {'al': 'l', 'fs': 19}),
 ('Frontpull movement', '前拉动作'), ('Four point kneeling movement', '四点跪位动作'), ('Frontshoulderraise movement', '肩前举动作'),
 ('EESOFF', '刺激关'), ('EESON', '刺激开'), ('Lumbar curvature (a.u)', '腰椎曲度（任意单位）'), ('Radius', '半径'), ('Average', '平均'),
 ('Execution time (s)', '完成时间（秒）'),
 (['Engaged/Targeted@716,262', 'muscles@692,274'], '参与 / 目标肌肉', {'al': 'l'}), (['Engaged/Targeted@716,565', 'muscles@692,577'], '参与 / 目标肌肉', {'al': 'l'}),
 (['Engaged/Targeted@682,939', 'muscles@658,952'], '参与 / 目标肌肉', {'al': 'l'}),
 ('Healthy', '健康人'), (['Stimulation reduces', 'lumbar lordosis', 'through activation of', 'abdominal muscles'], '刺激通过激活\n腹肌减少\n腰椎前凸', {'al': 'l'}),
 ('Active lordosis correction (a.u.)', '主动纠正前凸（任意单位）'), ('healthy subjects (n=5)', '健康人（5 人）'),
 ('Normalized Height', '归一化高度'), ('Weight (kg)', '重量（kg）'),
] + [(a, b, {'al': 'r'}) for a, b in [('Dp', '三角后'), ('SA', '前锯'), ('QL', '腰方'), ('Obl', '腹斜'), ('RF', '股直'), ('Viat', '股外'), ('Vmed', '股内'),
     ('Pm', '胸大'), ('iqo', '腹斜'), ('RA', '腹直')]]
_f = 0.655
def _b(x, y, w=10, h=7): return (x * _f - w, y * _f - h, x * _f + w, y * _f + h)
EXTRA = [((121, 92, 206, 141), '完成时间', {'fs': 26, 'rot': False}), (_b(998, 207, 9, 6), '竖脊', {'fs': 15, 'al': 'r'}),
         (_b(560, 690, 16, 12), '半径', {'fs': 22, 'rot': False}), (_b(560, 915, 16, 12), '半径', {'fs': 22, 'rot': False})]
EXTRA += [(_b(x, y, 9, 4.5), t, {'fs': 13, 'al': 'r'}) for x, y, t in [(993, 673, '斜方'), (998, 700, '胸大'), (998, 765, '腰方'), (998, 778, '腹直'),
          (995, 797, '髂腰'), (995, 808, '臀'), (993, 824, '缝匠'), (940, 1207, '斜方'), (940, 1222, '三角'), (940, 1303, '腰方')]]
