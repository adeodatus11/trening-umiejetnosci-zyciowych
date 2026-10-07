#!/usr/bin/env python3
"""Wstawia pasek logotypów (TUZ, COVE Polska, WIN4SMEs, UE) do wersji do druku.

Skrypt jest idempotentny: bloki oznaczone komentarzami BRAND są usuwane
i wstawiane od nowa przy każdym uruchomieniu.

Użycie: python3 narzedzia/branding.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Pliki do druku i ich klasa „strony” (każda sekcja = jedna kartka A4).
TARGETS = sorted(
    list((ROOT / "materialy" / "druk").glob("*.html"))
    + list((ROOT / "materialy" / "arkusze").glob("*.html"))
    + list((ROOT / "materialy" / "ankiety").glob("*.html"))
    + [ROOT / "materialy" / "specyfikacja-grafik-dobowy.html"]
)

DISCLAIMER = (
    "Dofinansowane przez Unię Europejską. Poglądy i opinie wyrażone są jednak wyłącznie "
    "poglądami autora lub autorów i niekoniecznie odzwierciedlają poglądy Unii Europejskiej "
    "lub Europejskiej Agencji Wykonawczej ds. Edukacji i Kultury (EACEA). Unia Europejska "
    "ani EACEA nie ponoszą za nie odpowiedzialności."
)

LICENSE = "Materiał udostępniony na licencji CC BY 4.0 (creativecommons.org/licenses/by/4.0/deed.pl)."

CSS = """<style id="brand-css">/* BRAND */
.brand-strip{display:flex;align-items:center;justify-content:space-between;gap:6mm;padding:0 0 2mm;margin:0 0 3.5mm;border-bottom:1px solid #b9c6cc;break-inside:avoid;break-after:avoid}
.brand-strip img{display:block;width:auto;max-width:none;object-fit:contain}
.brand-strip .b-tuz{height:11mm}.brand-strip .b-cove{height:7mm}.brand-strip .b-win{height:10mm}.brand-strip .b-eu{height:7mm}
.brand-note{margin:3mm 0 0;padding-top:1.5mm;border-top:1px solid #d3dbdf;font-size:7pt;line-height:1.25;color:#46616b;break-inside:avoid}
@media print{.brand-strip,.brand-note{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
@media screen and (max-width:600px){.brand-strip{gap:3mm}.brand-strip .b-tuz{height:10mm}.brand-strip .b-cove{height:6mm}.brand-strip .b-win{height:9mm}.brand-strip .b-eu{height:6mm}}
</style>"""


def strip_html(prefix):
    a = prefix + "asets/druk/"
    return (
        "<!-- BRAND:START -->"
        '<div class="brand-strip" role="img" aria-label="Logotypy: Trening Umiejętności Życiowych, '
        'COVE Polska, WIN4SMEs, Dofinansowane przez Unię Europejską">'
        f'<img class="b-tuz" src="{a}tuz.png" alt="">'
        f'<img class="b-cove" src="{a}cove-polska.png" alt="">'
        f'<img class="b-win" src="{a}win4smes.png" alt="">'
        f'<img class="b-eu" src="{a}eu-dofinansowanie.png" alt="">'
        "</div><!-- BRAND:END -->"
    )


NOTE = f'<!-- BRAND:START --><p class="brand-note">{DISCLAIMER} {LICENSE}</p><!-- BRAND:END -->'

SECTION_RE = re.compile(r'(<(?:section|main) class="(?:sheet|page)\b[^"]*"[^>]*>)')


def brand(path):
    html = path.read_text(encoding="utf-8")
    html = re.sub(r"<!-- BRAND:START -->.*?<!-- BRAND:END -->", "", html, flags=re.S)
    html = re.sub(r'<style id="brand-css">.*?</style>', "", html, flags=re.S)
    depth = len(path.relative_to(ROOT).parts) - 1
    prefix = "../" * depth
    html = html.replace("</head>", CSS + "</head>", 1)
    html, n = SECTION_RE.subn(lambda m: m.group(1) + strip_html(prefix), html)
    if not n:
        raise SystemExit(f"Brak sekcji sheet/page w {path}")
    # Klauzula UE na końcu ostatniej kartki.
    tag = "section" if "<section class=" in html else "main"
    idx = html.rfind(f"</{tag}>")
    last = html[:idx]
    fpos = last.rfind("<footer")
    if fpos > last.rfind(f"<{tag}"):
        html = html[:fpos] + NOTE + html[fpos:]
    else:
        html = html[:idx] + NOTE + html[idx:]
    path.write_text(html, encoding="utf-8")
    return n


SITE_PAGES = sorted(ROOT.glob("*.html"))


def brand_site(path):
    """Strony serwisu: pasek logotypów i klauzula UE widoczne tylko na wydruku."""
    html = path.read_text(encoding="utf-8")
    html = re.sub(r"<!-- BRAND:START -->.*?<!-- BRAND:END -->", "", html, flags=re.S)
    block = strip_html("").replace('class="brand-strip"', 'class="brand-strip print-only"')
    note = NOTE.replace('class="brand-note"', 'class="brand-note print-only"')
    html = html.replace('<main id="main">', '<main id="main">' + block, 1)
    html = html.replace("</main>", note + "</main>", 1)
    path.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    for p in SITE_PAGES:
        brand_site(p)
    for p in TARGETS:
        print(f"{p.relative_to(ROOT)}: {brand(p)} kartek")
