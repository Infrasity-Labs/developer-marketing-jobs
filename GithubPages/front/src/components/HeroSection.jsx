import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

// --- NEURAL BACKGROUND COMPONENT (Unchanged) ---
const NeuralBackground = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let particles = [];
    const numParticles = 80;
    const connectionDistance = 150;
    let mouse = { x: -1000, y: -1000 };

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', resize);
    resize();

    class Particle {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.8;
        this.vy = (Math.random() - 0.5) * 0.8;
        this.radius = Math.random() * 2 + 1;
      }
      update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
      }
      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(99, 102, 241, 0.4)'; 
        ctx.fill();
      }
    }

    for (let i = 0; i < numParticles; i++) {
      particles.push(new Particle());
    }

    const handleMouseMove = (e) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    };
    const handleMouseLeave = () => {
      mouse.x = -1000;
      mouse.y = -1000;
    };

    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseleave', handleMouseLeave);

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      for (let i = 0; i < numParticles; i++) {
        particles[i].update();
        particles[i].draw();

        for (let j = i + 1; j < numParticles; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < connectionDistance) {
            const mouseDx = mouse.x - (particles[i].x + particles[j].x) / 2;
            const mouseDy = mouse.y - (particles[i].y + particles[j].y) / 2;
            const mouseDist = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy);
            
            let baseOpacity = 1 - (dist / connectionDistance);
            
            if (mouseDist < 200) {
              const intensity = 1 - (mouseDist / 200);
              ctx.strokeStyle = `rgba(34, 211, 238, ${baseOpacity + intensity * 0.5})`; 
              ctx.lineWidth = 1.5;
            } else {
              ctx.strokeStyle = `rgba(99, 102, 241, ${baseOpacity * 0.2})`; 
              ctx.lineWidth = 0.8;
            }

            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }
      animationFrameId = requestAnimationFrame(animate);
    };
    
    animate();

    return () => {
      window.removeEventListener('resize', resize);
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('mouseleave', handleMouseLeave);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return <canvas ref={canvasRef} className="absolute inset-0 z-0 opacity-60" />;
};


// --- MAIN HERO COMPONENT ---
export default function HeroSection() {
  // Master timeline for stagger effects
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 }
    }
  };

  // Smooth fade-up for general items
  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 80, damping: 20 } }
  };

  // Specific variant for the word-by-word headline reveal
  const wordVariants = {
    hidden: { opacity: 0, y: 20, rotateX: 20 },
    visible: { opacity: 1, y: 0, rotateX: 0, transition: { duration: 0.5, ease: "easeOut" } }
  };

  const titleText = "The Automated Developer Marketing";

  return (
    <section className="relative w-full min-h-[90vh] flex flex-col items-center justify-center overflow-hidden border-b border-slate-800/50">
      
      <NeuralBackground />

      <motion.div 
        className="relative z-10 w-full max-w-5xl px-6 py-24 flex flex-col items-center text-center pointer-events-none"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Upgraded Pill Badge */}
        <motion.div 
          variants={itemVariants} 
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900/50 text-indigo-300 text-sm font-medium mb-8 ring-1 ring-indigo-500/30 backdrop-blur-md shadow-[0_0_15px_rgba(99,102,241,0.15)] pointer-events-auto"
        >
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
          </span>
          Updated Daily at 6 AM UTC
        </motion.div>

        {/* Upgraded Headline with Word Staggering */}
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-extrabold tracking-tighter mb-6 leading-[1.1] drop-shadow-2xl">
          {titleText.split(" ").map((word, i) => (
            <motion.span key={i} variants={wordVariants} className="inline-block mr-[0.25em] text-white">
              {word}
            </motion.span>
          ))}
          <br/>
          <motion.span 
            variants={wordVariants}
            className="inline-block text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-cyan-400 to-teal-300"
          >
            Job Board
          </motion.span>
        </h1>

        {/* Upgraded Subtitle */}
        <motion.p 
          variants={itemVariants} 
          className="text-lg md:text-xl text-slate-400 max-w-2xl mb-10 leading-relaxed font-light drop-shadow-md"
        >
          Aggregating <span className="text-slate-200 font-medium">500+</span> Developer Marketing, Technical Writing, and Community roles daily from <span className="text-slate-200 font-medium">30,000+ sources</span> and <span className="text-slate-200 font-medium">6,500+ companies</span>. Fully automated, 100% open source.
        </motion.p>

        {/* Upgraded Interactive Buttons */}
        <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-4 pointer-events-auto w-full sm:w-auto">
          <motion.a 
            href="https://github.com/Infrasity-Labs/developer-marketing-jobs" 
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            className="flex items-center justify-center gap-2 bg-indigo-600 text-white px-8 py-4 rounded-xl font-semibold transition-colors hover:bg-indigo-500 shadow-[0_0_20px_rgba(99,102,241,0.3)] ring-1 ring-indigo-500/50 w-full sm:w-auto"
          >
            ⭐ Star the Repository
          </motion.a>
          <motion.a 
            href="https://github.com/Infrasity-Labs/developer-marketing-jobs#readme" 
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            className="flex items-center justify-center gap-2 bg-slate-900/80 text-white px-8 py-4 rounded-xl font-semibold transition-colors hover:bg-slate-800 ring-1 ring-slate-700 backdrop-blur-md w-full sm:w-auto"
          >
            View Live Jobs
          </motion.a>
        </motion.div>
        
        {/* Upgraded Stats Row */}
        <motion.div 
          variants={itemVariants} 
          className="grid grid-cols-2 md:grid-cols-3 gap-8 mt-24 w-full pt-12 border-t border-slate-800/60 pointer-events-auto"
        >
          {[
            { label: "Companies Tracked", value: "6,500+" },
            { label: "Jobs Fetched Daily", value: "30,000" },
            { label: "Active ATS Sources", value: "8" },
            
          ].map((stat, i) => (
            <motion.div 
              key={i} 
              whileHover={{ y: -5 }}
              className="flex flex-col gap-2 p-4 rounded-2xl hover:bg-slate-800/30 transition-colors"
            >
              <span className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-white to-slate-400">
                {stat.value}
              </span>
              <span className="text-slate-500 text-xs font-bold uppercase tracking-widest">
                {stat.label}
              </span>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </section>
  );
}