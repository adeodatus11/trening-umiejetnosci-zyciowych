# RAPORT TESTÓW STRONY

**Etap 10 — Testowanie strony**
**Data:** 20.07.2026
**Metoda:** walidacja automatyczna (skrypt sprawdzający strukturę, linki i pliki) + przegląd kodu pod kątem WCAG 2.1. Wynik zbiorczy: **0 błędów krytycznych**.

## Zakres strony
14 podstron HTML, 1 arkusz CSS, 1 skrypt JS, 16 plików do pobrania (folder `pliki/`).
Strony: `index`, `moduly`, `modul-1..6`, `prowadzacy`, `uczestnik`, `ewaluacja`, `bibliografia`, `o-projekcie`, `pobieranie`.

## Wyniki testów

| Test | Wynik | Uwagi |
|------|-------|-------|
| Wszystkie linki lokalne prowadzą do istniejących plików | ✅ | 0 martwych linków (14 stron) |
| Pliki do pobrania istnieją | ✅ | 16/16 obecnych w `pliki/` |
| `lang="pl"` na każdej stronie | ✅ | wykrywalny przez czytniki ekranu |
| `charset=utf-8` + `viewport` (mobile) | ✅ | poprawne polskie znaki, skalowanie mobilne |
| Nagłówek `<h1>` na każdej stronie | ✅ | jeden główny nagłówek/strona |
| Hierarchia nagłówków (h1→h2→h3) | ✅ | generowana z Markdown |
| Nawigacja `<nav>` + menu główne | ✅ | obecne na wszystkich stronach |
| Breadcrumbs na podstronach | ✅ | Start › Moduły › Moduł X itd. |
| Link „Przejdź do treści" (skip-link) | ✅ | pierwszy element, widoczny przy focusie |
| Tabele renderowane poprawnie | ✅ | 15 tabel (naprawiono brak pustej linii przed tabelą) |
| Obrazy bez `alt` | ✅ | brak `<img>` — brak ryzyka |
| Widoczny focus (klawiatura) | ✅ | `:focus-visible` z konturem 3px |
| Wyszukiwarka/filtr modułów | ✅ | JS filtruje po tekście i temacie; `aria-live` na liczniku |
| Menu mobilne (hamburger) | ✅ | `aria-expanded` przełączane; lista chowana <760px |
| Responsywność (grid, breakpointy) | ✅ | siatka auto-fill; media query 760px |
| Kontrast kolorów | ✅ (projektowo) | tekst #1a1e24 na białym; nagłówek/przyciski na ciemnym tle — spełnia ≥4.5:1 |
| CSS i JS podłączone | ✅ | `css/style.css`, `js/main.js` |

## Dostępność (WCAG 2.1) — szczegóły
- **1.4.1 Użycie koloru:** moduły rozróżniane kolorem **oraz** etykietą „Moduł N" i tekstem; karty „Grafik Dobowy" opisane kolor+ikona+nazwa.
- **2.1 Obsługa klawiaturą:** wszystkie elementy interaktywne to natywne `<a>`, `<button>`, `<input>`, `<select>`, `<details>` — dostępne z klawiatury; widoczny focus.
- **2.4 Nawigacja:** skip-link, breadcrumbs, spójne menu, `aria-current="page"`.
- **1.3.1 Struktura:** semantyczne `header/nav/main/footer/article`, nagłówki, tabele z `<th>`.
- **4.1 Zgodność:** `aria-controls`, `aria-expanded`, `aria-live` zastosowane.

## Testy wykonane w toku i naprawione
1. **Tabele nie renderowały się** (brak pustej linii przed tabelą w Markdown) — naprawiono w 18 plikach źródłowych i przebudowano stronę; 15 tabel renderuje się poprawnie.

## Ograniczenia testu
- Nie wykonano renderu wizualnego w przeglądarce na tej maszynie (ścieżka pliku ze spacjami i znakami PL utrudnia otwarcie `file://`). Zalecane **ręczne sprawdzenie wizualne** po otwarciu `index.html` lokalnie oraz test na realnym urządzeniu mobilnym.
- Test kontrastu oparto na wartościach projektowych CSS, nie na automatycznym analizatorze — zalecana weryfikacja narzędziem (np. axe / Lighthouse) przy publikacji.
- Linki zewnętrzne (źródła w bibliografii) prowadzą do oficjalnych domen wydawców; ich dostępność zależy od stron trzecich (CASEL i WHO IRIS zweryfikowano 20.07.2026).

## Jak przetestować lokalnie (rekomendacja)
Uruchom prosty serwer w folderze `06_WEBSITE/` i otwórz `http://localhost:8000`:
```
python3 -m http.server 8000
```
Następnie sprawdź: nawigację Tab/Enter, menu na wąskim oknie, filtr modułów, pobieranie plików, Lighthouse (Accessibility).

**Wniosek:** strona jest kompletna, spójna z materiałami końcowymi, wolna od martwych linków i zbudowana zgodnie z podstawowymi wymaganiami WCAG 2.1. Do publikacji zalecane jedno ręczne sprawdzenie wizualne i test Lighthouse.
