# 一百种狗狗 · 品种图鉴

一个可以直接双击打开的单页图鉴，收录 100 个真实犬种，按 AKC 七大组别整理。

```
index.html   页面（内联 CSS/JS，无构建步骤、无框架依赖）
breeds.js    数据层（GROUPS + BREEDS，替换此文件即可换掉全站内容）
test/        图片三级回退的单元测试：node test/image-fallback.test.js
```

## 数据

`breeds.js` 导出两个全局变量：

- `GROUPS`：AKC 七大组别，各自带浅色/深色两套语义色
- `BREEDS`：100 条犬种记录，字段说明写在文件头部的注释里

数据与视图完全分离，`index.html` 只依赖上面两个变量的结构。

## 图片

页面不内置任何图片，运行时在浏览器端按三级回退抓取：

1. 中文维基百科条目摘要里的 `thumbnail.source`（自动升到 640px）
2. `dog.ceo` 对应路径的随机图
3. 统一风格的线描 SVG 占位图（描边走 `currentColor`，自动跟随组别色与深色模式）

每张候选图都会先用 `Image` 实际下载验证一次，避免"HTTP 200 但内容坏掉"导致裂图；
并发上限 6，配合 `IntersectionObserver` 懒加载；结果只存内存 `Map`，不使用 localStorage。

离线打开时会全部落到第三级占位图，页面依然完整可用。
