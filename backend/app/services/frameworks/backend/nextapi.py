# backend/app/services/frameworks/backend/nextapi.py
from pathlib import Path
from typing import Dict


def normalize(v: str) -> str:
    return 'nextjs'


def meta() -> Dict:
    return {'id': 'nextjs', 'port': 5177}


def preview(config: Dict) -> Dict:
    name = config.get('backend_folder_name', 'backend')
    return {
        'name': name,
        'type': 'directory',
        'children': [
            {
                'name': 'app',
                'type': 'directory',
                'children': [
                    {
                        'name': 'api',
                        'type': 'directory',
                        'children': [
                            {
                                'name': 'v1',
                                'type': 'directory',
                                'children': [
                                    {
                                        'name': 'users',
                                        'type': 'directory',
                                        'children': [
                                            {'name': 'route.ts', 'type': 'file'},
                                            {
                                                'name': '[id]',
                                                'type': 'directory',
                                                'children': [
                                                    {'name': 'route.ts', 'type': 'file'}
                                                ],
                                            },
                                        ],
                                    },
                                    {
                                        'name': 'auth',
                                        'type': 'directory',
                                        'children': [
                                            {
                                                'name': 'login',
                                                'type': 'directory',
                                                'children': [
                                                    {'name': 'route.ts', 'type': 'file'}
                                                ],
                                            },
                                            {
                                                'name': 'register',
                                                'type': 'directory',
                                                'children': [
                                                    {'name': 'route.ts', 'type': 'file'}
                                                ],
                                            },
                                        ],
                                    },
                                ],
                            }
                        ],
                    },
                    {
                        'name': 'middleware',
                        'type': 'directory',
                        'children': [{'name': 'auth.ts', 'type': 'file'}],
                    },
                    {
                        'name': 'lib',
                        'type': 'directory',
                        'children': [
                            {'name': 'db.ts', 'type': 'file'},
                            {'name': 'validators.ts', 'type': 'file'},
                        ],
                    },
                    {
                        'name': 'types',
                        'type': 'directory',
                        'children': [{'name': 'user.ts', 'type': 'file'}],
                    },
                    {
                        'name': 'utils',
                        'type': 'directory',
                        'children': [{'name': 'logger.ts', 'type': 'file'}],
                    },
                    {'name': 'globals.css', 'type': 'file'},
                ],
            },
            {'name': '.env.example', 'type': 'file'},
            {'name': 'next.config.mjs', 'type': 'file'},
            {'name': 'tsconfig.json', 'type': 'file'},
            {'name': 'package.json', 'type': 'file'},
            {'name': 'README.md', 'type': 'file'},
        ],
    }


