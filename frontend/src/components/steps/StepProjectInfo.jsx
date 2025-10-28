/** @jsxImportSource @emotion/react */
import React from 'react'
import { css } from '@emotion/react'
import { motion } from 'framer-motion'
import { FaPython, FaReact, FaVuejs, FaAngular, FaHtml5, FaNodeJs, FaLeaf } from 'react-icons/fa'
import { SiFlask, SiFastapi, SiDjango, SiExpress, SiNestjs, SiNextdotjs, SiNuxtdotjs, SiSvelte, SiSolid } from 'react-icons/si'
import bunLogo from 'simple-icons/icons/bun.svg'
import axios from 'axios'

const containerStyles = css`
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 3rem;
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

const formGroupStyles = css`
  margin-bottom: 2rem;
  
  label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.8rem;
    color: var(--text);
    font-size: 1.1rem;
  }
  
  input, textarea {
    width: 100%;
    padding: 1rem;
    background: rgba(15, 15, 30, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: var(--text);
    font-size: 1rem;
    font-family: inherit;
    transition: all 0.3s ease;
    
    &:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    &::placeholder {
      color: var(--text-muted);
    }
  }
  
  textarea {
    resize: vertical;
    min-height: 120px;
  }
  
  .hint {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
  }
`

const frameworkGridStyles = css`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
`

const frameworkCardStyles = css`
  background: rgba(15, 15, 30, 0.6);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  
  &:hover {
    transform: translateY(-4px);
    border-color: rgba(102, 126, 234, 0.5);
    background: rgba(15, 15, 30, 0.8);
  }
  
  &.selected {
    border-color: var(--primary);
    background: rgba(102, 126, 234, 0.1);
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
  }
  
  .icon {
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
    color: var(--primary);
  }
  
  .name {
    font-weight: 600;
    color: var(--text);
    font-size: 1rem;
  }
`

const sectionStyles = css`
  margin-bottom: 2.5rem;
  
  h3 {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
  }
  
  .description {
    color: var(--text-muted);
    margin-bottom: 1rem;
  }
`

function StepProjectInfo({ data, updateData }) {
  const [backendFrameworks, setBackendFrameworks] = React.useState([])
  const [frontendFrameworks, setFrontendFrameworks] = React.useState([])

  const iconMap = {
    fastapi: <SiFastapi />,
    flask: <SiFlask />,
    django: <SiDjango />,
    express: <SiExpress />,
    nestjs: <SiNestjs />,
    springboot: <FaLeaf />,
    nextdotjs: <SiNextdotjs />,
    bun: (
      <div aria-label="Bun" style={{ width: '2.5rem', height: '2.5rem', backgroundColor: 'var(--primary)', WebkitMaskImage: `url(${bunLogo})`, maskImage: `url(${bunLogo})`, WebkitMaskRepeat: 'no-repeat', maskRepeat: 'no-repeat', WebkitMaskPosition: 'center', maskPosition: 'center', WebkitMaskSize: 'contain', maskSize: 'contain', display: 'inline-block' }} />
    ),
    koa: <FaNodeJs />,
    react: <FaReact />,
    vue: <FaVuejs />,
    nuxtdotjs: <SiNuxtdotjs />,
    angular: <FaAngular />,
    svelte: <SiSvelte />,
    solid: <SiSolid />,
    html5: <FaHtml5 />
  }

  React.useEffect(() => {
    const load = async () => {
      try {
        const res = await axios.get('/api/projects/frameworks')
        const b = (res.data.backend || []).map(f => ({ ...f, iconEl: iconMap[f.icon] || <FaPython /> }))
        const f = (res.data.frontend || []).map(fr => ({ ...fr, iconEl: iconMap[fr.icon] || <FaHtml5 /> }))
        // Append a "none" option
        setBackendFrameworks([...b, { id: 'none', name: 'None', iconEl: <FaPython /> }])
        setFrontendFrameworks([...f, { id: 'none', name: 'None', iconEl: <FaHtml5 /> }])
      } catch (e) {
        // Fallback to minimal defaults
        setBackendFrameworks([
          { id: 'fastapi', name: 'FastAPI', iconEl: <SiFastapi /> },
          { id: 'flask', name: 'Flask', iconEl: <SiFlask /> },
          { id: 'django', name: 'Django', iconEl: <SiDjango /> },
          { id: 'express', name: 'Express.js', iconEl: <SiExpress /> },
          { id: 'none', name: 'None', iconEl: <FaPython /> }
        ])
        setFrontendFrameworks([
          { id: 'react', name: 'React', iconEl: <FaReact /> },
          { id: 'nextjs', name: 'Next.js', iconEl: <SiNextdotjs /> },
          { id: 'html', name: 'HTML/CSS/JS', iconEl: <FaHtml5 /> },
          { id: 'none', name: 'None', iconEl: <FaHtml5 /> }
        ])
      }
    }
    load()
  }, [])

  const handleChange = (field, value) => {
    updateData({ [field]: value })
  }

  const generateFolderName = (projectName) => {
    // Keep letters only, remove spaces/symbols, preserve original casing
    const lettersOnly = String(projectName || '').replace(/[^A-Za-z]/g, '')
    // Fallback to 'Project' if empty after sanitization
    return lettersOnly || 'Project'
  }

  const [dirConfirmed, setDirConfirmed] = React.useState(false)
  const [parentDir, setParentDir] = React.useState('')

  const handleProjectNameChange = (value) => {
    handleChange('project_name', value)
    setDirConfirmed(false)
  }

  return (
    <motion.div
      css={containerStyles}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <h2 css={titleStyles}>Project Information</h2>
      <p css={subtitleStyles}>
        Let's start by defining your project basics
      </p>

      <div css={formGroupStyles}>
        <label htmlFor="project_name">Project Name *</label>
        <input
          id="project_name"
          type="text"
          placeholder="e.g., My Awesome App"
          value={data.project_name}
          onChange={(e) => handleProjectNameChange(e.target.value)}
          autoFocus
        />
        {data.project_name && (
          <div className="hint">
            📁 Folder name (auto): <strong>/{generateFolderName(data.project_name)}</strong>
            <br />
            No need to create it manually — we’ll create this folder for you.
          </div>
        )}
      </div>

      <div css={formGroupStyles}>
        <label htmlFor="parent_dir">Parent Directory (optional)</label>
        <input
          id="parent_dir"
          type="text"
          placeholder="e.g., /home/john/projects"
          value={parentDir}
          onChange={(e) => { setParentDir(e.target.value); setDirConfirmed(false); }}
        />
        {data.project_name && (
          <div
            css={css`
              margin-top: 0.75rem;
              padding: 0.75rem 1rem;
              border-radius: 10px;
              border: 1px solid ${dirConfirmed ? 'rgba(72,187,120,0.6)' : 'rgba(102,126,234,0.4)'};
              background: ${dirConfirmed ? 'rgba(72,187,120,0.1)' : 'rgba(102,126,234,0.08)'};
              color: var(--text);
              display: flex;
              align-items: center;
              justify-content: space-between;
              gap: 1rem;
            `}
          >
            {(() => {
              const folder = generateFolderName(data.project_name)
              const base = String(parentDir || '').replace(/\/+$/,'')
              const full = (base ? base + '/' : '') + folder
              return (
                <>
                  <span>📂 Target path: <code>{full}</code></span>
                  {!dirConfirmed ? (
                    <button
                      onClick={() => { setDirConfirmed(true); handleChange('target_directory', full) }}
                      css={css`
                        padding: 0.5rem 0.9rem;
                        border-radius: 8px;
                        border: 1px solid var(--primary);
                        background: rgba(102,126,234,0.15);
                        color: var(--text);
                        cursor: pointer;
                      `}
                    >Confirm</button>
                  ) : (
                    <span css={css`color: var(--success); font-weight: 600;`}>✔ Confirmed</span>
                  )}
                </>
              )
            })()}
          </div>
        )}
      </div>

      <div css={formGroupStyles}>
        <label htmlFor="description">Project Description *</label>
        <textarea
          id="description"
          placeholder="Describe what your project does..."
          value={data.description}
          onChange={(e) => handleChange('description', e.target.value)}
        />
      </div>

      <div css={formGroupStyles}>
        <div className="form-label">Git Options (optional)</div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '.5rem' }}>
            <input
              type="checkbox"
              checked={!!data.initialize_git}
              onChange={(e) => handleChange('initialize_git', e.target.checked)}
            />
            Initialize Git repository
          </label>
          <input
            id="git_repo_url"
            name="git_repo_url"
            type="text"
            placeholder="Git repository URL (optional)"
            value={data.git_repo_url || ''}
            onChange={(e) => handleChange('git_repo_url', e.target.value)}
            style={{ minWidth: '320px' }}
          />
        </div>
        <div className="hint">If provided, the PDF will include git init/remote commands.</div>
      </div>

      <div css={sectionStyles}>
        <h3>Backend Framework</h3>
        <p className="description">Choose your backend technology (or skip)</p>
        <div css={frameworkGridStyles}>
          {backendFrameworks.map((framework) => (
            <motion.div
              key={framework.id}
              css={frameworkCardStyles}
              className={data.backend_framework === framework.id ? 'selected' : ''}
              onClick={() => handleChange('backend_framework', framework.id === 'none' ? '' : framework.id)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <div className="icon">{framework.iconEl}</div>
              <div className="name">{framework.name}</div>
            </motion.div>
          ))}
        </div>
      </div>

      <div css={sectionStyles}>
        <h3>Frontend Framework</h3>
        <p className="description">Choose your frontend technology (or skip)</p>
        <div css={frameworkGridStyles}>
          {frontendFrameworks.map((framework) => (
            <motion.div
              key={framework.id}
              css={frameworkCardStyles}
              className={data.frontend_framework === framework.id ? 'selected' : ''}
              onClick={() => handleChange('frontend_framework', framework.id === 'none' ? '' : framework.id)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <div className="icon">{framework.iconEl}</div>
              <div className="name">{framework.name}</div>
            </motion.div>
          ))}
        </div>
      </div>

      {!data.backend_framework && !data.frontend_framework && (
        <motion.div
          css={css`
            padding: 1rem;
            background: rgba(237, 137, 54, 0.1);
            border: 1px solid rgba(237, 137, 54, 0.3);
            border-radius: 12px;
            color: var(--warning);
            text-align: center;
          `}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          ⚠️ Please select at least one framework (backend or frontend)
        </motion.div>
      )}
    </motion.div>
  )
}

export default StepProjectInfo
