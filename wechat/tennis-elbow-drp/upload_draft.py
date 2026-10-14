#!/usr/bin/env python3
"""把 article_body.html 上传到公众号草稿箱（只进草稿箱，不会群发）。

用法：
    export WX_APPID=你的AppID WX_SECRET=你的AppSecret
    python3 build.py && python3 upload_draft.py

前提：运行本脚本的机器出口 IP 已加入公众号后台
「设置与开发 → 基本配置 → IP 白名单」。
"""
import json
import mimetypes
import os
import pathlib
import sys
import urllib.request
import uuid

HERE = pathlib.Path(__file__).parent
API = "https://api.weixin.qq.com/cgi-bin"

TITLE = "「网球肘」从肩胛到手腕：一套分期进阶的肱骨外上髁肌腱病综合康复方案"
SHORT_TITLE = "「网球肘」从肩胛到手腕：肱骨外上髁肌腱病综合康复方案"
AUTHOR = "悦美力"
DIGEST = "IJSPT 2019 临床评论精读：热身、肩胛与腕肘三阶段强化、MWM 松动、教育与辅助手段，附完整进阶标准和剂量。"


def call(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.loads(r.read().decode("utf-8"))
    if res.get("errcode"):
        raise SystemExit(f"微信接口报错：{res}")
    return res


def upload(url, path):
    boundary = uuid.uuid4().hex
    ctype = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"media\"; filename=\"{path.name}\"\r\n"
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode() + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    return call(url, body, {"Content-Type": f"multipart/form-data; boundary={boundary}"})


def main():
    appid, secret = os.environ.get("WX_APPID"), os.environ.get("WX_SECRET")
    if not appid or not secret:
        sys.exit("请先设置环境变量 WX_APPID 和 WX_SECRET")
    token = call(f"{API}/token?grant_type=client_credential&appid={appid}&secret={secret}")["access_token"]

    content = (HERE / "article_body.html").read_text(encoding="utf-8")
    for f in sorted((HERE / "images").glob("img*.jpg")):
        key = f"__{f.stem.upper()}__"
        if key in content:
            url = upload(f"{API}/media/uploadimg?access_token={token}", f)["url"]
            content = content.replace(key, url)
            print("正文图片已上传：", f.name)

    thumb = upload(f"{API}/material/add_material?access_token={token}&type=image", HERE / "images" / "cover.jpg")
    print("封面已上传：", thumb["media_id"])

    for title in (TITLE, SHORT_TITLE):
        article = {
            "title": title,
            "author": AUTHOR,
            "digest": DIGEST,
            "content": content,
            "thumb_media_id": thumb["media_id"],
            "need_open_comment": 1,
            "only_fans_can_comment": 0,
        }
        data = json.dumps({"articles": [article]}, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(f"{API}/draft/add?access_token={token}", data,
                                     {"Content-Type": "application/json; charset=utf-8"})
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.loads(r.read().decode("utf-8"))
        if res.get("errcode") == 45003 and title != SHORT_TITLE:
            print("标题超长，改用短标题重试")
            continue
        if res.get("errcode"):
            raise SystemExit(f"创建草稿失败：{res}")
        print("草稿创建成功，media_id：", res["media_id"])
        return


if __name__ == "__main__":
    main()
