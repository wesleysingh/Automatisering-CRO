---
name: verfplaza-huisstijl
description: Verfplaza-huisstijl (kleuren, Roboto, logo, tone of voice) voor alles wat visueel voor of over Verfplaza wordt gemaakt. Gebruik bij elke grafiek, chart, plot, presentatie, slide deck, PowerPoint, Word/PDF-document, rapport of HTML-pagina voor Verfplaza / Verf-plaza / verfplaza.nl, ook als de huisstijl niet expliciet genoemd wordt.
---

# Verfplaza-huisstijl

Bron: verfplaza.nl (CSS + logo). Alle waarden staan in [tokens.json](tokens.json); dat is de enige bron van waarheid, dus neem kleuren daaruit over en verzin geen eigen kleuren.

## Kern in één oogopslag

| Rol | Kleur | Hex |
|---|---|---|
| Primair (koppen, tekst, vlakken) | Navy | `#143D59` |
| Accent (highlight, logo-geel) | Geel | `#F3B41A` |
| CTA / positief / winnaar | Groen | `#11A24A` |
| Negatief / verliezer / fout | Rood | `#E13522` |
| Rustig vlak / achtergrondblok | Lichtblauw | `#E2EFF7` |
| Neutraal / controle | Grijs | `#919191` |

- **Font:** Roboto (400 tekst, 500 medium, 700 koppen); fallback Arial.
- **Vorm:** licht afgeronde hoeken (4–8 px), veel wit, geen schaduwen of verlopen.
- **Logo:** [assets/logo.svg](assets/logo.svg) (navy + geel). Altijd op een witte of lichte ondergrond, nooit vervormen of hercoloren.
- **Tone of voice:** informeel en behulpzaam: spreek de lezer aan met **je/jouw** (geen u), korte zinnen, concreet en zonder vakjargon. De merknaam is "Verfplaza" (de website gebruikt ook "Verf-plaza").

## Gebruik geel spaarzaam
Geel is een accentkleur: één highlight per grafiek of slide. Zet nooit witte tekst op geel; op geel staat navy tekst.

## Per outputtype
- **Grafieken** (matplotlib, plotly, charts in artifacts) → lees [references/grafieken.md](references/grafieken.md). Python: `scripts/verfplaza_style.py` (`apply_matplotlib()`, `plotly_template()`).
- **Presentaties en documenten** (pptx, docx, pdf, HTML-rapport) → lees [references/presentaties.md](references/presentaties.md).

Combineer je dit met de `dataviz`-skill, volg dan de methode daarvan, maar vervang het palet door de paletten uit `tokens.json` → `grafiek`.
