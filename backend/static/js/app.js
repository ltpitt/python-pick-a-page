/**
 * Main Application Entry Point
 * 
 * Responsibility: Initialize and wire up all services and controllers.
 * Following Dependency Injection principle - creates instances and injects dependencies.
 * Following Single Responsibility - only handles application bootstrapping.
 */

class Application {
    constructor() {
        this.apiService = null;
        this.i18nService = null;
        this.storyManager = null;
        this.uiController = null;
    }

    /**
     * Initialize the application
     */
    async init() {
        try {
            // Create service instances with dependency injection
            this.apiService = new ApiService();
            this.i18nService = new I18nService(this.apiService);
            this.storyManager = new StoryManager(this.apiService, this.i18nService);
            this.uiController = new UIController(this.storyManager, this.i18nService);

            // Initialize i18n (load languages and translations)
            await this.i18nService.init();

            // Populate language selector
            const languageSelector = document.getElementById('languageSelector');
            this.i18nService.populateLanguageSelector(languageSelector);

            // Initialize UI
            this.uiController.init();

            // Load initial data
            await this.uiController.loadStories();

            console.log('✅ Application initialized successfully');
        } catch (error) {
            console.error('❌ Application initialization failed:', error);
            this._showCriticalError(error);
        }
    }

    /**
     * Show critical error to user
     * @private
     */
    _showCriticalError(error) {
        const container = document.querySelector('.container');
        if (container) {
            container.innerHTML = `
                <div class="book">
                    <div class="message error active">
                        <strong>Application Error:</strong> ${error.message}
                        <br><br>
                        Please refresh the page or contact support if the problem persists.
                    </div>
                </div>
            `;
        }
    }
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const app = new Application();
    app.init();
});

// Export for debugging/testing
window.Application = Application;
