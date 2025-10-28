# backend/app/services/frameworks/frontend/solidjs.py
from pathlib import Path
from typing import Dict

def normalize(v: str) -> str:
    return 'solidjs'

def meta() -> Dict:
    return { 'id': 'solidjs', 'port': 3010 }

def preview(config: Dict) -> Dict:
    name = config.get('frontend_folder_name', 'frontend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'public', 'type': 'directory', 'children': [ { 'name': 'favicon.ico', 'type': 'file' } ] },
            { 'name': 'src', 'type': 'directory', 'children': [
                { 'name': 'components', 'type': 'directory', 'children': [ { 'name': 'Header.tsx', 'type': 'file' } ] },
                { 'name': 'App.tsx', 'type': 'file' },
                { 'name': 'index.css', 'type': 'file' },
                { 'name': 'main.tsx', 'type': 'file' },
            ]},
            { 'name': '.env.example', 'type': 'file' },
            { 'name': 'index.html', 'type': 'file' },
            { 'name': 'package.json', 'type': 'file' },
            { 'name': 'postcss.config.cjs', 'type': 'file' },
            { 'name': 'tailwind.config.cjs', 'type': 'file' },
            { 'name': 'tsconfig.json', 'type': 'file' },
            { 'name': 'README.md', 'type': 'file' },
        ]
    }

def build(root: Path, config: Dict) -> Dict:
    frontend = config.get('frontend_folder_name', 'frontend')
    base = root / frontend
    ops, errs = [], []
    try:
        (base / 'public').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'components').mkdir(parents=True, exist_ok=True)
        files: Dict[str,str] = {
            'package.json': '{\n  "name": "solidjs-boilerplate",\n  "version": "1.0.0",\n  "private": true,\n  "scripts": {"dev": "vite --port 3010", "build": "vite build", "preview": "vite preview"},\n  "dependencies": { "solid-js": "^1.9.0" },\n  "devDependencies": { "typescript": "^5.3.3", "vite": "^5.0.0", "vite-plugin-solid": "^2.9.0", "tailwindcss": "^3.4.0", "postcss": "^8.4.30", "autoprefixer": "^10.4.16" }\n}\n',
            'index.html': '<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>SolidJS Boilerplate</title></head><body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>\n',
            'postcss.config.cjs': 'module.exports={plugins:{tailwindcss:{},autoprefixer:{}}}\n',
            'tailwind.config.cjs': 'module.exports={content:["./index.html","./src/**/*.{js,ts,jsx,tsx}"],theme:{extend:{}},plugins:[]}\n',
            'tsconfig.json': '{"compilerOptions":{"target":"esnext","module":"esnext","jsx":"preserve","strict":true,"moduleResolution":"bundler","esModuleInterop":true,"forceConsistentCasingInFileNames":true},"include":["src"]}\n',
            'src/index.css': '@tailwind base;\n@tailwind components;\n@tailwind utilities;\nbody{font-family:Inter,sans-serif;}\n',
            'src/components/Header.tsx': 'export default function Header(){return(<header class="w-full bg-white shadow p-4 text-center font-semibold text-gray-700">🚀 SolidJS App Starter</header>)}\n',
            'src/App.tsx': 'import { createSignal } from "solid-js";import Header from "./components/Header";export default function App(){const [count,setCount]=createSignal(0);return(<div class="min-h-screen bg-gray-50 text-gray-800 flex flex-col items-center justify-center"><Header /><h1 class="text-4xl font-bold text-blue-600 mt-4">⚡ SolidJS Boilerplate</h1><p class="mt-2 text-gray-600">Build ultra-fast web apps with Solid + Vite + Tailwind</p><button class="mt-6 bg-blue-500 text-white px-5 py-2 rounded-lg shadow hover:bg-blue-600 transition" onClick={()=>setCount(count()+1)}>Count: {count()}</button></div>)}\n',
            'src/main.tsx': '/* Entry Point */\nimport { render } from "solid-js/web";\nimport App from "./App";\nimport "./index.css";\nrender(()=> <App />, document.getElementById("root") as HTMLElement);\n',
            '.env.example': 'VITE_API_URL=http://localhost:3010\n',
            'README.md': '# ⚡ SolidJS Boilerplate\n\nA fast, minimal starter built with SolidJS, Vite, and Tailwind CSS.\n',
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {frontend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'frontend_type': 'solidjs' }
