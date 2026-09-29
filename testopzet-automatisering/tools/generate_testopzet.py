"""Genereert de testopzet (aanleiding, hypothese, strategie, principe) met de Claude API."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import anthropic

MODEL = "claude-opus-5-5"
KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
STRATEGIEEN = ["Ability", "Attention", "Motivation", "Certainty", "Choice Architecture"]
MAX_WOORDEN_AANLEIDING = 150

_TOELICHTING = {
    "type": "object",
    "properties": {"naam": {"type": "string"}, "toelichting": {"type": "string"}},
    "required": ["naam", "toelichting"],
    "additionalProperties": False,
}

SCHEMA = {
    "type": "object",
    "properties": {
        "aanleiding": {"type": "string"},
        "hypothese": {
            "type": "object",
            "description": "Alleen de tekst ná de woorden als/dan/omdat, zonder die woorden zelf",
            "properties": {"als": {"type": "string"}, "dan": {"type": "string"}, "omdat": {"type": "string"}},
            "required": ["als", "dan", "omdat"],
            "additionalProperties": False,
        },
        "optimalisatiestrategie": {
            **_TOELICHTING,
            "properties": {"naam": {"type": "string", "enum": STRATEGIEEN}, "toelichting": {"type": "string"}},
        },
        "psychologisch_principe": {
            **_TOELICHTING,
            "properties": {
                "naam": {"type": "string", "description": "Engelse term, bijv. Risk Aversion"},
                "toelichting": {"type": "string"},
            },
        },
    },
    "required": ["aanleiding", "hypothese", "optimalisatiestrategie", "psychologisch_principe"],
    "additionalProperties": False,
}


class GeneratieFout(RuntimeError):
    pass


@dataclass
class Invoer:
    test_titel: str  # naam van de Jira-taak, bijv. "VP 016 - Afrekenknop bovenaan weghalen"
    idee_titel: str
    idee_omschrijving: str
    vorige_testen: list[tuple[str, str]]  # (paginatitel, paginatekst)
    webshop: str
    webshop_context: str
    kpi: str


def system_prompt(kpi: str) -> str:
    """Stabiel per klant-KPI, zodat prompt caching werkt."""
    instructies = (KNOWLEDGE_DIR / "instructies.md").read_text().replace("{kpi}", kpi)
    return "\n\n".join([
        "Je bent een CRO-specialist die A/B-testopzetten schrijft voor webshops. "
        "Je ontvangt een globaal testidee uit Jira en eventueel de Confluence-pagina van een vorige test. "
        "Schrijf in het Nederlands, volg de instructies exact en lever de onderdelen aan in het gevraagde JSON-formaat.",
        instructies,
        (KNOWLEDGE_DIR / "boom_strategie.md").read_text(),
        (KNOWLEDGE_DIR / "voorbeeld_testopzet.md").read_text(),
    ])


def user_prompt(invoer: Invoer, feedback: list[str] | None = None) -> str:
    delen = [f"Webshop: {invoer.webshop}"]
    if invoer.webshop_context:
        delen.append(f"Over de webshop: {invoer.webshop_context}")
    delen.append(f"# Test: {invoer.test_titel}\n\nIdee: {invoer.idee_titel}\n\n{invoer.idee_omschrijving or '(geen omschrijving)'}")
    if invoer.vorige_testen:
        for titel, tekst in invoer.vorige_testen:
            delen.append(f"# Vorige test: {titel}\n\n{tekst}")
        delen.append(
            "Dit is een vervolgtest. Begin de aanleiding met \"Uit <code en naam vorige test> blijkt dat\" "
            "en gebruik de belangrijkste inzichten uit de vorige test."
        )
    else:
        delen.append("Er is geen vorige test bijgevoegd.")
    if feedback:
        delen.append("Je vorige poging voldeed niet aan deze eisen, los ze op:\n- " + "\n- ".join(feedback))
    return "\n\n".join(delen)


def valideer(data: dict, heeft_vorige_test: bool) -> list[str]:
    """Deterministische controles op de regels uit de instructies."""
    fouten = []
    woorden = len(data["aanleiding"].split())
    if woorden > MAX_WOORDEN_AANLEIDING:
        fouten.append(f"De aanleiding heeft {woorden} woorden, maximaal {MAX_WOORDEN_AANLEIDING}.")
    alle_tekst = json.dumps(data, ensure_ascii=False)
    if re.search(r"[—–]", alle_tekst):
        fouten.append("Gebruik geen m-dashes of en-dashes (— of –).")
    if re.search(r"\bBOOM\b", data["aanleiding"], re.IGNORECASE):
        fouten.append('Het woord "BOOM" mag niet in de aanleiding staan.')
    if heeft_vorige_test and not data["aanleiding"].strip().startswith("Uit "):
        fouten.append('De aanleiding moet beginnen met "Uit <vorige test> blijkt dat".')
    if data["optimalisatiestrategie"]["naam"] not in STRATEGIEEN:
        fouten.append(f"Optimalisatiestrategie moet een van {', '.join(STRATEGIEEN)} zijn.")
    return fouten


def normaliseer(data: dict) -> dict:
    """Haalt dubbele sleutelwoorden en eindleestekens weg, zodat de template 'Als …, dan …, omdat ….' klopt."""
    h = data["hypothese"]
    for sleutel in ("als", "dan", "omdat"):
        tekst = h[sleutel].strip()
        tekst = re.sub(rf"^{sleutel}\b[\s,:]*", "", tekst, flags=re.IGNORECASE)
        h[sleutel] = tekst.rstrip(" .,;")
    return data


def _vraag_claude(client: anthropic.Anthropic, system: str, prompt: str) -> dict:
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        output_config={"effort": "high", "format": {"type": "json_schema", "schema": SCHEMA}},
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": prompt}],
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if response.stop_reason == "refusal":
        raise GeneratieFout(f"Claude weigerde de aanvraag: {response.stop_details}")
    if response.stop_reason == "max_tokens":
        raise GeneratieFout("Antwoord afgekapt (max_tokens bereikt).")
    tekst = next(b.text for b in response.content if b.type == "text")
    return json.loads(tekst)


def genereer(invoer: Invoer, client: anthropic.Anthropic | None = None) -> dict:
    """Genereert en valideert de testopzet; bij fouten volgt één nieuwe poging met feedback."""
    client = client or anthropic.Anthropic()
    system = system_prompt(invoer.kpi)
    heeft_vorige = bool(invoer.vorige_testen)

    data = normaliseer(_vraag_claude(client, system, user_prompt(invoer)))
    fouten = valideer(data, heeft_vorige)
    if fouten:
        data = normaliseer(_vraag_claude(client, system, user_prompt(invoer, feedback=fouten)))
        fouten = valideer(data, heeft_vorige)
    if fouten:
        raise GeneratieFout("Testopzet voldoet na 2 pogingen niet: " + " ".join(fouten))
    return data
