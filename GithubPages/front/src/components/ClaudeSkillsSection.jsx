export default function ClaudeSkillsSection() {
  return (
    <section className="w-full max-w-6xl px-6 py-24">
      <div className="flex flex-col md:flex-row gap-12 items-center">
        <div className="flex-1">
          <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
            🤖 Powered by Claude Code
          </h2>
          <p className="text-slate-400 mb-6 text-lg leading-relaxed">
            We leverage Claude Code CLI as executable markdown skills to maintain the repository automatically. 
            Running in an isolated subprocess ensures exact context boundaries.
          </p>
          <ul className="space-y-4">
            <li className="flex gap-3 items-start">
              <span className="text-indigo-500 shrink-0 mt-1">✓</span>
              <div>
                <strong className="block text-slate-200">keyword_expander.py</strong>
                <span className="text-slate-400 text-sm">Expands hardcoded dev-tools categories from 10 to 30+ semantic keywords.</span>
              </div>
            </li>
            <li className="flex gap-3 items-start">
              <span className="text-indigo-500 shrink-0 mt-1">✓</span>
              <div>
                <strong className="block text-slate-200">expand-greenhouse-companies.md</strong>
                <span className="text-slate-400 text-sm">Auto-discovers new Greenhouse ATS URLs and updates our python scraper configurations.</span>
              </div>
            </li>
          </ul>
        </div>
        <div className="flex-1 w-full bg-slate-900 border border-slate-800 rounded-xl p-6 font-mono text-sm shadow-xl">
          <div className="flex gap-2 mb-4">
            <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
            <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></div>
          </div>
          <p className="text-indigo-400 mb-2"># Run the keyword expansion skill</p>
          <p className="text-slate-300">$ claude skills/expand-keywords.md</p>
          <p className="text-slate-500 mt-4">Running in temp isolated environment...</p>
          <p className="text-slate-500">Expanding: Product-Led Growth...</p>
          <p className="text-green-400 mt-2">✓ Updated main.py with 24 new keywords.</p>
        </div>
      </div>
    </section>
  );
}