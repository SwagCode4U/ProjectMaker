# backend/app/services/frameworks/backend/flask.py
from pathlib import Path
from typing import Dict
from .. import templates_adapter as T

def normalize(v: str) -> str:
    return 'flask'

def meta() -> Dict:
    return { 'id': 'flask', 'port': 5000 }

def preview(config: Dict) -> Dict:
    name = config.get('backend_folder_name', 'backend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'app.py', 'type': 'file' },
            { 'name': 'config.py', 'type': 'file' },
            { 'name': 'models.py', 'type': 'file' },
            { 'name': 'routes.py', 'type': 'file' },
            { 'name': 'requirements.txt', 'type': 'file' },
            { 'name': '.env.example', 'type': 'file' },
        ]
    }

def build(root: Path, config: Dict) -> Dict:
    backend = config.get('backend_folder_name', 'backend')
    base = root / backend
    ops, errs = [], []
    try:
        base.mkdir(parents=True, exist_ok=True)
        files = {
            'app.py': T.flask_app(config),
            'config.py': T.flask_config(config),
            'models.py': T.flask_models(config),
            'routes.py': T.flask_routes(config),
            'requirements.txt': T.flask_requirements(),
            '.env.example': T.env_example(config),
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {backend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'backend_type': 'flask' }
