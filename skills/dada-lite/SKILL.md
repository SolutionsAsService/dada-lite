---
name: dada-lite
description: "DADA-Lite: the Directed Ambition Design Agent at a fraction of the token cost. Use when asked to design, redesign or critique a website, landing page, poster, identity or other visual artifact with real ambition but on a budget, or when the user asks for dada-lite or a cheaper DADA. Measures first with bundled scripts (overflow, contrast, contrast over photos, targets), judges with one four-seat critic panel per round run by at most one sub-agent, caps the run at three rounds, and keeps a one-file design log. Escalate to full DADA only when the user asks for it by name."
---

# DADA-Lite

Full DADA convenes one sub-agent per critic, every round, until two rounds come back clean. On a recent run that was about 35 critic agents per website. DADA-Lite keeps what actually found the defects and drops the rest:

- **Measurements found most of the real problems** (text over photos, focus rings cut off, overflow, a regression a fix introduced). Scripts are cheap, so they run first, every round.
- **Critics were best at strategy and taste** (name, claims, ambition, hierarchy). One panel pass per round covers that.
- **Several "defects" were capture artefacts** (smooth scrolling, fixed bars in stitched shots). Check the live page before spending a move on a screenshot finding.

## Budget (hard limits)

- At most **one critic sub-agent per round**. It plays all four seats. If you have no sub-agent tool, or the change is small, run the panel inline.
- At most **three panel rounds** after the build: R1, then R2 only if R1 had an OBJECT, then R3 only if R2 changed the page. Stop as soon as a round has no OBJECT.
- Critics read the **first-screen shots** (`*-top.jpg`) plus at most four full-page shots. Never every page at every width.
- No premortem agent. Do the premortem yourself from the old site's captures and its audit.

## Mode

- **Adaptive** (default for anything with a client, customer or public): both poles must hold — *most advanced yet acceptable* (Loewy's MAYA).
- **Autonomous** (art on its own terms): only if the brief says so.

## The four seats

One voice each, arguing only from its own source, each pointing at something visible in the work:

| Seat | Source | Asks |
|---|---|---|
| Provocateur | Viktor Shklovsky, *Art as Technique* | What here could belong to no one else? What has gone automatic? |
| Inclusion | Ronald Mace et al., *The Principles of Universal Design* | Who can't use this, and where? (Read the audit numbers.) |
| Usability | Steve Krug, *Don't Make Me Think* | Is the page self-evident in five seconds? What words can go? |
| Craft | Robert Bringhurst, *The Elements of Typographic Style* | Is there one type system, a scale, a measure, honest details? |

The Provocateur and Usability seats are a deliberate dotted pair: estrangement against ease. MAYA decides between them, usually by putting the break where it costs nothing (a hero, a device) and keeping the action path plain.

For brand or claims-heavy work, swap Craft for **Honesty** (Alberto Cairo, *How Charts Lie*): every number, testimonial or promise on the page must be sourced or marked as a placeholder. Never invent reviews, stats, prices, licences or years in business.

## Workflow

### 0. Read the carry-forward
Read [references/carry-forward.md](references/carry-forward.md) and the project's own `CARRY-FORWARD.md` if one exists. Apply them before building.

### 1. Plan (5 minutes, in the log)
- One-sentence brief and the mode.
- **Seed**: one stance, two rules, one breaker, and one counterpoint reached by a dotted edge, copied verbatim from [references/anchor-graph.md](references/anchor-graph.md). Good defaults for websites: stance `Make It Bigger (Paula Scher)` or `White (Kenya Hara)`; rules `Grid Systems in Graphic Design (Josef Müller-Brockmann)` and `WCAG 2.2 Contrast and Perceivability (W3C)`; a breaker such as `Saul Bass: A Life in Film and Design (Jennifer Bass, Pat Kirkham)`, `Learning from Las Vegas (Venturi, Scott Brown, Izenour)` or `Irma Boom: Biography in Books (Irma Boom)`.
- **Pages**: websites are multi-page whenever possible: a page per service, product, topic or tool, plus home and the contact, about or legal pages that apply, under shared navigation. One page only for something that is genuinely one screen (a single-purpose tool or game), with the reason in the log. Redesigning a one-page site means splitting it.
- **Premortem** of what exists, if anything: capture it, run the audit, and list its failures yourself.

### 2. Build
Make the moves. Before each batch, write a short record for each move:

```
M3 BREAK — <name>. Anchors: <labels>. Why: <claim, grounds>. Rejected: <one alternative>. Measure: <what number should change>.
```

### 3. Measure (every round, before any critic)
```bash
python tools/capture.py --base http://localhost:8000 --pages index,about --out shots/r1
python tools/audit.py   --base http://localhost:8000 --pages index,about --widths 1280,390,320
```
Fix everything the audit reports that is real, then re-run until `TOTAL` holds only what you can defend. Small targets inside a list with spacing, or a 24px-plus link, may pass WCAG 2.5.8 even if the audit lists them. Once per project, break something on purpose and confirm the audit fails.

### 4. Panel (one round = one pass)
Give the critic agent (or yourself) a brief with: the artifact, the mode, the four seats, the `-top` shots plus up to four full pages, the audit output, the move records, and any placeholders that are deliberate. Each seat answers in under 120 words: what the work says, one question, the verdict PASS or OBJECT, and at most two concrete changes (page or selector).

Before acting on an OBJECT, **check its premise on the live page**. If a measurement refuses it, overrule it and record the measurement. Don't spend a move on it.

### 5. Fix, then decide whether to stop
- An OBJECT that holds becomes a move, re-measured with the audit.
- **Stop when:** a panel round has no OBJECT, the audit is clean (or every remaining line is defended in the log), and the boldest move has been pushed once, with what changed measured.
- Never stop on a round count alone, and never exceed three panel rounds. If round three still objects, log the open items and tell the user.

### 6. Log and carry forward
One file, `DESIGN-LOG.md`, kept short: plan and seed, move records, a table per panel round (seat, verdict, change), the audit totals per round, and a stop check. Add any new fact about the medium (a CSS trap, a capture trap) to `CARRY-FORWARD.md`, with the measurement that proved it.

## What to tell the user
The mode, how many panel rounds ran, the audit result, what was overruled by measurement, and every placeholder the owner must fill (phone, email, licence, photos, prices). Say plainly if the run stopped at the round cap with objections open.
