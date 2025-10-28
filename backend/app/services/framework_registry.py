# backend/app/services/framework_registry.py
from pathlib import Path
from typing import Dict, Optional

# Reuse existing template providers
from .templates import BackendTemplates, FrontendTemplates

# ---------- Normalizers ----------

BACKEND_ALIASES = {
    "express.js": "express", "expressjs": "express", "node": "express", "nodejs": "express",
    "nest": "nestjs", "nestjs.js": "nestjs",
    "next": "nextjs", "next.js": "nextjs", "nextjs-api": "nextjs", "nextjs_api": "nextjs", "nextjsapi": "nextjs",
}

FRONTEND_ALIASES = {
    "next": "nextjs", "next.js": "nextjs",
    "solid": "solidjs", "solid.js": "solidjs",
}

def normalize_backend(value: Optional[str]) -> str:
    v = str(value or '').strip().lower()
    return BACKEND_ALIASES.get(v, v)

def normalize_frontend(value: Optional[str]) -> str:
    v = str(value or '').strip().lower()
    return FRONTEND_ALIASES.get(v, v)

# ---------- Preview trees ----------

def preview_backend_tree(config: Dict) -> Optional[Dict]:
    fw = normalize_backend(config.get('backend_framework'))
    if not fw:
        return None
    backend_name = config.get('backend_folder_name', 'backend')

    if fw == 'fastapi':
        return {
            "name": backend_name, "type": "directory", "children": [
                {"name": "app", "type": "directory", "children": [
                    {"name": "__init__.py", "type": "file"},
                    {"name": "main.py", "type": "file"},
                    {"name": "database.py", "type": "file"},
                    {"name": "models.py", "type": "file"},
                    {"name": "schemas.py", "type": "file"},
                    {"name": "crud.py", "type": "file"},
                    {"name": "routes", "type": "directory", "children": [
                        {"name": "__init__.py", "type": "file"},
                        {"name": "project_routes.py", "type": "file"},
                    ]},
                ]},
                {"name": "requirements.txt", "type": "file"},
                {"name": ".env.example", "type": "file"},
            ]
        }
    if fw == 'flask':
        return {
            "name": backend_name, "type": "directory", "children": [
                {"name": "app.py", "type": "file"},
                {"name": "config.py", "type": "file"},
                {"name": "models.py", "type": "file"},
                {"name": "routes.py", "type": "file"},
                {"name": "requirements.txt", "type": "file"},
                {"name": ".env.example", "type": "file"},
            ]
        }
    if fw == 'django':
        return {
            "name": backend_name, "type": "directory", "children": [
                {"name": "manage.py", "type": "file"},
                {"name": "requirements.txt", "type": "file"},
                {"name": "core", "type": "directory", "children": [
                    {"name": "__init__.py", "type": "file"},
                    {"name": "settings.py", "type": "file"},
                    {"name": "urls.py", "type": "file"},
                    {"name": "wsgi.py", "type": "file"},
                ]},
            ]
        }
    if fw == 'express':
        return {
            "name": backend_name, "type": "directory", "children": [
                {"name": "src", "type": "directory", "children": [
                    {"name": "app.js", "type": "file"},
                    {"name": "server.js", "type": "file"},
                    {"name": "routes", "type": "directory", "children": [{"name": "index.js", "type": "file"}]},
                    {"name": "controllers", "type": "directory", "children": [{"name": "homeController.js", "type": "file"}]},
                    {"name": "middlewares", "type": "directory", "children": [{"name": "errorHandler.js", "type": "file"}]},
                    {"name": "utils", "type": "directory", "children": [{"name": "logger.js", "type": "file"}]},
                ]},
                {"name": ".env.example", "type": "file"},
                {"name": "package.json", "type": "file"},
                {"name": "README.md", "type": "file"},
            ]
        }
    if fw == 'nextjs':
        return {
            "name": backend_name, "type": "directory", "children": [
                {"name": "pages", "type": "directory", "children": [
                    {"name": "api", "type": "directory", "children": [
                        {"name": "hello.js", "type": "file"},
                        {"name": "items.js", "type": "file"},
                    ]}
                ]},
                {"name": "next.config.mjs", "type": "file"},
                {"name": "package.json", "type": "file"},
            ]
        }
    return {
        "name": backend_name, "type": "directory", "children": []
    }

