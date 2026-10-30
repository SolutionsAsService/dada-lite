# Carry-forward: facts about the web medium, each measured in a real run

Read before building. Each line names the trap, the measurement that proved it, and the lever that worked.

## Layout and CSS
- **`clip-path` cuts away outlines and box-shadows.** A focus ring outside a clipped button is invisible (computed `outline-style: solid`, nothing on screen). Draw the ring inside: `outline-offset: -7px; outline-color: currentColor`.
- **A more specific "ring colour on this field" rule repaints rings on elements with their own fill**, e.g. an ink ring on an ink button. Exclude buttons with `:not(.btn)`.
- **`backdrop-filter`, `filter` or `transform` on a fixed header** makes it the containing block for its fixed children, so a full-screen mobile menu collapses to the header's height. Put the blur on `::before`.
- **An inline `style="grid-template-columns:…"` beats every media query**, so the layout never reflows (page 537px at 390). Use a class.
- **`1fr` has an automatic minimum.** A card containing a `nowrap` URL refused to shrink (323px at 320). Use `minmax(0, 1fr)` and `min-width: 0` on flex children.
- **A `display: grid` list item turns loose text and an inline `<code>` into separate grid items**, so the code drops to its own row and `&nbsp;` is inert. Wrap the value in one element.
- **`img { height: 100% }` in a grid row pushes the caption outside its figure** and under the next item. Use `align-items: start` and natural image height.
- **Visually hidden inputs** (`position: absolute; opacity: 0`) with no positioned parent widened a page to 1344px at 1280. Give the row `position: relative`.
- **Absolutely positioned sr-only spans inside a horizontal scroller escape its scroll box** (page 2123px at 390). Make each item `position: relative`.
- **`a[href^="tel:"]` has specificity 0,1,1 and beats a later `.class`.** A broad `nowrap` on phone links froze a label inside the link (451px at 390); `.x { white-space: normal }` was inert, `a.x` worked.

## Colour and contrast
- **Contrast over a photo can't be read from CSS.** Measure it from pixels with the text hidden (`audit.py` does this). A light scrim measured 1.7–4.7:1 under a hero headline; a directional scrim (dense where text sits) measured 5.2–14.5:1.
- **Mid-saturation brand oranges and coppers** (#D76A3C, #D98A4E) take ink text at 5–6:1 but give only 3.0–3.5:1 with white or cream. Use ink on the brand colour, and a darker shade of it for small text on light grounds.

## Capturing for critics
- **Smooth scrolling ruins full-page shots.** With `html { scroll-behavior: smooth }`, the scroll back to the top was still animating (`scrollY = 39`), so a sticky header was painted part-way down and five critics reported a collision that did not exist. Force `scroll-behavior: auto` before scrolling (`capture.py` does).
- **Fixed bars appear once, mid-page, in a stitched full-page shot.** Judge them from the first-screen shot and say so in the brief.
- **Lazy images don't load in a full-page shot** unless the page is walked first and the shot waits for `img.complete`.

## Content honesty
- No invented testimonials, stats, years in business, prices, licences or response times. Use plainly marked placeholders ("licence: add number") and a fictional 555-01xx phone number until the owner supplies real ones.
- A claim you wrote yourself (e.g. "we reply within one business day") is still a claim. Remove it unless the owner can stand behind it.

## Measured in later runs (2026-10-29)
- **`display: block` on a class beats the browser's `[hidden] { display: none }`**, so `hidden` error messages showed on a pristine form and after a valid submit. Add `[hidden] { display: none !important; }`, and assert hidden state after every interaction, not only the success state.
- **Google Fonts' woff2 files did not appear in Resource Timing**, so a page measuring its own weight undercounted by 120 KB (27.7 → 150.8 KB once self-hosted). Self-host fonts on any page that reports its own size.
- **Google Apps Script web apps send no CORS headers**, so `fetch(..., { mode: "no-cors" })` resolves whatever happened on the server. Say "sent", never "confirmed", and keep the fields on a network error.
- **A leading space inside a span in an `inline-flex` link collapses** ("Call(760)…"). Use `gap` on the link.
- **An upright phone version of a horizontal rail** needs an explicit track height (a track of only absolute children collapses to 0 px) and one shared `transform` for every stop (a different one on the last stop overlapped its neighbour).
- **`<p>` with a global `max-width: 62ch` inside a full-width rail** stopped scale labels mid-rail. Put scale labels inside the track, positioned at its ends.
- **Next.js 16 static export writes nested prefetch files as `__next.<route>/__PAGE__.txt`** while the client asks for `__next.<route>.__PAGE__.txt`; every client-side prefetch 404s on a static host until a flat copy is written.
- **Times for a place come from the place.** A sky for Southern California computed with the visitor's clock was wrong for visitors in other time zones; compute in `America/Los_Angeles` with `Intl`.
- **Moon phase epoch:** the reference new moon 2000-01-06 18:14 UTC is day 10962.76 after the Unix epoch (not 10957.26, which is 2000-01-01).
- **Cold-tab timings from a local Python server** read 1.6–6.5 s for DOMContentLoaded against 36–100 ms warm; treat them as instrument noise.
