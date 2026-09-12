/**
 * 图片三级回退单测
 * 直接从 index.html 里抽出 @test-block:resolver 标记之间的 resolveImage，
 * 注入假的 fetchJSON / preload，逐级验证回退行为。
 * 运行：node test/image-fallback.test.js
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const block = html.match(/@test-block:resolver[^\n]*\*\/([\s\S]*?)\/\*\s*@end-test-block/);
if (!block) { console.error('找不到 resolver 测试块'); process.exit(1); }

const ctx = { console };
vm.createContext(ctx);
vm.runInContext(block[1] + '\nthis.resolveImage = resolveImage;', ctx);
const resolveImage = ctx.resolveImage;

const GOLDEN  = { zh: '金毛寻回犬', en: 'Golden Retriever', wikiZh: '黃金獵犬', dogCeoPath: 'retriever/golden' };
const NO_CEO  = { zh: '灵缇', en: 'Greyhound', wikiZh: '靈緹', dogCeoPath: '' };
const NO_WIKI = { zh: '测试犬', en: 'Test Dog', wikiZh: '', dogCeoPath: 'beagle' };

const reject = () => Promise.reject(new Error('fail'));
const okPreload = (src) => Promise.resolve(src);

let pass = 0, fail = 0;
const cases = [];
function t(name, fn) { cases.push([name, fn]); }
function eq(actual, expected, label) {
  if (actual === expected) { pass++; console.log('  ✓ ' + label); }
  else { fail++; console.log('  ✗ ' + label + '  期望 ' + JSON.stringify(expected) + '，实际 ' + JSON.stringify(actual)); }
}

// ---- ① 维基命中 ----
t('① 维基有缩略图 → 走 wiki，并自动升到 640px', async () => {
  const calls = [];
  const r = await resolveImage(GOLDEN, {
    fetchJSON: (u) => { calls.push(u); return Promise.resolve({ thumbnail: { source: 'https://x/320px-A.jpg' } }); },
    preload: (s) => { calls.push('preload:' + s); return okPreload(s); }
  });
  eq(r.tier, 'wiki', 'tier = wiki');
  eq(r.src, 'https://x/640px-A.jpg', '缩略图升到 640px');
  eq(calls[0].includes('zh.wikipedia.org'), true, '请求的是中文维基');
  eq(calls.length, 2, 'dog.ceo 没有被调用');
});

t('① 640px 版本下载失败 → 退回原始缩略图，仍算 wiki 级', async () => {
  const r = await resolveImage(GOLDEN, {
    fetchJSON: () => Promise.resolve({ thumbnail: { source: 'https://x/320px-A.jpg' } }),
    preload: (s) => s.includes('640px') ? Promise.reject(new Error('404')) : okPreload(s)
  });
  eq(r.tier, 'wiki', 'tier = wiki');
  eq(r.src, 'https://x/320px-A.jpg', '回退到原始缩略图');
});

// ---- ② dog.ceo 命中 ----
t('② 维基请求失败 → 落到 dog.ceo', async () => {
  const urls = [];
  const r = await resolveImage(GOLDEN, {
    fetchJSON: (u) => {
      urls.push(u);
      if (u.includes('wikipedia')) return reject();
      return Promise.resolve({ status: 'success', message: 'https://images.dog.ceo/a.jpg' });
    },
    preload: okPreload
  });
  eq(r.tier, 'dogceo', 'tier = dogceo');
  eq(r.src, 'https://images.dog.ceo/a.jpg', '取到 message 字段');
  eq(urls[1], 'https://dog.ceo/api/breed/retriever/golden/images/random', '子品种路径拼接正确');
});

t('② 维基条目存在但没有配图 → 落到 dog.ceo', async () => {
  const r = await resolveImage(GOLDEN, {
    fetchJSON: (u) => u.includes('wikipedia')
      ? Promise.resolve({ title: '黃金獵犬' })                       // 无 thumbnail
      : Promise.resolve({ status: 'success', message: 'https://d/b.jpg' }),
    preload: okPreload
  });
  eq(r.tier, 'dogceo', 'tier = dogceo');
});

t('② 维基图片本身下载失败（假 200） → 落到 dog.ceo', async () => {
  const r = await resolveImage(GOLDEN, {
    fetchJSON: (u) => u.includes('wikipedia')
      ? Promise.resolve({ thumbnail: { source: 'https://x/320px-A.jpg' } })
      : Promise.resolve({ status: 'success', message: 'https://d/c.jpg' }),
    preload: (s) => s.includes('/x/') ? Promise.reject(new Error('broken')) : okPreload(s)
  });
  eq(r.tier, 'dogceo', '裂图的维基图不会被采用');
  eq(r.src, 'https://d/c.jpg', '改用 dog.ceo 的图');
});

t('② 没有 wikiZh 的条目直接跳到 dog.ceo', async () => {
  const urls = [];
  const r = await resolveImage(NO_WIKI, {
    fetchJSON: (u) => { urls.push(u); return Promise.resolve({ status: 'success', message: 'https://d/d.jpg' }); },
    preload: okPreload
  });
  eq(r.tier, 'dogceo', 'tier = dogceo');
  eq(urls.length, 1, '完全没有请求维基');
});

// ---- ③ 占位图 ----
t('③ 两级都失败 → 占位图', async () => {
  const r = await resolveImage(GOLDEN, { fetchJSON: reject, preload: reject });
  eq(r.tier, 'placeholder', 'tier = placeholder');
  eq(r.src, null, 'src 为 null，由页面渲染 SVG');
});

t('③ dogCeoPath 留空且维基失败 → 占位图（覆盖灵缇这类条目）', async () => {
  const urls = [];
  const r = await resolveImage(NO_CEO, {
    fetchJSON: (u) => { urls.push(u); return reject(); },
    preload: reject
  });
  eq(r.tier, 'placeholder', 'tier = placeholder');
  eq(urls.length, 1, '空路径不会拼出 dog.ceo/api/breed//images/random');
});

t('③ dog.ceo 返回 status=error → 占位图', async () => {
  const r = await resolveImage(GOLDEN, {
    fetchJSON: (u) => u.includes('wikipedia') ? reject() : Promise.resolve({ status: 'error', message: 'Breed not found' }),
    preload: okPreload
  });
  eq(r.tier, 'placeholder', 'status=error 不被当成成功');
});

t('③ 全链路网络断开（离线）→ 占位图，绝不裂图', async () => {
  const boom = () => Promise.reject(new TypeError('Failed to fetch'));
  const r = await resolveImage(GOLDEN, { fetchJSON: boom, preload: boom });
  eq(r.tier, 'placeholder', '离线也能收敛到占位图');
});

(async () => {
  for (const [name, fn] of cases) { console.log('\n' + name); await fn(); }
  console.log('\n────────────────────────');
  console.log(fail === 0 ? `全部通过：${pass} 项断言` : `失败 ${fail} 项 / 通过 ${pass} 项`);
  process.exit(fail === 0 ? 0 : 1);
})();
