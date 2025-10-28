# backend/app/services/frameworks/backend/express.py
from pathlib import Path
from typing import Dict
from .. import templates_adapter as T

PORT = 5177

def normalize(v: str) -> str:
    return 'express'

def meta() -> Dict:
    return { 'id': 'express', 'port': PORT }

def preview(config: Dict) -> Dict:
    name = config.get('backend_folder_name', 'backend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'src', 'type': 'directory', 'children': [
                { 'name': 'app.js', 'type': 'file' },
                { 'name': 'server.js', 'type': 'file' },
                { 'name': 'routes', 'type': 'directory', 'children': [ { 'name': 'index.js', 'type': 'file' } ] },
                { 'name': 'controllers', 'type': 'directory', 'children': [ { 'name': 'homeController.js', 'type': 'file' } ] },
                { 'name': 'middlewares', 'type': 'directory', 'children': [ { 'name': 'errorHandler.js', 'type': 'file' } ] },
                { 'name': 'utils', 'type': 'directory', 'children': [ { 'name': 'logger.js', 'type': 'file' } ] },
            ]},
            { 'name': '.env.example', 'type': 'file' },
            { 'name': 'package.json', 'type': 'file' },
            { 'name': 'README.md', 'type': 'file' },
        ]
    }

def build(root: Path, config: Dict) -> Dict:
    backend = config.get('backend_folder_name', 'backend')
    base = root / backend
    ops, errs = [], []
    try:
        (base / 'src' / 'routes').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'controllers').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'middlewares').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'utils').mkdir(parents=True, exist_ok=True)
        files = {
            'package.json': T.express_package_json(config),
            'src/app.js': T.express_app_js(config),
            'src/server.js': T.express_server_js(config),
            'src/routes/index.js': T.express_routes_index_js(config),
            'src/controllers/homeController.js': T.express_home_controller_js(config),
            'src/middlewares/errorHandler.js': T.express_error_handler_js(config),
            'src/utils/logger.js': T.express_logger_js(config),
            '.env.example': T.express_env_example(config),
            'README.md': T.express_readme(config),
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {backend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'backend_type': 'express' }
