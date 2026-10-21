_sel = [('Left', v) for v in ('0.250', '0.116', '0.000')] + [('Right', v) for v in ('0.156', '0.074', '0.038')]
_w = [(w, '左') for w in ('Left', 'Left-', 'Left -', '-Left', 'Left ', 'Left .', 'eft', 'HLeft')] + \
     [(w, '右') for w in ('Right', 'Right-', '-Right-')] + [('Trunk', '躯干'), ('runk', '躯干'), ('Leg', '腿'), ('Knees', '膝'),
     ('QL', '腰方'), ('Obl', '腹斜'), ('UA', '上腹'), ('Add', '内收'), ('RF', '股直')] + \
     [(w, '外展 — 内收') for w in ('-Abduction-Adduction', 'Abduction-Adduction', '-Abduction—Adduction-', '-Abduction--Adduction', '-Abduction—Adduction', 'Abduction-—Adduction')]
SPEC = [
 ('Step 1 Targeting motor neurons innervating trunk muscles', '步骤 1　靶向支配躯干肌的运动神经元'),
 ('Step 2 From stimulation pulses to selective activation of trunk muscles', '步骤 2　从刺激脉冲到躯干肌的选择性激活'),
 (['A set of trunk and upperleg muscles is selected tostabilize and', 'controltrunkposture'], '选定一组躯干和大腿上部肌肉，\n用于稳定和控制躯干姿势'),
 (['Muscle responses to single pulses of EEs at increasing amplitude are analysed to define', 'the electrodes yielding the highest selective recruitment of targeted trunk muscles'],
  '分析递增强度单脉冲刺激下的肌肉反应，\n找出对目标躯干肌选择性募集最高的电极'),
 ('SPINAL ARRAY', '脊髓电极阵列'), (['Normalized', 'response@935,146', 'amplitude@936,155'], '归一化\n反应幅值', {'al': 'l'}),
 ('Concatenated responses', '拼接的反应'), ('yun', '躯干'), ('xew', '最大'), ('min', '最小'), ('max', '最大'), ('EES', '刺激'),
 ('Muscle 1', '肌肉 1'), ('Muscle 2', '肌肉 2'), (['Stimulation', 'amplitude@935,240'], '刺激\n强度', {'al': 'l'}),
 (['Selectstimulationamplitude', 'leading to highest selectivity'], '选择选择性\n最高的刺激强度'),
 (['relativemuscular', 'activation at best', 'amplitude@803,362'], '最佳强度下的\n相对肌肉激活'), ('LEGS', '腿部'), ('TRUNK', '躯干'),
 (['mostselective', 'amplitude@940,374'], '选择性\n最高强度', {'al': 'l'}), ('Iliopsoas (IL)', '髂腰肌（髂腰）', {'al': 'l'}),
 (['Calculate selectivity index', 'by weighing trunk and', 'leg recruitment'], '权衡躯干和腿部募集，\n计算选择性指数'),
 (['stimulation', 'artefact'], '刺激伪迹', {'rot': True}), ('Upper Abdominals (UA)', '上腹肌（上腹）', {'al': 'l'}),
 ('Adductors (Add)', '内收肌（内收）', {'al': 'l'}), ('Obliques (Obl)', '腹斜肌（腹斜）', {'al': 'l'}),
 (['Nomalized', 'response', 'amplitudes'], '归一化\n反应幅值', {'al': 'l'}), ('Rectus Femoris (RF)', '股直肌（股直）', {'al': 'l'}),
 ('Quadratus Lomborum(QL)', '腰方肌（腰方）', {'al': 'l'}), ('Step 3 Targeted activation of trunk muscles', '步骤 3　躯干肌的靶向激活'),
 ('Step 4 Kinematic response to targeted stimulation of trunk motor neurons', '步骤 4　靶向刺激躯干运动神经元的运动学反应'),
 (['Singlepulses of targetedEES appliedtotheT12rootselectively recruit', 'trunkmuscleswithminimal recruitmentofthelegmuscles'],
  '对 T12 根施加靶向单脉冲刺激，选择性募集躯干肌，\n腿部肌肉募集极少'),
 (['Targeted high-frequency stimulation of the T12 root leads to side-specific trunk excursion', 'withoutvisiblelegmovement'],
  '对 T12 根靶向高频刺激，引起特定一侧的躯干偏移，\n且无明显腿部运动'),
 ('500ms', '500 毫秒'), (['Kinematic response', 'during stimulation trains', 'of500msat120Hz'], '500 毫秒、120 Hz 刺激串\n期间的运动学反应'),
] + [(f'{s} trunk selectivity = {v}', f'{"左" if s == "Left" else "右"}侧躯干选择性 = {v}') for s, v in _sel] + _w
EXTRA = []
_tpl = [(-70, -73, '腹斜'), (-22, -95, '上腹'), (32, -95, '上腹'), (75, -73, '腹斜'), (-97, -27, '腰方'), (100, -32, '腰方'),
        (-95, 30, '髂腰'), (95, 23, '髂腰'), (-68, 75, '内收'), (80, 73, '内收'), (-25, 97, '股直'), (22, 97, '股直')]
_f = 0.56
def _lab(cx, cy, s=1.0, fs=16):
    out = []
    for dx, dy, t in _tpl:
        x, y = (cx + dx * s) * _f, (cy + dy * s) * _f
        out.append(((x - 8 * min(s, 1.3), y - 6 * min(s, 1.3), x + 8 * min(s, 1.3), y + 6 * min(s, 1.3)), t, {'fs': fs, 'rot': False}))
    return out
for c in [(190, 1035), (512, 1035), (190, 1400), (512, 1400), (190, 1760), (512, 1760)]:
    EXTRA += _lab(*c)
EXTRA += _lab(1376, 345, 1.6, 20) + _lab(1553, 688, 0.6, 14)
EXTRA += [((130, 212, 145, 225), '髂腰', {'fs': 18}), ((130, 239, 145, 252), '股直', {'fs': 18}), ((368, 347, 382, 359), '髂腰', {'al': 'r', 'fs': 18}),
          ((946, 975, 960, 1010), '膝', {'rot': False})]
EXTRA += [((722, 102, 742, 123), '上腹', {'fs': 20, 'rot': False}), ((720, 258, 742, 280), '股直', {'fs': 20, 'rot': False}), ((800, 260, 822, 282), '股直', {'fs': 20, 'rot': False})]
