# Skill: `security-review`

## Wanneer gebruiken

Gebruik **`/security-review`** wanneer:
- Het project werkt met API-sleutels, tokens of wachtwoorden
- Er authenticatie of autorisatielogica aanwezig is
- Data van gebruikers wordt verwerkt of opgeslagen
- Het project communiceert met externe services of APIs
- De gebruiker vraagt om beveiligingsanalyse

## Wat het doet

Analyseert de huidige branch/diff op:
- Hardcoded credentials of secrets
- Onveilige dataverwerking of opslag
- Kwetsbaarheden in authenticatieflows
- Onveilige API-aanroepen of configuraties
- Ontbrekende input-validatie

## Triggers in project-CLAUDE.md

- "security", "auth", "tokens", "API-keys", "wachtwoorden", "kwetsbaarheden"
- Aanwezige bestanden: `.env`, `auth.py`, `middleware.js`, `secrets.*`
- Project-domein: financieel, medisch, gebruikersdata, betalingen

## Combineer met

- Na `code-review` voor een volledige analyse
- Vóór een release of productie-deploy

## Voorbeeld aankondiging

> 🎯 **Skill: `security-review`** — Dit project verwerkt API-sleutels en gebruikersdata. Ik voer `/security-review` uit om kwetsbaarheden in de huidige wijzigingen op te sporen.
