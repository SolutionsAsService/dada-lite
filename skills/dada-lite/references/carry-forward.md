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
