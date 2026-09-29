"""Entrypoint: zoekt afgeronde 'Testopzet uitwerken'-subtaken en maakt de testpagina in Confluence.

Gebruik:
    python tools/poll_jira.py --all                        # alle klanten in clients/
    python tools/poll_jira.py --client verfplaza            # één klant
    python tools/poll_jira.py --client verfplaza --issue CRO-123 --dry-run
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR.parent / "shared" / "tools"))

from adf_to_text import adf_to_text, extract_urls, storage_to_text  # noqa: E402
from atlassian_client import AtlassianClient, AtlassianError  # noqa: E402
from build_page import render  # noqa: E402
from generate_testopzet import GeneratieFout, Invoer, genereer  # noqa: E402

log = logging.getLogger("testopzet")
CLIENTS_DIR = PROJECT_DIR / "clients"
TMP_DIR = PROJECT_DIR / ".tmp"
# Onzichtbare Jira-eigenschap waarin een mislukte poging wordt onthouden (geen labels nodig)
PROPERTY_KEY = "testopzet-automatisering"
SUBTAAK_VELDEN = ["summary", "parent", "statuscategorychangedate"]


@dataclass
class Klant:
    slug: str
    naam: str
    atlassian_url: str
    jira_project: str
    parent_page_id: str
    secrets_prefix: str = ""
    subtaak_naam: str = "Testopzet uitwerken"
    kpi_hypothese: str = "bestellingen"
    webshop_context: str = ""
    vanaf_datum: str = ""
    template: str = "testpagina.xml.j2"

    @classmethod
    def laad(cls, slug: str) -> "Klant":
        """Klant-yaml, aangevuld met de gedeelde standaarden uit clients/_standaard.yaml."""
        standaard = CLIENTS_DIR / "_standaard.yaml"
        data = (yaml.safe_load(standaard.read_text()) or {}) if standaard.exists() else {}
        data.update(yaml.safe_load((CLIENTS_DIR / f"{slug}.yaml").read_text()))
        data["parent_page_id"] = str(data["parent_page_id"])
        return cls(slug=slug, **data)


class Overslaan(Exception):
    """Subtaak kan (nog) niet verwerkt worden; reden gaat als commentaar naar Jira."""


class AlKlaar(Exception):
    """De Confluence-pagina bestaat al: subtaak is eerder verwerkt."""


def alle_klanten() -> list[str]:
    return sorted(p.stem for p in CLIENTS_DIR.glob("*.yaml") if not p.stem.startswith("_"))


def zoek_subtaken(jira: AtlassianClient, klant: Klant) -> list[dict]:
    jql = (
        f'project = "{klant.jira_project}" AND issuetype in subTaskIssueTypes() '
        f'AND summary ~ "\\"{klant.subtaak_naam}\\"" AND statusCategory = Done'
    )
    if klant.vanaf_datum:
        jql += f' AND statusCategoryChangedDate >= "{klant.vanaf_datum}"'
    issues = jira.search_issues(jql, fields=SUBTAAK_VELDEN)
    # `summary ~` is een fuzzy zoekopdracht; hier exact filteren
    return [i for i in issues if i["fields"]["summary"].strip().lower() == klant.subtaak_naam.lower()]


def _datum(waarde: str) -> datetime:
    """Parseert Jira-tijden ('2026-09-29T14:38:28.095+0200') en ISO-tijden."""
    try:
        return datetime.strptime(waarde, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        return datetime.fromisoformat(waarde)


def al_gemeld(fout_op: str | None, statuswijziging: str | None) -> bool:
    """True als de laatste fout ná de laatste keer 'Gereed' is gemeld; dan niet opnieuw proberen."""
    if not fout_op or not statuswijziging:
        return False
    return _datum(fout_op) >= _datum(statuswijziging)


def vind_idee(jira: AtlassianClient, subtaak: dict) -> dict:
    """Subtaak -> parent-taak -> gekoppeld Jira Product Discovery-idee (delivery-link)."""
    parent = subtaak["fields"]["parent"]
    taak = jira.get_issue(parent["key"], fields=["issuelinks"])
    for link in taak["fields"].get("issuelinks", []):
        gelinkt = link.get("inwardIssue") or link.get("outwardIssue")
        if not gelinkt:
            continue
        kandidaat = jira.get_issue(gelinkt["key"], fields=["summary", "description", "project"])
        if kandidaat["fields"]["project"].get("projectTypeKey") == "product_discovery":
            return kandidaat
    raise Overslaan(f"Geen Discovery-idee gevonden dat gekoppeld is aan {parent['key']}.")


def haal_vorige_testen(conf: AtlassianClient, omschrijving: str) -> list[tuple[str, str]]:
    """Leest Confluence-pagina's waarnaar in de idee-omschrijving gelinkt wordt."""
    host = conf.base_url.split("//", 1)[1]
    testen = []
    for url in extract_urls(omschrijving):
        if host not in url or "/wiki/" not in url:
            continue
        page_id = conf.resolve_page_id(url)
        if not page_id:
            log.warning("Kon geen pagina-ID halen uit %s", url)
            continue
        page = conf.get_page(page_id, body_format="storage")
        testen.append((page["title"], storage_to_text(page["body"]["storage"]["value"])))
    return testen


