# backend/app/services/frameworks/frontend/react.py
from pathlib import Path
from typing import Dict
from .. import templates_adapter as T

def normalize(v: str) -> str:
    return 'react'

def meta() -> Dict:
    return { 'id': 'react', 'port': 3010 }

def preview(config: Dict) -> Dict:
    name = config.get('frontend_folder_name', 'frontend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'src', 'type': 'directory', 'children': [
                { 'name': 'App.jsx', 'type': 'file' },
                { 'name': 'main.jsx', 'type': 'file' },
                { 'name': 'index.css', 'type': 'file' },
                { 'name': 'components', 'type': 'directory', 'children': [
                    { 'name': 'Navbar.jsx', 'type': 'file' },
                    { 'name': 'Hero.jsx', 'type': 'file' },
                    { 'name': 'Footer.jsx', 'type': 'file' },
                ]},
                { 'name': 'hooks', 'type': 'directory', 'children': [ { 'name': 'useLenis.js', 'type': 'file' } ] },
                { 'name': 'styles', 'type': 'directory', 'children': [ { 'name': 'theme.js', 'type': 'file' } ] },
            ]},
            { 'name': 'public', 'type': 'directory', 'children': [ { 'name': 'favicon.ico', 'type': 'file' } ] },
            { 'name': 'index.html', 'type': 'file' },
            { 'name': 'tailwind.config.js', 'type': 'file' },
            { 'name': 'postcss.config.js', 'type': 'file' },
            { 'name': 'README.md', 'type': 'file' },
            { 'name': 'package.json', 'type': 'file' },
        ]
    }

def build(root: Path, config: Dict) -> Dict:
    frontend = config.get('frontend_folder_name', 'frontend')
    base = root / frontend
    ops, errs = [], []
    try:
        (base / 'src' / 'components').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'hooks').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'styles').mkdir(parents=True, exist_ok=True)
        (base / 'public').mkdir(parents=True, exist_ok=True)
        files = {
            'package.json': T.react_package_json(config),
            'index.html': T.react_index_html(config),
            'src/App.jsx': T.react_app(config),
            'src/main.jsx': T.react_main(config),
            'src/index.css': T.react_css(config),
            'src/components/Navbar.jsx': T.react_navbar(config),
            'src/components/Hero.jsx': T.react_hero(config),
            'src/components/Footer.jsx': T.react_footer(config),
            'src/hooks/useLenis.js': T.react_use_lenis(config),
            'src/styles/theme.js': T.react_theme(config),
            'tailwind.config.js': T.tailwind_config(config, framework='react'),
            'postcss.config.js': T.postcss_config(),
            'README.md': T.react_readme(config),
            'public/favicon.ico': 'placeholder',
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {frontend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'frontend_type': 'react' }
