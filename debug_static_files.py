#!/usr/bin/env python3
"""
Flask Static Files Debugging Script
Run this script to diagnose and fix common static file issues
"""

import os
import sys

# Add the app directory to Python path
app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_dir)

# Import Flask app and helper functions
from app import app
from helpers import debug_static_configuration, check_common_image_issues, validate_image_path, generate_correct_image_urls

def main():
    print("🔍 Flask Static Files Diagnostic Tool")
    print("=" * 60)
    
    with app.app_context():
        # 1. Debug Flask static configuration
        debug_static_configuration(app)
        
        # 2. Check for common issues
        print("\n🚨 COMMON ISSUES CHECK")
        print("=" * 60)
        issues_report = check_common_image_issues(app)
        
        if issues_report['issues']:
            print("❌ Issues found:")
            for issue in issues_report['issues']:
                print(f"  - {issue}")
        else:
            print("✅ No obvious configuration issues found")
        
        if issues_report['recommendations']:
            print("\n💡 Recommendations:")
            for rec in issues_report['recommendations']:
                print(f"  - {rec}")
        
        # 3. Test specific project images
        print("\n🖼️ PROJECT IMAGES VALIDATION")
        print("=" * 60)
        
        # Load projects to test their images
        from helpers import load_projects
        projects = load_projects()
        
        for project in projects:
            if 'hero_image' in project:
                print(f"\nTesting project: {project.get('title', 'Unknown')}")
                print(f"Image path: {project['hero_image']}")
                
                result = validate_image_path(project['hero_image'], app)
                if result['valid']:
                    print("✅ Image file exists and is accessible")
                else:
                    print("❌ Image file issues:")
                    for suggestion in result['suggestions']:
                        print(f"  - {suggestion}")
        
        # 4. Show correct template examples
        print("\n📝 CORRECT TEMPLATE USAGE EXAMPLES")
        print("=" * 60)
        examples = generate_correct_image_urls()
        
        for name, example in examples.items():
            print(f"\n{example['description']}:")
            print(f"Template: {example['template_code']}")
            print(f"HTML: {example['html_example']}")
        
        # 5. Browser debugging tips
        print("\n🌐 BROWSER DEBUGGING TIPS")
        print("=" * 60)
        print("1. Open browser Developer Tools (F12)")
        print("2. Check Console tab for 404 errors on images")
        print("3. Check Network tab to see failed image requests")
        print("4. Right-click on broken image → 'Inspect Element' to see actual URL")
        print("5. Try accessing image URL directly: http://localhost:5003/static/projects/data_cleaner.png")
        print("6. Clear browser cache if images were recently updated")
        
        # 6. Quick fixes
        print("\n🔧 QUICK FIXES TO TRY")
        print("=" * 60)
        print("1. Restart Flask development server")
        print("2. Clear browser cache (Ctrl+Shift+R / Cmd+Shift+R)")
        print("3. Check file case sensitivity (image.png vs Image.PNG)")
        print("4. Verify file permissions (especially on Linux/Mac)")
        print("5. Use url_for('static', filename='...') in templates")
        print("6. Make sure static folder is in the right location")

if __name__ == "__main__":
    main()
