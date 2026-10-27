# DADA-Lite

The Directed Ambition Design Agent on a budget. Same goal as [DADA](https://github.com/SolutionsAsService/dada): ambitious design that survives critique. It costs far fewer tokens.

| | DADA | DADA-Lite |
|---|---|---|
| Critics | one sub-agent per authority (7+ seats), every round | four seats in **one** pass per round, run by at most one sub-agent |
| Rounds | until two consecutive rounds are clean, no cap | at most **three**; stop at the first round with no objection |
| Defect finding | critics read screenshots | **scripts measure first**: overflow, text contrast, contrast over photos, targets, alt |
| Log | five artifacts, full anchor ledger | one short `DESIGN-LOG.md` |

Why it works: on recent site redesigns, most real defects (text over photos, cut-off focus rings, overflow, a fix's own regression) were found by measurement, not by critics, and several critic "defects" were screenshot artefacts. DADA-Lite measures first and spends the critic pass on what scripts can't judge: ambition, claims, hierarchy and type.

## Install

```sh
npx skills add SolutionsAsService/dada-lite -s dada-lite
```

Or copy `skills/dada-lite` into your agent's skills folder (for Claude Code, `~/.claude/skills/dada-lite`). `.agents/skills/dada-lite` links to it for workspace discovery.

## Use

Invoke `$dada-lite` (or `/dada-lite`) with a brief, for example "redesign this landing page" or "a site for a hot tub dealer in San Diego". Read [`skills/dada-lite/SKILL.md`](skills/dada-lite/SKILL.md) for the contract.

The bundled tools need Python with `pip install playwright pillow`, plus a local Chrome or `playwright install chromium`:

```sh
python skills/dada-lite/tools/audit.py   --base http://localhost:8000 --pages index,contact --widths 1280,390,320
python skills/dada-lite/tools/capture.py --base http://localhost:8000 --pages index,contact --out shots/r1
```

`references/carry-forward.md` lists CSS and capture traps found in earlier runs, each with the measurement that proved it. Read it before building.

## Repository

- `skills/dada-lite/`: the skill (SKILL.md, references, tools, agent metadata).
- `tools/` and `web/`: the DADA showcase page and its measurement tools, inherited from the DADA repository.
- `scripts/validate_skills.py`: metadata and link validation (CI runs it on every push).
