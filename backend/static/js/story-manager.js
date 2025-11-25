/**
 * Story Manager
 * 
 * Responsibility: Business logic for story operations.
 * Following Single Responsibility Principle - manages story state and operations.
 * Following Dependency Inversion - depends on ApiService abstraction.
 */

class StoryManager {
    constructor(apiService, i18nService) {
        this.apiService = apiService;
        this.i18n = i18nService;
        this.stories = [];
        this.selectedStory = null;
        this.currentEditingFilename = null;
    }

    /**
     * Load all stories from API
     * @returns {Promise<Array>} Array of stories
     */
    async loadStories() {
        try {
            this.stories = await this.apiService.getStories();
            return this.stories;
        } catch (error) {
            console.error('Error loading stories:', error);
            throw error;
        }
    }

    /**
     * Get all stories
     * @returns {Array}
     */
    getStories() {
        return this.stories;
    }

    /**
     * Select a story
     * @param {Object} story - Story object to select
     */
    selectStory(story) {
        this.selectedStory = story;
    }

    /**
     * Get selected story
     * @returns {Object|null}
     */
    getSelectedStory() {
        return this.selectedStory;
    }

    /**
     * Clear selected story
     */
    clearSelection() {
        this.selectedStory = null;
    }

    /**
     * Load story content for editing
     * @param {Object} story - Story to load
     * @returns {Promise<string>} Story content
     */
    async loadStoryForEditing(story) {
        try {
            const data = await this.apiService.getStoryContent(story.filename);
            this.currentEditingFilename = story.filename;
            return data.content;
        } catch (error) {
            console.error('Error loading story for editing:', error);
            throw error;
        }
    }

    /**
     * Get template for new story
     * @returns {string} New story template
     */
    getNewStoryTemplate() {
        const t = (key) => this.i18n.t(key);
        return `---
title: ${t('web_new_story_title')}
author: ${t('web_new_story_author')}
---

[[beginning]]

${t('web_new_story_content')}

[[${t('web_new_story_choice')}]]

---

[[${t('web_new_story_choice')}]]

${t('web_new_story_continue')}
`;
    }

    /**
     * Validate story content
     * @param {string} content - Story content to validate
     * @returns {Promise<Object>} Validation result
     */
    async validateStory(content) {
        if (!content.trim()) {
            throw new Error(this.i18n.t('web_msg_empty'));
        }
        return this.apiService.validateStory(content);
    }

    /**
     * Save story
     * @param {string} content - Story content
     * @param {string} filename - Filename (optional, will prompt if not provided)
     * @returns {Promise<Object>} Save result
     */
    async saveStory(content, filename = null) {
        if (!content.trim()) {
            throw new Error(this.i18n.t('web_msg_empty'));
        }

        const saveFilename = filename || this.currentEditingFilename;
        if (!saveFilename) {
            throw new Error('No filename provided');
        }

        const result = await this.apiService.saveStory(content, saveFilename);
        if (result.success) {
            this.currentEditingFilename = result.filename;
            // Refresh stories list
            await this.loadStories();
        }
        return result;
    }

    /**
     * Delete a story
     * @param {string} filename - Story filename to delete
     * @returns {Promise<Object>} Delete result
     */
    async deleteStory(filename) {
        const result = await this.apiService.deleteStory(filename);
        if (result.success) {
            // Clear selection if deleted story was selected
            if (this.selectedStory && this.selectedStory.filename === filename) {
                this.clearSelection();
            }
            // Refresh stories list
            await this.loadStories();
        }
        return result;
    }

    /**
     * Compile story
     * @param {string} content - Story content
     * @param {string} filename - Story filename
     * @returns {Promise<Object>} Compilation result
     */
    async compileStory(content, filename = null) {
        if (!content.trim()) {
            throw new Error(this.i18n.t('web_msg_empty'));
        }

        const compileFilename = filename || this.currentEditingFilename || 'preview_story.txt';
        return this.apiService.compileStory(content, compileFilename);
    }

    /**
     * Play selected story
     * @returns {Promise<Object>} Compilation result with play_url
     */
    async playSelectedStory() {
        if (!this.selectedStory) {
            throw new Error('No story selected');
        }

        const data = await this.apiService.getStoryContent(this.selectedStory.filename);
        return this.apiService.compileStory(data.content, this.selectedStory.filename);
    }

    /**
     * Get current editing filename
     * @returns {string|null}
     */
    getCurrentEditingFilename() {
        return this.currentEditingFilename;
    }

    /**
     * Set current editing filename
     * @param {string} filename
     */
    setCurrentEditingFilename(filename) {
        this.currentEditingFilename = filename;
    }

    /**
     * Clear current editing state
     */
    clearEditingState() {
        this.currentEditingFilename = null;
    }
}

// Export for use in other modules
window.StoryManager = StoryManager;
