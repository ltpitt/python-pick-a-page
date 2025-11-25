/**
 * API Service Layer
 * 
 * Responsibility: Handle all HTTP communication with backend API.
 * Following Single Responsibility Principle - only handles data fetching/posting.
 * Following Dependency Inversion - returns data structures, doesn't manipulate DOM.
 */

class ApiService {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }

    /**
     * Generic fetch wrapper with error handling
     * @private
     */
    async _fetch(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    }

    /**
     * Get list of all available stories
     * @returns {Promise<Array>} Array of story objects
     */
    async getStories() {
        return this._fetch('/api/stories', {
            cache: 'no-cache'
        });
    }

    /**
     * Get content of a specific story
     * @param {string} filename - Story filename
     * @returns {Promise<Object>} Story content and metadata
     */
    async getStoryContent(filename) {
        return this._fetch(`/api/story/${encodeURIComponent(filename)}`);
    }

    /**
     * Save story to file
     * @param {string} content - Story content
     * @param {string} filename - Filename to save as
     * @returns {Promise<Object>} Save result
     */
    async saveStory(content, filename) {
        return this._fetch('/api/save', {
            method: 'POST',
            body: JSON.stringify({ content, filename })
        });
    }

    /**
     * Delete a story
     * @param {string} filename - Story filename to delete
     * @returns {Promise<Object>} Delete result
     */
    async deleteStory(filename) {
        return this._fetch('/api/delete', {
            method: 'POST',
            body: JSON.stringify({ filename })
        });
    }

    /**
     * Validate story structure
     * @param {string} content - Story content to validate
     * @returns {Promise<Object>} Validation result
     */
    async validateStory(content) {
        return this._fetch('/api/validate', {
            method: 'POST',
            body: JSON.stringify({ content })
        });
    }

    /**
     * Compile story to HTML
     * @param {string} content - Story content
     * @param {string} filename - Story filename
     * @returns {Promise<Object>} Compilation result with play_url
     */
    async compileStory(content, filename) {
        return this._fetch('/api/compile', {
            method: 'POST',
            body: JSON.stringify({ content, filename })
        });
    }

    /**
     * Get available languages
     * @returns {Promise<Object>} Languages object
     */
    async getLanguages() {
        return this._fetch('/api/languages');
    }

    /**
     * Get translations for a specific language
     * @param {string} lang - Language code (e.g., 'en', 'nl')
     * @returns {Promise<Object>} Translations object
     */
    async getTranslations(lang) {
        return this._fetch(`/api/translations/${encodeURIComponent(lang)}`);
    }
}

// Export for use in other modules
window.ApiService = ApiService;
