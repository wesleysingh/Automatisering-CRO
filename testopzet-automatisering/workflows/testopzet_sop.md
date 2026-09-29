# SOP: automatische testopzet

## Hoe het werkt
1. Je werkt een idee uit in Jira Product Discovery (omschrijving = globaal idee + inzichten).
2. Via "Create delivery ticket" ontstaat een taak op het CRO-bord (bijv. `VP 016 - Afrekenknop bovenaan weghalen`), met subtaak **Testopzet uitwerken**.
3. Zet je die subtaak op **Gereed**, dan stuurt een Jira Automation-regel direct een seintje naar GitHub Actions. Binnen 1 à 2 minuten:
   - leest het gekoppelde idee en eventuele Confluence-links naar een vorige test,
   - schrijft met Claude de aanleiding, hypothese, optimalisatiestrategie en psychologisch principe,
   - maakt onder de testenpagina een pagina aan met exact de naam van de Jira-taak,
   - plaatst de link als commentaar op de subtaak en op het idee.

Vangnet: GitHub controleert daarnaast elk uur alle klanten, voor het geval een seintje mislukt.

Er worden geen labels gebruikt. Het script ziet aan de Confluence-pagina (zelfde naam als de Jira-taak) of een subtaak al verwerkt is.
4. Vul daarna zelf in: Testsegment, Significantielevel, MDE, Testperiode, KPI, Guardrail, Aanvullende metrics en de A/B-screenshots.

**Vervolgtest?** Plak de link naar de Confluence-pagina van de vorige test in de omschrijving van het idee. De aanleiding begint dan met "Uit <vorige test> blijkt dat…".

## Nieuwe klant toevoegen
Alle klanten staan op `wesleysingh.atlassian.net`, met per klant een eigen Confluence-space, CRO-project en Discovery-project.
1. Maak in Atlassian aan: de Confluence-space van de klant met daarin een pagina of map voor de testen, het CRO-project en het Discovery-project. Geef de klant toegang.
2. Kopieer `clients/_voorbeeld.yaml` naar `clients/<klant>.yaml` en vul het in: naam, projectkey, ID van de testenpagina/-map en `vanaf_datum` op vandaag.
3. Maak in het CRO-project van de klant de Jira Automation-regel aan (zie hieronder), met de klant-slug in `client`.
4. Test met een dry-run (zie hieronder).

Verder hoeft er niets te veranderen: de inloggegevens en de GitHub-workflow gelden voor alle klanten.

## Jira Automation-regel (per klant, in het CRO-project)
Project settings → Automation → Create rule:
- **Trigger:** *Work item transitioned*, naar status **Gereed**
- **Condition:** *JQL condition*: `issuetype in subTaskIssueTypes() AND summary ~ "\"Testopzet uitwerken\""`
- **Action:** *Send web request*
  - URL: `https://api.github.com/repos/<github-gebruiker>/<repo>/actions/workflows/testopzet.yml/dispatches`
  - HTTP method: `POST`
  - Web request body: *Custom data*: `{"ref": "main", "inputs": {"client": "verfplaza", "issue": "{{issue.key}}"}}`
  - Headers: `Accept: application/vnd.github+json`, `Authorization: Bearer <GitHub-token>`, `X-GitHub-Api-Version: 2022-11-28`
- Een geslaagd seintje geeft status **204** in de audit log van de regel.

**GitHub-token voor Jira:** GitHub → Settings → Developer settings → Personal access tokens → *Fine-grained tokens* → Generate new token. Repository access: alleen deze repo. Permissions: **Actions: Read and write** (verder niets). Let op de vervaldatum: vernieuw het token op tijd en werk het bij in de Jira-regels.

**Pagina- of map-ID vinden:** open de pagina of map in Confluence; het ID is het getal in de adresbalk (bijv. `.../pages/123456789/Testen` of `.../folder/123456789`).

## Handmatig draaien
```bash
cd testopzet-automatisering
python tools/poll_jira.py --client verfplaza --issue CRO-123 --dry-run   # bekijken, niets schrijven
python tools/poll_jira.py --client verfplaza --issue CRO-123             # echt aanmaken
```
Of in GitHub: Actions → "Testopzet automatisering" → Run workflow.

## Als het misgaat
| Situatie | Wat er gebeurt | Oplossen |
|---|---|---|
| Geen idee gekoppeld / tekst voldoet 2× niet aan de regels | Eén commentaar met de reden op de subtaak; het script onthoudt dit onzichtbaar en probeert het niet elke poll opnieuw | Oorzaak oplossen, subtaak terugzetten en opnieuw op Gereed zetten |
| Pagina met de naam van de taak bestaat al | Subtaak wordt stil overgeslagen (geldt als verwerkt) | Wil je een nieuwe versie: oude pagina verwijderen of hernoemen |
| Tijdelijke Atlassian-fout | Workflow faalt (je krijgt een e-mail van GitHub) | Niets: volgende poll probeert opnieuw |
| Jira-taak hernoemd nadat de pagina is gemaakt | Script vindt de pagina niet en maakt een tweede aan | Pagina dezelfde naam geven als de taak |

## Instructies aanpassen
- Schrijfregels: `knowledge/instructies.md` (`{kpi}` wordt per klant ingevuld)
- Optimalisatiestrategieën: `knowledge/boom_strategie.md`
- Voorbeeld: `knowledge/voorbeeld_testopzet.md`
- Paginaopbouw: `templates/testpagina.xml.j2` (per klant te overschrijven via `template:` in de klant-yaml)