def preview_frontend_tree(config: Dict) -> Optional[Dict]:
    fw = normalize_frontend(config.get('frontend_framework'))
    if not fw:
        return None
    frontend_name = config.get('frontend_folder_name', 'frontend')

    if fw == 'react':
        return {
            "name": frontend_name, "type": "directory", "children": [
                {"name": "src", "type": "directory", "children": [
                    {"name": "App.jsx", "type": "file"},
                    {"name": "main.jsx", "type": "file"},
                    {"name": "index.css", "type": "file"},
                ]},
                {"name": "public", "type": "directory", "children": [{"name": "favicon.ico", "type": "file"}]},
                {"name": "index.html", "type": "file"},
                {"name": "package.json", "type": "file"},
            ]
        }
    if fw == 'vue':
        return {
            "name": frontend_name, "type": "directory", "children": [
                {"name": "src", "type": "directory", "children": [
                    {"name": "App.vue", "type": "file"}, {"name": "main.js", "type": "file"}
                ]},
                {"name": "index.html", "type": "file"},
                {"name": "package.json", "type": "file"},
            ]
        }
    if fw == 'svelte':
        return {
            "name": frontend_name, "type": "directory", "children": [
                {"name": "src", "type": "directory", "children": [
                    {"name": "App.svelte", "type": "file"}, {"name": "app.css", "type": "file"},
                    {"name": "lib", "type": "directory", "children": [{"name": "api.js", "type": "file"}, {"name": "utils.js", "type": "file"}]},
                    {"name": "routes", "type": "directory", "children": [
                        {"name": "Home.svelte", "type": "file"}, {"name": "Explorer.svelte", "type": "file"}, {"name": "CreateFile.svelte", "type": "file"}, {"name": "DBDesigner.svelte", "type": "file"}
                    ]}
                ]},
                {"name": "public", "type": "directory", "children": [{"name": "logo.png", "type": "file"}]},
                {"name": "index.html", "type": "file"},
                {"name": "vite.config.js", "type": "file"},
                {"name": "tailwind.config.js", "type": "file"},
                {"name": "postcss.config.js", "type": "file"},
                {"name": "package.json", "type": "file"},
            ]
        }
    if fw == 'nextjs':
        return {
            "name": frontend_name, "type": "directory", "children": [
                {"name": "app", "type": "directory", "children": [
                    {"name": "layout.jsx", "type": "file"}, {"name": "page.jsx", "type": "file"}
                ]},
                {"name": "next.config.mjs", "type": "file"},
                {"name": "package.json", "type": "file"},
            ]
        }
    return {
        "name": frontend_name, "type": "directory", "children": []
    }

# ---------- Builders (actual files) ----------

