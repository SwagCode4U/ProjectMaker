/** @jsxImportSource @emotion/react */
import { useState } from 'react'
import { css } from '@emotion/react'
import { motion } from 'framer-motion'
import { FaFolder, FaPlus, FaTimes, FaGit, FaApple, FaLinux, FaWindows } from 'react-icons/fa'
import { SiMysql, SiPostgresql, SiMongodb } from 'react-icons/si'
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
  
  input {
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
  }
`

const folderListStyles = css`
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  margin-top: 1rem;
`

const folderTagStyles = css`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 50px;
  color: var(--text);
  font-size: 0.9rem;
  
  .icon {
    color: var(--primary);
  }
  
  button {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
    transition: color 0.2s;
    
    &:hover {
      color: var(--error);
    }
  }
`

const addFolderStyles = css`
  display: flex;
  gap: 0.8rem;
  margin-top: 1rem;
  
  input {
    flex: 1;
  }
  
  button {
    padding: 1rem 1.5rem;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }
  }
`

const osGridStyles = css`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1rem;
`

const osCardStyles = css`
  background: rgba(15, 15, 30, 0.6);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  
  &:hover {
    transform: translateY(-4px);
    border-color: rgba(102, 126, 234, 0.5);
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
  }
`

const toggleStyles = css`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.2rem;
  background: rgba(15, 15, 30, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(15, 15, 30, 0.8);
    border-color: rgba(102, 126, 234, 0.3);
  }
  
  .switch {
    position: relative;
    width: 50px;
    height: 26px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50px;
    transition: all 0.3s ease;
    
    &.active {
      background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    }
    
    .slider {
      position: absolute;
      top: 3px;
      left: 3px;
      width: 20px;
      height: 20px;
      background: white;
      border-radius: 50%;
      transition: all 0.3s ease;
      
      &.active {
        transform: translateX(24px);
      }
    }
  }
  
  .label {
    flex: 1;
    
    .title {
      font-weight: 600;
      color: var(--text);
      margin-bottom: 0.2rem;
    }
    
    .description {
      font-size: 0.9rem;
      color: var(--text-muted);
    }
  }
