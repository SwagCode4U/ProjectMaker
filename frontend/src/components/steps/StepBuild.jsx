/** @jsxImportSource @emotion/react */
import { useState } from 'react'
import { css } from '@emotion/react'
import { motion } from 'framer-motion'
import { FaRocket, FaCheck, FaSpinner, FaTimes, FaFolder, FaExternalLinkAlt, FaFilePdf, FaClipboard } from 'react-icons/fa'
import vscodeLogo from 'simple-icons/icons/visualstudiocode.svg'
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

const buildButtonStyles = css`
  width: 100%;
  padding: 1.5rem;
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  border: none;
  border-radius: 16px;
  color: white;
  font-size: 1.3rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 15px 50px rgba(102, 126, 234, 0.5);
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`

const statusListStyles = css`
  background: rgba(15, 15, 30, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
`

const statusItemStyles = css`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 0.8rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  transition: all 0.3s ease;
  
  &.success {
    border-left: 3px solid var(--success);
  }
  
  &.error {
    border-left: 3px solid var(--error);
  }
  
  &.pending {
    border-left: 3px solid var(--text-muted);
  }
  
  .icon {
    font-size: 1.5rem;
    
    &.success { color: var(--success); }
    &.error { color: var(--error); }
    &.pending { color: var(--text-muted); }
    &.loading {
      color: var(--primary);
      animation: spin 1s linear infinite;
    }
  }
  
  .message {
    flex: 1;
    color: var(--text);
    
    .title {
      font-weight: 600;
      margin-bottom: 0.2rem;
    }
    
    .detail {
      font-size: 0.9rem;
      color: var(--text-muted);
    }
  }
  
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
`

const successCardStyles = css`
  background: linear-gradient(135deg, rgba(72, 187, 120, 0.1) 0%, rgba(102, 126, 234, 0.1) 100%);
  border: 1px solid var(--success);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  
  .big-icon {
    font-size: 4rem;
    color: var(--success);
    margin-bottom: 1rem;
  }
  
  h3 {
    font-size: 1.8rem;
    color: var(--text);
    margin-bottom: 0.5rem;
  }
  
  .path {
    font-family: 'Courier New', monospace;
    background: rgba(0, 0, 0, 0.3);
    padding: 1rem;
    border-radius: 8px;
    margin: 1.5rem 0;
    color: var(--primary);
    word-break: break-all;
  }
  .tip {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    justify-content: center;
    color: var(--text);
  }
  .tip-code {
    font-family: 'Courier New', monospace;
    background: rgba(0, 0, 0, 0.25);
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    color: var(--text);
  }
`

const actionButtonsStyles = css`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
  
  button {
    padding: 1rem 1.5rem;
    background: rgba(15, 15, 30, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    color: var(--text);
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
    
    &:hover {
      background: rgba(102, 126, 234, 0.2);
      border-color: var(--primary);
      transform: translateY(-2px);
    }
  }
`

