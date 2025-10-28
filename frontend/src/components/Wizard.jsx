/** @jsxImportSource @emotion/react */
import { useState } from 'react'
import { css } from '@emotion/react'
import { motion, AnimatePresence } from 'framer-motion'
import { FaArrowLeft, FaArrowRight, FaCheck } from 'react-icons/fa'
import StepProjectInfo from './steps/StepProjectInfo'
import StepCustomization from './steps/StepCustomization'
import StepPreview from './steps/StepPreview'
import StepBuild from './steps/StepBuild'

const wizardStyles = css`
  min-height: 100vh;
  padding: 2rem;
`

const headerStyles = css`
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto 3rem;
`

const backButtonStyles = css`
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--text);
  padding: 0.8rem 1.5rem;
  border-radius: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: var(--primary);
  }
`

const progressStyles = css`
  max-width: 1200px;
  margin: 0 auto 3rem;
  
  .steps {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    
    &::before {
      content: '';
      position: absolute;
      top: 20px;
      left: 0;
      right: 0;
      height: 2px;
      background: rgba(255, 255, 255, 0.1);
      z-index: 0;
    }
  }
  
  .step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.8rem;
    position: relative;
    z-index: 1;
    flex: 1;
    
    .circle {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: rgba(26, 26, 46, 0.8);
      border: 2px solid rgba(255, 255, 255, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      transition: all 0.3s ease;
      
      &.active {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border-color: transparent;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
      }
      
      &.completed {
        background: var(--success);
        border-color: transparent;
      }
    }
    
    .label {
      font-size: 0.9rem;
      color: var(--text-muted);
      
      &.active {
        color: var(--text);
        font-weight: 600;
      }
    }
  }
`

const contentStyles = css`
  max-width: 1200px;
  margin: 0 auto;
`

const navigationStyles = css`
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 3rem auto 0;
  gap: 1rem;
`

const buttonStyles = css`
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  transition: all 0.3s ease;
  border: none;
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`

const prevButtonStyles = css`
  ${buttonStyles}
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--text);
  
  &:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.05);
    border-color: var(--primary);
  }
`

const nextButtonStyles = css`
  ${buttonStyles}
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  color: white;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
  }
`

const steps = [
  { id: 1, label: 'Project Info', component: StepProjectInfo },
  { id: 2, label: 'Customization', component: StepCustomization },
  { id: 3, label: 'Preview', component: StepPreview },
  { id: 4, label: 'Build', component: StepBuild }
]

function Wizard({ onBack }) {
  const [currentStep, setCurrentStep] = useState(1)
  const [projectData, setProjectData] = useState({
    project_name: '',
    description: '',
    backend_framework: '',
    frontend_framework: '',
    backend_folder_name: 'backend',
    frontend_folder_name: 'frontend',
    custom_folders: ['docs', 'tests'],
    custom_files: [],
    initialize_git: true,
    target_directory: '',
    step2_dir_confirmed: false,
    database_type: '',
    database_name: '',
    database_user: '',
    database_password: '',
    database_tables: []
  })

  const CurrentStepComponent = steps.find(s => s.id === currentStep)?.component

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrev = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const updateProjectData = (data) => {
    setProjectData(prev => ({ ...prev, ...data }))
  }

  const isStepValid = () => {
    if (currentStep === 1) {
      return projectData.project_name && projectData.description && (projectData.backend_framework || projectData.frontend_framework) && projectData.target_directory
    }
    if (currentStep === 2) {
      return Boolean(projectData.target_directory && projectData.step2_dir_confirmed)
    }
    return true
  }

  return (
    <motion.div
      css={wizardStyles}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
    >
      <div css={headerStyles}>
        <button css={backButtonStyles} onClick={onBack}>
          <FaArrowLeft /> Back to Home
        </button>
      </div>

      <div css={progressStyles}>
        <div className="steps">
          {steps.map((step) => (
            <div key={step.id} className="step">
              <motion.div
                className={`circle ${currentStep === step.id ? 'active' : ''} ${
                  currentStep > step.id ? 'completed' : ''
                }`}
                whileHover={{ scale: 1.1 }}
              >
                {currentStep > step.id ? <FaCheck /> : step.id}
              </motion.div>
              <span
                className={`label ${currentStep === step.id ? 'active' : ''}`}
              >
                {step.label}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div css={contentStyles}>
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            <CurrentStepComponent
              data={projectData}
              updateData={updateProjectData}
              onNext={handleNext}
            />
          </motion.div>
        </AnimatePresence>
      </div>

      {currentStep < steps.length && (
        <div css={navigationStyles}>
          <button
            css={prevButtonStyles}
            onClick={handlePrev}
            disabled={currentStep === 1}
          >
            <FaArrowLeft /> Previous
          </button>
          <button
            css={nextButtonStyles}
            onClick={handleNext}
            disabled={!isStepValid()}
          >
            Next <FaArrowRight />
          </button>
        </div>
      )}
    </motion.div>
  )
}

export default Wizard
