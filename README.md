# Automatisering CRO — Overzicht

Werkmap voor Claude-projecten rond CRO-automatisering. Alle projecten volgen het **WAT-framework** (Workflows, Agents, Tools). Zie [CLAUDE.md](CLAUDE.md) voor de root-instructies.

## Structuur

| Map | Doel |
|-----|------|
| `Skills/` | Skill-profielen + beslislogica voor automatische skill-selectie |
| `shared/tools/` | Herbruikbare Python-scripts voor alle projecten |
| `shared/workflows/` | Herbruikbare SOPs voor alle projecten |
| `_template/` | Startpunt voor elk nieuw project |
| `<project>/` | Actieve projecten (kopie van `_template/`) |

## Nieuw project starten

```bash
cp -R _template "<projectnaam>"
cp "<projectnaam>/.env.example" "<projectnaam>/.env"   # vul sleutels in
```

Vul daarna `<projectnaam>/CLAUDE.md` in en open het project met Claude; die kiest automatisch de passende skill.
