"""Zet Atlassian Document Format (Jira-omschrijvingen) en Confluence storage-HTML om naar leesbare tekst."""

from __future__ import annotations

import re
from html.parser import HTMLParser

_BLOCKS = {"paragraph", "heading", "blockquote", "codeBlock", "panel", "tableRow", "rule"}


def adf_to_text(node: dict | list | None) -> str:
    """Converteert een ADF-document naar platte tekst met markdown-achtige lijsten en links."""
    if not node:
        return ""
    text = _render(node, depth=0)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _render(node, depth: int) -> str:
    if isinstance(node, list):
        return "".join(_render(n, depth) for n in node)

    ntype = node.get("type")
    attrs = node.get("attrs") or {}
    children = node.get("content") or []

    if ntype == "text":
        text = node.get("text", "")
        for mark in node.get("marks") or []:
            href = (mark.get("attrs") or {}).get("href")
            if mark.get("type") == "link" and href and href != text:
                text = f"{text} ({href})"
        return text
    if ntype in ("inlineCard", "blockCard", "embedCard"):
        return attrs.get("url", "") + ("\n" if ntype != "inlineCard" else "")
    if ntype == "hardBreak":
        return "\n"
    if ntype == "mention":
        return attrs.get("text", "")
    if ntype == "emoji":
        return attrs.get("text") or attrs.get("shortName", "")
    if ntype == "status":
        return attrs.get("text", "")
    if ntype == "date":
        return attrs.get("timestamp", "")
    if ntype in ("bulletList", "orderedList"):
        lines = []
        for i, item in enumerate(children, start=1):
            bullet = f"{i}." if ntype == "orderedList" else "-"
            body = _render(item.get("content") or [], depth + 1).strip()
            lines.append("  " * depth + f"{bullet} {body}")
        return "\n".join(lines) + "\n"
    if ntype == "heading":
        return "#" * attrs.get("level", 1) + " " + _render(children, depth).strip() + "\n\n"
    if ntype == "tableCell" or ntype == "tableHeader":
        return _render(children, depth).strip() + " | "
    if ntype == "media" or ntype == "mediaSingle" or ntype == "mediaGroup":
        return "[afbeelding]\n" if ntype != "media" else ""

    inner = _render(children, depth)
    if ntype in _BLOCKS:
        return inner.rstrip() + "\n\n"
    return inner


class _HTMLText(HTMLParser):
    _BREAKS = {"p", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "div", "table"}

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.parts.append("\n" + "#" * int(tag[1]) + " ")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag in ("td", "th"):
            self.parts.append(" | ")

    def handle_endtag(self, tag):
        if tag in self._BREAKS:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)


def storage_to_text(html: str) -> str:
    """Converteert Confluence storage-format (XHTML) naar platte tekst."""
    parser = _HTMLText()
    parser.feed(html or "")
    text = "".join(parser.parts)
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def extract_urls(text: str) -> list[str]:
    """Alle unieke URL's in volgorde van voorkomen."""
    seen: list[str] = []
    for url in re.findall(r"https?://[^\s)\]>\"']+", text):
        url = url.rstrip(".,;")
        if url not in seen:
            seen.append(url)
    return seen
