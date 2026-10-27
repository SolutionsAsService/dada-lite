#!/usr/bin/env python3
"""Measure before anyone critiques: the checks that found most real defects.

    python audit.py --base http://localhost:8000 --pages index,contact
    python audit.py --base https://example.com --pages index --widths 1280,390,320

Per page and width it reports:
  overflow  page wider than the viewport, and the widest offending elements
  contrast  every visible text node against its nearest opaque background
            (WCAG: 4.5:1, or 3:1 for 24px+ / 18.66px+ bold)
  photo     text over an image (an image overlaps it above its nearest opaque
            background): worst-case contrast against the rendered pixels behind
            the glyph box, with the text hidden (5th/95th-percentile pixel)
  targets   links and buttons under --target px (default 24, WCAG 2.2 AA) that are not
            inline in a sentence; hidden inputs with a label are skipped
  alt       <img> without an alt attribute

A clean run prints "0" for every check. Test the auditor once per project by
breaking something on purpose and seeing it fail; a check that cannot fail
proves nothing.

Needs: pip install playwright pillow (and a Chrome or `playwright install chromium`).
"""
import argparse
import asyncio
import io

from PIL import Image
from playwright.async_api import async_playwright

JS = r"""
(MIN) => {
  const parse = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(Number); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const W = innerWidth;
  const out = {overflow: [], contrast: [], photo: [], targets: [], alt: []};

  const bgOf = el => { for (let e = el; e; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage !== 'none' && /url\(/.test(cs.backgroundImage)) return {photo: true};
      const c = parse(cs.backgroundColor); if (c && c.a > 0.9) return {color: c}; }
    return {color: {r: 255, g: 255, b: 255, a: 1}}; };
  const solidAncestor = el => { for (let e = el; e; e = e.parentElement) {
      const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0.9) return e; } return document.documentElement; };
  // Text is "over a photo" only when an image overlaps it and sits above the nearest opaque background
  // (that background's element contains the image). A button with its own fill is judged on its fill.
  const overImg = el => { const r = el.getBoundingClientRect(), solid = solidAncestor(el);
    return [...document.images].some(i => { const q = i.getBoundingClientRect();
      return q.width > 40 && r.left < q.right && r.right > q.left && r.top < q.bottom && r.bottom > q.top &&
             !i.contains(el) && solid.contains(i) && getComputedStyle(i).visibility !== 'hidden'; }); };

  if (document.documentElement.scrollWidth > W)
    out.overflow = [...document.querySelectorAll('body *')]
      .filter(e => e.getBoundingClientRect().right > W + 0.5)
      .slice(0, 5).map(e => `${e.tagName.toLowerCase()}.${e.className} right=${Math.round(e.getBoundingClientRect().right)}`);

  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = walker.currentNode, el = t.parentElement, txt = t.textContent.trim();
    if (!txt || !el || el.closest('svg,script,style,.sr-only,[aria-hidden="true"]')) continue;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    if (!r.width || !r.height || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
    const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
    const need = (size >= 24 || (size >= 18.66 && bold)) ? 3 : 4.5;
    const key = el.tagName + txt.slice(0, 30); if (seen.has(key)) continue; seen.add(key);
    const bg = bgOf(el);
    if (bg.photo || overImg(el)) { el.dataset.auditPhoto = need; out.photo.push(null); continue; }
    const v = ratio(parse(cs.color), bg.color);
    if (v < need) out.contrast.push(`${v.toFixed(2)} < ${need}  ${size}px "${txt.slice(0, 40)}"`);
  }
  out.photo = [];

  document.querySelectorAll('a[href], button, [role=button], input, select, textarea').forEach(e => {
    const r = e.getBoundingClientRect(); if (!r.width || !r.height) return;
    const cs = getComputedStyle(e);
    const inline = cs.display === 'inline' && e.closest('p, li') && e.closest('p, li').textContent.trim().length > e.textContent.trim().length + 10;
    const hiddenInput = e.matches('input') && (+cs.opacity === 0 || r.width <= 2) && e.labels && e.labels.length;
    if ((r.width < MIN || r.height < MIN) && !inline && !hiddenInput && !e.matches('.skip, .sr-only'))
      out.targets.push(`${e.tagName.toLowerCase()} ${Math.round(r.width)}x${Math.round(r.height)} "${(e.textContent || e.value || '').trim().slice(0, 30)}"`);
  });
  document.querySelectorAll('img:not([alt])').forEach(i => out.alt.push(i.currentSrc.split('/').pop()));
  return out;
}
"""

PHOTO_BOXES = """() => [...document.querySelectorAll('[data-audit-photo]')].map(e => {
  const rg = document.createRange(); rg.selectNodeContents(e);
  const r = rg.getBoundingClientRect(), c = getComputedStyle(e).color.match(/\\d+/g).map(Number);
  return {x: r.x, y: r.y + scrollY, w: r.width, h: r.height, need: +e.dataset.auditPhoto, color: c,
          text: e.textContent.trim().slice(0, 40)}; })"""


def lum(c):
    c = [x / 255 for x in c[:3]]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


async def launch(p):
    try:
        return await p.chromium.launch(channel="chrome")
    except Exception:
        return await p.chromium.launch()


async def main(a):
    total = 0
    async with async_playwright() as p:
        browser = await launch(p)
        for w in [int(x) for x in a.widths.split(",")]:
            page = await browser.new_page(viewport={"width": w, "height": 844 if w < 700 else 900})
            for name in a.pages.split(","):
                url = f"{a.base.rstrip('/')}/{name}" + ("" if "." in name or a.clean else ".html")
                await page.goto(url, wait_until="networkidle")
                await page.add_style_tag(content="html{scroll-behavior:auto!important}*{transition:none!important;animation:none!important}")
                await page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
                res = await page.evaluate(JS, a.target)
                boxes = await page.evaluate(PHOTO_BOXES)
                if boxes:
                    await page.add_style_tag(content="[data-audit-photo]{color:transparent!important;text-shadow:none!important}")
                    shot = Image.open(io.BytesIO(await page.screenshot(full_page=True))).convert("RGB")
                    for b in boxes:
                        crop = shot.crop((int(b["x"]), int(b["y"]), int(b["x"] + b["w"]), int(b["y"] + b["h"])))
                        ls = sorted(lum(px) for px in crop.getdata()) or [0]
                        fg = lum(b["color"])
                        worst = min(ls[int(len(ls) * 0.05)], ls[int(len(ls) * 0.95) - 1], key=lambda g: (max(fg, g) + 0.05) / (min(fg, g) + 0.05))
                        v = (max(fg, worst) + 0.05) / (min(fg, worst) + 0.05)
                        if v < b["need"]:
                            res["photo"].append(f'{v:.2f} < {b["need"]}  "{b["text"]}"')
                n = sum(len(v) for v in res.values())
                total += n
                print(f"{name} @{w}: " + "  ".join(f"{k} {len(v)}" for k, v in res.items()))
                for k, v in res.items():
                    for line in v[: a.show]:
                        print(f"    {k}: {line}")
            await page.close()
        await browser.close()
    print(f"TOTAL {total}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--pages", default="index")
    ap.add_argument("--widths", default="1280,390")
    ap.add_argument("--show", type=int, default=6, help="max lines shown per check")
    ap.add_argument("--target", type=int, default=24, help="minimum target size in px (WCAG 2.2 AA is 24; 44 is the touch guideline)")
    ap.add_argument("--clean", action="store_true", help="pages have clean URLs (no .html)")
    asyncio.run(main(ap.parse_args()))
