# Example: How to Update Templates for Translations

This example shows you exactly how to convert your existing templates to support multiple languages.

## Before & After Comparison

### Example 1: Navigation (base.html)

**BEFORE:**
```html
<ul class="nav-links">
    <li>
        <a href="{{ url_for('projects_index') }}" class="nav-link">
           Projects
        </a>
    </li>
    <li>
        <a href="{{ url_for('pricing') }}" class="nav-link">
           Pricing
        </a>
    </li>
    <li>
        <a href="{{ url_for('about') }}" class="nav-link">
           About
        </a>
    </li>
    <li>
        <a href="/blog" class="nav-link">
           Blog
        </a>
    </li>
</ul>
```

**AFTER:**
```html
<ul class="nav-links">
    <li>
        <a href="{{ url_for('projects_index', lang=current_lang) }}" class="nav-link">
           {{ _('Projects') }}
        </a>
    </li>
    <li>
        <a href="{{ url_for('pricing', lang=current_lang) }}" class="nav-link">
           {{ _('Pricing') }}
        </a>
    </li>
    <li>
        <a href="{{ url_for('about', lang=current_lang) }}" class="nav-link">
           {{ _('About') }}
        </a>
    </li>
    <li>
        <a href="{{ url_for('blog', lang=current_lang) }}" class="nav-link">
           {{ _('Blog') }}
        </a>
    </li>
</ul>
```

### Example 2: Hero Section (index.html)

**BEFORE:**
```html
<header class="hero-unified">
    <div style="max-width: 1000px; margin: 0 auto;">
        <h1 class="hero-title-unified">
            Stop fighting with spreadsheets.
            <br>
            <span style="color: var(--accent-blue);">I automate the struggle.</span>
        </h1>
        <p class="hero-subtitle-unified">
            15+ years of retail operations experience meeting modern Python automation.
        </p>
    </div>
</header>
```

**AFTER:**
```html
<header class="hero-unified">
    <div style="max-width: 1000px; margin: 0 auto;">
        <h1 class="hero-title-unified">
            {{ _('Stop fighting with spreadsheets.') }}
            <br>
            <span style="color: var(--accent-blue);">{{ _('I automate the struggle.') }}</span>
        </h1>
        <p class="hero-subtitle-unified">
            {{ _('15+ years of retail operations experience meeting modern Python automation.') }}
        </p>
    </div>
</header>
```

### Example 3: Pricing Card (pricing.html)

**BEFORE:**
```html
<div class="card pricing-card">
    <h2>Quick Cleanup</h2>
    <p>Perfect for one-off tasks</p>

    <div>
        <span class="price">$10</span>
        <span class="period">/ file</span>
    </div>

    <ul class="check-list">
        <li>Up to 5,000 rows</li>
        <li>Remove duplicates</li>
        <li>Format standardization</li>
        <li>24–48h delivery</li>
    </ul>

    <a href="mailto:adriana.gropan@gmail.com" class="btn">
        Get Started
    </a>
</div>
```

**AFTER:**
```html
<div class="card pricing-card">
    <h2>{{ _('Quick Cleanup') }}</h2>
    <p>{{ _('Perfect for one-off tasks') }}</p>

    <div>
        <span class="price">$10</span>
        <span class="period">{{ _('/ file') }}</span>
    </div>

    <ul class="check-list">
        <li>{{ _('Up to 5,000 rows') }}</li>
        <li>{{ _('Remove duplicates') }}</li>
        <li>{{ _('Format standardization') }}</li>
        <li>{{ _('24–48h delivery') }}</li>
    </ul>

    <a href="mailto:adriana.gropan@gmail.com" class="btn">
        {{ _('Get Started') }}
    </a>
</div>
```

### Example 4: Footer (base.html)

**BEFORE:**
```html
<footer>
    <div>
        <h3>Adriana Gropan</h3>
        <p>Python automation solutions for business operations.</p>

        <h3>Quick Links</h3>
        <ul>
            <li><a href="{{ url_for('projects_index') }}">Projects</a></li>
            <li><a href="{{ url_for('about') }}">About Me</a></li>
        </ul>

        <h3>Resources</h3>

        <p>© 2025 Adriana Gropan. Built with Flask and Python.</p>
    </div>
</footer>
```

**AFTER:**
```html
<footer>
    <div>
        <h3>Adriana Gropan</h3>
        <p>{{ _('Python automation solutions for business operations.') }}</p>

        <h3>{{ _('Quick Links') }}</h3>
        <ul>
            <li><a href="{{ url_for('projects_index', lang=current_lang) }}">{{ _('Projects') }}</a></li>
            <li><a href="{{ url_for('about', lang=current_lang) }}">{{ _('About Me') }}</a></li>
        </ul>

        <h3>{{ _('Resources') }}</h3>

        <p>{{ _('© 2025 Adriana Gropan. Built with Flask and Python.') }}</p>
    </div>
</footer>
```

