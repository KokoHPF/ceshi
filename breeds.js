/*!
 * breeds.js — 100 种狗狗品种数据
 * ---------------------------------------------------------------
 * 纯数据层，与视图完全分离。替换本文件即可换掉整站内容，
 * index.html 只依赖下面两个全局变量：GROUPS 和 BREEDS。
 *
 * BREEDS 每条记录的字段：
 *   zh          中文名
 *   en          英文名
 *   origin      原产国 / 地区
 *   group       AKC 组别 key，取值见 GROUPS
 *   size        体型：'小' | '中' | '大'
 *   height      肩高区间（cm）
 *   weight      体重区间（kg）
 *   life        平均寿命
 *   traits      性格关键词，固定 3 个
 *   exercise    运动需求 1-5
 *   shedding    掉毛程度 1-5
 *   novice      新手友好度 1-5
 *   intro       40 字以内简介
 *   fact        一条冷知识
 *   wikiZh      中文维基条目名（图片来源一级回退）
 *   wikiEn      英文维基条目名（详情页外链）
 *   dogCeoPath  dog.ceo 路径（图片来源二级回退），不确定则留空字符串
 * ---------------------------------------------------------------
 */

/** AKC 七大组别：中文名 + 浅色/深色两套语义色 */
const GROUPS = [
  { key: 'sporting',    label: '运动犬组',   en: 'Sporting',     color: '#C2703D', colorDark: '#E09A6B' },
  { key: 'hound',       label: '猎犬组',     en: 'Hound',        color: '#B08A3E', colorDark: '#D4B473' },
  { key: 'working',     label: '工作犬组',   en: 'Working',      color: '#A35A4E', colorDark: '#D08A7E' },
  { key: 'terrier',     label: '㹴犬组',     en: 'Terrier',      color: '#4E7C8A', colorDark: '#86B3C0' },
  { key: 'toy',         label: '玩赏犬组',   en: 'Toy',          color: '#9C6B8F', colorDark: '#C79BBB' },
  { key: 'nonsporting', label: '非运动犬组', en: 'Non-Sporting', color: '#6B6F8C', colorDark: '#A0A4BE' },
  { key: 'herding',     label: '牧羊犬组',   en: 'Herding',      color: '#7C8B6F', colorDark: '#AEBBA0' }
];

