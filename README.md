# YoSiDi CAD - Landing Page

Landing page profesional y minimalista para la aplicación iOS **YoSiDi CAD**.

## 🎯 Sobre YoSiDi CAD

YoSiDi CAD es una aplicación de dibujo CAD para iPad/iPhone enfocada en hacer levantamientos de espacios y edificios existentes de manera rápida y eficaz.

## ✨ Características de la Landing Page

- ✅ Diseño minimalista y elegante
- ✅ Totalmente responsive (móvil, tablet, desktop)
- ✅ Animaciones sutiles al hacer scroll
- ✅ Sistema de internacionalización (i18n) - Español e Inglés
- ✅ Optimizada para SEO
- ✅ Meta tags Open Graph y Twitter Cards
- ✅ Sin dependencias (Vanilla JavaScript)
- ✅ Accesible (WCAG 2.1)

## 📁 Estructura del Proyecto

```
yosidi-web/
├── index.html              # Página principal
├── css/
│   └── styles.css          # Estilos CSS
├── js/
│   ├── main.js             # JavaScript principal (animaciones, carrusel)
│   └── i18n.js             # Sistema de internacionalización
├── images/
│   ├── logo.png            # Logo de la app (placeholder SVG)
│   ├── favicon.png         # Favicon
│   ├── screenshot1.png     # Captura 1 (placeholder SVG)
│   ├── screenshot2.png     # Captura 2 (placeholder SVG)
│   └── screenshot3.png     # Captura 3 (placeholder SVG)
├── locales/
│   ├── es.json             # Traducciones en español
│   └── en.json             # Traducciones en inglés
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Este archivo
```

## 🚀 Instalación y Uso

### Requisitos Previos

- Un navegador web moderno
- (Opcional) Un servidor HTTP local para desarrollo

### Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/yosidi-web.git
cd yosidi-web
```

2. Abre el archivo `index.html` en tu navegador, o usa un servidor local:

**Opción 1: Servidor con Python**
```bash
# Python 3
python -m http.server 8000

# Luego abre: http://localhost:8000
```

**Opción 2: Servidor con Node.js (http-server)**
```bash
npx http-server -p 8000

# Luego abre: http://localhost:8000
```

**Opción 3: Live Server (VS Code)**
- Instala la extensión "Live Server" en VS Code
- Click derecho en `index.html` → "Open with Live Server"

## 🖼️ Reemplazar Imágenes Placeholder

Las imágenes actuales son SVG placeholders. Para usar imágenes reales:

1. **Logo** (`images/logo.png`):
   - Tamaño recomendado: 200x200 px
   - Formato: PNG con fondo transparente

2. **Favicon** (`images/favicon.png`):
   - Tamaño: 64x64 px o 32x32 px
   - Formato: PNG

3. **Screenshots** (`images/screenshot1.png`, `screenshot2.png`, `screenshot3.png`):
   - Tamaño recomendado: 800x600 px o mayor
   - Formato: PNG o JPG
   - Capturas reales de la app en iPad/iPhone

Simplemente reemplaza los archivos manteniendo los mismos nombres.

## 🌍 Agregar Nuevos Idiomas

1. Crea un nuevo archivo JSON en la carpeta `locales/`:
   ```bash
   # Ejemplo para francés
   locales/fr.json
   ```

2. Copia la estructura de `es.json` o `en.json` y traduce los textos.

3. Actualiza el array de idiomas soportados en `js/i18n.js`:
   ```javascript
   const supportedLangs = ['es', 'en', 'fr'];
   ```

4. Añade el botón de idioma en `index.html`:
   ```html
   <button id="lang-fr" class="lang-btn">FR</button>
   ```

## 🎨 Personalización

### Colores

Los colores principales se definen en `css/styles.css` usando variables CSS:

```css
:root {
    --color-primary: #007AFF;        /* Color principal */
    --color-primary-dark: #0051D5;   /* Color principal oscuro */
    --color-text: #1d1d1f;           /* Color del texto */
    --color-text-secondary: #6e6e73; /* Color del texto secundario */
    /* ... más variables ... */
}
```

### Tipografía

Cambia la fuente en `css/styles.css`:

```css
:root {
    --font-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, ...;
}
```

## 📤 Desplegar en GitHub Pages

1. **Sube tu repositorio a GitHub**:
   ```bash
   git remote add origin https://github.com/tu-usuario/yosidi-web.git
   git branch -M main
   git push -u origin main
   ```

2. **Configura GitHub Pages**:
   - Ve a Settings → Pages
   - En "Source", selecciona la rama `main`
   - Carpeta: `/ (root)`
   - Click en "Save"

3. **Dominio personalizado** (opcional):
   - En Settings → Pages → Custom domain
   - Ingresa tu dominio (ej: `www.yosidi.com`)
   - Configura los DNS según las instrucciones de GitHub

Tu sitio estará disponible en: `https://tu-usuario.github.io/yosidi-web/`

## 🔗 Enlaces

- **App Store**: https://apps.apple.com/es/app/yosidi-cad/id6743679420
- **YouTube**: https://www.youtube.com/@YoSiDi-CAD
- **TikTok**: https://www.tiktok.com/@yosidi_cad

## 📝 Tecnologías Utilizadas

- HTML5
- CSS3 (Variables CSS, Flexbox, Grid)
- JavaScript (ES6+, Vanilla)
- SVG (para iconos y placeholders)

## 🐛 Solución de Problemas

### Las traducciones no se cargan

- Verifica que los archivos JSON estén en la carpeta `locales/`
- Comprueba la consola del navegador para errores
- Asegúrate de estar usando un servidor HTTP (no `file://`)

### Las animaciones no funcionan

- Verifica que `main.js` se cargue correctamente
- Comprueba la consola del navegador
- Algunos navegadores antiguos pueden no soportar las animaciones

### El carrusel no responde

- Asegúrate de que las imágenes existan en `images/`
- Verifica que los selectores en `main.js` coincidan con el HTML

## 📄 Licencia

© 2026 YoSiDi CAD. Todos los derechos reservados.

## 🤝 Contribuir

Si encuentras algún problema o tienes sugerencias:

1. Abre un Issue en GitHub
2. Envía un Pull Request con mejoras

---

**Desarrollado con ❤️ para YoSiDi CAD**
