SPEC = [
 (['Spinal cord', 'injury'], '脊髓\n损伤', {'al': 'l'}), ('Personalizedcomputationalmodel', '个体化计算模型'), ('Selectivity', '选择性'),
 ('lliopsoas', '髂腰肌', {'al': 'r'}), (['Vastus', 'lateralis'], '股外侧肌', {'al': 'r'}), (['Tibialis', 'anterior'], '胫前肌', {'al': 'r'}),
 (['Gastrocnemius', 'medialis&Soleus'], '腓肠肌内侧头\n和比目鱼肌', {'al': 'r'}),
 ('Selectivitypredicted in silico', '计算机模拟预测的选择性'), ('Selectivity quantified intraoperatively', '术中实测的选择性'),
 ('Combined selectivity', '综合选择性'), (['Multipolarstimulation', 'torecruitsacraldorsal roots'], '多极刺激\n募集骶段背根'),
 ('Right Left', '右　　　左'), ('Left', '左'), ('Right', '右'), ('Hip flexion', '屈髋'), ('Ankleextension', '踝伸展（跖屈）'),
 ('Normalized activity [a.u.]', '归一化肌肉活动（任意单位）'), ('Targeted', '目标肌', {'al': 'l'}), ('Non targeted', '非目标肌', {'al': 'l'}),
 (['New', 'Paddle', 'Lead'], '新型\n桨状\n电极'), (['Specify', '5-6-5'], '传统\n5-6-5\n电极'),
 ('Normalizedselectivityindex', '归一化选择性指数'),
]
_m = ['髂腰肌', '股直肌', '股外侧肌', '半腱肌', '胫前肌', '腓肠肌', '比目鱼肌']
_xl = [693, 713, 733, 753, 775, 795, 817]; _xr = [852, 872, 892, 912, 933, 953, 975]
EXTRA = [((360, 785, 735, 815), '　　综合选择性最高的位置', {'al': 'l', 'fg': (30, 30, 30)}),
         ((360, 1190, 735, 1219), '　　综合选择性最高的位置', {'al': 'l', 'fg': (30, 30, 30)}),
         ((683, 1988, 992, 2058), '', {})]
EXTRA += [((x - 9, 1992, x + 9, 2056), '左' + m, {'rot': True, 'fs': 22, 'fg': (40, 40, 40)}) for x, m in zip(_xl, _m)]
EXTRA += [((x - 9, 1992, x + 9, 2056), '右' + m, {'rot': True, 'fs': 22, 'fg': (40, 40, 40)}) for x, m in zip(_xr, _m[::-1])]