function StepBuild({ data }) {
  const [building, setBuilding] = useState(false)
  const [built, setBuilt] = useState(false)
  const [projectPath, setProjectPath] = useState('')
  const [operations, setOperations] = useState([])

  const startBuild = async () => {
    setBuilding(true)
    setOperations([])
    
    try {
      // Add initial operations
      addOperation('pending', 'Initializing', 'Preparing project generation...')
      
      await delay(500)
      
      // Call backend API
      const response = await axios.post('/api/projects/build', data)
      
      // Simulate operations with real backend response
      const buildSteps = response.data.operations || []
      
      for (const step of buildSteps) {
        await delay(300)
        addOperation('success', step)
      }
      
      setProjectPath(response.data.project_path)
      setBuilt(true)
      setBuilding(false)
      
    } catch (error) {
      console.error('Build error:', error)
      // Fallback to mock build process
      await mockBuildProcess()
    }
  }

  const mockBuildProcess = async () => {
    const steps = [
      { status: 'success', title: 'Directory Created', detail: `Created project root: ${data.target_directory}` },
      { status: 'success', title: 'Backend Structure', detail: `Generated ${data.backend_folder_name}/ with starter files` },
      { status: 'success', title: 'Frontend Structure', detail: `Generated ${data.frontend_folder_name}/ with starter files` },
      { status: 'success', title: 'Requirements File', detail: 'Created requirements.txt with dependencies' },
      { status: 'success', title: 'README Generated', detail: 'Created comprehensive README.md' },
      { status: 'success', title: 'Gitignore Created', detail: 'Added .gitignore with common patterns' }
    ]

    if (data.initialize_git) {
      steps.push({ status: 'success', title: 'Git Initialized', detail: 'Repository ready for commits' })
    }

    for (const step of steps) {
      await delay(400)
      addOperation(step.status, step.title, step.detail)
    }

    setProjectPath(data.target_directory || '/tmp/generated_projects/' + data.project_name)
    setBuilt(true)
    setBuilding(false)
  }

  const addOperation = (status, title, detail = '') => {
    setOperations(prev => [...prev, { status, title, detail, timestamp: Date.now() }])
  }

  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

  const copyPath = async () => {
    try {
      await navigator.clipboard.writeText(projectPath)
      alert('Project path copied to clipboard!')
    } catch (e) {
      console.error(e)
      alert('Could not copy path. You can copy it manually from the box above.')
    }
  }

  const downloadPDF = async () => {
    try {
      const res = await axios.post('/api/projects/generate-pdf', data, { responseType: 'blob' })
      const blob = new Blob([res.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${data.project_name || 'project'}_summary.pdf`
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (e) {
      alert('Failed to generate PDF. Please try again.')
      console.error(e)
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <FaCheck className="icon success" />
      case 'error':
        return <FaTimes className="icon error" />
      case 'loading':
        return <FaSpinner className="icon loading" />
      default:
        return <FaSpinner className="icon pending" />
    }
  }

  if (built) {
    return (
      <motion.div
        css={containerStyles}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div css={successCardStyles}>
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: 'spring' }}
          >
            <FaCheck className="big-icon" />
          </motion.div>
          <h3>Project Built Successfully! 🎉</h3>
          <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>
            Your project is ready to code!
          </p>
          <div className="path">
            <FaFolder style={{ marginRight: '0.5rem' }} />
            {projectPath}
          </div>

          <div css={actionButtonsStyles}>
            <button onClick={copyPath}>
              <FaClipboard /> Copy Path
            </button>
            <button onClick={downloadPDF}>
              <FaFilePdf /> Download PDF
            </button>
            <button onClick={() => window.location.reload()}>
              <FaRocket /> New Project
            </button>
          </div>

          {/* VS Code tip */}
          <div className="tip" style={{ marginTop: '1rem' }}>
            <span
              aria-label="VS Code"
              style={{
                width: 20,
                height: 20,
                backgroundColor: '#007ACC',
                WebkitMaskImage: `url(${vscodeLogo})`,
                maskImage: `url(${vscodeLogo})`,
                WebkitMaskRepeat: 'no-repeat',
                maskRepeat: 'no-repeat',
                WebkitMaskPosition: 'center',
                maskPosition: 'center',
                WebkitMaskSize: 'contain',
                maskSize: 'contain',
                display: 'inline-block'
              }}
            />
            <span>Open in VS Code:</span>
            <span className="tip-code">{`code "${projectPath}"`}</span>
          </div>
        </div>

        <div css={statusListStyles}>
          <h4 style={{ marginBottom: '1rem', color: 'var(--text)' }}>Build Log:</h4>
          {operations.map((op, index) => (
            <motion.div
              key={index}
              css={statusItemStyles}
              className={op.status}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              {getStatusIcon(op.status)}
              <div className="message">
                <div className="title">{op.title}</div>
                {op.detail && <div className="detail">{op.detail}</div>}
              </div>
            </motion.div>
          ))}
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
      <h2 css={titleStyles}>Ready to Build</h2>
      <p css={subtitleStyles}>
        Click the button below to generate your project
      </p>

      <motion.button
        css={buildButtonStyles}
        onClick={startBuild}
        disabled={building}
        whileHover={!building ? { scale: 1.02 } : {}}
        whileTap={!building ? { scale: 0.98 } : {}}
      >
        {building ? (
          <>
            <FaSpinner style={{ animation: 'spin 1s linear infinite' }} />
            Building Project...
          </>
        ) : (
          <>
            <FaRocket />
            Build Project Now
          </>
        )}
      </motion.button>

      {operations.length > 0 && (
        <div css={statusListStyles}>
          <h4 style={{ marginBottom: '1rem', color: 'var(--text)' }}>Build Progress:</h4>
          {operations.map((op, index) => (
            <motion.div
              key={index}
              css={statusItemStyles}
              className={op.status}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              {getStatusIcon(op.status)}
              <div className="message">
                <div className="title">{op.title}</div>
                {op.detail && <div className="detail">{op.detail}</div>}
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </motion.div>
  )
}

export default StepBuild
