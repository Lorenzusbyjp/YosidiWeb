#!/usr/bin/env python3
"""Genera el mini-sitio de Math Fury (identidad oscura neón) dentro de yosidi.com.

Independiente de build.py (que es de YOSIDI CAD): escribe SOLO en /mathfury/ y no
toca el resto del sitio. Una página por idioma (en, es, fr, de, it, pt):

  /mathfury/              /mathfury/privacy/           (en, por defecto)
  /mathfury/{lang}/       /mathfury/{lang}/privacy/    (es, fr, de, it, pt)

Las URLs por defecto (/mathfury/ y /mathfury/privacy/) son las que están en
App Store Connect. Estilos en /mathfury/mathfury.css.

Uso:  python3 _src/build_mathfury.py
"""
from pathlib import Path

SITE = "https://www.yosidi.com"
LANGS = ["en", "es", "fr", "de", "it", "pt"]
LABELS = {"en": "EN", "es": "ES", "fr": "FR", "de": "DE", "it": "IT", "pt": "PT"}
OUT = Path(__file__).resolve().parent.parent / "mathfury"

C = {
    "en": {
        "support_title": "Math Fury — Support",
        "support_desc": "Support and contact for Math Fury, a mental math game against the clock. No ads, no purchases, no data collection.",
        "tagline": "Mental math against the clock",
        "clean_line": "No ads · No purchases · No data collected",
        "support_heading": "Support",
        "support_body": "Got a question, found a bug or want to suggest something? Email us and we'll get back to you:",
        "email_btn": "Email support",
        "privacy_btn": "Privacy policy",
        "privacy_title": "Privacy Policy — Math Fury",
        "privacy_desc": "Math Fury collects no data: no network, no analytics, no ads, no third-party SDKs. Your scores stay on your device.",
        "privacy_heading": "Privacy Policy",
        "privacy_intro": "Math Fury does not collect, store or share any personal data.",
        "bullets": [
            "The app requires no account, registration or sign-in.",
            "It makes no network connections.",
            "It uses no analytics, advertising or third-party SDKs.",
            "It does not track your activity inside or outside the app.",
        ],
        "privacy_storage": "Your high scores, streaks and statistics are stored only on your device (using the system's <code>UserDefaults</code>) and are never sent to any server. Uninstalling the app deletes that data with it.",
        "contact_heading": "Contact",
        "back": "← Math Fury",
    },
    "es": {
        "support_title": "Math Fury — Soporte",
        "support_desc": "Soporte y contacto de Math Fury, juego de cálculo mental a contrarreloj. Sin anuncios, sin compras y sin recopilación de datos.",
        "tagline": "Cálculo mental a contrarreloj",
        "clean_line": "Sin anuncios · Sin compras · Sin datos",
        "support_heading": "Soporte",
        "support_body": "¿Tienes una duda, has encontrado un fallo o quieres sugerir algo? Escríbenos y te respondemos:",
        "email_btn": "Escribir a soporte",
        "privacy_btn": "Política de privacidad",
        "privacy_title": "Política de privacidad — Math Fury",
        "privacy_desc": "Math Fury no recopila datos: sin red, sin analíticas, sin anuncios ni SDKs de terceros. Tus récords se quedan en tu dispositivo.",
        "privacy_heading": "Política de privacidad",
        "privacy_intro": "Math Fury no recopila, almacena ni comparte ningún dato personal.",
        "bullets": [
            "La app no requiere cuenta, registro ni inicio de sesión.",
            "No realiza ninguna conexión de red.",
            "No utiliza analíticas, publicidad ni SDKs de terceros.",
            "No rastrea tu actividad dentro ni fuera de la app.",
        ],
        "privacy_storage": "Tus récords, rachas y estadísticas se guardan solo en tu dispositivo (mediante <code>UserDefaults</code> del sistema) y nunca se envían a ningún servidor. Si desinstalas la app, esos datos se eliminan con ella.",
        "contact_heading": "Contacto",
        "back": "← Math Fury",
    },
    "fr": {
        "support_title": "Math Fury — Assistance",
        "support_desc": "Assistance et contact pour Math Fury, jeu de calcul mental contre la montre. Sans publicité, sans achats, sans collecte de données.",
        "tagline": "Calcul mental contre la montre",
        "clean_line": "Sans pub · Sans achats · Sans données",
        "support_heading": "Assistance",
        "support_body": "Une question, un bug ou une suggestion ? Écrivez-nous, nous vous répondrons :",
        "email_btn": "Contacter l'assistance",
        "privacy_btn": "Politique de confidentialité",
        "privacy_title": "Politique de confidentialité — Math Fury",
        "privacy_desc": "Math Fury ne collecte aucune donnée : pas de réseau, pas d'analyse, pas de publicité ni de SDK tiers. Vos scores restent sur votre appareil.",
        "privacy_heading": "Politique de confidentialité",
        "privacy_intro": "Math Fury ne collecte, ne stocke ni ne partage aucune donnée personnelle.",
        "bullets": [
            "L'application ne nécessite aucun compte, inscription ou connexion.",
            "Elle n'établit aucune connexion réseau.",
            "Elle n'utilise aucune analyse, publicité ni SDK tiers.",
            "Elle ne suit pas votre activité, dans l'application ou en dehors.",
        ],
        "privacy_storage": "Vos meilleurs scores, séries et statistiques sont enregistrés uniquement sur votre appareil (via les <code>UserDefaults</code> du système) et ne sont jamais envoyés à un serveur. Désinstaller l'application supprime ces données.",
        "contact_heading": "Contact",
        "back": "← Math Fury",
    },
    "de": {
        "support_title": "Math Fury — Support",
        "support_desc": "Support und Kontakt für Math Fury, ein Kopfrechen-Spiel gegen die Uhr. Keine Werbung, keine Käufe, keine Datenerfassung.",
        "tagline": "Kopfrechnen gegen die Uhr",
        "clean_line": "Keine Werbung · Keine Käufe · Keine Daten",
        "support_heading": "Support",
        "support_body": "Frage, Fehler gefunden oder ein Vorschlag? Schreib uns, wir melden uns:",
        "email_btn": "Support kontaktieren",
        "privacy_btn": "Datenschutzerklärung",
        "privacy_title": "Datenschutzerklärung — Math Fury",
        "privacy_desc": "Math Fury erfasst keine Daten: kein Netzwerk, keine Analyse, keine Werbung, keine Drittanbieter-SDKs. Deine Punkte bleiben auf deinem Gerät.",
        "privacy_heading": "Datenschutzerklärung",
        "privacy_intro": "Math Fury erfasst, speichert und teilt keine personenbezogenen Daten.",
        "bullets": [
            "Die App erfordert kein Konto, keine Registrierung und keine Anmeldung.",
            "Sie stellt keine Netzwerkverbindungen her.",
            "Sie verwendet keine Analyse, Werbung oder Drittanbieter-SDKs.",
            "Sie verfolgt deine Aktivität nicht, weder in der App noch außerhalb.",
        ],
        "privacy_storage": "Deine Bestwerte, Serien und Statistiken werden nur auf deinem Gerät gespeichert (über die System-<code>UserDefaults</code>) und niemals an einen Server gesendet. Beim Deinstallieren der App werden diese Daten mitgelöscht.",
        "contact_heading": "Kontakt",
        "back": "← Math Fury",
    },
    "it": {
        "support_title": "Math Fury — Assistenza",
        "support_desc": "Assistenza e contatto per Math Fury, gioco di calcolo mentale contro il tempo. Senza pubblicità, senza acquisti, senza raccolta dati.",
        "tagline": "Calcolo mentale contro il tempo",
        "clean_line": "Niente pubblicità · Niente acquisti · Nessun dato",
        "support_heading": "Assistenza",
        "support_body": "Hai una domanda, un bug o un suggerimento? Scrivici e ti risponderemo:",
        "email_btn": "Contatta l'assistenza",
        "privacy_btn": "Informativa sulla privacy",
        "privacy_title": "Informativa sulla privacy — Math Fury",
        "privacy_desc": "Math Fury non raccoglie dati: niente rete, niente analisi, niente pubblicità né SDK di terze parti. I tuoi punteggi restano sul dispositivo.",
        "privacy_heading": "Informativa sulla privacy",
        "privacy_intro": "Math Fury non raccoglie, conserva né condivide alcun dato personale.",
        "bullets": [
            "L'app non richiede account, registrazione o accesso.",
            "Non effettua alcuna connessione di rete.",
            "Non utilizza analisi, pubblicità o SDK di terze parti.",
            "Non traccia la tua attività dentro o fuori dall'app.",
        ],
        "privacy_storage": "I tuoi record, le serie e le statistiche vengono salvati solo sul tuo dispositivo (tramite gli <code>UserDefaults</code> di sistema) e non vengono mai inviati ad alcun server. Disinstallando l'app, quei dati vengono eliminati con essa.",
        "contact_heading": "Contatti",
        "back": "← Math Fury",
    },
    "pt": {
        "support_title": "Math Fury — Apoio",
        "support_desc": "Apoio e contacto da Math Fury, jogo de cálculo mental contra o tempo. Sem anúncios, sem compras, sem recolha de dados.",
        "tagline": "Cálculo mental contra o tempo",
        "clean_line": "Sem anúncios · Sem compras · Sem dados",
        "support_heading": "Apoio",
        "support_body": "Tens uma dúvida, encontraste um erro ou queres sugerir algo? Escreve-nos e respondemos:",
        "email_btn": "Contactar o apoio",
        "privacy_btn": "Política de privacidade",
        "privacy_title": "Política de privacidade — Math Fury",
        "privacy_desc": "A Math Fury não recolhe dados: sem rede, sem análises, sem anúncios nem SDKs de terceiros. As tuas pontuações ficam no teu dispositivo.",
        "privacy_heading": "Política de privacidade",
        "privacy_intro": "A Math Fury não recolhe, armazena nem partilha qualquer dado pessoal.",
        "bullets": [
            "A app não requer conta, registo nem início de sessão.",
            "Não efetua qualquer ligação de rede.",
            "Não utiliza análises, publicidade nem SDKs de terceiros.",
            "Não monitoriza a tua atividade dentro ou fora da app.",
        ],
        "privacy_storage": "As tuas pontuações, sequências e estatísticas são guardadas apenas no teu dispositivo (através das <code>UserDefaults</code> do sistema) e nunca são enviadas para nenhum servidor. Ao desinstalar a app, esses dados são eliminados com ela.",
        "contact_heading": "Contacto",
        "back": "← Math Fury",
    },
}

