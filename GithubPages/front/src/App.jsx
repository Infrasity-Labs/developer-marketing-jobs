import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import React from 'react';

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
                Architecture
              </NavLink>
              <a
                href="https://github.com/Infrasity-Labs/developer-marketing-jobs"
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2 bg-slate-100 text-slate-900 px-4 py-2 rounded-full hover:bg-white transition-all hover:scale-105 font-bold"
              >
                ⭐ Star Repo
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