/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react'
import { motion } from 'framer-motion'
import { FaRocket, FaCode, FaLayerGroup, FaGithub } from 'react-icons/fa'

const heroStyles = css`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 2rem 5rem; /* extra space for footer */
  text-align: center;
  position: relative;
  overflow: hidden;

  /* subtle gradient orbs */
  &::before, &::after {
    content: '';
    position: absolute;
    width: 60vmax; height: 60vmax;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.15;
    z-index: 0;
  }
  &::before { background: #667eea; top: -20vmax; left: -20vmax; }
  &::after { background: #764ba2; bottom: -25vmax; right: -25vmax; }
`

const titleStyles = css`
  font-size: clamp(3rem, 8vw, 6rem);
  font-weight: 900;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
`

const subtitleStyles = css`
  font-size: clamp(1.2rem, 3vw, 1.8rem);
  color: var(--text-muted);
  margin-bottom: 3rem;
  max-width: 700px;
  line-height: 1.6;
`

const buttonStyles = css`
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  color: white;
  border: none;
  padding: 1.2rem 3rem;
  font-size: 1.2rem;
  font-weight: 600;
  border-radius: 50px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  transition: all 0.3s ease;
  box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 50px rgba(102, 126, 234, 0.5);
  }
  
  &:active {
    transform: translateY(0);
  }
`

const featuresStyles = css`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 5rem;
  max-width: 1200px;
  width: 100%;
`

const featureCardStyles = css`
  background: rgba(26, 26, 46, 0.5);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  text-align: left;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    border-color: rgba(102, 126, 234, 0.5);
    background: rgba(26, 26, 46, 0.8);
  }
  
  .icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  h3 {
    font-size: 1.5rem;
    margin-bottom: 0.8rem;
    color: var(--text);
  }
  
  p {
    color: var(--text-muted);
    line-height: 1.6;
  }
`

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  },
  exit: {
    opacity: 0,
    y: -50,
    transition: { duration: 0.3 }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5 }
  }
}

const footerStyles = css`
  position: absolute;
  bottom: 16px;
  left: 0; right: 0;
  display: flex;
  justify-content: center;
  z-index: 1;
  color: var(--text-muted);
  font-size: 0.95rem;
  
  a { color: var(--primary); text-decoration: none; }
  a:hover { text-decoration: underline; }
`;

function Hero({ onStart }) {
  const features = [
    {
      icon: <FaRocket />,
      title: 'Fast Scaffolding',
      description: 'Generate complete project structures in seconds with customizable templates'
    },
    {
      icon: <FaCode />,
      title: 'Multi-Framework',
      description: 'Supports FastAPI, Flask, Django, Express, Nest.js, Bun, Spring Boot, Koa for backend and React, Vue, Angular, Nuxt, Svelte, Solid.Js for frontend'
    },
    {
      icon: <FaLayerGroup />,
      title: 'Smart Templates',
      description: 'Production-ready starter code with best practices and modern tooling, Includes DB integration'
    },
    {
      icon: <FaGithub />,
      title: 'Git Ready',
      description: 'Optional Git initialization with proper .gitignore and README generation'
    }
  ]

  return (
    <motion.div
      css={heroStyles}
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
    >
      <motion.h1 css={titleStyles} variants={itemVariants}>
        ProjectMaker
      </motion.h1>
      
      <motion.p css={subtitleStyles} variants={itemVariants}>
        The intelligent project scaffolding wizard that builds full-stack applications
        with backend and frontend structures, starter code, and dependencies—all without
        manually creating files.
      </motion.p>
      
      <motion.button
        css={buttonStyles}
        variants={itemVariants}
        onClick={onStart}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <FaRocket />
        Start Building
      </motion.button>
      
      <motion.div css={featuresStyles} variants={containerVariants}>
        {features.map((feature, index) => (
          <motion.div
            key={index}
            css={featureCardStyles}
            variants={itemVariants}
            whileHover={{ scale: 1.02 }}
          >
            <div className="icon">{feature.icon}</div>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </motion.div>
        ))}
      </motion.div>

      {/* Footer credits */}
      <div css={footerStyles}>
        <span>
          Generated with ProjectMaker ·
          {' '}<a href="https://github.com/SwagCode4U/projectmaker" target="_blank" rel="noreferrer">GitHub</a>
          {' '}· Contact:{' '}<a href="mailto:amit9000@tutanota.com">amit9000@tutanota.com</a>
        </span>
      </div>
    </motion.div>
  )
}

export default Hero
