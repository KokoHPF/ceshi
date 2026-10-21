SPEC = [
 ('Step1Generalizedmodel', '步骤 1　通用模型'), ('Step2Personalizedmodel', '步骤 2　个体化模型'),
 ('Participant P1', '受试者 P1'), ('Participant P2', '受试者 P2'), ('Participant P3', '受试者 P3'),
 ('Average spinal cord dimensions', '平均脊髓尺寸'), ('vertebrae', '椎骨'),
 ('Step 3 Simulations basedon incremental models', '步骤 3　逐步细化模型的模拟'), ('Step4 Finalplacementandpredictiveposition', '步骤 4　最终置入位置与预测位置'),
 (['Generalizedmodel', 'withgenericmotor', 'neuron locations'], '通用模型＋\n通用运动神经元位置'),
 (['Generalized model', 'withpersonalized@283,530', 'projectome@284,544'], '通用模型＋\n个体化投射区'),
 (['Personalized model@443,524', 'with generic projectome'], '个体化模型＋\n通用投射区'),
 (['Personalized model@604,517', 'with personalized@604,531', 'projectome@606,546'], '个体化模型＋\n个体化投射区'),
 (['Personalized vertebrae', 'with optimal lead position'], '个体化椎骨＋\n最佳电极位置'), (['CT Scan of intra-', 'operative lead position'], '术中电极位置的\n断层扫描'),
 (['Prediction matches', 'validated optimal', 'leadposition'], '预测与验证的\n最佳电极位置一致', {'al': 'l'}),
 (['Prediction does not match', 'validated optimal lead position'], '预测与验证的最佳\n电极位置不一致'),
 (['I shift@178,728', 'Rostrocaudal@178,766'], '头尾向移动', {'rot': True}), (['I shift@172,971', 'Rostrocaudal@172,1011'], '头尾向移动', {'rot': True}),
 ('Combined selectivity', '综合选择性'), ('Rostrocaudal shift', '头尾向移动'),
 (['Patient-specific projectome', 'is similar to generic', 'projectome'], '个体投射区\n与通用投射区相似', {'al': 'l'}),
 (['Positionstestedtocoverthelumbosacralspinalsegments', 'mismatchbetweengeneralizedandpersonalized', 'model due to difference in segmental alignment'],
  '测试的位置覆盖腰骶脊髓节段；\n节段对位不同，导致通用模型\n与个体化模型不一致', {'al': 'l'}),
]
EXTRA = []
