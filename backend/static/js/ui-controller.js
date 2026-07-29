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
        // Markdown features the child has used in the current story (badges).
        this._earnedBadges = new Set();
        // id -> localized label, filled from the Markdown help content.
        this._badgeLabels = {};
        this._badgeInputTimer = null;
        // A playful emoji that matches each Markdown feature being rewarded.
        this._badgeEmojis = {
            heading: '📜',
            bold: '💪',
            italic: '✨',
            image: '🖼️',
            choice: '🔀',
            list: '📋',
        };
    }

    /**
     * Initialize UI and cache DOM elements
     */
    init() {
        this._cacheElements();
        this._setupEventListeners();
        this._setupNavigation();
        this._animatePageTitle(this.currentPage);
        this._loadLearningContent();
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
            editorToolbar: document.getElementById('editorToolbar'),
            toolbarFormat: document.getElementById('toolbarFormat'),
            toolbarInsert: document.getElementById('toolbarInsert'),

            // In-editor micro-rewards
            editorBadges: document.getElementById('editorBadges'),
            editorBadgesLabel: document.getElementById('editorBadgesLabel'),
            editorBadgesList: document.getElementById('editorBadgesList'),

            // Tutorial
            tutorialBtn: document.getElementById('tutorialBtn'),
            tutorialBtnLabel: document.getElementById('tutorialBtnLabel'),
            editorTutorialBtn: document.getElementById('editorTutorialBtn'),
            editorTutorialBtnLabel: document.getElementById('editorTutorialBtnLabel'),
            tutorialOverlay: document.getElementById('tutorialOverlay'),
            tutorialClose: document.getElementById('tutorialClose'),
            tutorialDone: document.getElementById('tutorialDone'),
            tutorialHeading: document.getElementById('tutorialHeading'),
            tutorialSteps: document.getElementById('tutorialSteps'),
            tutorialCheat: document.getElementById('tutorialCheat'),
            tutorialCheatHeading: document.getElementById('tutorialCheatHeading'),

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

        // In-editor micro-rewards: award badges as the child types (debounced).
        if (this.elements.storyEditor) {
            this.elements.storyEditor.addEventListener('input', () => {
                clearTimeout(this._badgeInputTimer);
                // Short delay keeps detection near real-time while still
                // coalescing rapid keystrokes.
                this._badgeInputTimer = setTimeout(() => this._updateBadges(), 120);
            });
        }

        // Tutorial
        if (this.elements.tutorialBtn) {
            this.elements.tutorialBtn.addEventListener('click', () => this._openTutorial());
        }
        if (this.elements.editorTutorialBtn) {
            this.elements.editorTutorialBtn.addEventListener('click', () => this._openTutorial());
        }
        if (this.elements.tutorialClose) {
            this.elements.tutorialClose.addEventListener('click', () => this._closeTutorial());
        }
        if (this.elements.tutorialDone) {
            this.elements.tutorialDone.addEventListener('click', () => this._closeTutorial());
        }
        if (this.elements.tutorialOverlay) {
            this.elements.tutorialOverlay.addEventListener('click', (e) => {
                if (e.target === this.elements.tutorialOverlay) this._closeTutorial();
            });
        }
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this._closeTutorial();
        });
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
        this._animatePageTitle(pageName);

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

            this._loadLearningContent();
            this._animatePageTitle(this.currentPage);
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
            this._resetBadges();
            this._updateBadges(false);
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
        this._resetBadges();
        this._updateBadges(false);
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
                // Prefer the child-friendly hints when the backend provides them.
                const details = result.error_details || [];
                const messages = details.length
                    ? details.map(d => d.hint || d.message)
                    : (result.errors || [result.error]);
                this.showEditorMessage(
                    this.i18n.t('web_msg_validation_errors') + ': ' + messages.join(' '), 
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
     * Replay the title animation for the active page.
     * @private
     */
    _animatePageTitle(pageName) {
        const title = document.querySelector(`#page-${pageName} .magic-title`);
        if (!title) return;

        title.classList.remove('is-animating');
        // Defer to the next frame(s) so the animation reliably (re)starts.
        // On first load init() runs before the browser's first paint, so a
        // synchronous reflow can't start the animation; waiting for a painted
        // frame fixes the "broken title on app start" case and re-triggers.
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                title.classList.add('is-animating');
                this._spawnSparkles(title);
            });
        });
    }

    /**
     * Sprinkle a short-lived burst of sparkles over the page title.
     * Uses fixed-position particles appended to <body> so they are never
     * clipped by the title's overflow. Skipped when the user prefers
     * reduced motion.
     * @private
     */
    _spawnSparkles(title) {
        if (window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }

        const rect = title.getBoundingClientRect();
        if (!rect.width) return;

        const layer = document.createElement('div');
        layer.className = 'sparkle-layer';

        const count = 16;
        for (let i = 0; i < count; i++) {
            const sparkle = document.createElement('span');
            sparkle.className = 'sparkle';

            const originX = rect.left + Math.random() * rect.width;
            const originY = rect.top + rect.height * (0.15 + Math.random() * 0.7);
            sparkle.style.left = `${originX}px`;
            sparkle.style.top = `${originY}px`;

            const angle = Math.random() * Math.PI * 2;
            const distance = 16 + Math.random() * 40;
            sparkle.style.setProperty('--dx', `${Math.cos(angle) * distance}px`);
            sparkle.style.setProperty('--dy', `${Math.sin(angle) * distance}px`);
            sparkle.style.setProperty('--size', `${8 + Math.random() * 8}px`);
            sparkle.style.animationDelay = `${Math.random() * 220}ms`;

            layer.appendChild(sparkle);
        }

        document.body.appendChild(layer);
        window.setTimeout(() => layer.remove(), 1500);
    }

    /**
     * Fetch the localized tutorial + Markdown reference for the current
     * language and (re)render the toolbar, help panel and tutorial modal.
     * @private
     */
    async _loadLearningContent() {
        const lang = this.i18n.getCurrentLanguage();
        const api = this.i18n.apiService;
        try {
            const [tutorial, help] = await Promise.all([
                api.getTutorial(lang),
                api.getMarkdownHelp(lang),
            ]);
            this._tutorialData = tutorial;
            this._helpData = help;
            this._renderToolbar(help.items);
            this._renderCheatSheet(help);
            // Keep localized labels for the earned badges.
            this._badgeLabels = {};
            help.items.forEach(item => { this._badgeLabels[item.id] = item.label; });
            if (this.elements.tutorialBtnLabel) {
                this.elements.tutorialBtnLabel.textContent = tutorial.cta;
            }
            if (this.elements.editorTutorialBtnLabel) {
                this.elements.editorTutorialBtnLabel.textContent = tutorial.cta;
            }
            if (this.elements.editorBadgesLabel && help.badges) {
                this.elements.editorBadgesLabel.textContent = help.badges;
            }
            // Re-render any badges already earned so their labels follow the
            // newly selected language.
            this._renderBadges();
        } catch (error) {
            console.error('Failed to load learning content:', error);
        }
    }

    /**
     * Build the Word-style snippet toolbar: a Format group (title, bold,
     * italic) and an Insert group (picture, choice, list). Each button shows
     * an icon with a short label and a rich tooltip, and inserts its snippet.
     * @private
     */
    _renderToolbar(items) {
        const formatGroup = this.elements.toolbarFormat;
        const insertGroup = this.elements.toolbarInsert;
        if (!formatGroup || !insertGroup) return;
        formatGroup.innerHTML = '';
        insertGroup.innerHTML = '';

        const icons = {
            heading: 'H',
            bold: 'B',
            italic: 'I',
            image: '🖼️',
            choice: '🔀',
            list: '≡',
        };
        const formatIds = ['heading', 'bold', 'italic'];

        items.forEach(item => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'toolbar-btn';
            button.dataset.id = item.id;
            button.title = `${item.label} — ${item.hint}\n${item.example}`;
            button.setAttribute('aria-label', item.label);
            button.innerHTML =
                `<span class="toolbar-icon" aria-hidden="true">${icons[item.id] || '＋'}</span>` +
                `<span class="toolbar-label">${this._escapeHtml(item.label)}</span>`;
            button.addEventListener('click', () => this._insertMarkdown(item));
            (formatIds.includes(item.id) ? formatGroup : insertGroup).appendChild(button);
        });
    }

    /**
     * Render the Markdown cheat-sheet section inside the tutorial overlay.
     * @private
     */
    _renderCheatSheet(help) {
        if (this.elements.tutorialCheatHeading) {
            this.elements.tutorialCheatHeading.textContent = help.summary;
        }
        const container = this.elements.tutorialCheat;
        if (!container) return;
        container.innerHTML = '';

        help.items.forEach(item => {
            const row = document.createElement('div');
            row.className = 'markdown-help-item';
            row.innerHTML =
                `<div class="mh-label">${this._escapeHtml(item.label)}</div>` +
                `<div class="mh-hint">${this._escapeHtml(item.hint)}</div>` +
                `<code class="mh-syntax">${this._escapeHtml(item.syntax)}</code>`;
            container.appendChild(row);
        });
    }

    /**
     * Apply a Markdown action to the editor, operating on the current caret
     * position or selection. Wrapping actions (bold, italic, choice) wrap the
     * selected text (or a placeholder); line actions (heading, list) prefix the
     * current line(s); other actions insert their snippet at the caret.
     * @private
     */
    _insertMarkdown(item) {
        const editor = this.elements.storyEditor;
        if (!editor) return;

        const actions = {
            heading: { type: 'line', prefix: '# ', placeholder: 'My Story' },
            bold: { type: 'wrap', before: '**', after: '**', placeholder: 'brave' },
            italic: { type: 'wrap', before: '*', after: '*', placeholder: 'whisper' },
            choice: { type: 'wrap', before: '[[', after: ']]', placeholder: 'Open the door' },
            list: { type: 'line', prefix: '- ', placeholder: 'a sword' },
        };
        const action = actions[item.id] || { type: 'insert', text: item.syntax };

        const value = editor.value;
        const start = editor.selectionStart ?? value.length;
        const end = editor.selectionEnd ?? value.length;

        if (action.type === 'wrap') {
            const inner = value.slice(start, end) || action.placeholder;
            const replacement = action.before + inner + action.after;
            editor.value = value.slice(0, start) + replacement + value.slice(end);
            // Select the inner text so the child can immediately retype it.
            const innerStart = start + action.before.length;
            editor.focus();
            editor.setSelectionRange(innerStart, innerStart + inner.length);
        } else if (action.type === 'line') {
            const lineStart = value.lastIndexOf('\n', start - 1) + 1;
            let lineEnd = value.indexOf('\n', end);
            if (lineEnd === -1) lineEnd = value.length;
            const region = value.slice(lineStart, lineEnd) || action.placeholder;
            const prefixed = region
                .split('\n')
                .map(line => action.prefix + line)
                .join('\n');
            editor.value = value.slice(0, lineStart) + prefixed + value.slice(lineEnd);
            const caret = lineStart + prefixed.length;
            editor.focus();
            editor.setSelectionRange(caret, caret);
        } else {
            const before = value.slice(0, start);
            const needsLeadingNewline = before.length > 0 && !before.endsWith('\n');
            const text = (action.text.startsWith('#') || action.text.startsWith('-')) && needsLeadingNewline
                ? '\n' + action.text
                : action.text;
            editor.value = before + text + value.slice(end);
            const caret = start + text.length;
            editor.focus();
            editor.setSelectionRange(caret, caret);
        }

        this._updateBadges();
    }

    /**
     * Scan the editor content and award a badge the first time the child
     * uses each Markdown feature. Purely client-side and debounced.
     *
     * @param {boolean} [celebrate=true] When false, badges already present in
     *   the loaded story are marked earned silently (no toast or pop) — used
     *   when opening an existing story so only genuinely new actions delight.
     * @private
     */
    _updateBadges(celebrate = true) {
        const editor = this.elements.storyEditor;
        if (!editor) return;

        const content = editor.value;
        // Strip bold first so a lone * pair isn't mistaken for italics.
        const withoutBold = content.replace(/\*\*[^*\n]+\*\*/g, '');
        const detectors = {
            heading: /^\s*#\s+\S/m.test(content),
            bold: /\*\*[^*\n]+\*\*/.test(content),
            italic: /\*[^*\n]+\*/.test(withoutBold),
            image: /!\[[^\]]*\]\([^)\s]+\)/.test(content),
            choice: /\[\[[^\]\n]+\]\]/.test(content),
            list: /^\s*-\s+\S/m.test(content),
        };

        const newlyEarned = [];
        Object.keys(detectors).forEach(id => {
            if (detectors[id] && !this._earnedBadges.has(id)) {
                this._earnedBadges.add(id);
                newlyEarned.push(id);
            }
        });
        if (newlyEarned.length === 0) return;

        if (celebrate) {
            newlyEarned.forEach(id => this._renderBadges(id));
        } else {
            // Silent: show the chips without any animation.
            this._renderBadges();
        }
    }

    /**
     * Render the earned-badges row. Pops the newly earned chip in place with a
     * little sparkle burst (unless the child prefers reduced motion).
     * @private
     */
    _renderBadges(justEarnedId = null) {
        const wrap = this.elements.editorBadges;
        const list = this.elements.editorBadgesList;
        if (!wrap || !list) return;

        list.innerHTML = '';
        if (this._earnedBadges.size === 0) {
            wrap.hidden = true;
            return;
        }
        wrap.hidden = false;

        const reduceMotion = window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        this._earnedBadges.forEach(id => {
            const chip = document.createElement('span');
            chip.className = 'badge-chip';
            chip.innerHTML =
                `<span class="badge-star" aria-hidden="true">${this._badgeEmojis[id] || '⭐'}</span>` +
                `<span class="badge-text">${this._escapeHtml(this._badgeLabels[id] || id)}</span>`;
            if (id === justEarnedId && !reduceMotion) {
                chip.classList.add('badge-pop');
                const burst = document.createElement('span');
                burst.className = 'badge-burst';
                burst.setAttribute('aria-hidden', 'true');
                burst.textContent = '✨';
                chip.appendChild(burst);
                window.setTimeout(() => burst.remove(), 900);
            }
            list.appendChild(chip);
        });
    }

    /**
     * Forget all earned badges (called when a new/other story is opened).
     * @private
     */
    _resetBadges() {
        this._earnedBadges.clear();
        this._renderBadges();
    }

    /**
     * Open the guided tutorial modal, rendering the current language steps.
     * @private
     */
    _openTutorial() {
        const data = this._tutorialData;
        if (!data || !this.elements.tutorialOverlay) return;

        if (this.elements.tutorialHeading) {
            this.elements.tutorialHeading.textContent = data.heading;
        }
        if (this.elements.tutorialDone) {
            this.elements.tutorialDone.textContent = data.done;
        }

        const container = this.elements.tutorialSteps;
        container.innerHTML = '';
        data.steps.forEach(step => {
            const el = document.createElement('div');
            el.className = 'tutorial-step';
            el.innerHTML =
                `<div class="ts-number" aria-hidden="true">${step.step}</div>` +
                `<div class="ts-body">` +
                `<h3 class="ts-title">${this._escapeHtml(step.title)}</h3>` +
                `<p class="ts-text">${this._escapeHtml(step.body)}</p>` +
                `<pre class="ts-example"><code>${this._escapeHtml(step.example)}</code></pre>` +
                `</div>`;
            container.appendChild(el);
        });

        this.elements.tutorialOverlay.hidden = false;
    }

    /**
     * Close the guided tutorial modal.
     * @private
     */
    _closeTutorial() {
        if (this.elements.tutorialOverlay) {
            this.elements.tutorialOverlay.hidden = true;
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
