# backend/app/services/frameworks/backend/nestjs.py
from pathlib import Path
from typing import Dict

def normalize(v: str) -> str:
    return 'nestjs'

def meta() -> Dict:
    return { 'id': 'nestjs', 'port': 5177 }

def preview(config: Dict) -> Dict:
    name = config.get('backend_folder_name', 'backend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'src', 'type': 'directory', 'children': [
                { 'name': 'modules', 'type': 'directory', 'children': [
                    { 'name': 'auth', 'type': 'directory', 'children': [
                        { 'name': 'auth.controller.ts', 'type': 'file' },
                        { 'name': 'auth.service.ts', 'type': 'file' },
                        { 'name': 'auth.module.ts', 'type': 'file' },
                        { 'name': 'dto', 'type': 'directory', 'children': [
                            { 'name': 'login.dto.ts', 'type': 'file' },
                            { 'name': 'register.dto.ts', 'type': 'file' }
                        ]}
                    ]},
                    { 'name': 'users', 'type': 'directory', 'children': [
                        { 'name': 'users.controller.ts', 'type': 'file' },
                        { 'name': 'users.service.ts', 'type': 'file' },
                        { 'name': 'users.module.ts', 'type': 'file' },
                        { 'name': 'dto', 'type': 'directory', 'children': [ { 'name': 'create-user.dto.ts', 'type': 'file' } ] }
                    ]},
                    { 'name': 'shared', 'type': 'directory', 'children': [
                        { 'name': 'guards', 'type': 'directory', 'children': [ { 'name': 'jwt-auth.guard.ts', 'type': 'file' } ] },
                        { 'name': 'interceptors', 'type': 'directory', 'children': [ { 'name': 'logging.interceptor.ts', 'type': 'file' } ] },
                        { 'name': 'pipes', 'type': 'directory', 'children': [ { 'name': 'validation.pipe.ts', 'type': 'file' } ] }
                    ]}
                ]},
                { 'name': 'common', 'type': 'directory', 'children': [
                    { 'name': 'exceptions', 'type': 'directory', 'children': [ { 'name': 'http.exception.ts', 'type': 'file' } ] },
                    { 'name': 'filters', 'type': 'directory', 'children': [ { 'name': 'http-exception.filter.ts', 'type': 'file' } ] },
                    { 'name': 'constants.ts', 'type': 'file' }
                ]},
                { 'name': 'config', 'type': 'directory', 'children': [ { 'name': 'configuration.ts', 'type': 'file' } ] },
                { 'name': 'main.ts', 'type': 'file' },
                { 'name': 'app.module.ts', 'type': 'file' },
                { 'name': 'app.controller.ts', 'type': 'file' }
            ]},
            { 'name': '.env.example', 'type': 'file' },
            { 'name': '.gitignore', 'type': 'file' },
            { 'name': 'package.json', 'type': 'file' },
            { 'name': 'tsconfig.json', 'type': 'file' },
            { 'name': 'nest-cli.json', 'type': 'file' },
            { 'name': 'README.md', 'type': 'file' }
        ]
    }