## Rules for Updating Templates

### 1. Wrap ALL user-facing text in `{{ _('...') }}`

✅ **DO translate:**
- Headings and titles
- Body text and paragraphs
- Button labels
- Navigation links
- Form labels
- Error messages
- Placeholder text

❌ **DON'T translate:**
- URLs
- Email addresses
- Code snippets
- CSS class names
- Variable names
- Numbers (unless they're part of a sentence)

### 2. Keep HTML structure intact

```html
<!-- ✅ CORRECT -->
<h1>{{ _('Stop fighting with spreadsheets.') }}</h1>

<!-- ❌ WRONG - Don't include HTML tags in translation string -->
<h1>{{ _('<h1>Stop fighting with spreadsheets.</h1>') }}</h1>
```

### 3. Handle multi-line text carefully

```html
<!-- ✅ CORRECT - Keep as one translation string -->
<p>{{ _('This is a long paragraph that contains multiple sentences. It should be kept together as one translatable unit.') }}</p>

<!-- ❌ WRONG - Don't split sentences unnecessarily -->
<p>{{ _('This is a long paragraph') }} {{ _('that contains multiple sentences.') }}</p>
```

### 4. Variables in translations

If you need to insert dynamic content:

```html
<!-- Use format strings -->
<p>{{ _('Welcome, %(name)s!', name=user.name) }}</p>
<p>{{ _('You have %(count)d new messages', count=message_count) }}</p>
```

### 5. Add language parameter to all url_for() calls

```html
<!-- ✅ CORRECT -->
<a href="{{ url_for('about', lang=current_lang) }}">{{ _('About') }}</a>

<!-- ❌ WRONG - Missing lang parameter -->
<a href="{{ url_for('about') }}">{{ _('About') }}</a>
```

## Quick Checklist

When updating a template, check:

- [ ] All visible text wrapped in `{{ _('...') }}`
- [ ] All `url_for()` calls include `lang=current_lang`
- [ ] HTML tags are OUTSIDE translation strings
- [ ] No hardcoded language-specific text remains
- [ ] Email addresses and URLs are NOT translated
- [ ] Numbers and prices handled correctly
- [ ] Page still renders without errors

## Testing Your Changes

1. Update the template file
2. Extract new translatable strings:
   ```bash
   pybabel extract -F babel.cfg -o messages.pot .
   ```

3. Update translation files:
   ```bash
   pybabel update -i messages.pot -d translations
   ```

4. Edit `translations/ro/LC_MESSAGES/messages.po` and add Romanian translations
5. Edit `translations/es/LC_MESSAGES/messages.po` and add Spanish translations

6. Compile translations:
   ```bash
   pybabel compile -d translations
   ```

7. Restart Flask and test:
   - Visit `/` (English)
   - Visit `/ro/` (Romanian)
   - Visit `/es/` (Spanish)

## Common Mistakes to Avoid

### Mistake 1: Including HTML in translation strings
```html
<!-- ❌ WRONG -->
{{ _('<strong>Important:</strong> Read this') }}

<!-- ✅ CORRECT -->
<strong>{{ _('Important:') }}</strong> {{ _('Read this') }}
```

### Mistake 2: Translating code or technical terms
```html
<!-- ❌ WRONG -->
<code>{{ _('def my_function():') }}</code>

<!-- ✅ CORRECT -->
<code>def my_function():</code>
```

### Mistake 3: Breaking up natural phrases
```html
<!-- ❌ WRONG -->
<p>{{ _('Click') }} <a href="#">{{ _('here') }}</a> {{ _('to continue') }}</p>

<!-- ✅ CORRECT (use placeholder) -->
<p>{{ _('Click <a href="#">here</a> to continue') | safe }}</p>
```

### Mistake 4: Forgetting to update url_for
```html
<!-- ❌ WRONG - Will lose language when navigating -->
<a href="{{ url_for('contact') }}">{{ _('Contact') }}</a>

<!-- ✅ CORRECT - Maintains language across navigation -->
<a href="{{ url_for('contact', lang=current_lang) }}">{{ _('Contact') }}</a>
```

---

## Need the Full Translation List?

All translations are in:
- **Website_Multilingual_Translations.docx** - Complete reference document

Use this as your source for:
- Romanian translations
- Spanish translations
- Consistent terminology across pages
