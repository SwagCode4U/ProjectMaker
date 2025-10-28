/** @jsxImportSource @emotion/react */
import { useState, useEffect } from 'react'
import { css } from '@emotion/react'
import { motion, AnimatePresence } from 'framer-motion'
import { FaFolder, FaFolderOpen, FaFile, FaChevronRight, FaChevronDown, FaSpinner, FaPlus, FaTimes } from 'react-icons/fa'
import axios from 'axios'

const containerStyles = css`
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 3rem;
`

const toastWrapStyles = css`
  position: fixed;
  top: 16px;
  right: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 1000;
`

const toastStyles = (type) => css`
  background: ${type === 'error' ? 'rgba(255, 99, 99, 0.15)' : 'rgba(76, 175, 80, 0.15)'};
  border: 1px solid ${type === 'error' ? 'rgba(255, 99, 99, 0.35)' : 'rgba(76, 175, 80, 0.35)'};
  color: ${type === 'error' ? '#ff8a8a' : '#8ae68a'};
  padding: 10px 12px;
  border-radius: 8px;
  min-width: 240px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.25);
`

const titleStyles = css`
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`

const subtitleStyles = css`
  color: var(--text-muted);
  margin-bottom: 2rem;
`

const gridStyles = css`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  
  @media (max-width: 968px) {
    grid-template-columns: 1fr;
  }
`

const panelStyles = css`
  background: rgba(15, 15, 30, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  
  h3 {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
`

const creatorStyles = css`
  margin-bottom: 1rem;
  padding: 1rem;
  border: 1px dashed rgba(255,255,255,0.15);
  border-radius: 12px;
  background: rgba(26, 26, 46, 0.5);

  .row { display: grid; grid-template-columns: 1fr auto; gap: 0.6rem; align-items: center; }
  .meta { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.6rem; }
  input[type="text"] { 
    width: 100%; padding: 0.75rem 0.9rem; border-radius: 10px; 
    border: 1px solid rgba(255,255,255,0.15); background: rgba(0,0,0,0.25); color: var(--text);
  }
  .actions { display: flex; gap: 0.6rem; justify-content: flex-end; margin-top: 0.6rem; }
  .btn { 
    padding: 0.6rem 1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.15); 
    background: rgba(15,15,30,0.8); color: var(--text); cursor: pointer; display: inline-flex; align-items: center; gap: 0.5rem;
  }
  .btn.primary { background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); border: none; color: #fff; }
  .hint { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.4rem; }
`

const treeStyles = css`
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.8;
  
  .tree-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.8rem;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.2s ease;
    
    &:hover {
      background: rgba(102, 126, 234, 0.1);
    }
    
    .icon {
      color: var(--primary);
      font-size: 1rem;
    }
    
    .chevron {
      color: var(--text-muted);
      font-size: 0.8rem;
      transition: transform 0.2s ease;
      
      &.open {
        transform: rotate(90deg);
      }
    }
    
    .name {
      color: var(--text);
      
      &.folder {
        font-weight: 600;
      }
      
      &.file {
        color: var(--text-muted);
      }
    }
  }
  
  .tree-children {
    padding-left: 1.5rem;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    margin-left: 0.5rem;
  }
`

const codeBlockStyles = css`
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  max-height: 400px;
  overflow-y: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  line-height: 1.6;
  color: var(--text-muted);
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 3px;
  }
`

const summaryStyles = css`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
`

const statCardStyles = css`
  background: rgba(15, 15, 30, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  
  .value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 0.5rem;
  }
  
  .label {
    font-size: 0.9rem;
    color: var(--text-muted);
  }
`

const loadingStyles = css`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  gap: 1rem;
  
  .spinner {
    font-size: 2rem;
    color: var(--primary);
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
`

