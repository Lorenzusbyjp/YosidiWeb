/**
 * YOSIDI CAD — Language switcher (post multilang migration).
 *
 * The site is now pre-rendered per language (/, /es/, /fr/, /de/, /it/, /pt/).
 * Each language link in the switcher is a real <a href> that navigates to the
 * equivalent page in that language. This script only:
 *   1. Toggles the dropdown open/closed when clicking the current-language button.
 *   2. Persists the chosen language in localStorage so the root page can honor
 *      it next time without re-detecting via navigator.language.
 */

(function () {
    function setupLanguageSwitcher() {
        const switcher = document.querySelector('.language-switcher');
        const currentBtn = document.querySelector('.lang-current');
        if (!switcher || !currentBtn) return;

        currentBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            const open = switcher.classList.toggle('open');
            currentBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
        });

        document.addEventListener('click', function () {
            switcher.classList.remove('open');
            currentBtn.setAttribute('aria-expanded', 'false');
        });

        document.querySelectorAll('.lang-btn').forEach(function (link) {
            link.addEventListener('click', function () {
                const id = link.id || '';
                const lang = id.replace('lang-', '');
                if (lang) {
                    try { localStorage.setItem('preferred-lang', lang); } catch (e) {}
                }
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupLanguageSwitcher);
    } else {
        setupLanguageSwitcher();
    }
})();
