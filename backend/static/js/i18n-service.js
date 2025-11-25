/**
 * Internationalization Service
 * 
 * Responsibility: Handle language switching and translations.
 * Following Single Responsibility Principle - only manages i18n.
 * Following Open/Closed Principle - easy to extend with new languages.
 */

class I18nService {
    constructor(apiService) {
        this.apiService = apiService;
        this.currentLanguage = localStorage.getItem('language') || 'en';
        this.translations = {};
        this.availableLanguages = {};
    }

    /**
     * Initialize i18n service
     * @returns {Promise<void>}
     */
    async init() {
        await this.loadAvailableLanguages();
        await this.loadLanguage(this.currentLanguage);
    }

    /**
     * Load all available languages
     * @returns {Promise<void>}
     */
    async loadAvailableLanguages() {
        try {
            const data = await this.apiService.getLanguages();
            this.availableLanguages = data.languages;
        } catch (error) {
            console.error('Error loading languages:', error);
            throw error;
        }
    }

    /**
     * Load translations for a specific language
     * @param {string} lang - Language code
     * @returns {Promise<void>}
     */
    async loadLanguage(lang) {
        try {
            const data = await this.apiService.getTranslations(lang);
            this.translations = data.translations;
            this.currentLanguage = lang;
            localStorage.setItem('language', lang);
            
            // Update all translated elements in DOM
            this._updateTranslations();
        } catch (error) {
            console.error('Error loading language:', error);
            throw error;
        }
    }

    /**
     * Get translation for a key
     * @param {string} key - Translation key
     * @returns {string} Translated text or key if not found
     */
    t(key) {
        return this.translations[key] || key;
    }

    /**
     * Get current language code
     * @returns {string}
     */
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    /**
     * Get all available languages
     * @returns {Object}
     */
    getAvailableLanguages() {
        return this.availableLanguages;
    }

    /**
     * Update all DOM elements with data-i18n attributes
     * @private
     */
    _updateTranslations() {
        // Update text content
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (this.translations[key]) {
                element.textContent = this.translations[key];
            }
        });

        // Update placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            if (this.translations[key]) {
                element.placeholder = this.translations[key];
            }
        });
    }

    /**
     * Populate language selector dropdown
     * @param {HTMLSelectElement} selector - Select element
     */
    populateLanguageSelector(selector) {
        selector.innerHTML = '';
        
        // Sort by native language name
        const sortedCodes = Object.keys(this.availableLanguages).sort((a, b) => {
            return this.availableLanguages[a].name.localeCompare(
                this.availableLanguages[b].name
            );
        });

        sortedCodes.forEach(code => {
            const lang = this.availableLanguages[code];
            const option = document.createElement('option');
            option.value = code;
            option.textContent = `${lang.flag} ${lang.name}`;
            selector.appendChild(option);
        });

        selector.value = this.currentLanguage;
    }
}

// Export for use in other modules
window.I18nService = I18nService;
