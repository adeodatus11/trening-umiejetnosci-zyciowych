#!/usr/bin/env python3
"""Łączy PDF-y w „cały program” i buduje pakiet ZIP z materiałami do druku."""
import pathlib
import zipfile

from pypdf import PdfWriter

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "materialy" / "pdf"

PROGRAM = ["przewodnik-prowadzacego.pdf"] + [f"scenariusz-modul-{i}.pdf" for i in range(1, 7)] + [
    "informacje-dla-uczestnikow.pdf", "ewaluacja-programu.pdf", "bibliografia.pdf"]

README = """Trening Umiejętności Życiowych (TUZ) — pakiet materiałów do druku

Zawartość:
  program/   — cały program, scenariusze modułów 1–6, przewodnik prowadzącego, bibliografia
  modul-1/ … modul-6/ — karty, scenki i arkusze uczestnika do poszczególnych modułów
  pomoce/    — plansze dydaktyczne
  ewaluacja/ — ankiety (PDF i DOCX) oraz karta wdrożenia

Drukuj w formacie A4, w skali 100%, z wyłączonymi nagłówkami i stopkami przeglądarki.
Aktualna wersja materiałów: https://tuz.covepolska.pl

Materiał opracowano w ramach projektu WIN4SMEs – Workplace Innovation for SMEs,
we współpracy z COVE Polska i ZSZ nr 5 we Wrocławiu.
Dofinansowane przez Unię Europejską. Poglądy i opinie wyrażone są jednak wyłącznie
poglądami autora lub autorów i niekoniecznie odzwierciedlają poglądy Unii Europejskiej
lub Europejskiej Agencji Wykonawczej ds. Edukacji i Kultury (EACEA). Unia Europejska
ani EACEA nie ponoszą za nie odpowiedzialności.

Licencja: Creative Commons Uznanie autorstwa 4.0 Międzynarodowe (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/deed.pl
"""

GROUPS = {
    "program": PROGRAM + ["program-calosc.pdf", "specyfikacja-grafik-dobowy.pdf"],
    "modul-1": ["modul-1-arkusze.pdf", "lekcja-1-dzien-doroslego.pdf", "moduly-1-2-scenki.pdf",
                "grafik-dobowy-karty.pdf", "grafik-dobowy-instrukcja.pdf", "arkusze-modul-1.pdf"],
    "modul-2": ["modul-2-karty-rol.pdf", "arkusze-modul-2.pdf"],
    "modul-3": ["modul-3-karty-sytuacji.pdf", "moduly-3-4-karty.pdf", "arkusze-modul-3.pdf"],
    "modul-4": ["modul-4-karty.pdf", "arkusze-modul-4.pdf"],
    "modul-5": ["modul-5-mapa-wyzwalaczy.pdf", "modul-5-karty-scenki.pdf", "arkusze-modul-5.pdf"],
    "modul-6": ["modul-6-arkusze.pdf", "arkusze-modul-6.pdf"],
    "pomoce": ["kompendium-dydaktyczne.pdf", "program-szesc-modulow.pdf", "techniki-regulacji-emocji.pdf",
               "arkusze-wszystkie.pdf"],
    "ewaluacja": ["narzedzia-ewaluacji.pdf", "ankieta-wejsciowa.pdf", "ankieta-koncowa.pdf", "karta-wdrozenia.pdf"],
}


def main():
    w = PdfWriter()
    for name in PROGRAM:
        w.append(str(PDF / name))
    w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    w.add_metadata({"/Title": "Trening Umiejętności Życiowych — cały program",
                    "/Author": "Trening Umiejętności Życiowych (TUZ) — WIN4SMEs, COVE Polska"})
    with open(PDF / "program-calosc.pdf", "wb") as f:
        w.write(f)

    out = ROOT / "materialy" / "materialy-do-druku.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("CZYTAJ-MNIE.txt", README)
        for folder, files in GROUPS.items():
            for name in files:
                if (PDF / name).exists():
                    z.write(PDF / name, f"{folder}/{name}")
        for docx in sorted((ROOT / "materialy" / "ankiety").glob("*.docx")):
            z.write(docx, f"ewaluacja/{docx.name}")
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
