#!/usr/bin/env python3
"""把 article_body.html 上传到公众号草稿箱（只进草稿箱，不会群发）。

用法：
    export WX_APPID=你的AppID WX_SECRET=你的AppSecret
    python3 build.py && python3 upload_draft.py
    # 更新已有草稿（不新建）：再加 WX_DRAFT_ID=草稿的 media_id

前提：运行本脚本的机器出口 IP 已加入公众号后台「设置与开发 → 基本配置 → IP 白名单」。
"""
import json
import os
import pathlib
import re
import sys
import urllib.request
import uuid

HERE = pathlib.Path(__file__).parent
API = "https://api.weixin.qq.com/cgi-bin"

TITLE = "「踝关节」崴脚后怎么练？从急性扭伤到慢性不稳的三阶段康复"
SHORT_TITLE = "「踝关节」崴脚后的三阶段康复"
AUTHOR = "骨科康复小黄"
DIGEST = "J Athl Train 2002 综述：Ⅰ、Ⅱ度崴脚别长期固定，受伤当天开始练；早期活动度和力量（徒手阻力、DAPRE），中期本体感觉与平衡，后期走跑交替回到运动。附原文表格与 15 项研究汇总。"


def call(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.loads(r.read().decode("utf-8"))
    if res.get("errcode"):
        raise SystemExit(f"微信接口报错：{res}")
    return res


def upload(url, path):
    boundary = uuid.uuid4().hex
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"media\"; filename=\"{path.name}\"\r\n"
        f"Content-Type: {'image/gif' if path.suffix == '.gif' else 'image/jpeg'}\r\n\r\n"
    ).encode() + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    return call(url, body, {"Content-Type": f"multipart/form-data; boundary={boundary}"})


def prepare_content():
    html = (HERE / "article_body.html").read_text(encoding="utf-8")
    # 标签之间的换行在公众号编辑器里可能变成空段落，统一去掉
    return re.sub(r">\s*\n\s*<", "><", html)


def main():
    appid, secret = os.environ.get("WX_APPID"), os.environ.get("WX_SECRET")
    if not appid or not secret:
        sys.exit("请先设置环境变量 WX_APPID 和 WX_SECRET")
    token = call(f"{API}/token?grant_type=client_credential&appid={appid}&secret={secret}")["access_token"]

    content = prepare_content()
    for src in sorted(set(re.findall(r'src="((?:images|gifs)/[^"]+)"', content))):
        if src.endswith(".gif"):
            # 动图超过 uploadimg 的 1MB 限制，走永久图片素材（≤10MB），同样返回可用于正文的 url
            url = upload(f"{API}/material/add_material?access_token={token}&type=image", HERE / src)["url"]
        else:
            url = upload(f"{API}/media/uploadimg?access_token={token}", HERE / src)["url"]
        content = content.replace(f'src="{src}"', f'src="{url}"')
        print("正文图片已上传：", src)

    draft_id = os.environ.get("WX_DRAFT_ID")
    if draft_id:
        # 更新已有草稿：沿用原封面，只替换正文
        old = call(f"{API}/draft/get?access_token={token}", json.dumps({"media_id": draft_id}).encode())["news_item"][0]
        article = {
            "title": old["title"], "author": old["author"], "digest": old["digest"], "content": content,
            "thumb_media_id": old["thumb_media_id"], "need_open_comment": 1, "only_fans_can_comment": 0,
        }
        call(f"{API}/draft/update?access_token={token}",
             json.dumps({"media_id": draft_id, "index": 0, "articles": article}, ensure_ascii=False).encode("utf-8"),
             {"Content-Type": "application/json; charset=utf-8"})
        print("草稿已更新：", draft_id)
        return

    thumb = upload(f"{API}/material/add_material?access_token={token}&type=image", HERE / "images" / "cover.jpg")
    print("封面已上传")

    for title in (TITLE, SHORT_TITLE):
        article = {
            "title": title, "author": AUTHOR, "digest": DIGEST, "content": content,
            "thumb_media_id": thumb["media_id"], "need_open_comment": 1, "only_fans_can_comment": 0,
        }
        req = urllib.request.Request(f"{API}/draft/add?access_token={token}",
                                     json.dumps({"articles": [article]}, ensure_ascii=False).encode("utf-8"),
                                     {"Content-Type": "application/json; charset=utf-8"})
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.loads(r.read().decode("utf-8"))
        if res.get("errcode") == 45003 and title != SHORT_TITLE:
            print("标题超长，改用短标题重试")
            continue
        if res.get("errcode"):
            raise SystemExit(f"创建草稿失败：{res}")
        print("草稿创建成功，标题：", title)
        print("media_id：", res["media_id"])
        return


if __name__ == "__main__":
    main()
