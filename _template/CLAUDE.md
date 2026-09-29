# <Projectnaam>

> Volgt de root-instructies in `../CLAUDE.md` (WAT-framework + automatische skill-selectie).

## Doel
<Wat moet er worden opgeleverd?>

## Domein
<code / content / data / API / automatisering>

## Frequentie
<eenmalig / dagelijks / wekelijks / continu>

## Inputs
- <bronnen, bestanden, API's>

## Outputs
- <rapport, dataset, dashboard, ...>

## Workflows
- `workflows/` — <lijst de SOPs zodra ze bestaan>

## Tools
- `tools/` — projectspecifieke scripts
- `../shared/tools/` — gedeelde scripts (eerst hier zoeken)

## Context & afspraken
- API-sleutels staan in `.env` (zie `.env.example`), nooit in code of workflows
- Tijdelijke bestanden in `.tmp/`
