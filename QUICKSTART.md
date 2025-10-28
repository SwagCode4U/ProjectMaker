# ProjectMaker - Quick Start Guide - SwagCode4U❤️‍🔥

## 🎉 Complete System Ready!

Your interactive project scaffolding wizard is now fully built with:
- ✅ React + Framer Motion + Emotion + Lenis frontend
- ✅ FastAPI backend with project generation
- ✅ All 4 wizard steps implemented
- ✅ Real-time preview and build feedback
- ✅ Support for FastAPI, Flask, Django, React, Vue, Angular

## 🚀 Run the Application

### CORS Configuration (clone-and-run)
By default, the backend allows common local dev origins:
- http://localhost:3000
- http://localhost:3010
- http://localhost:5173
- http://127.0.0.1:3000
- http://127.0.0.1:3010
- http://127.0.0.1:5173

Override by setting FRONTEND_ORIGINS in a .env file at repo root:

```
FRONTEND_ORIGINS=http://your-app.local:8081,https://your-domain.com
```

If FRONTEND_ORIGINS is set to an empty string, the backend allows any localhost port via regex (credentials disabled in this mode).

### Terminal 1: Start Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Backend runs on: **http://localhost:8000**

API Docs: **http://localhost:8000/docs**

### Terminal 2: Start Frontend

```bash
cd frontend
npm install    # First time only
npm run dev
```

Frontend runs on: **http://localhost:3000**

## 📋 Usage Flow

1. **Landing Page** - Beautiful animated hero with features
2. **Click "Start Building"** - Opens wizard
3. **Step 1: Project Info**
   - Enter project name and description
   - Select backend framework (FastAPI, Flask, Django)
   - Select frontend framework (React, Vue, Angular, HTML)
4. **Step 2: Customization**
   - Choose target OS (Linux, Mac, Windows)
   - Set target directory
   - Customize folder names
   - Add custom folders
   - Toggle Git initialization
5. **Step 3: Preview**
   - See expandable project tree
   - Preview requirements.txt / package.json
   - View file/folder counts
6. **Step 4: Build**
   - Click "Build Project Now"
   - Watch real-time progress
   - See success message with project path
   - Options to open folder or create new project

## 🎨 Features

## Logging Configuration

## Security Headers
Lightweight security headers are applied to all responses:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Content-Security-Policy: default-src 'self' data: blob:

These are safe defaults for APIs and local dev. Adjust CSP if you serve HTML assets from other origins.

## Rate Limiting (optional)
Global per-client rate limiting can be enabled if slowapi is installed.
- Enable/disable via .env: RATE_LIMIT_ENABLED=true|false
- Default limit via RATE_LIMIT_DEFAULT (e.g., 120/minute)

Limits apply per client IP to all endpoints via middleware. 429 status is returned when exceeded.

This application uses structured logging (Loguru) to help with debugging and monitoring.

- Logs are written to the logs directory inside /backend/logs.
- linux- ls -la /your_dir/projectMaker/backend/logs 2>/dev/null | tail -n +1
- A new file is created daily and retained for 7 days.
- Log level is INFO by default; request/response lines are emitted for each HTTP call.

View logs during development to troubleshoot issues, or tail the latest file in logs/.

### Frontend
- **Smooth Scrolling**: Lenis for buttery smooth page scroll
- **Animations**: Framer Motion for fluid UI transitions
- **Styling**: Emotion CSS-in-JS with gradient themes
- **Icons**: React Icons for beautiful UI elements
- **Responsive**: Works on all screen sizes

### Backend
- **Project Generation**: Complete file/folder creation
- **Template System**: Framework-specific starter code
- **Preview API**: Non-destructive tree preview
- **Build API**: Actual project creation
- **CORS Enabled**: Frontend can call backend seamlessly

### Project Generation
Supports these combinations:
- FastAPI + React
- Flask + Vue
- Django + Angular
- Any backend + Any frontend
- Backend only or Frontend only

