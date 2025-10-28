# backend/app/routes/generator_routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import io
from app.services.project_generator import ProjectGenerator
from app.services.templates import BackendTemplates, FrontendTemplates
from app.services.pdf_generator import PDFGenerator
from app.services.script_generator import ScriptGenerator

router = APIRouter(prefix="/api/projects", tags=["Generator"])

# Pydantic models
class ProjectConfig(BaseModel):
    project_name: str
    description: str
    backend_framework: Optional[str] = None
    frontend_framework: Optional[str] = None
    backend_folder_name: str = "backend"
    frontend_folder_name: str = "frontend"
    custom_folders: List[str] = ["docs", "tests"]
    custom_files: List[dict] = []  # [{"name": "script.sh", "content": "..."}, ...]
    initialize_git: bool = True
    git_repo_url: Optional[str] = None
    target_directory: Optional[str] = None
    
    # Library selections
    libraries: List[str] = []  # tailwind, emotion, framer-motion, lenis, etc.
    
    # Database configuration
    database_type: Optional[str] = None  # mysql, postgresql, mongodb, sqlite
    database_name: Optional[str] = None
    database_user: Optional[str] = None
    database_password: Optional[str] = None
    database_tables: Optional[List[str]] = None
    use_alembic: bool = False
    auto_generate_tables: bool = False


