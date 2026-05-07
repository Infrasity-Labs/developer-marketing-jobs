export default function AtsSection() {
  return (
    <section className="w-full bg-slate-900/50 border-y border-slate-800 py-24">
      <div className="max-w-6xl mx-auto px-6 text-center">
        <h2 className="text-3xl font-bold mb-4">Supported ATS & Job Boards</h2>
        <p className="text-slate-400 mb-12 max-w-2xl mx-auto">Fetching data seamlessly from 8 distinct platforms via APIs, Algolia reverse-engineering, and CommonCrawl indexing.</p>
        <div className="flex flex-wrap justify-center gap-4">
          {["Greenhouse", "YC", "Lever", "Workable", "Ashby", "RemoteOK", "Remotive", "Adzuna"].map((ats, i) => (
            <span key={i} className="px-6 py-3 bg-slate-950 border border-slate-800 rounded-lg text-slate-300 font-medium shadow-sm hover:border-indigo-500/50 transition-colors">
              {ats}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}