# Presentaties en documenten in huisstijl Wesley Singh

## Slide-opbouw (16:9)
| Type | Achtergrond | Tekst | Details |
|---|---|---|---|
| **Titelslide** | Donkerblauw `#275773` | Wit, titel Open Sans 700 ±40pt | Teal balk (`#33998B`, ±6pt hoog) onder de titel; logo rechtsboven op een wit afgerond vlak |
| **Sectieslide** | Lichtteal `#BCE2DC` | Inkt `#0E201E`, 32pt | Klein label in hoofdletters boven de titel in `#2A7E73` |
| **Inhoudsslide** | Wit | Titel `#0E201E` 700 28pt, tekst `#333333` 16–18pt | Logo klein rechtsonder; dunne teal lijn onder de titel |
| **KPI-slide** | Wit | Grote getallen `#275773` 700 48pt | Uplift teal `#33998B` (▲) of rood `#C8553D` (▼); 2–4 tegels op `#F5F5F5`, radius 8px |
| **Conclusie** | Donkerblauw | Wit | Belangrijkste les in lichtteal `#80C7BD` |

Regels: maximaal één kernboodschap per slide, de titel is een conclusie ("Variant B verhoogt conversie met 6,2%") en geen onderwerp ("Resultaten"). Linkermarge 0,6 inch. Voor klantrapportages zet je de klantnaam in de titel of subtitel; de vormgeving blijft in deze huisstijl.

## python-pptx
```python
from pptx.dml.color import RGBColor
TEAL, BLAUW, INKT, ROOD = RGBColor(0x33,0x99,0x8B), RGBColor(0x27,0x57,0x73), RGBColor(0x0E,0x20,0x1E), RGBColor(0xC8,0x55,0x3D)
run.font.name = "Open Sans"; run.font.color.rgb = INKT
slide.shapes.add_picture(".claude/skills/wesley-singh-huisstijl/assets/logo.png", left, top, width=Inches(2.4))
```

## Word / PDF / HTML-rapport
- Kop 1: Open Sans 700, 24pt, `#0E201E`. Kop 2: 700, 16pt, `#275773`. Tekst: 400, 11pt, `#333333`, regelhoogte 1,6.
- Callout/samenvatting: vlak `#E6F4F1` met links een teal rand van 4px.
- Tabellen: kopregel `#275773` met witte tekst, rijen afwisselend wit en `#F5F5F5`, randen `#EAEAEA`.
- Positief/negatief in tabellen: teal of rood tekst, geen gekleurde celvullingen.
- Logo linksboven in de koptekst, ±5 cm breed.

## Toon
Direct, no-nonsense en datagedreven; je/jij, actief, kort. Onderbouw elke conclusie met data ("van aannames naar inzichten"). Getallen in Nederlandse notatie (1.234; 12,4%).
