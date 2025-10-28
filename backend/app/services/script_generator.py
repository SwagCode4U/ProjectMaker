# backend/app/services/script_generator.py
from typing import Dict, List


class ScriptGenerator:
    """
    Generates installation and setup scripts for different platforms
    Includes complete commented boilerplate scripts
    """
    
    @staticmethod
    def generate_setup_scripts(config: Dict) -> Dict[str, str]:
        """
        Generate all setup scripts based on configuration
        Returns dict with script names and their contents
        """
        scripts = {}
        
        # Generate main setup script for Linux/Mac
        scripts['setup.sh'] = ScriptGenerator._generate_bash_setup(config)
        
        # Generate Windows batch script
        scripts['setup.bat'] = ScriptGenerator._generate_windows_setup(config)
        
        # Generate database setup script if needed
        if config.get('database_type'):
            scripts['db_setup.sh'] = ScriptGenerator._generate_db_setup(config)
            
        # Generate Alembic scripts if needed
        if config.get('use_alembic'):
            scripts['alembic_init.sh'] = ScriptGenerator._generate_alembic_setup(config)
            
        # Generate Docker files if requested
        scripts['Dockerfile'] = ScriptGenerator._generate_dockerfile(config)
        scripts['docker-compose.yml'] = ScriptGenerator._generate_docker_compose(config)
        
        # Generate README with all commands
        scripts['INSTALL_GUIDE.md'] = ScriptGenerator._generate_install_guide(config)
        
        return scripts
    
    @staticmethod
    def _generate_bash_setup(config: Dict) -> str:
        """Complete commented bash setup script"""
        backend = config.get('backend_framework', '')
        frontend = config.get('frontend_framework', '')
        libraries = config.get('libraries', [])
        git_repo = config.get('git_repo_url', '')
        
        script = f"""#!/bin/bash
# ============================================================================
# ProjectMaker - Automated Setup Script
# Project: {config.get('project_name')}
# Generated: {config.get('description')}
# ============================================================================

set -e  # Exit on any error

echo "🚀 Starting setup for {config.get('project_name')}..."

# Colors for output
GREEN='\\033[0.32m'
BLUE='\\033[0;34m'
RED='\\033[0;31m'
NC='\\033[0m' # No Color

# ============================================================================
# STEP 1: Git Repository Setup
# ============================================================================
"""
        
        if git_repo:
            script += f"""
echo "${{BLUE}}📦 Setting up Git repository...${{NC}}"
git init
git remote add origin {git_repo}
git add .
git commit -m "Initial commit from ProjectMaker"
# Uncomment to push:
# git push -u origin main
echo "${{GREEN}}✅ Git repository initialized${{NC}}"
"""
        else:
            script += """
echo "${BLUE}📦 Initializing Git...${{NC}}"
git init
echo "${GREEN}✅ Git initialized${{NC}}"
"""

        # Backend setup
        if backend:
            if backend in ['fastapi', 'flask', 'django']:
                script += f"""
# ============================================================================
# STEP 2: Backend Setup ({backend.upper()})
# ============================================================================
echo "${{BLUE}}🐍 Setting up Python backend...${{NC}}"
cd {config.get('backend_folder_name', 'backend')}

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

"""
                if str(backend).lower() == 'django':
                    script += """
# Apply Django migrations
echo "Applying Django migrations..."
python manage.py migrate || true
"""
                script += """
echo "${GREEN}✅ Backend setup complete!${NC}"
cd ..
"""
            elif backend in ['express', 'nestjs']:
                script += f"""
# ============================================================================
# STEP 2: Backend Setup ({backend.upper()})
# ============================================================================
echo "${{BLUE}}📦 Setting up Node.js backend...${{NC}}"
cd {config.get('backend_folder_name', 'backend')}

# Install dependencies
echo "Installing npm packages..."
npm install

echo "${{GREEN}}✅ Backend setup complete!${{NC}}"
cd ..
"""

        # Frontend setup
        if frontend:
            libs_cmd = ""
            if libraries:
                lib_packages = ScriptGenerator._get_npm_packages(libraries)
                if lib_packages:
                    libs_cmd = f"\necho \"Installing additional libraries...\"\nnpm install {' '.join(lib_packages)}\n"
            # Prefer legacy peer deps for Vue to avoid ESLint v9 peer conflicts
            fe_install_cmd = "npm install --legacy-peer-deps" if str(frontend).lower() == 'vue' else "npm install"
            
            script += f"""
# ============================================================================
# STEP 3: Frontend Setup ({frontend.upper()})
# ============================================================================
echo "${{BLUE}}🎨 Setting up frontend...${{NC}}"
cd {config.get('frontend_folder_name', 'frontend')}

# Install dependencies (using legacy peer deps for compatibility)
echo "Installing npm packages..."
{fe_install_cmd}
{libs_cmd}
echo "${{GREEN}}✅ Frontend setup complete!${{NC}}"
cd ..
"""

        # Database setup
        if config.get('database_type'):
            script += f"""
# ============================================================================
# STEP 4: Database Setup ({config.get('database_type').upper()})
# ============================================================================
echo "${{BLUE}}🗄️  Setting up database...${{NC}}"
# Run the database setup script
bash db_setup.sh
echo "${{GREEN}}✅ Database setup complete!${{NC}}"
"""

        # Final instructions
        script += f"""
# ============================================================================
# SETUP COMPLETE! 🎉
# ============================================================================
echo ""
echo "${{GREEN}}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${{NC}}"
echo "${{GREEN}}   ✨ Setup Complete for {config.get('project_name')}! ✨${{NC}}"
echo "${{GREEN}}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${{NC}}"
echo ""
echo "${{BLUE}}📝 Next Steps:${{NC}}"
echo ""
"""
        
        if backend and backend in ['fastapi', 'flask', 'django']:
            script += f"""echo "1. Start Backend:"
echo "   cd {config.get('backend_folder_name', 'backend')}"
echo "   source venv/bin/activate"
echo "   {'uvicorn app.main:app --reload' if backend == 'fastapi' else 'python app.py' if backend == 'flask' else 'python manage.py runserver'}"
echo ""
"""
        elif backend in ['express', 'nestjs']:
            script += f"""echo "1. Start Backend:"
echo "   cd {config.get('backend_folder_name', 'backend')}"
echo "   npm run dev"
echo ""
"""
        
        if frontend:
            script += f"""echo "2. Start Frontend:"
echo "   cd {config.get('frontend_folder_name', 'frontend')}"
echo "   npm run dev"
echo ""
"""
        
        script += """echo "🔗 Visit: http://localhost:3000 (frontend)"
echo "🔗 API: http://localhost:8000 (backend)"
echo ""
echo "${GREEN}Happy coding! 🚀${NC}"
"""
        
        return script
    
    @staticmethod
    def _generate_windows_setup(config: Dict) -> str:
        """Windows batch setup script"""
        backend = config.get('backend_framework', '')
        frontend = config.get('frontend_framework', '')
        
        script = f"""@echo off
REM ============================================================================
REM ProjectMaker - Windows Setup Script
REM Project: {config.get('project_name')}
REM ============================================================================

echo Starting setup for {config.get('project_name')}...

"""
        
        if backend in ['fastapi', 'flask', 'django']:
            script += f"""
echo Setting up Python backend...
cd {config.get('backend_folder_name', 'backend')}
python -m venv venv
call venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
"""
            if str(backend).lower() == 'django':
                script += """
REM Apply Django migrations
python manage.py migrate
"""
            script += """
cd ..
"""
        
        if frontend:
            script += f"""
echo Setting up frontend...
cd {config.get('frontend_folder_name', 'frontend')}
npm install
cd ..
"""
        
        script += """
echo.
echo Setup Complete!
echo.
pause
"""
        return script
    
    @staticmethod
    def generate_db_text_bundle(config: Dict) -> Dict[str, str]:
        """Return rationale, raw SQL/NoSQL script, Node example, and .env text for the selected DB"""
        db_type = (config.get('database_type') or '').lower()
        db_name = config.get('database_name') or (config.get('project_name', 'mydb').lower().replace(' ', '_'))
        user = config.get('database_user') or 'appuser'
        password = config.get('database_password') or 'password123'
        tables = config.get('database_tables') or []
        if isinstance(tables, str):
            tables = [t.strip() for t in tables.split(',') if t.strip()]
        tables = [t for t in tables if t]
        
        def sanitize_ident(s: str) -> str:
            import re
            return re.sub(r"[^a-zA-Z0-9_]+", "_", s.strip())
        
        db_name = sanitize_ident(db_name)
        user = sanitize_ident(user)
        tables = [sanitize_ident(t) for t in tables]
        
        bundle = { 'database': db_type, 'rationale': '', 'script': '', 'node_example': '', 'env': '', 'how_to_run': '' }
        
        if db_type == 'mysql':
            bundle['rationale'] = 'Best for structured relational data with transactions and wide hosting support.'
            script = f"""-- Create Database and User
CREATE DATABASE {db_name};
CREATE USER '{user}'@'localhost' IDENTIFIED BY '{password}';
GRANT ALL PRIVILEGES ON {db_name}.* TO '{user}'@'localhost';
FLUSH PRIVILEGES;

-- Use DB
USE {db_name};
"""
            # Basic tables
            for t in tables or ['users']:
                if t == 'users':
                    script += """
-- users
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(120) UNIQUE,
  password VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
                else:
                    script += f"""
