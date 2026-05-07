import { motion } from 'framer-motion';
import { GitMerge, Database, Globe } from 'lucide-react';

function FeatureCard({ icon, title, desc, variants }) {
  return (
    <motion.div 
      variants={variants}
      whileHover={{ y: -8, scale: 1.02 }}
      className="group bg-slate-900/50 border border-slate-800 p-8 rounded-3xl transition-all duration-300 hover:bg-slate-800/80 hover:border-indigo-500/30 hover:shadow-[0_0_40px_rgba(99,102,241,0.1)] backdrop-blur-sm"
    >
      {/* Icon Container with subtle glow on hover */}
    
      
      <h3 className="font-quicksand text-2xl font-bold text-slate-100 mb-3 group-hover:text-white transition-colors">
        {title}
      </h3>
      
      <p className="font-inter text-slate-400 leading-relaxed group-hover:text-slate-300 transition-colors">
        {desc}
      </p>
    </motion.div>
  );
}

export default function FeaturesSection() {
  // Container variants handle the staggered children effect
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { 
        staggerChildren: 0.2, 
        delayChildren: 0.1 
      }
    }
  };

  // Item variants handle the individual card pop-up
  const cardVariants = {
    hidden: { opacity: 0, y: 40 },
    visible: { 
      opacity: 1, 
      y: 0, 
      transition: { type: 'spring', stiffness: 80, damping: 20 } 
    }
  };

  return (
    <section className="w-full max-w-6xl mx-auto px-6 py-32 relative">
      
      {/* Subtle background glow behind the section */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3/4 h-3/4 bg-indigo-500/5 rounded-full blur-[120px] pointer-events-none"></div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.6 }}
        className="text-center mb-16 relative z-10"
      >
        <h2 className="font-quicksand text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight">
          Engineering <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Architecture</span>
        </h2>
        <p className="font-inter text-slate-400 max-w-2xl mx-auto text-lg">
          Built for scale and speed, entirely on zero-maintenance cloud infrastructure.
        </p>
      </motion.div>

      {/* motion.div wrapper with whileInView triggers the animation when scrolled to */}
      <motion.div 
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-50px" }} // Triggers slightly before they come into view
        className="grid md:grid-cols-3 gap-6 relative z-10"
      >
        <FeatureCard 
          variants={cardVariants}
          icon={<GitMerge size={28} />}
          title="Parallel Scraping" 
          desc="Runs 6 parallel GitHub Action jobs and utilizes threading with Playwright to cut scraping time in half."
        />
        <FeatureCard 
          variants={cardVariants}
          icon={<Database size={28} />}
          title="Zero-DB Flat Arch" 
          desc="Operates entirely on flat JSON caches (7-30 day TTLs) and GitHub Actions. No database infrastructure required."
        />
        <FeatureCard 
          variants={cardVariants}
          icon={<Globe size={28} />}
          title="Auto-Discovery" 
          desc="Uses CommonCrawl and DataForSEO to autonomously find new YC, Greenhouse, Lever, and Workable companies."
        />
      </motion.div>

    </section>
  );
}