"""Losslessly compress the original animated hero without resizing or retiming.

Requires the same Pillow version as the contribution dashboard workflow.
Run after replacing ascii-magic-profile.gif; keep that original as the source.
Also compose the transparent signature into self-contained SVG delivery files.
"""
from pathlib import Path
from base64 import b64encode
from io import BytesIO
import sys

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "ascii-magic-profile.gif"
OUTPUT = ROOT / "assets/profile-hero.webp"


def build_signed_hero():
    """Embed the hero and signature together so GitHub needs no overlay CSS."""
    with Image.open(OUTPUT) as hero:
        width, height = hero.size
        hero.seek(hero.n_frames // 2)
        static_frame = BytesIO()
        hero.convert("RGBA").save(static_frame, format="PNG", optimize=True)

    for reduced_motion, media_type, background in [
        (False, "image/webp", OUTPUT.read_bytes()),
        (True, "image/png", static_frame.getvalue()),
    ]:
        suffix = "-static" if reduced_motion else ""
        signature = (ROOT / f"assets/signature{suffix}.svg").read_text(encoding="utf-8")
        # The top of the lettering clears the final interests row; the underline
        # stays inside the existing card border. Preserve the signature's tilt.
        signature = signature.replace(
            'width="398" height="216"',
            'x="1565" y="542" width="335" height="182"',
            1,
        )
        encoded = b64encode(background).decode("ascii")
        signed = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="hero-title">\n'
            '  <title id="hero-title">Viraj Singh Ranawat profile and signature</title>\n'
            f'  <image width="{width}" height="{height}" href="data:{media_type};base64,{encoded}" />\n'
            f'{signature}</svg>\n'
        )
        target = ROOT / f"assets/profile-hero{suffix}.svg"
        target.write_text(signed, encoding="utf-8")
        print(f"Built {target.name}: {target.stat().st_size:,} bytes")


def main():
    with Image.open(SOURCE) as source:
        durations = []
        for index in range(source.n_frames):
            source.seek(index)
            source.load()
            durations.append(source.info["duration"])
        source.seek(0)
        source.save(OUTPUT, format="WEBP", save_all=True, duration=durations,
                    loop=source.info.get("loop", 0), lossless=True,
                    method=6, minimize_size=True, exact=True)

    # Compare the decoded timelines, allowing the encoder to merge identical
    # consecutive frames. Every displayed pixel and millisecond must match.
    with Image.open(SOURCE) as source, Image.open(OUTPUT) as result:
        if source.size != result.size or source.info.get("loop") != result.info.get("loop"):
            raise AssertionError("Hero dimensions or loop behavior changed")
        source_index = result_index = 0
        source_remaining = result_remaining = 0
        elapsed = 0
        while source_index < source.n_frames or source_remaining:
            if not source_remaining:
                source.seek(source_index)
                source.load()
                source_frame = source.convert("RGBA")
                source_remaining = source.info["duration"]
                source_index += 1
            if not result_remaining:
                if result_index >= result.n_frames:
                    raise AssertionError("WebP timeline ended early")
                result.seek(result_index)
                result.load()  # WebP duration metadata is available after load.
                result_frame = result.convert("RGBA")
                result_remaining = result.info["duration"]
                result_index += 1
            if ImageChops.difference(source_frame, result_frame).getbbox(alpha_only=False):
                raise AssertionError(f"Hero pixels changed at {elapsed}ms")
            step = min(source_remaining, result_remaining)
            source_remaining -= step
            result_remaining -= step
            elapsed += step
        if result_remaining or result_index != result.n_frames:
            raise AssertionError("WebP timeline extended past the original")
    saved = 100 * (1 - OUTPUT.stat().st_size / SOURCE.stat().st_size)
    print(f"Verified every pixel and frame duration: {elapsed}ms, {source_index} original frames")
    print(f"{SOURCE.stat().st_size:,} -> {OUTPUT.stat().st_size:,} bytes ({saved:.1f}% smaller)")
    build_signed_hero()


if __name__ == "__main__":
    if sys.argv[1:] == ["--signature-only"]:
        build_signed_hero()
    else:
        main()
