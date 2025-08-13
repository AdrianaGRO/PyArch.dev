# PyArch.dev Blog

A simple and elegant Flask blog with Markdown support.

## Features

- Responsive and clean design
- Markdown post content with code syntax highlighting
- Image upload support
- Category and tag organization
- Authentication system for admin access
- Dark/light theme toggle

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pyarch.dev.git
cd pyarch.dev
```

2. Install the requirements:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your credentials:
```
FLASK_APP=app.py
FLASK_ENV=development
BLOG_ADMIN_USERNAME=your_username
BLOG_ADMIN_PASSWORD=your_secure_password
SECRET_KEY=your_secret_key_here
```

4. Run the application:
```bash
flask run
```

## Deploying to PythonAnywhere

1. Sign up for a free [PythonAnywhere](https://www.pythonanywhere.com) account.

2. Go to the Dashboard and click on "Web" > "Add a new web app".

3. Choose "Flask" and the latest Python version.

4. In "Files" section, upload your project files or clone from your git repository:
```bash
git clone https://github.com/yourusername/pyarch.dev.git
```

5. Create a virtual environment and install dependencies:
```bash
mkvirtualenv --python=python3.9 myflaskblog
cd pyarch.dev
pip install -r requirements.txt
```

6. Configure environment variables:
   - Go to the "Web" tab
   - Click on "Environment" under your web app configuration
   - Add the following variables:
     - BLOG_ADMIN_USERNAME
     - BLOG_ADMIN_PASSWORD
     - SECRET_KEY

7. Update the WSGI configuration file to point to your app:
```python
import sys
import os

path = '/home/yourusername/pyarch.dev'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

8. Reload your web app, and it should be live at yourusername.pythonanywhere.com

## Security Notes

- Always use strong, unique passwords for your admin login
- In production, ensure your SECRET_KEY is a complex random string
- Never expose your .env file or credentials in public repositories
- Regularly update dependencies to address security vulnerabilities

## License

MIT License
