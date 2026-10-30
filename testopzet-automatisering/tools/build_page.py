"""Rendert de Confluence-pagina (storage format) uit de template."""

from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
TESTCODE = re.compile(r"^\s*([A-Za-z]{1,5})[\s-]?(\d{1,4})(?!\d)")  # "VP 012 - ..." -> ("VP", "012")


def testcode(titel: str) -> tuple[str, int] | None:
    match = TESTCODE.match(titel)
    return (match.group(1).upper(), int(match.group(2))) if match else None


def maak_testsegment(paginas: list[str], device: str | None) -> str:
    """'Alle bezoekers die de PDP bezoeken'; het device alleen noemen bij desktop of mobile."""
    if not paginas:
        return ""
    device = (device or "").strip().lower()
    bezoekers = f"Alle {device} bezoekers" if device in ("desktop", "mobile") else "Alle bezoekers"
    if any(p.strip().lower() == "alle" for p in paginas):
        return bezoekers
    return f"{bezoekers} die de {' of de '.join(paginas)} bezoeken"


def _link_eerste(html: str, titel: str, url: str) -> tuple[str, bool]:
    """Maakt de eerste vermelding van de test (volledige titel, anders de code) klikbaar."""
    patronen = [re.escape(str(escape(titel)))]
    code = testcode(titel)
    if code:
        patronen.append(rf"\b{code[0]}[\s-]?0*{code[1]}(?!\d)")
    for patroon in patronen:
        match = re.search(patroon, html, re.IGNORECASE)
        if match:
            link = f'<a href="{escape(url)}">{match.group(0)}</a>'
            return html[:match.start()] + link + html[match.end():], True
    return html, False


def aanleiding_html(tekst: str, vorige_testen: list[tuple[str, str]]) -> Markup:
    """Escapet de aanleiding, zet lege regels om in alinea's en linkt naar de vorige test(en)."""
    alineas = [str(escape(a.strip())) for a in re.split(r"\n\s*\n", tekst) if a.strip()]
    for titel, url in vorige_testen:
        for i, alinea in enumerate(alineas):
            alineas[i], gelinkt = _link_eerste(alinea, titel, url)
            if gelinkt:
                break
    return Markup("</p><p>".join(alineas))


def render(testopzet: dict, template: str = "testpagina.xml.j2", vorige_testen: list[tuple[str, str]] = (),
           testsegment: str = "") -> str:
    """`vorige_testen` = (paginatitel, url) van de vorige test(en), om in de aanleiding naar te linken."""
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(default=True, default_for_string=True),
        keep_trailing_newline=True,
    )
    context = {**testopzet, "aanleiding": aanleiding_html(testopzet["aanleiding"], list(vorige_testen)),
               "testsegment": testsegment}
    return env.get_template(template).render(**context)
