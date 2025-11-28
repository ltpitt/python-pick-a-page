/**
 * Internationalization Service - Legacy Browser Compatible Version
 * 
 * This version uses Promise chains instead of async/await for Firefox 52 ESR compatibility.
 * 
 * Responsibility: Handle language switching and translations.
 * Following Single Responsibility Principle - only manages i18n.
 * Following Open/Closed Principle - easy to extend with new languages.
 */

var I18nService = (function() {
    'use strict';
    
    function I18nService(apiService) {
        this.apiService = apiService;
        this.currentLanguage = localStorage.getItem('language') || 'en';
        this.translations = {};
        this.availableLanguages = {};
    }

    /**
     * Initialize i18n service
     * @returns {Promise<void>}
     */
    I18nService.prototype.init = function() {
        var self = this;
        return this.loadAvailableLanguages()
            .then(function() {
                return self.loadLanguage(self.currentLanguage);
            });
    };

    /**
     * Load all available languages
     * @returns {Promise<void>}
     */
    I18nService.prototype.loadAvailableLanguages = function() {
        var self = this;
        return this.apiService.getLanguages()
            .then(function(data) {
                self.availableLanguages = data.languages;
            })
            .catch(function(error) {
                console.error('Error loading languages:', error);
                throw error;
            });
    };

    /**
     * Load translations for a specific language
     * @param {string} lang - Language code
     * @returns {Promise<void>}
     */
    I18nService.prototype.loadLanguage = function(lang) {
        var self = this;
        return this.apiService.getTranslations(lang)
            .then(function(data) {
                self.translations = data.translations;
                self.currentLanguage = lang;
                localStorage.setItem('language', lang);
                
                // Update all translated elements in DOM
                self._updateTranslations();
            })
            .catch(function(error) {
                console.error('Error loading language:', error);
                throw error;
            });
    };

    /**
     * Get translation for a key
     * @param {string} key - Translation key
     * @returns {string} Translated text or key if not found
     */
    I18nService.prototype.t = function(key) {
        return this.translations[key] || key;
    };

    /**
     * Get current language code
     * @returns {string}
     */
    I18nService.prototype.getCurrentLanguage = function() {
        return this.currentLanguage;
    };

    /**
     * Get all available languages
     * @returns {Object}
     */
    I18nService.prototype.getAvailableLanguages = function() {
        return this.availableLanguages;
    };

    /**
     * Update all DOM elements with data-i18n attributes
     * @private
     */
    I18nService.prototype._updateTranslations = function() {
        var self = this;
        
        // Update text content
        var elements = document.querySelectorAll('[data-i18n]');
        for (var i = 0; i < elements.length; i++) {
            var element = elements[i];
            var key = element.getAttribute('data-i18n');
            if (self.translations[key]) {
                element.textContent = self.translations[key];
            }
        }

        // Update placeholders
        var placeholderElements = document.querySelectorAll('[data-i18n-placeholder]');
        for (var j = 0; j < placeholderElements.length; j++) {
            var el = placeholderElements[j];
            var placeholderKey = el.getAttribute('data-i18n-placeholder');
            if (self.translations[placeholderKey]) {
                el.placeholder = self.translations[placeholderKey];
            }
        }
    };

    /**
     * Populate language selector dropdown
     * @param {HTMLSelectElement} selector - Select element
     */
    I18nService.prototype.populateLanguageSelector = function(selector) {
        var self = this;
        selector.innerHTML = '';
        
        // Sort by native language name
        var sortedCodes = Object.keys(this.availableLanguages).sort(function(a, b) {
            return self.availableLanguages[a].name.localeCompare(
                self.availableLanguages[b].name
            );
        });

        for (var i = 0; i < sortedCodes.length; i++) {
            var code = sortedCodes[i];
            var lang = self.availableLanguages[code];
            var option = document.createElement('option');
            option.value = code;
            option.textContent = lang.flag + ' ' + lang.name;
            selector.appendChild(option);
        }

        selector.value = this.currentLanguage;
    };

    return I18nService;
})();

// Export for use in other modules
window.I18nService = I18nService;
