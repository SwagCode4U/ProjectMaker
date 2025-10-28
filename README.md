<div align="center">

# 🚀 ProjectMaker

Build full‑stack apps in minutes — not hours.

[![Made with FastAPI](https://img.shields.io/badge/Backend-FastAPI-05998b?logo=fastapi&logoColor=white)](#)
[![Frontend-React](https://img.shields.io/badge/Frontend-React-61dafb?logo=react&logoColor=0d1117)](#)
[![PDF](https://img.shields.io/badge/PDF-fpdf2-30363d)](#)
[![License](https://img.shields.io/badge/License-MIT-2ea043)](#)

</div>

A modern open‑source scaffolding engine that generates complete backend + frontend boilerplates with a polished PDF summary. Designed for developers who value speed, structure, and simplicity.

---

## Table of Contents
- Features
- Supported Frameworks
- How It Works
- Developer API
- Installation (Clone & Run)
- Configuration (CORS, Rate Limiting, Logs)
- Architecture
- Contributing & Support

---

## ✨ Features
- Full‑stack generator with live preview and safe file creation
- Professional PDF summary (ASCII-only) with Ports & Scripts and Next Steps
- Per‑framework READMEs, .env.example hints, and .gitignore in subprojects
- Flexible CORS, optional rate limiting, structured JSON errors, Loguru logs
- Modular backend/frontend registry with aliasing and lazy loading

## 🧩 Supported Frameworks

| Category  | Frameworks |
|-----------|------------|
| Backend   | FastAPI • Express • NestJS • Next.js API • Bun.js • Koa • Spring Boot • Flask • Django |
| Frontend  | React • Vue • Svelte • Next.js • Angular • HTML/CSS |

> Special case: when both sides are Next.js (frontend + backend), a single full‑stack app can be generated.

## ⚙️ How It Works
1. Pick backend and frontend frameworks
2. Customize folders, libraries, or database options
3. Preview the tree and requirements
4. Build the project to disk
5. Download the PDF summary and start coding

## 🛠️ Developer API

| Endpoint                       | Description                         |
|--------------------------------|-------------------------------------|
| GET  `/version`               | Show version, git sha, build date   |
| POST `/api/projects/preview`  | Return live preview tree            |
| POST `/api/projects/build`    | Generate backend & frontend         |
| GET  `/api/projects/frameworks`| List frameworks and libraries       |
| GET  `/api/projects/generate-pdf` | Download polished PDF summary   |
| GET  `/api/fs/list`           | List files/folders (jailed)         |
| POST `/api/fs/create`         | Create file/folder (jailed)         |

## 📦 Installation (Clone & Run)

```bash
# 1) Clone
git clone https://github.com/SwagCode4U/projectmaker.git
cd projectmaker

# 2) Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 3) Frontend
cd ../frontend
npm install
npm run dev   # Vite (5173) or set to 3010 if preferred
```

Open the UI at: http://localhost:5173 (or 3010) and the API at: http://localhost:8000

### Configuration
- CORS: set `FRONTEND_ORIGINS` (.env at repo root) to a comma‑separated list of allowed origins
- Rate limiting (optional): `RATE_LIMIT_ENABLED=true|false`, `RATE_LIMIT_DEFAULT=120/minute`
- Logs: written to `logs/`, rotated daily, kept 7 days

## 🧱 Architecture (High Level)
```
projectmaker/
├─ backend/
│  ├─ app/
│  │  ├─ routes/         # APIs (preview, build, pdf, fs, frameworks)
│  │  ├─ services/
│  │  │  ├─ frameworks/  # per‑framework backends/frontends + registry
│  │  │  ├─ pdf_generator.py
│  │  │  └─ project_generator.py
│  │  └─ main.py         # FastAPI app, CORS, logging, errors, /version
│  └─ requirements.txt
└─ frontend/
   └─ src/               # React + Vite wizard (4 steps)
```

## 📄 PDF Summary (What you get)
- Colored header, section dividers, and branding footer
- Configuration, Project Structure (ASCII tree), Dependencies
- Ports & Scripts table (dev commands and ports)
- Next Steps (env copy hints, install/run, optional git remote)

## 🤝 Contributing & Support
- PRs welcome for new frameworks, fixes, and docs
- Open issues for bugs or ideas
- Contact: amit9000@tutanota.com

If you find this useful:
- ⭐ Star the repo
- 🍴 Fork and build something awesome
- 📣 Share with your dev friends

<div align="center">

Made with ❤️ by SwagCode4U

Generated with [ProjectMaker](https://github.com/SwagCode4U/projectmaker)

</div>



