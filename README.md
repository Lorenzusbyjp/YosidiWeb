# YOSIDI CAD — Landing Page

Landing oficial de **YOSIDI CAD** (app iOS para levantamientos CAD profesionales en iPad e iPhone). Web estática, multi-idioma, hosteada en GitHub Pages bajo `www.yosidi.com`.

## Stack y filosofía

- **Cero dependencias en producción.** HTML estático + un único `styles.css` + dos JS minimos. Sin frameworks, sin build de JS/CSS.
- **Multi-URL por idioma.** Cada idioma tiene su URL real (`/`, `/es/`, `/fr/`, `/de/`, `/it/`, `/pt/`) → SEO multi-idioma real, sin parpadeo de traducción cliente.
- **Hosting:** GitHub Pages + dominio `www.yosidi.com` (CNAME).
- **Analítica:** Cloudflare Web Analytics (cookieless, sin banner GDPR).

## Estructura del proyecto

```
YosidiWeb/
├── README.md                    ← Este archivo
├── CNAME                        ← Dominio personalizado (www.yosidi.com)
├── .nojekyll                    ← Desactiva Jekyll en GitHub Pages
├── build.py                     ← Build script (genera todas las páginas)
│
├── _src/                        ← Source files (no se sirven en producción)
│   ├── templates/               ← Plantillas HTML con [data-i18n] hooks
│   │   ├── index.html
│   │   ├── privacy.html
│   │   ├── terms.html
│   │   └── 404.html
│   └── scripts/                 ← Herramientas de desarrollo
│       ├── optimize-images.sh
│       └── update-image-dimensions.sh
│
├── locales/                     ← Traducciones (source para el build)
│   ├── en.json                  ← Inglés (idioma por defecto)
│   ├── es.json                  ← Español
│   ├── fr.json, de.json, it.json, pt.json
│
├── css/styles.css               ← Estilos compartidos (todos los idiomas)
├── js/
│   ├── i18n.js                  ← Toggle del switcher + persiste idioma elegido
│   └── main.js                  ← Animaciones, carrusel, hamburguesa, etc.
│
├── images/
│   ├── og/og_yosidi.png         ← Master OG (2400×1260)
│   ├── og-image.png             ← Web OG (1200×630, lo que ven LinkedIn/FB)
│   ├── og-image.webp
│   ├── optimized/               ← PNGs+WebPs optimizados para la galería
│   │   ├── IPAD SCREENSHOT.{png,webp}
│   │   └── screenshot1..10.{png,webp}
│   └── ...                      ← Originales App Store
│
├── index.html                   ← English (root + canonical EN)  ┐
├── privacy.html                 ← Privacy Policy (EN)            │
├── terms.html                   ← Terms of Use (EN)              │ Generadas
├── 404.html                     ← Página 404 (universal)         │ por
├── es/{index,privacy,terms}.html  ← Español                      │ build.py
├── fr/{index,privacy,terms}.html  ← Francés                      │
├── de/{index,privacy,terms}.html  ← Alemán                       │
├── it/{index,privacy,terms}.html  ← Italiano                     │
├── pt/{index,privacy,terms}.html  ← Portugués                    │
├── sitemap.xml                  ← 18 URLs con hreflang alternates ┘
└── robots.txt
```

> ⚠️ **No edites a mano** los archivos HTML del root ni de `/<lang>/`. Son output del build. Edita `_src/templates/` o `locales/*.json` y corre `python3 build.py`.

## Arquitectura multi-idioma

### URLs

| URL | Idioma |
|---|---|
| `https://www.yosidi.com/` | English (canonical EN) |
| `https://www.yosidi.com/es/` | Español |
| `https://www.yosidi.com/fr/` | Français |
| `https://www.yosidi.com/de/` | Deutsch |
| `https://www.yosidi.com/it/` | Italiano |
| `https://www.yosidi.com/pt/` | Português |

Cada idioma además tiene `<lang>/privacy.html` y `<lang>/terms.html`.

### Detección automática

El `<head>` del `index.html` (root) contiene un script inline que:

1. Lee `localStorage.preferred-lang` si el usuario eligió antes un idioma.
2. Si no hay preferencia, lee `navigator.language` del navegador.
3. Si el idioma detectado es uno de los soportados (`es`, `fr`, `de`, `it`, `pt`) y el usuario está en `/`, redirige a `/<lang>/`.
4. Si el idioma es inglés u otro no soportado, se queda en `/` (English).

