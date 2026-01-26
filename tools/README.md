# Development Tools

This folder contains reusable maintenance utilities for the PyArch.dev project.

## 🌐 Translation Management

### `babel.cfg`
Babel configuration file that defines how to extract translatable strings from Python and Jinja2 templates.
- **Use case**: When adding new translatable content, this config tells Babel where to look
- **Command**: Used automatically by `pybabel extract` commands

### `messages.pot`
Translation template file containing all extractable strings from the application.
- **Use case**: Base template for creating new language translations
- **Update**: Run `pybabel extract` to regenerate when new translatable strings are added

### `setup_translations.sh`
Shell script to set up translation infrastructure for new languages.
- **Use case**: Adding support for a new language (French, German, etc.)
- **Usage**: `./setup_translations.sh <language_code>`
- **What it does**: Creates folder structure, initializes .po files, compiles translations

### `verify_translations.sh`
Shell script to verify translation completeness and compile existing translations.
- **Use case**: Before deploying, ensure all translations are complete and compiled
- **Usage**: `./verify_translations.sh`
- **What it does**: Checks .po files, compiles to .mo files, reports missing translations

### `translations/`
Directory containing actual translation files organized by language code.
```
translations/
├── ro/LC_MESSAGES/  # Romanian translations
└── es/LC_MESSAGES/  # Spanish translations
```

## 🚀 Quick Commands

```bash
# Extract new translatable strings
pybabel extract -F babel.cfg -k _l -o messages.pot ../app

# Update existing translations with new strings  
pybabel update -i messages.pot -d translations

# Compile translations for production
pybabel compile -d translations

# Add a new language (e.g., French)
./setup_translations.sh fr
```

## 📝 Notes

- These tools support the multilingual functionality (currently disabled in production)
- Keep these files when refactoring - they'll be needed when re-enabling multiple languages
- All scripts assume they're run from the `tools/` directory
