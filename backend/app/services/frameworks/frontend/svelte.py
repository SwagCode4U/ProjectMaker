# backend/app/services/frameworks/frontend/svelte.py
from pathlib import Path
from typing import Dict
from .. import templates_adapter as T

def normalize(v: str) -> str:
    return 'svelte'

def meta() -> Dict:
    return { 'id': 'svelte', 'port': 3010 }

def preview(config: Dict) -> Dict:
    name = config.get('frontend_folder_name', 'frontend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'src', 'type': 'directory', 'children': [
                { 'name': 'App.svelte', 'type': 'file' }, { 'name': 'app.css', 'type': 'file' },
                { 'name': 'lib', 'type': 'directory', 'children': [ { 'name': 'api.js', 'type': 'file' }, { 'name': 'utils.js', 'type': 'file' } ] },
                { 'name': 'routes', 'type': 'directory', 'children': [
                    { 'name': 'Home.svelte', 'type': 'file' }, { 'name': 'Explorer.svelte', 'type': 'file' }, { 'name': 'CreateFile.svelte', 'type': 'file' }, { 'name': 'DBDesigner.svelte', 'type': 'file' }
                ]}
            ]},
            { 'name': 'public', 'type': 'directory', 'children': [ { 'name': 'logo.png', 'type': 'file' } ] },
            { 'name': 'index.html', 'type': 'file' },
            { 'name': 'vite.config.js', 'type': 'file' },
            { 'name': 'tailwind.config.js', 'type': 'file' },
            { 'name': 'postcss.config.js', 'type': 'file' },
            { 'name': 'package.json', 'type': 'file' },
        ]
    }

def build(root: Path, config: Dict) -> Dict:
    frontend = config.get('frontend_folder_name', 'frontend')
    base = root / frontend
    ops, errs = [], []
    try:
        (base / 'src' / 'lib').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'routes').mkdir(parents=True, exist_ok=True)
        (base / 'public').mkdir(parents=True, exist_ok=True)
        files = {
            'package.json': T.svelte_package_json(config),
            'vite.config.js': T.svelte_vite_config(config),
            'index.html': T.svelte_index_html(config),
            'tailwind.config.js': T.tailwind_config(config, framework='svelte'),
            'postcss.config.js': T.postcss_config(),
            'src/App.svelte': T.svelte_app(config),
            'src/app.css': T.svelte_app_css(config),
            'src/lib/api.js': T.svelte_lib_api_js(config),
            'src/lib/utils.js': T.svelte_lib_utils_js(config),
            'src/routes/Home.svelte': T.svelte_home(config),
            'src/routes/Explorer.svelte': T.svelte_explorer(config),
            'src/routes/CreateFile.svelte': T.svelte_create_file(config),
            'src/routes/DBDesigner.svelte': T.svelte_db_designer(config),
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {frontend}/{rel}")
        (base / 'public' / 'logo.png').write_text('placeholder')
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'frontend_type': 'svelte' }
