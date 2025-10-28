# backend/app/services/project_generator.py
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from .frameworks.registry import (
    preview_backend_tree,
    preview_frontend_tree,
    build_backend as registry_build_backend,
    build_frontend as registry_build_frontend,
)


class ProjectGenerator:
    """
    Core service for generating project structures with files and folders
    """
    
    def __init__(self, base_output_dir: str = "/tmp/generated_projects"):
        self.base_output_dir = base_output_dir
        os.makedirs(base_output_dir, exist_ok=True)
    
    def _normalize_rel(self, raw: str, config: Dict) -> str:
        """Normalize any user path to a safe project-relative path.
        - Strips everything up to <project_name>/ if present (case-insensitive)
        - If 'backend' or 'frontend' appears anywhere, slices from that anchor and maps
          to configured folder names
        - Removes parent traversals
        """
        s = str(raw).replace('\\', '/').strip()
        parts = [p for p in s.split('/') if p]
        lowers = [p.lower() for p in parts]
        proj = (config.get('project_name') or '').lower()
        
# If project name appears, remove everything before it
        if proj in lowers:
            i = lowers.index(proj)
            parts = parts[i+1:]
            lowers = lowers[i+1:]
        # anchor slice
        if 'backend' in lowers or 'frontend' in lowers:
            if 'backend' in lowers:
                i = lowers.index('backend')
                parts = parts[i:]
                lowers = lowers[i:]
                parts[0] = config.get('backend_folder_name', 'backend')
            else:
                i = lowers.index('frontend')
                parts = parts[i:]
                lowers = lowers[i:]
                parts[0] = config.get('frontend_folder_name', 'frontend')
        # join cleaned parts, remove any parent traversal markers and
        # ensure the returned path is always a relative path (no leading slash)
        rel = '/'.join(parts)
        # remove any parent traversal remnants
        rel = rel.replace('..', '')
        # strip any leading path separators just in case an absolute-like
        # component slipped through (prevents Path(project_root) / rel
        # from becoming absolute)
        rel = rel.lstrip('/\\')
        # collapse repeated separators and empty segments
        rel = '/'.join([p for p in rel.split('/') if p])
        return rel
    
    def generate_project_tree(self, config: Dict) -> Dict:
        """
        Generate a preview of the project structure without creating files
        Returns a tree structure representation
        """
        # Special-case: Next.js fullstack (single app) when both sides selected as Next.js
        bf = str((config.get('backend_framework') or '').lower())
        ff = str((config.get('frontend_framework') or '').lower())
        bnorm = 'nextjs' if bf in ['nextjs','next','next.js','nextjs-api','nextjs_api','nextjsapi'] else bf
        fnorm = 'nextjs' if ff in ['nextjs','next','next.js'] else ff
        if bnorm == 'nextjs' and fnorm == 'nextjs':
            return self._next_fullstack_tree(config)

        tree = {
            "name": config["project_name"],
            "type": "directory",
            "children": []
        }
        
        # Backend tree via registry
        be_tree = preview_backend_tree(config)
        if be_tree:
            tree["children"].append(be_tree)
        
        # Frontend tree via registry
        fe_tree = preview_frontend_tree(config)
        if fe_tree:
            tree["children"].append(fe_tree)
        
        # Add common folders and any file-like entries passed via custom_folders
        def _is_file_like(name: str) -> bool:
            from pathlib import Path as _P
            return bool(_P(str(name)).suffix)
        
        for entry in config.get("custom_folders", ["docs", "tests"]):
            rel = self._normalize_rel(entry, config)
            if rel and _is_file_like(rel):
                tree["children"].append({
                    "name": rel,
                    "type": "file"
                })
            elif rel:
                tree["children"].append({
                    "name": rel,
                    "type": "directory",
                    "children": []
                })
        
        # Add explicitly specified custom files (if any)
        for f in config.get("custom_files", []):
            name = (f or {}).get("name")
            if name:
                relname = self._normalize_rel(name, config)
                if relname:
                    tree["children"].append({
                        "name": relname,
                        "type": "file"
                    })
        
        # Add root files
        root_files = ["README.md", ".gitignore"]
        if config.get("initialize_git"):
            root_files.append(".git")
        
        for file in root_files:
            tree["children"].append({
                "name": file,
                "type": "file"
            })
        
        return tree
    
    def _generate_backend_tree(self, framework: str, config: Dict) -> Dict:
        """Generate backend folder structure based on framework"""
        backend_name = config.get("backend_folder_name", "backend")
        # Apply same alias normalization used in preview
        aliases = {
            "express.js": "express", "expressjs": "express", "node": "express", "nodejs": "express",
            "nest": "nestjs", "nestjs.js": "nestjs",
            "next": "nextjs", "next.js": "nextjs", "nextjs-api": "nextjs", "nextjs_api": "nextjs", "nextjsapi": "nextjs"
        }
        fw = aliases.get(framework.lower(), framework.lower())
        
        if fw == "fastapi":
            return {
                "name": backend_name,
                "type": "directory",
                "children": [
                    {
                        "name": "app",
                        "type": "directory",
                        "children": [
                            {"name": "__init__.py", "type": "file"},
                            {"name": "main.py", "type": "file"},
                            {"name": "database.py", "type": "file"},
                            {"name": "models.py", "type": "file"},
                            {"name": "schemas.py", "type": "file"},
                            {"name": "crud.py", "type": "file"},
                            {
                                "name": "routes",
                                "type": "directory",
                                "children": [
                                    {"name": "__init__.py", "type": "file"},
                                    {"name": "api_routes.py", "type": "file"}
                                ]
                            }
                        ]
                    },
                    {"name": "requirements.txt", "type": "file"},
                    {"name": ".env.example", "type": "file"}
                ]
            }
        elif fw == "flask":
            return {
                "name": backend_name,
                "type": "directory",
                "children": [
                    {"name": "app.py", "type": "file"},
                    {"name": "config.py", "type": "file"},
                    {"name": "models.py", "type": "file"},
                    {"name": "routes.py", "type": "file"},
                    {"name": "requirements.txt", "type": "file"},
                    {"name": ".env.example", "type": "file"}
                ]
            }
        elif fw == "django":
            return {
                "name": backend_name,
                "type": "directory",
                "children": [
                    {"name": "manage.py", "type": "file"},
                    {"name": "requirements.txt", "type": "file"},
                    {
                        "name": "core",
                        "type": "directory",
                        "children": [
                            {"name": "__init__.py", "type": "file"},
                            {"name": "settings.py", "type": "file"},
                            {"name": "urls.py", "type": "file"},
                            {"name": "wsgi.py", "type": "file"}
                        ]
                    }
                ]
            }
        elif fw in ["express", "nestjs"]:
            return {
                "name": backend_name,
                "type": "directory",
                "children": [
                    {"name": "package.json", "type": "file"},
                    {"name": "server.js", "type": "file"},
                    {"name": ".env.example", "type": "file"}
                ]
            }
        elif fw in ["nextjs", "nextjs-api", "nextjs_api", "nextjsapi"]:
            return {
                "name": backend_name,
                "type": "directory",
                "children": [
                    {"name": "package.json", "type": "file"},
                    {"name": "next.config.mjs", "type": "file"},
                    {
                        "name": "pages",
                        "type": "directory",
                        "children": [
                            {
                                "name": "api",
                                "type": "directory",
                                "children": [
                                    {"name": "hello.js", "type": "file"},
                                    {"name": "items.js", "type": "file"}
                                ]
                            }
                        ]
                    }
                ]
            }
        else:
            return {
                "name": backend_name,
                "type": "directory",
                "children": []
            }
    
    def _generate_frontend_tree(self, framework: str, config: Dict) -> Dict:
        """Generate frontend folder structure based on framework"""
        frontend_name = config.get("frontend_folder_name", "frontend")
        fw = framework.lower()
        
        if fw == "react":
            return {
                "name": frontend_name,
                "type": "directory",
                "children": [
                    {"name": "package.json", "type": "file"},
                    {"name": "index.html", "type": "file"},
                    {
                        "name": "src",
                        "type": "directory",
                        "children": [
                            {"name": "App.jsx", "type": "file"},
                            {"name": "main.jsx", "type": "file"},
                            {"name": "index.css", "type": "file"}
                        ]
                    },
                    {
                        "name": "public",
                        "type": "directory",
                        "children": [
                            {"name": "favicon.ico", "type": "file"}
                        ]
                    }
                ]
            }
        elif fw == "vue":
            return {
                "name": frontend_name,
                "type": "directory",
                "children": [
                    {"name": "package.json", "type": "file"},
                    {"name": "index.html", "type": "file"},
                    {
                        "name": "src",
                        "type": "directory",
                        "children": [
                            {"name": "App.vue", "type": "file"},
                            {"name": "main.js", "type": "file"}
                        ]
                    }
                ]
            }
        elif fw == "svelte":
            return {
                "name": frontend_name,
                "type": "directory",
                "children": [
                    {"name": "package.json", "type": "file"},
                    {"name": "index.html", "type": "file"},
                    {"name": "vite.config.js", "type": "file"},
                    {"name": "tailwind.config.js", "type": "file"},
                    {"name": "postcss.config.js", "type": "file"},
                    {"name": "public/logo.png", "type": "file"},
                    {
                        "name": "src",
                        "type": "directory",
                        "children": [
                            {"name": "App.svelte", "type": "file"},
                            {"name": "app.css", "type": "file"},
                            {"name": "lib", "type": "directory", "children": [
                                {"name": "api.js", "type": "file"},
                                {"name": "utils.js", "type": "file"}
                            ]},
                            {"name": "routes", "type": "directory", "children": [
                                {"name": "Home.svelte", "type": "file"},
                                {"name": "Explorer.svelte", "type": "file"},
                                {"name": "CreateFile.svelte", "type": "file"},
                                {"name": "DBDesigner.svelte", "type": "file"}
                            ]}
                        ]
                    }
                ]
            }
        elif fw == "angular":
            return {
                "name": frontend_name,
                "type": "directory",
                "children": [
                    {"name": "package.json", "type": "file"},
                    {"name": "angular.json", "type": "file"},
                    {"name": "tsconfig.json", "type": "file"},
                    {
                        "name": "src",
                        "type": "directory",
                        "children": [
                            {"name": "index.html", "type": "file"},
                            {"name": "main.ts", "type": "file"},
                            {
                                "name": "app",
                                "type": "directory",
                                "children": [
                                    {"name": "app.component.ts", "type": "file"},
                                    {"name": "app.component.html", "type": "file"}
                                ]
                            }
                        ]
                    }
                ]
            }
        elif fw == "nextjs":
            return {
                "name": frontend_name,
                "type": "directory",
                "children": [
                    {"name": "package.json", "type": "file"},
                    {"name": "next.config.mjs", "type": "file"},
                    {"name": "app", "type": "directory", "children": [
                        {"name": "layout.jsx", "type": "file"},
                        {"name": "page.jsx", "type": "file"}
                    ]}
                ]
            }
        else:
            return {
                "name": frontend_name,
                "type": "directory",
                "children": [
                    {"name": "index.html", "type": "file"},
                    {"name": "style.css", "type": "file"},
                    {"name": "script.js", "type": "file"}
                ]
            }
    
    def build_project(self, config: Dict, target_directory: Optional[str] = None) -> Dict:
        """
        Actually create the project files and folders on disk
        Returns status of operations
        """
        if target_directory is None:
            target_directory = os.path.join(self.base_output_dir, config["project_name"])
        
        project_root = Path(target_directory)
        
        status = {
            "success": True,
            "project_path": str(project_root),
            "operations": [],
            "errors": []
        }
        
        try:
            # Create root directory
            project_root.mkdir(parents=True, exist_ok=True)
            status["operations"].append(f"✅ Created project root: {project_root}")

            # Special-case: Next.js fullstack single app
            bf = str((config.get('backend_framework') or '').lower())
            ff = str((config.get('frontend_framework') or '').lower())
            bnorm = 'nextjs' if bf in ['nextjs','next','next.js','nextjs-api','nextjs_api','nextjsapi'] else bf
            fnorm = 'nextjs' if ff in ['nextjs','next','next.js'] else ff
            if bnorm == 'nextjs' and fnorm == 'nextjs':
                fs = self._create_next_fullstack(project_root, config)
                status["operations"].append("🔧 Backend: nextjs (fullstack)")
                status["operations"].append("🎨 Frontend: nextjs (fullstack)")
                status["operations"].extend(fs["operations"])
                status["errors"].extend(fs.get("errors", []))
            else:
                # Create backend
                if config.get("backend_framework"):
                    backend_status = registry_build_backend(project_root, config)
                    bt = backend_status.get("backend_type")
                    if bt:
                        status["operations"].append(f"🔧 Backend: {bt}")
                    status["operations"].extend(backend_status["operations"])
                    status["errors"].extend(backend_status.get("errors", []))
                    # Fallback: if registry produced nothing OR the backend folder is effectively empty
                    try:
                        backend_name = config.get("backend_folder_name", "backend")
                        backend_path = project_root / backend_name
                        is_empty = True
                        if backend_path.exists():
                            for _p in backend_path.rglob('*'):
                                is_empty = False
                                break
                        if (not backend_status.get("operations")) or is_empty:
                            legacy = self._create_backend(project_root, config)
                            status["operations"].extend(legacy.get("operations", []))
                            status["errors"].extend(legacy.get("errors", []))
                    except Exception as _e:
                        status["errors"].append(f"❌ Backend fallback error: {_e}")
                
                # Create frontend
                ffw_raw = str(config.get("frontend_framework") or "").strip()
                if ffw_raw:
                    frontend_status = registry_build_frontend(project_root, config)
                    ft = frontend_status.get("frontend_type")
                    if ft:
                        status["operations"].append(f"🎨 Frontend: {ft}")
                    status["operations"].extend(frontend_status["operations"])
                    status["errors"].extend(frontend_status.get("errors", []))
            
            # Create custom folders and file-like entries
            def _is_file_like(name: str) -> bool:
                from pathlib import Path as _P
                return bool(_P(str(name)).suffix)
            
            for entry in config.get("custom_folders", ["docs", "tests"]):
                if not entry:
                    continue
                rel_norm = self._normalize_rel(entry, config)
                if _is_file_like(rel_norm):
                    rel = rel_norm.replace('..', '')
                    file_path = project_root / rel
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_path.write_text("")
                    status["operations"].append(f"✅ Created file: {rel}")
                elif rel_norm:
                    rel_dir = rel_norm.replace('..', '')
                    folder_path = project_root / rel_dir
                    folder_path.mkdir(parents=True, exist_ok=True)
                    status["operations"].append(f"✅ Created folder: {rel_dir}")
            
            # Create explicitly specified custom files
            for f in config.get("custom_files", []):
                try:
                    name = str((f or {}).get("name", "")).strip()
                    if not name:
                        continue
                    content = (f or {}).get("content", "")
                    from pathlib import Path as _P
                    rel = self._normalize_rel(name, config)
                    dest = project_root / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text(content)
                    status["operations"].append(f"✅ Created file: {rel}")
                except Exception as ce:
                    status["errors"].append(f"❌ Custom file error ({(f or {}).get('name')}): {str(ce)}")
            
            # Create root files
            self._create_readme(project_root, config)
            status["operations"].append("✅ Created README.md")
            
            self._create_gitignore(project_root, config)
            status["operations"].append("✅ Created .gitignore")

            # Generate helper scripts (setup.sh, setup.bat, db_setup.sh, Docker, etc.)
            try:
                from .script_generator import ScriptGenerator
                scripts = ScriptGenerator.generate_setup_scripts(config)
                for name, content in scripts.items():
                    fp = project_root / name
                    fp.write_text(content)
                    # Make shell scripts executable
                    if name.endswith('.sh'):
                        try:
                            import os, stat
                            os.chmod(fp, os.stat(fp).st_mode | stat.S_IXUSR)
                        except Exception:
                            pass
                    status["operations"].append(f"✅ Created script: {name}")
            except Exception as se:
                status["errors"].append(f"❌ Script generation error: {str(se)}")
            
            # Initialize git if requested
            if config.get("initialize_git"):
                import subprocess
                subprocess.run(["git", "init"], cwd=project_root, capture_output=True)
                status["operations"].append("✅ Initialized Git repository")
            
        except Exception as e:
            status["success"] = False
            status["errors"].append(f"❌ Error: {str(e)}")
            
        return status
    
    def _create_backend(self, project_root: Path, config: Dict) -> Dict:
        """Create backend structure and files"""
        from .templates import BackendTemplates
        
        backend_name = config.get("backend_folder_name", "backend")
        backend_path = project_root / backend_name
        fw_raw = str(config.get("backend_framework") or "").strip().lower()
        aliases = {
            "express.js": "express", "expressjs": "express", "node": "express", "nodejs": "express",
            "nest": "nestjs", "nestjs.js": "nestjs",
            "next": "nextjs", "next.js": "nextjs", "nextjs-api": "nextjs", "nextjs_api": "nextjs", "nextjsapi": "nextjs"
        }
        framework = aliases.get(fw_raw, fw_raw)
        
        status = {"operations": [], "errors": [], "backend_type": framework}
        
        try:
            if framework == "fastapi":
                # Create structure
                app_path = backend_path / "app"
                routes_path = app_path / "routes"
                
                app_path.mkdir(parents=True, exist_ok=True)
                routes_path.mkdir(exist_ok=True)
                
                # Create files
                files = {
                    "app.py": BackendTemplates.fastapi_root_app(config),
                    "app/__init__.py": "",
                    "app/main.py": BackendTemplates.fastapi_main(config),
                    "app/database.py": BackendTemplates.fastapi_database(config),
                    "app/models.py": BackendTemplates.fastapi_models(config),
                    "app/schemas.py": BackendTemplates.fastapi_schemas(config),
                    "app/crud.py": BackendTemplates.fastapi_crud(config),
                    "app/routes/__init__.py": "",
                    "app/routes/project_routes.py": BackendTemplates.fastapi_routes(config),
                    "requirements.txt": BackendTemplates.fastapi_requirements(),
                    ".env.example": BackendTemplates.env_example(config)
                }
                
                for file_path, content in files.items():
                    full_path = backend_path / file_path
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content)
                    status["operations"].append(f"✅ Created: {backend_name}/{file_path}")
            
            elif framework == "flask":
                backend_path.mkdir(parents=True, exist_ok=True)
                files = {
                    "app.py": BackendTemplates.flask_app(config),
                    "config.py": BackendTemplates.flask_config(config),
                    "models.py": BackendTemplates.flask_models(config),
                    "routes.py": BackendTemplates.flask_routes(config),
                    "requirements.txt": BackendTemplates.flask_requirements(),
                    ".env.example": BackendTemplates.env_example(config)
                }
                
                for file_path, content in files.items():
                    (backend_path / file_path).write_text(content)
                    status["operations"].append(f"✅ Created: {backend_name}/{file_path}")
            
            elif framework == "django":
                backend_path.mkdir(parents=True, exist_ok=True)
                core_path = backend_path / "core"
                core_path.mkdir(exist_ok=True)
                
                files = {
                    "manage.py": BackendTemplates.django_manage(config),
                    "requirements.txt": BackendTemplates.django_requirements(),
                    "core/__init__.py": "",
                    "core/settings.py": BackendTemplates.django_settings(config),
                    "core/urls.py": BackendTemplates.django_urls(config),
                    "core/wsgi.py": BackendTemplates.django_wsgi(config)
                }
                
                for file_path, content in files.items():
                    (backend_path / file_path).write_text(content)
                    status["operations"].append(f"✅ Created: {backend_name}/{file_path}")
            
            elif framework == "express":
                backend_path.mkdir(parents=True, exist_ok=True)
                # Create modular structure
                (backend_path / "src" / "routes").mkdir(parents=True, exist_ok=True)
                (backend_path / "src" / "controllers").mkdir(parents=True, exist_ok=True)
                (backend_path / "src" / "middlewares").mkdir(parents=True, exist_ok=True)
                (backend_path / "src" / "utils").mkdir(parents=True, exist_ok=True)
                files = {
                    "package.json": BackendTemplates.express_package_json(config),
                    "src/app.js": BackendTemplates.express_app_js(config),
                    "src/server.js": BackendTemplates.express_server_js(config),
                    "src/routes/index.js": BackendTemplates.express_routes_index_js(config),
                    "src/controllers/homeController.js": BackendTemplates.express_home_controller_js(config),
                    "src/middlewares/errorHandler.js": BackendTemplates.express_error_handler_js(config),
                    "src/utils/logger.js": BackendTemplates.express_logger_js(config),
                    ".env.example": BackendTemplates.express_env_example(config),
                    "README.md": BackendTemplates.express_readme(config)
                }
                for file_path, content in files.items():
                    full = backend_path / file_path
                    full.parent.mkdir(parents=True, exist_ok=True)
                    full.write_text(content)
                    status["operations"].append(f"✅ Created: {backend_name}/{file_path}")
            
            elif framework in ["nextjs", "nextjs-api", "nextjs_api", "nextjsapi"]:
                backend_path.mkdir(parents=True, exist_ok=True)
                # Minimal Next.js project focused on API routes (backend port 5177)
                pages_api = backend_path / "pages" / "api"
                pages_api.mkdir(parents=True, exist_ok=True)
                (backend_path / "package.json").write_text("""{
  \"name\": \"nextjs-api-backend\",
  \"private\": true,
  \"version\": \"1.0.0\",
  \"type\": \"module\",
  \"scripts\": {
    \"dev\": \"next dev -p 5177\",
    \"build\": \"next build\",
    \"start\": \"next start -p 5177\"
  },
  \"dependencies\": {
    \"next\": \"latest\",
    \"react\": \"^18\",
    \"react-dom\": \"^18\"
  }
}\n""")
                (backend_path / "next.config.mjs").write_text("""/** @type {import('next').NextConfig} */
const nextConfig = { reactStrictMode: true }
export default nextConfig
""")
                # API routes
                (pages_api / "hello.js").write_text("""export default function handler(req, res) {
  res.status(200).json({ message: 'Hello from Next.js API' })
}
""")
                (pages_api / "items.js").write_text("""let items = [{ id: 1, title: 'Sample item' }]
export default function handler(req, res) {
  if (req.method === 'GET') return res.status(200).json(items)
  if (req.method === 'POST') { const item = { id: Date.now(), ...(req.body||{}) }; items.push(item); return res.status(201).json(item) }
  res.status(405).json({ error: 'Method not allowed' })
}
""")
                status["operations"].append(f"✅ Created: {backend_name}/Next.js API scaffold")
            
        except Exception as e:
            status["errors"].append(f"❌ Backend error: {str(e)}")
        
        return status
    
    def _next_fullstack_tree(self, config: Dict) -> Dict:
        name = config.get('project_name')
        return {
            "name": name,
            "type": "directory",
            "children": [
                {"name": "app", "type": "directory", "children": [
                    {"name": "api", "type": "directory", "children": [
                        {"name": "v1", "type": "directory", "children": [
                            {"name": "hello", "type": "directory", "children": [ {"name": "route.ts", "type": "file"} ] },
                            {"name": "users", "type": "directory", "children": [ {"name": "route.ts", "type": "file"} ] }
                        ]}
                    ]},
                    {"name": "components", "type": "directory", "children": [
                        {"name": "Navbar.tsx", "type": "file"},
                        {"name": "Footer.tsx", "type": "file"},
                        {"name": "Button.tsx", "type": "file"}
                    ]},
                    {"name": "layout.tsx", "type": "file"},
                    {"name": "page.tsx", "type": "file"},
                    {"name": "globals.css", "type": "file"}
                ]},
                {"name": "public", "type": "directory", "children": [
                    {"name": "favicon.ico", "type": "file"},
                    {"name": "images", "type": "directory"}
                ]},
                {"name": ".env.example", "type": "file"},
                {"name": "next.config.mjs", "type": "file"},
                {"name": "postcss.config.mjs", "type": "file"},
                {"name": "tailwind.config.mjs", "type": "file"},
                {"name": "tsconfig.json", "type": "file"},
                {"name": "package.json", "type": "file"},
                {"name": "README.md", "type": "file"}
            ]
        }

    def _create_next_fullstack(self, project_root: Path, config: Dict) -> Dict:
        ops, errs = [], []
        try:
            (project_root / 'app' / 'api' / 'v1' / 'hello').mkdir(parents=True, exist_ok=True)
            (project_root / 'app' / 'api' / 'v1' / 'users').mkdir(parents=True, exist_ok=True)
            (project_root / 'app' / 'components').mkdir(parents=True, exist_ok=True)
            (project_root / 'public' / 'images').mkdir(parents=True, exist_ok=True)
            files = {
                'package.json': """{
  "name": "nextjs-boilerplate",
  "version": "1.0.0",
  "private": true,
  "scripts": { "dev": "next dev -p 3010", "build": "next build", "start": "next start", "lint": "next lint" },
  "dependencies": { "next": "latest", "react": "^18", "react-dom": "^18" },
  "devDependencies": { "autoprefixer": "^10", "postcss": "^8", "tailwindcss": "^3", "typescript": "^5" }
}
""",
                'next.config.mjs': """/** @type {import('next').NextConfig} */
const nextConfig = { reactStrictMode: true, experimental: { appDir: true } }
export default nextConfig
""",
                'postcss.config.mjs': """export default { plugins: { tailwindcss: {}, autoprefixer: {} } }
""",
                'tailwind.config.mjs': """export default { content: ["./app/**/*.{ts,tsx}"], theme: { extend: {} }, plugins: [] }
""",
                'tsconfig.json': """{ "compilerOptions": { "target": "ES2020", "lib": ["dom","dom.iterable","esnext"], "strict": true, "esModuleInterop": true, "module": "esnext", "moduleResolution": "bundler", "resolveJsonModule": true, "isolatedModules": true, "jsx": "preserve", "incremental": true, "plugins": [{ "name": "next" }] }, "include": ["next-env.d.ts","**/*.ts","**/*.tsx"], "exclude": ["node_modules"] }
""",
                '.env.example': """NEXT_PUBLIC_API_URL=http://localhost:3010/api/v1
""",
                'README.md': """# ⚡ Next.js Boilerplate

A clean, modern boilerplate built with **Next.js 14**, **App Router**, **TypeScript**, and **Tailwind CSS**.
""",
                'app/layout.tsx': """import "./globals.css";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
export const metadata = { title: "Next.js Boilerplate", description: "A clean starter for modern Next.js apps" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">
        <Navbar />
        <main className="max-w-4xl mx-auto p-6">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
""",
                'app/page.tsx': """export default function Home(){ return (<div className=\"text-center mt-10\"><h1 className=\"text-4xl font-bold text-blue-600\">🚀 Next.js Boilerplate</h1><p className=\"mt-4 text-lg text-gray-700\">Start building your app instantly — powered by Next.js 14 + Tailwind CSS.</p></div>); }
""",
                'app/components/Navbar.tsx': """import Link from "next/link";
export default function Navbar(){ return (<nav className=\"flex justify-between p-4 shadow bg-white\"><Link href=\"/\" className=\"font-semibold text-blue-600\">NextBoiler</Link><div className=\"space-x-4\"><Link href=\"/about\">About</Link><Link href=\"/contact\">Contact</Link></div></nav>); }
""",
                'app/components/Footer.tsx': """export default function Footer(){ return (<footer className=\"text-center p-4 bg-white shadow mt-10\"><p className=\"text-gray-600\">© 2025 NextBoiler. All rights reserved.</p></footer>); }
""",
                'app/components/Button.tsx': """export default function Button({ children }:{ children: React.ReactNode }){ return (<button className=\"px-4 py-2 bg-blue-600 text-white rounded\">{children}</button>); }
""",
                'app/api/v1/hello/route.ts': """import { NextResponse } from "next/server";
export async function GET(){ return NextResponse.json({ message: "Hello from Next.js API Route!" }); }
""",
                'app/api/v1/users/route.ts': """import { NextResponse } from "next/server";
export async function GET(){ const users=[{id:1,name:"John Doe"},{id:2,name:"Jane Doe"}]; return NextResponse.json(users); }
""",
                'app/globals.css': """@tailwind base;
@tailwind components;
@tailwind utilities;
body { font-family: 'Inter', sans-serif; }
""",
                'public/favicon.ico': 'placeholder',
            }
            for rel, content in files.items():
                fp = project_root / rel
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(content)
                ops.append(f"✅ Created: {rel}")
        except Exception as e:
            errs.append(str(e))
        return { "operations": ops, "errors": errs }

    def _create_frontend(self, project_root: Path, config: Dict) -> Dict:
        """Create frontend structure and files"""
        from .templates import FrontendTemplates
        
        frontend_name = config.get("frontend_folder_name", "frontend")
        frontend_path = project_root / frontend_name
        ffw_raw = str(config.get("frontend_framework") or "").strip().lower()
        aliases = {
            "next": "nextjs", "next.js": "nextjs",
            "solid": "solidjs", "solid.js": "solidjs",
        }
        framework = aliases.get(ffw_raw, ffw_raw)
        
        status = {"operations": [], "errors": [], "frontend_type": framework}
        
        try:
            if framework == "react":
                src_path = frontend_path / "src"
                public_path = frontend_path / "public"
                src_path.mkdir(parents=True, exist_ok=True)
                public_path.mkdir(exist_ok=True)
                
                files = {
                    "package.json": FrontendTemplates.react_package_json(config),
                    "index.html": FrontendTemplates.react_index_html(config),
                    "src/App.jsx": FrontendTemplates.react_app(config),
                    "src/main.jsx": FrontendTemplates.react_main(config),
                    "src/index.css": FrontendTemplates.react_css(config),
                    "src/components/Navbar.jsx": FrontendTemplates.react_navbar(config),
                    "src/components/Hero.jsx": FrontendTemplates.react_hero(config),
                    "src/components/Footer.jsx": FrontendTemplates.react_footer(config),
                    "src/hooks/useLenis.js": FrontendTemplates.react_use_lenis(config),
                    "src/styles/theme.js": FrontendTemplates.react_theme(config),
                    "tailwind.config.js": FrontendTemplates.tailwind_config(config, framework="react"),
                    "postcss.config.js": FrontendTemplates.postcss_config(),
                    "README.md": FrontendTemplates.react_readme(config)
                }
                
                for file_path, content in files.items():
                    full_path = frontend_path / file_path
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content)
                    status["operations"].append(f"✅ Created: {frontend_name}/{file_path}")
            
            elif framework == "vue":
                src_path = frontend_path / "src"
                src_path.mkdir(parents=True, exist_ok=True)
                
                files = {
                    "package.json": FrontendTemplates.vue_package_json(config),
                    "index.html": FrontendTemplates.vue_index_html(config),
                    "src/App.vue": FrontendTemplates.vue_app(config),
                    "src/main.js": FrontendTemplates.vue_main(config)
                }
                
                for file_path, content in files.items():
                    (frontend_path / file_path).write_text(content)
                    status["operations"].append(f"✅ Created: {frontend_name}/{file_path}")
            
            elif framework == "svelte":
                (frontend_path / "src" / "lib").mkdir(parents=True, exist_ok=True)
                (frontend_path / "src" / "routes").mkdir(parents=True, exist_ok=True)
                (frontend_path / "public").mkdir(parents=True, exist_ok=True)

                files = {
                    "package.json": FrontendTemplates.svelte_package_json(config),
                    "vite.config.js": FrontendTemplates.svelte_vite_config(config),
                    "index.html": FrontendTemplates.svelte_index_html(config),
                    "tailwind.config.js": FrontendTemplates.tailwind_config(config, framework="svelte"),
                    "postcss.config.js": FrontendTemplates.postcss_config(),
                    "src/App.svelte": FrontendTemplates.svelte_app(config),
                    "src/app.css": FrontendTemplates.svelte_app_css(config),
                    "src/main.js": FrontendTemplates.svelte_main_js(config),
                    "src/lib/api.js": FrontendTemplates.svelte_lib_api_js(config),
                    "src/lib/utils.js": FrontendTemplates.svelte_lib_utils_js(config),
                    "src/routes/Home.svelte": FrontendTemplates.svelte_home(config),
                    "src/routes/Explorer.svelte": FrontendTemplates.svelte_explorer(config),
                    "src/routes/CreateFile.svelte": FrontendTemplates.svelte_create_file(config),
                    "src/routes/DBDesigner.svelte": FrontendTemplates.svelte_db_designer(config)
                }

                for file_path, content in files.items():
                    full = frontend_path / file_path
                    full.parent.mkdir(parents=True, exist_ok=True)
                    full.write_text(content)
                    status["operations"].append(f"✅ Created: {frontend_name}/{file_path}")
                # placeholder logo
                (frontend_path / "public" / "logo.png").write_text("placeholder")
            
            elif framework == "angular":
                src_path = frontend_path / "src" / "app"
                src_path.mkdir(parents=True, exist_ok=True)
                
                files = {
                    "package.json": FrontendTemplates.angular_package_json(config),
                    "angular.json": FrontendTemplates.angular_json(config),
                    "src/index.html": FrontendTemplates.angular_index_html(config),
                    "src/main.ts": FrontendTemplates.angular_main(config),
                    "src/app/app.component.ts": FrontendTemplates.angular_component(config)
                }
                
                for file_path, content in files.items():
                    full_path = frontend_path / file_path
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content)
                    status["operations"].append(f"✅ Created: {frontend_name}/{file_path}")
            
            elif framework == "nextjs":
                frontend_path.mkdir(parents=True, exist_ok=True)
                app_path = frontend_path / "app"
                app_path.mkdir(parents=True, exist_ok=True)
                files = {
                    "package.json": FrontendTemplates.nextjs_package_json(config),
                    "next.config.mjs": FrontendTemplates.nextjs_config(config),
                    "app/layout.jsx": FrontendTemplates.nextjs_layout(config),
                    "app/page.jsx": FrontendTemplates.nextjs_page(config)
                }
                for file_path, content in files.items():
                    full_path = frontend_path / file_path
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content)
                    status["operations"].append(f"✅ Created: {frontend_name}/{file_path}")
            
            else:  # Plain HTML/CSS/JS
                frontend_path.mkdir(parents=True, exist_ok=True)
                files = {
                    "index.html": FrontendTemplates.plain_html(config),
                    "style.css": FrontendTemplates.plain_css(config),
                    "script.js": FrontendTemplates.plain_js(config)
                }
                
                for file_path, content in files.items():
                    (frontend_path / file_path).write_text(content)
                    status["operations"].append(f"✅ Created: {frontend_name}/{file_path}")
        
        except Exception as e:
            status["errors"].append(f"❌ Frontend error: {str(e)}")
        
        # Ensure frontend .gitignore exists
        try:
            (frontend_path / '.gitignore').write_text("node_modules\ndist\n.env\n")
            status["operations"].append(f"✅ Created: {frontend_name}/.gitignore")
        except Exception as _:
            pass
        
        return status
    
    def _create_readme(self, project_root: Path, config: Dict):
        """Generate README.md"""
        readme_content = f"""# {config['project_name']}

{config.get('description', 'A project generated with ProjectMaker')}

## Tech Stack

**Backend:** {config.get('backend_framework', 'N/A')}
**Frontend:** {config.get('frontend_framework', 'N/A')}

## Getting Started

### Backend Setup

```bash
cd {config.get('backend_folder_name', 'backend')}
pip install -r requirements.txt
python -m uvicorn app.main:app --reload  # For FastAPI
```

### Frontend Setup

```bash
cd {config.get('frontend_folder_name', 'frontend')}
npm install
npm run dev
```

## Project Structure

Generated with [ProjectMaker](https://github.com/SwagCode4U/projectmaker)

Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        (project_root / "README.md").write_text(readme_content)
    
    def _create_gitignore(self, project_root: Path, config: Dict):
        """Generate .gitignore"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env

# Node
node_modules/
dist/
build/
*.log

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite3
"""
        (project_root / ".gitignore").write_text(gitignore_content)