FOOTER = '<footer>© 2026 Pedro Lorencio · Jose Antonio Lorencio · Juan Pablo Lorencio · Math Fury</footer>'


def support_path(lang): return "/mathfury/" if lang == "en" else f"/mathfury/{lang}/"
def privacy_path(lang): return "/mathfury/privacy/" if lang == "en" else f"/mathfury/{lang}/privacy/"


def switcher(page, current):
    paths = support_path if page == "support" else privacy_path
    rows = []
    for L in LANGS:
        if L == current:
            rows.append(f'<span class="current">{LABELS[L]}</span>')
        else:
            rows.append(f'<a href="{paths(L)}">{LABELS[L]}</a>')
    return "\n".join(rows)


def hreflangs(page):
    paths = support_path if page == "support" else privacy_path
    tags = [f'<link rel="alternate" hreflang="{L}" href="{SITE}{paths(L)}"/>' for L in LANGS]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{paths("en")}"/>')
    return "\n".join(tags)


def head(lang, title, desc, canonical, page):
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="theme-color" content="#0a0d17"/>
<meta name="format-detection" content="telephone=no"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="{canonical}"/>
{hreflangs(page)}
<link rel="stylesheet" href="/mathfury/mathfury.css"/>
</head>"""


def support_page(lang):
    c = C[lang]
    return f"""{head(lang, c['support_title'], c['support_desc'], SITE + support_path(lang), 'support')}
