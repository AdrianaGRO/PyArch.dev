import json
import os
from typing import List, Dict, Optional

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'projects.json')


def _ensure_file():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)


def load_projects() -> List[Dict]:
    """Load projects from the JSON file."""
    _ensure_file()
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_projects(projects: List[Dict]) -> None:
    """Persist projects to the JSON file."""
    _ensure_file()
    with open(DATA_FILE, 'w') as f:
        json.dump(projects, f, indent=4)


def get_project(slug: str) -> Optional[Dict]:
    """Get a single project by its slug/name."""
    projects = load_projects()
    return next((p for p in projects if p.get('slug') == slug), None)
