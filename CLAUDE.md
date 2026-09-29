# Claude Projects — Root Instructies

> Deze instructies gelden voor **alle projecten** in deze map. Project-specifieke instructies staan in het `CLAUDE.md` van elk subproject.

---

## 🎯 Automatische Skill-selectie

**Bij het openen of starten van elk project bepaal je altijd zelf welke skill het beste past. Dit doe je als volgt:**

### Stap 1 — Lees het project-CLAUDE.md
Open en lees het `CLAUDE.md` van het actieve project. Let op:
- **Doel**: wat moet er worden opgeleverd?
- **Domein**: code, content, data, API, automatisering?
- **Frequentie**: eenmalig, wekelijks, continu?

### Stap 2 — Scan de projectbestanden
Kijk welke bestanden aanwezig zijn:
- `.py`, `.js`, `.ts`, `.go` → code-project
- `import anthropic` / `@anthropic-ai/sdk` → Claude API-project
- `.env`, `auth.*`, `secrets.*` → security-gevoelig project
- `main.py`, `app.py`, `server.*`, `index.js` → uitvoerbare app
- Geen code, alleen `.md` → content/workflow-project

### Stap 3 — Vergelijk met de skill-profielen
Lees `../skills/README.md` (of het relevante skill-bestand) en match op basis van de beslislogica daarin.

### Stap 4 — Kondig je keuze aan
Meld **altijd** welke skill je hebt gekozen en waarom, in dit formaat:

```
🎯 Skill: `<skill-naam>`
Reden: <één zin waarom deze skill het beste past bij dit project/taak>
```

Daarna ga je direct aan de slag met die skill, tenzij de gebruiker een andere keuze maakt.

---

## 📁 Mappenstructuur

```
Claude/
├── CLAUDE.md                        ← dit bestand (root-instructies)
├── README.md                        ← overzicht van de structuur
├── skills/                          ← skill-profielen voor auto-detectie
│   ├── README.md                    ← beslislogica + overzichtstabel
│   ├── code-review.md
│   ├── security-review.md
│   ├── claude-api.md
│   ├── schedule.md
│   └── run-verify.md
├── shared/                          ← gedeelde tools en workflows
│   ├── tools/
│   └── workflows/
├── _template/                       ← kopieer bij elk nieuw project
└── [project-mappen]/                ← actieve projecten
```

---

## 📋 WAT-framework (geldt voor alle projecten)

Elk project volgt het **WAT-framework**:

| Laag | Wat | Waar |
|------|-----|------|
| **W**orkflows | SOPs en instructies | `workflows/` |
| **A**gents | Jij — coördinatie en beslissingen | (dit ben jij) |
| **T**ools | Python-scripts voor uitvoering | `tools/` + `../shared/tools/` |

**Kernregels:**
1. Zoek altijd eerst naar een bestaand tool voordat je iets nieuws bouwt
2. Gebruik deterministische scripts voor uitvoering — jij handelt de coördinatie
3. Sla API-sleutels op in `.env`, nooit in code of workflows
4. Werk workflows bij wanneer je nieuwe kennis opdoet (na toestemming)

---

## 🔄 Bij een nieuw project

1. Kopieer `_template/` en geef het een duidelijke naam
2. Vul `CLAUDE.md` in met doel, inputs en context
3. Voer automatische skill-detectie uit (zie hierboven)
4. Start met de geselecteerde skill
