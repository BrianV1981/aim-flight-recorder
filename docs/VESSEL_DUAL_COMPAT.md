# Vessel dual compatibility (Grok + AGY)

**Rule:** Improvements for Grok CLI must **not** strip AGY brain paths, history hooks, or install docs.

## Session sources

| Vessel | Path pattern |
|--------|----------------|
| AGY | `~/.gemini/antigravity-cli/brain/<id>/.system_generated/logs/transcript.jsonl` |
| Grok | `~/.grok/sessions/<urlencode(cwd)>/<session_id>/updates.jsonl` |

## Skill install

| Vessel | Skills dir |
|--------|------------|
| Grok | `~/.grok/skills/` or `<project>/.grok/skills/` |
| AGY | `~/.gemini/antigravity-cli/skills/` or project `.gemini/skills/` |

Symlink the **repository root** (contains `SKILL.md` + `scripts/`).

## Scripts

- `scripts/flight_recorder.py` — auto-detect format (`parse_agy_transcript` / `parse_grok_updates`); `--input` for either file.
- `scripts/list_sessions.py` — lists **both** vessels.

## Path hygiene

No machine-local absolute homes (`/home/<user>/…`) in `SKILL.md` / README examples. Use `$SKILL_ROOT`, `$HOME`, `~`, or relative `scripts/…`.

## Tests

```bash
python3 -m unittest tests.test_flight_recorder -v
```
