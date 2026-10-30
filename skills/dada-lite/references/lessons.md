# Lessons from runs: how to run DADA-Lite well

Process lessons, each from a real run (2026-10-29: Loadbearing, A-Z's Mobile Detailing, Divine Transport Group, Waves Window Washing, Stargazer Spas). Facts about the web medium itself live in [carry-forward.md](carry-forward.md).

## Lite is usually enough
- **Two full runs (premortem panel, branch round, three whole rounds, eight seats each) ended with every seat passing from round 2 on.** Rounds 2 and 3 produced only optional notes. Three lite runs (one sub-agent seating five or six critics, one round, inline fixes) caught the same classes of defect: invented claims, overlapping fixed bars, unhonest captions, tiny mobile labels, focus and target gaps. Default to lite; add a second round only when round 1 changes structure.
- **One sub-agent can seat several critics** if the prompt asks for separate verdicts that don't react to each other, each under ~90 words with anchor, observed, verdict, requested change and Andon. Keep the whole prompt under ~350 words and put the facts in a file.

## Evidence before panel
- **Write the evidence file, then check it exists before launching the panel.** A chained shell command failed at an assertion, the evidence file was never written, and the panel judged screenshots taken before the bold move. Two of its objections were about a hero that no longer existed.
- **Re-capture after every structural move.** Screenshots go stale silently; name the capture time in the brief.
- **Put only sourced facts in a seat prompt.** A conductor typed an unsourced detail about an owner into one prompt; it had to be retracted mid-run. Point seats at the evidence file instead of describing the business from memory.

## Real businesses: truth is move one
- **On a real client's site, the premortem's strongest finding was always dishonesty, not style:** a rating counted a placeholder review, AI-generated photos sat under "real cars, real customers", a watermarked logo, invented stats ("500+ happy clients"), promises the owner never made ("we redo it before we leave"). Five of eight seats pulled the Andon on one site. Make removing these M1, and keep a list of what the owner must supply.
- **Separate the owner's claims from yours.** Wording the owner published (licensed and insured, same-week service) can stay; wording a previous designer or you invented comes out.
- **Ask what is real before using media.** Real job photos had names like `real-*.jpg`; the rest (smiling models, studio portraits, a van composite) looked stock or generated. Use only what you can tie to the business.

## Bold moves that held up
- **Put the concept onto real evidence.** The strongest breakers all did this: a real job photo as the hero with the tagline reflected in its paint; the clean-pass haze wiping a real client's window; a home page that load-tests itself in the visitor's browser; tonight's real sky computed for the visitor's time. A drawn or staged version of the same idea drew Debord and Cairo objections every time.
- **Verify every computed claim against a known fact.** Polaris altitude equals the latitude (33.1° at 33°N). Moon phase: 100% at a known full moon, 0% at a known new moon (this caught a 5.5-day epoch error). Page weight: recompute from file sizes. Webhook payload: compare byte-for-byte with the old site's.
- **A computed caption must not over-claim.** "The 15 brightest stars" was false for a hand-picked list; "15 bright stars from our 29-star chart" is true. Approximate figures say "about".
- **Strangeness on the home page, recognition inside.** Every panel accepted a striking home hero with plain, navigable inner pages; none accepted strangeness that slowed booking.

## Branching is cheap and decisive
- **Two hero spikes judged by three seats with a Pugh row** settled direction in one round; all three picked a merge of both. A spike is the hero plus one section, rendered at 1440 and 390.

## Forms and live endpoints
- **Never let a generic test script touch a real form.** A form test written for one site nearly ran against another site's live CRM form; it only failed because a selector didn't match. Disable shared form tests by default; write a per-site test that intercepts the endpoint (`page.route`) and stubs `navigator.sendBeacon`.
- **Test both paths:** success (payload exact, message, focus) and failure (fields kept, call/text offered).

## Deploy shape
- **A static site's repo root must not look like a framework project.** A root `package.json` with `next` and a `next.config.ts` made the host build it as Next.js and no deployment came out, even with `"framework": null` in `vercel.json`. Keep generators in `web/` or `_src/`, commit the built folder.
- **Multi-page by default.** A one-page redesign was later split into seven pages; plan the pages before building.
