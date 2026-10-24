#!/usr/bin/env python3
"""按 DOI 查找并下载论文的补充材料（视频、高清原图）。

用法：python3 fetch_supplement.py <DOI> out_dir
顺序：DOI → PMCID（PMC idconv 接口）→ Europe PMC 补充材料打包接口（zip，含 mmc*.mp4 和 gr*.jpg 高清图）。
期刊官网（Elsevier/Wiley/LWW）常返回 403 或人机验证页，这条路通常更稳。下载后自行用 ffprobe 检查。
依赖：仅标准库
"""
import json, os, sys, urllib.request, zipfile, io
doi, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0'}
def get(u, t=120):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read()
rec = json.loads(get(f'https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids={doi}&format=json'))['records'][0]
pmc = rec.get('pmcid'); print('PMCID:', pmc, ' PMID:', rec.get('pmid'))
if not pmc: sys.exit('该文没有 PMC 全文，补充材料只能去期刊网站手动下载')
try:
    z = get(f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/supplementaryFiles', 600)
    zipfile.ZipFile(io.BytesIO(z)).extractall(out)
    for f in sorted(os.listdir(out)): print(f'  {f}  {os.path.getsize(os.path.join(out, f))} bytes')
except Exception as e:
    print('Europe PMC 未提供补充材料：', e)
