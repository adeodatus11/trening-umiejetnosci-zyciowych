#!/usr/bin/env python3
"""Podmienia rząd logotypów na kartach „Grafik Dobowy” na: TUZ, COVE Polska, WIN4SMEs, UE.

Źródło: narzedzia/zrodla/grafik-dobowy-karty.pdf (oryginał z 3 logotypami na karcie).
Wynik:  materialy/pdf/grafik-dobowy-karty.pdf
"""
import io
import pathlib

import sys

import pypdfium2 as pdfium
from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "narzedzia" / "zrodla" / "grafik-dobowy-karty.pdf"
DST = ROOT / "materialy" / "pdf" / "grafik-dobowy-karty.pdf"
A = ROOT / "asets" / "druk"
sys.path.insert(0, str(ROOT / "narzedzia"))
from branding import DISCLAIMER, LICENSE  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.lib.utils import simpleSplit  # noqa: E402
# (plik, wysokość w pt)
LOGOS = [("tuz.png", 28), ("cove-polska.png", 15), ("win4smes.png", 26), ("eu-dofinansowanie.png", 13)]
GAP = 8


def logo_rows(page):
    """Grupuje obrazy w trójki (rząd logotypów na karcie) i zwraca ich obrys."""
    boxes = sorted(
        (o.get_bounds() for o in page.get_objects() if o.type == pdfium.raw.FPDF_PAGEOBJ_IMAGE),
        key=lambda b: (-round(b[1] / 20), b[0]),
    )
    rows = []
    for b in boxes:
        for r in rows:
            if abs(r[1] - b[1]) < 15 and b[0] - r[2] < 20:
                r[:] = [min(r[0], b[0]), min(r[1], b[1]), max(r[2], b[2]), max(r[3], b[3])]
                break
        else:
            rows.append(list(b))
    return rows


FONT = "Helvetica"
for _p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans.ttf"):
    if pathlib.Path(_p).exists():
        pdfmetrics.registerFont(TTFont("DejaVuSans", _p))
        FONT = "DejaVuSans"
        break


def main():
    reader = PdfReader(SRC)
    pdf = pdfium.PdfDocument(str(SRC))
    writer = PdfWriter()
    imgs = [(ImageReader(str(A / f)), h) for f, h in LOGOS]
    for i, page in enumerate(reader.pages):
        w, h = float(page.mediabox.width), float(page.mediabox.height)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(w, h))
        for x0, y0, x1, y1 in logo_rows(pdf[i]):
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            c.setFillColorRGB(1, 1, 1)
            c.rect(x0 - 1.5, y0 - 1.5, x1 - x0 + 3, y1 - y0 + 3, stroke=0, fill=1)
            sizes = [(img, ih * img.getSize()[0] / img.getSize()[1], ih) for img, ih in imgs]
            total = sum(s[1] for s in sizes) + GAP * (len(sizes) - 1)
            x = cx - total / 2
            for img, iw, ih in sizes:
                c.drawImage(img, x, cy - ih / 2, iw, ih, mask="auto")
                x += iw + GAP
        # Klauzula UE w dolnym marginesie strony.
        c.setFillColorRGB(0.27, 0.38, 0.42)
        c.setFont(FONT, 5.5)
        lines = simpleSplit(f"{DISCLAIMER} {LICENSE}", FONT, 5.5, w - 100)
        for k, line in enumerate(lines):
            c.drawCentredString(w / 2, 30 - k * 7, line)
        c.save()
        buf.seek(0)
        page.merge_page(PdfReader(buf).pages[0])
        writer.add_page(page)
    writer.add_metadata(reader.metadata or {})
    with open(DST, "wb") as f:
        writer.write(f)
    print(DST)


if __name__ == "__main__":
    main()
