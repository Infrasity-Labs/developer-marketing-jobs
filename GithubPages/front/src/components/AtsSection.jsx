import { motion } from 'framer-motion';
import { Network, ServerCog } from 'lucide-react';

// Enriched data from your architecture diagrams
const ATS_SOURCES = [
  { name: "Y Combinator", method: "Algolia API", stats: "5,600+ Companies" },
  { name: "Greenhouse", method: "CommonCrawl", stats: "842+ Discovered" },
  { name: "Lever", method: "DataForSEO + API", stats: "Auto-discovered" },
  { name: "Workable", method: "DataForSEO + API", stats: "Auto-discovered" },
  { name: "Ashby", method: "Public API", stats: "Direct Fetch" },
  { name: "RemoteOK", method: "Public API", stats: "Direct Fetch" },
  { name: "Remotive", method: "Public API", stats: "Direct Fetch" },
  { name: "Adzuna", method: "Paid API", stats: "4 Global Regions" }
];

export default function AtsSection() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, scale: 0.9, y: 20 },
    visible: { 
      opacity: 1, 
      scale: 1, 
      y: 0, 
      transition: { type: 'spring', stiffness: 100, damping: 15 } 
    }
  };

  return (
    <section className="w-full relative py-32 overflow-hidden border-y border-slate-800/60 bg-slate-950">
      
      {/* Subtle Background Elements */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:64px_64px] pointer-events-none opacity-20"></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-[300px] bg-indigo-500/5 blur-[100px] pointer-events-none"></div>

      <div className="max-w-6xl mx-auto px-6 relative z-10">
        
        {/* Header Content */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          
          <h2 className="font-quicksand text-4xl md:text-5xl font-bold text-white mb-6 tracking-tight">
            Supported <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Integrations</span>
          </h2>
          <p className="font-inter text-slate-400 max-w-2xl mx-auto text-lg leading-relaxed">
            Fetching data seamlessly from 8 distinct platforms via APIs, Algolia reverse-engineering, and CommonCrawl indexing pipelines.
          </p>
        </motion.div>

        {/* ATS Grid */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
        >
          {ATS_SOURCES.map((ats, i) => (
            <motion.div 
              key={i} 
              variants={itemVariants}
              whileHover={{ y: -5, scale: 1.02 }}
              className="group relative bg-slate-900/40 border border-slate-700/50 p-5 rounded-2xl hover:bg-slate-800/60 hover:border-indigo-500/40 transition-all duration-300 backdrop-blur-md overflow-hidden"
            >
              {/* Hover Glow */}
              <div className="absolute top-0 left-1/2 -translate-x-1/2 w-1/2 h-1/2 bg-indigo-500/20 blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>

              {/* Status Dot & Name */}
              <div className="flex items-center justify-between mb-4 relative z-10">
                <h3 className="font-quicksand text-lg font-bold text-slate-200 group-hover:text-white transition-colors">
                  {ats.name}
                </h3>
                <div className="flex items-center gap-2">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                  </span>
                </div>
              </div>

              {/* Stats & Method */}
              <div className="space-y-2 relative z-10">
                <div className="flex items-center gap-2 text-slate-400 font-inter text-sm group-hover:text-slate-300 transition-colors">
                  <ServerCog size={14} className="text-indigo-400/70" />
                  <span>{ats.method}</span>
                </div>
                <div className="font-inter text-xs font-bold text-slate-500 uppercase tracking-widest bg-slate-950/50 inline-block px-2 py-1 rounded-md border border-slate-800">
                  {ats.stats}
                </div>
              </div>

            </motion.div>
          ))}
        </motion.div>
        
      </div>
    </section>
  );
}