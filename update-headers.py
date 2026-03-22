#!/usr/bin/env python3
"""
Update all HTML pages with the new global header component
"""

import re
import os

# Files to update
files = [
    'index-enhanced.html',
    'services.html',
    'blog.html',
    'checkout.html',
    'order-confirmation.html',
    'general-contracting.html',
    'acquisitions.html',
    'brokerage.html',
    'development.html'
]

def update_file(filename):
    """Update a single file with the new header"""
    print(f"Processing {filename}...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the old navbar section
        # Look for <nav class="navbar"> or similar and replace with header placeholder
        
        # First, try to find and replace the entire navbar block
        navbar_patterns = [
            # Pattern 1: Full navbar with all content
            r'<!-- Navigation -->.*?</nav>',
            r'<!-- ===== NAVIGATION BAR ===== -->.*?</nav>',
            r'<nav class="navbar">.*?</nav>',
        ]
        
        replaced = False
        for pattern in navbar_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(
                    pattern,
                    '<!-- GLOBAL HEADER -->\n    <div id="header-placeholder"></div>\n    <script src="load-header.js"></script>',
                    content,
                    flags=re.DOTALL,
                    count=1
                )
                replaced = True
                print(f"  ✓ Replaced navbar in {filename}")
                break
        
        if not replaced:
            print(f"  ⚠ Could not find navbar pattern in {filename}, trying alternative approach...")
            # Alternative: Look for any <nav> tag in the body
            if '<nav' in content:
                # Find the nav element and replace it
                nav_match = re.search(r'<nav[^>]*>.*?</nav>', content, re.DOTALL)
                if nav_match:
                    content = content.replace(
                        nav_match.group(0),
                        '<!-- GLOBAL HEADER -->\n    <div id="header-placeholder"></div>\n    <script src="load-header.js"></script>'
                    )
                    replaced = True
                    print(f"  ✓ Replaced nav element in {filename}")
        
        if not replaced:
            print(f"  ✗ Could not find and replace navbar in {filename}")
            return False
        
        # Now remove the old navbar CSS
        css_patterns = [
            # Remove navbar-related CSS
            r'/\* Navigation \*/.*?(?=/\*|</style>)',
            r'/\* ===== NAVIGATION BAR.*?\*/.*?(?=/\*|@media|</style>)',
            r'\.navbar\s*\{[^}]*\}',
            r'\.logo[^{]*\{[^}]*\}',
            r'\.nav-links[^{]*\{[^}]*\}',
            r'\.nav-phone[^{]*\{[^}]*\}',
            r'\.menu-toggle[^{]*\{[^}]*\}',
            r'\.dropdown[^{]*\{[^}]*\}',
            r'\.dropdown-content[^{]*\{[^}]*\}',
        ]
        
        for pattern in css_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Clean up any mobile menu JS
        js_patterns = [
            r'// Mobile Menu Toggle.*?(?=// |</script>)',
            r'const menuToggle.*?(?=// |</script>)',
        ]
        
        for pattern in js_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Write back
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Successfully updated {filename}\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Error updating {filename}: {e}\n")
        return False

def main():
    print("=" * 60)
    print("Updating Southern Cities Website Headers")
    print("=" * 60 + "\n")
    
    os.chdir('/Users/ashborn/.openclaw/workspace/southern-cities-website')
    
    success_count = 0
    for file in files:
        if os.path.exists(file):
            if update_file(file):
                success_count += 1
        else:
            print(f"⚠ File not found: {file}\n")
    
    print("=" * 60)
    print(f"Updated {success_count}/{len(files)} files successfully")
    print("=" * 60)

if __name__ == '__main__':
    main()
