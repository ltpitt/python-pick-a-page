/**
 * UI Controller
 * 
 * Responsibility: Handle all DOM manipulation and user interactions.
 * Following Single Responsibility Principle - only manages presentation layer.
 * Following Dependency Inversion - depends on StoryManager abstraction.
 */

class UIController {
    constructor(storyManager, i18nService) {
        this.storyManager = storyManager;
        this.i18n = i18nService;
        this.currentPage = 'library';
        this.elements = {};
    }

    /**
     * Initialize UI and cache DOM elements
     */
    init() {
        this._cacheElements();
        this._setupEventListeners();
        this._setupNavigation();
    }

    /**
     * Cache frequently used DOM elements
     * @private
     */
    _cacheElements() {
        this.elements = {
            // Navigation
            bookmarks: document.querySelectorAll('.bookmark'),
            pages: document.querySelectorAll('.page'),
            playerBookmark: document.getElementById('playerBookmark'),
            languageSelector: document.getElementById('languageSelector'),
            
            // Library page
            storyList: document.getElementById('storyList'),
            message: document.getElementById('message'),
            playBtn: document.getElementById('playBtn'),
            editLibraryBtn: document.getElementById('editLibraryBtn'),
            newStoryBtn: document.getElementById('newStoryBtn'),
            
            // Editor page
            storyEditor: document.getElementById('storyEditor'),
            editorTitle: document.getElementById('editorTitle'),
            editorMessage: document.getElementById('editorMessage'),
            validateBtn: document.getElementById('validateBtn'),
            saveBtn: document.getElementById('saveBtn'),
            compileBtn: document.getElementById('compileBtn'),
            
            // Player page
            storyPlayer: document.getElementById('storyPlayer')
        };
    }

    /**
     * Setup event listeners
     * @private
     */
    _setupEventListeners() {
        // Language selector
        this.elements.languageSelector.addEventListener('change', (e) => {
            this._handleLanguageChange(e.target.value);
        });

        // Library buttons
        this.elements.playBtn.addEventListener('click', () => this._handlePlayStory());
        this.elements.editLibraryBtn.addEventListener('click', () => this._handleEditFromLibrary());
        this.elements.newStoryBtn.addEventListener('click', () => this._handleNewStory());

        // Editor buttons
        this.elements.validateBtn.addEventListener('click', () => this._handleValidateStory());
        this.elements.saveBtn.addEventListener('click', () => this._handleSaveStory());
        this.elements.compileBtn.addEventListener('click', () => this._handleCompileAndPlay());
    }

    /**
     * Setup page navigation
     * @private
     */
    _setupNavigation() {
        this.elements.bookmarks.forEach(bookmark => {
            bookmark.addEventListener('click', () => {
                const targetPage = bookmark.dataset.page;
                this.switchPage(targetPage);
            });
        });
    }

    /**
     * Switch to a different page
     * @param {string} pageName - Page to switch to ('library', 'editor', 'player')
     */
    switchPage(pageName) {
        // Update bookmarks
        this.elements.bookmarks.forEach(b => {
            b.classList.toggle('active', b.dataset.page === pageName);
        });

        // Show player bookmark if switching to player
        if (pageName === 'player') {
            this.elements.playerBookmark.style.display = 'block';
        }

        // Update pages
        this.elements.pages.forEach(p => {
            p.classList.toggle('active', p.id === `page-${pageName}`);
        });

        this.currentPage = pageName;

        // Refresh story list when switching to library
        if (pageName === 'library') {
            this.loadStories();
        }
    }

    /**
     * Load and display stories
     */
    async loadStories() {
        const listEl = this.elements.storyList;
        
        // Show loading state
        listEl.innerHTML = `
            <div class="loading active">
                <div class="spinner"></div>
                <p data-i18n="web_loading_stories">${this.i18n.t('web_loading_stories')}</p>
            </div>
        `;

        try {
            const stories = await this.storyManager.loadStories();
            listEl.innerHTML = '';

            if (stories.length === 0) {
                this._renderEmptyState(listEl);
            } else {
                this._renderStoryGrid(listEl, stories);
            }
        } catch (error) {
            this.showMessage(this.i18n.t('web_msg_error') + ': ' + error.message, 'error');
        }
    }

