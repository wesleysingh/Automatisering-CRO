"""Verfplaza-huisstijl voor grafieken. Leest alle waarden uit ../tokens.json.

Gebruik:
    from verfplaza_style import apply_matplotlib, plotly_template
    apply_matplotlib()
    fig.update_layout(template=plotly_template())

`python verfplaza_style.py [uitvoer.png]` rendert een voorbeeldgrafiek.
"""
import json
from pathlib import Path

_TOKENS = json.loads((Path(__file__).resolve().parent.parent / "tokens.json").read_text())
KLEUREN = _TOKENS["kleuren"]
GRAFIEK = _TOKENS["grafiek"]
CATEGORISCH = GRAFIEK["categorisch"]
FONT = _TOKENS["typografie"]["font"]
FONT_STACK = [FONT, *_TOKENS["typografie"]["fallback"]]


def apply_matplotlib():
    """Zet matplotlib-rcParams op Verfplaza-stijl."""
    import matplotlib as mpl
    from cycler import cycler

    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": FONT_STACK + list(mpl.rcParams["font.sans-serif"]),
        "axes.prop_cycle": cycler(color=CATEGORISCH),
        "axes.edgecolor": GRAFIEK["rasterlijn"],
        "axes.labelcolor": GRAFIEK["as_tekst"],
        "axes.titlecolor": KLEUREN["navy"],
        "axes.titleweight": "bold",
        "axes.titlesize": 14,
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": GRAFIEK["rasterlijn"],
        "grid.linewidth": 0.8,
        "xtick.color": GRAFIEK["as_tekst"],
        "ytick.color": GRAFIEK["as_tekst"],
        "text.color": KLEUREN["navy"],
        "figure.facecolor": KLEUREN["wit"],
        "axes.facecolor": KLEUREN["wit"],
        "legend.frameon": False,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    })


def plotly_template():
    """Geeft een plotly-template in Verfplaza-stijl terug."""
    import plotly.graph_objects as go

    return go.layout.Template(layout=go.Layout(
        font=dict(family=", ".join(FONT_STACK), color=KLEUREN["navy"], size=13),
        title=dict(font=dict(size=18, color=KLEUREN["navy"]), x=0, xanchor="left"),
        colorway=CATEGORISCH,
        paper_bgcolor=KLEUREN["wit"],
        plot_bgcolor=KLEUREN["wit"],
        xaxis=dict(showgrid=False, linecolor=GRAFIEK["rasterlijn"], tickfont=dict(color=GRAFIEK["as_tekst"])),
        yaxis=dict(gridcolor=GRAFIEK["rasterlijn"], zeroline=False, tickfont=dict(color=GRAFIEK["as_tekst"])),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        colorscale=dict(sequential=GRAFIEK["sequentieel"], diverging=GRAFIEK["divergerend"]),
    ))


if __name__ == "__main__":
    import sys
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    apply_matplotlib()
    uit = sys.argv[1] if len(sys.argv) > 1 else "verfplaza_voorbeeld.png"
    devices = ["Mobiel", "Desktop", "Tablet"]
    controle, variant = [2.1, 3.4, 2.6], [2.4, 3.5, 2.9]
    x = range(len(devices))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([i - 0.2 for i in x], controle, 0.4, color=GRAFIEK["controle"], label="Controle")
    ax.bar([i + 0.2 for i in x], variant, 0.4, color=GRAFIEK["variant"], label="Variant")
    ax.set_xticks(list(x), devices)
    ax.set_ylabel("Conversieratio (%)")
    ax.set_title("Variant wint vooral op mobiel")
    ax.legend(loc="upper left")
    fig.savefig(uit)
    print(f"Voorbeeld opgeslagen: {uit}")
