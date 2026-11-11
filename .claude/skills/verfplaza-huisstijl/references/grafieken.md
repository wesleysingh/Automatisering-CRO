# Grafieken in Verfplaza-stijl

## Paletten (uit tokens.json → `grafiek`)
- **Categorisch** (volgorde aanhouden): `#143D59` navy, `#F3B41A` geel, `#578AAC` blauw, `#11A24A` groen, `#BDD7E6` lichtblauw, `#919191` grijs. Zijn er meer dan 6 categorieën, groepeer de rest dan als "Overig" in grijs.
- **Sequentieel** (laag → hoog): `#E2EFF7` → `#BDD7E6` → `#578AAC` → `#1F3D57` → `#0C2636`.
- **Divergerend** (negatief → positief): `#E13522` → `#F4A397` → `#F3F3F3` → `#8FD1A7` → `#11A24A`.

## CRO-conventies (A/B-tests)
- **Controle = grijs `#919191`, variant = navy `#143D59`.** Bij meerdere varianten: navy, blauw `#578AAC`, lichtblauw `#BDD7E6`.
- **Uplift:** positief/significant winnend = groen `#11A24A`, negatief = rood `#E13522`, niet significant = grijs.
- **Highlight** (het ene getal waar het om draait): geel `#F3B41A`; de rest blijft navy of grijs.
- Betrouwbaarheidsintervallen: dezelfde kleur als de reeks, 25% dekking.

## Opmaak
- Font Roboto; titel 700 navy, links uitgelijnd; subtitel of as-labels 400 `#4B4B4B`.
- Witte achtergrond; alleen horizontale rasterlijnen `#E3E3E3`; geen boven- en rechteras; geen 3D, schaduw of verlopen.
- Directe labels bij lijnen en balken boven een legenda; percentages met komma ("12,4%"), want Nederlandse notatie.
- Bron/periode klein onderaan in `#919191`.

## Python
```python
import sys; sys.path.insert(0, ".claude/skills/verfplaza-huisstijl/scripts")
from verfplaza_style import apply_matplotlib, plotly_template, KLEUREN, CATEGORISCH

apply_matplotlib()                 # matplotlib: rcParams + Roboto (indien geïnstalleerd)
fig.update_layout(template=plotly_template())   # plotly
```
Is Roboto niet geïnstalleerd, dan valt matplotlib terug op Arial. Installeer Roboto voor exacte huisstijl (Google Fonts).

## HTML / artifacts
```css
:root{--vp-navy:#143D59;--vp-geel:#F3B41A;--vp-groen:#11A24A;--vp-rood:#E13522;
      --vp-blauw:#578AAC;--vp-blauw-zacht:#E2EFF7;--vp-grijs:#919191;--vp-rand:#E3E3E3;}
body{font-family:Roboto,Arial,sans-serif;color:var(--vp-navy);}
```
Google Fonts: `https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap`