-- {t}
CREATE TABLE IF NOT EXISTS {t} (
  id INT AUTO_INCREMENT PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
            bundle['script'] = script.strip()
            bundle['node_example'] = f"""// db.js
import mysql from 'mysql2/promise';
const db = await mysql.createConnection({{
  host: 'localhost',
  user: '{user}',
  password: '{password}',
  database: '{db_name}'
}});
console.log('✅ DB Connected!');
""".strip()
            bundle['env'] = f"""DB_TYPE=mysql
DB_NAME={db_name}
DB_USER={user}
DB_PASS={password}
DB_HOST=localhost
""".strip()
            bundle['how_to_run'] = "mysql -u root -p < script.sql"
        elif db_type == 'postgresql':
            bundle['rationale'] = 'Great for complex relational data, constraints, and JSON support.'
            script = f"""-- Create Database and User
CREATE DATABASE {db_name};
CREATE USER {user} WITH ENCRYPTED PASSWORD '{password}';
GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};

\\c {db_name}
"""
            for t in tables or ['users']:
                if t == 'users':
                    script += """
-- users
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(120) UNIQUE,
  password VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
                else:
                    script += f"""
-- {t}
CREATE TABLE IF NOT EXISTS {t} (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
            bundle['script'] = script.strip()
            bundle['node_example'] = f"""// db.js
import pkg from 'pg';
const {{ Client }} = pkg;
const client = new Client({{
  host: 'localhost',
  user: '{user}',
  password: '{password}',
  database: '{db_name}'
}});
await client.connect();
console.log('✅ DB Connected!');
""".strip()
            bundle['env'] = f"""DB_TYPE=postgresql
DB_NAME={db_name}
DB_USER={user}
DB_PASS={password}
DB_HOST=localhost
""".strip()
            bundle['how_to_run'] = "psql -U postgres -f script.sql"
        elif db_type == 'mongodb':
            bundle['rationale'] = 'Ideal for flexible schemas, rapid iteration, and document models.'
            script = f"""// mongosh script
use {db_name}

// Create user
// Run as admin
// db.createUser({{ user: '{user}', pwd: '{password}', roles: [{{ role: 'readWrite', db: '{db_name}' }}] }})

// Collections
"""
            for t in tables or ['users']:
                script += f"db.createCollection('{t}');\n"
            script += "\n// Indexes\ndb.users.createIndex({ email: 1 }, { unique: true });\n"
            bundle['script'] = script.strip()
            bundle['node_example'] = f"""// db.js
import {{ MongoClient }} from 'mongodb';
const client = new MongoClient('mongodb://localhost:27017');
await client.connect();
const db = client.db('{db_name}');
console.log('✅ DB Connected!');
""".strip()
            bundle['env'] = f"""DB_TYPE=mongodb
MONGO_URI=mongodb://localhost:27017/{db_name}
DB_NAME={db_name}
""".strip()
            bundle['how_to_run'] = "mongosh < script.js"
        else:
            raise ValueError("Unsupported or missing database_type. Choose mysql, postgresql, or mongodb.")
        
        return bundle

    @staticmethod
    def generate_table_schema_text_bundle(payload: Dict) -> Dict[str, str]:
        """Build full table/collection schema text with comments based on columns."""
        db_type = (payload.get('database_type') or '').lower()
        db_name = payload.get('database_name') or 'mydb'
        table = payload.get('table_name') or 'my_table'
        cols = payload.get('columns') or []

        def q(s: str) -> str:
            return s.replace("'", "''")

        # Ensure id column for SQL
        has_id = any((c.get('name') or '').lower() == 'id' for c in cols)
        lines = []

        def map_type_sql(c: Dict, engine: str) -> str:
            t = (c.get('type') or 'string').lower()
            length = c.get('length') or c.get('size')
            precision = c.get('precision') or (c.get('length') if t == 'decimal' else None)
            scale = c.get('scale') or (2 if t == 'decimal' else None)
            if engine == 'mysql':
                if t == 'string':
                    return f"VARCHAR({length or 255})"
                if t == 'text':
                    return "TEXT"
                if t == 'int':
                    return "INT"
                if t == 'decimal':
                    return f"DECIMAL({precision or 10},{scale or 2})"
                if t == 'boolean':
                    return "TINYINT(1)"
                if t == 'datetime':
                    return "TIMESTAMP"
                if t == 'enum':
                    vals = c.get('values') or []
                    vals_q = ','.join([f"'{q(v)}'" for v in vals]) or "'value'"
                    return f"ENUM({vals_q})"
                return "VARCHAR(255)"
            else:  # postgres
                if t == 'string':
                    return f"VARCHAR({length or 255})"
                if t == 'text':
                    return "TEXT"
                if t == 'int':
                    return "INTEGER"
                if t == 'decimal':
                    return f"NUMERIC({precision or 10},{scale or 2})"
                if t == 'boolean':
                    return "BOOLEAN"
                if t == 'datetime':
                    return "TIMESTAMP"
                if t == 'enum':
                    # emulate enum via CHECK
                    return f"VARCHAR({length or 50})"
                return "VARCHAR(255)"

        if db_type in ['mysql', 'postgresql']:
            engine = db_type
            header = f"-- DATABASE: {db_type.upper()}\n-- TABLE: {table}\n-- Generated by ProjectMaker Schema Designer\n\n"
            if engine == 'mysql':
                create = [f"CREATE TABLE {table} ("]
                if not has_id:
                    create.append("  id INT AUTO_INCREMENT PRIMARY KEY,")
                for i, c in enumerate(cols):
                    name = c.get('name', f'col_{i}')
                    typ = map_type_sql(c, engine)
                    parts = [f"  {name} {typ}"]
                    if c.get('auto_increment') and typ.startswith(('INT','DECIMAL')):
                        parts.append('AUTO_INCREMENT')
                    if c.get('unique'):
                        parts.append('UNIQUE')
                    if c.get('nullable') is False:
                        parts.append('NOT NULL')
                    if c.get('default') not in [None, '']:
                        parts.append(f"DEFAULT {c.get('default') if str(c.get('default')).upper().startswith(('CURRENT_', 'NOW()')) else "'"+q(str(c.get('default')))+"'"}")
                    line = ' '.join(parts) + ','
                    create.append(line)
                # trim last comma
                if create[-1].endswith(','):
                    create[-1] = create[-1][:-1]
                create.append(")\n;")
                lines.append('\n'.join(create))
            else:
                create = [f"CREATE TABLE {table} ("]
                if not has_id:
                    create.append("  id SERIAL PRIMARY KEY,")
                for i, c in enumerate(cols):
                    name = c.get('name', f'col_{i}')
                    typ = map_type_sql(c, engine)
                    parts = [f"  {name} {typ}"]
                    if c.get('unique'):
                        parts.append('UNIQUE')
                    if c.get('nullable') is False:
                        parts.append('NOT NULL')
                    if c.get('default') not in [None, '']:
                        parts.append(f"DEFAULT {c.get('default') if str(c.get('default')).upper().startswith(('CURRENT_', 'NOW()')) else "'"+q(str(c.get('default')))+"'"}")
                    line = ' '.join(parts) + ','
                    create.append(line)
                if create[-1].endswith(','):
                    create[-1] = create[-1][:-1]
                create.append(")\n;")
                # Postgres enum emulation via CHECK
                for c in cols:
                    if (c.get('type') or '').lower() == 'enum' and c.get('values'):
                        vals_q = ','.join([f"'{q(v)}'" for v in c['values']])
                        create.insert(-1, f"  CHECK ({c.get('name')} IN ({vals_q})),")
                lines.append('\n'.join(create))
            # Insert example
            sample_cols = [c.get('name') for c in cols if c.get('name')][:5]
            if sample_cols:
                placeholders = []
                for c in cols[:5]:
                    t = (c.get('type') or 'string').lower()
                    if t in ['int','decimal','boolean']:
                        placeholders.append('0')
                    elif t in ['datetime']:
                        placeholders.append('CURRENT_TIMESTAMP')
                    else:
                        placeholders.append("'example'")
                lines.append("\n-- Insert Example\n" + f"INSERT INTO {table} (" + ', '.join(sample_cols) + ")\nVALUES (" + ', '.join(placeholders) + ");")
            # Indexes
            idx_cols = [c.get('name') for c in cols if c.get('index')]
            if idx_cols:
                lines.append("\n-- Recommended Indexes")
                for n in idx_cols:
                    lines.append(f"CREATE INDEX idx_{table}_{n} ON {table}({n});")
            # Optional alter
            lines.append("\n-- Optional Alter\n-- ALTER TABLE {table} ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")
            script_text = header + '\n\n'.join(lines)
            return { 'script': script_text }
        elif db_type == 'mongodb':
            header = f"// DATABASE: MongoDB\n// COLLECTION: {table}\n// Generated by ProjectMaker Schema Designer\n\n"
            # JSON-like schema doc
            schema = { c.get('name','field'): (c.get('type') or 'string') for c in cols if c.get('name') }
            json_block = '{\n' + ',\n'.join([f"  \"{k}\": \"{v}\"" for k,v in schema.items()]) + '\n}'
            lines.append("// Create collection and indexes")
            lines.append(f"db.createCollection('{table}')")
            idx_cols = [c.get('name') for c in cols if c.get('index') or c.get('unique')]
            for n in idx_cols:
                unique = any(c.get('name') == n and c.get('unique') for c in cols)
                lines.append(f"db.{table}.createIndex({{{{{ {n}: 1 }}}}}{', { unique: true }' if unique else ''})")
            example_doc = '{ ' + ', '.join([f"{n}: 'example'" for n in schema.keys()]) + ' }'
            script_text = header + (
                "// Schema (informal)\n" + json_block +
                "\n\n// Insert Example\n" + f"db.{table}.insertOne({example_doc})\n" +
                "\n// Indexes\n" + '\n'.join(lines)
            )
            return { 'script': script_text }
        else:
            raise ValueError('Unsupported database_type')

    def _generate_db_setup(config: Dict) -> str:
        """Database setup script with auto table generation"""
        db_type = config.get('database_type', 'mysql')
        db_name = config.get('database_name', config.get('project_name', 'mydb').lower().replace(' ', '_'))
        description = config.get('description', '')
        
        script = f"""#!/bin/bash
# ============================================================================
# Database Setup Script - {db_type.upper()}
# ============================================================================
# This script creates database and tables for: {config.get('project_name')}
# Description: {description}
# ============================================================================

set -e

DB_NAME="{db_name}"
"""
        
        if db_type == 'mysql':
            script += """
echo "🗄️  Setting up MySQL database..."

# MySQL credentials (change as needed)
MYSQL_USER="${MYSQL_USER:-root}"
MYSQL_PASS="${MYSQL_PASS:-}"

# Create database
echo "Creating database $DB_NAME..."
mysql -u $MYSQL_USER -p$MYSQL_PASS -e "CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo "✅ Database created: $DB_NAME"

# Auto-generate tables based on description
echo "Setting up tables..."
mysql -u $MYSQL_USER -p$MYSQL_PASS $DB_NAME << 'EOF'

-- ============================================================================
-- AUTO-GENERATED TABLES
-- Based on project description and common patterns
-- ============================================================================

-- Users table (common in most apps)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Main data table (customize based on your needs)
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    user_id INT,
    status ENUM('active', 'inactive', 'pending') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sessions table (for authentication)
CREATE TABLE IF NOT EXISTS sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_token (token),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

EOF

echo "✅ Tables created successfully!"
echo ""
echo "📋 Database Summary:"
echo "   Database: $DB_NAME"
echo "   Tables: users, items, sessions"
echo ""
echo "🔧 Update your .env file with:"
echo "   DATABASE_URL=mysql://user:pass@localhost:3306/$DB_NAME"
"""
        
        elif db_type == 'postgresql':
            script += f"""
echo "🗄️  Setting up PostgreSQL database..."

# PostgreSQL credentials
PGUSER="${{PGUSER:-postgres}}"

# Create database
echo "Creating database $DB_NAME..."
psql -U $PGUSER -c "CREATE DATABASE $DB_NAME;"

echo "✅ Database created: $DB_NAME"

# Create tables
echo "Setting up tables..."
psql -U $PGUSER -d $DB_NAME << 'EOF'

-- ============================================================================
-- AUTO-GENERATED TABLES FOR POSTGRESQL
-- ============================================================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Items table
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_items_user_id ON items(user_id);
CREATE INDEX idx_items_status ON items(status);

-- Sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);

EOF

echo "✅ Tables created successfully!"
echo ""
echo "🔧 Update your .env file with:"
echo "   DATABASE_URL=postgresql://user:pass@localhost:5432/$DB_NAME"
"""
        
        elif db_type == 'mongodb':
            script += f"""
echo "🗄️  Setting up MongoDB database..."

# MongoDB connection
MONGO_URI="${{MONGO_URI:-mongodb://localhost:27017}}"

# Create database and collections
echo "Creating database and collections..."
mongosh --eval "
use $DB_NAME;

// Create collections
db.createCollection('users');
db.createCollection('items');
db.createCollection('sessions');

// Create indexes
db.users.createIndex({{ email: 1 }}, {{ unique: true }});
db.users.createIndex({{ username: 1 }}, {{ unique: true }});
db.items.createIndex({{ user_id: 1 }});
db.sessions.createIndex({{ token: 1 }}, {{ unique: true }});
db.sessions.createIndex({{ user_id: 1 }});

print('✅ Database and collections created!');
"

echo "✅ MongoDB setup complete!"
echo ""
echo "🔧 Update your .env file with:"
echo "   MONGO_URI=mongodb://localhost:27017/$DB_NAME"
"""
        
        return script
    
    @staticmethod
    def _generate_alembic_setup(config: Dict) -> str:
        """Alembic migration setup script"""
        return f"""#!/bin/bash
# ============================================================================
# Alembic Migration Setup
# ============================================================================

echo "🔄 Setting up Alembic for database migrations..."

cd {config.get('backend_folder_name', 'backend')}

# Initialize Alembic
alembic init alembic

echo "✅ Alembic initialized!"
echo ""
echo "📝 Next steps:"
echo "1. Configure alembic.ini with your database URL"
echo "2. Create your first migration:"
echo "   alembic revision --autogenerate -m 'Initial migration'"
echo "3. Apply migrations:"
echo "   alembic upgrade head"
"""
    
    @staticmethod
    def _generate_dockerfile(config: Dict) -> str:
        """Docker configuration"""
        backend = config.get('backend_framework', '')
        
        if backend in ['fastapi', 'flask', 'django']:
            return f"""# Dockerfile for {config.get('project_name')}
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        elif backend in ['express', 'nestjs']:
            return f"""# Dockerfile for {config.get('project_name')}
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application
COPY . .

# Build if needed
RUN npm run build || true

# Expose port
EXPOSE 3000

# Run application
CMD ["npm", "start"]
"""
        return ""
    
    @staticmethod
    def _generate_docker_compose(config: Dict) -> str:
        """Docker Compose configuration"""
        db_type = config.get('database_type', 'mysql')
        backend = config.get('backend_framework', '')
        
        compose = f"""version: '3.8'

services:
  backend:
    build: ./{config.get('backend_folder_name', 'backend')}
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${{DATABASE_URL}}
    depends_on:
      - db
"""
        
        if db_type == 'mysql':
            compose += """
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: mydb
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
"""
        elif db_type == 'postgresql':
            compose += """
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""
        elif db_type == 'mongodb':
            compose += """
  db:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
"""
        
        return compose
    
    @staticmethod
    def _generate_install_guide(config: Dict) -> str:
        """Complete installation guide with all commands"""
        backend = config.get('backend_framework', '')
        frontend = config.get('frontend_framework', '')
        db_type = config.get('database_type')
        git_repo = config.get('git_repo_url', '')
        
        guide = f"""# 🚀 Installation Guide - {config.get('project_name')}

> {config.get('description')}

## 📋 Prerequisites

"""
        
        if backend in ['fastapi', 'flask', 'django']:
            guide += "- Python 3.9+ installed\n"
        if backend in ['express', 'nestjs'] or frontend:
            guide += "- Node.js 18+ and npm installed\n"
        if db_type:
            guide += f"- {db_type.upper()} database installed\n"
        if git_repo:
            guide += f"- Git access to: {git_repo}\n"
        
        guide += f"""

## ⚡ Quick Start

### Option 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```batch
setup.bat
```

### Option 2: Manual Setup

"""
        
        if git_repo:
            guide += f"""#### 1. Clone Repository
```bash
git clone {git_repo}
cd {config.get('project_name', 'project').lower().replace(' ', '-')}
```

"""
        else:
            guide += """#### 1. Initialize Git
```bash
git init
```

"""
        
        if backend:
            if backend in ['fastapi', 'flask', 'django']:
                guide += f"""#### 2. Setup Backend
```bash
cd {config.get('backend_folder_name', 'backend')}

# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate
# OR Activate (Windows)
venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

"""
                if backend == 'django':
                    guide += """# Apply Django migrations
python manage.py migrate
# See pending migrations
python manage.py showmigrations

"""
                guide += """# Run migrations (if using Alembic)
# alembic upgrade head
```

"""
            else:
                guide += f"""#### 2. Setup Backend
```bash
cd {config.get('backend_folder_name', 'backend')}
npm install
```

"""
        
        if frontend:
            legacy = " --legacy-peer-deps" if str(frontend).lower() == 'vue' else ""
            guide += f"""#### 3. Setup Frontend
```bash
cd {config.get('frontend_folder_name', 'frontend')}
npm install{legacy}
```

If you see peer-deps conflicts (e.g., ESLint v9), use the legacy flag as above.

"""
        
        if db_type:
            guide += f"""#### 4. Setup Database
```bash
# Run database setup script
chmod +x db_setup.sh
./db_setup.sh

# Or manually create database
"""
            
            if db_type == 'mysql':
                guide += """mysql -u root -p
CREATE DATABASE mydb;
```

"""
            elif db_type == 'postgresql':
                guide += """psql -U postgres
CREATE DATABASE mydb;
```

"""
            elif db_type == 'mongodb':
                guide += """mongosh
use mydb
```

"""
        
        guide += """## 🎯 Running the Application

"""
        
        if backend:
            if backend == 'fastapi':
                guide += f"""### Start Backend
```bash
cd {config.get('backend_folder_name', 'backend')}
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```
Backend will run on: http://localhost:8000
API Docs: http://localhost:8000/docs

"""
            elif backend == 'flask':
                guide += f"""### Start Backend
```bash
cd {config.get('backend_folder_name', 'backend')}
source venv/bin/activate
python app.py
```
Backend will run on: http://localhost:5000

"""
            elif backend == 'django':
                guide += f"""### Start Backend
```bash
cd {config.get('backend_folder_name', 'backend')}
source venv/bin/activate
python manage.py runserver
```
Backend will run on: http://localhost:8000

"""
            elif backend in ['express', 'nestjs']:
                guide += f"""### Start Backend
```bash
cd {config.get('backend_folder_name', 'backend')}
npm run dev
```
Backend will run on: http://localhost:3000

"""
        
        if frontend:
            guide += f"""### Start Frontend
```bash
cd {config.get('frontend_folder_name', 'frontend')}
npm run dev
```
Frontend will run on: http://localhost:3000

"""
        
        guide += """## 📦 Project Structure

```
.
"""
        
        if backend:
            guide += f"""├── {config.get('backend_folder_name', 'backend')}/  # Backend application
"""
        if frontend:
            guide += f"""├── {config.get('frontend_folder_name', 'frontend')}/  # Frontend application
"""
        
        for folder in config.get('custom_folders', []):
            guide += f"""├── {folder}/
"""
        
        guide += """├── setup.sh           # Automated setup script
├── db_setup.sh        # Database setup script
└── README.md          # This file
```

## 🔧 Environment Variables

Create `.env` file in backend folder:

```env
"""
        
        if db_type == 'mysql':
            guide += """DATABASE_URL=mysql://user:password@localhost:3306/mydb
"""
        elif db_type == 'postgresql':
            guide += """DATABASE_URL=postgresql://user:password@localhost:5432/mydb
"""
        elif db_type == 'mongodb':
            guide += """MONGO_URI=mongodb://localhost:27017/mydb
"""
        
        guide += """SECRET_KEY=your-secret-key-here
DEBUG=True
```

## 🐳 Docker Setup (Optional)

```bash
docker-compose up -d
```

## 📝 Common Commands

"""
        
        if backend in ['fastapi', 'flask', 'django']:
            guide += f"""### Backend Commands
```bash
# Activate virtual environment
cd {config.get('backend_folder_name', 'backend')}
source venv/bin/activate

# Install new package
pip install package_name

# Update requirements
pip freeze > requirements.txt

# Run tests
pytest
```

"""
        
        if frontend:
            guide += f"""### Frontend Commands
```bash
cd {config.get('frontend_folder_name', 'frontend')}

# Install new package
npm install package_name

# Build for production
npm run build

# Run tests
npm test
```

"""
        
        if config.get('use_alembic'):
            guide += """### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

"""
        
        guide += f"""## 🚀 Deployment

See deployment guides in `/docs` folder.

## 📖 Documentation

- API Documentation: http://localhost:8000/docs (if FastAPI)
- Additional docs: `/docs` folder

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

MIT License

---

**Generated by ProjectMaker** 🎉
"""
        
        return guide
    
    @staticmethod
    def _get_npm_packages(libraries: List[str]) -> List[str]:
        """Convert library IDs to npm package names"""
        package_map = {
            'tailwind': 'tailwindcss postcss autoprefixer',
            'emotion': '@emotion/react @emotion/styled',
            'styled-components': 'styled-components',
            'framer-motion': 'framer-motion',
            'lenis': 'lenis',
            'gsap': 'gsap',
            'three': 'three',
            'axios': 'axios',
            'react-query': '@tanstack/react-query',
            'zustand': 'zustand',
            'redux': '@reduxjs/toolkit react-redux'
        }
        
        packages = []
        for lib in libraries:
            if lib in package_map:
                packages.append(package_map[lib])
        
        return ' '.join(packages).split() if packages else []
