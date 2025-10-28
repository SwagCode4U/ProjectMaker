# backend/app/services/frameworks/backend/bun.py
from pathlib import Path
from typing import Dict


def normalize(v: str) -> str:
    return 'bun'


def meta() -> Dict:
    # Common dev port for Bun/Express
    return {'id': 'bun', 'port': 5178}


def preview(config: Dict) -> Dict:
    name = config.get('backend_folder_name', 'backend')
    return {
        'name': name,
        'type': 'directory',
        'children': [
            {
                'name': 'src', 'type': 'directory', 'children': [
                    {'name': 'controllers', 'type': 'directory', 'children': [
                        {'name': 'auth.controller.ts', 'type': 'file'},
                        {'name': 'user.controller.ts', 'type': 'file'},
                    ]},
                    {'name': 'middlewares', 'type': 'directory', 'children': [
                        {'name': 'auth.middleware.ts', 'type': 'file'},
                    ]},
                    {'name': 'models', 'type': 'directory', 'children': [
                        {'name': 'user.model.ts', 'type': 'file'},
                    ]},
                    {'name': 'routes', 'type': 'directory', 'children': [
                        {'name': 'user.routes.ts', 'type': 'file'},
                    ]},
                    {'name': 'services', 'type': 'directory', 'children': [
                        {'name': 'auth.service.ts', 'type': 'file'},
                    ]},
                    {'name': 'utils', 'type': 'directory', 'children': [
                        {'name': 'logger.ts', 'type': 'file'},
                    ]},
                    {'name': 'app.ts', 'type': 'file'},
                    {'name': 'server.ts', 'type': 'file'},
                ]
            },
            {'name': '.env.example', 'type': 'file'},
            {'name': 'bun.lockb', 'type': 'file'},
            {'name': 'package.json', 'type': 'file'},
            {'name': 'tsconfig.json', 'type': 'file'},
            {'name': 'README.md', 'type': 'file'},
        ]
    }


def build(root: Path, config: Dict) -> Dict:
    backend = config.get('backend_folder_name', 'backend')
    base = root / backend
    ops, errs = [], []
    try:
        # Create directories
        for p in [
            base / 'src' / 'controllers',
            base / 'src' / 'middlewares',
            base / 'src' / 'models',
            base / 'src' / 'routes',
            base / 'src' / 'services',
            base / 'src' / 'utils',
        ]:
            p.mkdir(parents=True, exist_ok=True)
        # Files content
        files: Dict[str, str] = {
            'src/app.ts': """import express from 'express';
import userRoutes from './routes/user.routes';

const app = express();

// Middleware
app.use(express.json());

// Routes
app.use('/api/v1/users', userRoutes);

export default app;
""",
            'src/server.ts': """import app from './app';
import { config } from 'dotenv';

config(); // Load environment variables

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
""",
            'src/controllers/auth.controller.ts': """import { Request, Response } from 'express';
import { AuthService } from '../services/auth.service';

export class AuthController {
  async login(req: Request, res: Response) {
    const { username, password } = req.body;
    const user = await AuthService.login(username, password);
    if (user) {
      res.json(user);
    } else {
      res.status(401).json({ message: 'Invalid credentials' });
    }
  }
}
""",
            'src/controllers/user.controller.ts': """import { Request, Response } from 'express';
export class UserController {
  async me(req: Request, res: Response) {
    res.json({ id: 1, username: 'demo' });
  }
}
""",
            'src/middlewares/auth.middleware.ts': """import { Request, Response, NextFunction } from 'express';
export function authMiddleware(req: Request, res: Response, next: NextFunction){
  // TODO: verify token
  next();
}
""",
            'src/models/user.model.ts': """export interface User {
  id: number;
  username: string;
  password: string; // Consider hashing passwords
}
""",
            'src/routes/user.routes.ts': """import { Router } from 'express';
import { AuthController } from '../controllers/auth.controller';

const router = Router();
const authController = new AuthController();

router.post('/login', authController.login);

export default router;
""",
            'src/services/auth.service.ts': """import { User } from '../models/user.model';

export class AuthService {
  static async login(username: string, password: string): Promise<User | null> {
    // Implement user authentication logic
    return null; // Replace with actual logic
  }
}
""",
            'src/utils/logger.ts': """export function log(message: string) {
  console.log(`[${new Date().toISOString()}] ${message}`);
}
""",
            '.env.example': """PORT=3000
DATABASE_URL=your_database_url
JWT_SECRET=your_jwt_secret
""",
            'package.json': """{
  "name": "bun-boilerplate",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "bun run start",
    "start": "bun run build && node build/server.js",
    "build": "bun build src -o build"
  },
  "dependencies": {
    "express": "^4.17.1",
    "dotenv": "^10.0.0"
  },
  "devDependencies": {
    "typescript": "^4.5.0",
    "ts-node": "^10.0.0",
    "@types/express": "^4.17.13",
    "@types/node": "^16.11.7"
  }
}
""",
            'tsconfig.json': """{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "build"
  },
  "include": ["src/**/*"]
}
""",
'README.md': """# Bun.js Boilerplate

A boilerplate project for building applications using **Bun.js** and **Express**.

## Features
- Modular architecture (controllers, services, routes)
- Authentication scaffold
- Env config with dotenv
- TypeScript setup

## Setup
```bash
bun install
cp .env.example .env
bun run dev
```

## Build
```bash
bun run build
```

---

Generated with [ProjectMaker](https://github.com/SwagCode4U/projectmaker)
""",
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {backend}/{rel}")
        # create empty bun.lockb placeholder
        (base / 'bun.lockb').write_text('')
        ops.append(f"✅ Created: {backend}/bun.lockb")
    except Exception as e:
        errs.append(str(e))
    return {'operations': ops, 'errors': errs, 'backend_type': 'bun'}
