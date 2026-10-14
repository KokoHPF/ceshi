#!/usr/bin/env python3
"""把 article_body.html 上传到公众号草稿箱（只进草稿箱，不会群发）。

用法：
    export WX_APPID=你的AppID WX_SECRET=你的AppSecret
    python3 build.py && python3 upload_draft.py

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

TITLE = "「腰椎间盘」运动员腰椎间盘突出症分期康复方案：从麦肯基力学伸展到动力链功能进阶"
SHORT_TITLE = "「腰椎间盘」运动员腰椎间盘突出症分期康复方案"
AUTHOR = "悦美力"
DIGEST = "IJSPT 2013 临床评论精读：按椎间盘愈合时钟排布的四阶段康复——麦肯基伸展、抗旋转、动态旋转与回归运动，附各阶段练习库。"


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
        "Content-Type: image/jpeg\r\n\r\n"
    ).encode() + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    return call(url, body, {"Content-Type": f"multipart/form-data; boundary={boundary}"})


def prepare_content():
    html = (HERE / "article_body.html").read_text(encoding="utf-8")
    # 去掉“使用说明”框、正文里的大标题和署名行（标题和作者在草稿字段里填写）
    html = re.sub(r"<!-- 使用说明：发布前删除本框 -->\s*<section[^>]*>.*?</section>\s*", "", html, count=1, flags=re.S)
    html = re.sub(r"<h1[^>]*>.*?</h1>\s*", "", html, count=1, flags=re.S)
    html = re.sub(r'<p style="font-size:13px; color:rgb\(136,136,136\); margin:0 0 24px; font-style:italic;">原创.*?</p>\s*', "", html, count=1, flags=re.S)
    html = html.replace("欢迎关注公众号，", "欢迎关注悦美力公众号，")
    assert "使用说明" not in html and "<h1" not in html
    return html


def main():
    appid, secret = os.environ.get("WX_APPID"), os.environ.get("WX_SECRET")
    if not appid or not secret:
        sys.exit("请先设置环境变量 WX_APPID 和 WX_SECRET")
    token = call(f"{API}/token?grant_type=client_credential&appid={appid}&secret={secret}")["access_token"]

    content = prepare_content()
    for src in sorted(set(re.findall(r'src="(images/[^"]+)"', content))):
        url = upload(f"{API}/media/uploadimg?access_token={token}", HERE / src)["url"]
        content = content.replace(f'src="{src}"', f'src="{url}"')
        print("正文图片已上传：", src)

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