`

function ConfirmTargetDir({ data, updateData }) {
  const [confirmed, setConfirmed] = useState(!!data.step2_dir_confirmed)
  const onConfirm = () => {
    setConfirmed(true)
    updateData({ step2_dir_confirmed: true })
  }
  return (
    <>
      {!confirmed ? (
        <button
          onClick={onConfirm}
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
}

function StepCustomization({ data, updateData }) {
  const [newFolder, setNewFolder] = useState('')
  const [targetOS, setTargetOS] = useState('linux')
  const [dbScript, setDbScript] = useState(null)
  const [dbTablesInput, setDbTablesInput] = useState((data.database_tables || []).join(', '))

  const handleChange = (field, value) => {
    updateData({ [field]: value })
  }

  const handleDbGenerate = async () => {
    try {
      const payload = {
        ...data,
        database_tables: dbTablesInput
          .split(',')
          .map(s => s.trim())
          .filter(Boolean),
      }
      const res = await axios.post('/api/projects/generate-db-script', payload)
      setDbScript(res.data)
      // persist parsed tables to wizard data
      updateData({ database_tables: payload.database_tables })
    } catch (e) {
      console.error(e)
      alert('Failed to generate DB script. Check inputs and try again.')
    }
  }

  const downloadDbTxt = () => {
    if (!dbScript) return
    const content = `Database: ${dbScript.database}\n\nRationale:\n${dbScript.rationale}\n\n-- Script --\n${dbScript.script}\n\n-- Node.js Example --\n${dbScript.node_example}\n\n-- .env --\n${dbScript.env}\n\nHow to run: ${dbScript.how_to_run}\n`
    const blob = new Blob([content], { type: 'text/plain' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${data.project_name || 'project'}_${data.database_type || 'db'}_setup.txt`
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  }

  const addFolder = () => {
    if (newFolder.trim() && !data.custom_folders.includes(newFolder.trim())) {
      handleChange('custom_folders', [...data.custom_folders, newFolder.trim()])
      setNewFolder('')
    }
  }


  const removeFolder = (folder) => {
    handleChange('custom_folders', data.custom_folders.filter(f => f !== folder))
  }

  const operatingSystems = [
    { id: 'linux', name: 'Linux', icon: <FaLinux /> },
    { id: 'mac', name: 'macOS', icon: <FaApple /> },
    { id: 'windows', name: 'Windows', icon: <FaWindows /> }
  ]

  return (
    <motion.div
      css={containerStyles}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <h2 css={titleStyles}>Customize Structure</h2>
      <p css={subtitleStyles}>
        Fine-tune your project directories and settings
      </p>

      <div css={formGroupStyles}>
        <div className="form-label">Target Operating System</div>
        <div css={osGridStyles}>
          {operatingSystems.map((os) => (
            <motion.div
              key={os.id}
              css={osCardStyles}
              className={targetOS === os.id ? 'selected' : ''}
              onClick={() => setTargetOS(os.id)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <div className="icon">{os.icon}</div>
              <div className="name">{os.name}</div>
            </motion.div>
          ))}
        </div>
      </div>

      <div css={formGroupStyles}>
        <div className="form-label">Target Directory</div>
        <div
          css={css`
            padding: 0.9rem 1rem;
            background: rgba(15,15,30,0.8);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            display:flex; align-items:center; justify-content:space-between; gap:1rem;
          `}
        >
          <span><FaFolder style={{ marginRight: '.5rem' }} /> <code>{data.target_directory || 'Not set'}</code></span>
          <ConfirmTargetDir data={data} updateData={updateData} />
        </div>
        <div className="hint">This is carried over from Step 1. Confirm below to proceed.</div>
      </div>

      {data.backend_framework && (
        <div css={formGroupStyles}>
          <label htmlFor="backend_folder">Backend Folder Name</label>
          <input
            id="backend_folder"
            type="text"
            placeholder="backend"
            value={data.backend_folder_name}
            onChange={(e) => handleChange('backend_folder_name', e.target.value)}
          />
        </div>
      )}

      {data.frontend_framework && (
        <div css={formGroupStyles}>
          <label htmlFor="frontend_folder">Frontend Folder Name</label>
          <input
            id="frontend_folder"
            type="text"
            placeholder="frontend"
            value={data.frontend_folder_name}
            onChange={(e) => handleChange('frontend_folder_name', e.target.value)}
          />
        </div>
      )}

      <div css={formGroupStyles}>
        <div className="form-label">Additional Folders</div>
        <div css={folderListStyles}>
          {data.custom_folders.map((folder, index) => (
            <motion.div
              key={index}
              css={folderTagStyles}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
            >
              <FaFolder className="icon" />
              <span>{folder}</span>
              <button onClick={() => removeFolder(folder)}>
                <FaTimes />
              </button>
            </motion.div>
          ))}
        </div>
        
        <div css={addFolderStyles}>
          <input
            type="text"
            placeholder="Add custom folder (e.g., scripts, config)"
            value={newFolder}
            onChange={(e) => setNewFolder(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addFolder()}
          />
          <button onClick={addFolder} disabled={!newFolder.trim()}>
            <FaPlus /> Add Folder
          </button>
        </div>
      </div>

      <div css={formGroupStyles}>
        <div className="form-label">Database (optional)</div>
        <div css={osGridStyles}>
          {[{ id: 'mysql', name: 'MySQL', icon: <SiMysql /> }, { id: 'postgresql', name: 'PostgreSQL', icon: <SiPostgresql /> }, { id: 'mongodb', name: 'MongoDB', icon: <SiMongodb /> }].map(db => (
            <motion.div
              key={db.id}
              css={osCardStyles}
              className={data.database_type === db.id ? 'selected' : ''}
              onClick={() => handleChange('database_type', db.id)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <div className="icon">{db.icon}</div>
              <div className="name">{db.name}</div>
            </motion.div>
          ))}
        </div>
      </div>

      {data.database_type && (
        <div css={formGroupStyles}>
          <div className="form-label">Database Details</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.8rem' }}>
            <input
              id="db_name"
              name="database_name"
              type="text"
              placeholder="DB Name"
              value={data.database_name || ''}
              onChange={(e) => handleChange('database_name', e.target.value)}
            />
            <input
              id="db_user"
              name="database_user"
              type="text"
              placeholder="Username"
              value={data.database_user || ''}
              onChange={(e) => handleChange('database_user', e.target.value)}
            />
            <input
              id="db_password"
              name="database_password"
              type="password"
              placeholder="Password"
              value={data.database_password || ''}
              onChange={(e) => handleChange('database_password', e.target.value)}
            />
          </div>
          <div style={{ marginTop: '0.8rem' }}>
            <input
              id="db_tables"
              name="database_tables"
              type="text"
              placeholder="Tables/Collections (comma-separated, e.g., users, orders)"
              value={dbTablesInput}
              onChange={(e) => setDbTablesInput(e.target.value)}
              onBlur={() => updateData({ database_tables: dbTablesInput.split(',').map(s => s.trim()).filter(Boolean) })}
            />
          </div>
          <div style={{ display: 'flex', gap: '0.8rem', marginTop: '0.8rem' }}>
            <button onClick={handleDbGenerate} style={{ padding: '0.8rem 1.2rem', borderRadius: 8, border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(15,15,30,0.8)', color: 'var(--text)', cursor: 'pointer' }}>
              Generate DB Script
            </button>
            {dbScript && (
              <>
                <button onClick={downloadDbTxt} style={{ padding: '0.8rem 1.2rem', borderRadius: 8, border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(15,15,30,0.8)', color: 'var(--text)', cursor: 'pointer' }}>
                  Download as .txt
                </button>
                <button onClick={() => handleChange('open_schema_designer', true)} style={{ padding: '0.8rem 1.2rem', borderRadius: 8, border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(15,15,30,0.8)', color: 'var(--text)', cursor: 'pointer' }}>
                  Design Columns
                </button>
              </>
            )}
          </div>
          {dbScript && !data.open_schema_designer && (
            <div style={{ marginTop: '1rem', display: 'grid', gap: '1rem' }}>
              <div css={folderListStyles} style={{ display: 'block' }}>
                <div style={{ color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Rationale</div>
                <pre css={css`white-space: pre-wrap; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px;`}>
                  {dbScript.rationale}
                </pre>
              </div>
              <div>
                <div style={{ color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Script</div>
                <pre css={css`white-space: pre-wrap; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; overflow: auto; maxHeight: 280px;`}>
{dbScript.script}
                </pre>
              </div>
              <div>
                <div style={{ color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Node.js Example</div>
                <pre css={css`white-space: pre-wrap; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; overflow: auto; maxHeight: 280px;`}>
{dbScript.node_example}
                </pre>
              </div>
              <div>
                <div style={{ color: 'var(--text-muted)', marginBottom: '0.5rem' }}>.env</div>
                <pre css={css`white-space: pre-wrap; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px;`}>
{dbScript.env}
                </pre>
              </div>
            </div>
          )}

          {dbScript && data.open_schema_designer && (
            <SchemaDesigner data={data} updateData={updateData} />
          )}
        </div>
      )}

      <div css={formGroupStyles}>
        <div className="form-label">Optional Features</div>
        
        <motion.div
          css={toggleStyles}
          onClick={() => handleChange('initialize_git', !data.initialize_git)}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <div className={`switch ${data.initialize_git ? 'active' : ''}`}>
            <div className={`slider ${data.initialize_git ? 'active' : ''}`} />
          </div>
          <div className="label">
            <div className="title">
              <FaGit style={{ marginRight: '0.5rem' }} />
              Initialize Git Repository
            </div>
            <div className="description">
              Creates .git, .gitignore, and prepares for version control
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  )
}

function SchemaDesigner({ data, updateData }) {
  const [tableName, setTableName] = useState((data.database_tables && data.database_tables[0]) || '')
  const [columns, setColumns] = useState([])
  const [script, setScript] = useState('')

  const addCol = () => setColumns([...columns, { name: '', type: 'string', length: '', default: '', nullable: true, auto_increment: false, unique: false, index: false, values: '' }])
  const removeCol = (i) => setColumns(columns.filter((_, idx) => idx !== i))
  const setCol = (i, key, val) => setColumns(columns.map((c, idx) => idx === i ? { ...c, [key]: val } : c))

  const build = async () => {
    try {
      const cols = columns.map(c => ({
        name: c.name,
        type: c.type,
        length: c.length ? Number(c.length) : undefined,
        default: c.default || undefined,
        nullable: !!c.nullable,
        auto_increment: !!c.auto_increment,
        unique: !!c.unique,
        index: !!c.index,
        values: (c.type === 'enum' && c.values) ? c.values.split(',').map(s => s.trim()).filter(Boolean) : undefined
      }))
      const payload = {
        database_type: data.database_type,
        database_name: data.database_name || (data.project_name || 'mydb').toLowerCase().replace(/\s+/g, '_'),
        table_name: tableName || 'my_table',
        columns: cols
      }
      const res = await axios.post('/api/projects/generate-schema', payload)
      setScript(res.data.script)
    } catch (e) {
      console.error(e)
      alert('Failed to build schema')
    }
  }

  const download = () => {
    const blob = new Blob([script], { type: 'text/plain' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${data.project_name || 'project'}_${tableName || 'table'}_schema.txt`
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div style={{ marginTop: '1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.8rem' }}>
        <strong style={{ color: 'var(--text)' }}>Schema Designer</strong>
        <button onClick={() => updateData({ open_schema_designer: false })} style={{ padding: '0.4rem 0.8rem', borderRadius: 8, border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(15,15,30,0.8)', color: 'var(--text)', cursor: 'pointer' }}>Close</button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.8rem', marginBottom: '0.8rem' }}>
        <input name="table_name" type="text" placeholder="Table name" value={tableName} onChange={(e) => setTableName(e.target.value)} />
        <select name="database_type" value={data.database_type || 'mysql'} onChange={(e) => updateData({ database_type: e.target.value })}>
          <option value="mysql">MySQL</option>
          <option value="postgresql">PostgreSQL</option>
          <option value="mongodb">MongoDB</option>
        </select>
        <button onClick={addCol} style={{ padding: '0.8rem 1.2rem', borderRadius: 8, border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(15,15,30,0.8)', color: 'var(--text)', cursor: 'pointer' }}>Add Column</button>
      </div>
      {columns.map((c, i) => (
        <div key={i} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '0.6rem', marginBottom: '0.6rem' }}>
          <input name={`col_${i}_name`} placeholder="name" value={c.name} onChange={(e) => setCol(i, 'name', e.target.value)} />
          <select name={`col_${i}_type`} value={c.type} onChange={(e) => setCol(i, 'type', e.target.value)}>
            <option value="string">string</option>
            <option value="text">text</option>
            <option value="int">int</option>
            <option value="decimal">decimal</option>
            <option value="boolean">boolean</option>
            <option value="datetime">datetime</option>
            <option value="enum">enum</option>
          </select>
          <input name={`col_${i}_length`} placeholder="length/precision" value={c.length} onChange={(e) => setCol(i, 'length', e.target.value)} />
          <input name={`col_${i}_default`} placeholder="default" value={c.default} onChange={(e) => setCol(i, 'default', e.target.value)} />
          <input name={`col_${i}_values`} placeholder="enum values (a,b,c)" value={c.values} onChange={(e) => setCol(i, 'values', e.target.value)} />
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}><input name={`col_${i}_nullable`} type="checkbox" checked={!!c.nullable} onChange={(e) => setCol(i, 'nullable', e.target.checked)} /> nullable</label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}><input name={`col_${i}_auto_increment`} type="checkbox" checked={!!c.auto_increment} onChange={(e) => setCol(i, 'auto_increment', e.target.checked)} /> auto inc</label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}><input name={`col_${i}_unique`} type="checkbox" checked={!!c.unique} onChange={(e) => setCol(i, 'unique', e.target.checked)} /> unique</label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}><input name={`col_${i}_index`} type="checkbox" checked={!!c.index} onChange={(e) => setCol(i, 'index', e.target.checked)} /> index</label>
          <button onClick={() => removeCol(i)} style={{ padding: '0.4rem 0.8rem', borderRadius: 8, border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(15,15,30,0.8)', color: 'var(--text)', cursor: 'pointer' }}>Remove</button>
        </div>
      ))}
      <div style={{ display: 'flex', gap: '0.8rem', marginTop: '0.8rem' }}>
        <button onClick={build} style={{ padding: '0.8rem 1.2rem', borderRadius: 8, border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(15,15,30,0.8)', color: 'var(--text)', cursor: 'pointer' }}>Build Schema</button>
        {script && <button onClick={download} style={{ padding: '0.8rem 1.2rem', borderRadius: 8, border: '1px solid rgba(255,255,255,0.2)', background: 'rgba(15,15,30,0.8)', color: 'var(--text)', cursor: 'pointer' }}>Download .txt</button>}
      </div>
      {script && (
        <pre css={css`white-space: pre-wrap; background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; margin-top: 1rem; max-height: 360px; overflow: auto;`}>{script}</pre>
      )}
    </div>
  )
}

export default StepCustomization