const BREEDS = [
  /* ============ 运动犬组 Sporting（14 条） ============ */
  {
    zh: '金毛寻回犬', en: 'Golden Retriever', origin: '英国（苏格兰）', group: 'sporting',
    size: '大', height: '51–61 cm', weight: '25–34 kg', life: '10–12 年',
    traits: ['温顺', '聪明', '亲人'], exercise: 4, shedding: 5, novice: 5,
    intro: '性格稳定的家庭伴侣犬，对人几乎没有戒心，服从性高，适合初次养狗的家庭。',
    fact: '它最初被培育来叼回坠水的猎禽，嘴劲轻到可以叼住一枚生鸡蛋而不弄破。',
    wikiZh: '黃金獵犬', wikiEn: 'Golden Retriever', dogCeoPath: 'retriever/golden'
  },
  {
    zh: '拉布拉多寻回犬', en: 'Labrador Retriever', origin: '加拿大', group: 'sporting',
    size: '大', height: '54–57 cm', weight: '25–36 kg', life: '10–12 年',
    traits: ['忠诚', '贪吃', '稳定'], exercise: 4, shedding: 4, novice: 5,
    intro: '全球最常见的导盲与工作犬之一，食欲旺盛、学习快，需要严格控制体重。',
    fact: '祖先是纽芬兰的圣约翰水犬，拥有防水双层被毛和粗壮的“水獭尾”作方向舵。',
    wikiZh: '拉布拉多犬', wikiEn: 'Labrador Retriever', dogCeoPath: 'labrador'
  },
  {
    zh: '切萨皮克海湾寻回犬', en: 'Chesapeake Bay Retriever', origin: '美国', group: 'sporting',
    size: '大', height: '53–66 cm', weight: '25–36 kg', life: '10–13 年',
    traits: ['坚韧', '护主', '独立'], exercise: 5, shedding: 3, novice: 2,
    intro: '寻回犬里最硬派的一支，主见强、护卫心重，需要有经验的主人引导。',
    fact: '被毛带油脂且短硬，能在接近冰点的水里连续叼回上百只野鸭。',
    wikiZh: '乞沙比克獵犬', wikiEn: 'Chesapeake Bay Retriever', dogCeoPath: 'retriever/chesapeake'
  },
  {
    zh: '平毛寻回犬', en: 'Flat-Coated Retriever', origin: '英国', group: 'sporting',
    size: '大', height: '56–62 cm', weight: '25–36 kg', life: '8–10 年',
    traits: ['开朗', '长不大', '友善'], exercise: 5, shedding: 3, novice: 3,
    intro: '永远像幼犬一样跳脱的黑色寻回犬，对陌生人也毫无敌意，几乎不适合看家。',
    fact: '被爱好者称为“彼得潘犬”，三四岁了仍保持幼犬般的举止与好奇心。',
    wikiZh: '平毛尋回犬', wikiEn: 'Flat-coated Retriever', dogCeoPath: 'retriever/flatcoated'
  },
  {
    zh: '美国可卡犬', en: 'American Cocker Spaniel', origin: '美国', group: 'sporting',
    size: '中', height: '34–39 cm', weight: '7–14 kg', life: '12–15 年',
    traits: ['甜美', '粘人', '敏感'], exercise: 3, shedding: 3, novice: 4,
    intro: 'AKC 运动犬组体型最小的成员，情感需求高，长耳朵需要每周清理护理。',
    fact: '耳朵长到垂进饭盆，所以许多主人要为它准备口径特别窄的锥形犬碗。',
    wikiZh: '美國可卡犬', wikiEn: 'American Cocker Spaniel', dogCeoPath: 'spaniel/cocker'
  },
  {
    zh: '英国史宾格犬', en: 'English Springer Spaniel', origin: '英国', group: 'sporting',
    size: '中', height: '46–51 cm', weight: '18–25 kg', life: '12–14 年',
    traits: ['热情', '勤奋', '亲人'], exercise: 5, shedding: 3, novice: 4,
    intro: '耐力极好的中型猎鸟犬，也是常见的缉毒与搜救犬，需要大量户外活动。',
    fact: '名字来自它的工作方式——冲进灌木丛把鸟“惊飞”（spring）起来让猎人射击。',
    wikiZh: '英國史賓格犬', wikiEn: 'English Springer Spaniel', dogCeoPath: 'springer/english'
  },
  {
    zh: '布列塔尼犬', en: 'Brittany', origin: '法国', group: 'sporting',
    size: '中', height: '44–52 cm', weight: '14–18 kg', life: '12–14 年',
    traits: ['活泼', '敏捷', '黏人'], exercise: 5, shedding: 3, novice: 3,
    intro: '兼具指示与寻回能力的紧凑型猎犬，反应快、精力充沛，很难接受长时间独处。',
    fact: '它是历史上获得美国“田野冠军”头衔最多的犬种，部分个体天生短尾。',
    wikiZh: '布列塔尼犬', wikiEn: 'Brittany dog', dogCeoPath: 'spaniel/brittany'
  },
  {
    zh: '爱尔兰塞特犬', en: 'Irish Setter', origin: '爱尔兰', group: 'sporting',
    size: '大', height: '61–67 cm', weight: '24–32 kg', life: '12–15 年',
    traits: ['热情', '顽皮', '晚熟'], exercise: 5, shedding: 3, novice: 3,
    intro: '一身红栗色长毛的大型猎鸟犬，社交欲极强，心理成熟要到三岁以后。',
    fact: '因为长期保持幼犬心态，圈内常戏称它是“永远处在青春期”的犬种。',
    wikiZh: '愛爾蘭雪達犬', wikiEn: 'Irish Setter', dogCeoPath: 'setter/irish'
  },
  {
    zh: '英国塞特犬', en: 'English Setter', origin: '英国', group: 'sporting',
    size: '大', height: '58–69 cm', weight: '20–36 kg', life: '10–12 年',
    traits: ['温和', '优雅', '合群'], exercise: 4, shedding: 3, novice: 3,
    intro: '举止斯文的老牌猎鸟犬，与同类和小孩都相处融洽，被毛需要定期梳理。',
    fact: '它身上细碎的斑点花纹有专门的名称“贝尔顿”（Belton），按底色分若干种。',
    wikiZh: '英國雪達犬', wikiEn: 'English Setter', dogCeoPath: 'setter/english'
  },
  {
    zh: '戈登塞特犬', en: 'Gordon Setter', origin: '英国（苏格兰）', group: 'sporting',
    size: '大', height: '58–69 cm', weight: '20–36 kg', life: '10–12 年',
    traits: ['忠诚', '自信', '沉着'], exercise: 4, shedding: 3, novice: 2,
    intro: '三种塞特犬中骨量最重的一支，对家人专一，对陌生人则相当保留。',
    fact: '黑底加红褐斑的经典配色，定型于 19 世纪苏格兰戈登公爵的私人犬舍。',
    wikiZh: '戈登雪達犬', wikiEn: 'Gordon Setter', dogCeoPath: 'setter/gordon'
  },
  {
    zh: '德国短毛指示犬', en: 'German Shorthaired Pointer', origin: '德国', group: 'sporting',
    size: '大', height: '53–64 cm', weight: '20–32 kg', life: '10–12 年',
    traits: ['精力旺', '聪明', '全能'], exercise: 5, shedding: 3, novice: 2,
    intro: '陆地追踪、水中叼回、指示鸟位样样都行的全能猎犬，运动量需求极大。',
    fact: '脚趾之间有蹼，既能在水中推进，也能在松软的沼泽地上分散体重。',
    wikiZh: '德國短毛指示犬', wikiEn: 'German Shorthaired Pointer', dogCeoPath: 'pointer/german'
  },
  {
    zh: '维兹拉犬', en: 'Vizsla', origin: '匈牙利', group: 'sporting',
    size: '中', height: '53–61 cm', weight: '20–29 kg', life: '12–14 年',
    traits: ['黏人', '敏感', '耐力好'], exercise: 5, shedding: 2, novice: 3,
    intro: '匈牙利的国宝级猎犬，锈金色短毛，极度依恋主人，独处容易焦虑。',
    fact: '被称为“魔术贴犬”，因为总紧贴着人；它的鼻头和眼圈与被毛同色。',
    wikiZh: '維茲拉犬', wikiEn: 'Vizsla', dogCeoPath: 'vizsla'
  },
  {
    zh: '威玛猎犬', en: 'Weimaraner', origin: '德国', group: 'sporting',
    size: '大', height: '56–69 cm', weight: '25–40 kg', life: '10–13 年',
    traits: ['警觉', '黏人', '好动'], exercise: 5, shedding: 2, novice: 2,
    intro: '银灰被毛配琥珀色眼睛的大型猎犬，精力与分离焦虑都是养育难点。',
    fact: '因为独特的毛色和悄无声息的移动方式，它被称为“灰色幽灵”。',
    wikiZh: '威瑪犬', wikiEn: 'Weimaraner', dogCeoPath: 'weimaraner'
  },
  {
    zh: '苏塞克斯獚', en: 'Sussex Spaniel', origin: '英国', group: 'sporting',
    size: '中', height: '33–38 cm', weight: '16–20 kg', life: '11–13 年',
    traits: ['沉稳', '慢性子', '忠厚'], exercise: 3, shedding: 3, novice: 3,
    intro: '身长腿短的金肝色獚犬，节奏慢、脾气好，是极稀有的英国古老犬种。',
    fact: '它是唯一会一边搜寻猎物一边吠叫报信的獚犬，方便猎人在密林中定位。',
    wikiZh: '蘇塞克斯獵犬', wikiEn: 'Sussex Spaniel', dogCeoPath: 'spaniel/sussex'
  },

  /* ============ 猎犬组 Hound（15 条） ============ */
  {
    zh: '比格犬', en: 'Beagle', origin: '英国', group: 'hound',
    size: '中', height: '33–41 cm', weight: '9–11 kg', life: '12–15 年',
    traits: ['好奇', '合群', '吃货'], exercise: 4, shedding: 3, novice: 4,
    intro: '嗅觉驱动的群猎犬，性格开朗但容易循着气味走丢，吠声洪亮。',
    fact: '美国农业部的检疫犬队就叫“米格鲁旅”，专门在机场嗅查违禁农产品。',
    wikiZh: '米格魯', wikiEn: 'Beagle', dogCeoPath: 'beagle'
  },
  {
    zh: '腊肠犬', en: 'Dachshund', origin: '德国', group: 'hound',
    size: '小', height: '13–23 cm', weight: '4–15 kg', life: '12–16 年',
    traits: ['勇敢', '固执', '爱挖'], exercise: 3, shedding: 3, novice: 3,
    intro: '长身短腿的洞穴猎犬，胆子极大，需要避免跳跃以保护椎间盘。',
    fact: '德语名字直译就是“獾犬”，长身短腿正是为了钻进獾洞里作战。',
    wikiZh: '臘腸犬', wikiEn: 'Dachshund', dogCeoPath: 'dachshund'
  },
  {
    zh: '巴吉度猎犬', en: 'Basset Hound', origin: '法国', group: 'hound',
    size: '中', height: '28–38 cm', weight: '20–29 kg', life: '12–13 年',
    traits: ['憨厚', '固执', '温和'], exercise: 2, shedding: 3, novice: 3,
    intro: '短腿重骨的追踪犬，节奏慢、嗓门低，训练时需要足够的耐心和零食。',
    fact: '拖地的长耳朵会把地面气味扇向鼻子，追踪能力仅次于寻血猎犬。',
    wikiZh: '巴吉度獵犬', wikiEn: 'Basset Hound', dogCeoPath: 'hound/basset'
  },
  {
    zh: '寻血猎犬', en: 'Bloodhound', origin: '比利时', group: 'hound',
    size: '大', height: '58–69 cm', weight: '36–50 kg', life: '10–12 年',
    traits: ['执着', '温顺', '慢热'], exercise: 4, shedding: 3, novice: 2,
    intro: '世界上鼻子最好的犬种，一旦锁定气味几乎无法叫停，口水量惊人。',
    fact: '在美国部分州，经过认证的寻血猎犬追踪结果可以作为法庭证据采信。',
    wikiZh: '尋血獵犬', wikiEn: 'Bloodhound', dogCeoPath: 'hound/blood'
  },
  {
    zh: '阿富汗猎犬', en: 'Afghan Hound', origin: '阿富汗', group: 'hound',
    size: '大', height: '63–74 cm', weight: '23–27 kg', life: '12–14 年',
    traits: ['高冷', '独立', '优雅'], exercise: 4, shedding: 2, novice: 1,
    intro: '视觉型猎犬中最华丽的一种，被毛需要天天打理，召回训练极具挑战。',
    fact: '那身长丝被毛原本是高原御寒装备，在阿富汗山区能抵御严寒和碎石。',
    wikiZh: '阿富汗獵犬', wikiEn: 'Afghan Hound', dogCeoPath: 'hound/afghan'
  },
  {
    zh: '灵缇', en: 'Greyhound', origin: '英国', group: 'hound',
    size: '大', height: '68–76 cm', weight: '27–40 kg', life: '10–14 年',
    traits: ['温和', '安静', '爆发力强'], exercise: 3, shedding: 1, novice: 4,
    intro: '短跑之王，但日常极为安静，每天两次散步加一次冲刺就足够。',
    fact: '冲刺时速可达 70 公里，回到家却是出了名的“沙发土豆”。',
    wikiZh: '靈緹', wikiEn: 'Greyhound', dogCeoPath: ''
  },
  {
    zh: '惠比特犬', en: 'Whippet', origin: '英国', group: 'hound',
    size: '中', height: '44–56 cm', weight: '11–18 kg', life: '12–15 年',
    traits: ['安静', '温柔', '敏捷'], exercise: 3, shedding: 1, novice: 4,
    intro: '灵缇的缩小版，室内几乎没有存在感，怕冷且体脂极低需要软垫。',
    fact: '19 世纪英国矿工用它比赛消遣，因此得名“穷人的赛马”。',
    wikiZh: '惠比特犬', wikiEn: 'Whippet', dogCeoPath: 'whippet'
  },
  {
    zh: '罗德西亚脊背犬', en: 'Rhodesian Ridgeback', origin: '南非', group: 'hound',
    size: '大', height: '61–69 cm', weight: '29–39 kg', life: '10–12 年',
    traits: ['独立', '沉稳', '护主'], exercise: 4, shedding: 2, novice: 2,
    intro: '力量型的南非猎犬，对家人温和，对陌生人保留，需要坚定一致的规则。',
    fact: '背脊上有一道逆向生长的毛脊，过去成群使用来牵制狮子等待猎人。',
    wikiZh: '羅德西亞背脊犬', wikiEn: 'Rhodesian Ridgeback', dogCeoPath: 'ridgeback/rhodesian'
  },
  {
    zh: '萨路基猎犬', en: 'Saluki', origin: '中东', group: 'hound',
    size: '大', height: '58–71 cm', weight: '18–27 kg', life: '12–14 年',
    traits: ['矜持', '敏感', '优雅'], exercise: 4, shedding: 1, novice: 2,
    intro: '身形极瘦的沙漠视猎犬，情感内敛，不喜欢被强行拥抱或粗暴对待。',
    fact: '它是最古老的犬种之一，古埃及墓室壁画上已经出现了它的身影。',
    wikiZh: '薩路基犬', wikiEn: 'Saluki', dogCeoPath: 'saluki'
  },
  {
    zh: '苏俄猎狼犬', en: 'Borzoi', origin: '俄罗斯', group: 'hound',
    size: '大', height: '68–85 cm', weight: '27–48 kg', life: '9–14 年',
    traits: ['安静', '矜持', '优雅'], exercise: 3, shedding: 3, novice: 2,
    intro: '体型高大却举止安静的丝毛视猎犬，追逐本能强，散步务必牵绳。',
    fact: '沙俄贵族成对放出它来围捕野狼，一场狩猎常动用上百只。',
    wikiZh: '俄羅斯獵狼犬', wikiEn: 'Borzoi', dogCeoPath: 'borzoi'
  },
  {
    zh: '爱尔兰猎狼犬', en: 'Irish Wolfhound', origin: '爱尔兰', group: 'hound',
    size: '大', height: '76–86 cm', weight: '48–70 kg', life: '6–8 年',
    traits: ['温和', '沉稳', '亲人'], exercise: 3, shedding: 3, novice: 3,
    intro: '身高居犬界之首却性情温吞，居家安静，但幼犬期骨骼发育需格外小心。',
    fact: '它是 AKC 认可犬种中最高的一种，寿命却通常只有六到八年。',
    wikiZh: '愛爾蘭獵狼犬', wikiEn: 'Irish Wolfhound', dogCeoPath: 'wolfhound/irish'
  },
  {
    zh: '苏格兰猎鹿犬', en: 'Scottish Deerhound', origin: '英国', group: 'hound',
    size: '大', height: '71–81 cm', weight: '34–50 kg', life: '8–11 年',
    traits: ['温和', '安静', '尊贵'], exercise: 4, shedding: 2, novice: 2,
    intro: '披着粗硬灰蓝色被毛的大型视猎犬，室内安静，室外需要大面积跑动。',
    fact: '在苏格兰历史上，只有伯爵以上的贵族才有资格饲养这个犬种。',
    wikiZh: '蘇格蘭獵鹿犬', wikiEn: 'Scottish Deerhound', dogCeoPath: 'deerhound/scottish'
  },
  {
    zh: '伊比赞猎犬', en: 'Ibizan Hound', origin: '西班牙', group: 'hound',
    size: '大', height: '56–74 cm', weight: '20–25 kg', life: '11–14 年',
    traits: ['机警', '顽皮', '爱跳'], exercise: 5, shedding: 1, novice: 2,
    intro: '大立耳的地中海猎兔犬，弹跳力惊人，院子围栏必须做到足够高。',
    fact: '它能从原地垂直跳过一人多高的围墙，被称为会“跳高”的猎犬。',
    wikiZh: '依比沙獵犬', wikiEn: 'Ibizan Hound', dogCeoPath: 'hound/ibizan'
  },
  {
    zh: '巴仙吉犬', en: 'Basenji', origin: '中非', group: 'hound',
    size: '中', height: '40–43 cm', weight: '9–11 kg', life: '13–14 年',
    traits: ['独立', '爱干净', '机灵'], exercise: 4, shedding: 1, novice: 2,
    intro: '来自刚果的原始猎犬，几乎没有体味，独立性强，服从训练难度高。',
    fact: '它不会汪汪叫，喉部结构特殊，只能发出类似约德尔唱腔的怪声。',
    wikiZh: '巴辛吉犬', wikiEn: 'Basenji', dogCeoPath: 'basenji'
  },
  {
    zh: '挪威猎麋犬', en: 'Norwegian Elkhound', origin: '挪威', group: 'hound',
    size: '中', height: '49–52 cm', weight: '20–23 kg', life: '12–15 年',
    traits: ['勇敢', '友善', '有主见'], exercise: 4, shedding: 5, novice: 3,
    intro: '灰色双层厚毛的北欧狩猎犬，耐寒能力极强，换毛季掉毛量非常可观。',
    fact: '维京时代它就随船出海，狩猎时靠围住麋鹿持续吠叫等待猎人赶到。',
    wikiZh: '挪威獵麋犬', wikiEn: 'Norwegian Elkhound', dogCeoPath: 'elkhound/norwegian'
  },

  /* ============ 工作犬组 Working（16 条） ============ */
  {
    zh: '西伯利亚雪橇犬', en: 'Siberian Husky', origin: '俄罗斯', group: 'working',
    size: '中', height: '50–60 cm', weight: '16–27 kg', life: '12–14 年',
    traits: ['活泼', '爱闹', '爱逃'], exercise: 5, shedding: 5, novice: 2,
    intro: '耐力型雪橇犬，拆家与越狱能力并存，几乎没有护卫意识。',
    fact: '1925 年它们接力把白喉血清送进阿拉斯加诺姆镇，纽约中央公园为此立像。',
    wikiZh: '西伯利亞雪橇犬', wikiEn: 'Siberian Husky', dogCeoPath: 'husky'
  },
  {
    zh: '阿拉斯加雪橇犬', en: 'Alaskan Malamute', origin: '美国', group: 'working',
    size: '大', height: '58–64 cm', weight: '34–39 kg', life: '10–14 年',
    traits: ['憨厚', '固执', '力大'], exercise: 4, shedding: 5, novice: 2,
    intro: '体格厚重的重载雪橇犬，力量惊人，对同性犬有较强的支配欲。',
    fact: '它的定位是重载慢跑的货运犬，与追求速度的哈士奇完全是两种分工。',
    wikiZh: '阿拉斯加雪橇犬', wikiEn: 'Alaskan Malamute', dogCeoPath: 'malamute'
  },
  {
    zh: '萨摩耶犬', en: 'Samoyed', origin: '俄罗斯', group: 'working',
    size: '中', height: '48–60 cm', weight: '16–30 kg', life: '12–14 年',
    traits: ['爱笑', '亲人', '爱叫'], exercise: 4, shedding: 5, novice: 3,
    intro: '西伯利亚的白色牧鹿犬，社交需求高，被毛打理和掉毛量是主要负担。',
    fact: '嘴角上扬的“萨摩耶微笑”其实是实用结构，可以防止口水滴落结冰。',
    wikiZh: '薩摩耶犬', wikiEn: 'Samoyed dog', dogCeoPath: 'samoyed'
  },
  {
    zh: '罗威纳犬', en: 'Rottweiler', origin: '德国', group: 'working',
    size: '大', height: '56–69 cm', weight: '35–60 kg', life: '9–10 年',
    traits: ['自信', '沉稳', '护主'], exercise: 4, shedding: 3, novice: 2,
    intro: '力量与自信兼备的护卫犬，需要从幼犬期开始持续社会化与规则训练。',
    fact: '它的祖先是随罗马军团翻越阿尔卑斯山、负责驱赶军粮牛群的赶牛犬。',
    wikiZh: '羅威納犬', wikiEn: 'Rottweiler', dogCeoPath: 'rottweiler'
  },
  {
    zh: '杜宾犬', en: 'Doberman Pinscher', origin: '德国', group: 'working',
    size: '大', height: '61–72 cm', weight: '27–45 kg', life: '10–13 年',
    traits: ['警觉', '聪明', '黏人'], exercise: 5, shedding: 2, novice: 2,
    intro: '反应极快的护卫犬，其实非常依恋家人，独处时间过长容易出问题。',
    fact: '19 世纪末由一位身兼税务员和捕犬员的德国人培育，目的是保护自己收税。',
    wikiZh: '杜賓犬', wikiEn: 'Dobermann', dogCeoPath: 'doberman'
  },
  {
    zh: '拳师犬', en: 'Boxer', origin: '德国', group: 'working',
    size: '大', height: '53–64 cm', weight: '25–32 kg', life: '10–12 年',
    traits: ['顽皮', '忠诚', '长不大'], exercise: 5, shedding: 2, novice: 3,
    intro: '心态永远停在少年期的护卫犬，对小孩耐心，短鼻结构不耐高温。',
    fact: '它打招呼时喜欢用两只前爪拍打对方，“拳师”的名字正来源于此。',
    wikiZh: '拳師犬', wikiEn: 'Boxer (dog)', dogCeoPath: 'boxer'
  },
  {
    zh: '大丹犬', en: 'Great Dane', origin: '德国', group: 'working',
    size: '大', height: '71–86 cm', weight: '50–79 kg', life: '7–10 年',
    traits: ['温和', '亲人', '粘人'], exercise: 3, shedding: 3, novice: 3,
    intro: '体型巨大但性情温和的伴侣犬，运动量中等，需要防范胃扭转风险。',
    fact: '它被称为“温柔的巨人”，常常忘记自己的体型，试图坐到人的腿上。',
    wikiZh: '大丹犬', wikiEn: 'Great Dane', dogCeoPath: 'dane/great'
  },
  {
    zh: '圣伯纳犬', en: 'St. Bernard', origin: '瑞士', group: 'working',
    size: '大', height: '65–90 cm', weight: '54–82 kg', life: '8–10 年',
    traits: ['温厚', '沉稳', '慢吞吞'], exercise: 2, shedding: 4, novice: 3,
    intro: '阿尔卑斯山口的救援犬后裔，性格厚道，口水多且极不耐热。',
    fact: '脖子上挂小酒桶的经典形象纯属 19 世纪一位画家的想象，历史上并不存在。',
    wikiZh: '聖伯納犬', wikiEn: 'St. Bernard (dog)', dogCeoPath: 'stbernard'
  },
  {
    zh: '纽芬兰犬', en: 'Newfoundland', origin: '加拿大', group: 'working',
    size: '大', height: '66–71 cm', weight: '45–68 kg', life: '9–10 年',
    traits: ['温柔', '耐心', '爱水'], exercise: 3, shedding: 4, novice: 3,
    intro: '天生的水上救生犬，对孩子极有耐心，厚重被毛需要大量梳理时间。',
    fact: '它的脚掌有蹼，游泳时用的是蹬水式而非常见的刨水式，推进效率更高。',
    wikiZh: '紐芬蘭犬', wikiEn: 'Newfoundland dog', dogCeoPath: 'newfoundland'
  },
  {
    zh: '伯恩山犬', en: 'Bernese Mountain Dog', origin: '瑞士', group: 'working',
    size: '大', height: '58–70 cm', weight: '32–52 kg', life: '7–10 年',
    traits: ['温和', '忠厚', '慢热'], exercise: 3, shedding: 4, novice: 3,
    intro: '三色被毛的瑞士农场犬，对家人极其依恋，遗憾的是寿命偏短。',
    fact: '过去瑞士农民让它拉着装满奶酪的小车走山路，一只犬可拉起自重数倍的货。',
    wikiZh: '伯恩山犬', wikiEn: 'Bernese Mountain Dog', dogCeoPath: 'mountain/bernese'
  },
  {
    zh: '大白熊犬', en: 'Great Pyrenees', origin: '法国', group: 'working',
    size: '大', height: '65–82 cm', weight: '39–73 kg', life: '10–12 年',
    traits: ['独立', '沉稳', '夜巡'], exercise: 3, shedding: 4, novice: 2,
    intro: '典型的护羊犬，独立决策能力强，服从性一般，夜间吠叫是天性。',
    fact: '它的后肢通常长着双悬趾，这是护羊犬在陡坡上稳住身体的古老特征。',
    wikiZh: '大白熊犬', wikiEn: 'Great Pyrenees', dogCeoPath: 'pyrenees'
  },
  {
    zh: '藏獒', en: 'Tibetan Mastiff', origin: '中国（西藏）', group: 'working',
    size: '大', height: '61–76 cm', weight: '34–73 kg', life: '10–12 年',
    traits: ['独立', '护地盘', '倔强'], exercise: 3, shedding: 4, novice: 1,
    intro: '高原护卫犬，领地意识极强，不适合城市与缺乏经验的饲主。',
    fact: '它一年只换一次毛，而且多数母犬一年只发情一次，繁殖节律接近野生犬科。',
    wikiZh: '藏獒', wikiEn: 'Tibetan Mastiff', dogCeoPath: 'mastiff/tibetan'
  },
  {
    zh: '英国獒犬', en: 'English Mastiff', origin: '英国', group: 'working',
    size: '大', height: '70–91 cm', weight: '54–100 kg', life: '6–10 年',
    traits: ['沉稳', '温和', '护家'], exercise: 2, shedding: 3, novice: 2,
    intro: '体重居犬界之首的古老獒犬，日常慵懒，但幼犬期的力量控制是难点。',
    fact: '有记录的最重个体超过 150 公斤，被列入吉尼斯世界纪录。',
    wikiZh: '英國獒犬', wikiEn: 'English Mastiff', dogCeoPath: 'mastiff/english'
  },
  {
    zh: '秋田犬', en: 'Akita', origin: '日本', group: 'working',
    size: '大', height: '61–71 cm', weight: '32–59 kg', life: '10–13 年',
    traits: ['忠诚', '矜持', '爱干净'], exercise: 3, shedding: 5, novice: 2,
    intro: '日本国家天然纪念物，对家人忠诚，对同性犬容忍度低，不喜被陌生人触碰。',
    fact: '在涩谷车站等了主人九年的“忠犬八公”，就是一只秋田犬。',
    wikiZh: '秋田犬', wikiEn: 'Akita (dog)', dogCeoPath: 'akita'
  },
  {
    zh: '莱昂贝格犬', en: 'Leonberger', origin: '德国', group: 'working',
    size: '大', height: '65–80 cm', weight: '41–77 kg', life: '8–9 年',
    traits: ['温和', '沉稳', '爱水'], exercise: 3, shedding: 5, novice: 2,
    intro: '狮鬃般被毛的大型伴侣犬，情绪稳定，常用于水上救援和治疗犬工作。',
    fact: '两次世界大战后全球仅剩八只可繁育个体，今天所有莱昂贝格犬都源自它们。',
    wikiZh: '蘭伯格犬', wikiEn: 'Leonberger', dogCeoPath: 'leonberg'
  },
  {
    zh: '可蒙犬', en: 'Komondor', origin: '匈牙利', group: 'working',
    size: '大', height: '65–80 cm', weight: '36–61 kg', life: '10–12 年',
    traits: ['独立', '沉稳', '护群'], exercise: 3, shedding: 1, novice: 1,
    intro: '一身绳索状毛辫的匈牙利护羊犬，几乎不掉毛，但毛辫护理极其费时。',
    fact: '那身毛辫让它混在羊群里几乎难以分辨，也能挡住狼牙的撕咬。',
    wikiZh: '可蒙犬', wikiEn: 'Komondor', dogCeoPath: 'komondor'
  },

  /* ============ 㹴犬组 Terrier（15 条） ============ */
  {
    zh: '西高地白㹴', en: 'West Highland White Terrier', origin: '英国', group: 'terrier',
    size: '小', height: '25–28 cm', weight: '6–10 kg', life: '13–15 年',
    traits: ['自信', '开朗', '固执'], exercise: 3, shedding: 2, novice: 4,
    intro: '苏格兰高地的捕鼠小㹴，性格自信开朗，皮肤敏感需要注意饮食。',
    fact: '一身纯白被毛是刻意选育的结果，为的是在荒野上不被猎人误认成猎物。',
    wikiZh: '西高地白㹴', wikiEn: 'West Highland White Terrier', dogCeoPath: 'terrier/westhighland'
  },
  {
    zh: '苏格兰㹴', en: 'Scottish Terrier', origin: '英国', group: 'terrier',
    size: '小', height: '25–28 cm', weight: '8–10 kg', life: '11–13 年',
    traits: ['独立', '倔强', '尊贵'], exercise: 3, shedding: 2, novice: 2,
    intro: '短腿长脸的黑色小㹴，独立性强，对主人忠诚但不轻易讨好任何人。',
    fact: '罗斯福总统的爱犬“法拉”就是苏格兰㹴，曾随总统出席雅尔塔会议。',
    wikiZh: '蘇格蘭㹴', wikiEn: 'Scottish Terrier', dogCeoPath: 'terrier/scottish'
  },
  {
    zh: '凯恩㹴', en: 'Cairn Terrier', origin: '英国', group: 'terrier',
    size: '小', height: '24–33 cm', weight: '6–8 kg', life: '13–15 年',
    traits: ['机灵', '勇敢', '爱挖'], exercise: 3, shedding: 2, novice: 4,
    intro: '毛糙耐脏的小型工作㹴，适应力强，挖掘欲旺盛，院子容易遭殃。',
    fact: '《绿野仙踪》里桃乐丝的小狗托托，就是由一只凯恩㹴出演的。',
    wikiZh: '凱恩㹴', wikiEn: 'Cairn Terrier', dogCeoPath: 'terrier/cairn'
  },
  {
    zh: '杰克罗素㹴', en: 'Russell Terrier', origin: '英国', group: 'terrier',
    size: '小', height: '25–30 cm', weight: '4–8 kg', life: '13–16 年',
    traits: ['精力旺', '机灵', '闹腾'], exercise: 5, shedding: 3, novice: 2,
    intro: '体型虽小但运动需求极高，聪明好动，缺乏消耗时破坏力惊人。',
    fact: '由一位英国牧师培育，标准要求胸围窄到能被人双手环握，好钻进狐狸洞。',
    wikiZh: '傑克羅素㹴', wikiEn: 'Russell Terrier', dogCeoPath: 'terrier/russell'
  },
  {
    zh: '万能㹴', en: 'Airedale Terrier', origin: '英国', group: 'terrier',
    size: '大', height: '56–61 cm', weight: '22–32 kg', life: '11–14 年',
    traits: ['自信', '聪明', '多才'], exercise: 4, shedding: 2, novice: 3,
    intro: '体型最大的㹴犬，既能狩猎也能护卫，需要足够的脑力游戏消耗。',
    fact: '它被称为“㹴犬之王”，第一次世界大战期间在战场上当过信使犬。',
    wikiZh: '萬能㹴', wikiEn: 'Airedale Terrier', dogCeoPath: 'airedale'
  },
  {
    zh: '边境㹴', en: 'Border Terrier', origin: '英国', group: 'terrier',
    size: '小', height: '28–40 cm', weight: '5–7 kg', life: '12–15 年',
    traits: ['随和', '耐劳', '亲人'], exercise: 4, shedding: 2, novice: 4,
    intro: '㹴犬里性格最温和的一支，耐力好、易相处，适合活跃的家庭。',
    fact: '它是少数能跟上马队长途奔跑的小型㹴犬，腿长比例特意留得偏高。',
    wikiZh: '邊境㹴', wikiEn: 'Border Terrier', dogCeoPath: 'terrier/border'
  },
  {
    zh: '贝灵顿㹴', en: 'Bedlington Terrier', origin: '英国', group: 'terrier',
    size: '中', height: '39–44 cm', weight: '8–10 kg', life: '11–16 年',
    traits: ['温和', '敏捷', '倔强'], exercise: 4, shedding: 1, novice: 3,
    intro: '外形酷似小羊羔的卷毛㹴犬，室内安静，遇到挑衅时毫不退让。',
    fact: '19 世纪英国矿工用它抓老鼠并参加打斗，绵羊般的外表完全是伪装。',
    wikiZh: '貝林登㹴', wikiEn: 'Bedlington Terrier', dogCeoPath: 'terrier/bedlington'
  },
  {
    zh: '爱尔兰㹴', en: 'Irish Terrier', origin: '爱尔兰', group: 'terrier',
    size: '中', height: '46–48 cm', weight: '11–12 kg', life: '13–15 年',
    traits: ['勇敢', '忠诚', '好胜'], exercise: 4, shedding: 2, novice: 2,
    intro: '红褐色被毛的中型㹴犬，对人热情，对同性犬的容忍度却很低。',
    fact: '一战中它担任前线信使犬，因无畏的作风被士兵称为“红色魔鬼”。',
    wikiZh: '愛爾蘭㹴', wikiEn: 'Irish Terrier', dogCeoPath: 'terrier/irish'
  },
  {
    zh: '凯利蓝㹴', en: 'Kerry Blue Terrier', origin: '爱尔兰', group: 'terrier',
    size: '中', height: '46–50 cm', weight: '15–18 kg', life: '12–15 年',
    traits: ['聪明', '好胜', '活泼'], exercise: 4, shedding: 1, novice: 2,
    intro: '几乎不掉毛的蓝灰色㹴犬，学习快，但需要持续的犬际社会化。',
    fact: '幼犬出生时通体乌黑，要花一年半到两年才逐渐褪成标志性的蓝灰色。',
    wikiZh: '凱利藍㹴', wikiEn: 'Kerry Blue Terrier', dogCeoPath: 'terrier/kerryblue'
  },
  {
    zh: '迷你雪纳瑞', en: 'Miniature Schnauzer', origin: '德国', group: 'terrier',
    size: '小', height: '30–36 cm', weight: '5–9 kg', life: '12–15 年',
    traits: ['机警', '爱叫', '亲人'], exercise: 3, shedding: 1, novice: 5,
    intro: '掉毛极少的城市伴侣犬，警觉爱叫，胡子需要每次进食后清理。',
    fact: '标志性的大胡子原本是实用“护具”，用来保护口鼻不被老鼠咬伤。',
    wikiZh: '迷你雪納瑞', wikiEn: 'Miniature Schnauzer', dogCeoPath: 'schnauzer/miniature'
  },
  {
    zh: '美国斯塔福德㹴', en: 'American Staffordshire Terrier', origin: '美国', group: 'terrier',
    size: '中', height: '43–48 cm', weight: '18–32 kg', life: '12–16 年',
    traits: ['自信', '亲人', '勇敢'], exercise: 4, shedding: 2, novice: 2,
    intro: '肌肉结实、对人极其友好的力量型㹴犬，犬际相处需要主人把控。',
    fact: '一战期间美国的宣传海报常用它作为国家形象的拟人化代表。',
    wikiZh: '美國斯塔福郡㹴', wikiEn: 'American Staffordshire Terrier', dogCeoPath: 'terrier/american'
  },
  {
    zh: '斯塔福斗牛㹴', en: 'Staffordshire Bull Terrier', origin: '英国', group: 'terrier',
    size: '中', height: '36–41 cm', weight: '11–17 kg', life: '12–14 年',
    traits: ['亲人', '勇敢', '耐痛'], exercise: 4, shedding: 2, novice: 3,
    intro: '短小精悍的英国㹴犬，对人热情外向，运动需求高但居住空间要求低。',
    fact: '在英国它有“保姆犬”的绰号，以对小孩出了名的耐心而著称。',
    wikiZh: '斯塔福郡鬥牛㹴', wikiEn: 'Staffordshire Bull Terrier', dogCeoPath: 'bullterrier/staffordshire'
  },
  {
    zh: '牛头㹴', en: 'Bull Terrier', origin: '英国', group: 'terrier',
    size: '中', height: '53–56 cm', weight: '22–38 kg', life: '11–14 年',
    traits: ['顽皮', '固执', '搞怪'], exercise: 4, shedding: 2, novice: 2,
    intro: '性格像个大孩子的肌肉型㹴犬，好奇心重，容易误食异物需要留意。',
    fact: '它是唯一拥有三角形眼睛的犬种，鸡蛋形的侧脸轮廓也是品种标准之一。',
    wikiZh: '牛頭㹴', wikiEn: 'Bull Terrier', dogCeoPath: 'bullterrier'
  },
  {
    zh: '软毛麦色㹴', en: 'Soft Coated Wheaten Terrier', origin: '爱尔兰', group: 'terrier',
    size: '中', height: '43–48 cm', weight: '13–18 kg', life: '12–14 年',
    traits: ['开朗', '热情', '爱扑'], exercise: 4, shedding: 1, novice: 3,
    intro: '柔软丝质被毛的爱尔兰农场㹴，对人热情到需要专门训练不扑人。',
    fact: '它见到人就直立起来贴脸问好，这个招牌动作被称为“小麦跳”。',
    wikiZh: '愛爾蘭軟毛麥色㹴', wikiEn: 'Soft-Coated Wheaten Terrier', dogCeoPath: 'terrier/wheaten'
  },
  {
    zh: '丹迪丁蒙㹴', en: 'Dandie Dinmont Terrier', origin: '英国', group: 'terrier',
    size: '小', height: '20–28 cm', weight: '8–11 kg', life: '12–15 年',
    traits: ['独立', '沉稳', '倔强'], exercise: 3, shedding: 1, novice: 2,
    intro: '头顶一簇蓬松丝毛的稀有㹴犬，嗓音低沉，性格比多数㹴犬安静。',
    fact: '它是唯一以小说人物命名的犬种，名字出自司各特的《盖伊·曼纳令》。',
    wikiZh: '丹第丁蒙㹴', wikiEn: 'Dandie Dinmont Terrier', dogCeoPath: 'terrier/dandie'
  },

  /* ============ 玩赏犬组 Toy（15 条） ============ */
  {
    zh: '吉娃娃', en: 'Chihuahua', origin: '墨西哥', group: 'toy',
    size: '小', height: '15–23 cm', weight: '1.5–3 kg', life: '12–20 年',
    traits: ['大胆', '黏人', '警觉'], exercise: 2, shedding: 2, novice: 3,
    intro: '世界上最小的犬种，胆量与体型完全不成比例，怕冷且易骨折。',
    fact: '它的头骨顶部常留有一块未完全闭合的“泉门”，类似婴儿的囟门。',
    wikiZh: '吉娃娃', wikiEn: 'Chihuahua (dog)', dogCeoPath: 'chihuahua'
  },
  {
    zh: '博美犬', en: 'Pomeranian', origin: '德国 / 波兰', group: 'toy',
    size: '小', height: '18–30 cm', weight: '1.5–3 kg', life: '12–16 年',
    traits: ['活泼', '爱叫', '自信'], exercise: 3, shedding: 4, novice: 3,
    intro: '蓬松双层被毛的小型尖嘴犬，警觉爱叫，需要从小做减敏训练。',
    fact: '它的祖先是几十公斤重的北欧雪橇犬，维多利亚女王带火了小型化版本。',
    wikiZh: '博美犬', wikiEn: 'Pomeranian dog', dogCeoPath: 'pomeranian'
  },
  {
    zh: '约克夏㹴', en: 'Yorkshire Terrier', origin: '英国', group: 'toy',
    size: '小', height: '18–23 cm', weight: '2–3 kg', life: '13–16 年',
    traits: ['大胆', '黏人', '机灵'], exercise: 2, shedding: 1, novice: 3,
    intro: '起源于纺织厂捕鼠工作的迷你㹴犬，胆大黏人，长毛需要每日梳理。',
    fact: '它的被毛是丝状结构，更接近人的头发，因此几乎不随季节脱落。',
    wikiZh: '約克夏㹴', wikiEn: 'Yorkshire Terrier', dogCeoPath: 'terrier/yorkshire'
  },
  {
    zh: '马尔济斯犬', en: 'Maltese', origin: '马耳他', group: 'toy',
    size: '小', height: '20–25 cm', weight: '2–4 kg', life: '12–15 年',
    traits: ['温柔', '粘人', '活泼'], exercise: 2, shedding: 1, novice: 3,
    intro: '一身纯白垂坠长毛的古老玩赏犬，情感需求高，泪痕需要日常护理。',
    fact: '古希腊人曾为它立过墓碑，是有文字记载最古老的玩赏犬之一。',
    wikiZh: '馬爾濟斯犬', wikiEn: 'Maltese dog', dogCeoPath: 'maltese'
  },
  {
    zh: '蝴蝶犬', en: 'Papillon', origin: '法国 / 比利时', group: 'toy',
    size: '小', height: '20–28 cm', weight: '3–5 kg', life: '14–16 年',
    traits: ['聪明', '活泼', '敏捷'], exercise: 3, shedding: 2, novice: 4,
    intro: '玩赏犬里学习能力最强的一种，常在敏捷比赛中击败大型犬。',
    fact: '名字是法语的“蝴蝶”，指两只饰毛张开的大耳朵；垂耳型则被称作“蛾犬”。',
    wikiZh: '蝴蝶犬', wikiEn: 'Papillon dog', dogCeoPath: 'papillon'
  },
  {
    zh: '巴哥犬', en: 'Pug', origin: '中国', group: 'toy',
    size: '小', height: '25–33 cm', weight: '6–8 kg', life: '12–15 年',
    traits: ['憨厚', '粘人', '爱睡'], exercise: 2, shedding: 4, novice: 4,
    intro: '短鼻皱脸的中国古老玩赏犬，性格憨厚，但呼吸道结构决定它极不耐热。',
    fact: '英语里一群巴哥的集合量词是 grumble（咕哝），源自它们独特的呼噜声。',
    wikiZh: '巴哥犬', wikiEn: 'Pug', dogCeoPath: 'pug'
  },
  {
    zh: '西施犬', en: 'Shih Tzu', origin: '中国', group: 'toy',
    size: '小', height: '23–27 cm', weight: '4–7 kg', life: '10–16 年',
    traits: ['甜美', '黏人', '倔强'], exercise: 2, shedding: 1, novice: 4,
    intro: '典型的膝上犬，运动需求低、掉毛少，长毛若不剪短需每天梳理。',
    fact: '名字意为“狮子狗”，曾长期是清宫御犬，几乎不被允许流出宫外。',
    wikiZh: '西施犬', wikiEn: 'Shih Tzu', dogCeoPath: 'shihtzu'
  },
  {
    zh: '骑士查理王小猎犬', en: 'Cavalier King Charles Spaniel', origin: '英国', group: 'toy',
    size: '小', height: '30–33 cm', weight: '5–8 kg', life: '12–15 年',
    traits: ['温顺', '亲人', '随和'], exercise: 3, shedding: 3, novice: 5,
    intro: '脾气最好的玩赏犬之一，对人对犬都友好，需要定期做心脏检查。',
    fact: '据说查理二世曾下令允许这种犬进入任何公共场所，包括英国议会大厦。',
    wikiZh: '騎士查理王獵犬', wikiEn: 'Cavalier King Charles Spaniel', dogCeoPath: 'spaniel/blenheim'
  },
  {
    zh: '京巴犬', en: 'Pekingese', origin: '中国', group: 'toy',
    size: '小', height: '15–23 cm', weight: '3–6 kg', life: '12–15 年',
    traits: ['高傲', '忠诚', '独立'], exercise: 2, shedding: 4, novice: 3,
    intro: '步态摇摆的宫廷犬，自尊心强、不喜被随意摆布，短鼻同样不耐热。',
    fact: '它曾是紫禁城的御用犬，1860 年英法联军攻入圆明园后被带往欧洲。',
    wikiZh: '北京犬', wikiEn: 'Pekingese', dogCeoPath: 'pekinese'
  },
  {
    zh: '意大利灵缇', en: 'Italian Greyhound', origin: '意大利', group: 'toy',
    size: '小', height: '33–38 cm', weight: '3–5 kg', life: '14–15 年',
    traits: ['敏感', '黏人', '怕冷'], exercise: 3, shedding: 1, novice: 3,
    intro: '迷你版视猎犬，室内安静爱钻被窝，骨骼纤细需要防止高处跳落。',
    fact: '它的腿骨极细，从沙发上跳下都可能骨折，冬天外出通常需要穿衣。',
    wikiZh: '義大利靈緹', wikiEn: 'Italian Greyhound', dogCeoPath: 'greyhound/italian'
  },
  {
    zh: '玩具贵宾犬', en: 'Toy Poodle', origin: '法国 / 德国', group: 'toy',
    size: '小', height: '24–28 cm', weight: '2–4 kg', life: '12–18 年',
    traits: ['聪明', '敏感', '活泼'], exercise: 3, shedding: 1, novice: 4,
    intro: '贵宾犬中最小的尺寸，几乎不掉毛，但需要每月修剪并注意膝关节。',
    fact: '贵宾犬的三种尺寸在 AKC 属于同一个犬种，只按肩高划分组别。',
    wikiZh: '貴賓犬', wikiEn: 'Poodle', dogCeoPath: 'poodle/toy'
  },
  {
    zh: '迷你杜宾犬', en: 'Miniature Pinscher', origin: '德国', group: 'toy',
    size: '小', height: '25–32 cm', weight: '4–5 kg', life: '12–16 年',
    traits: ['自信', '好动', '爱探险'], exercise: 3, shedding: 2, novice: 2,
    intro: '被称为“玩具犬之王”的小型护院犬，好奇心强，逃跑技能一流。',
    fact: '它并不是缩小版的杜宾犬，两者没有直接血缘；走路是高抬腿的“马步”。',
    wikiZh: '迷你杜賓犬', wikiEn: 'Miniature Pinscher', dogCeoPath: 'pinscher/miniature'
  },
  {
    zh: '日本狆', en: 'Japanese Chin', origin: '日本', group: 'toy',
    size: '小', height: '20–27 cm', weight: '2–5 kg', life: '12–14 年',
    traits: ['优雅', '安静', '猫性'], exercise: 2, shedding: 3, novice: 3,
    intro: '举止优雅安静的日本宫廷犬，独立性偏强，情绪细腻不喜欢喧闹。',
    fact: '它会用前爪洗脸、喜欢爬到高处观察，行为习惯常被形容为像猫。',
    wikiZh: '日本狆', wikiEn: 'Japanese Chin', dogCeoPath: 'spaniel/japanese'
  },
  {
    zh: '猴㹴', en: 'Affenpinscher', origin: '德国', group: 'toy',
    size: '小', height: '23–30 cm', weight: '3–6 kg', life: '12–15 年',
    traits: ['顽皮', '大胆', '搞怪'], exercise: 3, shedding: 2, novice: 3,
    intro: '表情丰富的粗毛小型犬，自认体型很大，对陌生犬毫不怯场。',
    fact: '德语名字意为“猴子㹴”，而法国人则叫它“留小胡子的小魔鬼”。',
    wikiZh: '猴㹴', wikiEn: 'Affenpinscher', dogCeoPath: 'affenpinscher'
  },
  {
    zh: '哈瓦那犬', en: 'Havanese', origin: '古巴', group: 'toy',
    size: '小', height: '23–29 cm', weight: '3–6 kg', life: '14–16 年',
    traits: ['开朗', '黏人', '爱表演'], exercise: 3, shedding: 1, novice: 5,
    intro: '古巴唯一的本土犬种，性格外向、掉毛极少，非常适合公寓生活。',
    fact: '它走路时后腿有独特的弹跳感，这种步态被称为“哈瓦那弹簧步”。',
    wikiZh: '哈瓦那犬', wikiEn: 'Havanese dog', dogCeoPath: 'havanese'
  },

  /* ============ 非运动犬组 Non-Sporting（12 条） ============ */
  {
    zh: '英国斗牛犬', en: 'Bulldog', origin: '英国', group: 'nonsporting',
    size: '中', height: '31–40 cm', weight: '18–25 kg', life: '8–10 年',
    traits: ['沉稳', '倔强', '爱赖'], exercise: 2, shedding: 3, novice: 3,
    intro: '头大身宽的短鼻犬，性格温吞好相处，对热和剧烈运动都很脆弱。',
    fact: '因为胎儿头部过大，绝大多数斗牛犬必须靠剖腹产出生；它们也几乎不会游泳。',
    wikiZh: '鬥牛犬', wikiEn: 'Bulldog', dogCeoPath: 'bulldog/english'
  },
  {
    zh: '法国斗牛犬', en: 'French Bulldog', origin: '法国', group: 'nonsporting',
    size: '小', height: '28–33 cm', weight: '8–13 kg', life: '10–12 年',
    traits: ['亲人', '搞笑', '安静'], exercise: 2, shedding: 3, novice: 4,
    intro: '城市公寓的热门选择，运动需求低、吠叫少，但呼吸道问题需长期关注。',
    fact: '因短鼻结构风险，多数航空公司禁止法斗以货舱方式托运。',
    wikiZh: '法國鬥牛犬', wikiEn: 'French Bulldog', dogCeoPath: 'bulldog/french'
  },
  {
    zh: '波士顿㹴', en: 'Boston Terrier', origin: '美国', group: 'nonsporting',
    size: '小', height: '38–43 cm', weight: '5–11 kg', life: '11–13 年',
    traits: ['开朗', '亲人', '好脾气'], exercise: 3, shedding: 2, novice: 5,
    intro: '黑白配色的小型伴侣犬，脾气温和、适应力强，是新手的稳妥选择。',
    fact: '因为天生像穿着礼服的配色，它被称为“美国绅士”，也是马萨诸塞州的州犬。',
    wikiZh: '波士頓㹴', wikiEn: 'Boston Terrier', dogCeoPath: 'bulldog/boston'
  },
  {
    zh: '标准贵宾犬', en: 'Standard Poodle', origin: '德国 / 法国', group: 'nonsporting',
    size: '大', height: '45–60 cm', weight: '20–32 kg', life: '12–15 年',
    traits: ['聪明', '敏感', '活跃'], exercise: 4, shedding: 1, novice: 4,
    intro: '智商名列前茅的水猎犬后裔，几乎不掉毛，但美容成本不低。',
    fact: '夸张的“狮子剪”有实用来源——保住关节和胸腔的保暖，同时减少水中阻力。',
    wikiZh: '貴賓犬', wikiEn: 'Poodle', dogCeoPath: 'poodle/standard'
  },
  {
    zh: '迷你贵宾犬', en: 'Miniature Poodle', origin: '德国 / 法国', group: 'nonsporting',
    size: '小', height: '28–38 cm', weight: '5–8 kg', life: '12–16 年',
    traits: ['聪明', '机敏', '黏人'], exercise: 3, shedding: 1, novice: 4,
    intro: '介于标准与玩具尺寸之间，学习能力强，适合想要低掉毛量的家庭。',
    fact: '它是马戏团最爱的犬种之一，学会一条新指令平均只需不到五次重复。',
    wikiZh: '貴賓犬', wikiEn: 'Poodle', dogCeoPath: 'poodle/miniature'
  },
  {
    zh: '大麦町犬', en: 'Dalmatian', origin: '克罗地亚', group: 'nonsporting',
    size: '大', height: '48–61 cm', weight: '20–32 kg', life: '11–13 年',
    traits: ['精力旺', '忠诚', '独立'], exercise: 5, shedding: 5, novice: 2,
    intro: '历史上的马车护卫犬，耐力惊人，短硬被毛掉毛量常被低估。',
    fact: '幼犬出生时全身纯白，那些著名的黑色斑点要到三四周后才逐渐显现。',
    wikiZh: '大麥町犬', wikiEn: 'Dalmatian dog', dogCeoPath: 'dalmatian'
  },
  {
    zh: '松狮犬', en: 'Chow Chow', origin: '中国', group: 'nonsporting',
    size: '中', height: '43–51 cm', weight: '20–32 kg', life: '8–12 年',
    traits: ['高冷', '独立', '认主'], exercise: 2, shedding: 5, novice: 1,
    intro: '中国古老的多用途犬，性格独立疏离，往往只认定一位主人。',
    fact: '它和沙皮犬一样长着蓝紫色的舌头，后腿几乎笔直，因此走路像踩高跷。',
    wikiZh: '鬆獅犬', wikiEn: 'Chow Chow', dogCeoPath: 'chow'
  },
  {
    zh: '沙皮犬', en: 'Chinese Shar-Pei', origin: '中国', group: 'nonsporting',
    size: '中', height: '46–51 cm', weight: '20–27 kg', life: '8–12 年',
    traits: ['独立', '沉稳', '忠诚'], exercise: 2, shedding: 2, novice: 2,
    intro: '广东南部的古老犬种，皮肤褶皱需要保持干燥，对陌生人相当戒备。',
    fact: '1978 年它曾被吉尼斯纪录列为“世界最稀有犬种”，靠海外繁育才救回族群。',
    wikiZh: '沙皮犬', wikiEn: 'Shar Pei', dogCeoPath: 'sharpei'
  },
  {
    zh: '柴犬', en: 'Shiba Inu', origin: '日本', group: 'nonsporting',
    size: '中', height: '33–43 cm', weight: '8–11 kg', life: '13–16 年',
    traits: ['独立', '爱干净', '倔强'], exercise: 3, shedding: 4, novice: 2,
    intro: '日本最小的本土犬种，爱干净、好训厕所，但召回训练难度很高。',
    fact: '被强行摆布时会发出高分贝的“柴犬尖叫”；它也会像猫一样自己舔毛清洁。',
    wikiZh: '柴犬', wikiEn: 'Shiba Inu', dogCeoPath: 'shiba'
  },
  {
    zh: '拉萨犬', en: 'Lhasa Apso', origin: '中国（西藏）', group: 'nonsporting',
    size: '小', height: '25–28 cm', weight: '5–8 kg', life: '12–15 年',
    traits: ['独立', '警觉', '倔强'], exercise: 2, shedding: 1, novice: 2,
    intro: '西藏寺院的室内哨兵犬，警觉性高、主见强，长毛护理相当费时。',
    fact: '它在寺院里担任内哨，靠敏锐听觉报警，藏语名字的含义近似“吠声哨兵”。',
    wikiZh: '拉薩犬', wikiEn: 'Lhasa Apso', dogCeoPath: 'lhasa'
  },
  {
    zh: '比熊犬', en: 'Bichon Frise', origin: '法国 / 西班牙', group: 'nonsporting',
    size: '小', height: '23–30 cm', weight: '5–8 kg', life: '14–15 年',
    traits: ['开朗', '亲人', '爱闹'], exercise: 3, shedding: 1, novice: 4,
    intro: '性格阳光的白色卷毛犬，掉毛极少，但需要高频次的专业美容。',
    fact: '蓬松的“粉扑”造型必须靠逆向吹梳才能立起来，是美容师的基本功。',
    wikiZh: '比熊犬', wikiEn: 'Bichon Frise', dogCeoPath: 'frise/bichon'
  },
  {
    zh: '荷兰毛狮犬', en: 'Keeshond', origin: '荷兰', group: 'nonsporting',
    size: '中', height: '43–48 cm', weight: '16–20 kg', life: '12–15 年',
    traits: ['亲人', '合群', '爱叫'], exercise: 3, shedding: 5, novice: 4,
    intro: '荷兰驳船上的看家犬，对家人极其黏，双层厚毛掉毛量大。',
    fact: '眼睛周围深浅相间的纹路像戴了一副眼镜，是该品种不可缺少的特征。',
    wikiZh: '荷蘭毛獅犬', wikiEn: 'Keeshond', dogCeoPath: 'keeshond'
  },

  /* ============ 牧羊犬组 Herding（13 条） ============ */
  {
    zh: '德国牧羊犬', en: 'German Shepherd', origin: '德国', group: 'herding',
    size: '大', height: '55–65 cm', weight: '22–40 kg', life: '9–13 年',
    traits: ['聪明', '忠诚', '勤奋'], exercise: 5, shedding: 5, novice: 3,
    intro: '世界上应用最广的工作犬，需要明确的任务感，缺乏训练易出行为问题。',
    fact: '整个品种由一位德国骑兵上尉在 1899 年从一只名叫 Horand 的犬开始系统培育。',
    wikiZh: '德國牧羊犬', wikiEn: 'German Shepherd', dogCeoPath: 'germanshepherd'
  },
  {
    zh: '边境牧羊犬', en: 'Border Collie', origin: '英国', group: 'herding',
    size: '中', height: '46–56 cm', weight: '14–20 kg', life: '12–15 年',
    traits: ['聪明', '工作狂', '敏感'], exercise: 5, shedding: 4, novice: 2,
    intro: '公认智商最高的犬种，脑力消耗不足时会自行“发明”工作，例如追车。',
    fact: '它靠一种被称为“凝视”的眼神压力控制羊群；有个体能辨认上千个玩具名字。',
    wikiZh: '邊境牧羊犬', wikiEn: 'Border Collie', dogCeoPath: 'collie/border'
  },
  {
    zh: '澳大利亚牧羊犬', en: 'Australian Shepherd', origin: '美国', group: 'herding',
    size: '中', height: '46–58 cm', weight: '16–32 kg', life: '12–15 年',
    traits: ['精力旺', '聪明', '黏人'], exercise: 5, shedding: 4, novice: 2,
    intro: '美国西部牧场的全能牧羊犬，需要高强度运动与持续的脑力任务。',
    fact: '尽管名字叫澳大利亚牧羊犬，它其实定型于美国西部，与澳大利亚关系不大。',
    wikiZh: '澳洲牧羊犬', wikiEn: 'Australian Shepherd', dogCeoPath: 'australian/shepherd'
  },
  {
    zh: '喜乐蒂牧羊犬', en: 'Shetland Sheepdog', origin: '英国', group: 'herding',
    size: '小', height: '33–41 cm', weight: '6–12 kg', life: '12–14 年',
    traits: ['敏感', '聪明', '爱叫'], exercise: 4, shedding: 5, novice: 3,
    intro: '小型长毛牧羊犬，服从性极高但也非常爱叫，需要早期做减敏。',
    fact: '它不是缩小版的苏格兰牧羊犬，而是设得兰群岛上独立发展出的小型犬种。',
    wikiZh: '喜樂蒂牧羊犬', wikiEn: 'Shetland Sheepdog', dogCeoPath: 'sheepdog/shetland'
  },
  {
    zh: '粗毛柯利牧羊犬', en: 'Rough Collie', origin: '英国', group: 'herding',
    size: '大', height: '51–66 cm', weight: '20–34 kg', life: '12–14 年',
    traits: ['温和', '敏感', '亲人'], exercise: 4, shedding: 5, novice: 4,
    intro: '性情温和的长毛牧羊犬，对孩子友善，厚重被毛需要固定梳理。',
    fact: '因电影《灵犬莱西》风靡全球；部分个体带 MDR1 基因突变，对某些药物敏感。',
    wikiZh: '蘇格蘭牧羊犬', wikiEn: 'Rough Collie', dogCeoPath: ''
  },
  {
    zh: '古代英国牧羊犬', en: 'Old English Sheepdog', origin: '英国', group: 'herding',
    size: '大', height: '51–61 cm', weight: '27–45 kg', life: '10–12 年',
    traits: ['憨厚', '顽皮', '慢性子'], exercise: 3, shedding: 5, novice: 2,
    intro: '一身厚重长毛的赶群犬，性格憨厚爱闹，被毛管理是最大的门槛。',
    fact: '过去农民会剃下它的毛纺成线织衣；它走路是熊一样左右摇摆的步态。',
    wikiZh: '古代英國牧羊犬', wikiEn: 'Old English Sheepdog', dogCeoPath: 'sheepdog/english'
  },
  {
    zh: '彭布罗克威尔士柯基', en: 'Pembroke Welsh Corgi', origin: '英国', group: 'herding',
    size: '小', height: '25–30 cm', weight: '10–14 kg', life: '12–15 年',
    traits: ['活泼', '聪明', '爱叫'], exercise: 3, shedding: 4, novice: 4,
    intro: '短腿赶牛犬，精力比外形更旺盛，需要控制体重以保护脊椎。',
    fact: '英国女王伊丽莎白二世一生养过三十多只柯基，几乎都是这一支。',
    wikiZh: '彭布羅克威爾斯柯基犬', wikiEn: 'Pembroke Welsh Corgi', dogCeoPath: 'pembroke'
  },
  {
    zh: '卡迪根威尔士柯基', en: 'Cardigan Welsh Corgi', origin: '英国', group: 'herding',
    size: '小', height: '26–32 cm', weight: '11–17 kg', life: '12–15 年',
    traits: ['沉稳', '机警', '忠诚'], exercise: 3, shedding: 4, novice: 3,
    intro: '比彭布罗克更古老的一支柯基，骨量更重，性格也更沉稳保留。',
    fact: '两种柯基最直观的区别是尾巴——卡迪根天生带一条长而蓬松的大尾巴。',
    wikiZh: '卡提根威爾斯柯基犬', wikiEn: 'Cardigan Welsh Corgi', dogCeoPath: 'corgi/cardigan'
  },
  {
    zh: '比利时玛利诺犬', en: 'Belgian Malinois', origin: '比利时', group: 'herding',
    size: '大', height: '56–66 cm', weight: '18–36 kg', life: '14–16 年',
    traits: ['精力旺', '专注', '警觉'], exercise: 5, shedding: 3, novice: 1,
    intro: '当今各国军警的主力工作犬，驱动力极高，完全不适合普通家庭。',
    fact: '它可以跟随伞兵一起跳伞执行任务，通常与训导员绑在同一副伞具上。',
    wikiZh: '比利時瑪利諾犬', wikiEn: 'Malinois dog', dogCeoPath: 'malinois'
  },
  {
    zh: '比利时特伏丹犬', en: 'Belgian Tervuren', origin: '比利时', group: 'herding',
    size: '大', height: '56–66 cm', weight: '20–34 kg', life: '12–14 年',
    traits: ['聪明', '警觉', '黏人'], exercise: 5, shedding: 4, novice: 1,
    intro: '长毛版的比利时牧羊犬，敏感聪明，需要大量的陪伴与工作任务。',
    fact: '它与玛利诺同源，只是被毛长度与颜色不同，比利时本国视为同一个品种。',
    wikiZh: '比利時特伏丹犬', wikiEn: 'Tervuren', dogCeoPath: 'tervuren'
  },
  {
    zh: '比利时格罗安达犬', en: 'Belgian Sheepdog', origin: '比利时', group: 'herding',
    size: '大', height: '56–66 cm', weight: '20–34 kg', life: '12–14 年',
    traits: ['警觉', '忠诚', '敏感'], exercise: 5, shedding: 4, novice: 1,
    intro: '通体纯黑长毛的比利时牧羊犬，警戒心强，对陌生环境反应敏锐。',
    fact: '第一次世界大战期间，它曾担任红十字会的伤员搜救犬和前线信使。',
    wikiZh: '比利時格羅安達犬', wikiEn: 'Groenendael', dogCeoPath: 'groenendael'
  },
  {
    zh: '澳大利亚牧牛犬', en: 'Australian Cattle Dog', origin: '澳大利亚', group: 'herding',
    size: '中', height: '43–51 cm', weight: '15–22 kg', life: '12–16 年',
    traits: ['硬朗', '机灵', '爱咬脚'], exercise: 5, shedding: 3, novice: 1,
    intro: '为长途驱赶牛群而生的硬派工作犬，咬脚跟的本能需要专门纠正。',
    fact: '它的血统中混有澳洲野犬丁格，这让它具备极强的耐热与耐力。',
    wikiZh: '澳洲牧牛犬', wikiEn: 'Australian Cattle Dog', dogCeoPath: 'cattledog/australian'
  },
  {
    zh: '布里亚德犬', en: 'Briard', origin: '法国', group: 'herding',
    size: '大', height: '56–69 cm', weight: '25–45 kg', life: '11–12 年',
    traits: ['忠诚', '独立', '护主'], exercise: 4, shedding: 3, novice: 2,
    intro: '长毛遮眼的法国牧羊犬，护卫意识强，需要早期充分的社会化。',
    fact: '拿破仑和杰斐逊都养过这个品种；一战时它是法军的搜救与哨兵犬。',
    wikiZh: '伯瑞犬', wikiEn: 'Briard', dogCeoPath: 'briard'
  }
];

/* 同时支持 <script> 全局引入与模块化引入，方便后续替换数据源 */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { GROUPS, BREEDS };
}
