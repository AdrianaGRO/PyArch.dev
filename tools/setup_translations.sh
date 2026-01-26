#!/bin/bash

# Multilingual Setup Script for adrianagropan.com
# This script initializes Flask-Babel translations for Romanian and Spanish

echo "🌍 Setting up multilingual support for adrianagropan.com"
echo "=================================================="

# Step 1: Install Flask-Babel
echo ""
echo "📦 Step 1: Installing Flask-Babel..."
pip install Flask-Babel

# Step 2: Extract translatable strings
echo ""
echo "🔍 Step 2: Extracting translatable strings from templates..."
pybabel extract -F babel.cfg -k _l -k lazy_gettext -o messages.pot .

# Step 3: Initialize Romanian translations
echo ""
echo "🇷🇴 Step 3: Initializing Romanian (ro) translations..."
pybabel init -i messages.pot -d translations -l ro

# Step 4: Initialize Spanish translations
echo ""
echo "🇪🇸 Step 4: Initializing Spanish (es) translations..."
pybabel init -i messages.pot -d translations -l es

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit translations/ro/LC_MESSAGES/messages.po (Romanian)"
echo "2. Edit translations/es/LC_MESSAGES/messages.po (Spanish)"
echo "3. Run: pybabel compile -d translations"
echo "4. Update your templates with {{ _('text') }} tags"
echo ""
echo "Reference the translation document: Website_Multilingual_Translations.docx"
echo "Read the guide: MULTILINGUAL_IMPLEMENTATION_GUIDE.md"
