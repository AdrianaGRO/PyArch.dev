# PyArch.dev - Professional Data Automation Portfolio

A modern Flask-based portfolio website showcasing data automation services with integrated blog functionality and professional service offerings.

## 🏗️ Project Structure

```
PyArch.dev/
├── app/                    # Core application logic
│   ├── app.py              # Flask routes and configuration
│   ├── helpers.py          # Utility functions (auth, data management)
│   └── config.py           # Application configuration
├── content/                # Business data (JSON)
│   ├── posts.json          # Blog posts content
│   ├── projects.json       # Portfolio projects
│   └── pricing.json        # Service pricing tiers
├── frontend/               # User interface
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # CSS, JavaScript, images
├── tools/                  # Development utilities
│   ├── babel.cfg           # Translation configuration
│   ├── setup_translations.sh   # New language setup
│   └── translations/       # i18n language files
├── run.py                  # Application entry point
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AdrianaGRO/PyArch.dev.git
   cd PyArch.dev
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env  # Create your .env file
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the website**
   ```
   http://localhost:5003
   ```

## ✨ Key Features

<!-- Admin Dashboard feature not present -->
**🌐 Internationalization** - Multi-language support infrastructure (currently hidden/disabled)
- **⚡ Performance Optimized** - Clean, efficient Flask architecture
- **📊 Service Pages** - Professional pricing and service information
- **🖼️ Media Support** - Image upload and management capabilities

## 🌐 Internationalization (i18n)
## 🌐 Internationalization (i18n)

Translation infrastructure is located in the `tools/` directory:

- **Translation Management**: Use scripts in `tools/` for adding new languages
- **Current Status**: English-only (other languages are hidden/disabled for quality assurance)
- **Adding Languages**: Run `./tools/setup_translations.sh <language_code>` (feature currently disabled)
- **Documentation**: See `tools/README.md` for detailed translation workflow

- **Translation Management**: Use scripts in `tools/` for adding new languages
- **Current Status**: English-only (Romanian/Spanish temporarily disabled for quality assurance)
- **Adding Languages**: Run `./tools/setup_translations.sh <language_code>`
- **Documentation**: See `tools/README.md` for detailed translation workflow

## 🛠️ Development

### Project Philosophy
This project prioritizes **clarity and maintainability** over architectural complexity. The structure is designed for:
- **Easy Navigation** - Clear separation of concerns
- **Beginner Friendly** - Minimal abstraction, maximum clarity  
- **Professional Quality** - Clean, production-ready code

### Architecture Decisions
- **Consolidated Helpers** - All utilities in single `helpers.py` file
- **Content-Driven** - Business data separated from application logic
- **Template-First** - Frontend assets organized for easy modification

## 📄 License

MIT License - See LICENSE file for details

---

**Live Demo**: [adrianagropan.com](https://adrianagropan.com) | **Author**: [Adriana Gropan](https://github.com/AdrianaGRO)
