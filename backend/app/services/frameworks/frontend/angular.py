# backend/app/services/frameworks/frontend/angular.py
from pathlib import Path
from typing import Dict
from .. import templates_adapter as T

def normalize(v: str) -> str:
    return 'angular'

def meta() -> Dict:
    return { 'id': 'angular', 'port': 3010 }

def preview(config: Dict) -> Dict:
    name = config.get('frontend_folder_name', 'frontend')
    return {
        'name': name, 'type': 'directory', 'children': [
            { 'name': 'src', 'type': 'directory', 'children': [
                { 'name': 'index.html', 'type': 'file' },
                { 'name': 'main.ts', 'type': 'file' },
                { 'name': 'app', 'type': 'directory', 'children': [
                    { 'name': 'app.module.ts', 'type': 'file' },
                    { 'name': 'app-routing.module.ts', 'type': 'file' },
                    { 'name': 'app.component.ts', 'type': 'file' },
                    { 'name': 'app.component.html', 'type': 'file' },
                    { 'name': 'app.component.css', 'type': 'file' },
                    { 'name': 'components', 'type': 'directory', 'children': [
                        { 'name': 'header', 'type': 'directory', 'children': [
                            { 'name': 'header.component.ts', 'type': 'file' },
                            { 'name': 'header.component.html', 'type': 'file' }
                        ]},
                        { 'name': 'footer', 'type': 'directory', 'children': [
                            { 'name': 'footer.component.ts', 'type': 'file' },
                            { 'name': 'footer.component.html', 'type': 'file' }
                        ]}
                    ]},
                    { 'name': 'pages', 'type': 'directory', 'children': [
                        { 'name': 'home', 'type': 'directory', 'children': [
                            { 'name': 'home.component.ts', 'type': 'file' },
                            { 'name': 'home.component.html', 'type': 'file' }
                        ]},
                        { 'name': 'about', 'type': 'directory', 'children': [
                            { 'name': 'about.component.ts', 'type': 'file' },
                            { 'name': 'about.component.html', 'type': 'file' }
                        ]}
                    ]}
                ]},
            ]},
            { 'name': 'angular.json', 'type': 'file' },
            { 'name': 'package.json', 'type': 'file' },
            { 'name': 'tailwind.config.cjs', 'type': 'file' },
            { 'name': 'postcss.config.cjs', 'type': 'file' },
        ]
    }

def build(root: Path, config: Dict) -> Dict:
    frontend = config.get('frontend_folder_name', 'frontend')
    base = root / frontend
    ops, errs = [], []
    try:
        (base / 'src' / 'app' / 'components' / 'header').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'app' / 'components' / 'footer').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'app' / 'pages' / 'home').mkdir(parents=True, exist_ok=True)
        (base / 'src' / 'app' / 'pages' / 'about').mkdir(parents=True, exist_ok=True)
        files = {
            'package.json': T.angular_package_json(config),
            'angular.json': T.angular_json(config),
            'src/index.html': T.angular_index_html(config),
            'src/main.ts': T.angular_main(config),
            'src/app/app.module.ts': T.angular_app_module(config),
            'src/app/app-routing.module.ts': T.angular_app_routing_module(config),
            'src/app/app.component.ts': """import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent { title = 'Angular Boilerplate'; }
""",
            'src/app/app.component.html': """<app-header></app-header>
<main class=\"p-10 max-w-4xl mx-auto\">
  <router-outlet></router-outlet>
</main>
<app-footer></app-footer>
""",
            'src/app/app.component.css': "",
            'src/app/components/header/header.component.ts': T.angular_header_component_ts(config),
            'src/app/components/header/header.component.html': T.angular_header_component_html(config),
            'src/app/components/footer/footer.component.ts': T.angular_footer_component_ts(config),
            'src/app/components/footer/footer.component.html': T.angular_footer_component_html(config),
            'src/app/pages/home/home.component.ts': T.angular_home_component_ts(config),
            'src/app/pages/home/home.component.html': T.angular_home_component_html(config),
            'src/app/pages/about/about.component.ts': T.angular_about_component_ts(config),
            'src/app/pages/about/about.component.html': T.angular_about_component_html(config),
            'tailwind.config.cjs': "module.exports={content:['./src/**/*.{html,ts}'],theme:{extend:{}},plugins:[]}\n",
            'postcss.config.cjs': "module.exports={plugins:{tailwindcss:{},autoprefixer:{}}}\n",
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {frontend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return { 'operations': ops, 'errors': errs, 'frontend_type': 'angular' }