def build(root: Path, config: Dict) -> Dict:
    backend = config.get('backend_folder_name', 'backend')
    base = root / backend
    ops, errs = [], []
    try:
        # create dirs
        (base / 'app' / 'api' / 'v1' / 'users' / '[id]').mkdir(parents=True, exist_ok=True)
        (base / 'app' / 'api' / 'v1' / 'auth' / 'login').mkdir(parents=True, exist_ok=True)
        (base / 'app' / 'api' / 'v1' / 'auth' / 'register').mkdir(parents=True, exist_ok=True)
        (base / 'app' / 'middleware').mkdir(parents=True, exist_ok=True)
        (base / 'app' / 'lib').mkdir(parents=True, exist_ok=True)
        (base / 'app' / 'types').mkdir(parents=True, exist_ok=True)
        (base / 'app' / 'utils').mkdir(parents=True, exist_ok=True)
        # files
        files = {
            'package.json': (
                '{\n'
                '  "name": "nextjs-backend",\n'
                '  "version": "1.0.0",\n'
                '  "private": true,\n'
                '  "scripts": { "dev": "next dev -p 5177", "build": "next build", "start": "next start", "lint": "next lint" },\n'
                '  "dependencies": { "next": "latest", "react": "^18", "react-dom": "^18", "jsonwebtoken": "^9.0.0", "bcrypt": "^5.0.0" },\n'
                '  "devDependencies": { "typescript": "^5", "eslint": "^8", "@typescript-eslint/eslint-plugin": "^5", "@typescript-eslint/parser": "^5" }\n'
                '}\n'
            ),
            'next.config.mjs': (
                '/** @type {import(\'next\').NextConfig} */\n'
                'const nextConfig = { reactStrictMode: true, experimental: { appDir: true } }\n'
                'export default nextConfig\n'
            ),
            'tsconfig.json': (
                '{ "compilerOptions": { "target": "ES2020", "lib": ["dom","dom.iterable","esnext"], "strict": true, "esModuleInterop": true, "module": "esnext", "moduleResolution": "bundler", "resolveJsonModule": true, "isolatedModules": true, "jsx": "preserve", "incremental": true }, "include": ["**/*.ts","**/*.tsx"], "exclude": ["node_modules"] }\n'
            ),
            '.env.example': 'DATABASE_URL=your_database_url\nJWT_SECRET=your_jwt_secret\n',
            'README.md': '# Next.js Backend\n\nA backend boilerplate built with **Next.js**, serving as an API for your frontend applications.\n',
            'app/globals.css': '/* Global styles can go here */\n',
            'app/api/v1/users/route.ts': (
                "import { NextResponse } from 'next/server';\n"
                "import { getUsers, createUser } from '../../../lib/db';\n"
                "export async function GET(){ const users = await getUsers(); return NextResponse.json(users); }\n"
                "export async function POST(request: Request){ const body = await request.json(); const newUser = await createUser(body); return NextResponse.json(newUser, { status: 201 }); }\n"
            ),
            'app/api/v1/users/[id]/route.ts': (
                "import { NextResponse } from 'next/server';\n"
                "import { getUserById, updateUser, deleteUser } from '../../../lib/db';\n"
                "export async function GET(request: Request, { params }: { params: { id: string } }){ const user = await getUserById(params.id); return NextResponse.json(user); }\n"
                "export async function PUT(request: Request, { params }: { params: { id: string } }){ const body = await request.json(); const updatedUser = await updateUser(params.id, body); return NextResponse.json(updatedUser); }\n"
                "export async function DELETE(request: Request, { params }: { params: { id: string } }){ await deleteUser(params.id); return NextResponse.json({ message: 'User deleted' }); }\n"
            ),
            'app/api/v1/auth/login/route.ts': (
                "import { NextResponse } from 'next/server';\n"
                "import { authenticateUser } from '../../../lib/db';\n"
                "export async function POST(request: Request){ const { username, password } = await request.json(); const user = await authenticateUser(username, password); if(!user){ return NextResponse.json({ message: 'Invalid credentials' }, { status: 401 }); } return NextResponse.json({ message: 'Login successful', user }); }\n"
            ),
            'app/api/v1/auth/register/route.ts': (
                "import { NextResponse } from 'next/server';\n"
                "export async function POST(request: Request){ const body = await request.json(); return NextResponse.json({ message: 'Registered', user: body }, { status: 201 }); }\n"
            ),
            'app/middleware/auth.ts': (
                "import { NextResponse } from 'next/server';\n"
                "export function middleware(request: Request){ const token = (request.headers as any).get?.('Authorization'); if(!token){ return NextResponse.redirect(new URL('/api/auth/login', (request as any).url)); } return NextResponse.next(); }\n"
            ),
            'app/lib/db.ts': (
                "// Mock database functions\n"
                "export async function getUsers(){ return [{ id: 1, name: 'John Doe' }, { id: 2, name: 'Jane Doe' }]; }\n"
                "export async function createUser(data:any){ return { id: 3, ...data }; }\n"
                "export async function getUserById(id:string){}\n"
                "export async function updateUser(id:string, data:any){}\n"
                "export async function deleteUser(id:string){}\n"
                "export async function authenticateUser(username:string, password:string){}\n"
            ),
            'app/lib/validators.ts': 'export function isEmail(v:string){ return /@/.test(v); }\n',
            'app/types/user.ts': 'export interface User { id: number; name: string; email: string }\n',
            'app/utils/logger.ts': 'export function log(message:string){ console.log(`[${new Date().toISOString()}] ${message}`); }\n',
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {backend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return {'operations': ops, 'errors': errs, 'backend_type': 'nextjs_api'}
