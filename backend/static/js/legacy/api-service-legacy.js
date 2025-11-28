/**
 * API Service Layer - Legacy Browser Compatible Version
 * 
 * This version uses Promise chains instead of async/await and
 * Object.assign instead of spread operators for Firefox 52 ESR compatibility.
 * 
 * Responsibility: Handle all HTTP communication with backend API.
 * Following Single Responsibility Principle - only handles data fetching/posting.
 * Following Dependency Inversion - returns data structures, doesn't manipulate DOM.
 */

var ApiService = (function() {
    'use strict';
    
    function ApiService(baseUrl) {
        this.baseUrl = baseUrl || '';
    }

    /**
     * Generic fetch wrapper with error handling
     * @private
     */
    ApiService.prototype._fetch = function(endpoint, options) {
        var self = this;
        options = options || {};
        
        var fetchOptions = Object.assign({}, options, {
            headers: Object.assign({
                'Content-Type': 'application/json'
            }, options.headers || {})
        });

        return fetch(self.baseUrl + endpoint, fetchOptions)
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('HTTP ' + response.status + ': ' + response.statusText);
                }
                return response.json();
            })
            .catch(function(error) {
                console.error('API Error [' + endpoint + ']:', error);
                throw error;
            });
    };

    /**
     * Get list of all available stories
     * @returns {Promise<Array>} Array of story objects
     */
    ApiService.prototype.getStories = function() {
        return this._fetch('/api/stories', {
            cache: 'no-cache'
        });
    };

    /**
     * Get content of a specific story
     * @param {string} filename - Story filename
     * @returns {Promise<Object>} Story content and metadata
     */
    ApiService.prototype.getStoryContent = function(filename) {
        return this._fetch('/api/story/' + encodeURIComponent(filename));
    };

    /**
     * Save story to file
     * @param {string} content - Story content
     * @param {string} filename - Filename to save as
     * @returns {Promise<Object>} Save result
     */
    ApiService.prototype.saveStory = function(content, filename) {
        return this._fetch('/api/save', {
            method: 'POST',
            body: JSON.stringify({ content: content, filename: filename })
        });
    };

    /**
     * Delete a story
     * @param {string} filename - Story filename to delete
     * @returns {Promise<Object>} Delete result
     */
    ApiService.prototype.deleteStory = function(filename) {
        return this._fetch('/api/delete', {
            method: 'POST',
            body: JSON.stringify({ filename: filename })
        });
    };

    /**
     * Validate story structure
     * @param {string} content - Story content to validate
     * @returns {Promise<Object>} Validation result
     */
    ApiService.prototype.validateStory = function(content) {
        return this._fetch('/api/validate', {
            method: 'POST',
            body: JSON.stringify({ content: content })
        });
    };

    /**
     * Compile story to HTML
     * @param {string} content - Story content
     * @param {string} filename - Story filename
     * @returns {Promise<Object>} Compilation result with play_url
     */
    ApiService.prototype.compileStory = function(content, filename) {
        return this._fetch('/api/compile', {
            method: 'POST',
            body: JSON.stringify({ content: content, filename: filename })
        });
    };

    /**
     * Get available languages
     * @returns {Promise<Object>} Languages object
     */
    ApiService.prototype.getLanguages = function() {
        return this._fetch('/api/languages');
    };

    /**
     * Get translations for a specific language
     * @param {string} lang - Language code (e.g., 'en', 'nl')
     * @returns {Promise<Object>} Translations object
     */
    ApiService.prototype.getTranslations = function(lang) {
        return this._fetch('/api/translations/' + encodeURIComponent(lang));
    };

    return ApiService;
})();

// Export for use in other modules
window.ApiService = ApiService;