    /**
     * Render empty state
     * @private
     */
    _renderEmptyState(container) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📚</div>
                <h3>${this.i18n.t('web_empty_title')}</h3>
                <p>${this.i18n.t('web_empty_text')}</p>
            </div>
        `;
    }

    /**
     * Render story grid
     * @private
     */
    _renderStoryGrid(container, stories) {
        const grid = document.createElement('div');
        grid.className = 'story-grid';

        stories.forEach(story => {
            const card = this._createStoryCard(story);
            grid.appendChild(card);
        });

        container.appendChild(grid);
    }

    /**
     * Create a story card element
     * @private
     */
    _createStoryCard(story) {
        const card = document.createElement('div');
        card.className = 'story-card';
        card.innerHTML = `
            <button class="story-card-delete" 
                    title="${this.i18n.t('web_btn_delete')}" 
                    data-filename="${story.filename}"
                    aria-label="${this.i18n.t('web_btn_delete')} ${story.title}">✕</button>
            <div class="story-card-title">${this._escapeHtml(story.title)}</div>
            <div class="story-card-meta">${this.i18n.t('web_by')} ${this._escapeHtml(story.author)}</div>
            <div class="story-card-meta">${story.sections || '?'} ${this.i18n.t('web_sections')}</div>
        `;

        // Single click to select
        card.addEventListener('click', (e) => {
            if (!e.target.classList.contains('story-card-delete')) {
                this._selectStoryCard(story, card);
            }
        });

        // Double click to play
        card.addEventListener('dblclick', (e) => {
            if (!e.target.classList.contains('story-card-delete')) {
                this._selectStoryCard(story, card);
                this._handlePlayStory();
            }
        });

        // Delete button
        const deleteBtn = card.querySelector('.story-card-delete');
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this._handleDeleteStory(story.filename, story.title);
        });

        return card;
    }

    /**
     * Select a story card
     * @private
     */
    _selectStoryCard(story, element) {
        // Deselect all cards
        document.querySelectorAll('.story-card').forEach(c => 
            c.classList.remove('selected')
        );

        // Select this card
        element.classList.add('selected');
        this.storyManager.selectStory(story);

        // Enable action buttons
        this.elements.playBtn.disabled = false;
        this.elements.editLibraryBtn.disabled = false;
    }

    /**
     * Show message in library
     * @param {string} text - Message text
     * @param {string} type - Message type ('success', 'error', 'info')
     */
    showMessage(text, type) {
        this._showMessageInElement(this.elements.message, text, type);
    }

    /**
     * Show message in editor
     * @param {string} text - Message text
     * @param {string} type - Message type ('success', 'error', 'info')
     */
    showEditorMessage(text, type) {
        this._showMessageInElement(this.elements.editorMessage, text, type);
    }

    /**
     * Show message in a specific element
     * @private
     */
    _showMessageInElement(element, text, type) {
        element.textContent = text;
        element.className = `message ${type} active`;
        
        setTimeout(() => {
            element.classList.remove('active');
        }, 5000);
    }

    /**
     * Event Handlers
     */

    async _handleLanguageChange(lang) {
        try {
            await this.i18n.loadLanguage(lang);
            // Refresh current page to update translations
            if (this.currentPage === 'library') {
                await this.loadStories();
            }
        } catch (error) {
            this.showMessage(this.i18n.t('web_msg_error') + ': ' + error.message, 'error');
        }
    }

    async _handlePlayStory() {
        const selected = this.storyManager.getSelectedStory();
        if (!selected) return;

        this.showMessage(this.i18n.t('web_msg_loading'), 'info');

        try {
            const result = await this.storyManager.playSelectedStory();
            
            if (result.success) {
                this.elements.storyPlayer.src = result.play_url;
                this.elements.storyPlayer.classList.add('active');
                this.switchPage('player');
            } else {
                this.showMessage(
                    this.i18n.t('web_msg_errors') + ': ' + 
                    (result.errors || [result.error]).join(', '), 
                    'error'
                );
            }
        } catch (error) {
            this.showMessage(this.i18n.t('web_msg_error') + ': ' + error.message, 'error');
        }
    }

    async _handleEditFromLibrary() {
        const selected = this.storyManager.getSelectedStory();
        if (!selected) return;

        try {
            const content = await this.storyManager.loadStoryForEditing(selected);
            this.elements.storyEditor.value = content;
            this.elements.editorTitle.textContent = 
                `✏️ ${this.i18n.t('web_editing')}: ${selected.title}`;
            this.showEditorMessage(
                `${this.i18n.t('web_msg_loaded')} ${selected.filename}`, 
                'success'
            );
            this.switchPage('editor');
        } catch (error) {
            this.showEditorMessage(this.i18n.t('web_msg_error') + ': ' + error.message, 'error');
        }
    }

    _handleNewStory() {
        this.elements.storyEditor.value = this.storyManager.getNewStoryTemplate();
        this.elements.editorTitle.textContent = '✨ ' + this.i18n.t('web_title_editor');
        this.storyManager.clearEditingState();
        this.showEditorMessage(this.i18n.t('web_msg_ready'), 'info');
        this.switchPage('editor');
    }

    async _handleValidateStory() {
        const content = this.elements.storyEditor.value;

        try {
            const result = await this.storyManager.validateStory(content);
            
            if (result.valid) {
                this.showEditorMessage(
                    `✓ ${this.i18n.t('web_msg_valid')} ${result.sections} ${this.i18n.t('web_sections')}.`, 
                    'success'
                );
            } else {
                this.showEditorMessage(
                    this.i18n.t('web_msg_validation_errors') + ': ' + 
                    (result.errors || [result.error]).join(', '), 
                    'error'
                );
            }
        } catch (error) {
            this.showEditorMessage(this.i18n.t('web_msg_error') + ': ' + error.message, 'error');
        }
    }

    async _handleSaveStory() {
        const content = this.elements.storyEditor.value;
        
        const filename = prompt(
            this.i18n.t('web_prompt_save'), 
            this.storyManager.getCurrentEditingFilename() || 'my_story.txt'
        );
        
        if (!filename) return;

        try {
            const result = await this.storyManager.saveStory(content, filename);
            
            if (result.success) {
                this.showEditorMessage(
                    `✓ ${this.i18n.t('web_msg_saved')} ${result.filename}!`, 
                    'success'
                );
            } else {
                this.showEditorMessage(
                    this.i18n.t('web_msg_error') + ': ' + 
                    (result.error || this.i18n.t('web_msg_unknown_error')), 
                    'error'
                );
            }
        } catch (error) {
            this.showEditorMessage(this.i18n.t('web_msg_error') + ': ' + error.message, 'error');
        }
    }

    async _handleCompileAndPlay() {
        const content = this.elements.storyEditor.value;

        this.showEditorMessage(this.i18n.t('web_msg_compiling'), 'info');

        try {
            const result = await this.storyManager.compileStory(content);
            
            if (result.success) {
                this.elements.storyPlayer.src = result.play_url;
                this.elements.storyPlayer.classList.add('active');
                this.switchPage('player');
            } else {
                this.showEditorMessage(
                    this.i18n.t('web_msg_compilation_errors') + ': ' + 
                    (result.errors || [result.error]).join(', '), 
                    'error'
                );
            }
        } catch (error) {
            this.showEditorMessage(this.i18n.t('web_msg_error') + ': ' + error.message, 'error');
        }
    }

    async _handleDeleteStory(filename, title) {
        const confirmMsg = this.i18n.t('web_confirm_delete').replace('{title}', title);
        if (!confirm(confirmMsg)) return;

        try {
            const result = await this.storyManager.deleteStory(filename);
            
            if (result.success) {
                this.showMessage(
                    `✓ ${this.i18n.t('web_msg_deleted')} ${title}`, 
                    'success'
                );
                this.elements.playBtn.disabled = true;
                this.elements.editLibraryBtn.disabled = true;
                await this.loadStories();
            } else {
                this.showMessage(
                    this.i18n.t('web_msg_error') + ': ' + 
                    (result.error || this.i18n.t('web_msg_unknown_error')), 
                    'error'
                );
            }
        } catch (error) {
            this.showMessage(this.i18n.t('web_msg_error') + ': ' + error.message, 'error');
        }
    }

    /**
     * Utility: Escape HTML to prevent XSS
     * @private
     */
    _escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Export for use in other modules
window.UIController = UIController;
