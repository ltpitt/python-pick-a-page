/**
 * Main Application Entry Point - Legacy Browser Compatible Version
 * 
 * This version uses Promise chains instead of async/await for Firefox 52 ESR compatibility.
 * 
 * Responsibility: Initialize and wire up all services and controllers.
 * Following Dependency Injection principle - creates instances and injects dependencies.
 * Following Single Responsibility - only handles application bootstrapping.
 */

var Application = (function() {
    'use strict';
    
    function Application() {
        this.apiService = null;
        this.i18nService = null;
        this.storyManager = null;
        this.uiController = null;
    }

    /**
     * Initialize the application
     */
    Application.prototype.init = function() {
        var self = this;
        
        try {
            // Create service instances with dependency injection
            this.apiService = new ApiService();
            this.i18nService = new I18nService(this.apiService);
            this.storyManager = new StoryManager(this.apiService, this.i18nService);
            this.uiController = new UIController(this.storyManager, this.i18nService);

            // Initialize i18n (load languages and translations)
            this.i18nService.init()
                .then(function() {
                    // Populate language selector
                    var languageSelector = document.getElementById('languageSelector');
                    self.i18nService.populateLanguageSelector(languageSelector);

                    // Initialize UI
                    self.uiController.init();

                    // Load initial data
                    return self.uiController.loadStories();
                })
                .then(function() {
                    console.log('✅ Application initialized successfully (Legacy mode)');
                })
                .catch(function(error) {
                    console.error('❌ Application initialization failed:', error);
                    self._showCriticalError(error);
                });
        } catch (error) {
            console.error('❌ Application initialization failed:', error);
            this._showCriticalError(error);
        }
    };

    /**
     * Show critical error to user
     * @private
     */
    Application.prototype._showCriticalError = function(error) {
        var container = document.querySelector('.container');
        if (container) {
            container.innerHTML = 
                '<div class="book">' +
                    '<div class="message error active">' +
                        '<strong>Application Error:</strong> ' + error.message +
                        '<br><br>' +
                        'Please refresh the page or contact support if the problem persists.' +
                    '</div>' +
                '</div>';
        }
    };

    return Application;
})();

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    var app = new Application();
    app.init();
});

// Export for debugging/testing
window.Application = Application;
