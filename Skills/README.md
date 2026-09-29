# Skills — Automatische Skill-detectie

Deze map bevat profielen voor elke beschikbare Claude Code skill. Bij het openen van een project leest Claude dit automatisch en bepaalt welke skill het best aansluit.

## Hoe het werkt

Wanneer Claude een project opstart:
1. Leest Claude het project-`CLAUDE.md` (doel, domein, inputs/outputs)
2. Scant Claude de aanwezige bestanden (extensies, configuratiebestanden)
3. Vergelijkt Claude dit met de profielen hieronder
4. Kondigt de beste skill aan en legt uit waarom

---

## Skill-profielen op een rij

| Skill | Beste voor | Triggerwoorden |
|-------|-----------|----------------|
| `code-review` | Code-wijzigingen beoordelen | review, audit, diff, kwaliteit, bugs |
| `simplify` | Code opruimen + vereenvoudigen | refactor, opruimen, vereenvoudig, cleanup |
| `security-review` | Beveiligingsanalyse | security, auth, tokens, API-keys, kwetsbaarheden |
| `claude-api` | Anthropic SDK / Claude API integraties | anthropic, claude API, SDK, prompt caching |
| `run` | App starten en gedrag verifiëren | start, draai, test de app, screenshot |
| `verify` | Bevestigen dat een fix werkt | werkt het, controleer, valideer, verifieer |
| `schedule` | Terugkerende of geplande taken | elke dag, wekelijks, automatisch, cron |
| `loop` | Herhalende monitoring/polling | poll, houd bij, blijf controleren, interval |
| `init` | Nieuw project opzetten | nieuw project, leeg project, initialiseer |

---

## Beslislogica (voor Claude)

Volg deze volgorde bij het kiezen:

### Stap 1 — Taal/technologie detecteren
- Python-bestanden (`.py`) + `requirements.txt` → code-gerelateerde skill
- `import anthropic` of `@anthropic-ai/sdk` → **claude-api**
- JS/TS + `package.json` → code-gerelateerde skill
- Alleen Markdown/content → content-gerelateerde skill

### Stap 2 — Project-intentie uit CLAUDE.md lezen
- Bevat "review", "audit", "kwaliteit" → **code-review**
- Bevat "security", "auth", "kwetsbaarheden" → **security-review**
- Bevat "elke dag", "wekelijks", "automatisch" → **schedule**
- Bevat "monitor", "poll", "controleer regelmatig" → **loop**
- Bevat "start", "test", "draai de app" → **run**
- Bevat "nieuw", "initialiseer", "leeg" → **init**

### Stap 3 — Bestandsstatus
- Er zijn gewijzigde bestanden (git diff niet leeg) → overweeg **code-review** of **simplify**
- App-entrypoint aanwezig (`main.py`, `app.py`, `index.js`) → overweeg **run** of **verify**

### Stap 4 — Aankondiging
Meld altijd welke skill is gekozen en waarom, bijvoorbeeld:

> 🎯 **Skill: `code-review`** — Dit project bevat Python-scripts met recente wijzigingen. Ik gebruik code-review om de kwaliteit te beoordelen.

---

## Meerdere skills tegelijk?

Soms passen meerdere skills. Prioriteer dan:
1. De skill die het meest aansluit bij het **huidige doel** (niet het project in het algemeen)
2. Bij twijfel: vraag de gebruiker

---

## Skill-bestanden in deze map

- [code-review.md](code-review.md) — wanneer code-review gebruiken
- [security-review.md](security-review.md) — wanneer security-review gebruiken
- [claude-api.md](claude-api.md) — wanneer claude-api gebruiken
- [schedule.md](schedule.md) — wanneer schedule/loop gebruiken
- [run-verify.md](run-verify.md) — wanneer run/verify gebruiken