@router.post("/preview")
def preview_project(config: ProjectConfig):
    """
    Generate a preview of the project structure without creating files
    Returns the project tree and requirements.txt content
    """
    try:
        from app.services.frameworks.registry import preview_backend_tree, preview_frontend_tree
        cfg = config.dict()
        be_tree = preview_backend_tree(cfg)
        fe_tree = preview_frontend_tree(cfg)
        # Debug: log what we received
        print(f"[preview] backend={config.backend_framework} -> has_tree={bool(be_tree)} | frontend={config.frontend_framework} -> has_tree={bool(fe_tree)}")

        tree = {
            "name": config.project_name,
            "type": "directory",
            "children": [x for x in [be_tree, fe_tree] if x]
        }
        
        # Get dependencies preview (requirements.txt or package.json)
        requirements = ""
        try:
            if config.backend_framework:
                fw = config.backend_framework.lower()
                if fw == "fastapi":
                    requirements = BackendTemplates.fastapi_requirements()
                elif fw == "flask":
                    requirements = BackendTemplates.flask_requirements()
                elif fw == "django":
                    requirements = BackendTemplates.django_requirements()
                elif fw in ["express", "nestjs"]:
                    requirements = BackendTemplates.express_package_json(config)
                elif fw in ["nextjs_api", "nextjs-api", "nextjsapi"]:
                    # Minimal Next.js API package.json preview (backend port 5177)
                    requirements = '{\n  "name": "nextjs-api-backend",\n  "private": true,\n  "version": "1.0.0",\n  "scripts": { "dev": "next dev -p 5177", "build": "next build", "start": "next start -p 5177" },\n  "dependencies": { "next": "latest", "react": "^18", "react-dom": "^18" }\n}\n'
                elif fw in ["bun", "bunjs", "bun.js"]:
                    # Bun.js boilerplate package.json preview
                    requirements = '{\n  "name": "bun-boilerplate",\n  "version": "1.0.0",\n  "private": true,\n  "scripts": {\n    "dev": "bun run start",\n    "start": "bun run build && node build/server.js",\n    "build": "bun build src -o build"\n  },\n  "dependencies": {\n    "express": "^4.17.1",\n    "dotenv": "^10.0.0"\n  },\n  "devDependencies": {\n    "typescript": "^4.5.0",\n    "ts-node": "^10.0.0",\n    "@types/express": "^4.17.13",\n    "@types/node": "^16.11.7"\n  }\n}\n'
                elif fw in ["springboot", "spring-boot", "spring"]:
                    # Spring Boot build.gradle preview
                    requirements = 'plugins {\\n  id \'org.springframework.boot\' version \'3.1.0\'\\n  id \'io.spring.dependency-management\' version \'1.0.12.RELEASE\'\\n  id \'java\'\\n}\\n\\nrepositories { mavenCentral() }\\n' 
                elif fw in ["koa", "koa.js", "koajs"]:
                    # Koa package.json preview
                    requirements = '{\n  "name": "koa-boilerplate",\n  "version": "1.0.0",\n  "private": true,\n  "scripts": { "start": "node src/server.js", "dev": "nodemon src/server.js" },\n  "dependencies": { "koa": "^2.13.4", "koa-router": "^10.0.0", "koa-bodyparser": "^4.4.0", "dotenv": "^10.0.0", "ws": "^8.0.0", "@koa/cors": "^5.0.0" },\n  "devDependencies": { "nodemon": "^2.0.12" }\n}\n'
            elif config.frontend_framework:
                ff = config.frontend_framework.lower()
                if ff == "react":
                    requirements = FrontendTemplates.react_package_json(config)
                elif ff == "nextjs":
                    requirements = FrontendTemplates.nextjs_package_json(config)
                elif ff == "vue":
                    # Minimal Vue + Vite package.json preview
                    requirements = '{\n  "name": "vue-app",\n  "private": true,\n  "version": "1.0.0",\n  "scripts": { "dev": "vite --port 3010", "build": "vite build", "preview": "vite preview" },\n  "dependencies": { "vue": "^3.4.0" },\n  "devDependencies": { "vite": "^5.0.0", "@vitejs/plugin-vue": "^5.0.0", "typescript": "^5.3.0" }\n}\n'
                elif ff == "svelte":
                    requirements = '{\n  "name": "svelte-app",\n  "private": true,\n  "version": "1.0.0",\n  "scripts": { "dev": "vite --port 3010", "build": "vite build", "preview": "vite preview" },\n  "dependencies": { "@motionone/svelte": "^10.16.4" },\n  "devDependencies": { "vite": "^5.0.0" }\n}\n'
                elif ff == "angular":
                    requirements = '{\n  "name": "angular-boilerplate",\n  "private": true,\n  "version": "1.0.0"\n}\n'
                elif ff in ["nuxt", "nuxtjs"]:
                    requirements = '{\n  "name": "nuxt-app",\n  "private": true,\n  "version": "1.0.0",\n  "scripts": { "dev": "nuxt dev -p 3010", "build": "nuxt build", "preview": "nuxt preview" },\n  "dependencies": { "nuxt": "^3.13.0" }\n}\n'
                elif ff == "solidjs":
                    requirements = '{\n  "name": "solidjs-boilerplate",\n  "private": true,\n  "version": "1.0.0",\n  "scripts": { "dev": "vite --port 3010", "build": "vite build", "preview": "vite preview" },\n  "dependencies": { "solid-js": "^1.9.0" }\n}\n'
        except Exception as e:
            print(f"[preview] requirements error: {e}")
            requirements = requirements or ''
        
        return {
            "tree": tree,
            "requirements": requirements,
            "config": config.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/build")
def build_project(config: ProjectConfig):
    """
    Actually build the project - create all files and folders
    Returns the status of all operations
    """
    try:
        generator = ProjectGenerator()
        
        # Build the project
        result = generator.build_project(
            config.dict(),
            target_directory=config.target_directory
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail={"message": "Build failed", "errors": result["errors"]}
            )
        
        return {
            "success": True,
            "project_path": result["project_path"],
            "operations": result["operations"],
            "errors": result.get("errors", [])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/frameworks")
def list_frameworks():
    """
    Get list of supported frameworks and libraries
    """
    return {
        "backend": [
            {"id": "fastapi", "name": "FastAPI", "description": "Modern, fast web framework", "icon": "fastapi"},
            {"id": "flask", "name": "Flask", "description": "Lightweight WSGI framework", "icon": "flask"},
            {"id": "django", "name": "Django", "description": "High-level web framework", "icon": "django"},
            {"id": "express", "name": "Express.js", "description": "Fast Node.js web framework", "icon": "express"},
            {"id": "nestjs", "name": "NestJS", "description": "Progressive Node.js framework", "icon": "nestjs"},
            {"id": "springboot", "name": "Spring Boot", "description": "Production-ready Java framework", "icon": "springboot"},
            {"id": "koa", "name": "Koa.js", "description": "Minimalist Node.js framework", "icon": "koa"},
            {"id": "bun", "name": "Bun.js", "description": "Fast all-in-one JavaScript runtime", "icon": "bun"},
            {"id": "nextjs_api", "name": "Next.js API", "description": "API backend using Next.js (App Router)", "icon": "nextdotjs"}
        ],
        "frontend": [
            {"id": "react", "name": "React", "description": "UI library by Facebook", "icon": "react"},
            {"id": "nextjs", "name": "Next.js", "description": "React framework with SSR", "icon": "nextdotjs"},
            {"id": "vue", "name": "Vue", "description": "Progressive framework", "icon": "vuedotjs"},
            {"id": "nuxt", "name": "Nuxt", "description": "Vue framework with SSR", "icon": "nuxtdotjs"},
            {"id": "angular", "name": "Angular", "description": "Platform by Google", "icon": "angular"},
            {"id": "svelte", "name": "Svelte", "description": "Cybernetically enhanced apps", "icon": "svelte"},
            {"id": "solid", "name": "SolidJS", "description": "Simple and performant", "icon": "solid"},
            {"id": "html", "name": "HTML/CSS/JS", "description": "Plain web technologies", "icon": "html5"}
        ],
        "libraries": [
            {"id": "tailwind", "name": "Tailwind CSS", "description": "Utility-first CSS framework", "version": "3.3.0"},
            {"id": "emotion", "name": "Emotion", "description": "CSS-in-JS library", "version": "11.11.0"},
            {"id": "styled-components", "name": "Styled Components", "description": "CSS-in-JS", "version": "6.1.0"},
            {"id": "framer-motion", "name": "Framer Motion", "description": "Animation library", "version": "11.0.0"},
            {"id": "lenis", "name": "Lenis", "description": "Smooth scroll", "version": "1.1.0"},
            {"id": "gsap", "name": "GSAP", "description": "Animation platform", "version": "3.12.0"},
            {"id": "three", "name": "Three.js", "description": "3D library", "version": "0.160.0"},
            {"id": "axios", "name": "Axios", "description": "HTTP client", "version": "1.6.0"},
            {"id": "react-query", "name": "React Query", "description": "Data fetching", "version": "5.0.0"},
            {"id": "zustand", "name": "Zustand", "description": "State management", "version": "4.4.0"},
            {"id": "redux", "name": "Redux Toolkit", "description": "State management", "version": "2.0.0"}
        ],
        "databases": [
            {"id": "mysql", "name": "MySQL", "description": "Relational database"},
            {"id": "postgresql", "name": "PostgreSQL", "description": "Advanced relational DB"},
            {"id": "mongodb", "name": "MongoDB", "description": "NoSQL document database"},
            {"id": "sqlite", "name": "SQLite", "description": "Lightweight file-based DB"}
        ]
    }


@router.post("/generate-db-script")
def generate_db_script(config: ProjectConfig):
    """Generate DB setup text bundle (script, rationale, examples)"""
    try:
        bundle = ScriptGenerator.generate_db_text_bundle(config.dict())
        return bundle
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class ColumnDef(BaseModel):
    name: str
    type: str
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    default: Optional[str] = None
    nullable: Optional[bool] = True
    auto_increment: Optional[bool] = False
    unique: Optional[bool] = False
    index: Optional[bool] = False
    values: Optional[List[str]] = None

class SchemaDesign(BaseModel):
    database_type: str
    database_name: str
    table_name: str
    columns: List[ColumnDef]


@router.post("/generate-schema")
def generate_schema(payload: SchemaDesign):
    try:
        bundle = ScriptGenerator.generate_table_schema_text_bundle(payload.dict())
        return bundle
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-pdf")
def generate_pdf(config: ProjectConfig):
    """Generate downloadable PDF with project summary"""
    try:
        from app.services.pdf_generator import PDFGenerator
        generator = ProjectGenerator()
        tree = generator.generate_project_tree(config.dict())
        requirements = ""
        if config.backend_framework:
            if config.backend_framework.lower() == "fastapi":
                requirements = BackendTemplates.fastapi_requirements()
            elif config.backend_framework.lower() == "flask":
                requirements = BackendTemplates.flask_requirements()
        
        pdf_bytes = PDFGenerator.generate_summary_pdf(config.dict(), tree, requirements)
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={config.project_name}_summary.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

