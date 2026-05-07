export default function CtaSection() {
  return (
    <section className="w-full max-w-4xl mx-auto px-6 pb-24 text-center">
      <div className="bg-gradient-to-b from-indigo-900/40 to-slate-900 border border-indigo-500/30 rounded-3xl p-12 relative overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-50"></div>
        
        <div className="inline-flex items-center gap-2 bg-emerald-500/10 text-emerald-400 px-4 py-1.5 rounded-full font-bold text-sm mb-6 border border-emerald-500/20">
          ⚡ 100% Open Source
        </div>
        <h2 className="text-4xl font-bold mb-6">Join the Community</h2>
        <p className="text-slate-400 mb-10 max-w-xl mx-auto text-lg">
          Whether you are looking for your next DevRel role or want to contribute to our scraping pipelines, everything is public on GitHub under the MIT License.
        </p>
        <a href="https://github.com/Infrasity-Labs/developer-marketing-jobs" 
           className="inline-flex items-center gap-2 bg-white text-slate-950 px-8 py-4 rounded-full font-bold text-lg hover:scale-105 transition-transform">
          ⭐ Star Infrasity-Labs/developer-marketing-jobs
        </a>
      </div>
    </section>
  );
}