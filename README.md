# Sistem Diagnoză Auto (OBD-II / DTC)

Aplicație desktop în Python (Tkinter + SQLite) care simulează un tester de diagnoză auto: identifică mașina după VIN sau după marcă, model, an și motorizare, „scanează” modulele electronice și interpretează codurile de eroare DTC folosind o bază de date locală. Fiecare scanare se salvează în istoric.

> Desktop app (Python, Tkinter, SQLite) that simulates an OBD-II diagnostic tool: vehicle lookup by VIN, module scan, DTC interpretation from a local database and scan history.

<!-- Adauga aici o captura de ecran: screenshots/aplicatie.png -->

## Funcționalități

- Identificare vehicul după VIN sau selecție manuală (marcă → model → an → combustibil → motorizare → transmisie)
- Scanare completă sau pe un singur modul (ECU Motor, ABS/ESP, Airbag/SRS, Cutie viteze, Climatizare etc.)
- Interpretarea codurilor DTC: descriere, sistem afectat, gravitate, cauze posibile, simptome, recomandare service
- Căutare rapidă a unui cod pe internet, direct din raport
- Istoricul scanărilor, salvat în baza de date
- Interfață dark, cu mod full screen (F11)

> Notă: scanarea este **simulată**. Codurile de eroare sunt alese aleator din baza de date, nu citite de la o interfață OBD reală.

## Baza de date

SQLite, 5 tabele, cu chei străine:

| Tabel | Conținut |
|---|---|
| `masini` | VIN, marcă, model, an, motorizare, combustibil, transmisie |
| `module_auto` | modulele electronice ale mașinii |
| `coduri_eroare` | codurile DTC, cu descriere, gravitate, cauze, simptome, recomandări |
| `scanari` | fiecare scanare: mașina, data, statusul |
| `scanari_coduri` | legătura many-to-many: scanare ↔ modul ↔ cod |

Baza de date (`diagnoza_auto.db`) se creează și se populează automat la prima pornire, cu 10 mașini, 8 module și 20 de coduri DTC (date demonstrative).

## Rulare

Necesită Python 3.9+ (Tkinter este inclus în instalarea standard de Python pe Windows). Nu sunt necesare biblioteci externe.

```bash
python interfata.py
```

Opțional, `python main.py` doar creează și populează baza de date, fără să deschidă interfața.

## Structură

```text
database.py    # crearea tabelelor si datele initiale
interfata.py   # interfata Tkinter si logica de scanare
main.py        # initializeaza doar baza de date
```

## Context

Proiect realizat la disciplina Baze de Date, Facultatea de Automatică, Calculatoare și Electronică (FACE), Universitatea din Craiova.
