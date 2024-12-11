import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import AboutHeader from './AboutHeader.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AboutHeader/>
    <App />
  </StrictMode>,
)
