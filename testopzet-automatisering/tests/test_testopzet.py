import json
from types import SimpleNamespace

import pytest

from adf_to_text import adf_to_text, extract_urls, storage_to_text
from build_page import maak_testsegment, render
from generate_testopzet import GeneratieFout, Invoer, genereer, normaliseer, system_prompt, valideer


def maak_testopzet(**overrides):
    data = {
        "aanleiding": "Uit VP 012 blijkt dat 30% van de mobiele bezoekers de leverdatum niet ziet.",
        "hypothese": {"als": "we de leverdatum bovenaan tonen", "dan": "stijgen de bestellingen", "omdat": "bezoekers meer zekerheid hebben"},
        "optimalisatiestrategie": {"naam": "Certainty", "toelichting": "Minder onzekerheid over levering."},
    }
    data.update(overrides)
    return data


# ------------------------------------------------------------------ validatie

def test_geldige_testopzet_heeft_geen_fouten():
    assert valideer(maak_testopzet(), heeft_vorige_test=True) == []


def test_te_lange_aanleiding():
    fouten = valideer(maak_testopzet(aanleiding="woord " * 151), heeft_vorige_test=False)
    assert any("151 woorden" in f for f in fouten)


@pytest.mark.parametrize("dash", ["—", "–"])
def test_dashes_niet_toegestaan(dash):
    data = maak_testopzet()
    data["optimalisatiestrategie"]["toelichting"] = f"Zekerheid {dash} vertrouwen"
    assert any("dashes" in f for f in valideer(data, heeft_vorige_test=True))


def test_te_lang_omdat_deel():
    data = maak_testopzet()
    data["hypothese"]["omdat"] = "reden " * 21
    assert any("omdat-deel" in f for f in valideer(data, heeft_vorige_test=True))


def test_boom_niet_in_aanleiding():
    fouten = valideer(maak_testopzet(aanleiding="Uit VP 012 blijkt dat de BOOM strategie werkt."), heeft_vorige_test=True)
    assert any("BOOM" in f for f in fouten)


def test_vervolgtest_moet_met_uit_beginnen():
    fouten = valideer(maak_testopzet(aanleiding="Vanuit theorie weten we dat..."), heeft_vorige_test=True)
    assert any('beginnen met "Uit' in f for f in fouten)
    assert valideer(maak_testopzet(aanleiding="Vanuit theorie weten we dat..."), heeft_vorige_test=False) == []


def test_normaliseer_haalt_sleutelwoorden_en_punten_weg():
    data = maak_testopzet()
    data["hypothese"] = {"als": "Als we X doen,", "dan": "dan stijgen de bestellingen", "omdat": "omdat Y."}
    data = normaliseer(data)
    assert data["hypothese"] == {"als": "we X doen", "dan": "stijgen de bestellingen", "omdat": "Y"}


def test_system_prompt_vult_kpi_in():
    prompt = system_prompt("purchasers")
    assert "dit is altijd purchasers" in prompt
    assert "{kpi}" not in prompt
    assert "Choice Architecture" in prompt


# ------------------------------------------------------------ genereer (mock)

class NepClient:
    def __init__(self, antwoorden):
        self.antwoorden = list(antwoorden)
        self.prompts = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.prompts.append(kwargs["messages"][0]["content"])
        blok = SimpleNamespace(type="text", text=json.dumps(self.antwoorden.pop(0)))
        return SimpleNamespace(stop_reason="end_turn", stop_details=None, content=[blok])


INVOER = Invoer("VP 015 - Leverdatum bovenaan", "Leverdatum", "Omschrijving", [("VP 012 - Leverdatum", "Inzichten...")], "VerfPlaza", "", "bestellingen")


def test_genereer_probeert_opnieuw_met_feedback():
    client = NepClient([maak_testopzet(aanleiding="Te lang " * 200), maak_testopzet()])
    assert genereer(INVOER, client)["aanleiding"].startswith("Uit VP 012")
    assert "voldeed niet" in client.prompts[1]


