# backend/app/services/pdf_generator.py
from fpdf import FPDF
from typing import Dict
from datetime import datetime

class PDFGenerator:
    @staticmethod
    def generate_summary_pdf(config: Dict, tree: Dict, requirements: str) -> bytes:
        def _ascii(s) -> str:
            try:
                return str(s).encode('latin-1', 'replace').decode('latin-1')
            except Exception:
                return str(s)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Header banner (Material Blue) — full width, fixed height
        pdf.set_fill_color(33, 150, 243)
        pdf.rect(0, 0, pdf.w, 20, 'F')
        pdf.set_xy(10, 5)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, _ascii("ProjectMaker Report"), ln=True)

        # Reset for body
        pdf.set_text_color(0, 0, 0)
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, txt=_ascii(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), ln=True)
        pdf.ln(4)

        # Sections helper: colored header + divider
        def section_header(title: str):
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), pdf.w - 10, pdf.get_y())
            pdf.ln(4)
            pdf.set_text_color(0, 102, 204)
            pdf.set_font("Arial", 'B', 14)
            pdf.set_fill_color(245, 245, 245)
            pdf.cell(0, 8, txt=_ascii(title), ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)

        # Config section
        section_header("Configuration")
        pdf.set_font("Arial", size=11)
        for key, value in config.items():
            # Skip the plain description here; it is rendered in a dedicated section at the end
            if str(key).lower() == 'description':
                continue
            pdf.multi_cell(0, 6, txt=_ascii(f"- {key}: {value}"))
        pdf.ln(2)

        # Tree section
        section_header("Project Structure")
        pdf.set_font("Arial", size=11)
        for line in PDFGenerator._format_tree_lines(tree):
            pdf.cell(0, 6, txt=_ascii(line), ln=True)
        pdf.ln(2)

        # Database section
        db_info = PDFGenerator._extract_database_info(config)
        if db_info:
            section_header("Database Configuration")
            pdf.set_font("Arial", size=11)
            for line in db_info:
                pdf.cell(0, 6, txt=_ascii(line), ln=True)
            pdf.ln(2)

        # Requirements
        if requirements:
            section_header("Dependencies")
            pdf.set_font("Arial", size=11)
            for line in requirements.split('\n'):
                if line.strip():
                    pdf.cell(0, 6, txt=_ascii(f"- {line}"), ln=True)
            pdf.ln(2)

        # Ports & Scripts table
        table = PDFGenerator._ports_scripts(config)
        if table:
            try:
                section_header("Ports & Scripts")
                pdf.set_font("Arial", 'B', 11)
                pdf.set_fill_color(240,240,240)
                pdf.cell(60, 8, _ascii("Component"), 1, 0, 'L', True)
                pdf.cell(80, 8, _ascii("Dev Command"), 1, 0, 'L', True)
                pdf.cell(40, 8, _ascii("Port"), 1, 1, 'L', True)
                pdf.set_font("Courier", size=10)
                for row in table:
                    comp, cmd, port = row
                    pdf.cell(60, 7, _ascii(comp), 1)
                    pdf.cell(80, 7, _ascii(cmd), 1)
                    pdf.cell(40, 7, _ascii(port), 1, 1)
                pdf.ln(2)
            except Exception:
                # Gracefully skip table rendering if any issue arises
                pass

        # Next Steps
        steps = PDFGenerator._next_steps(config)
        if steps:
            section_header("Next Steps")
            for line in steps:
                # Use Courier for command-like lines
                stripped = line.strip().lower()
                if stripped.startswith(("cd ", "npm ", "bun ", "uvicorn ", "python ", "./gradlew", "java -jar", "git ")):
                    pdf.set_font("Courier", size=11)
                elif stripped.startswith("(optional) initialize git"):
                    pdf.set_font("Arial", 'B', 11)
                elif stripped.startswith("your project is ready"):
                    pdf.set_font("Arial", 'I', 11)
                else:
                    pdf.set_font("Arial", size=11)
                pdf.multi_cell(0, 6, txt=_ascii(line))
            pdf.ln(2)

        # ---------------------------------------------------------------------
        # Feature: Append the user's Project Description at the very end
        # Beautiful header + long, wrapped body text
        # ---------------------------------------------------------------------
        desc = (config or {}).get('description')
        if desc:
            section_header("Project Description")
            # Use a more elegant font for the description body
            pdf.set_font("Times", 'I', 12)
            pdf.set_text_color(60, 60, 60)
            pdf.multi_cell(0, 6, txt=_ascii(str(desc)))
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)

        # Branding footer (centered, subtle)
        pdf.set_y(-25)
        pdf.set_font("Arial", 'I', 9)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 8, _ascii("Generated by ProjectMaker  |  (c) 2025 SwagCode4U"), 0, 0, 'C')
        pdf.set_text_color(0, 0, 0)

        # Output as bytes
        return pdf.output(dest='S').encode('latin-1', 'replace')

    @staticmethod
    def _format_tree_lines(node: Dict) -> list[str]:
        """Return a list of ASCII tree lines using |-- and `-- connectors.
        Uses only ASCII so it renders with built-in FPDF fonts.
        """
        lines: list[str] = []

        def format_name(n: Dict) -> str:
            name = str(n.get('name', ''))
            ntype = str(n.get('type', ''))
            # Add trailing slash for directories
            return name + ('/' if ntype == 'directory' else '')

        def walk_children(children: list, prefix: str = '') -> None:
            for idx, child in enumerate(children or []):
                last = idx == len(children) - 1
                connector = '`-- ' if last else '|-- '
                lines.append(f"{prefix}{connector}{format_name(child)}")
                walk_children(child.get('children', []), prefix + ('    ' if last else '|   '))

        # Start with root line, then recurse into its children
        lines.append(format_name(node))
        walk_children(list(node.get('children', []) or []), '')
        return lines

    @staticmethod
    def _extract_database_info(config: Dict) -> list[str]:
        """Extract database configuration details for PDF display."""
        db_lines = []
        
        db_type = config.get('database_type')
        if db_type:
            db_lines.append(f"- Database Type: {db_type.upper()}")
            
            db_name = config.get('database_name')
            if db_name:
                db_lines.append(f"- Database Name: {db_name}")
            
            db_user = config.get('database_user')
            if db_user:
                db_lines.append(f"- Database User: {db_user}")
            
            # Don't show password for security
            if config.get('database_password'):
                db_lines.append("- Database Password: [CONFIGURED]")
            
            db_tables = config.get('database_tables', [])
            if db_tables:
                db_lines.append(f"- Tables ({len(db_tables)}):")
                for table in db_tables:
                    db_lines.append(f"  * {table}")
            
            use_alembic = config.get('use_alembic')
            if use_alembic:
                db_lines.append("- Migration Tool: Alembic")
            
            auto_gen = config.get('auto_generate_tables')
            if auto_gen:
                db_lines.append("- Auto-generate Tables: Yes")
        
        return db_lines

    @staticmethod
    def _ports_scripts(config: Dict) -> list[tuple[str,str,str]]:
        be = (config.get('backend_framework') or '').lower()
        fe = (config.get('frontend_framework') or '').lower()
        rows: list[tuple[str,str,str]] = []
        # Backend
        be_install, be_start = PDFGenerator._backend_commands(be, config.get('backend_folder_name','backend'))
        if be_start:
            rows.append(("Backend", be_start, PDFGenerator._backend_port(be)))
        # Frontend
        fe_install, fe_start = PDFGenerator._frontend_commands(fe, config.get('frontend_folder_name','frontend'))
        if fe_start:
            rows.append(("Frontend", fe_start, PDFGenerator._frontend_port(fe)))
        return rows

    @staticmethod
    def _next_steps(config: Dict) -> list[str]:
        lines: list[str] = []
        proj_dir = str(config.get('target_directory') or f"./{config.get('project_name','project')}")
        be = (config.get('backend_framework') or '').lower()
        fe = (config.get('frontend_framework') or '').lower()
        backend_dir = config.get('backend_folder_name', 'backend')
        frontend_dir = config.get('frontend_folder_name', 'frontend')

        # Header
        lines.append(f"1) Navigate to your project directory:\n   cd {proj_dir}")

        # Backend install
        be_install, be_start = PDFGenerator._backend_commands(be, backend_dir)
        if be_install:
            lines.append(f"2) Install backend dependencies:\n   cd {backend_dir} && {be_install}")
        if be_start:
            lines.append(f"4) Start backend:\n   {be_start}")

        # Frontend install
        fe_install, fe_start = PDFGenerator._frontend_commands(fe, frontend_dir)
        if fe_install:
            lines.append(f"3) Install frontend dependencies:\n   cd ../{frontend_dir} && {fe_install}")
        if fe_start:
            lines.append(f"5) Start frontend:\n   {fe_start}")

        # Git (optional)
        if config.get('initialize_git'):
            repo = config.get('git_repo_url')
            git_lines = [
                "(Optional) Initialize Git:",
                "   git init",
                "   git add .",
                "   git commit -m 'Initial commit'",
            ]
            if repo:
                git_lines.append(f"   git remote add origin {repo}")
                git_lines.append("   git push -u origin main")
            lines.append("\n".join(git_lines))

        lines.append("Your project is ready for development!")
        return lines

    @staticmethod
    def _backend_commands(be: str, backend_dir: str) -> tuple[str, str]:
        be = be.strip()
        # install, start
        if be == 'fastapi':
            return ("pip install -r requirements.txt", "uvicorn app.main:app --reload --port 8000")
        if be == 'flask':
            return ("pip install -r requirements.txt", "python app.py")
        if be == 'django':
            return ("pip install -r requirements.txt", "python manage.py runserver")
        if be == 'express':
            return ("npm install", "npm run dev || node src/server.js")
        if be == 'nestjs':
            return ("npm install", "npm run start:dev")
        if be in ('nextjs', 'nextjs_api', 'nextjs-api', 'nextjsapi'):
            return ("npm install", "npm run dev")
        if be == 'bun':
            return ("bun install", "bun run dev")
        if be == 'springboot':
            return ("./gradlew build || ./mvnw package", "./gradlew bootRun || java -jar build/libs/*.jar")
        if be == 'koa':
            return ("npm install", "npm run dev")
        return ("", "")

    @staticmethod
    def _backend_port(be: str) -> str:
        ports = {
            'fastapi': '8000', 'flask': '5000', 'django': '8000',
            'express': '5177', 'nestjs': '3000', 'nextjs': '5177', 'nextjs_api': '5177', 'nextjs-api': '5177', 'nextjsapi': '5177',
            'bun': '3000', 'springboot': '8080', 'koa': '3000'
        }
        return ports.get(be, '')

    @staticmethod
    def _frontend_commands(fe: str, frontend_dir: str) -> tuple[str, str]:
        fe = fe.strip()
        if not fe:
            return ("", "")
        if fe in ('react', 'vue', 'svelte', 'nextjs'):
            return ("npm install", "npm run dev")
        if fe == 'angular':
            return ("npm install", "npm start || npm run dev")
        if fe == 'html':
            return ("", f"python -m http.server 3010  # or open {frontend_dir}/index.html in browser")
        return ("", "")

    @staticmethod
    def _frontend_port(fe: str) -> str:
        ports = {'react': '3010', 'vue': '3010', 'svelte': '3010', 'nextjs': '3010', 'angular': '4200', 'html': '3010'}
        return ports.get(fe, '')
