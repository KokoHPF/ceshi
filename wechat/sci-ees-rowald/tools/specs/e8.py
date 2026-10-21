SPEC = [
 ('Step 1 Immediate Effects', '步骤 1　即时效果'), ('Participant P1', '受试者 P1'), ('Participant P2', '受试者 P2'), ('Participant P3', '受试者 P3'),
 ('EESOFF', '刺激关'), ('EESON', '刺激开'), ('Iliopsoas', '髂腰肌'), ('lliopsoas', '髂腰肌'), ('Vastus Lateralis', '股外侧肌'),
 ('Semitendinosus', '半腱肌'), ('Tibialis Anterior', '胫前肌'), ('Step Height', '抬腿高度'), ('StepHeight', '抬腿高度'),
 
 
 ('Hip Range of Motion Knee Range of Motion', '髋关节活动度　　　　膝关节活动度'), ('Hip Range of Motion', '髋关节活动度'),
 ('Knee Rangeof Motion', '膝关节活动度'), ('KneeRangeof Motion', '膝关节活动度'), ('Ankle Range of Motion', '踝关节活动度'),
 ('AnkleRangeof Motion', '踝关节活动度'), ('AnkleRange of Motion', '踝关节活动度'),
 
 ('STANCE', '支撑期'), ('SWING', '摆动期'), ('Soleus', '比目鱼肌'), ('n/a', '无'),
 ('Step2Robustness', '步骤 2　稳定性'), ('Step 3 Voluntary modulation of stride length', '步骤 3　主动调节步长'),
 (['Numberof independent steps', 'duringthe very first session'], '首次训练中\n独立迈步的步数'), ('Step length [cm]', '步长（cm）'),
 ('Big step', '大步'), ('Normal step', '正常步'),
]
_lab = ['髋', '膝', '踝', '髂腰', '股外', '半腱', '胫前', '比目']
_ys = {(60, 85, 100, 332): [102, 133, 164, 189, 220, 248, 276, 304], (60, 355, 102, 600): [372, 403, 434, 462, 490, 521, 549, 577],
       (60, 630, 102, 875): [651, 682, 713, 747, 775, 800, 825, 853]}
EXTRA = []
for blk, ys in _ys.items():
    EXTRA.append((blk, '', {}))
    EXTRA += [((70, y - 15, 86, y + 15), t, {'rot': True, 'fs': 17, 'fg': (40, 40, 40)}) for y, t in zip(ys, _lab)]
for rows in ([(88, 150), (165, 228), (240, 312)], [(368, 428), (448, 510), (528, 592)], [(638, 702), (720, 786), (803, 872)]):
    for xc in (652, 746, 845):
        for j, (y0, y1) in enumerate(rows):
            t = '角度（°）' if j == 2 else ('距离（cm）' if xc == 845 and j == 1 else '幅值（mV）')
            EXTRA.append(((xc - 7, y0, xc + 6, y1), t, {'rot': True, 'fs': 16, 'bg': (255, 255, 255), 'fg': (40, 40, 40)}))
EXTRA += [((183, 343, 228, 366), '刺激关', {}), ((674, 321, 726, 343), '关　　开', {'fs': 16, 'bg': (255, 255, 255)}), ((674, 594, 726, 615), '关　　开', {'fs': 16, 'bg': (255, 255, 255)}),
          ((674, 870, 726, 891), '关　　开', {'fs': 16, 'bg': (255, 255, 255)})]
