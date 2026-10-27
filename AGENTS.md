# DADA-Lite project

The distributable skill lives in `skills/dada-lite/`. `.agents/skills/dada-lite` is a symlink to it for workspace discovery. Keep the YAML frontmatter `name` equal to the folder name, and keep `agents/openai.yaml` consistent with it (`$dada-lite` in the default prompt, short description 25–64 characters).

`references/anchor-graph.md` is copied verbatim from the DADA skill. Keep labels identical so seeds copied from it stay valid.

The skill's point is cost. Don't add steps that convene more agents or more rounds. If a lesson needs adding, add it to `references/carry-forward.md` as one line, with the measurement that proved it.

The bundled tools (`tools/audit.py`, `tools/capture.py`) must keep working against any site served over HTTP, with Playwright and a local Chrome or Playwright's Chromium. Test the auditor by breaking something on purpose and confirming it fails.

Validate with `python3 scripts/validate_skills.py` (needs PyYAML). Commit only as the repository owner, with no tool attribution lines.
