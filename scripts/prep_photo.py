#!/usr/bin/env python3
"""
Prepares a portrait photo for monochrome ASCII art generation:
1. Removes background using rembg (silueta model) to isolate subject.
2. Applies CLAHE (Contrast-Limited Adaptive Histogram Equalization) and bilateral filtering for edge clarity.
3. Contrast-stretches luminance over subject pixels.
4. Composites onto pure white (luminance 255 -> ASCII space glyph).
5. Centers and crops into a square image.
"""

import sys
import os
from PIL import Image
import numpy as np
import rembg
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.join(HERE, "..", "source-photo.jpg")
DEFAULT_OUT = os.path.join(HERE, "..", "source-prepped.png")

SRC = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
OUT = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT

if not os.path.exists(SRC):
    print(f"Error: Source image not found at {SRC}")
    sys.exit(1)

print(f"Processing {SRC}...")
im = Image.open(SRC).convert("RGB")

print("Removing background with rembg (silueta)...")
session = rembg.new_session("silueta")
nobg = rembg.remove(im, session=session)

arr = np.array(nobg)
rgb, alpha = arr[:, :, :3], arr[:, :, 3]
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

print("Enhancing edge contrast (CLAHE + Bilateral filter)...")
clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
cl = clahe.apply(gray)
smooth = cv2.bilateralFilter(cl, 7, 35, 7)

subj_pixels = smooth[alpha > 120]
if len(subj_pixels) > 0:
    lo, hi = np.percentile(subj_pixels, [3, 95])
    tone = np.clip((smooth.astype(np.float32) - lo) / max(hi - lo, 1), 0, 1)
else:
    tone = smooth.astype(np.float32) / 255.0

mask = (alpha.astype(np.float32) / 255.0)
out = tone * 255.0 * mask + 255.0 * (1.0 - mask)
out = out.astype(np.uint8)

ys, xs = np.where(alpha > 30)
if len(ys) > 0:
    cy = int(np.mean(ys) * 0.92)
    cx = int(np.mean(xs))
    side = int(max(xs.max() - xs.min(), ys.max() - ys.min()))

    canvas = np.full((side, side), 255, np.uint8)
    x0, y0 = cx - side // 2, cy - side // 2

    src_x0 = max(0, x0)
    src_y0 = max(0, y0)
    src_x1 = min(out.shape[1], x0 + side)
    src_y1 = min(out.shape[0], y0 + side)

    dst_x0 = src_x0 - x0
    dst_y0 = src_y0 - y0
    dst_x1 = dst_x0 + (src_x1 - src_x0)
    dst_y1 = dst_y0 + (src_y1 - src_y0)

    canvas[dst_y0:dst_y1, dst_x0:dst_x1] = out[src_y0:src_y1, src_x0:src_x1]
    final_img = Image.fromarray(canvas)
else:
    final_img = Image.fromarray(out)

final_img.save(OUT)
print(f"Successfully saved {OUT} ({final_img.size[0]}x{final_img.size[1]})")
