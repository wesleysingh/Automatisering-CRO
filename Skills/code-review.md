# Skill: `code-review` / `simplify`

## Wanneer gebruiken

Gebruik **`/code-review`** wanneer:
- Er recente codewijzigingen zijn (git diff aanwezig)
- De gebruiker vraagt om feedback op kwaliteit, leesbaarheid of correctheid
- Er bugs gerapporteerd worden en je wil de code scannen
- Een PR of branch gereed is voor review

Gebruik **`/simplify`** wanneer:
- De code werkt maar te complex, lang of redundant is
- De gebruiker vraagt om refactoring of cleanup
- Je zelf merkt dat code herhaalt of omslachtig is

## Niveaus

| Niveau | Gebruik |
|--------|---------|
| `low` | Snelle scan, alleen evidente problemen |
| `medium` | Standaard review (default) |
| `high` | Grondige analyse, ook subtiele problemen |
| `ultra` | Diepgaande multi-agent cloud review |

## Opties

- `--comment` → Post bevindingen als inline PR-opmerkingen
- `--fix` → Pas de bevindingen direct toe op de code

## Triggers in project-CLAUDE.md

- "review", "audit", "kwaliteit", "bugs", "correctheid"
- Aanwezige bestanden: `.py`, `.js`, `.ts`, `.go`, `.rs`
- Git-status: gewijzigde bestanden aanwezig

## Voorbeeld aankondiging

> 🎯 **Skill: `code-review`** — Dit project bevat Python-scripts met recente wijzigingen (3 bestanden gewijzigd). Ik gebruik `/code-review medium` om kwaliteit en correctheid te beoordelen.
