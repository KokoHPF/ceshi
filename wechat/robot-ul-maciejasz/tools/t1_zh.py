#!/usr/bin/env python3
"""表 1 中文翻译：按术语词典逐条替换，个别整句单独给出。用法：python3 t1_zh.py <t1_raw.json> <输出 json>"""
import sys, json, re

SECT = {'finger': '手指', 'shoulder': '肩', 'elbow': '肘', 'forearm': '前臂', 'wrist': '腕', 'finger(s)': '手指', 'fingers': '手指'}
WHOLE = {
 'Ögce [171]': None,
 'CI study: 2 traumatic brachial plexus injury': 'Ⅰ类研究：2 例创伤性臂丛损伤',
 'Commercial system for other applications, used in some clinical studies e.g. [191,192]': '为其他用途设计的商用系统，部分临床研究中用过，如 [191,192]',
 'Research device; often used for hand therapy (e.g. [185-187])': '研究用设备；常用于手部治疗（如 [185-187]）',
 'See separate information for MIME and RiceWrist system': '见 MIME 和 RiceWrist 各自条目',
 'CI study: 18 children with weak handwriting skills': 'Ⅰ类研究：18 名书写能力弱的儿童',
 '3 configurations possible: 1) shoulder * elbow, 2) forearm – PS, wrist – FE, 3) forearm – PS, wrist – AA':
     '3 种构型：① 肩*肘；② 前臂旋前旋后、腕屈伸；③ 前臂旋前旋后、腕内收外展',
 'sEMG, button, eye-movement orBranComputer Interface; object labels – radio frequency identification':
     '表面肌电、按钮、眼动或脑机接口；物体标签用射频识别',
 'elastic elements or DC brakes (shoulder-elbow-wrist exoskeleton), FES (optional), DC motor (optional hand orthosis)':
     '弹性元件或直流制动器（肩-肘-腕外骨骼）、功能性电刺激（可选）、直流电机（可选手部矫形器）',
 '[Shoulder – FE, AA, elbow – FE], optional: forearm – PS, wrist – FE (shoulder-elbow-wrist exoskeleton), optional: all fingers together – GR (hand orthosis)':
     '[肩屈伸、内收外展，肘屈伸]，可选：前臂旋前旋后、腕屈伸（肩-肘-腕外骨骼），可选：全部手指一起抓放（手部矫形器）',
 'Shoulder * elbow; also {* wrist} or {fingers - FE} if special handle used': '肩*肘；用专用手柄时还可 {*腕} 或 {手指屈伸}',
 'Prototype (with spring instead of an actuator in the hand part); C0 study: 1 hs; based on Gentle/S':
     '原型机（手部用弹簧代替驱动器）；0 类研究：1 名健康人；基于 Gentle/S',
 'FDA clearance; CI study: 20(11) cS; a modified version of the system is used for ankle rehabilitation':
     '获 FDA 许可；Ⅰ类研究：20(11) 例慢性卒中；改良版用于踝关节康复',
}
# 按长度从长到短替换
D = [
 # 运动
 ('Independent linear movement of each finger (1 at a time)', '每根手指独立直线运动（一次一根）'),
 ('Independent linear movement of each finger', '每根手指独立直线运动'),
 ('Independent passive movement of each finger', '每根手指独立被动运动'),
 ('Concurrent FE of 3 joints of a single finger', '单根手指 3 个关节同时屈伸'),
 ('FE and AA of all major joints of each finger', '每根手指所有主要关节的屈伸和内收外展'),
 ('Resistive force to each finger', '对每根手指施加阻力'),
 ('longitudinal movements of the forearm', '前臂纵向运动'), ('bilateral longitu-dinal movements of the forearms', '双侧前臂纵向运动'),
 ('forearm’s eleva-tion and yaw', '前臂抬高和偏转'), ('in the plane + gravity compensation', '平面内 + 重力补偿'),
 ('in the horizonatal or vertical plane', '水平或垂直平面内'), ('in the adjustable plane', '可调平面内'), ('in the plane', '平面内'),
 ('Forearm and fingers twisting movements', '前臂和手指扭转动作'), ('coupled together', '联动'),
 ('wrist and MCP joints of 4 fingers', '腕和 4 指掌指关节'), ('Wrist and 4 fin-gers (except the thumb) extension', '腕和 4 指（拇指除外）伸展'),
 ('4 fingers (except the thumb) together', '4 指（拇指除外）一起'), ('Thumb, index and middle finger together', '拇、示、中指一起'),
 ('thumb, middle and index finger together', '拇、中、示指一起'), ('Thumb, index, middle, and ring finger', '拇、示、中、环指'),
 ('Index, middle, and ring finger', '示、中、环指'), ('All fingers together', '全部手指一起'), ('all fingers together', '全部手指一起'),
 ('other fingers together', '其余手指一起'), ('otherfingers', '其余手指'), ('Each finger separately', '每根手指分别'),
 ('Each finger', '每根手指'), ('Fingers (each)', '每根手指'), ('Fingers(each)', '每根手指'), ('Index finger', '示指'), ('index finger', '示指'),
 ('1 finger', '1 根手指'), ('passive extension', '被动伸展'), ('passive release', '被动松开'), ('grasp robot', '抓握机器人'),
 ('Shoulder', '肩'), ('shoulder', '肩'), ('Elbow', '肘'), ('elbow', '肘'), ('Forearm', '前臂'), ('forearm', '前臂'), ('fore-arm', '前臂'),
 ('Wrist', '腕'), ('wrist', '腕'), ('Thumb', '拇指'), ('thumb', '拇指'), ('fingers', '手指'),
 ('flexion', '屈曲'), ('Flexion', '屈曲'), ('extension', '伸展'), ('grasp', '抓握'), ('3 DOF, Haptic-Master', '3 自由度，HapticMaster'),
 ('3 DOF, HapticMaster', '3 自由度，HapticMaster'),
 # 控制输入
 ('sEMG signals from not affected arm', '健侧手臂表面肌电'), ('Joint angles of the master hand', '主手的关节角度'),
 ('Joint angles of healthy hand', '健侧手的关节角度'), ('Joint angles (a Motion Capture System is used)', '关节角度（用动作捕捉系统）'),
 ('Hand-held trigger,indexand thumb fingers joint angles', '手持触发器、示指和拇指关节角度'), ('Hand motion (tremor)', '手部运动（震颤）'),
 ('Hand accelera-tions (Nintendo Wii console)', '手部加速度（任天堂 Wii 手柄）'), ('abnor-mal trunk posi-tion detection', '检测躯干异常姿势'),
 ('Actuator translation and inclination', '驱动器位移和倾角'), ('Flexion/Extension torque', '屈伸力矩'), ('Joystick (4 DOF)', '摇杆（4 自由度）'),
 ('Joint angular velocity', '关节角速度'), ('Device joint angles', '设备关节角度'), ('Joint positions', '关节位置'), ('Joint position', '关节位置'),
 ('Joint angles', '关节角度'), ('Joint angle', '关节角度'), ('joint angles', '关节角度'), ('joint angle', '关节角度'), ('joint angels', '关节角度'),
 ('Joint torques', '关节力矩'), ('toques', '力矩'), ('Joint', '关节'), ('joint forces/torques', '关节力 / 力矩'),
 ('End-point posi-tion', '末端位置'), ('End point posi-tion', '末端位置'), ('End-point position', '末端位置'), ('End-point torques', '末端力矩'),
 ('End-point torque', '末端力矩'), ('End-point force', '末端力'), ('end-point force', '末端力'), ('End-point', '末端'),
 ('Fingers positions and forces', '手指位置和力'), ('Fingers positions', '手指位置'), ('Finger positions and torques', '手指位置和力矩'),
 ('Finger position and torque', '手指位置和力矩'), ('Forearm position, orientation, torque', '前臂位置、方向和力矩'),
 ('Forearm position and torque', '前臂位置和力矩'), ('Handle torque and position', '手柄力矩和位置'), ('Torque and handle position', '力矩和手柄位置'),
 ('Wrist angle, flexion torque', '腕角度、屈曲力矩'), ('Motor positions', '电机位置'), ('Actuators pressure', '驱动器压力'),
 ('actuators pressure', '驱动器压力'), ('cylinder pressure', '气缸压力'), ('grasp force', '抓握力'), ('hand force', '手部力'),
 ('forearm torque', '前臂力矩'), ('pulleys position', '滑轮位置'), ('Switches or sEMG', '开关或表面肌电'),
 ('angular velocities and forces/torques', '角速度和力 / 力矩'), ('angular velocity', '角速度'), ('Angular velocity', '角速度'),
 ('Position, force', '位置、力'), ('Position, torque', '位置、力矩'), ('Force/torque', '力 / 力矩'), ('positions', '位置'), ('position', '位置'),
 ('orientation', '方向'), ('velocity', '速度'), ('torques', '力矩'), ('torque', '力矩'), ('Torque', '力矩'), ('forces', '力'), ('force', '力'),
 ('(optional)', '（可选）'), ('Not selected yet', '尚未确定'), ('Not specified', '未说明'), ('None', '无'), ('sEMG', '表面肌电'),
 # 驱动
 ('Electric motor + 2 vibrators (for flexor and extensor tendons)', '电机 + 2 个振动器（作用于屈肌腱和伸肌腱）'),
 ('Rotary-type pneumatic actuators', '旋转式气动驱动器'), ('Linear pneumatic actuators', '直线气动驱动器'),
 ('Rotational hydroelastic actuator', '旋转式液压弹性驱动器'), ('Hydraulic brake actuators', '液压制动驱动器'),
 ('Custom-made frameless brushless motor', '定制无框无刷电机'), ('Frameless DC brushless motors', '无框直流无刷电机'),
 ('DC frameless brushless motors', '直流无框无刷电机'), ('DC brushless ser-vomotors', '直流无刷伺服电机'), ('DC brusheless servomotors', '直流无刷伺服电机'),
 ('DC brushless motors', '直流无刷电机'), ('DC brushless motor', '直流无刷电机'), ('DC brushed servomotors', '直流有刷伺服电机'),
 ('DC brushed motors', '直流有刷电机'), ('AC brushless servomotors', '交流无刷伺服电机'), ('AC brushless motors', '交流无刷电机'),
 ('DC linear motors', '直流直线电机'), ('Electric linear motors', '直线电机'), ('AC linear motor', '交流直线电机'), ('Linear stepping motors', '直线步进电机'),
 ('DC step motor', '直流步进电机'), ('DC servomotors', '直流伺服电机'), ('DC servomotor', '直流伺服电机'), ('DC servo motors', '直流伺服电机'),
 ('AC servomotors', '交流伺服电机'), ('AC servomotor', '交流伺服电机'), ('AC servo motor', '交流伺服电机'), ('Electric servomotors', '伺服电机'),
 ('Electric servo-motor', '伺服电机'), ('Digital servomotors', '数字伺服电机'), ('Servo motors', '伺服电机'), ('servo motors', '伺服电机'),
 ('magnetic particle brakes', '磁粉制动器'), ('Magnetic particle brake', '磁粉制动器'), ('ERF clutches/brakes', '电流变液离合器 / 制动器'),
 ('ERF clutches', '电流变液离合器'), ('ERF brakes', '电流变液制动器'), ('ERF brake', '电流变液制动器'), ('MRF brakes', '磁流变液制动器'),
 ('MRF brake', '磁流变液制动器'), ('Electrical motors', '电机'), ('Electric motors', '电机'), ('Electric motor', '电机'), ('electric motors', '电机'),
 ('DC motors', '直流电机'), ('DC motor', '直流电机'), ('AC motors', '交流电机'), ('AC motor', '交流电机'), ('Electric', '电动'),
 ('Pneumatic', '气动'), ('Hydraulic', '液压'), ('PAMs', '气动人工肌肉'), ('PAM', '气动人工肌肉'), ('SEA', '串联弹性驱动器'),
 ('FES', '功能性电刺激'), ('x6 per exoskeleton', '每个外骨骼 ×6'), ('grasping device', '抓握装置'),
 ('ABB IRB 140 and IRB 1400H robots', 'ABB IRB 140 和 IRB 1400H 机器人'), ('PUMA 560 robot', 'PUMA 560 机器人'),
 ('AC (x3) and DC (x2) servo motors', '交流（×3）和直流（×2）伺服电机'),
 # 类型
 ('Stationary system, may be used as an add-on for InMotion ARM', '固定式系统，可作为 InMotion ARM 的附加模块'),
 ('Add-on module for InMotion ARM', 'InMotion ARM 的附加模块'), ('parallel robot + exoskeleton-based distal part', '并联机器人 + 外骨骼式远端'),
 ('end-effector-based, planar cable-driven robot', '末端执行器式，平面绳驱机器人'), ('end-effector-based, cable-driven robot', '末端执行器式，绳驱机器人'),
 ('end-effector-based, cable-driven', '末端执行器式，绳驱'), ('end-effector-based, using haptic device', '末端执行器式，用触觉设备'),
 ('end-effector-based, rotating handle', '末端执行器式，旋转手柄'), ('end-effector-based) with various handles', '末端执行器式），配多种手柄'),
 ('end-effector-based;', '末端执行器式）；'), ('end-effector-based', '末端执行器式'), ('end-effector- based', '末端执行器式'),
 ('exoskeleton-based', '外骨骼式'), ('exoskeleton- based', '外骨骼式'), ('with desktop mounted orthosis', '配桌面固定式矫形器'),
 ('robotic arm + orthosis', '机械臂 + 矫形器'), ('2 modified indus-trial robots', '2 台改装工业机器人'), ('2 robotic arms', '2 个机械臂'),
 ('two robotic arms', '2 个机械臂'), ('2 exoskeletons', '2 个外骨骼'), ('2 parallelograms', '2 个平行四边形机构'), ('parallel robot', '并联机器人'),
 ('underactuated mechanism', '欠驱动机构'), ('continuous passive motion device', '持续被动活动设备'), ('rotating handle', '旋转手柄'),
 ('handle-like', '手柄式'), ('Wheelchair mounted gravity balancing orthosis', '轮椅安装的重力平衡矫形器'),
 ('Modular wheelchair-mounted system', '模块化轮椅安装系统'), ('Wheelchair-mounted system', '轮椅安装系统'), ('Wheelchair mounted system', '轮椅安装系统'),
 ('Stationary master-slave system', '固定式主从系统'), ('Stationary system', '固定式系统'), ('Wearable (but not portable) orthosis', '可穿戴（但不便携）矫形器'),
 ('Wearable shoulder-elbow orthosis', '可穿戴肩肘矫形器'), ('Wearable orthosis', '可穿戴矫形器'), ('wearable orthosis', '可穿戴矫形器'),
 ('Wearable glove', '可穿戴手套'), ('Wearable system', '可穿戴系统'), ('Portable orthosis', '便携矫形器'), ('Portable system', '便携系统'),
 ('Portable (Gloreha Lite)/Movable (Gloreha Professional)', '便携（Gloreha Lite）/ 可移动（Gloreha Professional）'),
 ('Modular-finger exoskeleton', '模块化手指外骨骼'), ('Finger exoskeleton', '手指外骨骼'), ('force-feedback exoskeleton', '力反馈外骨骼'),
 ('Force-feedback glove', '力反馈手套'), ('Haptic interface', '触觉接口'), ('Exercising device', '训练装置'), ('”muscle suit“', '“肌肉服”'),
 ('interactions with virtual environment', '与虚拟环境交互'), ('physical therapy and assessment of therapy results', '物理治疗和疗效评估'),
 ('power assistance and physical therapy', '助力和物理治疗'), ('power assistance for explicitly specified muscles', '为指定肌肉助力'),
 ('orthopedic physical therapy', '骨科物理治疗'), ('physical therapy of children', '儿童物理治疗'), ('physical therapy (at home)', '物理治疗（居家）'),
 ('tendon physical therapy', '肌腱物理治疗'), ('fine motor hand therapy', '手部精细运动治疗'), ('physical therapy', '物理治疗'),
 ('power assistance', '助力'), ('power assis-tance', '助力'), ('tremor suppression', '震颤抑制'), ('grasp assistance', '抓握辅助'),
 ('movement assistance', '运动辅助'), ('orthosis', '矫形器'), ('exoskeleton', '外骨骼'), ('glove', '手套'),
 # 阶段
 ('Commercial system', '商用系统'), ('FDA Class I Device', 'FDA Ⅰ类器械'), ('FDA clearance', 'FDA 许可'), ('CE Mark', 'CE 认证'), ('CE mark', 'CE 认证'),
 ('An attempt to commercialize', '曾尝试商业化'), ('First prototype', '首台原型机'), ('Prototype', '原型机'), ('Design', '设计阶段'),
 ('CIII/CIV studies', 'Ⅲ/Ⅳ类研究'), ('CIII/CIV study', 'Ⅲ/Ⅳ类研究'), ('CII studies', 'Ⅱ类研究'), ('CII study', 'Ⅱ类研究'),
 ('CI studies', 'Ⅰ类研究'), ('CI study', 'Ⅰ类研究'), ('CI:', 'Ⅰ类研究：'), ('C0 study', '0 类研究'),
 ('predecessor of', '前身为'), ('successor of', '后续为'), ('see also:', '另见：'), ('see also', '另见'), ('based on:', '基于：'), ('based on', '基于'),
 ('merges concepts from MIME and ARM Guide', '融合 MIME 和 ARM Guide 的理念'), ('extension for', '扩展用于'), ('fMRI compatible', '兼容功能磁共振'),
 ('reconfigurable robot', '可重构机器人'), ('shoulder-elbow orthosis integrated with W-EXOS system', '肩肘矫形器，集成 W-EXOS'),
 ('shoulder, 肘 and shoulder-elbow-forearm orthoses developed by Kiguchi', 'Kiguchi 开发的肩、肘及肩-肘-前臂矫形器'),
 ('Guillain-Bare syndrome', '吉兰-巴雷综合征'), ('other diseases', '其他疾病'), ('mainly ET', '以特发性震颤为主'), ('2 studies', '2 项研究'),
 ('previous name', '旧名'), ('and others', '等'), ('stroke', '卒中'), ('cS', '例慢性卒中'), ('sS', '例亚急性卒中'), ('aS', '例急性卒中'),
 ('sA', '例急性卒中'), ('hs', '名健康人'), ('MS', '例多发性硬化'), ('SCI', '例脊髓损伤'), ('TBI', '例脑外伤'), ('CP', '例脑瘫'),
 ('ET', '例特发性震颤'), ('np', '人数未报告'), ('Research device', '研究用设备'),
 # 缩写
 (' – FE', '屈伸'), ('– FE', '屈伸'), (' - FE', '屈伸'), ('--FE', '屈伸'), ('-- FE', '屈伸'), (' – GR', '抓放'), (' - GR', '抓放'), (' – PS', '旋前旋后'),
 (' – AA', '内收外展'), ('–FE', '屈伸'), ('FE', '屈伸'), ('AA', '内收外展'), ('RT', '内外旋'), ('PS', '旋前旋后'), ('GR', '抓放'),
 ('VD', '垂直位移'), ('HD', '水平位移'), (' – ', ''), ('and', '和'), (' or ', '或'), ('optional:', '可选：'), ('together', '一起'),
]
D.sort(key=lambda x: -len(x[0]))


