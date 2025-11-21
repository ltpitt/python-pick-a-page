"""
HTML/CSS/JS templates for story output.

Contains template strings for generating the final HTML output.
"""

# HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
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
/* Screen styles */
body {{
    font-family: 'Georgia', serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
    color: #333;
}}

#story {{
    background: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}

.section {{
    margin-bottom: 40px;
    padding: 20px 0;
    border-bottom: 2px solid #e0e0e0;
    animation: fadeIn 0.5s ease-in;
    position: relative;
}}

.section::before {{
    content: "📖 Section";
    position: absolute;
    top: -25px;
    left: 0;
    font-size: 12px;
    color: #999;
    font-family: monospace;
}}

.section[id]::before {{
    content: "📖 Section [" attr(data-section-name) "]";
}}

.section:last-child {{
    border-bottom: none;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.section p {{
    margin: 0 0 1em 0;
    line-height: 1.8;
}}

.section p:last-of-type {{
    margin-bottom: 1.5em;
}}

.choices {{
    margin-top: 25px;
    padding-top: 10px;
}}

.choice {{
    display: inline-block;
    margin: 10px 5px;
    padding: 12px 24px;
    background: #4CAF50;
    color: white;
    text-decoration: none;
    border: none;
    border-radius: 4px;
    font-weight: bold;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

.choice:hover:not(.disabled) {{
    background: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}}

.choice.disabled {{
    background: #999;
    color: #ddd;
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
}}

/* Print styles */
@media print {{
    body {{
        background: white;
        max-width: none;
    }}
    
    #story {{
        box-shadow: none;
    }}
    
    .page-break {{
        page-break-after: always;
    }}
    
    .choice {{
        display: none;
    }}
}}
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
