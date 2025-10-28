# backend/app/services/frameworks/frontend/html.py
from pathlib import Path
from typing import Dict


def normalize(v: str) -> str:
    return 'html'


def meta() -> Dict:
    return {'id': 'html', 'port': 0}


def preview(config: Dict) -> Dict:
    name = config.get('frontend_folder_name', 'frontend')
    return {
        'name': name,
        'type': 'directory',
        'children': [
            {'name': 'index.html', 'type': 'file'},
            {'name': 'styles.css', 'type': 'file'},
            {'name': 'script.js', 'type': 'file'},
        ]
    }


def build(root: Path, config: Dict) -> Dict:
    frontend = config.get('frontend_folder_name', 'frontend')
    base = root / frontend
    ops, errs = [], []
    try:
        base.mkdir(parents=True, exist_ok=True)
        files: Dict[str, str] = {
            'index.html': """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <meta name=\"color-scheme\" content=\"light dark\" />
  <title>Project Maker</title>
  <link rel=\"stylesheet\" href=\"styles.css\" />
  <link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>✨</text></svg>\" />
</head>
<body>
  <div class=\"container\">
    <header>
      <h1 class=\"shiny-heading\">Project Maker</h1>
    </header>
    <main>
      <p>Welcome to your project! Start building amazing things.</p>
      <button id=\"toggle-mode\" aria-pressed=\"false\">Toggle Theme</button>
    </main>
  </div>
  <script src=\"script.js\"></script>
</body>
</html>
""",
            'styles.css': """/* Base reset */
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; height: 100%; }

:root {
  --bg: #121212;
  --fg: #ffffff;
  --accent: #ff4081;
  --accent-2: #6200ea;
}

@media (prefers-color-scheme: light) {
  :root { --bg: #ffffff; --fg: #000000; --accent: #6200ea; }
}

body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
  background: var(--bg); color: var(--fg); transition: background .3s ease, color .3s ease; }
.container { max-width: 860px; margin: 0 auto; padding: 24px; }
header { text-align: center; margin: 24px 0; }

.shiny-heading { font-size: clamp(2rem, 4vw, 2.75rem); color: var(--accent); text-shadow: 0 0 20px color-mix(in oklab, var(--accent), transparent 40%);
  letter-spacing: .5px; transition: transform .25s ease, text-shadow .25s ease; }
.shiny-heading:hover { transform: translateY(-2px) scale(1.02); text-shadow: 0 0 30px color-mix(in oklab, var(--accent), white 20%); }

button { padding: 10px 18px; font-size: 1rem; border: 0; border-radius: 10px; background: var(--accent-2); color: white; cursor: pointer; box-shadow: 0 6px 20px rgba(0,0,0,.25);
  transition: transform .2s ease, background .2s ease, box-shadow .2s ease; }
button:hover { transform: translateY(-1px); box-shadow: 0 10px 28px rgba(0,0,0,.3); }
button:active { transform: translateY(0); }

/* Light/dark override via class */
body.light { --bg: #ffffff; --fg: #000000; --accent: #6200ea; }
body.light .shiny-heading { text-shadow: 0 0 20px color-mix(in oklab, var(--accent), transparent 40%); }

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition: none !important; }
}
""",
            'script.js': """(() => {
  const KEY = 'pm-theme';
  const btn = document.getElementById('toggle-mode');
  const saved = localStorage.getItem(KEY);
  if (saved === 'light') document.body.classList.add('light');
  const applyAria = () => btn && btn.setAttribute('aria-pressed', String(document.body.classList.contains('light')));
  applyAria();
  btn?.addEventListener('click', () => {
    document.body.classList.toggle('light');
    localStorage.setItem(KEY, document.body.classList.contains('light') ? 'light' : 'dark');
    applyAria();
  });
})();
""",
        }
        for rel, content in files.items():
            fp = base / rel
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
            ops.append(f"✅ Created: {frontend}/{rel}")
    except Exception as e:
        errs.append(str(e))
    return {'operations': ops, 'errors': errs, 'frontend_type': 'html'}