def test_genereer_faalt_na_twee_pogingen():
    slecht = maak_testopzet(aanleiding="Te lang " * 200)
    with pytest.raises(GeneratieFout):
        genereer(INVOER, NepClient([slecht, slecht]))


# ------------------------------------------------------------------- pagina

def test_render_bevat_onderdelen_en_escapet():
    data = maak_testopzet(aanleiding="Prijs < €50 & gratis verzending")
    xml = render(data)
    assert "Prijs &lt; €50 &amp; gratis verzending" in xml
    assert "H1: <strong>Als</strong> we de leverdatum bovenaan tonen, <strong>dan</strong> stijgen de bestellingen, " \
           "<strong>omdat</strong> bezoekers meer zekerheid hebben." in xml
    for kop in ["Pre-test", "Testsegment:", "MDE:", "Guardrail metric:", "Raportage", "Vervolgtest"]:
        assert kop in xml


def test_render_vaste_velden():
    xml = render(maak_testopzet(), testsegment="Alle bezoekers die de PDP bezoeken")
    for regel in ["Testsegment:</strong> Alle bezoekers die de PDP bezoeken", "Significantielevel:</strong> 80%",
                  "MDE:</strong> x% (x weken)", '<time datetime="2026-05-05" /> - <time datetime="2026-06-08" />',
                  "KPI:</strong> Purchasers", "Guardrail metric:</strong> AOV", "<li><p>Omzet</p></li>"]:
        assert regel in xml


def test_render_linkt_vorige_test_en_maakt_alineas():
    data = maak_testopzet(aanleiding="Uit VP 012 blijkt dat 30% het mist.\n\nVanuit theorie <weten> we meer.")
    xml = render(data, vorige_testen=[("VP 012 - Leverdatum in winkelmandje", "https://x/wiki/pages/1?a=1&b=2")])
    assert 'Uit <a href="https://x/wiki/pages/1?a=1&amp;b=2">VP 012</a> blijkt dat 30% het mist.</p>' \
           '<p>Vanuit theorie &lt;weten&gt; we meer.' in xml


def test_render_linkt_volledige_titel_als_die_er_staat():
    data = maak_testopzet(aanleiding="Uit VP 012 - Leverdatum in winkelmandje blijkt dat VP 012 werkt.")
    xml = render(data, vorige_testen=[("VP 012 - Leverdatum in winkelmandje", "https://x/1")])
    assert '<a href="https://x/1">VP 012 - Leverdatum in winkelmandje</a> blijkt dat VP 012 werkt.' in xml


@pytest.mark.parametrize("paginas, device, verwacht", [
    (["PDP"], "Alle", "Alle bezoekers die de PDP bezoeken"),
    (["PDP"], "Mobile", "Alle mobile bezoekers die de PDP bezoeken"),
    (["PDP", "Cart"], "Desktop", "Alle desktop bezoekers die de PDP of de Cart bezoeken"),
    (["Alle"], "Mobile", "Alle mobile bezoekers"),
    ([], "Mobile", ""),
])
def test_testsegment(paginas, device, verwacht):
    assert maak_testsegment(paginas, device) == verwacht


# ------------------------------------------------------------------ adf/tekst

def test_adf_to_text_met_links_en_lijsten():
    adf = {"type": "doc", "content": [
        {"type": "paragraph", "content": [
            {"type": "text", "text": "Zie "},
            {"type": "text", "text": "VP 012", "marks": [{"type": "link", "attrs": {"href": "https://x.atlassian.net/wiki/spaces/CRO/pages/123/VP+012"}}]},
        ]},
        {"type": "bulletList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Punt 1"}]}]},
        ]},
        {"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "https://x.atlassian.net/wiki/x/AbC"}}]},
    ]}
    tekst = adf_to_text(adf)
    assert "VP 012 (https://x.atlassian.net/wiki/spaces/CRO/pages/123/VP+012)" in tekst
    assert "- Punt 1" in tekst
    assert extract_urls(tekst) == ["https://x.atlassian.net/wiki/spaces/CRO/pages/123/VP+012", "https://x.atlassian.net/wiki/x/AbC"]


