import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import React from 'react';

const Github = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 .5C5.65.5.5 5.65.5 12a11.5 11.5 0 0 0 7.86 10.92c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.78 1.2 1.78 1.2 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.7 0-1.26.45-2.29 1.18-3.1-.12-.29-.51-1.46.11-3.04 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.79 0c2.21-1.49 3.18-1.18 3.18-1.18.62 1.58.23 2.75.11 3.04.74.81 1.18 1.84 1.18 3.1 0 4.43-2.69 5.4-5.25 5.69.41.36.78 1.07.78 2.16v3.2c0 .31.21.67.8.56A11.5 11.5 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5z"/>
  </svg>
);

function App() {
  // Helper function for active navigation links
  const navLinkClass = ({ isActive }) =>
    `transition-colors font-medium ${
      isActive ? 'text-indigo-400' : 'text-slate-300 hover:text-indigo-300'
    }`;

  return (
    <Router>
      {/* Added flex flex-col to keep the footer at the bottom */}
      <div className="flex flex-col min-h-screen bg-slate-950 text-slate-50 font-sans selection:bg-indigo-500/30">
        
        <nav className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
            <NavLink to="/" className="text-xl font-bold tracking-tight flex items-center gap-2">
              <span className="text-indigo-400">Dev</span>Jobs
            </NavLink>
            <div className="flex gap-6 items-center text-sm">
              <NavLink to="/" className={navLinkClass}>
                Home
              </NavLink>
              <NavLink to="/about" className={navLinkClass}>
                WorkFlow
              </NavLink>
              <a
                href="https://github.com/Infrasity-Labs/developer-marketing-jobs"
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2 bg-slate-100 text-slate-900 px-4 py-2 rounded-full hover:bg-white transition-all hover:scale-105 font-bold"
              >
                <Github size={16} />
                Star Repo
              </a>
            </div>
          </div>
        </nav>

        {/* Main content area expands to fill available space */}
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>

        <footer className="border-t border-slate-800 py-12 text-center text-slate-400 mt-auto">
          <p>100% Open Source under the MIT License.</p>
          <div className="mt-4 flex justify-center gap-4 text-sm">
            <a 
              href="https://github.com/Infrasity-Labs" 
              target="_blank" 
              rel="noreferrer"
              className="hover:text-indigo-400 transition-colors"
            >
              Built by Infrasity-Labs
            </a>
            <span>•</span>
            <a 
              href="https://github.com/Infrasity-Labs/developer-marketing-jobs" 
              target="_blank" 
              rel="noreferrer"
              className="hover:text-indigo-400 transition-colors"
            >
              GitHub Repository
            </a>
          </div>
        </footer>
        
      </div>
    </Router>
  );
}

export default App;