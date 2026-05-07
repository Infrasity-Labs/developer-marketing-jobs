import { motion } from 'framer-motion';
import { Star, Zap } from 'lucide-react';

const Github = ({ size = 24, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" className={className} aria-hidden="true">
    <path d="M12 .5C5.65.5.5 5.65.5 12a11.5 11.5 0 0 0 7.86 10.92c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.78 1.2 1.78 1.2 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.7 0-1.26.45-2.29 1.18-3.1-.12-.29-.51-1.46.11-3.04 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.79 0c2.21-1.49 3.18-1.18 3.18-1.18.62 1.58.23 2.75.11 3.04.74.81 1.18 1.84 1.18 3.1 0 4.43-2.69 5.4-5.25 5.69.41.36.78 1.07.78 2.16v3.2c0 .31.21.67.8.56A11.5 11.5 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5z"/>
  </svg>
);

export default function CtaSection() {
  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0, y: 40, scale: 0.95 },
    visible: { 
      opacity: 1, 
      y: 0, 
      scale: 1,
      transition: { 
        duration: 0.6, 
        ease: "easeOut",
        staggerChildren: 0.15,
        delayChildren: 0.2
      } 
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 100, damping: 20 } }
  };

  return (
    <section className="w-full max-w-5xl mx-auto px-6 pb-32 pt-12 text-center relative">
      
      {/* Background Ambient Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80%] h-[80%] bg-indigo-500/10 rounded-full blur-[100px] pointer-events-none"></div>

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }} // Triggers when scrolling near the bottom
        className="bg-slate-900/60 border border-slate-700/50 rounded-[2.5rem] p-10 md:p-16 relative overflow-hidden shadow-2xl backdrop-blur-xl group"
      >
        {/* Animated Top Border Line */}
        <motion.div 
          initial={{ left: '-100%' }}
          whileInView={{ left: '100%' }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
          className="absolute top-0 w-1/2 h-[2px] bg-gradient-to-r from-transparent via-indigo-400 to-transparent opacity-75"
        />
        
        {/* Animated Corner Glows */}
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-indigo-500/20 rounded-full blur-3xl group-hover:bg-indigo-500/30 transition-colors duration-700"></div>
        <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-cyan-500/20 rounded-full blur-3xl group-hover:bg-cyan-500/30 transition-colors duration-700"></div>

        <div className="relative z-10 flex flex-col items-center">
          
          {/* Badge */}
          <motion.div 
            variants={itemVariants}
            className="font-inter inline-flex items-center gap-2 bg-emerald-500/10 text-emerald-400 px-5 py-2 rounded-full font-bold text-sm mb-8 border border-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.15)]"
          >
            <Zap size={16} className="fill-emerald-400" />
            100% Open Source
          </motion.div>
          
          {/* Heading */}
          <motion.h2 
            variants={itemVariants}
            className="font-quicksand text-4xl md:text-5xl lg:text-6xl font-bold mb-6 text-white tracking-tight"
          >
            Join the <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Community</span>
          </motion.h2>
          
          {/* Subtext */}
          <motion.p 
            variants={itemVariants}
            className="font-inter text-slate-400 mb-10 max-w-2xl mx-auto text-lg md:text-xl leading-relaxed"
          >
            Whether you are looking for your next DevRel role or want to contribute to our scraping pipelines, everything is public on GitHub under the MIT License.
          </motion.p>
          
          {/* CTA Button */}
          <motion.a 
            variants={itemVariants}
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
            href="https://github.com/Infrasity-Labs/developer-marketing-jobs" 
            target="_blank"
            rel="noreferrer"
            className="font-quicksand flex items-center gap-3 bg-white text-slate-950 px-8 py-4 md:px-10 md:py-5 rounded-full font-bold text-lg hover:bg-slate-100 transition-colors shadow-[0_0_30px_rgba(255,255,255,0.2)]"
          >
            <Github size={24} />
            Star Infrasity-Labs/developer-marketing-jobs
          </motion.a>

        </div>
      </motion.div>
    </section>
  );
}