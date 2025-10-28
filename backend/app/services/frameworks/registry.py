# backend/app/services/frameworks/registry.py
from pathlib import Path
from typing import Dict, Optional

# Optional imports so missing modules don't crash the server
import importlib

def _opt(module_path: str):
    try:
        return importlib.import_module(module_path)
    except Exception as e:
        print(f"[registry] failed import {module_path}: {e}")
        return None

# Backend modules (optional)
be_fastapi = _opt('app.services.frameworks.backend.fastapi')
be_express = _opt('app.services.frameworks.backend.express')
be_nextapi = _opt('app.services.frameworks.backend.nextapi')
be_flask = _opt('app.services.frameworks.backend.flask')
be_django = _opt('app.services.frameworks.backend.django')
be_nestjs = _opt('app.services.frameworks.backend.nestjs')
be_bun = _opt('app.services.frameworks.backend.bun')
be_springboot = _opt('app.services.frameworks.backend.springboot')
be_koa = _opt('app.services.frameworks.backend.koa')

# Frontend modules (optional)
fe_react = _opt('app.services.frameworks.frontend.react')
fe_svelte = _opt('app.services.frameworks.frontend.svelte')
fe_nextjs = _opt('app.services.frameworks.frontend.nextjs')
fe_vue = _opt('app.services.frameworks.frontend.vue')
fe_angular = _opt('app.services.frameworks.frontend.angular')
fe_solidjs = _opt('app.services.frameworks.frontend.solidjs')
fe_nuxt = _opt('app.services.frameworks.frontend.nuxt')
fe_html = _opt('app.services.frameworks.frontend.html')

_BACKENDS = { k:v for k,v in {
    'fastapi': be_fastapi,
    'express': be_express,
    'nextjs_api': be_nextapi,  # backend: Next.js API (distinct from frontend nextjs)
    'flask': be_flask,
    'django': be_django,
    'nestjs': be_nestjs,
    'bun': be_bun,
    'springboot': be_springboot,
    'koa': be_koa,
}.items() if v }

_FRONTENDS = { k:v for k,v in {
    'react': fe_react,
    'svelte': fe_svelte,
    'nextjs': fe_nextjs,
    'vue': fe_vue,
    'angular': fe_angular,
    'solidjs': fe_solidjs,
    'nuxt': fe_nuxt,
    'html': fe_html,
}.items() if v }

_BACKEND_ALIASES = {
    'express.js': 'express', 'expressjs': 'express', 'node': 'express', 'nodejs': 'express',
    'nest': 'nestjs', 'nestjs.js': 'nestjs',
    # Keep Next.js API distinct from Next.js frontend
    'nextjs-api': 'nextjs_api', 'nextjs_api': 'nextjs_api', 'nextjsapi': 'nextjs_api', 'nextjs api': 'nextjs_api', 'next js api': 'nextjs_api',
    # Bun aliases
    'bunjs': 'bun', 'bun.js': 'bun',
    # Spring Boot aliases
    'spring': 'springboot', 'spring-boot': 'springboot', 'springboot': 'springboot',
    # Koa aliases
    'koa.js': 'koa', 'koajs': 'koa',
    # Plain "next" or "next.js" refers to frontend nextjs only (not backend)
    'next': 'nextjs', 'next.js': 'nextjs', 'next js': 'nextjs'
}

_FRONTEND_ALIASES = {
    'next': 'nextjs', 'next.js': 'nextjs',
    'solid': 'solidjs', 'solid.js': 'solidjs',
    'nuxtjs': 'nuxt', 'nuxt.js': 'nuxt'
}

def _norm(value: Optional[str], aliases: Dict[str, str]) -> str:
    v = str(value or '').strip().lower()
    return aliases.get(v, v)

# Public API used by ProjectGenerator

def preview_backend_tree(config: Dict) -> Optional[Dict]:
    bid = _norm(config.get('backend_framework'), _BACKEND_ALIASES)
    mod = _BACKENDS.get(bid)
    if not mod:
        # Try dynamic import lazily
        dyn = _opt(f'app.services.frameworks.backend.{bid}') if bid else None
        if dyn:
            _BACKENDS[bid] = dyn
            mod = dyn
        else:
            print(f"[registry] backend module not found for '{bid}'. Available: {list(_BACKENDS.keys())}")
            return None
    try:
        return mod.preview(config)
    except Exception as e:
        print(f"[registry] backend preview error for '{bid}': {e}")
        return None

def preview_frontend_tree(config: Dict) -> Optional[Dict]:
    fid = _norm(config.get('frontend_framework'), _FRONTEND_ALIASES)
    mod = _FRONTENDS.get(fid)
    if not mod:
        # Try dynamic import lazily (hot-reload safe)
        dyn = _opt(f'app.services.frameworks.frontend.{fid}') if fid else None
        if dyn:
            _FRONTENDS[fid] = dyn
            mod = dyn
        else:
            print(f"[registry] frontend module not found for '{fid}'. Available: {list(_FRONTENDS.keys())}")
            return None
    return mod.preview(config)

def build_backend(project_root: Path, config: Dict) -> Dict:
    bid = _norm(config.get('backend_framework'), _BACKEND_ALIASES)
    mod = _BACKENDS.get(bid)
    if not mod and bid:
        dyn = _opt(f'app.services.frameworks.backend.{bid}')
        if dyn:
            _BACKENDS[bid] = dyn
            mod = dyn
    try:
        return mod.build(project_root, config) if mod else { 'operations': [], 'errors': [], 'backend_type': bid }
    except Exception as e:
        return { 'operations': [], 'errors': [str(e)], 'backend_type': bid }

def build_frontend(project_root: Path, config: Dict) -> Dict:
    fid = _norm(config.get('frontend_framework'), _FRONTEND_ALIASES)
    mod = _FRONTENDS.get(fid)
    if not mod and fid:
        dyn = _opt(f'app.services.frameworks.frontend.{fid}')
        if dyn:
            _FRONTENDS[fid] = dyn
            mod = dyn
    return mod.build(project_root, config) if mod else { 'operations': [], 'errors': [], 'frontend_type': fid }
