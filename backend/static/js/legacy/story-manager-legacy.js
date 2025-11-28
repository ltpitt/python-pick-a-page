/**
 * Story Manager - Legacy Browser Compatible Version
 * 
 * This version uses Promise chains instead of async/await for Firefox 52 ESR compatibility.
 * 
 * Responsibility: Business logic for story operations.
 * Following Single Responsibility Principle - manages story state and operations.
 * Following Dependency Inversion - depends on ApiService abstraction.
 */

var StoryManager = (function() {
    'use strict';
    
    function StoryManager(apiService, i18nService) {
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
    StoryManager.prototype.loadStories = function() {
        var self = this;
        return this.apiService.getStories()
            .then(function(stories) {
                self.stories = stories;
                return stories;
            })
            .catch(function(error) {
                console.error('Error loading stories:', error);
                throw error;
            });
    };

    /**
     * Get all stories
     * @returns {Array}
     */
    StoryManager.prototype.getStories = function() {
        return this.stories;
    };

    /**
     * Select a story
     * @param {Object} story - Story object to select
     */
    StoryManager.prototype.selectStory = function(story) {
        this.selectedStory = story;
    };

    /**
     * Get selected story
     * @returns {Object|null}
     */
    StoryManager.prototype.getSelectedStory = function() {
        return this.selectedStory;
    };

    /**
     * Clear selected story
     */
    StoryManager.prototype.clearSelection = function() {
        this.selectedStory = null;
    };

    /**
     * Load story content for editing
     * @param {Object} story - Story to load
     * @returns {Promise<string>} Story content
     */
    StoryManager.prototype.loadStoryForEditing = function(story) {
        var self = this;
        return this.apiService.getStoryContent(story.filename)
            .then(function(data) {
                self.currentEditingFilename = story.filename;
                return data.content;
            })
            .catch(function(error) {
                console.error('Error loading story for editing:', error);
                throw error;
            });
    };

    /**
     * Get template for new story
     * @returns {string} New story template
     */
    StoryManager.prototype.getNewStoryTemplate = function() {
        var t = this.i18n.t.bind(this.i18n);
        return '---\n' +
            'title: ' + t('web_new_story_title') + '\n' +
            'author: ' + t('web_new_story_author') + '\n' +
            '---\n\n' +
            '[[beginning]]\n\n' +
            t('web_new_story_content') + '\n\n' +
            '[[' + t('web_new_story_choice') + ']]\n\n' +
            '---\n\n' +
            '[[' + t('web_new_story_choice') + ']]\n\n' +
            t('web_new_story_continue') + '\n';
    };

    /**
     * Validate story content
     * @param {string} content - Story content to validate
     * @returns {Promise<Object>} Validation result
     */
    StoryManager.prototype.validateStory = function(content) {
        if (!content.trim()) {
            return Promise.reject(new Error(this.i18n.t('web_msg_empty')));
        }
        return this.apiService.validateStory(content);
    };

    /**
     * Save story
     * @param {string} content - Story content
     * @param {string} filename - Filename (optional, will prompt if not provided)
     * @returns {Promise<Object>} Save result
     */
    StoryManager.prototype.saveStory = function(content, filename) {
        var self = this;
        if (!content.trim()) {
            return Promise.reject(new Error(this.i18n.t('web_msg_empty')));
        }

        var saveFilename = filename || this.currentEditingFilename;
        if (!saveFilename) {
            return Promise.reject(new Error('No filename provided'));
        }

        return this.apiService.saveStory(content, saveFilename)
            .then(function(result) {
                if (result.success) {
                    self.currentEditingFilename = result.filename;
                    // Refresh stories list
                    return self.loadStories().then(function() {
                        return result;
                    });
                }
                return result;
            });
    };

    /**
     * Delete a story
     * @param {string} filename - Story filename to delete
     * @returns {Promise<Object>} Delete result
     */
    StoryManager.prototype.deleteStory = function(filename) {
        var self = this;
        return this.apiService.deleteStory(filename)
            .then(function(result) {
                if (result.success) {
                    // Clear selection if deleted story was selected
                    if (self.selectedStory && self.selectedStory.filename === filename) {
                        self.clearSelection();
                    }
                    // Refresh stories list
                    return self.loadStories().then(function() {
                        return result;
                    });
                }
                return result;
            });
    };

    /**
     * Compile story
     * @param {string} content - Story content
     * @param {string} filename - Story filename
     * @returns {Promise<Object>} Compilation result
     */
    StoryManager.prototype.compileStory = function(content, filename) {
        if (!content.trim()) {
            return Promise.reject(new Error(this.i18n.t('web_msg_empty')));
        }

        var compileFilename = filename || this.currentEditingFilename || 'preview_story.txt';
        return this.apiService.compileStory(content, compileFilename);
    };

    /**
     * Play selected story
     * @returns {Promise<Object>} Compilation result with play_url
     */
    StoryManager.prototype.playSelectedStory = function() {
        var self = this;
        if (!this.selectedStory) {
            return Promise.reject(new Error('No story selected'));
        }

        return this.apiService.getStoryContent(this.selectedStory.filename)
            .then(function(data) {
                return self.apiService.compileStory(data.content, self.selectedStory.filename);
            });
    };

    /**
     * Get current editing filename
     * @returns {string|null}
     */
    StoryManager.prototype.getCurrentEditingFilename = function() {
        return this.currentEditingFilename;
    };

    /**
     * Set current editing filename
     * @param {string} filename
     */
    StoryManager.prototype.setCurrentEditingFilename = function(filename) {
        this.currentEditingFilename = filename;
    };

    /**
     * Clear current editing state
     */
    StoryManager.prototype.clearEditingState = function() {
        this.currentEditingFilename = null;
    };

    return StoryManager;
})();

// Export for use in other modules
window.StoryManager = StoryManager;
