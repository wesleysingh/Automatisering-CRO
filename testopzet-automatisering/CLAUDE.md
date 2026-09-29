# Testopzet-automatisering

> Volgt de root-instructies in `../CLAUDE.md` (WAT-framework + automatische skill-selectie).

## Doel
Automatisch de testopzet (Pre-test-sectie) van een A/B-test in Confluence aanmaken zodra de Jira-subtaak "Testopzet uitwerken" op Gereed gaat. Herbruikbaar voor meerdere webshops.

## Domein
Automatisering + Claude API (Jira Cloud, Confluence Cloud, Anthropic SDK).

## Frequentie
Continu: GitHub Actions pollt elke 15 minuten.

## Inputs
- Jira Product Discovery-idee (titel + omschrijving), gevonden via subtaak → taak → delivery-link
- Confluence-links in de omschrijving van het idee → vorige test(en)
- `knowledge/`: schrijfinstructies, optimalisatiestrategieën, voorbeeld-testopzet
- `clients/<klant>.yaml`: configuratie per webshop (aangevuld met `clients/_standaard.yaml`)

## Atlassian-inrichting
Eén site (`wesleysingh.atlassian.net`) voor alle klanten. Per klant: eigen Confluence-space (met testenpagina of -map), eigen CRO-project en eigen Discovery-project; de klant krijgt toegang tot zijn eigen space/projecten.

## Outputs
- Confluence-pagina met exact de naam van de Jira-taak (bijv. `VP 016 - ...`) onder `parent_page_id`, met ingevulde aanleiding, hypothese, optimalisatiestrategie en psychologisch principe; overige velden leeg voor handmatige invulling
- Commentaar met link op de Jira-subtaak en het idee (geen labels)

## Workflows
- `workflows/testopzet_sop.md`: werking, nieuwe klant toevoegen, handmatig draaien, foutafhandeling

## Tools
- `tools/poll_jira.py`: entrypoint (`--all` / `--client` / `--issue` / `--dry-run`)
- `tools/generate_testopzet.py`: Claude-aanroep (`claude-opus-5-5`, structured output) + validatie van de schrijfregels
- `tools/build_page.py`: rendering van `templates/testpagina.xml.j2`
- `../shared/tools/atlassian_client.py`: Jira/Confluence REST-client (herbruikbaar)
- `../shared/tools/adf_to_text.py`: ADF/storage → tekst

## Context & afspraken
- Secrets: `ANTHROPIC_API_KEY` + `ATLASSIAN_EMAIL`/`ATLASSIAN_TOKEN` in `.env` (lokaal) en GitHub secrets
- Idempotentie zonder labels: 'klaar' = Confluence-pagina met de naam van de Jira-taak bestaat; 'mislukt' = onzichtbare issue property `testopzet-automatisering` (fout_op), opnieuw proberen door de subtaak opnieuw op Gereed te zetten
- Tests: `pytest` in deze map (draait ook in de workflow vóór elke poll)
- Tijdelijke bestanden (dry-run-output) in `.tmp/`
