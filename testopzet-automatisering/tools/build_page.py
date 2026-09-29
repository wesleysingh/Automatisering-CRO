"""Rendert de Confluence-pagina (storage format) uit de template."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def render(testopzet: dict, template: str = "testpagina.xml.j2") -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(default=True, default_for_string=True),
        keep_trailing_newline=True,
    )
    return env.get_template(template).render(**testopzet)
