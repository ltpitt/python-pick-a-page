/**
 * UI Controller - Legacy Browser Compatible Version
 * 
 * This version uses Promise chains instead of async/await for Firefox 52 ESR compatibility.
 * Uses for loops instead of forEach with arrow functions for compatibility.
 * 
 * Responsibility: Handle all DOM manipulation and user interactions.
 * Following Single Responsibility Principle - only manages presentation layer.
 * Following Dependency Inversion - depends on StoryManager abstraction.
 */

var UIController = (function() {
    'use strict';
    
    function UIController(storyManager, i18nService) {
        this.storyManager = storyManager;
        this.i18n = i18nService;
        this.currentPage = 'library';
        this.elements = {};
    }

    /**
     * Initialize UI and cache DOM elements
     */
    UIController.prototype.init = function() {
        this._cacheElements();
        this._setupEventListeners();
        this._setupNavigation();
    };

    /**
     * Cache frequently used DOM elements
     * @private
     */
    UIController.prototype._cacheElements = function() {
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
    };

    /**
     * Setup event listeners
     * @private
     */
    UIController.prototype._setupEventListeners = function() {
        var self = this;
        
        // Language selector
        this.elements.languageSelector.addEventListener('change', function(e) {
            self._handleLanguageChange(e.target.value);
        });

        // Library buttons
        this.elements.playBtn.addEventListener('click', function() {
            self._handlePlayStory();
        });
        this.elements.editLibraryBtn.addEventListener('click', function() {
            self._handleEditFromLibrary();
        });
        this.elements.newStoryBtn.addEventListener('click', function() {
            self._handleNewStory();
        });

        // Editor buttons
        this.elements.validateBtn.addEventListener('click', function() {
            self._handleValidateStory();
        });
        this.elements.saveBtn.addEventListener('click', function() {
            self._handleSaveStory();
        });
        this.elements.compileBtn.addEventListener('click', function() {
            self._handleCompileAndPlay();
        });
    };

    /**
     * Setup page navigation
     * @private
     */
    UIController.prototype._setupNavigation = function() {
        var self = this;
        var bookmarks = this.elements.bookmarks;
        
        for (var i = 0; i < bookmarks.length; i++) {
            (function(bookmark) {
                bookmark.addEventListener('click', function() {
                    var targetPage = bookmark.dataset.page;
                    self.switchPage(targetPage);
                });
            })(bookmarks[i]);
        }
    };

    /**
     * Switch to a different page
     * @param {string} pageName - Page to switch to ('library', 'editor', 'player')
     */
    UIController.prototype.switchPage = function(pageName) {
        var self = this;
        var bookmarks = this.elements.bookmarks;
        var pages = this.elements.pages;
        
        // Update bookmarks
        for (var i = 0; i < bookmarks.length; i++) {
            var b = bookmarks[i];
            if (b.dataset.page === pageName) {
                b.classList.add('active');
            } else {
                b.classList.remove('active');
            }
        }

        // Show player bookmark if switching to player
        if (pageName === 'player') {
            this.elements.playerBookmark.style.display = 'block';
        }

        // Update pages
        for (var j = 0; j < pages.length; j++) {
            var p = pages[j];
            if (p.id === 'page-' + pageName) {
                p.classList.add('active');
            } else {
                p.classList.remove('active');
            }
        }

        this.currentPage = pageName;

        // Refresh story list when switching to library
        if (pageName === 'library') {
            this.loadStories();
        }
    };

    /**
     * Load and display stories
     */
    UIController.prototype.loadStories = function() {
        var self = this;
        var listEl = this.elements.storyList;
        
        // Show loading state
        listEl.innerHTML = 
            '<div class="loading active">' +
                '<div class="spinner"></div>' +
                '<p data-i18n="web_loading_stories">' + this.i18n.t('web_loading_stories') + '</p>' +
            '</div>';

        return this.storyManager.loadStories()
            .then(function(stories) {
                listEl.innerHTML = '';

                if (stories.length === 0) {
                    self._renderEmptyState(listEl);
                } else {
                    self._renderStoryGrid(listEl, stories);
                }
            })
            .catch(function(error) {
                self.showMessage(self.i18n.t('web_msg_error') + ': ' + error.message, 'error');
            });
    };

    /**
     * Render empty state
     * @private
     */
    UIController.prototype._renderEmptyState = function(container) {
        container.innerHTML = 
            '<div class="empty-state">' +
                '<div class="empty-state-icon">📚</div>' +
                '<h3>' + this.i18n.t('web_empty_title') + '</h3>' +
                '<p>' + this.i18n.t('web_empty_text') + '</p>' +
            '</div>';
    };

    /**
     * Render story grid
     * @private
     */
    UIController.prototype._renderStoryGrid = function(container, stories) {
        var self = this;
        var grid = document.createElement('div');
        grid.className = 'story-grid';

        for (var i = 0; i < stories.length; i++) {
            var card = self._createStoryCard(stories[i]);
            grid.appendChild(card);
        }

        container.appendChild(grid);
    };

    /**
     * Create a story card element
     * @private
     */
    UIController.prototype._createStoryCard = function(story) {
        var self = this;
        var card = document.createElement('div');
        card.className = 'story-card';
        card.innerHTML = 
            '<button class="story-card-delete" ' +
                    'title="' + this.i18n.t('web_btn_delete') + '" ' +
                    'data-filename="' + story.filename + '" ' +
                    'aria-label="' + this.i18n.t('web_btn_delete') + ' ' + story.title + '">✕</button>' +
            '<div class="story-card-title">' + this._escapeHtml(story.title) + '</div>' +
            '<div class="story-card-meta">' + this.i18n.t('web_by') + ' ' + this._escapeHtml(story.author) + '</div>' +
            '<div class="story-card-meta">' + (story.sections || '?') + ' ' + this.i18n.t('web_sections') + '</div>';

        // Single click to select
        card.addEventListener('click', function(e) {
            if (!e.target.classList.contains('story-card-delete')) {
                self._selectStoryCard(story, card);
            }
        });

        // Double click to play
        card.addEventListener('dblclick', function(e) {
            if (!e.target.classList.contains('story-card-delete')) {
                self._selectStoryCard(story, card);
                self._handlePlayStory();
            }
        });

        // Delete button
        var deleteBtn = card.querySelector('.story-card-delete');
        deleteBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            self._handleDeleteStory(story.filename, story.title);
        });

        return card;
    };

    /**
     * Select a story card
     * @private
     */
    UIController.prototype._selectStoryCard = function(story, element) {
        // Deselect all cards
        var cards = document.querySelectorAll('.story-card');
        for (var i = 0; i < cards.length; i++) {
            cards[i].classList.remove('selected');
        }

        // Select this card
        element.classList.add('selected');
        this.storyManager.selectStory(story);

        // Enable action buttons
        this.elements.playBtn.disabled = false;
        this.elements.editLibraryBtn.disabled = false;
    };

    /**
     * Show message in library
     * @param {string} text - Message text
     * @param {string} type - Message type ('success', 'error', 'info')
     */
    UIController.prototype.showMessage = function(text, type) {
        this._showMessageInElement(this.elements.message, text, type);
    };

    /**
     * Show message in editor
     * @param {string} text - Message text
     * @param {string} type - Message type ('success', 'error', 'info')
     */
    UIController.prototype.showEditorMessage = function(text, type) {
        this._showMessageInElement(this.elements.editorMessage, text, type);
    };

    /**
     * Show message in a specific element
     * @private
     */
    UIController.prototype._showMessageInElement = function(element, text, type) {
        element.textContent = text;
        element.className = 'message ' + type + ' active';
        
        setTimeout(function() {
            element.classList.remove('active');
        }, 5000);
    };

    /**
     * Event Handlers
     */

    UIController.prototype._handleLanguageChange = function(lang) {
        var self = this;
        this.i18n.loadLanguage(lang)
            .then(function() {
                // Refresh current page to update translations
                if (self.currentPage === 'library') {
                    return self.loadStories();
                }
            })
            .catch(function(error) {
                self.showMessage(self.i18n.t('web_msg_error') + ': ' + error.message, 'error');
            });
    };

    UIController.prototype._handlePlayStory = function() {
        var self = this;
        var selected = this.storyManager.getSelectedStory();
        if (!selected) return;

        this.showMessage(this.i18n.t('web_msg_loading'), 'info');

        this.storyManager.playSelectedStory()
            .then(function(result) {
                if (result.success) {
                    self.elements.storyPlayer.src = result.play_url;
                    self.elements.storyPlayer.classList.add('active');
                    self.switchPage('player');
                } else {
                    var errors = result.errors || [result.error];
                    self.showMessage(
                        self.i18n.t('web_msg_errors') + ': ' + errors.join(', '), 
                        'error'
                    );
                }
            })
            .catch(function(error) {
                self.showMessage(self.i18n.t('web_msg_error') + ': ' + error.message, 'error');
            });
    };

    UIController.prototype._handleEditFromLibrary = function() {
        var self = this;
        var selected = this.storyManager.getSelectedStory();
        if (!selected) return;

        this.storyManager.loadStoryForEditing(selected)
            .then(function(content) {
                self.elements.storyEditor.value = content;
                self.elements.editorTitle.textContent = 
                    '✏️ ' + self.i18n.t('web_editing') + ': ' + selected.title;
                self.showEditorMessage(
                    self.i18n.t('web_msg_loaded') + ' ' + selected.filename, 
                    'success'
                );
                self.switchPage('editor');
            })
            .catch(function(error) {
                self.showEditorMessage(self.i18n.t('web_msg_error') + ': ' + error.message, 'error');
            });
    };

    UIController.prototype._handleNewStory = function() {
        this.elements.storyEditor.value = this.storyManager.getNewStoryTemplate();
        this.elements.editorTitle.textContent = '✨ ' + this.i18n.t('web_title_editor');
        this.storyManager.clearEditingState();
        this.showEditorMessage(this.i18n.t('web_msg_ready'), 'info');
        this.switchPage('editor');
    };

    UIController.prototype._handleValidateStory = function() {
        var self = this;
        var content = this.elements.storyEditor.value;

        this.storyManager.validateStory(content)
            .then(function(result) {
                if (result.valid) {
                    self.showEditorMessage(
                        '✓ ' + self.i18n.t('web_msg_valid') + ' ' + result.sections + ' ' + self.i18n.t('web_sections') + '.', 
                        'success'
                    );
                } else {
                    var errors = result.errors || [result.error];
                    self.showEditorMessage(
                        self.i18n.t('web_msg_validation_errors') + ': ' + errors.join(', '), 
                        'error'
                    );
                }
            })
            .catch(function(error) {
                self.showEditorMessage(self.i18n.t('web_msg_error') + ': ' + error.message, 'error');
            });
    };

    UIController.prototype._handleSaveStory = function() {
        var self = this;
        var content = this.elements.storyEditor.value;
        
        var filename = prompt(
            this.i18n.t('web_prompt_save'), 
            this.storyManager.getCurrentEditingFilename() || 'my_story.txt'
        );
        
        if (!filename) return;

        this.storyManager.saveStory(content, filename)
            .then(function(result) {
                if (result.success) {
                    self.showEditorMessage(
                        '✓ ' + self.i18n.t('web_msg_saved') + ' ' + result.filename + '!', 
                        'success'
                    );
                } else {
                    self.showEditorMessage(
                        self.i18n.t('web_msg_error') + ': ' + 
                        (result.error || self.i18n.t('web_msg_unknown_error')), 
                        'error'
                    );
                }
            })
            .catch(function(error) {
                self.showEditorMessage(self.i18n.t('web_msg_error') + ': ' + error.message, 'error');
            });
    };

    UIController.prototype._handleCompileAndPlay = function() {
        var self = this;
        var content = this.elements.storyEditor.value;

        this.showEditorMessage(this.i18n.t('web_msg_compiling'), 'info');

        this.storyManager.compileStory(content)
            .then(function(result) {
                if (result.success) {
                    self.elements.storyPlayer.src = result.play_url;
                    self.elements.storyPlayer.classList.add('active');
                    self.switchPage('player');
                } else {
                    var errors = result.errors || [result.error];
                    self.showEditorMessage(
                        self.i18n.t('web_msg_compilation_errors') + ': ' + errors.join(', '), 
                        'error'
                    );
                }
            })
            .catch(function(error) {
                self.showEditorMessage(self.i18n.t('web_msg_error') + ': ' + error.message, 'error');
            });
    };

    UIController.prototype._handleDeleteStory = function(filename, title) {
        var self = this;
        var confirmMsg = this.i18n.t('web_confirm_delete').replace('{title}', title);
        if (!confirm(confirmMsg)) return;

        this.storyManager.deleteStory(filename)
            .then(function(result) {
                if (result.success) {
                    self.showMessage(
                        '✓ ' + self.i18n.t('web_msg_deleted') + ' ' + title, 
                        'success'
                    );
                    self.elements.playBtn.disabled = true;
                    self.elements.editLibraryBtn.disabled = true;
                    return self.loadStories();
                } else {
                    self.showMessage(
                        self.i18n.t('web_msg_error') + ': ' + 
                        (result.error || self.i18n.t('web_msg_unknown_error')), 
                        'error'
                    );
                }
            })
            .catch(function(error) {
                self.showMessage(self.i18n.t('web_msg_error') + ': ' + error.message, 'error');
            });
    };

    /**
     * Utility: Escape HTML to prevent XSS
     * @private
     */
    UIController.prototype._escapeHtml = function(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    };

    return UIController;
})();

// Export for use in other modules
window.UIController = UIController;