def verwerk(klant: Klant, atl: AtlassianClient, space_id: str, subtaak: dict, dry_run: bool) -> None:
    key = subtaak["key"]
    parent = subtaak["fields"].get("parent")
    if not parent:
        raise Overslaan("De subtaak heeft geen bovenliggende taak.")
    # Paginatitel = naam van de Jira-taak, bijv. "VP 016 - Afrekenknop bovenaan weghalen"
    titel = parent["fields"]["summary"].strip()
    if atl.find_page(space_id, titel):
        raise AlKlaar(titel)

    idee = vind_idee(atl, subtaak)
    omschrijving = adf_to_text(idee["fields"].get("description"))
    vorige = haal_vorige_testen(atl, omschrijving)
    log.info("%s: %s, idee %s, %d vorige test(en)", key, titel, idee["key"], len(vorige))

    testopzet = genereer(Invoer(
        test_titel=titel,
        idee_titel=idee["fields"]["summary"],
        idee_omschrijving=omschrijving,
        vorige_testen=vorige,
        webshop=klant.naam,
        webshop_context=klant.webshop_context,
        kpi=klant.kpi_hypothese,
    ))

    xml = render(testopzet, klant.template)

    if dry_run:
        TMP_DIR.mkdir(exist_ok=True)
        pad = TMP_DIR / f"{key}.xml"
        pad.write_text(xml)
        print(f"\n=== [dry-run] {titel} ===\n(opgeslagen in {pad})\n\n{xml}")
        return

    page = atl.create_page(space_id, klant.parent_page_id, titel, xml)
    url = atl.page_url(page)
    log.info("%s: pagina aangemaakt: %s", key, url)
    atl.add_comment(key, "Testopzet automatisch aangemaakt in Confluence:", (titel, url))
    atl.add_comment(idee["key"], "Testopzet aangemaakt:", (titel, url))


def verwerk_klant(slug: str, issue: str | None, dry_run: bool) -> int:
    klant = Klant.laad(slug)
    atl = AtlassianClient.from_env(klant.atlassian_url, klant.secrets_prefix)
    subtaken = [atl.get_issue(issue, fields=SUBTAAK_VELDEN)] if issue else zoek_subtaken(atl, klant)
    space_id = atl.get_space_id(klant.parent_page_id)
    log.info("%s: %d subtaak/subtaken te controleren", klant.naam, len(subtaken))

    fouten = 0
    for subtaak in subtaken:
        key = subtaak["key"]
        try:
            # Eerder mislukt en sindsdien niet opnieuw op Gereed gezet? Dan niet elke poll opnieuw proberen.
            # Met --issue wordt het altijd opnieuw geprobeerd.
            melding = atl.get_issue_property(key, PROPERTY_KEY) or {}
            if not issue and al_gemeld(melding.get("fout_op"), subtaak["fields"].get("statuscategorychangedate")):
                continue
            verwerk(klant, atl, space_id, subtaak, dry_run)
        except AlKlaar as e:
            log.info("%s: pagina \"%s\" bestaat al, overgeslagen", key, e)
        except (Overslaan, GeneratieFout) as e:
            fouten += 1
            log.error("%s: %s", key, e)
            if not dry_run:
                atl.set_issue_property(key, PROPERTY_KEY, {"fout_op": datetime.now(timezone.utc).isoformat(), "reden": str(e)})
                atl.add_comment(key, f"Testopzet kon niet automatisch worden aangemaakt: {e} "
                                     "Zet deze subtaak terug en opnieuw op Gereed om het opnieuw te proberen.")
        except AtlassianError as e:
            # Tijdelijke API-fout: niets onthouden, volgende poll probeert opnieuw
            fouten += 1
            log.error("%s: Atlassian-fout: %s", key, e)
    return fouten


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    groep = parser.add_mutually_exclusive_group(required=True)
    groep.add_argument("--client", help="klant-slug (bestandsnaam in clients/ zonder .yaml)")
    groep.add_argument("--all", action="store_true", help="alle klanten")
    parser.add_argument("--issue", help="verwerk alleen deze subtaak (bijv. CRO-123), ook als die al verwerkt is")
    parser.add_argument("--dry-run", action="store_true", help="niets schrijven naar Jira/Confluence")
    args = parser.parse_args()
    if args.issue and args.all:
        parser.error("--issue werkt alleen samen met --client")

    load_dotenv(PROJECT_DIR / ".env")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    fouten = 0
    for slug in [args.client] if args.client else alle_klanten():
        try:
            fouten += verwerk_klant(slug, args.issue, args.dry_run)
        except Exception:
            fouten += 1
            log.exception("%s: klant overgeslagen door onverwachte fout", slug)
    return 1 if fouten else 0


if __name__ == "__main__":
    sys.exit(main())
