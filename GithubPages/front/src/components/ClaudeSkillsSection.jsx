import { motion } from 'framer-motion';
import { Bot, CheckCircle2, Terminal } from 'lucide-react';

export default function ClaudeSkillsSection() {
  const textVariants = {
    hidden: { opacity: 0, x: -30 },
    visible: { 
      opacity: 1, 
      x: 0, 
      transition: { duration: 0.6, staggerChildren: 0.15 } 
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  // Sped up the terminal stagger from 0.5 to 0.1 so it appears much faster
  const terminalVariants = {
    hidden: { opacity: 0, x: 30, scale: 0.95 },
    visible: { 
      opacity: 1, 
      x: 0, 
      scale: 1,
      transition: { duration: 0.6, delayChildren: 0.2, staggerChildren: 0.1 } 
    }
  };

  const lineVariants = {
    hidden: { opacity: 0, x: -10 },
    visible: { opacity: 1, x: 0 }
  };

  return (
    <section className="w-full max-w-6xl mx-auto px-6 py-32 relative">
      
      <div className="absolute top-1/2 right-0 -translate-y-1/2 w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-[120px] pointer-events-none"></div>

      <div className="flex flex-col lg:flex-row gap-16 items-center">
        
        {/* LEFT SIDE */}
        <motion.div 
          className="flex-1"
          variants={textVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
        >
          <motion.h2 
            variants={itemVariants}
            className="font-quicksand text-4xl font-bold mb-6 flex items-center gap-4 text-white"
          >
        
            Powered by Claude Code
          </motion.h2>
          
          <motion.p 
            variants={itemVariants}
            className="font-inter text-slate-400 mb-8 text-lg leading-relaxed"
          >
            We leverage <span className="text-slate-200 font-medium">Claude Code CLI</span> as executable markdown skills to maintain the repository automatically. 
            Running in an isolated subprocess ensures exact context boundaries and prevents accidental file modifications.
          </motion.p>
          
          <ul className="space-y-6">
            <motion.li variants={itemVariants} className="flex gap-4 items-start group">
              <div className="mt-1 bg-slate-900 border border-slate-700 rounded-full p-1 group-hover:border-indigo-500/50 transition-colors">
                <CheckCircle2 className="text-indigo-400" size={18}/>
              </div>
              <div>
                <strong className="font-quicksand block text-lg text-slate-200 mb-1 group-hover:text-indigo-300 transition-colors">keyword_expander.py</strong>
                <span className="font-inter text-slate-400 text-sm leading-relaxed">Expands hardcoded dev-tools categories from 10 to 30+ semantic keywords using AI context.</span>
              </div>
            </motion.li>
            
            <motion.li variants={itemVariants} className="flex gap-4 items-start group">
              <div className="mt-1 bg-slate-900 border border-slate-700 rounded-full p-1 group-hover:border-indigo-500/50 transition-colors">
                <CheckCircle2 className="text-indigo-400" size={18}/>
              </div>
              <div>
                <strong className="font-quicksand block text-lg text-slate-200 mb-1 group-hover:text-indigo-300 transition-colors">expand-greenhouse-companies.md</strong>
                <span className="font-inter text-slate-400 text-sm leading-relaxed">Auto-discovers new Greenhouse ATS URLs and updates our Python scraper configurations autonomously.</span>
              </div>
            </motion.li>
          </ul>
        </motion.div>

        {/* RIGHT SIDE: Animated Terminal Window */}
        <motion.div 
          variants={terminalVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="flex-1 w-full relative group"
        >
          <div className="absolute inset-0 bg-indigo-500/20 blur-2xl rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

          <div className="relative bg-[#0d1117] border border-slate-700/60 rounded-2xl p-6 shadow-2xl backdrop-blur-md overflow-hidden">
            
            {/* Mac Window Controls */}
            <div className="flex items-center gap-2 mb-6 pb-4 border-b border-slate-800/60">
              <div className="w-3 h-3 rounded-full bg-rose-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-amber-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-emerald-500/80"></div>
              <div className="ml-4 flex items-center gap-2 text-slate-500 font-mono text-xs font-medium">
                <Terminal size={14} />
                claude-cli — bash
              </div>
            </div>

            {/* Terminal Output Lines */}
            <div className="font-mono text-sm space-y-2">
              
              {/* --- SKILL 1 --- */}
              <motion.div variants={lineVariants} className="text-slate-500 italic mt-2">
                # 1. Run the keyword expansion skill
              </motion.div>
              <motion.div variants={lineVariants} className="text-slate-200 flex items-center gap-2">
                <span className="text-emerald-400 font-bold">$</span> 
                <span>claude skills/expand-keywords.md</span>
              </motion.div>
              <motion.div variants={lineVariants} className="text-emerald-400 pl-4 border-l-2 border-emerald-500/30 bg-emerald-500/5 py-1 rounded-r-md mt-2 font-medium flex items-center gap-2">
                <CheckCircle2 size={14} /> 
                Updated main.py with 24 new keywords.
              </motion.div>

              {/* Spacer */}
              <motion.div variants={lineVariants} className="h-4"></motion.div>

              {/* --- SKILL 2 --- */}
              <motion.div variants={lineVariants} className="text-slate-500 italic">
                # 2. Auto-discover new Greenhouse companies
              </motion.div>
              <motion.div variants={lineVariants} className="text-slate-200 flex items-center gap-2">
                <span className="text-emerald-400 font-bold">$</span> 
                <span>claude skills/expand-greenhouse-companies.md</span>
              </motion.div>
              <motion.div variants={lineVariants} className="text-emerald-400 pl-4 border-l-2 border-emerald-500/30 bg-emerald-500/5 py-1 rounded-r-md mt-2 font-medium flex items-center gap-2">
                <CheckCircle2 size={14} /> 
                Added 118 new slugs to greenhouse.py
              </motion.div>

              {/* Final Prompt with Cursor */}
              <motion.div variants={lineVariants} className="text-slate-200 flex items-center gap-2 pt-4">
                <span className="text-emerald-400 font-bold">$</span> 
                <span className="w-2 h-4 bg-slate-400 animate-pulse"></span>
              </motion.div>

            </div>
          </div>
        </motion.div>

      </div>
    </section>
  );
}