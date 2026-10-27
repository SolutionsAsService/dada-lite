#!/usr/bin/env python3
"""Capture what a critic needs to see, cheaply: first screens plus full pages.

    python capture.py --base http://localhost:8000 --pages index,services --out shots/r1
    python capture.py --base https://example.com --pages index --widths 1280,390

For each page and width it writes <out>-<page>-<width>.jpg (full page) and
<out>-<page>-<width>-top.jpg (first screen only). Hand critics the -top shots
first; they cover most findings for a fraction of the image tokens.

Two capture traps it avoids (each cost a round to learn):
- Smooth scrolling. With `html { scroll-behavior: smooth }` every scrollTo
  animates, so a full-page shot taken after scrolling catches the page mid-
  scroll and paints sticky headers part-way down. Smooth scrolling is forced
  off before anything scrolls.
- Lazy images. They load only near the viewport, so the page is walked from
  top to bottom and the shot waits until every image is complete.

Fixed bars (call bars, cookie banners) still appear once, mid-page, in a
stitched full-page shot. Tell critics so, or judge them from the -top shot.

Needs: pip install playwright pillow, and either `playwright install chromium`
or a local Chrome (used automatically through channel="chrome").
"""
import argparse
import asyncio
import io

from PIL import Image
from playwright.async_api import async_playwright

WALK = """async () => {
  for (let y = 0; y < document.body.scrollHeight; y += 400) {
    scrollTo(0, y); await new Promise(r => setTimeout(r, 120));
  }
  scrollTo(0, 0);
}"""


async def launch(p):
    try:
        return await p.chromium.launch(channel="chrome")
    except Exception:
        return await p.chromium.launch()


async def main(a):
    widths = [int(w) for w in a.widths.split(",")]
    async with async_playwright() as p:
        browser = await launch(p)
        for w in widths:
            h = 844 if w < 700 else 900
            ctx = await browser.new_context(viewport={"width": w, "height": h})
            page = await ctx.new_page()
            for name in a.pages.split(","):
                url = f"{a.base.rstrip('/')}/{name}" + ("" if "." in name or a.clean else ".html")
                await page.goto(url, wait_until="networkidle")
                await page.add_style_tag(content="html{scroll-behavior:auto!important}")
                await page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                await page.evaluate(WALK)
                await page.wait_for_function("[...document.images].every(i => i.complete)")
                await page.wait_for_timeout(800)
                full = Image.open(io.BytesIO(await page.screenshot(full_page=True))).convert("RGB")
                stem = f"{a.out}-{name.split('.')[0]}-{w}"
                full.save(stem + ".jpg", quality=70)
                full.crop((0, 0, w, min(full.height, h))).save(stem + "-top.jpg", quality=75)
                sw = await page.evaluate("document.documentElement.scrollWidth")
                print(f"{stem}.jpg  {full.width}x{full.height}  scrollWidth={sw}" + ("  OVERFLOW" if sw > w else ""))
            await ctx.close()
        await browser.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="site root, e.g. http://localhost:8000")
    ap.add_argument("--pages", default="index", help="comma list of page names")
    ap.add_argument("--widths", default="1280,390")
    ap.add_argument("--out", default="shots/r", help="output path prefix")
    ap.add_argument("--clean", action="store_true", help="pages have clean URLs (no .html)")
    asyncio.run(main(ap.parse_args()))
