function FeatureCard({ icon, title, desc }) {
  return (
    <div className="bg-slate-900/50 border border-slate-800 p-8 rounded-2xl hover:bg-slate-800/50 transition-colors">
      
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p className="text-slate-400 leading-relaxed">{desc}</p>
    </div>
  );
}

export default function FeaturesSection() {
  return (
    <section className="w-full max-w-6xl px-6 py-24">
      <h2 className="text-3xl font-bold mb-12 text-center">Engineering Architecture</h2>
      <div className="grid md:grid-cols-3 gap-6">
        <FeatureCard 
          icon="🔀"
          title="Parallel Browser Scraping" 
          desc="Runs 6 parallel GitHub Action jobs and utilizes threading with Playwright to cut scraping time in half."
        />
        <FeatureCard 
          icon="📊"
          title="Zero-DB Flat Architecture" 
          desc="Operates entirely on flat JSON caches (7-30 day TTLs) and GitHub Actions. No database infrastructure required."
        />
        <FeatureCard 
          icon="🌐"
          title="Auto-Discovery Pipelines" 
          desc="Uses CommonCrawl and DataForSEO to autonomously find new YC, Greenhouse, Lever, and Workable companies."
        />
      </div>
    </section>
  );
}