<body>
<div class="wrap">
<nav class="langs" aria-label="Idioma">
{switcher('support', lang)}
</nav>
<div class="wordmark"><span class="math">MATH</span><span class="fury">FURY</span></div>
<p class="tagline">{c['tagline']}</p>
<p class="badge">{c['clean_line']}</p>
<div class="btns">
<a class="btn btn-magenta" href="mailto:support@yosidi.com">{c['email_btn']}</a>
<a class="btn btn-cyan" href="{privacy_path(lang)}">{c['privacy_btn']}</a>
</div>
<h2>{c['support_heading']}</h2>
<p>{c['support_body']} <a href="mailto:support@yosidi.com">support@yosidi.com</a></p>
</div>
{FOOTER}
</body>
</html>
"""


def privacy_page(lang):
    c = C[lang]
    bullets = "\n".join(f"<li>{b}</li>" for b in c["bullets"])
    return f"""{head(lang, c['privacy_title'], c['privacy_desc'], SITE + privacy_path(lang), 'privacy')}
<body>
<div class="wrap">
<nav class="langs" aria-label="Idioma">
{switcher('privacy', lang)}
</nav>
<a class="back" href="{support_path(lang)}">{c['back']}</a>
<h1>{c['privacy_heading']}</h1>
<div class="card">
<p><strong>{c['privacy_intro']}</strong></p>
<ul>
{bullets}
</ul>
<p>{c['privacy_storage']}</p>
<h2>{c['contact_heading']}</h2>
<p><a href="mailto:support@yosidi.com">support@yosidi.com</a></p>
</div>
</div>
{FOOTER}
</body>
</html>
"""


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def main():
    for lang in LANGS:
        sp = OUT / "index.html" if lang == "en" else OUT / lang / "index.html"
        pp = OUT / "privacy" / "index.html" if lang == "en" else OUT / lang / "privacy" / "index.html"
        write(sp, support_page(lang))
        write(pp, privacy_page(lang))
    pages = sorted(str(p.relative_to(OUT.parent)) for p in OUT.rglob("*.html"))
    print(f"OK: {len(pages)} páginas generadas:")
    for p in pages:
        print("  ", p)


if __name__ == "__main__":
    main()