El switcher de idiomas en cualquier página es una lista de `<a>` que navegan a la versión equivalente; al hacer click, se persiste el idioma elegido en `localStorage`.

### SEO técnico

- **`hreflang`** real: cada página declara las 6 alternativas + `x-default` apuntando a `/`.
- **`canonical`** auto-generado por idioma.
- **`sitemap.xml`** con 18 URLs, cada una con sus 7 alternates (`xhtml:link`).
- **OG/Twitter cards** localizadas: cada `/<lang>/` tiene su `og:title`, `og:description` y `og:locale` (e.g. `de_DE`) en el idioma correspondiente.
- **JSON-LD** (SoftwareApplication) **siempre en inglés** — Google usa rich snippets de forma global, no por idioma.
- **`og:image`** única (en inglés) para todas las versiones — la imagen es asset visual, no se localiza.

## Trabajar con la web

### 1. Cambiar copy de la home

Edita el JSON del idioma correspondiente en `locales/`. Ejemplo:

```bash
# Cambiar el subtítulo del hero en español
$EDITOR locales/es.json
# → buscar "hero" → "subtitle" → editar
```

Luego regenera:

```bash
python3 build.py
git add -A && git commit -m "Update Spanish hero subtitle" && git push
```

### 2. Cambiar estructura HTML

Edita `_src/templates/<archivo>.html`. Los hooks de traducción son atributos:

- `data-i18n="hero.title"` → reemplaza el contenido por la traducción de esa clave.
- `data-i18n-aria-label="accessibility.carousel_next"` → reemplaza `aria-label` por la traducción.
- Soporta placeholder `{n}` que se sustituye por `data-index + 1` (usado en los dots del carrusel).

Tras editar la plantilla:

```bash
python3 build.py
```

### 3. Añadir un idioma nuevo

1. Crea `locales/<lang>.json` copiando la estructura de `locales/en.json` y traduciendo todos los valores.
2. En `build.py`, añade el código a la lista `LANGUAGES`.
3. Añade el botón al switcher en `_src/templates/index.html`, `privacy.html` y `terms.html`:
   ```html
   <button id="lang-XX" class="lang-btn notranslate">XX</button>
   ```
4. En `build.py`, añade su locale BCP-47 al diccionario `OG_LOCALE`.
5. En el script de redirect inline (en `_src/templates/index.html`), añade el código del idioma a la lista `supported`.
6. `python3 build.py`.

### 4. Cambiar imágenes del carrusel

```bash
# Reemplaza los originales en images/screenshotN.png e IPAD SCREENSHOT.png
# Luego optimiza y actualiza dimensiones en el template:
bash _src/scripts/optimize-images.sh

# Regenera HTMLs
python3 build.py
```

### 5. Cambiar la imagen OG

```bash
# El master 2400×1260 vive en images/og/og_yosidi.png
# Genera versión web 1200×630:
sips -Z 1200 images/og/og_yosidi.png --out images/og-image.png
cwebp -q 85 images/og-image.png -o images/og-image.webp
```

Tras pushear, invalida la caché en:
- Facebook: https://developers.facebook.com/tools/debug/
- LinkedIn: https://www.linkedin.com/post-inspector/

## Build pipeline

```bash
python3 build.py
```

Hace, en orden:

1. Lee `_src/templates/*.html` y `locales/*.json`.
2. Para cada idioma, para cada plantilla:
   - Sustituye `[data-i18n]` y `[data-i18n-aria-label]` por la traducción.
   - Convierte los `<button class="lang-btn">` del switcher en `<a>` con `href` apuntando a la versión equivalente.
   - Ajusta `<html lang>`, `canonical`, `og:url`, `og:locale`, `og:title`, `og:description`, `twitter:*` (los traducibles desde el locale).
   - Añade hreflang completo (6 alternates + x-default).
   - Reescribe paths a absolutos (`./css/` → `/css/`).
   - Limpia atributos `data-i18n*` del output.
3. Escribe la salida en `/` (English) o `/<lang>/` (resto).
4. Genera `sitemap.xml` con todas las URLs y sus alternates.

