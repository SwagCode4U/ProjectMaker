# backend/app/services/frameworks/frontend/vue.py
from pathlib import Path
from typing import Dict

def normalize(v: str) -> str:
    return 'vue'

def meta() -> Dict:
    return { 'id': 'vue', 'port': 3010 }

# Full Vue 3 + Vite + TS + Router + Pinia preview

def preview(config: Dict) -> Dict:
    name = config.get('frontend_folder_name', 'frontend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'public', 'type': 'directory', 'children': [
                { 'name': 'favicon.ico', 'type': 'file' },
                { 'name': 'logo.png', 'type': 'file' },
            ]},
            { 'name': 'src', 'type': 'directory', 'children': [
                { 'name': 'assets', 'type': 'directory', 'children': [ { 'name': 'main.css', 'type': 'file' } ] },
                { 'name': 'components', 'type': 'directory', 'children': [ { 'name': 'HelloWorld.vue', 'type': 'file' } ] },
                { 'name': 'layouts', 'type': 'directory', 'children': [ { 'name': 'DefaultLayout.vue', 'type': 'file' } ] },
                { 'name': 'pages', 'type': 'directory', 'children': [ { 'name': 'Home.vue', 'type': 'file' }, { 'name': 'About.vue', 'type': 'file' } ] },
                { 'name': 'router', 'type': 'directory', 'children': [ { 'name': 'index.ts', 'type': 'file' } ] },
                { 'name': 'store', 'type': 'directory', 'children': [ { 'name': 'index.ts', 'type': 'file' } ] },
                { 'name': 'App.vue', 'type': 'file' },
                { 'name': 'main.ts', 'type': 'file' },
                { 'name': 'vite-env.d.ts', 'type': 'file' },
            ]},
            { 'name': '.env.example', 'type': 'file' },
            { 'name': 'index.html', 'type': 'file' },
            { 'name': 'package.json', 'type': 'file' },
            { 'name': 'tsconfig.json', 'type': 'file' },
            { 'name': 'vite.config.ts', 'type': 'file' },
            { 'name': 'README.md', 'type': 'file' },
        ]
    }

# Build full Vue boilerplate

def build(root: Path, config: Dict) -> Dict:
    frontend = config.get('frontend_folder_name', 'frontend')
    base = root / frontend
    ops, errs = [], []
    try:
        (base / 'public').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'assets').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'components').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'layouts').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'pages').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'router').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'store').mkdir(parents=True, exist_ok=True)

        files: Dict[str, str] = {
            'package.json': '{\n  "name": "vue-app",\n  "version": "1.0.0",\n  "private": true,\n  "scripts": {\n    "dev": "vite --port 3010",\n    "build": "vite build",\n    "preview": "vite preview",\n    "lint": "eslint src --ext .ts,.vue"\n  },\n  "dependencies": {\n    "vue": "^3.4.0",\n    "vue-router": "^4.3.0",\n    "pinia": "^2.1.7"\n  },\n  "devDependencies": {\n    "typescript": "^5.3.0",\n    "vite": "^5.0.0",\n    "@vitejs/plugin-vue": "^5.0.0",\n    "eslint": "^9.0.0",\n    "@vue/eslint-config-typescript": "^13.0.0"\n  }\n}\n',
            'vite.config.ts': "import { defineConfig } from 'vite'\nimport vue from '@vitejs/plugin-vue'\nexport default defineConfig({ plugins: [vue()], server: { port: 3010, open: true }, resolve: { alias: { '@': '/src' } } })\n",
            'tsconfig.json': '{\n  "compilerOptions": {\n    "target": "ES2020",\n    "useDefineForClassFields": true,\n    "module": "ESNext",\n    "moduleResolution": "Bundler",\n    "strict": true,\n    "jsx": "preserve",\n    "resolveJsonModule": true,\n    "isolatedModules": true,\n    "esModuleInterop": true,\n    "lib": ["ES2020", "DOM", "DOM.Iterable"]\n  },\n  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"]\n}\n',
            'index.html': '<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n    <title>Vue App</title>\n  </head>\n  <body>\n    <div id="app"></div>\n    <script type="module" src="/src/main.ts"></script>\n  </body>\n</html>\n',
            '.env.example': 'VITE_API_URL=http://localhost:3010\n',
            'README.md': '# Vue 3 + Vite Boilerplate\n\nA modern Vue 3 boilerplate preconfigured with Vite, TypeScript, Pinia, and Vue Router.\n',
            'public/favicon.ico': 'placeholder',
            'public/logo.png': 'placeholder',
            'src/assets/main.css': 'body { font-family: Inter, system-ui, sans-serif; }\n',
            'src/components/HelloWorld.vue': '<template><div class="hello"><h1>{{ msg }}</h1><p>This is a reusable component in Vue 3 + Vite boilerplate.</p></div></template>\n<script setup lang="ts">defineProps<{ msg: string }>()</script>\n<style scoped>.hello{padding:2rem;text-align:center;}</style>\n',
            'src/layouts/DefaultLayout.vue': '<template><div><header><nav><router-link to="/">Home</router-link><router-link to="/about">About</router-link></nav></header><main><slot /></main></div></template>\n<style scoped>nav{display:flex;gap:1rem;justify-content:center;background:#42b883;padding:1rem;}a{color:#fff;text-decoration:none;}a.router-link-exact-active{text-decoration:underline;}</style>\n',
            'src/pages/Home.vue': '<template><DefaultLayout><div class="home"><h1>🏠 Welcome to Vue 3 Boilerplate</h1><p>Built with Vite + TypeScript + Pinia + Router</p><router-link to="/about">Go to About →</router-link></div></DefaultLayout></template>\n<script setup lang="ts"></script>\n<style scoped>.home{text-align:center;padding:2rem;}</style>\n',
            'src/pages/About.vue': '<template><DefaultLayout><div class="home"><h2>About</h2></div></DefaultLayout></template>\n<script setup lang="ts"></script>\n',
            'src/router/index.ts': "import { createRouter, createWebHistory } from 'vue-router'\nimport Home from '@/pages/Home.vue'\nimport About from '@/pages/About.vue'\nconst routes=[{path:'/',name:'Home',component:Home},{path:'/about',name:'About',component:About}]\nexport default createRouter({ history: createWebHistory(), routes })\n",
            'src/store/index.ts': "import { defineStore } from 'pinia'\nexport const useMainStore=defineStore('main',{ state:()=>({ user:null as string|null, counter:0 }), actions:{ setUser(name:string){ this.user=name }, increment(){ this.counter++ } } })\n",
            'src/App.vue': '<template><router-view /></template>\n',
            'src/main.ts': "import { createApp } from 'vue'\nimport { createPinia } from 'pinia'\nimport App from './App.vue'\nimport router from './router'\nimport './assets/main.css'\nconst app=createApp(App);app.use(createPinia());app.use(router);app.mount('#app')\n",
            'src/vite-env.d.ts': '/// <reference types="vite/client" />\n',
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {frontend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'frontend_type': 'vue' }
