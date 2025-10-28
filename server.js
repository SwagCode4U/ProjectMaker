const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();

// Project root is the folder where you run `npm start` (or override via PROJECT_ROOT)
const rootDir = path.resolve(process.env.PROJECT_ROOT || process.cwd());

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

function safeResolve(rel = '.') {
  const p = path.resolve(rootDir, rel);
  const inRoot = p === rootDir || p.startsWith(rootDir + path.sep);
  if (!inRoot) throw new Error('Path escapes project root');
  return p;
}
function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

app.get('/api/list', (req, res) => {
  try {
    const rel = req.query.dir || '';
    const abs = safeResolve(rel);
    const items = fs
      .readdirSync(abs, { withFileTypes: true })
      .map(d => ({ name: d.name, type: d.isDirectory() ? 'dir' : 'file' }))
      .sort((a, b) => a.type.localeCompare(b.type) || a.name.localeCompare(b.name));
    res.json({ ok: true, dir: path.relative(rootDir, abs) || '.', items });
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
});

app.post('/api/create', (req, res) => {
  try {
    const { currentDir = '', input = '' } = req.body || {};
    const trimmed = String(input).trim();
    if (!trimmed) throw new Error('Empty input');

    const base = safeResolve(currentDir);
    let isFile = false;
    let name = trimmed;

    if (trimmed.startsWith('/')) {
      name = trimmed.replace(/^\/+/, ''); // create folder named after input (no leading /)
    } else {
      const last = path.basename(trimmed);
      isFile = /\.[A-Za-z0-9_-]+$/.test(last); // looks like filename -> file
    }

    // Normalize and prevent ../../ escapes
    const normalized = path
      .normalize(name)
      .replace(/^(\.{2}(\/|\\|$))+/, '')
      .replace(/^[/\\]+/, ''); // no absolute

    const target = safeResolve(path.join(path.relative(rootDir, base), normalized));

    if (isFile) {
      ensureDir(path.dirname(target));
      fs.writeFileSync(target, '', { flag: 'wx' }); // fail if exists
      return res.json({ ok: true, kind: 'file', path: path.relative(rootDir, target) });
    } else {
      ensureDir(target);
      return res.json({ ok: true, kind: 'dir', path: path.relative(rootDir, target) });
    }
  } catch (e) {
    const msg = e.code === 'EEXIST' ? 'File already exists' : e.message;
    res.status(400).json({ ok: false, error: msg });
  }
});

const PORT = process.env.PORT || 3030;
app.listen(PORT, () =>
  console.log(`FS tool running at http://localhost:${PORT} (root: ${rootDir})`)
);
