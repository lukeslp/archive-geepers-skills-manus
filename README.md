# geepers-manus

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Language: Markdown](https://img.shields.io/badge/language-markdown-blue.svg)](https://daringfireball.net/projects/markdown/)

Generated Manus skill mirror for the geepers ecosystem.

## Source of Truth

This repository is synced from canonical skills in:
- `https://github.com/lukeslp/geepers`
- Canonical path: `skills/source/`

Direct edits to `skills/` in this repo are blocked by CI. Make changes in canonical source, then sync.

## What Is Here

- `skills/`: generated skill folders for Manus workflows
- `manus-skills.json`: generated package metadata
- `aliases.generated.json`: migration alias map
- `.github/workflows/mirror-readonly-guard.yml`: mirror protection

## Sync Workflow

From canonical repo (`/home/coolhand/geepers`):

```bash
python3 scripts/validate-skills.py --strict
python3 scripts/build-platform-packages.py --platform manus --clean
bash scripts/sync-mirrors.sh --platform manus --delete --skip-build
bash scripts/report-drift.sh --platform manus --skip-missing
```

## License

MIT — see [LICENSE](LICENSE)

Built by [Luke Steuber](https://lukesteuber.com) · [luke@lukesteuber.com](mailto:luke@lukesteuber.com) · [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com)
