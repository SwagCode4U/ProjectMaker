# backend/app/services/frameworks/backend/django.py
from pathlib import Path
from typing import Dict
from .. import templates_adapter as T

def normalize(v: str) -> str:
    return 'django'

def meta() -> Dict:
    return { 'id': 'django', 'port': 8000 }

def preview(config: Dict) -> Dict:
    name = config.get('backend_folder_name', 'backend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'manage.py', 'type': 'file' },
            { 'name': 'requirements.txt', 'type': 'file' },
            { 'name': 'core', 'type': 'directory', 'children': [
                { 'name': '__init__.py', 'type': 'file' },
                { 'name': 'settings.py', 'type': 'file' },
                { 'name': 'urls.py', 'type': 'file' },
                { 'name': 'wsgi.py', 'type': 'file' },
            ]},
            { 'name': '.gitignore', 'type': 'file' },
            { 'name': 'README.md', 'type': 'file' },
        ]
    }

def build(root: Path, config: Dict) -> Dict:
    backend = config.get('backend_folder_name', 'backend')
    base = root / backend
    ops, errs = [], []
    try:
        (base / 'core').mkdir(parents=True, exist_ok=True)
        files = {
            'manage.py': T.django_manage(config),
            'requirements.txt': T.django_requirements(),
            'core/__init__.py': '',
            'core/settings.py': T.django_settings(config),
            'core/urls.py': T.django_urls(config),
            'core/wsgi.py': T.django_wsgi(config),
            '.gitignore': """*.pyc
__pycache__/
.env
/db.sqlite3
/staticfiles
""",
            'README.md': """# Django Boilerplate\n\nA minimal Django starter to get you moving quickly.\n\n## Getting Started\n```bash\npip install -r requirements.txt\npython manage.py runserver\n```\n\n---\n\nGenerated with [ProjectMaker](https://github.com/SwagCode4U/projectmaker)\n""",
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {backend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'backend_type': 'django' }
