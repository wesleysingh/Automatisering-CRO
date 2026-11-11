---
name: wesley-singh-huisstijl
description: Huisstijl van Wesley Singh (conversiespecialist): teal/donkerblauw, Open Sans, logo, tone of voice. Gebruik bij elke grafiek, chart, plot, presentatie, slide deck, PowerPoint, Word/PDF-document, CRO-rapportage, analyse of HTML-pagina die Wesley maakt, ook als die voor een klant is, en ook als de huisstijl niet expliciet genoemd wordt. Gebruik géén klantbranding, tenzij daar expliciet om gevraagd wordt.
---

# Huisstijl Wesley Singh

Bron: wesleysingh.nl (CSS + logo). Alle waarden staan in [tokens.json](tokens.json); dat is de enige bron van waarheid, dus neem kleuren daaruit over en verzin geen eigen kleuren. Ook rapporten voor klanten krijgen deze huisstijl: de klantnaam staat in de tekst, niet in de vormgeving.

## Kern in één oogopslag

| Rol | Kleur | Hex |
|---|---|---|
| Primair (accenten, highlights, positief) | Teal | `#33998B` |
| Actie / donkere vlakken / variant | Donkerblauw | `#275773` |
| Secundair vlak | Lichtteal | `#80C7BD` / zacht `#BCE2DC` |
| Koppen | Inkt | `#0E201E` |
| Lopende tekst | Antraciet | `#333333` |
| Negatief / verliezer (aanvulling) | Rood | `#C8553D` |
| Neutraal / controle | Grijs | `#9AA5A3` |

- **Font:** Open Sans (400 tekst, 600 medium, 700 koppen); fallback Arial.
- **Vorm:** afgeronde hoeken (4–8 px), veel wit, rustig. Knoppen donkerblauw met een harde schaduw `0 2px 0 0 #0B181F`; geen verlopen.
- **Logo:** [assets/logo.png](assets/logo.png) (beeldmerk + "WESLEY SINGH" + tagline "van aannames naar inzichten"), transparant, 501×151 px. Plaats het op wit of een licht vlak (op donkerblauw komt het teal te weinig uit, dus gebruik daar een wit afgerond vlak). Niet vergroten boven ±500 px breed (±6 cm in print), anders wordt het onscherp.
- **Tone of voice:** direct, no-nonsense en datagedreven. Spreek aan met **je/jouw**. Kernbelofte: *van aannames naar inzichten*. Formuleer concreet en resultaatgericht (conversie, omzet), zonder vakjargon of overdrijving.

## Per outputtype
- **Grafieken** (matplotlib, plotly, charts in artifacts) → lees [references/grafieken.md](references/grafieken.md). Python: `scripts/huisstijl.py` (`apply_matplotlib()`, `plotly_template()`).
- **Presentaties en documenten** (pptx, docx, pdf, HTML-rapport) → lees [references/presentaties.md](references/presentaties.md).

Combineer je dit met de `dataviz`-skill, volg dan de methode daarvan, maar vervang het palet door de paletten uit `tokens.json` → `grafiek`.
