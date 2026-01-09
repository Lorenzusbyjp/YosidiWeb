/**
 * YoSiDi CAD - Internationalization System
 * Simple i18n implementation using JSON locale files
 */

// ========================================
// i18n Configuration
// ========================================
const i18n = {
    currentLang: 'es', // Default language
    translations: {},
    defaultLang: 'es'
};

// ========================================
// Initialize i18n
// ========================================
async function initI18n() {
    // Get saved language preference or detect browser language
    const savedLang = localStorage.getItem('preferred-language');
    const browserLang = navigator.language.split('-')[0]; // Get 'es' from 'es-ES'

    // Determine initial language
    let initialLang = savedLang || browserLang;

    // Fallback to default if not supported
    const supportedLangs = ['es', 'en'];
    if (!supportedLangs.includes(initialLang)) {
        initialLang = i18n.defaultLang;
    }

    // Load the initial language
    await loadLanguage(initialLang);

    // Set up language switcher buttons
    setupLanguageSwitcher();
}

// ========================================
// Load Language File
// ========================================
async function loadLanguage(lang) {
    try {
        const response = await fetch(`./locales/${lang}.json`);

        if (!response.ok) {
            throw new Error(`Failed to load language file: ${lang}.json`);
        }

        const translations = await response.json();
        i18n.translations = translations;
        i18n.currentLang = lang;

        // Update the page with translations
        updatePageContent();

        // Save preference
        localStorage.setItem('preferred-language', lang);

        // Update language switcher buttons
        updateLanguageSwitcher(lang);

        // Update HTML lang attribute
        document.documentElement.lang = lang;

    } catch (error) {
        console.error('Error loading language:', error);

        // Fallback to default language if current language fails
        if (lang !== i18n.defaultLang) {
            console.warn(`Falling back to default language: ${i18n.defaultLang}`);
            loadLanguage(i18n.defaultLang);
        }
    }
}

// ========================================
// Update Page Content with Translations
// ========================================
function updatePageContent() {
    // Find all elements with data-i18n attribute
    const elements = document.querySelectorAll('[data-i18n]');

    elements.forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = getTranslation(key);

        if (translation) {
            // Check if it's a meta tag
            if (element.tagName === 'META') {
                element.setAttribute('content', translation);
            } else if (element.tagName === 'TITLE') {
                element.textContent = translation;
            } else {
                element.textContent = translation;
            }
        }
    });
}

// ========================================
// Get Translation by Key
// ========================================
function getTranslation(key) {
    // Split the key by dots to access nested objects
    // Example: 'hero.title' -> translations.hero.title
    const keys = key.split('.');
    let translation = i18n.translations;

    for (const k of keys) {
        if (translation && typeof translation === 'object' && k in translation) {
            translation = translation[k];
        } else {
            console.warn(`Translation not found for key: ${key}`);
            return key; // Return the key itself if translation not found
        }
    }

    return translation;
}

// ========================================
// Setup Language Switcher Buttons
// ========================================
function setupLanguageSwitcher() {
    const langButtons = document.querySelectorAll('.lang-btn');

    langButtons.forEach(button => {
        button.addEventListener('click', () => {
            const lang = button.id.replace('lang-', ''); // Extract language code from ID
            loadLanguage(lang);
        });
    });
}

// ========================================
// Update Language Switcher Active State
// ========================================
function updateLanguageSwitcher(lang) {
    const langButtons = document.querySelectorAll('.lang-btn');

    langButtons.forEach(button => {
        const buttonLang = button.id.replace('lang-', '');

        if (buttonLang === lang) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
}

// ========================================
// Get Current Language
// ========================================
function getCurrentLanguage() {
    return i18n.currentLang;
}

// ========================================
// Initialize when DOM is ready
// ========================================
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initI18n);
} else {
    // DOM is already ready
    initI18n();
}

// ========================================
// Export functions for use in other scripts (optional)
// ========================================
window.i18n = {
    loadLanguage,
    getTranslation,
    getCurrentLanguage
};