Dependencias:

```bash
pip3 install beautifulsoup4
```

## Scripts auxiliares

### `_src/scripts/optimize-images.sh`

Toma los PNGs de `images/` y genera versiones optimizadas a `images/optimized/` (max 1200px). Tras eso ejecuta `update-image-dimensions.sh` para sincronizar `width`/`height` en el template del index.

```bash
bash _src/scripts/optimize-images.sh
# o con argumentos custom:
bash _src/scripts/optimize-images.sh images images/optimized 1400
```

Requiere `sips` (incluido en macOS).

### `_src/scripts/update-image-dimensions.sh`

Actualiza atributos `width`/`height` de `<img>` en `_src/templates/index.html` leyendo dimensiones reales con `sips`. Útil tras un resize manual.

## Hosting, dominio, analítica

- **Hosting:** GitHub Pages, branch `main`, root del repo.
- **Dominio personalizado:** `www.yosidi.com` (configurado vía `CNAME`).
- **Analítica:** Cloudflare Web Analytics, snippet incluido en los 4 HTMLs del root y los 15 de los subidiomas. Sin cookies, sin banner GDPR.
- **Política de privacidad** declara explícitamente el uso de Cloudflare Web Analytics en los 6 idiomas.

## Workflow Git habitual

```bash
# 1. Editar fuente
$EDITOR locales/es.json   # o _src/templates/...

# 2. Regenerar
python3 build.py

# 3. Verificar localmente (opcional)
python3 -m http.server 8000
# → abrir http://localhost:8000/ y http://localhost:8000/es/

# 4. Commit y push
git add -A
git commit -m "Tu mensaje"
git push origin main
```

GitHub Pages tarda **30 segundos – 3 minutos** en publicar tras el push. Hard refresh (`Cmd + Shift + R`) en el navegador para ignorar caché.

## Decisiones técnicas (no reintroducir)

Cosas que se decidieron por una razón concreta y no conviene revertir sin contexto:

- **`og:image` única, en inglés, para todas las versiones.** No se localiza por idioma. Una imagen es un asset visual; mantener seis no aporta y multiplica trabajo.
- **JSON-LD (`SoftwareApplication`) siempre en inglés.** Google usa rich snippets de forma global, no por idioma. La `description`, `featureList` y `keywords` del JSON-LD están fijos en inglés en el template aunque la página esté en otro idioma.
- **`js/i18n.js` es deliberadamente mínimo (~40 líneas).** Antes intentaba actualizar `og:title`, `og:description`, `og:locale` dinámicamente al cambiar idioma. Era código muerto (los crawlers no ejecutan JS) y peligroso (algunas apps que leen DOM en vivo veían el OG traducido pero la imagen seguía en inglés → mismatch). No reintroducir lógica dinámica sobre meta tags OG/Twitter.
- **`<title>` de privacy/terms usa keys propias** (`privacy_page.meta_title`, `terms_page.meta_title`), NO `meta.title` (que es la del home). Antes tenían `data-i18n="meta.title"` y i18n.js las sobrescribía con el título de la home. No revertir.
- **`update-image-dimensions.sh` usa `grep`, no `rg`.** Antes requería `ripgrep` instalado. Cambiado para no tener dependencia extra. No re-introducir `rg`.
- **`locales/` vive en root, no en `_src/`.** Es source pero se edita con frecuencia (cambiar copy). Se prioriza accesibilidad sobre consistencia estricta.
- **No editar a mano los HTMLs del root ni de `/<lang>/`.** Son output de `build.py`. Tu cambio se perderá la próxima vez que se regenere.

## Pendientes / mejoras futuras opcionales

- **GitHub Action que ejecute `build.py` en cada push** — ahora hay que recordar correrlo manualmente. Una Action que detecte cambios en `_src/` o `locales/` y regenere automáticamente eliminaría ese paso.
- **`aggregateRating` en JSON-LD** — cuando haya reviews en App Store con número significativo, añadir las estrellas para opt-in a rich snippets de Google.

## Contacto

- Web: https://www.yosidi.com
- Email: support@yosidi.com
- App Store: https://apps.apple.com/app/yosidi-cad/id6743679420

---
© YOSIDI CAD. Todos los derechos reservados.