def build_backend(project_root: Path, config: Dict) -> Dict:
    backend_name = config.get('backend_folder_name', 'backend')
    backend_path = project_root / backend_name
    framework = normalize_backend(config.get('backend_framework'))
    status = {"operations": [], "errors": [], "backend_type": framework}

    try:
        if framework == 'fastapi':
            app_path = backend_path / 'app'
            routes_path = app_path / 'routes'
            app_path.mkdir(parents=True, exist_ok=True)
            routes_path.mkdir(exist_ok=True)
            files = {
                'app.py': BackendTemplates.fastapi_root_app(config),
                'app/__init__.py': '',
                'app/main.py': BackendTemplates.fastapi_main(config),
                'app/database.py': BackendTemplates.fastapi_database(config),
                'app/models.py': BackendTemplates.fastapi_models(config),
                'app/schemas.py': BackendTemplates.fastapi_schemas(config),
                'app/crud.py': BackendTemplates.fastapi_crud(config),
                'app/routes/__init__.py': '',
                'app/routes/project_routes.py': BackendTemplates.fastapi_routes(config),
                'requirements.txt': BackendTemplates.fastapi_requirements(),
                '.env.example': BackendTemplates.env_example(config),
            }
            for file_path, content in files.items():
                fp = backend_path / file_path
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(content)
                status['operations'].append(f"✅ Created: {backend_name}/{file_path}")
        elif framework == 'flask':
            backend_path.mkdir(parents=True, exist_ok=True)
            files = {
                'app.py': BackendTemplates.flask_app(config),
                'config.py': BackendTemplates.flask_config(config),
                'models.py': BackendTemplates.flask_models(config),
                'routes.py': BackendTemplates.flask_routes(config),
                'requirements.txt': BackendTemplates.flask_requirements(),
                '.env.example': BackendTemplates.env_example(config),
            }
            for file_path, content in files.items():
                (backend_path / file_path).write_text(content)
                status['operations'].append(f"✅ Created: {backend_name}/{file_path}")
        elif framework == 'django':
            backend_path.mkdir(parents=True, exist_ok=True)
            core_path = backend_path / 'core'
            core_path.mkdir(exist_ok=True)
            files = {
                'manage.py': BackendTemplates.django_manage(config),
                'requirements.txt': BackendTemplates.django_requirements(),
                'core/__init__.py': '',
                'core/settings.py': BackendTemplates.django_settings(config),
                'core/urls.py': BackendTemplates.django_urls(config),
                'core/wsgi.py': BackendTemplates.django_wsgi(config),
            }
            for file_path, content in files.items():
                (backend_path / file_path).write_text(content)
                status['operations'].append(f"✅ Created: {backend_name}/{file_path}")
        elif framework == 'express':
            backend_path.mkdir(parents=True, exist_ok=True)
            (backend_path / 'src' / 'routes').mkdir(parents=True, exist_ok=True)
            (backend_path / 'src' / 'controllers').mkdir(parents=True, exist_ok=True)
            (backend_path / 'src' / 'middlewares').mkdir(parents=True, exist_ok=True)
            (backend_path / 'src' / 'utils').mkdir(parents=True, exist_ok=True)
            files = {
                'package.json': BackendTemplates.express_package_json(config),
                'src/app.js': BackendTemplates.express_app_js(config),
                'src/server.js': BackendTemplates.express_server_js(config),
                'src/routes/index.js': BackendTemplates.express_routes_index_js(config),
                'src/controllers/homeController.js': BackendTemplates.express_home_controller_js(config),
                'src/middlewares/errorHandler.js': BackendTemplates.express_error_handler_js(config),
                'src/utils/logger.js': BackendTemplates.express_logger_js(config),
                '.env.example': BackendTemplates.express_env_example(config),
                'README.md': BackendTemplates.express_readme(config),
            }
            for file_path, content in files.items():
                fp = backend_path / file_path
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(content)
                status['operations'].append(f"✅ Created: {backend_name}/{file_path}")
        elif framework == 'nextjs':
            backend_path.mkdir(parents=True, exist_ok=True)
            pages_api = backend_path / 'pages' / 'api'
            pages_api.mkdir(parents=True, exist_ok=True)
            (backend_path / 'package.json').write_text('{\n  "name": "nextjs-api-backend",\n  "private": true,\n  "version": "1.0.0",\n  "type": "module",\n  "scripts": { "dev": "next dev -p 5177", "build": "next build", "start": "next start -p 5177" },\n  "dependencies": { "next": "latest", "react": "^18", "react-dom": "^18" }\n}\n')
            (backend_path / 'next.config.mjs').write_text('/** @type {import(\'next\').NextConfig} */\nconst nextConfig = { reactStrictMode: true }\nexport default nextConfig\n')
            (pages_api / 'hello.js').write_text("export default function handler(req, res) {\n  res.status(200).json({ message: 'Hello from Next.js API' })\n}\n")
            (pages_api / 'items.js').write_text("let items = [{ id: 1, title: 'Sample item' }]\nexport default function handler(req, res) {\n  if (req.method === 'GET') return res.status(200).json(items)\n  if (req.method === 'POST') { const item = { id: Date.now(), ...(req.body||{}) }; items.push(item); return res.status(201).json(item) }\n  res.status(405).json({ error: 'Method not allowed' })\n}\n")
            status['operations'].append(f"✅ Created: {backend_name}/Next.js API scaffold")
        else:
            # Unknown/none
            backend_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        status['errors'].append(str(e))
    return status

