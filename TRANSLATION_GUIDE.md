# YOSIDI Translation & Build Guide

How to edit content and add languages without breaking the site.

## How the build works

```
_src/templates/*.html  +  locales/{lang}.json  →  python3 build.py  →  HTML files
```

- **Edit text:** modify `locales/{lang}.json` (NEVER the generated HTML).
- **Edit structure/markup:** modify `_src/templates/*.html` (NEVER the generated HTML).
- **Run after any change:** `python3 build.py` regenerates the 21 output files (3 pages × 6 languages + sitemaps).
- **Default language:** English (output to root `/`, no `/en/` subdir).
- **Other languages:** `de`, `es`, `fr`, `it`, `pt` (PT-PT, not PT-BR).

## Tagline / brand voice

The product lema is **"[Plans] CAD from the first site visit"**, expressed naturally in each language:

| Lang | Hero title (lema) | Verb form (used in meta description) |
|---|---|---|
| EN | CAD plans from your first site visit | Deliver CAD plans... |
| ES | Planos CAD desde la primera visita | Levanta planos CAD... |
| DE | CAD-Pläne ab der ersten Begehung | Erstellen Sie CAD-Pläne... |
| FR | Plans CAO dès la première visite | Relevez vos plans CAO... |
| IT | Planimetrie CAD dal primo sopralluogo | Rileva planimetrie CAD... |
| PT | Plantas CAD desde a primeira visita | Levanta plantas CAD... |

Avoid "professional/profesional/professionelles" in headlines — overused. Use the verb form of the lema.

## Universal rules across all languages

- **Section titles use sentence case**, not English Title Case (`"Pagos seguros"`, NOT `"Pagos Seguros"`).
  Exception: formal document names (`"Política de Privacidad"`, `"Terms of Use"`, `"Termini di Utilizzo"`).
- **Touch verbs:** `tap` / `toque` / `Tippen` / `toucher` / `tocco` / `toque` — NEVER `click` (this is iPad/iPhone).
- **"Where the survey ends"** — use universal terms covering all 6 audience profiles (architects, interiors, engineers, appraisers, builders, trades). Avoid words that mean "construction phase" or "legal property":
  - EN `site` ✓ — not "construction site"
  - ES `sitio` / `lugar` ✓ — NOT `obra` (= construction phase) NOR `inmueble` (legal/cold; excludes plots)
  - DE `Objekt` ✓ — NOT `Gebäude` (excludes plots)
  - FR `lieux` ✓
  - IT `luogo` ✓ — NOT `cantiere` (= construction site) NOR `immobile`
  - PT `local` ✓ — NOT `imóvel` (legal/cold)
- **Repetition `with...with`** in image alt text — common bug. Use em dash: `Compatible with X — feature Y`.
- **Meta description ≤ 155 chars** (Google snippet limit). Pattern: *verb + lema + tech keywords (Bluetooth/iPad/DXF) + 3 audience profiles*.

## CAD/architecture glossary

The terms a native architect actually uses. Don't substitute.

