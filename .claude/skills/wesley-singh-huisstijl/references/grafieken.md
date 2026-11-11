# Grafieken in huisstijl Wesley Singh

## Paletten (uit tokens.json → `grafiek`)
- **Categorisch** (volgorde aanhouden): `#275773` donkerblauw, `#33998B` teal, `#80C7BD` lichtteal, `#0E201E` inkt, `#347499` blauw, `#9AA5A3` grijs. Zijn er meer dan 6 categorieën, groepeer de rest dan als "Overig" in grijs.
- **Sequentieel** (laag → hoog): `#E6F4F1` → `#BCE2DC` → `#80C7BD` → `#33998B` → `#206057`.
- **Divergerend** (negatief → positief): `#C8553D` → `#E5A898` → `#F5F5F5` → `#80C7BD` → `#206057`.

## CRO-conventies (A/B-tests)
- **Controle = grijs `#9AA5A3`, variant = donkerblauw `#275773`.** Bij meerdere varianten: `#275773`, `#347499`, `#80C7BD`.
- **Uplift:** positief/significant winnend = teal `#33998B`, negatief = rood `#C8553D`, niet significant = grijs.
- **Highlight** (het ene getal waar het om draait): teal `#33998B`; de rest blijft donkerblauw of grijs.
- Betrouwbaarheidsintervallen: dezelfde kleur als de reeks, 25% dekking.

## Opmaak
- Font Open Sans; titel 700 in `#0E201E`, links uitgelijnd en geformuleerd als conclusie; as-labels 400 `#5B6664`.
- Witte achtergrond; alleen horizontale rasterlijnen `#EAEAEA`; geen boven- en rechteras; geen 3D, schaduw of verlopen.
- Directe labels bij lijnen en balken boven een legenda; Nederlandse notatie ("12,4%", "1.234").
- Bron/periode klein onderaan in `#9AA5A3`.

## Python
```python
import sys; sys.path.insert(0, ".claude/skills/wesley-singh-huisstijl/scripts")
from huisstijl import apply_matplotlib, plotly_template, KLEUREN, GRAFIEK, CATEGORISCH

apply_matplotlib()                               # matplotlib
fig.update_layout(template=plotly_template())    # plotly
```
Is Open Sans niet geïnstalleerd, dan valt matplotlib terug op Arial. Installeer Open Sans (Google Fonts) voor de exacte huisstijl.

## HTML / artifacts
```css
:root{--ws-teal:#33998B;--ws-blauw:#275773;--ws-teal-licht:#80C7BD;--ws-teal-zacht:#BCE2DC;
      --ws-inkt:#0E201E;--ws-tekst:#333333;--ws-rood:#C8553D;--ws-grijs:#9AA5A3;--ws-rand:#EAEAEA;}
body{font-family:"Open Sans",Arial,sans-serif;color:var(--ws-tekst);}
h1,h2,h3{color:var(--ws-inkt);font-weight:700;}
```
Google Fonts: `https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap`
