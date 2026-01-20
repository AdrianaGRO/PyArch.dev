# Multilingual Website Implementation Guide

This guide will help you implement multilingual functionality (English, Romanian, Spanish) for adrianagropan.com.

## 📋 Table of Contents
1. [Overview](#overview)
2. [Step-by-Step Implementation](#step-by-step-implementation)
3. [File Structure](#file-structure)
4. [Testing](#testing)
5. [Deployment](#deployment)

---

## Overview

We'll use **Flask-Babel** for internationalization (i18n), which provides:
- ✅ Easy translation management
- ✅ Language switching via URL or cookie
- ✅ Template integration with `{{ _('text') }}` syntax
- ✅ Date/time localization support

### Implementation Method: URL-Based Language Switching

- English: `adrianagropan.com/` or `adrianagropan.com/en/`
- Romanian: `adrianagropan.com/ro/`
- Spanish: `adrianagropan.com/es/`

---

## Step-by-Step Implementation

### Step 1: Install Flask-Babel

```bash
cd /sessions/stoic-bold-dirac/mnt/PyArch.dev
pip install Flask-Babel
```

Update `requirements.txt`:
```bash
echo "Flask-Babel==4.0.0" >> requirements.txt
```

---

### Step 2: Configure Babel in app.py

Add to the top of `app.py`:

```python
from flask_babel import Babel, gettext, lazy_gettext as _l

# Babel Configuration
def get_locale():
    # Try to get language from URL
    lang = request.view_args.get('lang')
    if lang in ['en', 'ro', 'es']:
        return lang
    # Fallback to cookie or browser preference
    return request.accept_languages.best_match(['en', 'ro', 'es']) or 'en'

babel = Babel(app, locale_selector=get_locale)
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['LANGUAGES'] = {
    'en': 'English',
    'ro': 'Română',
    'es': 'Español'
}
```

Add language prefix support to all routes:

```python
# Add before_request to handle language
@app.before_request
def before_request():
    # Get current language from URL or default to 'en'
    lang = request.view_args.get('lang', 'en') if request.view_args else 'en'
    g.current_lang = lang

# Make language available in templates
@app.context_processor
def inject_conf_var():
    return dict(
        LANGUAGES=app.config['LANGUAGES'],
        current_lang=g.get('current_lang', 'en')
    )
```

---

### Step 3: Update Routes with Language Prefix

Modify your routes to accept optional language parameter:

```python
@app.route('/')
@app.route('/<lang>/')
def index(lang='en'):
    """Homepage - Shows hero, services, projects, and blog posts"""
    posts = load_posts()
    projects = load_all_projects()

    # Get featured project
    featured_project = next(
        (p for p in projects if p.get('featured')),
        projects[0] if projects else None
    )

    # Sort posts by date, newest first
    posts_sorted = sorted(
        posts,
        key=lambda x: x.get('created_at', ''),
        reverse=True
    )

    return render_template(
        'index.html',
        posts=posts_sorted,
        projects=projects,
        featured_project=featured_project
    )

@app.route('/<lang>/about')
@app.route('/about')
def about(lang='en'):
    """About page"""
    posts = load_posts()
    projects = load_all_projects()

    recent_posts = sorted(
        posts,
        key=lambda x: x.get('created_at', ''),
        reverse=True
    )[:3] if posts else []

    return render_template(
        'about.html',
        recent_posts=recent_posts,
        projects=projects
    )

# Repeat for all other routes: blog, pricing, contact, etc.
```

---

### Step 4: Create Translation Files

Initialize Babel translations:

```bash
# Initialize translation directories
pybabel extract -F babel.cfg -o messages.pot .

# Create Romanian translations
pybabel init -i messages.pot -d translations -l ro

# Create Spanish translations
pybabel init -i messages.pot -d translations -l es
```

Create `babel.cfg` in your project root:

```
[python: **.py]
[jinja2: **/templates/**.html]
encoding = utf-8
```

---

### Step 5: Update Templates with Translation Tags

Update `base.html` navigation:

```html
<!-- Before -->
<a href="{{ url_for('projects_index') }}" class="nav-link">Projects</a>

<!-- After -->
<a href="{{ url_for('projects_index', lang=current_lang) }}" class="nav-link">
    {{ _('Projects') }}
</a>
```

Update language switcher in `base.html`:

```html
<div class="language-switcher">
    <button class="lang-toggle" aria-label="Select language" title="Change Language">
        <i class="fas fa-globe"></i>
        <span class="current-lang">{{ current_lang.upper() }}</span>
        <i class="fas fa-chevron-down lang-arrow"></i>
    </button>
    <div class="lang-dropdown">
        <a href="{{ url_for(request.endpoint, lang='en', **request.view_args|reject_lang) }}"
           class="lang-option {% if current_lang == 'en' %}active{% endif %}">
            <span class="flag">🇺🇸</span>
            <span>English</span>
        </a>
        <a href="{{ url_for(request.endpoint, lang='ro', **request.view_args|reject_lang) }}"
           class="lang-option {% if current_lang == 'ro' %}active{% endif %}">
            <span class="flag">🇷🇴</span>
            <span>Română</span>
        </a>
        <a href="{{ url_for(request.endpoint, lang='es', **request.view_args|reject_lang) }}"
           class="lang-option {% if current_lang == 'es' %}active{% endif %}">
            <span class="flag">🇪🇸</span>
            <span>Español</span>
        </a>
    </div>
</div>
```

Add custom filter for rejecting language from view_args:

```python
@app.template_filter('reject_lang')
def reject_lang_filter(view_args):
    """Remove 'lang' from view_args to avoid duplication"""
    return {k: v for k, v in (view_args or {}).items() if k != 'lang'}
```

---

### Step 6: Translate Content

Edit translation files:

**translations/ro/LC_MESSAGES/messages.po:**
```po
msgid "Projects"
msgstr "Proiecte"

msgid "Pricing"
msgstr "Prețuri"

msgid "About"
msgstr "Despre"

msgid "Blog"
msgstr "Blog"

msgid "Contact"
msgstr "Contact"

msgid "Stop fighting with spreadsheets."
msgstr "Renunță la bătăliile cu fișierele Excel."

# Add all other translations from the document
```

**translations/es/LC_MESSAGES/messages.po:**
```po
msgid "Projects"
msgstr "Proyectos"

msgid "Pricing"
msgstr "Precios"

# Add all other translations
```

Compile translations:

```bash
pybabel compile -d translations
```

---

### Step 7: Update All Templates

For each page, wrap text in translation tags:

**index.html:**
```html
<!-- Before -->
<h1>Stop fighting with spreadsheets.</h1>

<!-- After -->
<h1>{{ _('Stop fighting with spreadsheets.') }}</h1>
```

**pricing.html:**
```html
<!-- Before -->
<h2>Quick Cleanup</h2>
<p>Perfect for one-off tasks</p>

<!-- After -->
<h2>{{ _('Quick Cleanup') }}</h2>
<p>{{ _('Perfect for one-off tasks') }}</p>
```

---

## File Structure

After implementation, your structure will be:

```
PyArch.dev/
├── app.py (updated with Babel)
├── babel.cfg (new)
├── requirements.txt (updated)
├── translations/ (new)
│   ├── ro/
│   │   └── LC_MESSAGES/
│   │       ├── messages.po
│   │       └── messages.mo
│   └── es/
│       └── LC_MESSAGES/
│           ├── messages.po
│           └── messages.mo
├── templates/
│   ├── base.html (updated with {{ _() }})
│   ├── index.html (updated)
│   ├── about.html (updated)
│   ├── pricing.html (updated)
│   ├── contact.html (updated)
│   ├── blog.html (updated)
│   └── ...
└── utils/
    └── ... (existing files)
```

---

## Testing

### Test Language Switching

1. Start your Flask app:
```bash
python app.py
```

2. Visit URLs:
- http://localhost:5003/ (English - default)
- http://localhost:5003/ro/ (Romanian)
- http://localhost:5003/es/ (Spanish)

3. Click language switcher to verify switching works

4. Check that all pages translate correctly:
- Homepage
- About
- Pricing
- Contact
- Blog

---

## Deployment

### Before deploying:

1. ✅ Compile all translations
```bash
pybabel compile -d translations
```

2. ✅ Test all language versions locally

3. ✅ Update your production environment with new dependencies

4. ✅ Ensure translation files are included in deployment

### SEO Considerations:

Add language meta tags to `base.html`:

```html
<head>
    <!-- Existing head content -->
    <link rel="alternate" hreflang="en" href="https://adrianagropan.com/en/" />
    <link rel="alternate" hreflang="ro" href="https://adrianagropan.com/ro/" />
    <link rel="alternate" hreflang="es" href="https://adrianagropan.com/es/" />
    <link rel="alternate" hreflang="x-default" href="https://adrianagropan.com/" />
</head>
```

---

## Quick Reference: Common Commands

```bash
# Extract translatable strings
pybabel extract -F babel.cfg -o messages.pot .

# Update existing translations (after adding new text)
pybabel update -i messages.pot -d translations

# Compile translations (before deployment)
pybabel compile -d translations

# Add a new language (e.g., French)
pybabel init -i messages.pot -d translations -l fr
```

---

## Need Help?

If you encounter issues:

1. Check Flask-Babel documentation: https://python-babel.github.io/flask-babel/
2. Verify `messages.mo` files are compiled
3. Ensure all routes have language parameter support
4. Check browser console for JavaScript errors in language switcher
5. Verify translations are wrapped in `{{ _('text') }}` tags

---

## Next Steps

After implementation:
1. ✅ Test all pages in all three languages
2. ✅ Add language-specific meta descriptions for SEO
3. ✅ Consider adding language detection based on user's browser
4. ✅ Update sitemap.xml with language-specific URLs
5. ✅ Monitor analytics to see which languages are most used

Good luck with your multilingual implementation! 🌍
