# Skill: `run` / `verify`

## Wanneer gebruiken

Gebruik **`/run`** wanneer:
- De app gestart moet worden om gedrag te observeren
- De gebruiker vraagt om een screenshot of live-demo van de app
- Een nieuwe feature getest moet worden in de echte omgeving
- Je wil bevestigen dat iets werkt *voor* je het commit

Gebruik **`/verify`** wanneer:
- Een specifieke fix of wijziging gecontroleerd moet worden
- De gebruiker vraagt "werkt het nu?", "klopt dit?", "check even of..."
- Je een eerdere change wil valideren zonder de hele app te starten

## Wat het doet

`/run`:
- Zoekt naar project-specifieke start-instructies (CLAUDE.md)
- Detecteert het project-type automatisch (CLI, server, browser, Electron)
- Start de app en observeert het gedrag

`/verify`:
- Voert de app/tests uit gericht op de gewijzigde functionaliteit
- Rapporteert wat het ziet (werkt ✅ / werkt niet ❌)

## Triggers in project-CLAUDE.md

- "start", "draai", "test de app", "screenshot", "controleer gedrag"
- Aanwezige bestanden: `main.py`, `app.py`, `index.js`, `server.py`
- Aanwezige configuratie: `Dockerfile`, `docker-compose.yml`

## Voorbeeld aankondiging

> 🎯 **Skill: `verify`** — Er is een recente bugfix doorgevoerd in `scraper.py`. Ik gebruik `/verify` om te bevestigen dat de fix correct werkt voordat we verder gaan.
