# Skill: `schedule` / `loop`

## Wanneer gebruiken

Gebruik **`/schedule`** wanneer:
- Een taak eenmalig of herhaaldelijk op een vast tijdstip moet draaien
- De gebruiker vraagt om een cron-job, dagelijkse/wekelijkse routine
- Een remote agent automatisch moet worden gestart op een schema
- "Herinner me aan X", "doe dit elke maandag", "plan dit voor 15:00"

Gebruik **`/loop`** wanneer:
- Een taak continu of op een interval herhaald moet worden *tijdens* een sessie
- Je iets wil blijven monitoren (bijv. elke 5 minuten status checken)
- Een build, deploy of CI-run gevolgd moet worden totdat het klaar is

## Verschil

| Aspect | `/schedule` | `/loop` |
|--------|-------------|---------|
| Timing | Vaste cron-tijden | Interval binnen sessie |
| Waar | Remote agent (buiten sessie) | In de huidige sessie |
| Gebruik | "Elke dag om 9:00" | "Blijf controleren totdat..." |

## Triggers in project-CLAUDE.md

- "automatisch", "elke dag", "wekelijks", "cron", "geplande taak"
- "poll", "monitor", "houd bij", "blijf controleren"
- Workflows met tijdgebonden frequentie (bijv. `Frequentie: dagelijks`)

## Voorbeeld aankondiging

> 🎯 **Skill: `schedule`** — Dit project heeft een wekelijkse data-export als workflow. Ik gebruik `/schedule` om een terugkerende agent in te plannen die dit automatisch uitvoert.
