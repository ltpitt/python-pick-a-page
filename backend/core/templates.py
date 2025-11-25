"""
HTML/CSS/JS templates for story output.

Contains template strings for generating the final HTML output.
"""

# HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {css}
    </style>
</head>
<body>
    <div id="story">
        {content}
    </div>
    <script>
        {javascript}
    </script>
</body>
</html>
"""

# CSS styles for both screen and print
CSS_TEMPLATE = """
/* Screen styles - Book-like appearance */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, Georgia, serif;
    line-height: 1.7;
    min-height: 100vh;
    padding: 0px 0px;
    color: #2c3e50;
}

#story {
    max-width: 700px;
    margin: 0 auto;
    background: #faf8f3;
    padding: 0px 0px;
    position: relative;
}

/* Book title on first section */
#story .section:first-child {
    margin-top: 0;
    padding-top: 0;
}

.section {
    margin-bottom: 45px;
    padding: 25px 0;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    animation: pageFlip 0.6s ease-out;
    position: relative;
}

.section:last-child {
    border-bottom: none;
    margin-bottom: 0;
}

@keyframes pageFlip {
    from { 
        opacity: 0; 
        transform: perspective(1000px) rotateY(-15deg);
    }
    to { 
        opacity: 1; 
        transform: perspective(1000px) rotateY(0deg);
    }
}

/* Subtle page number effect */
.section::after {
    content: '';
    display: block;
    width: 30px;
    height: 1px;
    background: rgba(0,0,0,0.1);
    margin: 30px auto 0;
}

.section p {
    margin: 0 0 1.2em 0;
    line-height: 1.8;
    text-align: justify;
    text-indent: 2em;
    font-size: 17px;
    color: #2c3e50;
}

.section p:first-of-type {
    text-indent: 0;
}

.section p:first-of-type::first-letter {
    font-size: 3.5em;
    line-height: 0.9;
    float: left;
    margin: 0.1em 0.1em 0 0;
    font-weight: bold;
    color: #8b6f47;
}

.section p:last-of-type {
    margin-bottom: 1.8em;
}

.section strong {
    font-weight: 600;
    color: #1a252f;
}

.section em {
    font-style: italic;
    color: #34495e;
}

.choices {
    margin-top: 35px;
    padding: 25px 0 0;
    border-top: 2px solid rgba(139, 111, 71, 0.2);
    text-align: center;
    text-indent: 0;
}

.choice {
    display: inline-block;
    margin: 8px 6px;
    padding: 14px 28px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-decoration: none;
    border: none;
    border-radius: 25px;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 
        0 4px 6px rgba(102, 126, 234, 0.3),
        0 1px 3px rgba(0,0,0,0.1);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    letter-spacing: 0.3px;
    position: relative;
    overflow: hidden;
}

.choice::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.choice:hover:not(.disabled) {
    transform: translateY(-2px);
    box-shadow: 
        0 6px 12px rgba(102, 126, 234, 0.4),
        0 3px 6px rgba(0,0,0,0.15);
}

.choice:hover:not(.disabled)::before {
    left: 100%;
}

.choice:active:not(.disabled) {
    transform: translateY(0);
    box-shadow: 
        0 2px 4px rgba(102, 126, 234, 0.3),
        0 1px 2px rgba(0,0,0,0.1);
}

.choice.disabled {
    background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
    color: rgba(255,255,255,0.6);
    cursor: not-allowed;
    box-shadow: 
        0 2px 4px rgba(0,0,0,0.1),
        0 1px 2px rgba(0,0,0,0.05);
    transform: none;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    body {
        padding: 20px 10px;
    }
    
    #story {
        padding: 0px 0px;
    }
    
    .section p {
        font-size: 16px;
        text-align: left;
    }
    
    .choice {
        font-size: 14px;
        padding: 12px 20px;
        margin: 6px 4px;
    }
}

/* Print styles - Clean book format */
@media print {
    body {
        background: white;
        padding: 0;
    }
    
    #story {
        max-width: none;
        box-shadow: none;
        background: white;
        padding: 20mm;
    }
    
    #story::before {
        display: none;
    }
    
    .section {
        page-break-inside: avoid;
    }
    
    .section p:first-of-type::first-letter {
        color: #000;
    }
    
    .page-break {
        page-break-after: always;
    }
    
    .choice, .choices {
        display: none;
    }
    
    @page {
        margin: 20mm;
    }
}
"""

# JavaScript for navigation
JAVASCRIPT_TEMPLATE = """
// Story navigation logic - Squiffy-style scrolling model with section cloning
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers using event delegation
    document.getElementById('story').addEventListener('click', function(e) {
        // Check if clicked element is a choice button
        if (e.target.classList.contains('choice') && !e.target.classList.contains('disabled')) {
            handleChoiceClick(e.target);
        }
    });
});

function handleChoiceClick(button) {
    const targetSectionName = button.getAttribute('data-target');
    
    // Disable all choices in the current section
    const currentSection = button.closest('.section');
    const currentChoices = currentSection.querySelectorAll('.choice');
    currentChoices.forEach(choice => {
        choice.classList.add('disabled');
        choice.disabled = true;
    });
    
    // Navigate to the target section
    navigateToSection(targetSectionName);
}

function navigateToSection(sectionName) {
    // Find the ORIGINAL template section (the one with an ID)
    const templateSection = document.getElementById('section-' + sectionName);
    
    if (!templateSection) {
        console.error('Section template not found:', sectionName);
        return;
    }
    
    // Check if this template section is already visible (was shown before)
    const isTemplateVisible = templateSection.style.display === 'block';
    
    if (isTemplateVisible) {
        // Going back to a previous section - clone it for a fresh instance
        console.log('Cloning section:', sectionName);
        const clone = templateSection.cloneNode(true);
        
        // Remove ID to avoid duplicates
        clone.removeAttribute('id');
        
        // Re-enable all buttons in the clone
        const clonedButtons = clone.querySelectorAll('.choice');
        clonedButtons.forEach(btn => {
            btn.classList.remove('disabled');
            btn.disabled = false;
        });
        
        // Ensure it's visible
        clone.style.display = 'block';
        
        // Append to story container (at the END)
        document.getElementById('story').appendChild(clone);
        
        // Scroll to the cloned section
        setTimeout(() => {
            clone.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 50);
    } else {
        // First time showing this section
        console.log('Showing section for first time:', sectionName);
        
        // MOVE the section to the end before showing it
        // This ensures it appears after everything else, not in its original position
        const storyContainer = document.getElementById('story');
        storyContainer.appendChild(templateSection);
        
        // Now make it visible
        templateSection.style.display = 'block';
        
        // Scroll to it
        setTimeout(() => {
            templateSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 50);
    }
    
    // Update story data
    storyData.currentSection = sectionName;
    storyData.history.push(sectionName);
}

// Optional: Add a restart function
function restartStory() {
    location.reload();
}
"""
