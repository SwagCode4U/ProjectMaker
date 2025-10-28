async function api(url, opts) {
  const r = await fetch(url, opts);
  const j = await r.json();
  if (!r.ok || !j.ok) throw new Error(j.error || r.statusText);
  return j;
}
const treeEl = document.getElementById('tree');
const rootPathEl = document.getElementById('root-path');

function liNode() {
  const li = document.createElement('li');
  li.className = 'node';
  li.innerHTML = `<div class="row">
      <span class="name dir" data-dir=".">.</span>
      <button class="btn add" title="Add inside this folder">＋</button>
    </div>
    <ul class="tree children"></ul>`;
  return li;
}

async function list(dir) {
  const data = await api('/api/list?dir=' + encodeURIComponent(dir));
  if (dir === '.') rootPathEl.textContent = data.dir || '.';
  return data.items;
}

async function renderChildren(ul, dir) {
  const items = await list(dir);
  ul.innerHTML = '';
  for (const it of items) {
    const li = document.createElement('li');
    li.className = 'node';
    if (it.type === 'dir') {
      li.innerHTML = `<div class="row">
          <span class="name dir" data-dir="${join(dir, it.name)}">${it.name}</span>
          <button class="btn add" title="Add inside this folder">＋</button>
        </div>
        <ul class="tree children" data-dir="${join(dir, it.name)}"></ul>`;
    } else {
      li.innerHTML = `<div class="row"><span class="name file">${it.name}</span></div>`;
    }
    ul.appendChild(li);
  }
}

function join(a, b) {
  return [a, b].filter(Boolean).join('/').replace(/\/+/g, '/').replace(/^\.\/+/, '.');
}

async function createInside(currentDir) {
  const input = prompt(`Create inside: ${currentDir}\n- "/name" = folder\n- "file.ext" = file`);
  if (!input) return;
  const res = await api('/api/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ currentDir, input })
  });
  alert(`Created ${res.kind}: ${res.path}`);
  // refresh this folder’s children
  const ul = treeEl.querySelector(`ul.children[data-dir="${cssEscape(currentDir)}"]`) ||
             treeEl.querySelector('ul.children'); // root fallback
  if (ul) renderChildren(ul, currentDir);
}

treeEl.addEventListener('click', async e => {
  const addBtn = e.target.closest('.add');
  const nameEl = e.target.closest('.name.dir');
  if (addBtn) {
    const dir = addBtn.parentElement.querySelector('.name.dir').dataset.dir;
    return void createInside(dir);
  }
  if (nameEl) {
    // toggle expand/collapse and prompt to add
    const dir = nameEl.dataset.dir;
    const ul = nameEl.parentElement.nextElementSibling;
    if (ul.childElementCount === 0) await renderChildren(ul, dir);
    // Show prompt immediately on name click
    return void createInside(dir);
  }
});

function cssEscape(s) { return s.replace(/["\\]/g, '\\$&'); }

(async function bootstrap() {
  const root = liNode();
  treeEl.appendChild(root);
  await renderChildren(root.querySelector('.children'), '.');
})();
