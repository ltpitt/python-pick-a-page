/**
 * Browser Feature Detection and Legacy Support Loader
 * 
 * This script detects browser capabilities and loads either modern or legacy
 * JavaScript files accordingly. It must be loaded first (before other scripts).
 * 
 * Target: Support Firefox 52 ESR (Aquafox) and other legacy browsers while
 * maintaining modern experience for capable browsers.
 * 
 * Features tested:
 * - async/await syntax support
 * - Object spread operator support
 * - fetch API (with fallback check)
 */

(function() {
    'use strict';
    
    /**
     * Check if browser supports async/await syntax
     * @returns {boolean}
     */
    function supportsAsyncAwait() {
        try {
            // eslint-disable-next-line no-new-func
            new Function('async function test() { await Promise.resolve(); }');
            return true;
        } catch (e) {
            return false;
        }
    }
    
    /**
     * Check if browser supports object spread operator
     * @returns {boolean}
     */
    function supportsObjectSpread() {
        try {
            // eslint-disable-next-line no-new-func
            new Function('var a = {...{x: 1}}; return a.x;')();
            return true;
        } catch (e) {
            return false;
        }
    }
    
    /**
     * Check if fetch API is available
     * @returns {boolean}
     */
    function supportsFetch() {
        return typeof window.fetch === 'function';
    }
    
    /**
     * Determine if we should use legacy scripts
     * @returns {boolean}
     */
    function needsLegacySupport() {
        // If any critical feature is missing, use legacy
        if (!supportsAsyncAwait()) {
            console.log('Browser does not support async/await - using legacy scripts');
            return true;
        }
        if (!supportsObjectSpread()) {
            console.log('Browser does not support object spread - using legacy scripts');
            return true;
        }
        if (!supportsFetch()) {
            console.log('Browser does not support fetch API - using legacy scripts');
            return true;
        }
        return false;
    }
    
    /**
     * Load a JavaScript file dynamically
     * @param {string} src - Script source URL
     * @returns {Promise}
     */
    function loadScript(src) {
        return new Promise(function(resolve, reject) {
            var script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    /**
     * Load all scripts in order
     * @param {Array<string>} scripts - Array of script URLs to load in order
     */
    function loadScriptsInOrder(scripts) {
        var current = 0;
        
        function loadNext() {
            if (current >= scripts.length) {
                return;
            }
            
            var script = document.createElement('script');
            script.src = scripts[current];
            script.onload = function() {
                current++;
                loadNext();
            };
            script.onerror = function(error) {
                console.error('Failed to load script:', scripts[current], error);
            };
            document.head.appendChild(script);
        }
        
        loadNext();
    }
    
    // Determine which scripts to load
    var useLegacy = needsLegacySupport();
    var basePath = '/static/js/';
    
    // Store detection result for other scripts to use
    window.PICK_A_PAGE_LEGACY_MODE = useLegacy;
    
    if (useLegacy) {
        console.log('📜 Loading legacy browser compatible scripts');
        loadScriptsInOrder([
            basePath + 'legacy/api-service-legacy.js',
            basePath + 'legacy/i18n-service-legacy.js',
            basePath + 'legacy/story-manager-legacy.js',
            basePath + 'legacy/ui-controller-legacy.js',
            basePath + 'legacy/app-legacy.js'
        ]);
    } else {
        console.log('🚀 Loading modern browser scripts');
        loadScriptsInOrder([
            basePath + 'api-service.js',
            basePath + 'i18n-service.js',
            basePath + 'story-manager.js',
            basePath + 'ui-controller.js',
            basePath + 'app.js'
        ]);
    }
})();
