#!/usr/bin/env bash
# 下载思源黑体（Noto Sans SC）四个字重到 ../fonts/。GitHub 直链不通时走 jsDelivr 镜像。
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)/fonts"; mkdir -p "$DIR"
for w in Regular Medium Bold Black; do
  f="$DIR/NotoSansSC-$w.otf"
  [ -s "$f" ] && [ "$(wc -c <"$f")" -gt 1000000 ] && continue
  for base in "https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/SubsetOTF/SC" "https://github.com/notofonts/noto-cjk/raw/main/Sans/SubsetOTF/SC"; do
    curl -fsSL -m 300 -o "$f" "$base/NotoSansSC-$w.otf" && [ "$(wc -c <"$f")" -gt 1000000 ] && break
  done
  echo "$w: $(wc -c <"$f") bytes"
done
