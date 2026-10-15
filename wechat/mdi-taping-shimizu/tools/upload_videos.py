#!/usr/bin/env python3
"""把 videos/ 下的视频上传到公众号永久素材库（素材管理 → 视频），供编辑器里一键插入正文。

用法：WX_APPID=... WX_SECRET=... python3 tools/upload_videos.py
说明：草稿接口不能直接在正文里放视频，所以视频走永久素材；正文里另有同内容的 GIF 动图。
"""
import json
import os
import pathlib
import sys
import urllib.request
import uuid

HERE = pathlib.Path(__file__).resolve().parent.parent
API = "https://api.weixin.qq.com/cgi-bin"
VIDEOS = [
    ("video1.mp4", "视频1：8 字贴扎前后主动肩前屈对比", "未贴扎时主动前屈约 95° 即有半脱位感；8 字贴扎后立即提高到 140°（Shimizu 2026 IJSPT 病例报告附件）"),
    ("video2.mp4", "视频2：干预 5 个月后的主动活动度", "矢状面前屈、冠状面前屈和外展均接近全范围（Shimizu 2026 IJSPT 病例报告附件）"),
]


def main():
    appid, secret = os.environ.get("WX_APPID"), os.environ.get("WX_SECRET")
    if not appid or not secret:
        sys.exit("请先设置环境变量 WX_APPID 和 WX_SECRET")
    with urllib.request.urlopen(f"{API}/token?grant_type=client_credential&appid={appid}&secret={secret}", timeout=60) as r:
        res = json.loads(r.read())
    if "access_token" not in res:
        sys.exit(f"获取 token 失败：{res}")
    token = res["access_token"]
    for name, title, intro in VIDEOS:
        b = uuid.uuid4().hex
        desc = json.dumps({"title": title, "introduction": intro}, ensure_ascii=False)
        body = (
            f"--{b}\r\nContent-Disposition: form-data; name=\"media\"; filename=\"{name}\"\r\nContent-Type: video/mp4\r\n\r\n".encode()
            + (HERE / "videos" / name).read_bytes()
            + f"\r\n--{b}\r\nContent-Disposition: form-data; name=\"description\"\r\n\r\n".encode()
            + desc.encode("utf-8") + f"\r\n--{b}--\r\n".encode()
        )
        req = urllib.request.Request(f"{API}/material/add_material?access_token={token}&type=video", body,
                                     {"Content-Type": f"multipart/form-data; boundary={b}"})
        with urllib.request.urlopen(req, timeout=300) as r:
            res = json.loads(r.read())
        if res.get("errcode"):
            sys.exit(f"上传失败：{res}")
        print("视频已上传到素材库：", title, res.get("media_id"))


if __name__ == "__main__":
    main()
