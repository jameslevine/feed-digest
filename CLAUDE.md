# feed-digest

Daily AI digest of James's RSS feeds. A scheduled Claude Code routine reads the
feeds in `feeds.opml`, leads with items that match `stack.yaml` and pushes the
result to `main`. Readers subscribe to `digest.xml` through raw.githubusercontent.com.

Global rules come from claude-setup (`~/.claude/CLAUDE.md`). This file adds
what's specific to this repo, and it wins where the two conflict.

## Stack

- Python 3, standard library only (no dependencies, nothing to install)
- Hosting: none. `digest.xml` is served from `main` by raw.githubusercontent.com
- The digest itself is written by a Claude Code routine, not by code in this repo

## Commands

| Task | Command |
|---|---|
| Regenerate `feeds.opml` | `python3 gen_feeds.py` (also overwrites `~/.config/netnewswire/feeds.opml`; not run during onboarding) |
| Lint | `uvx ruff@0.17.1 check --no-cache --select E9,F63,F7,F82 .` |
| Smoke check | the `run:` steps of the `smoke` job in `.github/workflows/ci.yml` |
| Secret scan | `gitleaks git --no-banner --redact .` |

There are no tests. CI (`.github/workflows/ci.yml`) runs the secret scan, lint
and smoke check on every PR and push to `main`.

## Layout

- `gen_feeds.py`: the one feed list. Writes `feeds.opml` and the NetNewsWire copy
- `feeds.opml`: the routine's sources (generated, commit it after regenerating)
- `stack.yaml`: what the digest leads with. Edit by hand, no code change needed
- `digest.xml`, `digests/<date>.html`, `state.json`: the routine's output

## Conventions

- Tickets: this repo's issues are its micro board, mirrored onto
  `jameslevine/personal-task-manager` as `project: feed-digest`.
- Branches: `ticket-<n>/<slug>`, one PR per ticket. The repo is public, so
  Claude opens PRs and James merges.
- Secrets: none. Nothing here reads an env var or an API key, so there is no
  `.env.tpl`. Keep it that way: everything in this repo is public.
- MCP: no `.mcp.json`. The user-scope core servers cover it.

## Gotchas

- The routine commits `digest: <date>` to `main` every morning (06:15 to 06:30
  UTC so far). Rebase onto `main` before review, and don't hand-edit its output files.
- The routine's environment can reach GitHub only for this repo, so the repo
  copy of `feeds.opml` swaps GitHub release feeds for PyPI ones, or drops them.
- Run `gen_feeds.py` from the repo root: it writes `feeds.opml` relative to
  the working directory.
