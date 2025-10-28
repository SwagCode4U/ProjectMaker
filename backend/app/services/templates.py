# backend/app/services/templates.py
from typing import Dict


class BackendTemplates:
    """Templates for backend frameworks"""
    
    @staticmethod
    def fastapi_root_app(config: Dict) -> str:
        return '''"""
FastAPI root runner for convenience
"""
import uvicorn

if __name__ == "__main__":
    # Runs app defined in app/main.py
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
'''

    @staticmethod
    def fastapi_main(config: Dict) -> str:
        project_name = config.get("project_name", "ProjectMaker")
        return f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import project_routes

app = FastAPI(title="{project_name} API", version="1.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def _banner():
    print('Built with ❤ for the developer community by SwagCode4U')

@app.get("/")
def root():
    return '{{"message": "Welcome to ProjectMaker API 🚀"}}'

# Include project routes
app.include_router(project_routes.router)
'''

    @staticmethod
    def express_package_json(config: Dict) -> str:
        project_name = config.get("project_name", "express-boilerplate").lower().replace(" ", "-")
        return f'''{{
  "name": "{project_name}-backend",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {{
    "dev": "nodemon src/server.js",
    "start": "node src/server.js"
  }},
  "dependencies": {{
    "express": "^4.19.2",
    "cors": "^2.8.5",
    "dotenv": "^16.4.5"
  }},
  "devDependencies": {{
    "nodemon": "^3.0.0"
  }}
}}\n'''

    @staticmethod
    def express_app_js(config: Dict) -> str:
        return '''import express from 'express'
import cors from 'cors'
import routes from './routes/index.js'
import { errorHandler } from './middlewares/errorHandler.js'

const app = express()
app.use(cors())
app.use(express.json())
app.use('/api', routes)
app.use(errorHandler)

export default app
'''

    @staticmethod
    def express_server_js(config: Dict) -> str:
        return '''import dotenv from 'dotenv'
import app from './app.js'

dotenv.config()
const PORT = process.env.PORT || 5177

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`)
  console.log('Built with ❤ for the developer community by SwagCode4U')
})
'''

    @staticmethod
    def express_routes_index_js(config: Dict) -> str:
        return '''import { Router } from 'express'
import { home } from '../controllers/homeController.js'

const router = Router()
router.get('/', home)
export default router
'''

    @staticmethod
    def express_home_controller_js(config: Dict) -> str:
        return '''export const home = (req, res) => {
  res.json({ message: 'Welcome to Express Boilerplate!' })
}
'''

    @staticmethod
    def express_error_handler_js(config: Dict) -> str:
        return '''export const errorHandler = (err, req, res, next) => {
  console.error(err.stack)
  res.status(500).json({ error: 'Something went wrong!' })
}
'''

    @staticmethod
    def express_logger_js(config: Dict) -> str:
        return '''export const log = (msg) => console.log(`[LOG]: ${msg}`)
'''

    @staticmethod
    def express_env_example(config: Dict) -> str:
        return '''PORT=5177
'''

    @staticmethod
    def express_readme(config: Dict) -> str:
        return '''# 🚀 Express.js Boilerplate

A clean, modular Express.js setup with routes, controllers, middlewares, and environment configuration.

## 📦 Installation

```bash
npm install
```

## 🧠 Run the App
```bash
npm run dev
```

## ⚙️ Features
- ES Module support
- Organized folder structure
- Global error handling
- Example route and controller
- Environment configuration
'''
    
    @staticmethod
    def fastapi_database(config: Dict) -> str:
        return '''from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "sqlite:///./projectmaker.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
    
    @staticmethod
    def fastapi_models(config: Dict) -> str:
        return '''from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text)
    backend_framework = Column(String(50))
    frontend_framework = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
'''
    
    @staticmethod
    def fastapi_schemas(config: Dict) -> str:
        return '''from pydantic import BaseModel
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: str
    backend_framework: str
    frontend_framework: str

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
'''
    
    @staticmethod
    def fastapi_crud(config: Dict) -> str:
        return '''from sqlalchemy.orm import Session
from app import models, schemas


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session):
    return db.query(models.Project).all()
'''
    
    @staticmethod
    def fastapi_routes(config: Dict) -> str:
        return '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, database

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.post("/", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    return crud.create_project(db, project)

@router.get("/", response_model=list[schemas.ProjectResponse])
def list_projects(db: Session = Depends(database.get_db)):
    return crud.get_projects(db)
'''
    
    @staticmethod
    def fastapi_requirements() -> str:
        return '''fastapi==0.119.0
uvicorn[standard]==0.38.0
sqlalchemy==2.0.44
pydantic==2.12.3
sqlite-utils==3.36
python-dotenv==1.0.0
pymysql==1.1.0
'''
    
    @staticmethod
    def flask_app(config: Dict) -> str:
        project_name = config.get("project_name", "MyProject")
        return f'''"""
{project_name} - Flask Backend
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db
from routes import api_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return jsonify('{{"message": "Welcome to {project_name} API"}}')

@app.route('/health')
def health():
    return jsonify({{"status": "healthy"}})

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print('Built with ❤ for the developer community by SwagCode4U')
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    @staticmethod
    def flask_config(config: Dict) -> str:
        return '''"""
Flask configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
'''
    
    @staticmethod
    def flask_models(config: Dict) -> str:
        return '''"""
Flask-SQLAlchemy models
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Item(db.Model):
    """Example model"""
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
'''
    
    @staticmethod
    def flask_routes(config: Dict) -> str:
        return '''"""
Flask API routes
"""
from flask import Blueprint, request, jsonify
from models import db, Item

api_bp = Blueprint('api', __name__)


@api_bp.route('/items', methods=['GET'])
def get_items():
    """Get all items"""
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])


@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get item by ID"""
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())


@api_bp.route('/items', methods=['POST'])
def create_item():
    """Create new item"""
    data = request.get_json()
    item = Item(
        title=data['title'],
        description=data.get('description'),
        is_active=data.get('is_active', True)
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@api_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update item"""
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    
    item.title = data.get('title', item.title)
    item.description = data.get('description', item.description)
    item.is_active = data.get('is_active', item.is_active)
    
    db.session.commit()
    return jsonify(item.to_dict())


@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete item"""
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({{"message": "Item deleted"}})
'''
    
    @staticmethod
    def flask_requirements() -> str:
        return '''Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
python-dotenv==1.0.0
pymysql==1.1.0
'''
    
    @staticmethod
    def django_manage(config: Dict) -> str:
        return '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''
    
    @staticmethod
    def django_settings(config: Dict) -> str:
        project_name = config.get("project_name", "myproject")
        return f'''"""
Django settings for {project_name}
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True  # Update in production
'''
    
    @staticmethod
    def django_urls(config: Dict) -> str:
        return '''"""
URL configuration
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
'''
    
    @staticmethod
    def django_wsgi(config: Dict) -> str:
        return '''"""
WSGI config
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
'''
    
    @staticmethod
    def django_requirements() -> str:
        return '''Django==5.0
djangorestframework==3.14.0
django-cors-headers==4.3.1
python-dotenv==1.0.0
pymysql==1.1.0
'''
    
    @staticmethod
    def env_example(config: Dict) -> str:
        return '''# Database Configuration
DATABASE_URL=sqlite:///./app.db
# For MySQL: mysql+pymysql://user:password@localhost:3306/dbname
# For PostgreSQL: postgresql://user:password@localhost:5432/dbname

# Application Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
'''


class FrontendTemplates:
    """Templates for frontend frameworks"""
    
    # ---------------- Svelte (Vite) ----------------
    @staticmethod
    def svelte_package_json(config: Dict) -> str:
        return '''{
  "name": "project-maker-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "serve": "vite preview"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@sveltejs/vite-plugin-svelte": "^3.0.0",
    "svelte": "^4.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  },
  "dependencies": {}
}
'''

    @staticmethod
    def tailwind_config(config: Dict, framework: str = "react") -> str:
        content_glob = "./src/**/*.{js,jsx,ts,tsx,html}"
        return f'''/** @type {{import('tailwindcss').Config}} */
export default {{
  content: ["{content_glob}"],
  theme: {{ extend: {{}} }},
  plugins: [],
}}
'''

    @staticmethod
    def svelte_vite_config(config: Dict) -> str:
        return '''import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  server: { open: true }
});
'''

    @staticmethod
    def svelte_index_html(config: Dict) -> str:
        return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ProjectMaker</title>
  <link rel="stylesheet" href="/src/app.css" />
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
  <!-- Built with ❤ for the developer community by SwagCode4U -->
</body>
</html>
'''

    @staticmethod
    def svelte_main_js(config: Dict) -> str:
        return '''import App from './App.svelte';

const app = new App({ target: document.getElementById('app') });
export default app;
'''

    @staticmethod
    def svelte_app(config: Dict) -> str:
        return '''<script>
  import { onMount } from 'svelte';
  import Home from './routes/Home.svelte';
  let currentPage = 'home';
  onMount(() => { /* Initial setup code */ });
</script>

<main>
  {#if currentPage === 'home'}
    <Home />
  {/if}
</main>

<style>
  /* Add global styles here */
</style>

<!-- Built with ❤ for the developer community by SwagCode4U -->
'''

    @staticmethod
    def svelte_app_css(config: Dict) -> str:
        return '''/* Global styles for your application */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f9f9f9;
}
/* Built with ❤ for the developer community by SwagCode4U */
'''

    @staticmethod
    def svelte_lib_api_js(config: Dict) -> str:
        return '''// API utility functions for your application
const BASE_URL = 'http://localhost:3000/api';
export async function fetchData(endpoint) {
  const response = await fetch(`${BASE_URL}/${endpoint}`);
  if (!response.ok) throw new Error('Network response was not ok');
  return await response.json();
}
// Built with ❤ for the developer community by SwagCode4U
'''

    @staticmethod
    def svelte_lib_utils_js(config: Dict) -> str:
        return '''// Utility functions for common tasks
export function formatDate(date) {
  return new Date(date).toLocaleDateString();
}
// Built with ❤ for the developer community by SwagCode4U
'''

    @staticmethod
    def svelte_home(config: Dict) -> str:
        return '''<script>
  // Home component script section
</script>

<h1>Welcome to ProjectMaker!</h1>
<p>Your journey begins here.</p>

<style>
  h1 { color: #333; }
</style>

<!-- Built with ❤ for the developer community by SwagCode4U -->
'''

    @staticmethod
    def svelte_explorer(config: Dict) -> str:
        return '''<script>
  // Explorer component script section
</script>

<h1>Explorer</h1>
<p>Explore your projects.</p>

<style>
  h1 { color: #333; }
</style>

<!-- Built with ❤ for the developer community by SwagCode4U -->
'''

    @staticmethod
    def svelte_create_file(config: Dict) -> str:
        return '''<script>
  // CreateFile component script section
</script>

<h1>Create a New File</h1>
<p>Fill in the details to create a new file.</p>

<style>
  h1 { color: #333; }
</style>

<!-- Built with ❤ for the developer community by SwagCode4U -->
'''

    @staticmethod
    def svelte_db_designer(config: Dict) -> str:
        return '''<script>
  // DBDesigner component script section
</script>

<h1>Database Designer</h1>
<p>Design your database schema here.</p>

<style>
  h1 { color: #333; }
</style>

<!-- Built with ❤ for the developer community by SwagCode4U -->
'''

    # ---------------- Next.js ----------------
    @staticmethod
    def nextjs_package_json(config: Dict) -> str:
        project_name = config.get("project_name", "my-app").lower().replace(" ", "-")
        return f'''{{
  "name": "{project_name}-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {{
    "dev": "next dev -p 3010",
    "build": "next build",
    "start": "next start -p 3010"
  }},
  "dependencies": {{
    "next": "latest",
    "react": "^18",
    "react-dom": "^18"
  }}
}}\n'''

    @staticmethod
    def nextjs_layout(config: Dict) -> str:
        project_name = config.get("project_name", "My App")
        return f'''export const metadata = {{
  title: '{project_name}',
  description: '{config.get('description', 'Generated by ProjectMaker')}'
}}

export default function RootLayout({{ children }}) {{
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: 'system-ui, sans-serif' }}>{{children}}</body>
    </html>
  )
}}
'''

    @staticmethod
    def nextjs_page(config: Dict) -> str:
        return '''"use client";
import { useEffect, useState } from 'react'

export default function Page() {
  const [message, setMessage] = useState('Loading...')
  useEffect(() => {
    fetch('http://localhost:8000/')
      .then(r => r.json())
      .then(d => setMessage(d.message || 'Connected'))
      .catch(() => setMessage('Backend not reachable'))
  }, [])
  return (
    <main style={{ padding: 32 }}>
      <h1>Welcome</h1>
      <p>Backend says: {message}</p>
    </main>
  )
}
'''

    @staticmethod
    def nextjs_config(config: Dict) -> str:
        return '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}
export default nextConfig
'''

    @staticmethod
    def react_package_json(config: Dict) -> str:
        project_name = config.get("project_name", "my-app").lower().replace(" ", "-")
        return f'''{{
  "name": "{project_name}",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite --port 3010",
    "build": "vite build",
    "preview": "vite preview --port 3010"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0",
    "@emotion/react": "^11.11.3",
    "@emotion/styled": "^11.11.0",
    "framer-motion": "^11.0.0",
    "lenis": "^1.0.29",
    "react-router-dom": "^6.26.0"
  }},
  "devDependencies": {{
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0"
  }}
}}
'''
    
    @staticmethod
    def react_index_html(config: Dict) -> str:
        project_name = config.get("project_name", "My App")
        return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_name}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
'''
    
    @staticmethod
    def react_app(config: Dict) -> str:
        project_name = config.get("project_name", "My App")
        description = config.get("description", "Built with React")
        template = '''import { useState, useEffect } from 'react'
import { ThemeProvider } from '@emotion/react'
import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import Footer from './components/Footer.jsx'
import useLenis from './hooks/useLenis.js'
import theme from './styles/theme.js'
import './index.css'

function App() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)
  useLenis()

  useEffect(() => {
    // Example API call - update with your backend URL
    fetch('http://localhost:8000/')
      .then(res => res.json())
      .then(data => {
        setMessage(data.message)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error:', err)
        setLoading(false)
      })
  }, [])

  return (
    <ThemeProvider theme={theme}>
      <Navbar />
      <main className="container">
        <Hero title="__PROJECT_NAME__" subtitle="__DESCRIPTION__" />
        <div className="card">
          {loading ? <p>Loading...</p> : <p>Backend says: {message || 'No connection'}</p>}
        </div>
      </main>
      <Footer />
    </ThemeProvider>
  )
}

export default App
'''
        return template.replace('__PROJECT_NAME__', project_name).replace('__DESCRIPTION__', description)
    
    @staticmethod
    def react_main(config: Dict) -> str:
        return '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
'''
    
    @staticmethod
    def react_css(config: Dict) -> str:
        return '''@tailwind base;
@tailwind components;
@tailwind utilities;

/* Base styles */
* { box-sizing: border-box; }
body { @apply min-h-screen bg-gradient-to-br from-indigo-400 to-purple-600 antialiased; }
.container { @apply max-w-3xl mx-auto p-8 bg-white rounded-xl shadow-2xl my-10; }
.card { @apply bg-gray-50 p-6 rounded-lg my-8; }
'''
    
    @staticmethod
    def react_navbar(config: Dict) -> str:
        return '''/** @jsxImportSource @emotion/react */
import styled from '@emotion/styled'

const Bar = styled.nav`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: white;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
`

export default function Navbar() {
  return (
    <Bar>
      <span style={{ fontWeight: 700, color: '#2563eb' }}>ReactBoiler</span>
      <div style={{ display: 'flex', gap: 16 }}>
        <a href="#features">Features</a>
        <a href="#docs">Docs</a>
        <a href="#about">About</a>
      </div>
    </Bar>
  )
}
'''

    @staticmethod
    def react_hero(config: Dict) -> str:
        return '''import { motion } from 'framer-motion'

export default function Hero({ title, subtitle }) {
  return (
    <section style={{ padding: '4rem 0' }}>
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        style={{ fontSize: '3rem', marginBottom: '1rem', background: 'linear-gradient(135deg,#667eea,#764ba2)', WebkitBackgroundClip: 'text', color: 'transparent' }}
      >
        {title}
      </motion.h1>
      <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} style={{ color: '#555', fontSize: '1.1rem' }}>
        {subtitle}
      </motion.p>
    </section>
  )
}
'''

    @staticmethod
    def react_use_lenis(config: Dict) -> str:
        return '''import { useEffect } from 'react'
import Lenis from 'lenis'

export default function useLenis() {
  useEffect(() => {
    const lenis = new Lenis({ smoothWheel: true })
    let raf;
    const loop = (time) => { lenis.raf(time); raf = requestAnimationFrame(loop) }
    raf = requestAnimationFrame(loop)
    return () => cancelAnimationFrame(raf)
  }, [])
}
'''

    @staticmethod
    def react_theme(config: Dict) -> str:
        return '''const theme = {
  colors: {
    primary: '#667eea',
    secondary: '#764ba2',
    text: '#111827',
    muted: '#6b7280'
  }
}
export default theme
'''

    @staticmethod
    def react_footer(config: Dict) -> str:
        return '''export default function Footer() {
  return (
    <footer style={{ textAlign: 'center', padding: '1rem', color: '#6b7280' }}>
      Built with ❤️ for the developer community by SwagCode4U.
    </footer>
  )
}
'''

    @staticmethod
    def react_readme(config: Dict) -> str:
        return '''# ⚛️ React Boilerplate

A modern React + Vite starter including:
- Emotion (CSS-in-JS)
- Framer Motion (animations)
- Lenis (smooth scrolling)
- Tailwind CSS (v3.3.x)

## Getting Started
```bash
npm install
npm run dev
```

## Tech
- React 18
- Vite 5
- Tailwind 3.3
- @emotion/react, @emotion/styled
- framer-motion
- lenis

## Structure
```
src/
  components/
    Hero.jsx
    Navbar.jsx
  hooks/
    useLenis.js
  styles/
    theme.js
  App.jsx
  main.jsx
  index.css
```

---
Built with ❤️ for the developer community by SwagCode4U.
'''

    @staticmethod
    def vue_package_json(config: Dict) -> str:
        project_name = config.get("project_name", "my-app").lower().replace(" ", "-")
        return f'''{{
  "name": "{project_name}",
  "version": "1.0.0",
  "private": true,
  "scripts": {{
    "dev": "vite --port 3010",
    "build": "vite build",
    "preview": "vite preview --port 3010"
  }},
  "dependencies": {{
    "vue": "^3.3.0",
    "axios": "^1.6.0"
  }},
  "devDependencies": {{
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.0"
  }}
}}
'''
    
    @staticmethod
    def vue_index_html(config: Dict) -> str:
        project_name = config.get("project_name", "My App")
        return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
'''
    
    @staticmethod
    def vue_app(config: Dict) -> str:
        project_name = config.get("project_name", "My App")
        description = config.get("description", "Built with Vue")
        return f'''<template>
  <div class="container">
    <h1>{project_name}</h1>
    <p class="description">{description}</p>
    
    <div class="card">
      <p v-if="loading">Loading...</p>
      <p v-else>Backend says: {{{{ message || 'No connection' }}}}</p>
    </div>
    
    <div class="info">
      <p>Edit <code>src/App.vue</code> to get started</p>
    </div>

    <footer style="text-align:center;color:#6b7280;margin-top:2rem;">
      Built with ❤️‍ for developers by SwagCode4U.
    </footer>
  </div>
</template>

<script>
export default {{
  name: 'App',
  data() {{
    return {{
      message: '',
      loading: true
    }}
  }},
  mounted() {{
    fetch('http://localhost:8000/')
      .then(res => res.json())
      .then(data => {{
        this.message = data.message
        this.loading = false
      }})
      .catch(err => {{
        console.error('Error:', err)
        this.loading = false
      }})
  }}
}}
</script>

<style scoped>
/* Add your styles here */
</style>
'''
    
    @staticmethod
    def vue_main(config: Dict) -> str:
        return '''import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
'''
    
    @staticmethod
    def angular_package_json(config: Dict) -> str:
        project_name = config.get("project_name", "my-app").lower().replace(" ", "-")
        return f'''{{
  "name": "{project_name}",
  "version": "1.0.0",
  "scripts": {{
    "ng": "ng",
    "start": "ng serve",
    "build": "ng build",
    "watch": "ng build --watch --configuration development"
  }},
  "private": true,
  "dependencies": {{
    "@angular/animations": "^17.0.0",
    "@angular/common": "^17.0.0",
    "@angular/compiler": "^17.0.0",
    "@angular/core": "^17.0.0",
    "@angular/forms": "^17.0.0",
    "@angular/platform-browser": "^17.0.0",
    "@angular/platform-browser-dynamic": "^17.0.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.14.2"
  }},
  "devDependencies": {{
    "@angular-devkit/build-angular": "^17.0.0",
    "@angular/cli": "^17.0.0",
    "@angular/compiler-cli": "^17.0.0",
    "typescript": "~5.2.2"
  }}
}}
'''
    
    @staticmethod
    def angular_json(config: Dict) -> str:
        project_name = config.get("project_name", "my-app").lower().replace(" ", "-")
        return f'''{{
  "version": 1,
  "projects": {{
    "{project_name}": {{
      "projectType": "application",
      "root": "",
      "sourceRoot": "src",
      "architect": {{
        "build": {{
          "builder": "@angular-devkit/build-angular:browser",
          "options": {{
            "outputPath": "dist",
            "index": "src/index.html",
            "main": "src/main.ts",
            "tsConfig": "tsconfig.json"
          }}
        }},
        "serve": {{
          "builder": "@angular-devkit/build-angular:dev-server",
          "options": {{
            "port": 4200
          }}
        }}
      }}
    }}
  }}
}}
'''
    
    @staticmethod
    def angular_index_html(config: Dict) -> str:
        project_name = config.get("project_name", "My App")
        return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{project_name}</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <app-root></app-root>
</body>
</html>
'''
    
    @staticmethod
    def angular_main(config: Dict) -> str:
        return '''import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));
'''

    @staticmethod
    def angular_app_module(config: Dict) -> str:
        return '''import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { HomeComponent } from './pages/home/home.component';
import { AboutComponent } from './pages/about/about.component';

@NgModule({
  declarations: [AppComponent, HeaderComponent, FooterComponent, HomeComponent, AboutComponent],
  imports: [BrowserModule, AppRoutingModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
'''

    @staticmethod
    def angular_app_routing_module(config: Dict) -> str:
        return '''import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { AboutComponent } from './pages/about/about.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'about', component: AboutComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
'''

    @staticmethod
    def angular_component(config: Dict) -> str:
        project_name = config.get("project_name", "My App")
        return f'''import {{ Component }} from '@angular/core';

@Component({{
  selector: 'app-root',
  template: `
    <div class="container">
      <h1>{project_name}</h1>
      <p>Welcome to Angular!</p>
    </div>
  `,
  styles: []
}})
export class AppComponent {{
  title = '{project_name}';
}}
'''

    @staticmethod
    def angular_header_component_ts(config: Dict) -> str:
        return '''import { Component } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html'
})
export class HeaderComponent {}
'''

    @staticmethod
    def angular_header_component_html(config: Dict) -> str:
        return '''<header class="p-4 shadow bg-white">
  <div class="max-w-5xl mx-auto flex items-center justify-between">
    <a class="font-semibold text-blue-600" href="#">NgBoiler</a>
    <nav class="space-x-4 text-gray-600">
      <a href="#features">Features</a>
      <a href="#docs">Docs</a>
      <a href="#about">About</a>
    </nav>
  </div>
</header>
'''

    @staticmethod
    def angular_footer_component_ts(config: Dict) -> str:
        return '''import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html'
})
export class FooterComponent {}
'''

    @staticmethod
    def angular_footer_component_html(config: Dict) -> str:
        return '''<footer class="text-center p-4 text-gray-500">
  Built with ❤️ for the developer community by SwagCode4U.
</footer>
'''

    @staticmethod
    def angular_home_component_ts(config: Dict) -> str:
        return '''import { Component } from '@angular/core';

@Component({ selector: 'app-home', templateUrl: './home.component.html' })
export class HomeComponent {}
'''

    @staticmethod
    def angular_home_component_html(config: Dict) -> str:
        return '''<section class="text-center">
  <h1 class="text-4xl font-bold text-blue-600">⚡ Angular Boilerplate</h1>
  <p class="mt-2 text-gray-600">Start building scalable apps instantly.</p>
</section>
'''

    @staticmethod
    def angular_about_component_ts(config: Dict) -> str:
        return '''import { Component } from '@angular/core';

@Component({ selector: 'app-about', templateUrl: './about.component.html' })
export class AboutComponent {}
'''

    @staticmethod
    def angular_about_component_html(config: Dict) -> str:
        return '''<section class="text-center">
  <h1 class="text-3xl font-semibold text-purple-600">About</h1>
  <p class="mt-2 text-gray-600">This is a starter Angular app scaffolded by ProjectMaker.</p>
</section>
'''

    @staticmethod
    def plain_html(config: Dict) -> str:
        project_name = config.get("project_name", "My App")
        description = config.get("description", "A simple web application")
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>{project_name}</h1>
        <p class="description">{description}</p>
        
        <div class="card">
            <p id="status">Loading...</p>
        </div>
        
        <div class="info">
            <p>Edit <code>index.html</code>, <code>style.css</code>, and <code>script.js</code> to customize</p>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>
'''
    
    @staticmethod
    def plain_css(config: Dict) -> str:
        return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.container {
    max-width: 800px;
    padding: 2rem;
    text-align: center;
    background: white;
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #667eea;
}

.description {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 2rem;
}

.card {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
    margin: 2rem 0;
}

.info {
    margin-top: 2rem;
    font-size: 0.9rem;
    color: #666;
}

code {
    background: #f1f3f5;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
}
'''
    
    @staticmethod
    def plain_js(config: Dict) -> str:
        return '''// Check backend connection
fetch('http://localhost:8000/')
    .then(res => res.json())
    .then(data => {
        document.getElementById('status').textContent = 'Backend says: ' + (data.message || 'Connected!');
    })
    .catch(err => {
        document.getElementById('status').textContent = 'Backend not connected';
        console.error('Error:', err);
    });
'''
