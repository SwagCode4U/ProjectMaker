/** @jsxImportSource @emotion/react */
import { useState } from 'react'
import { css } from '@emotion/react'
import { motion, AnimatePresence } from 'framer-motion'
import Wizard from './components/Wizard'
import Hero from './components/Hero'

const appStyles = css`
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  
  /* Animated background */
  background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 50%, #16213e 100%);
  
  &::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 40% 20%, rgba(240, 147, 251, 0.05) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
  }
`

const containerStyles = css`
  position: relative;
  z-index: 1;
`

function App() {
  const [showWizard, setShowWizard] = useState(false)

  return (
    <div css={appStyles}>
      <div css={containerStyles}>
        <AnimatePresence mode="wait">
          {!showWizard ? (
            <Hero key="hero" onStart={() => setShowWizard(true)} />
          ) : (
            <Wizard key="wizard" onBack={() => setShowWizard(false)} />
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default App