def build(root: Path, config: Dict) -> Dict:
    backend = config.get('backend_folder_name', 'backend')
    base = root / backend
    ops, errs = [], []
    try:
        # directories
        (base / 'src' / 'modules' / 'auth' / 'dto').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'modules' / 'users' / 'dto').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'modules' / 'shared' / 'guards').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'modules' / 'shared' / 'interceptors').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'modules' / 'shared' / 'pipes').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'common' / 'exceptions').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'common' / 'filters').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'config').mkdir(parents=True, exist_ok=True)
        
        files: Dict[str, str] = {
            'package.json': """{
  "name": "nestjs-boilerplate",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "start": "node dist/main",
    "start:dev": "nest start --watch",
    "build": "nest build",
    "lint": "eslint . --ext .ts"
  },
  "dependencies": {
    "@nestjs/common": "^9.0.0",
    "@nestjs/core": "^9.0.0",
    "@nestjs/platform-express": "^9.0.0",
    "class-validator": "^0.14.0",
    "class-transformer": "^0.5.0",
    "dotenv": "^10.0.0",
    "jsonwebtoken": "^9.0.0"
  },
  "devDependencies": {
    "@nestjs/cli": "^9.0.0",
    "@nestjs/schematics": "^9.0.0",
    "eslint": "^8.0.0",
    "typescript": "^4.5.0"
  }
}
""",
            'tsconfig.json': """{ "compilerOptions": { "module": "commonjs", "declaration": true, "removeComments": true, "emitDecoratorMetadata": true, "experimentalDecorators": true, "allowSyntheticDefaultImports": true, "target": "es2017", "sourceMap": true, "outDir": "./dist", "baseUrl": "./", "incremental": true }, "exclude": ["node_modules","dist"] }
""",
            'nest-cli.json': """{ "collection": "@nestjs/schematics", "sourceRoot": "src" }
""",
            '.env.example': """DATABASE_URL=your_database_url
JWT_SECRET=your_jwt_secret
PORT=3000
""",
            '.gitignore': """node_modules
dist
.env
""",
            'README.md': """# NestJS Boilerplate

A boilerplate project for building robust APIs using **NestJS**.
""",
            'src/main.ts': """import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
async function bootstrap(){ const app = await NestFactory.create(AppModule); app.useGlobalPipes(new ValidationPipe()); await app.listen(3000); }
bootstrap();
""",
            'src/app.module.ts': """import { Module } from '@nestjs/common';
import { AuthModule } from './modules/auth/auth.module';
import { UsersModule } from './modules/users/users.module';
@Module({ imports: [AuthModule, UsersModule] })
export class AppModule {}
""",
            'src/app.controller.ts': """import { Controller, Get } from '@nestjs/common';
@Controller()
export class AppController{ @Get() hello(){ return { message: 'Hello NestJS' } } }
""",
            # Auth
            'src/modules/auth/auth.module.ts': """import { Module } from '@nestjs/common';
import { AuthService } from './auth.service';
import { AuthController } from './auth.controller';
@Module({ controllers:[AuthController], providers:[AuthService] })
export class AuthModule {}
""",
            'src/modules/auth/auth.service.ts': """import { Injectable } from '@nestjs/common';
@Injectable()
export class AuthService{ login(){ return { ok:true } } }
""",
            'src/modules/auth/auth.controller.ts': """import { Controller, Post, Body } from '@nestjs/common';
import { AuthService } from './auth.service';
@Controller('auth')
export class AuthController{
  constructor(private readonly authService: AuthService){}
  @Post('login') login(@Body() body:any){ return this.authService.login() }
}
""",
            'src/modules/auth/dto/login.dto.ts': """import { IsString } from 'class-validator';
export class LoginDto{ @IsString() username:string; @IsString() password:string }
""",
            'src/modules/auth/dto/register.dto.ts': """import { IsString } from 'class-validator';
export class RegisterDto{ @IsString() username:string; @IsString() password:string }
""",
            # Users
            'src/modules/users/users.module.ts': """import { Module } from '@nestjs/common';
import { UsersService } from './users.service';
import { UsersController } from './users.controller';
@Module({ controllers:[UsersController], providers:[UsersService] })
export class UsersModule {}
""",
            'src/modules/users/users.service.ts': """import { Injectable } from '@nestjs/common';
@Injectable()
export class UsersService{ findAll(){ return [] } }
""",
            'src/modules/users/users.controller.ts': """import { Controller, Get } from '@nestjs/common';
import { UsersService } from './users.service';
@Controller('users')
export class UsersController{
  constructor(private readonly usersService: UsersService){}
  @Get() findAll(){ return this.usersService.findAll() }
}
""",
            'src/modules/users/dto/create-user.dto.ts': """export class CreateUserDto{ name:string }
""",
            # Shared
            'src/modules/shared/guards/jwt-auth.guard.ts': """export class JwtAuthGuard{}
""",
            'src/modules/shared/interceptors/logging.interceptor.ts': """export class LoggingInterceptor{}
""",
            'src/modules/shared/pipes/validation.pipe.ts': """export class ValidationPipe{}
""",
            # Common
            'src/common/exceptions/http.exception.ts': """import { HttpException, HttpStatus } from '@nestjs/common';
export class CustomHttpException extends HttpException{ constructor(message:string){ super(message, HttpStatus.BAD_REQUEST) } }
""",
            'src/common/filters/http-exception.filter.ts': """export class HttpExceptionFilter{}
""",
            'src/common/constants.ts': """export const APP_NAME='nestjs-boilerplate';
""",
            # Config
            'src/config/configuration.ts': """export default ()=>({ port: parseInt(process.env.PORT||'3000',10) || 3000, database: process.env.DATABASE_URL });
""",
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {backend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'backend_type': 'nestjs' }
