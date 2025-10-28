# backend/app/services/frameworks/frontend/nuxt.py
from pathlib import Path
from typing import Dict

def normalize(v: str) -> str:
    return 'nuxt'

def meta() -> Dict:
    return { 'id': 'nuxt', 'port': 3010 }

# Preview tree for Nuxt 3 + TS

def preview(config: Dict) -> Dict:
    name = config.get('frontend_folder_name', 'frontend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'assets', 'type': 'directory', 'children': [ { 'name': 'main.css', 'type': 'file' } ] },
            { 'name': 'components', 'type': 'directory', 'children': [ { 'name': 'Navbar.vue', 'type': 'file' } ] },
            { 'name': 'composables', 'type': 'directory' },
            { 'name': 'layouts', 'type': 'directory', 'children': [ { 'name': 'default.vue', 'type': 'file' } ] },
            { 'name': 'middleware', 'type': 'directory' },
            { 'name': 'pages', 'type': 'directory', 'children': [ { 'name': 'index.vue', 'type': 'file' }, { 'name': 'about.vue', 'type': 'file' }, { 'name': 'users.vue', 'type': 'file' } ] },
            { 'name': 'plugins', 'type': 'directory', 'children': [ { 'name': 'api.ts', 'type': 'file' } ] },
            { 'name': 'public', 'type': 'directory', 'children': [ { 'name': 'favicon.png', 'type': 'file' } ] },
            { 'name': 'server', 'type': 'directory', 'children': [ { 'name': 'api', 'type': 'directory', 'children': [ { 'name': 'hello.ts', 'type': 'file' } ] } ] },
            { 'name': 'utils', 'type': 'directory' },
            { 'name': 'app.vue', 'type': 'file' },
            { 'name': 'nuxt.config.ts', 'type': 'file' },
            { 'name': 'package.json', 'type': 'file' },
            { 'name': 'tsconfig.json', 'type': 'file' },
            { 'name': 'README.md', 'type': 'file' },
        ]
    }

# Build Nuxt 3 boilerplate

def build(root: Path, config: Dict) -> Dict:
    frontend = config.get('frontend_folder_name', 'frontend')
    base = root / frontend
    ops, errs = [], []
    try:
        # dirs
        (base / 'assets').mkdir(parents=True, exist_ok=True)
        (base / 'components').mkdir(parents=True, exist_ok=True)
        (base / 'composables').mkdir(parents=True, exist_ok=True)
        (base / 'layouts').mkdir(parents=True, exist_ok=True)
        (base / 'middleware').mkdir(parents=True, exist_ok=True)
        (base / 'pages').mkdir(parents=True, exist_ok=True)
        (base / 'plugins').mkdir(parents=True, exist_ok=True)
        (base / 'public').mkdir(parents=True, exist_ok=True)
        (base / 'server' / 'api').mkdir(parents=True, exist_ok=True)
        (base / 'utils').mkdir(parents=True, exist_ok=True)

        files: Dict[str, str] = {
            'package.json': """{
  "name": "nuxt-app",
  "version": "1.0.0",
  "description": "A clean Nuxt 3 boilerplate for modern web apps",
  "private": true,
  "scripts": {
    "dev": "nuxt dev -p 3010",
    "build": "nuxt build",
    "preview": "nuxt preview",
    "lint": "eslint --ext .js,.ts,.vue ."
  },
  "dependencies": { "nuxt": "^3.13.0" },
  "devDependencies": { "eslint": "^9.0.0", "eslint-plugin-nuxt": "^5.0.0", "typescript": "^5.4.0" }
}
""",
            'nuxt.config.ts': """// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/main.css'],
  app: {
    head: {
      title: 'Nuxt App - Boilerplate',
      meta: [
        { name: 'description', content: 'A Nuxt 3 starter template' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      link: [{ rel: 'icon', type: 'image/png', href: '/favicon.png' }]
    }
  },
  modules: [],
  typescript: { strict: true },
  runtimeConfig: {
    apiSecret: process.env.API_SECRET,
    public: { apiBase: '/api' }
  }
})
""",
            'tsconfig.json': """{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "jsx": "preserve",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"]
  },
  "include": ["**/*.ts", "**/*.vue"],
  "exclude": ["node_modules", ".nuxt"]
}
""",
            'README.md': """# Nuxt 3 Boilerplate

A clean, professional Nuxt 3 starter kit ready for modern web app development.
""",
            'assets/main.css': """body { font-family: Inter, system-ui, sans-serif; }
""",
            'components/Navbar.vue': """<template>
  <nav class="flex justify-between p-4 shadow bg-white">
    <NuxtLink to="/" class="font-semibold text-green-600">NuxtBoiler</NuxtLink>
    <div class="space-x-4">
      <NuxtLink to="/about">About</NuxtLink>
      <NuxtLink to="/users">Users</NuxtLink>
    </div>
  </nav>
</template>
""",
            'layouts/default.vue': """<template>
  <div>
    <Navbar />
    <main><slot /></main>
  </div>
</template>
""",
            'pages/index.vue': """<template>
  <div class="home">
    <Navbar />
    <section class="content">
      <h1>Welcome to Nuxt 3 Boilerplate</h1>
      <p>This app is fully typed and scalable.</p>
      <NuxtLink to="/about">Go to About Page</NuxtLink>
    </section>
  </div>
</template>
<script setup lang="ts">
definePageMeta({ layout: 'default' })
</script>
""",
            'pages/about.vue': """<template>
  <div class="p-6"><h2>About</h2></div>
</template>
""",
            'pages/users.vue': """<template>
  <div class="p-6"><h2>Users</h2></div>
</template>
""",
            'plugins/api.ts': """export default defineNuxtPlugin(() => { /* setup axios or fetch wrapper here */ })
""",
            'public/favicon.png': 'placeholder',
            'server/api/hello.ts': """export default defineEventHandler(() => ({
  message: 'Hello from Nuxt 3 Server API 👋'
}))
""",
            'app.vue': """<template><NuxtPage /></template>
""",
        }

        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {frontend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'frontend_type': 'nuxt' }
