# .claude — Claude Code hooks

Will hold `settings.json` and `hooks/idem-hook.sh`: deny writes under `00_fetch/00_snapshots/`,
validate every `*.tickets.md` after it is written, and block the session from finishing while any
fails. Not built yet.
