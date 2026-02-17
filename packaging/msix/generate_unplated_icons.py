"""
Generate all MSIX icon assets from icon.png.

Usage:
    python packaging/msix/generate_unplated_icons.py

This script reads the project's icon.png file and generates all required
PNG assets for MSIX packaging, including:
  - Square44x44Logo  (scale + targetsize + unplated variants)
  - Square71x71Logo  (scale variants)
  - Square150x150Logo (scale variants)
  - Square310x310Logo (scale variants)
  - Wide310x150Logo  (scale variants, icon centered on wide canvas)
  - StoreLogo        (scale variants)
"""

from PIL import Image
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "icon.png")
OUT_DIR = os.path.join(SCRIPT_DIR, "Assets")

PREFIX = "RDPHEARTBEAT"
SCALES = [100, 125, 150, 200, 400]

# ── Square logos: (name, base_width, base_height) ──────────────────────
SQUARE_LOGOS = [
    (f"{PREFIX}-Square44x44Logo",  44,  44),
    (f"{PREFIX}-Square71x71Logo",  71,  71),
    (f"{PREFIX}-Square150x150Logo", 150, 150),
    (f"{PREFIX}-Square310x310Logo", 310, 310),
    (f"{PREFIX}-Wide310x150Logo",  310, 150),
    ("StoreLogo",                   50,  50),
]

# ── Target-size variants (Square44x44Logo only) ───────────────────────
TARGET_SIZES = [16, 24, 32, 44, 48, 256]


def resize_square(src: Image.Image, size: int) -> Image.Image:
    """Resize source image to a square of the given size."""
    return src.resize((size, size), Image.LANCZOS)


def resize_wide(src: Image.Image, w: int, h: int) -> Image.Image:
    """Place source image centered on a wide canvas (w×h).

    The icon is scaled to fit the canvas height, then centered horizontally.
    """
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    icon = src.resize((h, h), Image.LANCZOS)
    x_offset = (w - h) // 2
    canvas.paste(icon, (x_offset, 0), icon)
    return canvas


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    src = Image.open(SRC_PATH).convert("RGBA")
    count = 0

    # ── Scale variants for all logo types ──────────────────────────────
    for name, base_w, base_h in SQUARE_LOGOS:
        for scale in SCALES:
            w = base_w * scale // 100
            h = base_h * scale // 100

            if base_w != base_h:  # wide logo
                img = resize_wide(src, w, h)
            else:
                img = resize_square(src, w)

            fname = f"{name}.scale-{scale}.png"
            img.save(os.path.join(OUT_DIR, fname), "PNG")
            print(f"Created: {fname} ({w}x{h})")
            count += 1

    # ── Target-size variants (Square44x44Logo) ─────────────────────────
    target_prefix = f"{PREFIX}-Square44x44Logo"
    target_variants = ["", "altform-unplated", "altform-lightunplated"]

    for sz in TARGET_SIZES:
        resized = resize_square(src, sz)
        for variant in target_variants:
            if variant:
                fname = f"{target_prefix}.targetsize-{sz}_{variant}.png"
            else:
                fname = f"{target_prefix}.targetsize-{sz}.png"
            resized.save(os.path.join(OUT_DIR, fname), "PNG")
            print(f"Created: {fname} ({sz}x{sz})")
            count += 1

    print(f"\nDone! {count} files generated in {OUT_DIR}")


if __name__ == "__main__":
    main()
