# -*- coding: utf-8 -*-
"""배경이 '투명처럼 보이는 격자'로 구워진 PNG 에서 진짜 투명 배경을 만듭니다(PIL + numpy 만 씀).
   · logo : 어두운 격자 위 흰·빨간 획 → 밝기로 알파
   · photo: 흰/회색 격자 위 인물 → 격자 무늬를 먼저 알아내고(칸 크기·위상), '그 자리에 있어야 할 격자색'과 같은
            픽셀만 배경 후보로 잡아 가장자리에서 채워 들어감. 흰 모자가 흰 칸과 섞이는 건 닫힘(closing)으로 메움
   python site/work/cutout.py <원본> <결과> logo|photo"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from collections import deque

def logo(src, dst):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bright = a.max(axis=2)
    alpha = np.clip((bright - 110) / 60.0, 0, 1)
    red = (r > 120) & (r - np.maximum(g, b) > 50)
    alpha = np.where(red, 1.0, alpha)
    out = np.zeros(a.shape[:2] + (4,), np.uint8)
    out[..., 0] = np.where(red, r, 255); out[..., 1] = np.where(red, g, 255); out[..., 2] = np.where(red, b, 255)
    out[..., 3] = (alpha * 255).astype(np.uint8)
    # 오른쪽 아래 작은 얼룩(생성 흔적) 지우기
    h, w = out.shape[:2]; out[int(h*.9):, int(w*.78):, 3] = 0
    Image.fromarray(out, "RGBA").save(dst)

def photo(src, dst):
    """격자를 무늬로 알아봅니다: 회색 칸 픽셀의 비율을 두 칸 크기 창으로 평균 내면
       격자 위에서는 0.5, 흰 모자처럼 밋밋한 곳에서는 0, 둘의 경계에서는 0.25 — 그래서 0.25 를 문턱으로 자르면 경계가 맞습니다."""
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    # 격자 칸 크기: 맨 위 줄의 밝기 변화 간격
    b = a[8, :, 0] > 220; fl = np.where(b[1:] != b[:-1])[0] + 1
    cell = float(np.median(np.diff(fl)))
    val = a.mean(axis=2)
    neutral = (a.max(axis=2) - a.min(axis=2)) < 14
    light = neutral & (val > 165)
    # 격자는 칸마다 날카로운 경계선이 있고(30px 마다), 모자의 그늘은 부드럽게 변합니다.
    # 날카로운 경계 픽셀의 밀도를 두 칸 창으로 재면 격자 위 ≈ 0.13, 모자 안 ≈ 0, 그 경계에서 절반
    gx = np.abs(np.diff(val, axis=1, prepend=val[:, :1])); gy = np.abs(np.diff(val, axis=0, prepend=val[:1, :]))
    edge = ((gx > 22) | (gy > 22)).astype(np.uint8) * 255
    dens = np.asarray(Image.fromarray(edge, "L").filter(ImageFilter.BoxBlur(cell))).astype(np.float32) / 255
    isbg = light & (dens > 0.06)
    m = int(cell * 1.5)                                   # 테두리 근처는 창이 잘려 밀도가 낮게 나오니 그냥 배경으로
    border = np.zeros((h, w), bool); border[:m, :] = border[-m:, :] = True; border[:, :m] = border[:, -m:] = True
    isbg |= light & border
    # 가장자리에서 이어진 배경만(옷 안의 밝은 점은 안 지워지게)
    seen = np.zeros((h, w), bool); q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if isbg[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if isbg[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
            if 0 <= ny < h and 0 <= nx < w and isbg[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; q.append((ny, nx))
    fgm = ~seen
    # 인물과 안 이어진 조각(원본에 남은 얼룩)은 버립니다 — 가운데 픽셀에서 이어진 덩어리만
    keep = np.zeros((h, w), bool); q = deque([(h//2, w//2)]); keep[h//2, w//2] = True
    while q:
        y, x = q.popleft()
        for ny, nx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
            if 0 <= ny < h and 0 <= nx < w and fgm[ny, nx] and not keep[ny, nx]:
                keep[ny, nx] = True; q.append((ny, nx))
    fg = Image.fromarray(np.where(keep, 255, 0).astype(np.uint8), "L")
    # 흰 모자에 흰 칸이 계단처럼 붙어 남습니다 → 한 칸보다 좁은 돌기를 깎는 열림(opening)
    k = int(cell * 1.6) | 1
    fg = fg.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))
    fg = fg.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(7))     # 작은 구멍 메움
    fg = fg.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.4))   # 가장자리 남은 테 2px 안으로
    out = im.copy(); out.putalpha(fg)
    bbox = fg.getbbox()
    if bbox: out = out.crop((max(0, bbox[0]-6), max(0, bbox[1]-6), min(w, bbox[2]+6), min(h, bbox[3]+6)))
    out.save(dst)
    print("cell %.1f px" % cell)

if __name__ == "__main__":
    src, dst, kind = sys.argv[1:4]
    (logo if kind == "logo" else photo)(src, dst)
    print(dst, Image.open(dst).size)