def test_storage_to_text():
    html = "<h2>Inzichten</h2><p>Mobile <strong>+1,85%</strong></p><ul><li>Punt</li></ul>"
    tekst = storage_to_text(html)
    assert "## Inzichten" in tekst and "Mobile +1,85%" in tekst and "- Punt" in tekst


# ------------------------------------------------------------------ klanten

def test_klant_krijgt_standaardwaarden():
    from poll_jira import Klant, alle_klanten
    klant = Klant.laad("verfplaza")
    assert klant.atlassian_url == "https://wesleysingh.atlassian.net"
    assert klant.secrets_prefix == ""
    assert klant.subtaak_naam == "Testopzet uitwerken"
    assert "_standaard" not in alle_klanten() and "_voorbeeld" not in alle_klanten()


def test_atlassian_credentials_uit_env(monkeypatch):
    from atlassian_client import AtlassianClient
    monkeypatch.setenv("ATLASSIAN_EMAIL", "a@b.nl")
    monkeypatch.setenv("ATLASSIAN_TOKEN", "t")
    assert AtlassianClient.from_env("https://x.atlassian.net").session.auth == ("a@b.nl", "t")


# --------------------------------------------------------- opnieuw proberen

def test_al_gemeld():
    from poll_jira import al_gemeld
    gereed = "2026-09-29T14:38:28.095+0200"          # Jira-formaat
    assert al_gemeld("2026-09-29T12:40:00+00:00", gereed)       # fout ná Gereed: niet opnieuw
    assert not al_gemeld("2026-09-29T12:00:00+00:00", gereed)   # opnieuw op Gereed gezet na de fout
    assert not al_gemeld(None, gereed)


# ------------------------------------------------------------ idee-velden en historie

def test_laatste_test():
    from poll_jira import laatste_test
    paginas = [
        {"id": "1", "parentId": "10", "title": "VP 017 - Prijs per liter"},
        {"id": "2", "parentId": "10", "title": "VP 016 - Afrekenknop"},
        {"id": "3", "parentId": "10", "title": "Backlog"},
        {"id": "4", "parentId": 10, "title": "VP 018 - Roerstokje"},
        {"id": "5", "parentId": "99", "title": "VP 050 - Ergens anders"},
        {"id": "6", "parentId": "10", "title": "AB 060 - Andere klantcode"},
    ]
    assert laatste_test(paginas, "10", "VP 019 - Nieuw")["id"] == "4"
    assert laatste_test(paginas, "10", "VP 018 - Roerstokje")["id"] == "1"
    assert laatste_test([], "10", "VP 019 - Nieuw") is None

def test_veldwaarden_op_naam():
    from poll_jira import veldwaarden
    idee = {"names": {"customfield_1": "Pagina", "customfield_2": "Devices"},
            "fields": {"customfield_1": [{"value": "PDP"}, {"value": "Cart"}], "customfield_2": {"value": "Mobile"}}}
    assert veldwaarden(idee, "Pagina") == ["PDP", "Cart"]
    assert veldwaarden(idee, "Device", "Devices") == ["Mobile"]
    assert veldwaarden(idee, "Onbekend") == []


def test_genoemde_testen():
    from poll_jira import genoemde_testen
    paginas = [{"id": str(i), "title": t} for i, t in enumerate([
        "VP 012 - Leverdatum in winkelmandje", "VP 014 - Leverdatum in winkelmandje (vervolgtest)",
        "VP 003 - Weghalen omschrijving kleuren PDP", "VP 016 - Afrekenknop bovenaan weghalen", "Template"])]
    titels = lambda tekst: [p["title"] for p in genoemde_testen(paginas, "VP 016 - Afrekenknop bovenaan weghalen", tekst)]
    assert titels("Zie VP003, en VP 16 zelf") == ["VP 003 - Weghalen omschrijving kleuren PDP"]
    assert titels("Net als bij de leverdatum in winkelmandje test") == ["VP 014 - Leverdatum in winkelmandje (vervolgtest)"]
    assert titels("VP 0123 en VP 1") == []
