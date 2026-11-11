# Presentaties en documenten in Verfplaza-stijl

## Slide-opbouw (16:9)
| Type | Achtergrond | Tekst | Details |
|---|---|---|---|
| **Titelslide** | Navy `#143D59` | Wit, titel Roboto 700 ±40pt | Gele balk (`#F3B41A`, ±6pt hoog) onder de titel; logo rechtsboven op een wit afgerond vlak, of het logo weglaten |
| **Sectieslide** | Lichtblauw `#E2EFF7` | Navy, 32pt | Klein geel label boven de titel (bijv. "TESTRESULTAAT") |
| **Inhoudsslide** | Wit | Titel navy 700 28pt, tekst `#373737` 16–18pt | Logo klein rechtsonder; dunne navy lijn onder de titel optioneel |
| **KPI-slide** | Wit | Grote getallen navy 700 48pt | Uplift groen `#11A24A` (▲) of rood `#E13522` (▼); 2–4 KPI-tegels op `#F7F7F7` met radius 8px |
| **Conclusie** | Navy | Wit | Belangrijkste les in geel `#F3B41A` |

Regels: maximaal één kernboodschap per slide, de titel is een conclusie ("Variant B verhoogt conversie met 6,2%") en geen onderwerp ("Resultaten"). Linkermarge 0,6 inch.

## python-pptx
```python
from pptx.dml.color import RGBColor
NAVY, GEEL, GROEN, ROOD = RGBColor(0x14,0x3D,0x59), RGBColor(0xF3,0xB4,0x1A), RGBColor(0x11,0xA2,0x4A), RGBColor(0xE1,0x35,0x22)
run.font.name = "Roboto"; run.font.color.rgb = NAVY
```
Logo: [../assets/logo.svg](../assets/logo.svg). python-pptx ondersteunt geen SVG, dus zet het eerst om naar PNG (bijv. `rsvg-convert -w 600 logo.svg > logo.png`, of cairosvg).

## Word / PDF / HTML-rapport
- Kop 1: Roboto 700, 24pt, navy. Kop 2: 700, 16pt, navy. Tekst: 400, 11pt, `#373737`, regelhoogte 1,5.
- Callout/samenvatting: vlak `#E2EFF7` met links een navy rand van 4px.
- Tabellen: kopregel navy met witte tekst, rijen afwisselend wit en `#F7F7F7`, randen `#E3E3E3`.
- Positief/negatief in tabellen: groen/rood tekst, geen gekleurde celvullingen.
- Logo bovenaan links in de koptekst, ±4 cm breed.

## Toon
Schrijf voor het Verfplaza-team zakelijk maar informeel: je/jij, actief, kort. Getallen in Nederlandse notatie (1.234; 12,4%).