function TreeNode({ node, level = 0, fullPath = '.', onSelectDir, expandPath }) {
  const [isOpen, setIsOpen] = useState(level < 2) // Auto-expand first 2 levels

  // Compute this node's absolute path in the preview tree
  const thisPath = fullPath === '.' ? node.name : `${fullPath}/${node.name}`

  // If a path was just created under this branch, force it open so the user can see it
  useEffect(() => {
    if (!expandPath) return
    if (expandPath === thisPath || expandPath.startsWith(thisPath + '/')) {
      setIsOpen(true)
    }
  }, [expandPath, thisPath])

  if (node.type === 'file') {
    return (
      <div className="tree-item" style={{ paddingLeft: `${level * 1.5}rem` }}>
        <FaFile className="icon" />
        <span className="name file">{node.name}</span>
      </div>
    )
  }

  return (
    <>
      <div 
        className="tree-item" 
        style={{ paddingLeft: `${level * 1.5}rem` }}
        onClick={(e) => {
          e.stopPropagation()
          // Open the folder and allow creating inside
          setIsOpen(true)
          if (typeof onSelectDir === 'function') {
            onSelectDir(thisPath)
          }
        }}
      >
        <FaChevronRight className={`chevron ${isOpen ? 'open' : ''}`} />
        {isOpen ? <FaFolderOpen className="icon" /> : <FaFolder className="icon" />}
        <span className="name folder">{node.name}</span>
      </div>
      <AnimatePresence>
        {isOpen && node.children && (
          <motion.div
            className="tree-children"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            {node.children.map((child, index) => (
              <TreeNode key={index} node={child} level={level + 1} fullPath={thisPath} onSelectDir={onSelectDir} expandPath={expandPath} />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}

function StepPreview({ data, updateData }) {
  const [tree, setTree] = useState(null)
  const [requirements, setRequirements] = useState('')
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({ files: 0, folders: 0, dependencies: 0 })
  const [toasts, setToasts] = useState([])
  const [expandPath, setExpandPath] = useState('')
  const [creatorOpen, setCreatorOpen] = useState(false)
  const [creatorDir, setCreatorDir] = useState('')
  const [creatorInput, setCreatorInput] = useState('')
  const [creating, setCreating] = useState(false)
  const [previewErrors, setPreviewErrors] = useState([])

  useEffect(() => {
    fetchPreview()
  }, [
    data.backend_framework,
    data.frontend_framework,
    data.backend_folder_name,
    data.frontend_folder_name,
    JSON.stringify(data.custom_folders || []),
    JSON.stringify(data.custom_files || [])
  ])

  const fetchPreview = async () => {
    try {
      setLoading(true)
      const response = await axios.post('/api/projects/preview', data)
      const t = response.data.tree
      setTree(t)
      setRequirements(response.data.requirements || '')

      // Detect missing framework sections to aid debugging
      const children = (t && t.children) || []
      const missing = []
      if ((data.backend_framework || '').trim()) {
        const beName = (data.backend_folder_name || 'backend')
        const hasBackend = !!children.find(n => n && n.name === beName)
        if (!hasBackend) missing.push(`Backend '${data.backend_framework}' not in preview`)
      }
      if ((data.frontend_framework || '').trim()) {
        const feName = (data.frontend_folder_name || 'frontend')
        const hasFrontend = !!children.find(n => n && n.name === feName)
        if (!hasFrontend) missing.push(`Frontend '${data.frontend_framework}' not in preview`)
      }
      setPreviewErrors(missing)
      
      // Calculate stats
      const fileCount = countNodes(response.data.tree, 'file')
      const folderCount = countNodes(response.data.tree, 'directory')
      const depCount = response.data.requirements ? response.data.requirements.split('\n').filter(l => l.trim()).length : 0
      
      setStats({ files: fileCount, folders: folderCount, dependencies: depCount })
      setLoading(false)
    } catch (error) {
      console.error('Error fetching preview:', error)
      // Fallback to mock data for development
      generateMockPreview()
    }
  }

  const generateMockPreview = () => {
    const mockTree = {
      name: data.project_name,
      type: 'directory',
      children: []
    }

    const bfw = String(data.backend_framework || '').toLowerCase()
    const ffw = String(data.frontend_framework || '').toLowerCase()

    // Backend mock by framework
    if (bfw) {
      const beName = data.backend_folder_name || 'backend'
      if (bfw === 'fastapi') {
        mockTree.children.push({
          name: beName, type: 'directory', children: [
            { name: 'app', type: 'directory', children: [
              { name: '__init__.py', type: 'file' },
              { name: 'main.py', type: 'file' },
              { name: 'database.py', type: 'file' },
              { name: 'models.py', type: 'file' },
              { name: 'schemas.py', type: 'file' },
              { name: 'crud.py', type: 'file' },
              { name: 'routes', type: 'directory', children: [
                { name: '__init__.py', type: 'file' },
                { name: 'project_routes.py', type: 'file' }
              ]}
            ]},
            { name: 'requirements.txt', type: 'file' },
            { name: '.env.example', type: 'file' }
          ]
        })
      } else if (['express','expressjs','node','nodejs'].includes(bfw)) {
        mockTree.children.push({
          name: beName, type: 'directory', children: [
            { name: 'src', type: 'directory', children: [
              { name: 'app.js', type: 'file' },
              { name: 'server.js', type: 'file' },
              { name: 'routes', type: 'directory', children: [ { name: 'index.js', type: 'file' } ] },
              { name: 'controllers', type: 'directory', children: [ { name: 'homeController.js', type: 'file' } ] },
              { name: 'middlewares', type: 'directory', children: [ { name: 'errorHandler.js', type: 'file' } ] },
              { name: 'utils', type: 'directory', children: [ { name: 'logger.js', type: 'file' } ] }
            ]},
            { name: '.env.example', type: 'file' },
            { name: 'package.json', type: 'file' },
            { name: 'README.md', type: 'file' }
          ]
        })
      } else if (['next','nextjs','next.js','nextjs-api','nextjs_api','nextjsapi'].includes(bfw)) {
        mockTree.children.push({
          name: beName, type: 'directory', children: [
            { name: 'pages', type: 'directory', children: [
              { name: 'api', type: 'directory', children: [ { name: 'hello.js', type: 'file' }, { name: 'items.js', type: 'file' } ] }
            ]},
            { name: 'next.config.mjs', type: 'file' },
            { name: 'package.json', type: 'file' }
          ]
        })
      } else if (bfw === 'flask') {
        mockTree.children.push({
          name: beName, type: 'directory', children: [
            { name: 'app.py', type: 'file' },
            { name: 'config.py', type: 'file' },
            { name: 'models.py', type: 'file' },
            { name: 'routes.py', type: 'file' },
            { name: 'requirements.txt', type: 'file' },
            { name: '.env.example', type: 'file' }
          ]
        })
      }
    }

    // Frontend mock by framework
    if (ffw) {
      const feName = data.frontend_folder_name || 'frontend'
      if (ffw === 'react') {
        mockTree.children.push({
          name: feName, type: 'directory', children: [
            { name: 'src', type: 'directory', children: [
              { name: 'App.jsx', type: 'file' }, { name: 'main.jsx', type: 'file' }, { name: 'index.css', type: 'file' }
            ]},
            { name: 'public', type: 'directory', children: [ { name: 'favicon.ico', type: 'file' } ] },
            { name: 'index.html', type: 'file' },
            { name: 'package.json', type: 'file' }
          ]
        })
      } else if (ffw === 'vue') {
        mockTree.children.push({
          name: feName, type: 'directory', children: [
            { name: 'src', type: 'directory', children: [ { name: 'App.vue', type: 'file' }, { name: 'main.js', type: 'file' } ] },
            { name: 'index.html', type: 'file' },
            { name: 'package.json', type: 'file' }
          ]
        })
      } else if (ffw === 'svelte') {
        mockTree.children.push({
          name: feName, type: 'directory', children: [
            { name: 'src', type: 'directory', children: [
              { name: 'App.svelte', type: 'file' }, { name: 'app.css', type: 'file' },
              { name: 'lib', type: 'directory', children: [ { name: 'api.js', type: 'file' }, { name: 'utils.js', type: 'file' } ] },
              { name: 'routes', type: 'directory', children: [
                { name: 'Home.svelte', type: 'file' }, { name: 'Explorer.svelte', type: 'file' }, { name: 'CreateFile.svelte', type: 'file' }, { name: 'DBDesigner.svelte', type: 'file' }
              ]}
            ]},
            { name: 'public', type: 'directory', children: [ { name: 'logo.png', type: 'file' } ] },
            { name: 'index.html', type: 'file' },
            { name: 'vite.config.js', type: 'file' },
            { name: 'tailwind.config.js', type: 'file' },
            { name: 'postcss.config.js', type: 'file' },
            { name: 'package.json', type: 'file' }
          ]
        })
      } else if (ffw === 'nextjs') {
        mockTree.children.push({
          name: feName, type: 'directory', children: [
            { name: 'app', type: 'directory', children: [ { name: 'layout.jsx', type: 'file' }, { name: 'page.jsx', type: 'file' } ] },
            { name: 'next.config.mjs', type: 'file' },
            { name: 'package.json', type: 'file' }
          ]
        })
      } else if (ffw === 'angular') {
        mockTree.children.push({
          name: feName, type: 'directory', children: [
            { name: 'src', type: 'directory', children: [
              { name: 'main.ts', type: 'file' },
              { name: 'index.html', type: 'file' },
              { name: 'app', type: 'directory', children: [
                { name: 'app.component.ts', type: 'file' },
                { name: 'app.component.html', type: 'file' }
              ]}
            ]},
            { name: 'angular.json', type: 'file' },
            { name: 'package.json', type: 'file' },
            { name: 'tailwind.config.cjs', type: 'file' },
            { name: 'postcss.config.cjs', type: 'file' }
          ]
        })
      }
    }

    // Custom folders
    (data.custom_folders || []).forEach(folder => {
      mockTree.children.push({ name: folder, type: 'directory', children: [] })
    })

    // Root files
    mockTree.children.push({ name: 'README.md', type: 'file' })
    mockTree.children.push({ name: '.gitignore', type: 'file' })

    // Mock requirements/package preview
    let mockRequirements = ''
    if (bfw === 'fastapi') {
      mockRequirements = 'fastapi==0.119.0\nuvicorn==0.38.0\nsqlalchemy==2.0.44\npydantic==2.12.3'
    } else if (bfw === 'flask') {
      mockRequirements = 'flask==3.0.0\nflask-sqlalchemy==3.1.1'
    } else if (['express','expressjs','node','nodejs'].includes(bfw)) {
      mockRequirements = '{\n  "name": "express-backend",\n  "private": true,\n  "scripts": { "dev": "nodemon src/server.js" }\n}'
    } else if (['nextjs','next','next.js'].includes(bfw)) {
      mockRequirements = '{\n  "name": "nextjs-api",\n  "private": true,\n  "scripts": { "dev": "next dev -p 5177" }\n}'
    }

    setTree(mockTree)
    setRequirements(mockRequirements)
    setStats({ 
      files: countNodes(mockTree, 'file'), 
      folders: countNodes(mockTree, 'directory'),
      dependencies: (mockRequirements && mockRequirements.includes('\n')) ? mockRequirements.split('\n').filter(Boolean).length : 0
    })
    setLoading(false)
  }

  const pushToast = (msg, type = 'success', ttl = 2200) => {
    const id = Math.random().toString(36).slice(2)
    setToasts((t) => [...t, { id, msg, type }])
    setTimeout(() => setToasts((t) => t.filter(x => x.id !== id)), ttl)
  }

  const addPathToTree = (relPath, kind) => {
    try {
      if (!tree) return
      const parts = String(relPath).split('/').filter(Boolean)
      // work inside tree.children (first node is project root)
      const rootNode = tree
      let cursor = rootNode
      for (let i = 0; i < parts.length; i++) {
        const name = parts[i]
        const isLast = i === parts.length - 1
        cursor.children = cursor.children || []
        let next = cursor.children.find((c) => c.name === name)
        if (!next) {
          next = { name, type: isLast ? (kind === 'dir' ? 'directory' : 'file') : 'directory', children: [] }
          cursor.children.push(next)
        }
        cursor = next
      }
      // trigger re-render
      setTree(JSON.parse(JSON.stringify(rootNode)))
    } catch {}
  }

  const normalizeRelDir = (dirPath) => {
    const root = (data.project_name || '').trim()
    let parts = String(dirPath || '.')
      .replace(/\\/g, '/').replace(/^\.\/?/, '')
      .split('/').filter(Boolean)
    if (root && parts[0] && parts[0].toLowerCase() === root.toLowerCase()) {
      parts = parts.slice(1)
    }
    if (parts[0] && parts[0].toLowerCase() === 'backend') parts[0] = (data.backend_folder_name || 'backend')
    if (parts[0] && parts[0].toLowerCase() === 'frontend') parts[0] = (data.frontend_folder_name || 'frontend')
    const relDir = parts.join('/') || '.'
    return relDir
  }

  const handleCreateAt = (dirPath) => {
    const relDir = normalizeRelDir(dirPath)
    setCreatorDir(relDir)
    setCreatorInput('')
    setCreatorOpen(true)
  }

  const handleCreatorSubmit = async () => {
    try {
      if (!creatorInput.trim()) return
      setCreating(true)
      const res = await axios.post('/api/fs/create', { currentDir: creatorDir || '.', input: creatorInput })
      const createdPath = String(res.data.path)
      const kind = String(res.data.kind)
      addPathToTree(createdPath, kind)
      // Expand the parent so the new item is visible
      const parentPath = kind === 'dir' ? createdPath : (createdPath.includes('/') ? createdPath.split('/').slice(0, -1).join('/') : createdPath)
      setExpandPath(parentPath)
      // Record in config so Build includes these
      if (kind === 'dir') {
        const set = new Set([...(data.custom_folders || [])])
        set.add(createdPath)
        updateData({ custom_folders: Array.from(set) })
      } else {
        const exists = (data.custom_files || []).some(f => f.name === createdPath)
        if (!exists) updateData({ custom_files: [...(data.custom_files || []), { name: createdPath, content: '' }] })
      }
      setCreatorOpen(false)
      setCreatorInput('')
      pushToast(`Created ${kind}: ${createdPath}`, 'success')
    } catch (e) {
      const msg = (e.response && e.response.data && e.response.data.detail) || e.message
      pushToast(`Error: ${msg}`, 'error')
    } finally {
      setCreating(false)
    }
  }


  const countNodes = (node, type) => {
    if (!node) return 0
    let count = node.type === type ? 1 : 0
    if (node.children) {
      count += node.children.reduce((sum, child) => sum + countNodes(child, type), 0)
    }
    return count
  }

  if (loading) {
    return (
      <motion.div
        css={containerStyles}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div css={loadingStyles}>
          <FaSpinner className="spinner" />
          <p>Generating preview...</p>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      css={containerStyles}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <h2 css={titleStyles}>Project Preview</h2>
      <p css={subtitleStyles}>
        Review your project structure before building
      </p>

      {previewErrors.length > 0 && (
        <div style={{ marginBottom: '1rem', padding: '0.8rem 1rem', borderRadius: 10, border: '1px solid rgba(255,99,99,0.35)', background: 'rgba(255,99,99,0.12)', color: '#ff8a8a' }}>
          <strong>Preview warning:</strong>
          <ul style={{ marginTop: 6 }}>
            {previewErrors.map((e,i) => (<li key={i}>• {e}</li>))}
          </ul>
        </div>
      )}

      <div css={summaryStyles}>
        <div css={statCardStyles}>
          <div className="value">{stats.folders}</div>
          <div className="label">Folders</div>
        </div>
        <div css={statCardStyles}>
          <div className="value">{stats.files}</div>
          <div className="label">Files</div>
        </div>
        <div css={statCardStyles}>
          <div className="value">{stats.dependencies}</div>
          <div className="label">Dependencies</div>
        </div>
      </div>

      <div css={toastWrapStyles}>
        {toasts.map(t => (
          <div key={t.id} css={toastStyles(t.type)}>{t.msg}</div>
        ))}
      </div>

      <div css={gridStyles}>
        <div css={panelStyles}>
          <h3>
            <FaFolder /> Project Structure
          </h3>
          {creatorOpen && (
            <div css={creatorStyles}>
              <div className="meta">Add inside: <strong>{creatorDir || '.'}</strong></div>
              <div className="row">
                <input
                  type="text"
                  placeholder="/folder  -> creates folder | file.ext  -> creates file"
                  value={creatorInput}
                  onChange={(e) => setCreatorInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') handleCreatorSubmit() }}
                  disabled={creating}
                />
                <button className="btn primary" onClick={handleCreatorSubmit} disabled={creating || !creatorInput.trim()}>
                  <FaPlus /> {creating ? 'Creating...' : 'Create'}
                </button>
              </div>
              <div className="actions">
                <button className="btn" onClick={() => setCreatorOpen(false)} disabled={creating}><FaTimes /> Cancel</button>
              </div>
              <div className="hint">Tip: start with "/name" to make a folder; use an extension to create a file.</div>
            </div>
          )}
          {data.project_name && (
            <p style={{ color: 'var(--text-muted)', marginTop: -8, marginBottom: 12 }}>
              Click any folder to open and add items inside. Root: /{data.project_name}
            </p>
          )}
          <div css={treeStyles}>
            {tree && <TreeNode node={tree} onSelectDir={handleCreateAt} expandPath={expandPath} />}
          </div>
        </div>

        <div css={panelStyles}>
          <h3>
            <FaFile /> {(['fastapi','flask','django'].includes((data.backend_framework||'').toLowerCase())) ? 'requirements.txt' : 'package.json'} Preview
          </h3>
          <div css={codeBlockStyles}>
            {requirements || 'No dependencies'}
          </div>
        </div>
      </div>

    </motion.div>
  )
}

export default StepPreview