def build_frontend(project_root: Path, config: Dict) -> Dict:
    frontend_name = config.get('frontend_folder_name', 'frontend')
    frontend_path = project_root / frontend_name
    framework = normalize_frontend(config.get('frontend_framework'))
    status = {"operations": [], "errors": [], "frontend_type": framework}

    try:
        if framework == 'react':
            src_path = frontend_path / 'src'
            public_path = frontend_path / 'public'
            src_path.mkdir(parents=True, exist_ok=True)
            public_path.mkdir(exist_ok=True)
            files = {
                'package.json': FrontendTemplates.react_package_json(config),
                'index.html': FrontendTemplates.react_index_html(config),
                'src/App.jsx': FrontendTemplates.react_app(config),
                'src/main.jsx': FrontendTemplates.react_main(config),
                'src/index.css': FrontendTemplates.react_css(config),
            }
            for file_path, content in files.items():
                fp = frontend_path / file_path
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(content)
                status['operations'].append(f"✅ Created: {frontend_name}/{file_path}")
        elif framework == 'vue':
            src_path = frontend_path / 'src'
            src_path.mkdir(parents=True, exist_ok=True)
            files = {
                'package.json': FrontendTemplates.vue_package_json(config),
                'index.html': FrontendTemplates.vue_index_html(config),
                'src/App.vue': FrontendTemplates.vue_app(config),
                'src/main.js': FrontendTemplates.vue_main(config),
            }
            for file_path, content in files.items():
                (frontend_path / file_path).write_text(content)
                status['operations'].append(f"✅ Created: {frontend_name}/{file_path}")
        elif framework == 'svelte':
            (frontend_path / 'src' / 'lib').mkdir(parents=True, exist_ok=True)
            (frontend_path / 'src' / 'routes').mkdir(parents=True, exist_ok=True)
            (frontend_path / 'public').mkdir(parents=True, exist_ok=True)
            files = {
                'package.json': FrontendTemplates.svelte_package_json(config),
                'vite.config.js': FrontendTemplates.svelte_vite_config(config),
                'index.html': FrontendTemplates.svelte_index_html(config),
                'tailwind.config.js': FrontendTemplates.tailwind_config(config, framework='svelte'),
                'postcss.config.js': FrontendTemplates.postcss_config(),
                'src/App.svelte': FrontendTemplates.svelte_app(config),
'src/app.css': FrontendTemplates.svelte_app_css(config),
                'src/main.js': FrontendTemplates.svelte_main_js(config),
                'src/lib/api.js': FrontendTemplates.svelte_lib_api_js(config),
                'src/lib/utils.js': FrontendTemplates.svelte_lib_utils_js(config),
                'src/routes/Home.svelte': FrontendTemplates.svelte_home(config),
                'src/routes/Explorer.svelte': FrontendTemplates.svelte_explorer(config),
                'src/routes/CreateFile.svelte': FrontendTemplates.svelte_create_file(config),
                'src/routes/DBDesigner.svelte': FrontendTemplates.svelte_db_designer(config),
            }
            for file_path, content in files.items():
                fp = frontend_path / file_path
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(content)
                status['operations'].append(f"✅ Created: {frontend_name}/{file_path}")
            (frontend_path / 'public' / 'logo.png').write_text('placeholder')
        elif framework == 'nextjs':
            frontend_path.mkdir(parents=True, exist_ok=True)
            app_path = frontend_path / 'app'
            app_path.mkdir(parents=True, exist_ok=True)
            files = {
                'package.json': FrontendTemplates.nextjs_package_json(config),
                'next.config.mjs': FrontendTemplates.nextjs_config(config),
                'app/layout.jsx': FrontendTemplates.nextjs_layout(config),
                'app/page.jsx': FrontendTemplates.nextjs_page(config),
            }
            for file_path, content in files.items():
                fp = frontend_path / file_path
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(content)
                status['operations'].append(f"✅ Created: {frontend_name}/{file_path}")
        else:
            frontend_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        status['errors'].append(str(e))
    return status