| Concept | EN | ES | DE | FR | IT | PT |
|---|---|---|---|---|---|---|
| Floor plan | floor plan | plano | Plan | plan | planimetria | planta |
| Survey (n.) | as-built survey | levantamiento | Aufmaß | relevé | rilievo | levantamento |
| Site visit | site visit | visita | Begehung / Ortstermin | visite | sopralluogo | visita |
| Title block | title block | cajetín | **Schriftfeld** (DIN 6771) | cartouche | cartiglio | legenda |
| Laser meter | laser meter | medidor láser | **Laser-Distanzmesser** | télémètre laser | distanziometro laser | medidor laser |
| Openings (holes in wall) | openings | huecos | Öffnungen | **ouvertures** (NOT *huisseries*!) | aperture / vani | vãos |
| Pocket door | pocket door | corredera empotrada | Wandschiebetür | porte à galandage | porta scorrevole a scomparsa | porta de correr embutida |
| Gross / Net floor area | gross / net | superficie construida / útil | BGF / NGF (DIN 277) | surface construite / utile | superficie lorda / netta | área bruta / útil |
| Existing conditions | existing conditions | estado actual | Bestand | état des lieux | stato attuale | estado atual |
| Trades (occupations) | trades | oficios | Handwerker | artisans | artigiani | ofícios |
| Closets | closets (US) | armarios | Schränke | placards | armadi | armários |
| Office (architect's) | office | estudio | Büro | agence | studio | atelier |
| Out-of-square walls | out-of-square walls | falsas escuadras | schiefe Wände | faux équerrages | pareti fuori squadra | paredes fora de esquadro |
| Energy certificate | energy certificate | certificado energético | Energieausweis | DPE / diagnostic énergétique | APE | certificado energético |
| Appraiser | appraiser | tasador / perito | Gutachter | expert / diagnostiqueur | perito / stimatore | perito / avaliador |

CAD command names (offset/fillet/trim/extend/copy/move/stretch/rotate/measure) — use the AutoCAD-localized terms, all as nouns for consistency:

| EN | ES | DE | FR | IT | PT |
|---|---|---|---|---|---|
| Offset, fillet, trim, extend, copy, move, stretch, rotate, measure | Paralela, empalme, recorte, alargue, copia, desplazamiento, estiramiento, giro, medición | Versatz, Abrunden, Trimmen, Verlängern, Kopieren, Verschieben, Dehnen, Drehen, Messen | Décaler, raccorder, ajuster, prolonger, copier, déplacer, étirer, faire pivoter, mesurer | Parallela, raccordo, taglio, estensione, copia, spostamento, stiramento, rotazione, misurazione | Paralela, concordância, corte, prolongamento, cópia, deslocação, alongamento, rotação, medição |

## Per-language gotchas

### EN (US)
- Oxford comma in lists: `"architects, engineers, and interior designers"`.
- US spelling: *color*, *behavior*, *dimension*.
- Use `gross/net floor area`, NOT `built/usable` (literal translation from ES).
- Use `existing conditions`, NOT `current state of the site`.

### ES (España)
- `añadir`, NOT `agregar` (Spain vs LatAm).
- Tuteo (`tú`) throughout.
- Architecture = `superficies` (not `áreas`); `levantar planos` (not `crear planos`).
- `interiorismo` (not `diseño de interiores`).

### DE
- Standard German orthography: `ß` (NOT Swiss `ss`). `ausschließlich`, `Fuß`, `verstoßen`.
- Always Umlauts: `Öffnungen`, `Änderung` (NEVER `Oeffnungen`, `Aenderung`).
- Formal `Sie` / `Ihr` throughout.
- Architects: `Begehung` for site visit, `Objekt` for the property, `Schriftfeld` for title block, `BGF/NGF` for floor areas.

### FR
- Sentence case in titles. Title Case is anglicism.
- Formal `vous` throughout.
- Space before `:`, `?`, `!`, `;`, and `«…»` quotes.
- `ouvertures` (NOT `huisseries` — that's the door frame, not the opening).
- `électroménager` (singular collective, NOT `électroménagers`).

### IT
- Sentence case in titles.
- Informal `tu` throughout (this site is consumer-friendly).
- `in loco` universally for on-site (NEVER `in cantiere` — implies construction phase).
- `stimatori` for appraisers (more technical than `valutatori`).
- `attestato di prestazione energetica` / `APE` is the legal term.

### PT (Portugal — NOT Brazil)
- `descarregar`, NOT `baixar` (PT-PT vs PT-BR).
- `câmara`, `ficheiros`, `definições`, `casa de banho`, `atelier`, `telemóvel` (PT-PT vocabulary).
- Tuteo (`tu` / `o teu`) throughout.
- `Site` alone, NEVER `Site web` (redundant: web web).
- Diacritical PT-PT spelling: `deteção`, `aceitação`, `direção` (no `c` before `t`).
- `áreas` for floor area (consistent with PT-PT architecture).

## Adding new content

1. Add the key to **all 6** `locales/{lang}.json` files (keep keys identical).
2. Add `data-i18n="path.to.key"` to the relevant element in `_src/templates/*.html`.
3. Run `python3 build.py`.
4. Verify the new string appears in `de/index.html`, `es/index.html`, etc.

## Adding a new language

1. Copy `locales/en.json` to `locales/{xx}.json` and translate.
2. Add `xx` to the `LANGUAGES` list in `build.py`.
3. Add the OG locale code (e.g. `"nl": "nl_NL"`) to the `OG_LOCALE` dict in `build.py`.
4. Add the new language entry to the language switcher in all 3 templates (`index.html`, `privacy.html`, `terms.html`).
5. Run `python3 build.py`.

## Meta tags strategy

Three meta description fields per page, each with a different audience:

| Field | Where it appears | Length budget |
|---|---|---|
| `meta.description` | Google/Bing search snippet | ≤ 155 chars (currently 134–151) |
| `meta.og_description` | WhatsApp, Facebook, LinkedIn, iMessage previews | ≤ 120 chars recommended |
| `meta.twitter_description` | Twitter/X card preview | ≤ 120 chars recommended |

Pattern for `meta.description`: **verb-form lema + Bluetooth/iPad keywords + DXF/DWG + 3 audience profiles** (architects, engineers, interior designers — highest SEO volume of the 6).