def zh(s):
    if s in WHOLE and WHOLE[s]: return WHOLE[s]
    s = s.replace('servo-motor', 'servomotors')
    out, i = '', 0
    toks = []
    for k, v in D:
        pass
    # 单次扫描，最长匹配
    while i < len(s):
        for k, v in D:
            if s.startswith(k, i) and (k[0] in ' –-(' or not k[0].isalpha() or i == 0 or not s[i - 1].isalpha()):
                end = i + len(k)
                if k[-1].isalpha() and end < len(s) and s[end].isalpha(): continue
                out += v; i = end; break
        else:
            out += s[i]; i += 1
    out = out.replace('(x', '（×').replace('x1!)', '×1！)').replace('(', '（').replace(')', '）').replace(';', '；').replace(', ', '，').replace(',', '，')
    out = re.sub(r'（×(\d+)）', r'（×\1）', out)
    out = re.sub(r'(?<=[一-鿿]) (?=[一-鿿])', '', out)
    out = out.replace(': ', '：').replace(':', '：')
    out = re.sub(r'\s*（', '（', out); out = re.sub(r'([；，、：])\s+', r'\1', out)
    out = re.sub(r'(\d) 卒中', r'\1 例卒中', out)
    out = re.sub(r'\+ 例', '+ ', out)
    out = re.sub(r'(\d)（(\d+|人数未报告)）', r'\1(\2)', out)
    for a, b in [('名健康人（人数未报告）', '健康人（人数未报告）'), ('10 以特发性震颤为主', '10 例，以特发性震颤为主'),
                 ('2 吉兰-巴雷综合征', '2 例吉兰-巴雷综合征'), ('3 其他疾病', '3 例其他疾病'), (') 卒中', ') 例卒中'),
                 ('另见：肩，肘和肩-肘-前臂 orthoses developed by Kiguchi 和 SUEFUL-7', '另见：Kiguchi 开发的肩、肘、肩-肘-前臂矫形器和 SUEFUL-7'),
                 ('另见：肩，肘和肩-肘 orthoses developed by Kiguchi 和 SUEFUL-7', '另见：Kiguchi 开发的肩、肘、肩-肘矫形器和 SUEFUL-7'),
                 ('） 关节角度', '）；关节角度'), ('） 电机', '）；电机')]:
        out = out.replace(a, b)
    out = re.sub(r'前身为 ([^；，]+)', r'为 \1 的前身', out)
    out = re.sub(r'后续为 ([^；，]+)', r'为 \1 的后续型号', out)
    out = re.sub(r'扩展用于 ([^；，]+)', r'\1 的扩展模块', out)
    return out.strip()


def sect(t):
    m = re.match(r'Systems assisting (.*) movements', t)
    parts = re.split(r', | and ', m.group(1).replace(' (whole arm)', ''))
    z = '、'.join(SECT.get(p.strip(), p) for p in parts)
    return f'辅助{z}运动的系统' + ('（全上肢）' if 'whole arm' in t else '')


rows = [r for r in json.load(open(sys.argv[1])) if any(r['c'])]
out = []
for r in rows:
    c = r['c']
    name = c[0].replace(', previous name ', '（旧名 ').replace('; based on: ', '；基于：')
    if '（旧名' in name: name = re.sub(r'（旧名 ([^,]+),', r'（旧名 \1）,', name)
    out.append({'sect': sect(r['sect']), 'c': [name, c[1]] + [zh(x) for x in c[2:]]})
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
