_ab = [('RF', '股直'), ('VLat', '股外'), ('ST', '半腱'), ('TA', '胫前'), ('MG', '腓肠'), ('Sol', '比目'),
       ('RII', '右髂腰'), ('RRF1', '右股直'), ('RRF', '右股直'), ('RVLat.', '右股外'), ('RVLati', '右股外'), ('RST:', '右半腱'), ('RTAI', '右胫前'),
       ('RTA|', '右胫前'), ('RMGI', '右腓肠'), ('RMG1', '右腓肠'), ('RSoll', '右比目'), ('LRF', '左股直'), ('LVLat', '左股外'), ('LST I', '左半腱'),
       ('LTAI', '左胫前'), ('LMGI', '左腓肠'), ('LSolI', '左比目')]
SPEC = [
 ('Step 1 Configuration of electrodes to target functional hotspots', '步骤 1　配置针对功能热点的电极'),
 ('Step 2 Library of electrode configurations targeting functional hotspots', '步骤 2　针对功能热点的电极配置库'),
 ('Participant P1', '受试者 P1'), ('Participant P3', '受试者 P3'),
 (['Target', 'Weight', 'Acceptance'], '目标：\n承重'), (['Target@113,595', 'Whole Leg@111,609', 'Flexion@112,624'], '目标：\n全腿屈曲'),
 (['Weight@460,413', 'Acceptance@462,429'], '承重'), (['Whole Leg@525,413', 'Flexion@526,428'], '全腿屈曲'),
 (['Weight@461,887', 'Acceptance@462,903'], '承重'), (['Whole Leg@525,887', 'Flexion@527,902'], '全腿屈曲'),
 (['Hip@232,414', 'Angle@232,429'], '髋角度'), (['Knee@285,413', 'Angle@285,429'], '膝角度'), (['Ankle@335,414', 'Angle@335,429'], '踝角度'),
 (['Hip@232,887', 'Angle@232,903'], '髋角度'), (['Knee@285,887', 'Angle@285,902'], '膝角度'), (['Ankle@338,887', 'Angle@338,902'], '踝角度'),
 ('Normalized Activity', '归一化活动'), ('Right', '右'), ('Left', '左'), ('155 a.u', '155 任意单位'), ('95 a.u', '95 任意单位'),
 ('selectivity [a.u]', '选择性（任意单位）'), (['selectivity', '[a.u]'], '选择性（任意单位）', {'rot': True}),
 (['1.4 x', 'Motorthreshold'], '1.4 倍\n运动阈值'), (['1.7 ×', 'Motorthreshold'], '1.7 倍\n运动阈值'),
 ('Whole Leg Flexion', '全腿屈曲'), ('Hip Flexion', '屈髋'), ('Weight Acceptance', '承重'), ('Propulsion', '推进'),
] + [(a, b, {'al': 'r'}) for a, b in _ab]
EXTRA = [((162, 922, 181, 972), '角度（°）', {'rot': True, 'fs': 18}), ((162, 799, 206, 817), '右比目', {'al': 'r'}), ((108, 1174, 152, 1192), '左髂腰', {'al': 'r'})]
