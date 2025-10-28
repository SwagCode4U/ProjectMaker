# backend/app/services/frameworks/backend/fastapi.py
from pathlib import Path
from typing import Dict
from .. import templates_adapter as T

def normalize(v: str) -> str:
    return 'fastapi'

def meta() -> Dict:
    return { 'id': 'fastapi', 'port': 8000 }

def preview(config: Dict) -> Dict:
    name = config.get('backend_folder_name', 'backend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'app', 'type': 'directory', 'children': [
                { 'name': '__init__.py', 'type': 'file' },
                { 'name': 'main.py', 'type': 'file' },
                { 'name': 'database.py', 'type': 'file' },
                { 'name': 'models.py', 'type': 'file' },
                { 'name': 'schemas.py', 'type': 'file' },
                { 'name': 'crud.py', 'type': 'file' },
                { 'name': 'routes', 'type': 'directory', 'children': [
                    { 'name': '__init__.py', 'type': 'file' },
                    { 'name': 'project_routes.py', 'type': 'file' },
                ]},
            ]},
            { 'name': 'requirements.txt', 'type': 'file' },
            { 'name': '.env.example', 'type': 'file' },
        ]
    }

def build(root: Path, config: Dict) -> Dict:
    backend = config.get('backend_folder_name', 'backend')
    base = root / backend
    ops, errs = [], []
    try:
        (base / 'app' / 'routes').mkdir(parents=True, exist_ok=True)
        files = {
            'app.py': T.fastapi_root_app(config),
            'app/__init__.py': '',
            'app/main.py': T.fastapi_main(config),
            'app/database.py': T.fastapi_database(config),
            'app/models.py': T.fastapi_models(config),
            'app/schemas.py': T.fastapi_schemas(config),
            'app/crud.py': T.fastapi_crud(config),
            'app/routes/__init__.py': '',
            'app/routes/project_routes.py': T.fastapi_routes(config),
            'requirements.txt': T.fastapi_requirements(),
            '.env.example': T.env_example(config),
            '.gitignore': """__pycache__/\n*.py[cod]\n.env\nvenv/\nprojectmaker.db\n""",
            'README.md': f"""# {config.get('project_name','FastAPI App')} (FastAPI)\n\nDev server: uvicorn app.main:app --reload --port 8000\n\nBuilt with ❤️ for the developer community by SwagCode4U.\n""",
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {backend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'backend_type': 'fastapi' }
