import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, Image as ImageIcon } from 'lucide-react';

// 1. ADD YOUR IMAGES HERE
// Place your actual image files inside the "public" folder of your Vite project.
// Then, update the 'src' below to match the filenames (e.g., '/screenshot-1.png').
const SCREENSHOTS = [
  {
    id: 1,
    src: 'https://infrasity-pull-zone.b-cdn.net/Job/Screenshot%202026-05-08%20002731.png', // Leave empty to see the placeholder, or add '/your-image.png'
    title: 'Live Jobs README Feed',
    description: 'The automated markdown table displaying 500+ daily jobs.'
  },
  {
    id: 2,
    src: 'https://infrasity-pull-zone.b-cdn.net/Job/Screenshot%202026-05-08%20002500.png', 
    title: 'GitHub Actions Pipeline',
    description: '6 parallel fetcher jobs running the automated scraping.'
  },
  {
    id: 3,
    src: 'https://infrasity-pull-zone.b-cdn.net/Job/Screenshot%202026-05-08%20003159.png', 
    title: 'Claude Code Terminal',
    description: 'Executing the skill to dynamically expand category keywords.'
  }
];

export default function ScreenshotSection() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [direction, setDirection] = useState(0);

  const slideVariants = {
    enter: (direction) => ({
      x: direction > 0 ? '100%' : '-100%',
      opacity: 0,
      scale: 0.95
    }),
    center: {
      x: 0,
      opacity: 1,
      scale: 1,
      transition: { duration: 0.5, type: 'spring', bounce: 0.2 }
    },
    exit: (direction) => ({
      x: direction < 0 ? '100%' : '-100%',
      opacity: 0,
      scale: 0.95,
      transition: { duration: 0.3 }
    })
  };

  const paginate = (newDirection) => {
    setDirection(newDirection);
    setCurrentIndex((prevIndex) => {
      let nextIndex = prevIndex + newDirection;
      if (nextIndex < 0) return SCREENSHOTS.length - 1;
      if (nextIndex >= SCREENSHOTS.length) return 0;
      return nextIndex;
    });
  };

  const goToSlide = (index) => {
    setDirection(index > currentIndex ? 1 : -1);
    setCurrentIndex(index);
  };

  const currentShot = SCREENSHOTS[currentIndex];

  return (
    <section className="w-full max-w-6xl mx-auto px-6 py-24 flex flex-col items-center">
      
      {/* Section Header */}
      <div className="text-center mb-12">
        <h2 className="font-quicksand text-3xl md:text-4xl font-bold text-white mb-4">
          See it in <span className="text-indigo-400">Action</span>
        </h2>
        <p className="font-inter text-slate-400">A look inside the automation pipeline and output.</p>
      </div>

      {/* Main Carousel Container */}
      <div className="w-full relative group">
        
        {/* The Glassmorphic Frame */}
        <div className="relative rounded-2xl border border-slate-700/60 bg-slate-900/40 p-2 md:p-4 shadow-2xl backdrop-blur-sm overflow-hidden aspect-[16/9] max-h-[600px] flex items-center justify-center">
          
          <AnimatePresence initial={false} custom={direction} mode="popLayout">
            <motion.div
              key={currentIndex}
              custom={direction}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              className="absolute inset-2 md:inset-4 flex flex-col items-center justify-center rounded-xl overflow-hidden bg-slate-950 border border-slate-800"
            >
              {currentShot.src ? (
                // Actual Image
                <img 
                  src={currentShot.src} 
                  alt={currentShot.title}
                  className="w-full h-full object-cover p-10"
                />
              ) : (
                // Wireframe Placeholder (Shows if src is empty)
                <div className="flex flex-col items-center justify-center text-slate-600">
                  <ImageIcon size={64} className="mb-4 opacity-50" />
                  <span className="font-mono text-sm tracking-wider uppercase">
                    [ Missing Image: {currentShot.title} ]
                  </span>
                  <span className="font-inter text-xs text-slate-500 mt-2">
                    Add path to SCREENSHOTS array
                  </span>
                </div>
              )}

              {/* Image Gradient Overlay & Caption */}
              <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-slate-950 via-slate-950/80 to-transparent p-6 pt-12">
                <h3 className="font-quicksand text-xl font-bold text-white">{currentShot.title}</h3>
                <p className="font-inter text-sm text-slate-300 mt-1">{currentShot.description}</p>
              </div>
            </motion.div>
          </AnimatePresence>

        </div>

        {/* Left Arrow Button */}
        <button
          onClick={() => paginate(-1)}
          className="absolute left-4 top-1/2 -translate-y-1/2 p-3 rounded-full bg-slate-950/80 border border-slate-700 text-white opacity-0 group-hover:opacity-100 transition-all hover:bg-indigo-600 hover:scale-110 z-20 backdrop-blur-md hidden md:block"
        >
          <ChevronLeft size={24} />
        </button>

        {/* Right Arrow Button */}
        <button
          onClick={() => paginate(1)}
          className="absolute right-4 top-1/2 -translate-y-1/2 p-3 rounded-full bg-slate-950/80 border border-slate-700 text-white opacity-0 group-hover:opacity-100 transition-all hover:bg-indigo-600 hover:scale-110 z-20 backdrop-blur-md hidden md:block"
        >
          <ChevronRight size={24} />
        </button>

      </div>

      {/* Dot Indicators */}
      <div className="flex gap-3 mt-8">
        {SCREENSHOTS.map((_, index) => (
          <button
            key={index}
            onClick={() => goToSlide(index)}
            className={`h-2.5 rounded-full transition-all duration-300 ${
              index === currentIndex 
                ? 'w-8 bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.6)]' 
                : 'w-2.5 bg-slate-700 hover:bg-slate-500'
            }`}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>

    </section>
  );
}