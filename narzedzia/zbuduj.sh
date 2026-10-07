#!/bin/sh
# Odtwarza wszystkie materiały do pobrania: branding, PDF-y, DOCX i pakiet ZIP.
# Użycie: sh narzedzia/zbuduj.sh   (z katalogu głównego repozytorium)
set -e
cd "$(dirname "$0")/.."
python3 narzedzia/branding.py
python3 narzedzia/karty_logo.py
python3 narzedzia/docx_branding.py
node narzedzia/pdf.js
python3 narzedzia/pakiet.py