Generates:
- Complete folder structure
- Starter code files
- requirements.txt / package.json
- README.md with setup instructions
- .gitignore
- .env.example
- Optional Git initialization

## 🔧 API Endpoints

### GET /
Health check and welcome message

### GET /health
Service health status

### GET /api/projects/frameworks
List all supported frameworks

### POST /api/projects/preview
Preview project structure (no files created)

**Request Body:**
```json
{
  "project_name": "My App",
  "description": "Description here",
  "backend_framework": "fastapi",
  "frontend_framework": "react",
  "backend_folder_name": "backend",
  "frontend_folder_name": "frontend",
  "custom_folders": ["docs", "tests"],
  "initialize_git": true,
  "target_directory": "/path/to/project"
}
```

**Response:**
```json
{
  "tree": { /* project structure */ },
  "requirements": "fastapi==0.119.0\n...",
  "config": { /* your config */ }
}
```

### POST /api/projects/build
Build actual project (creates files)

**Request Body:** Same as /preview

**Response:**
```json
{
  "success": true,
  "project_path": "/path/to/generated/project",
  "operations": [
    "✅ Created project root",
    "✅ Created backend/",
    "✅ Created frontend/",
    ...
  ],
  "errors": []
}
```

## 🎯 Example: Create a FastAPI + React App

1. Open http://localhost:3000
2. Click "Start Building"
3. Fill in:
   - Name: "TaskManager"
   - Description: "A task management app"
   - Backend: FastAPI
   - Frontend: React
4. Customize:
   - Target: `/home/john/projects/taskmanager`
   - Add folder: "migrations"
5. Preview structure
6. Click "Build Project Now"
7. Done! Project created at specified location

## 📁 Generated Project Structure

Example for FastAPI + React:

```
taskmanager/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── api_routes.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── index.html
├── docs/
├── tests/
├── README.md
└── .gitignore
```

## 🔥 What Makes This Special

1. **No Manual Setup** - Dev never creates folders/files manually
2. **Interactive Preview** - See structure before building
3. **Real-time Feedback** - Watch project being built
4. **Smart Defaults** - Sensible folder names and structure
5. **Customizable** - Change anything before building
6. **Cross-Platform** - Works on Linux, Mac, Windows
7. **Framework Agnostic** - Mix any backend with any frontend
8. **Production Ready** - Generated code follows best practices

## 🎨 UI Highlights

- **Dark Theme** with purple/pink gradients
- **Glass Morphism** effects
- **Smooth Animations** on all interactions
- **Progress Tracking** with visual indicators
- **Status Badges** for success/error feedback
- **Expandable Tree View** for project preview
- **Responsive Design** for all devices

## 🛠️ Tech Stack

### Frontend
- React 18.3.1
- Framer Motion 11.5.4
- Emotion 11.13.3
- Lenis 1.1.9
- Vite 5.4.3
- Axios 1.7.7
- React Icons 5.3.0

### Backend
- FastAPI 0.119.0
- SQLAlchemy 2.0.44
- Pydantic 2.12.3
- Uvicorn 0.38.0

## 🎁 Bonus Features

- Framework-specific starter code
- CRUD operations pre-built
- Database models included
- Environment variable templates
- Comprehensive README generation
- Git-ready projects

## 🚀 Next Steps

1. Run both servers
2. Visit http://localhost:3000
3. Create your first project
4. Optionally: Add PDF generation
5. Optionally: Add code snippet preview
6. Optionally: Add npm install automation

## 💡 Tips

- Project names become folder names (slugified)
- Empty fields show helpful hints
- Preview is non-destructive (no files created)
- Build creates actual files on disk
- Generated projects are immediately usable
- Check backend logs for detailed info

## 🎉 You're Ready!

Everything is built and ready to use. Just start both servers and enjoy your interactive project generator!
