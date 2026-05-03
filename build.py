#!/usr/bin/env python3
"""Build YOSIDI multi-language site from templates + locale JSONs.

Reads:
  _src/templates/*.html  (templates with data-i18n hooks)
  locales/{lang}.json    (translation strings)

Writes:
  /index.html, /privacy.html, /terms.html, /404.html             (English, default)
  /{lang}/index.html, /{lang}/privacy.html, /{lang}/terms.html   (other langs)

Usage:
  python3 build.py
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Missing dependency. Run: pip3 install beautifulsoup4")

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "_src" / "templates"
LOCALES_DIR = ROOT / "locales"
SITE_URL = "https://www.yosidi.com"

LANGUAGES = ["en", "es", "fr", "de", "it", "pt"]
DEFAULT_LANG = "en"  # output to root, no /en/ subdir

OG_LOCALE = {
    "en": "en_US", "es": "es_ES", "fr": "fr_FR",
    "de": "de_DE", "it": "it_IT", "pt": "pt_PT",
}

# Pages with localized navigation (have a lang switcher / nav)
PAGES = ["index.html", "privacy.html", "terms.html"]


def t(translations: dict, key: str):
    """Lookup nested translation key like 'meta.title'. Returns None if missing."""
    parts = key.split(".")
    val = translations
    for p in parts:
        if not isinstance(val, dict) or p not in val:
            return None
        val = val[p]
    return val if isinstance(val, str) else None


def url_for(lang: str, page: str) -> str:
    """Absolute URL for a given (lang, page)."""
    if lang == DEFAULT_LANG:
        if page == "index.html":
            return f"{SITE_URL}/"
        return f"{SITE_URL}/{page}"
    if page == "index.html":
        return f"{SITE_URL}/{lang}/"
    return f"{SITE_URL}/{lang}/{page}"


def path_for(lang: str, page: str) -> str:
    """Same as url_for but returns the absolute path only (for hrefs)."""
    if lang == DEFAULT_LANG:
        return "/" if page == "index.html" else f"/{page}"
    return f"/{lang}/" if page == "index.html" else f"/{lang}/{page}"


def get_lastmod(lang: str, page: str) -> str:
    """ISO date (YYYY-MM-DD) of the latest commit touching template+locale of
    this (lang, page). Falls back to today if not in a git repo or no commits."""
    sources = [TEMPLATES_DIR / page, LOCALES_DIR / f"{lang}.json"]
    dates = []
    for src in sources:
        if not src.exists():
            continue
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%cI", "--", str(src.relative_to(ROOT))],
                capture_output=True, text=True, cwd=ROOT, check=False,
            )
            d = result.stdout.strip()
            if d:
                dates.append(d.split("T")[0])
        except FileNotFoundError:
            pass
    if dates:
        return max(dates)
    from datetime import date
    return date.today().isoformat()


def translate_data_i18n(soup: BeautifulSoup, translations: dict):
    """Replace text/content of all [data-i18n] elements."""
    for el in soup.select("[data-i18n]"):
        key = el.get("data-i18n")
        text = t(translations, key)
        if text is not None:
            if el.name == "meta":
                el["content"] = text
            elif el.name == "title":
                el.string = text
            else:
                # Replace inner text. If the element contains nested children
                # (e.g. svg + span), this would wipe them — but in this codebase
                # data-i18n is only used on text-only elements.
                el.clear()
                el.append(text)
        del el["data-i18n"]


def translate_aria_labels(soup: BeautifulSoup, translations: dict):
    """Replace aria-label for [data-i18n-aria-label]; handle {n} placeholder."""
    for el in soup.select("[data-i18n-aria-label]"):
        key = el.get("data-i18n-aria-label")
        text = t(translations, key)
        if text is not None:
            if "{n}" in text and el.has_attr("data-index"):
                text = text.replace("{n}", str(int(el["data-index"]) + 1))
            el["aria-label"] = text
        del el["data-i18n-aria-label"]


def translate_alt_attrs(soup: BeautifulSoup, translations: dict):
    """Replace alt attribute for [data-i18n-alt]."""
    for el in soup.select("[data-i18n-alt]"):
        key = el.get("data-i18n-alt")
        text = t(translations, key)
        if text is not None:
            el["alt"] = text
        del el["data-i18n-alt"]


def add_breadcrumb_jsonld(soup: BeautifulSoup, lang: str, page: str, translations: dict):
    """Inject BreadcrumbList JSON-LD for non-home pages (Home → Page)."""
    if page == "index.html" or soup.head is None:
        return
    page_key = page.replace(".html", "")
    home_name = t(translations, "breadcrumb.home") or "Home"
    page_name = t(translations, f"breadcrumb.{page_key}") or page_key.title()
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home_name, "item": url_for(lang, "index.html")},
            {"@type": "ListItem", "position": 2, "name": page_name, "item": url_for(lang, page)},
        ],
    }
    script = soup.new_tag("script", type="application/ld+json")
    script.string = json.dumps(breadcrumb, ensure_ascii=False, indent=2)
    soup.head.append(script)


def rewrite_resource_paths(html: str) -> str:
    """Rewrite ./css/, ./images/, ./js/ to absolute /css/, /images/, /js/."""
    # Limit to known resource folders to avoid breaking inter-page links.
    return (
        html
        .replace('"./css/', '"/css/')
        .replace('"./images/', '"/images/')
        .replace('"./js/', '"/js/')
        .replace("'./css/", "'/css/")
        .replace("'./images/", "'/images/")
        .replace("'./js/", "'/js/")
    )


def update_canonical(soup: BeautifulSoup, lang: str, page: str):
    """Set/insert canonical link pointing to this exact (lang, page) URL."""
    url = url_for(lang, page)
    canon = soup.find("link", rel="canonical")
    if canon is not None:
        canon["href"] = url
    else:
        canon = soup.new_tag("link", rel="canonical", href=url)
        soup.head.append(canon)


def update_og_meta(soup: BeautifulSoup, lang: str, page: str, translations: dict):
    """Update og:url, og:locale, og:title, og:description, twitter equivalents."""
    url = url_for(lang, page)

    def set_meta(prop: str, content: str):
        el = soup.find("meta", property=prop) or soup.find("meta", attrs={"name": prop})
        if el is not None and content is not None:
            el["content"] = content

    set_meta("og:url", url)
    set_meta("twitter:url", url)
    set_meta("og:locale", OG_LOCALE[lang])

    # For the home page, use translated meta.og_title etc. from locale.
    if page == "index.html":
        og_title = t(translations, "meta.og_title")
        og_desc = t(translations, "meta.og_description")
        if og_title:
            set_meta("og:title", og_title)
            set_meta("twitter:title", og_title)
        if og_desc:
            set_meta("og:description", og_desc)
            set_meta("twitter:description", og_desc)
    # For privacy/terms, keep the static OG content (per-page already set in templates).


def remove_existing_alternates(soup: BeautifulSoup):
    """Remove any existing hreflang / og:locale:alternate tags before adding fresh ones."""
    for el in soup.find_all("link", rel="alternate"):
        if el.has_attr("hreflang"):
            el.decompose()
    for el in soup.find_all("meta", property="og:locale:alternate"):
        el.decompose()


def add_hreflang(soup: BeautifulSoup, page: str, current_lang: str):
    """Insert <link rel='alternate' hreflang='X' href='...'> for each language + x-default."""
    head = soup.head
    # Insert after canonical for cleanliness
    canon = soup.find("link", rel="canonical")
    anchor = canon if canon else head

    new_tags = []
    for lang in LANGUAGES:
        tag = soup.new_tag(
            "link",
            rel="alternate",
            hreflang=lang,
            href=url_for(lang, page),
        )
        new_tags.append(tag)
    # x-default points to the canonical default language version.
    new_tags.append(
        soup.new_tag(
            "link",
            rel="alternate",
            hreflang="x-default",
            href=url_for(DEFAULT_LANG, page),
        )
    )

    # og:locale:alternate (excluding the current language)
    og_alts = []
    for lang in LANGUAGES:
        if lang == current_lang:
            continue
        m = soup.new_tag("meta")
        m["property"] = "og:locale:alternate"
        m["content"] = OG_LOCALE[lang]
        og_alts.append(m)

    # Insert hreflang after canonical, og:locale:alternate after og:locale
    for tag in reversed(new_tags):
        anchor.insert_after(tag)

    og_locale_el = soup.find("meta", property="og:locale")
    if og_locale_el is not None:
        anchor2 = og_locale_el
        for m in reversed(og_alts):
            anchor2.insert_after(m)


def build_lang_switcher(soup: BeautifulSoup, lang: str, page: str):
    """Convert the lang-switcher <button> elements to <a> links pointing
    to the equivalent page in each language.
    """
    switcher = soup.select_one(".language-switcher")
    if switcher is None:
        return

    # Update the visible "current" button text + aria-label translation will be
    # handled by data-i18n-aria-label removal already.
    current_btn = switcher.select_one(".lang-current")
    if current_btn is not None:
        current_btn.string = lang.upper()

    # Replace each <button class="lang-btn"> with <a class="lang-btn">
    for btn in switcher.select(".lang-btn"):
        btn_lang = btn.get("id", "").replace("lang-", "")
        if not btn_lang or btn_lang not in LANGUAGES:
            continue

        a = soup.new_tag("a", href=path_for(btn_lang, page))
        a["class"] = btn.get("class", [])
        a["id"] = btn["id"]

        # Mark current language with class active; remove it from others.
        classes = list(a.get("class", []))
        if btn_lang == lang:
            if "active" not in classes:
                classes.append("active")
        else:
            classes = [c for c in classes if c != "active"]
        a["class"] = classes
        a.string = btn.string or btn_lang.upper()

        btn.replace_with(a)


def set_html_lang(soup: BeautifulSoup, lang: str):
    if soup.html is not None:
        soup.html["lang"] = lang


def render(template_html: str, translations: dict, lang: str, page: str) -> str:
    soup = BeautifulSoup(template_html, "html.parser")

    set_html_lang(soup, lang)
    translate_data_i18n(soup, translations)
    translate_aria_labels(soup, translations)
    translate_alt_attrs(soup, translations)
    update_canonical(soup, lang, page)
    update_og_meta(soup, lang, page, translations)
    remove_existing_alternates(soup)
    add_hreflang(soup, page, lang)
    build_lang_switcher(soup, lang, page)
    add_breadcrumb_jsonld(soup, lang, page, translations)

    # Pretty output (str() preserves original formatting reasonably).
    rendered = str(soup)
    rendered = rewrite_resource_paths(rendered)
    return rendered


def output_path(lang: str, page: str) -> Path:
    """Filesystem path where the rendered file should be written."""
    if lang == DEFAULT_LANG:
        return ROOT / page
    return ROOT / lang / page


def main():
    if not TEMPLATES_DIR.exists():
        sys.exit(f"Templates dir not found: {TEMPLATES_DIR}")
    if not LOCALES_DIR.exists():
        sys.exit(f"Locales dir not found: {LOCALES_DIR}")

    translations_by_lang = {}
    for lang in LANGUAGES:
        f = LOCALES_DIR / f"{lang}.json"
        if not f.exists():
            sys.exit(f"Missing locale file: {f}")
        translations_by_lang[lang] = json.loads(f.read_text(encoding="utf-8"))

    generated = []
    for lang in LANGUAGES:
        translations = translations_by_lang[lang]
        for page in PAGES:
            tpl_path = TEMPLATES_DIR / page
            if not tpl_path.exists():
                continue
            html = render(tpl_path.read_text(encoding="utf-8"), translations, lang, page)
            out = output_path(lang, page)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            generated.append(out.relative_to(ROOT))

    # 404.html only needed at root (one global fallback)
    err_tpl = TEMPLATES_DIR / "404.html"
    if err_tpl.exists():
        out = ROOT / "404.html"
        # 404 is mostly static; just copy and rewrite paths.
        html = rewrite_resource_paths(err_tpl.read_text(encoding="utf-8"))
        out.write_text(html, encoding="utf-8")
        generated.append(out.relative_to(ROOT))

    # Generate sitemap.xml with hreflang alternates for every URL.
    sitemap = build_sitemap()
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    generated.append(Path("sitemap.xml"))

    print(f"Generated {len(generated)} files:")
    for p in generated:
        print(f"  - {p}")


def build_sitemap() -> str:
    """Generate sitemap.xml listing all (lang, page) URLs with hreflang alternates."""
    priority_for = {"index.html": "1.0", "privacy.html": "0.3", "terms.html": "0.3"}
    changefreq_for = {"index.html": "weekly", "privacy.html": "monthly", "terms.html": "monthly"}

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for page in PAGES:
        for lang in LANGUAGES:
            loc = url_for(lang, page)
            lines.append("  <url>")
            lines.append(f"    <loc>{loc}</loc>")
            for alt_lang in LANGUAGES:
                lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="{alt_lang}" href="{url_for(alt_lang, page)}"/>'
                )
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_for(DEFAULT_LANG, page)}"/>'
            )
            lines.append(f"    <lastmod>{get_lastmod(lang, page)}</lastmod>")
            lines.append(f"    <changefreq>{changefreq_for[page]}</changefreq>")
            lines.append(f"    <priority>{priority_for[page]}</priority>")
            lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
