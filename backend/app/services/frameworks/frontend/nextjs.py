# backend/app/services/frameworks/frontend/nextjs.py
from pathlib import Path
from typing import Dict
from .. import templates_adapter as T

def normalize(v: str) -> str:
    return 'nextjs'

def meta() -> Dict:
    return { 'id': 'nextjs', 'port': 3010 }

def preview(config: Dict) -> Dict:
    name = config.get('frontend_folder_name', 'frontend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'app', 'type': 'directory', 'children': [
                { 'name': 'api', 'type': 'directory', 'children': [
                    { 'name': 'hello', 'type': 'directory', 'children': [ { 'name': 'route.ts', 'type': 'file' } ] }
                ]},
                { 'name': 'components', 'type': 'directory', 'children': [ { 'name': 'Navbar.tsx', 'type': 'file' } ] },
                { 'name': 'layout.tsx', 'type': 'file' },
                { 'name': 'page.tsx', 'type': 'file' },
                { 'name': 'globals.css', 'type': 'file' },
            ]},
            { 'name': 'public', 'type': 'directory', 'children': [ { 'name': 'favicon.ico', 'type': 'file' } ] },
            { 'name': '.env.example', 'type': 'file' },
            { 'name': 'next.config.mjs', 'type': 'file' },
            { 'name': 'postcss.config.mjs', 'type': 'file' },
            { 'name': 'tailwind.config.mjs', 'type': 'file' },
            { 'name': 'tsconfig.json', 'type': 'file' },
            { 'name': 'package.json', 'type': 'file' },
            { 'name': 'README.md', 'type': 'file' },
        ]
    }

def build(root: Path, config: Dict) -> Dict:
    frontend = config.get('frontend_folder_name', 'frontend')
    base = root / frontend
    ops, errs = [], []
    try:
        (base / 'app' / 'api' / 'hello').mkdir(parents=True, exist_ok=True)
        (base / 'app' / 'components').mkdir(parents=True, exist_ok=True)
        (base / 'public').mkdir(parents=True, exist_ok=True)
        # Files (hard-coded TS + Tailwind setup)
        files = {
            'package.json': '{\n  "name": "nextjs-boilerplate",\n  "version": "1.0.0",\n  "private": true,\n  "scripts": {\n    "dev": "next dev -p 3010",\n    "build": "next build",\n    "start": "next start",\n    "lint": "next lint"\n  },\n  "dependencies": {\n    "next": "latest",\n    "react": "^18",\n    "react-dom": "^18"\n  },\n  "devDependencies": {\n    "autoprefixer": "^10",\n    "postcss": "^8",\n    "tailwindcss": "^3",\n    "typescript": "^5"\n  }\n}\n',
            'next.config.mjs': '/** @type {import(\'next\').NextConfig} */\nconst nextConfig = { reactStrictMode: true, experimental: { appDir: true } }\nexport default nextConfig\n',
            'postcss.config.mjs': 'export default { plugins: { tailwindcss: {}, autoprefixer: {} } }\n',
            'tailwind.config.mjs': 'export default { content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"], theme: { extend: {} }, plugins: [] }\n',
            'tsconfig.json': '{\n  "compilerOptions": {\n    "target": "ES2020",\n    "lib": ["dom", "dom.iterable", "esnext"],\n    "allowJs": false,\n    "skipLibCheck": true,\n    "strict": true,\n    "forceConsistentCasingInFileNames": true,\n    "noEmit": true,\n    "esModuleInterop": true,\n    "module": "esnext",\n    "moduleResolution": "bundler",\n    "resolveJsonModule": true,\n    "isolatedModules": true,\n    "jsx": "preserve",\n    "incremental": true,\n    "plugins": [{ "name": "next" }]\n  },\n  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],\n  "exclude": ["node_modules"]\n}\n',
            '.env.example': 'NEXT_PUBLIC_API_URL=http://localhost:3010\n',
            'README.md': '# ⚡ Next.js Boilerplate\n\nA clean, modern boilerplate built with Next.js 14, TypeScript, and Tailwind CSS.\n',
            'app/layout.tsx': 'import "./globals.css";\nimport Navbar from "./components/Navbar";\nexport const metadata = { title: "Next.js Boilerplate", description: "A clean starter for modern Next.js apps" };\nexport default function RootLayout({ children }: { children: React.ReactNode }) {\n  return (<html lang="en"><body className="bg-gray-50 text-gray-900"><Navbar /><main className="max-w-4xl mx-auto p-6">{children}</main></body></html>);\n}\n',
            'app/page.tsx': 'export default function Home(){ return (<div className="text-center mt-10"><h1 className="text-4xl font-bold text-blue-600">🚀 Next.js Boilerplate</h1><p className="mt-4 text-lg text-gray-700">Start building your app instantly — powered by Next.js 14 + Tailwind CSS.</p></div>);}\n',
            'app/components/Navbar.tsx': 'import Link from "next/link";\nexport default function Navbar(){ return (<nav className="flex justify-between p-4 shadow bg-white"><Link href="/" className="font-semibold text-blue-600">NextBoiler</Link><div className="space-x-4"><Link href="/about">About</Link><Link href="/contact">Contact</Link></div></nav>); }\n',
            'app/api/hello/route.ts': 'import { NextResponse } from "next/server";\nexport async function GET(){ return NextResponse.json({ message: "Hello from Next.js API Route!" }); }\n',
            'app/globals.css': '@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\nbody{ font-family: "Inter", sans-serif; }\n',
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {frontend}/{rel}")
        # favicon
        (base / 'public' / 'favicon.ico').write_text('placeholder')
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'frontend_type': 'nextjs' }
