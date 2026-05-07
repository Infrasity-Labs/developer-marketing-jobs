export default function ScreenshotSection() {
  return (
    <section className="w-full max-w-5xl px-6 py-12">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-2 shadow-2xl relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent z-10 pointer-events-none"></div>
        {/* Replace src with your actual screenshot image path */}
        <div className="w-full h-[400px] bg-slate-800 rounded-xl flex items-center justify-center border border-slate-700">
           <span className="text-slate-500 font-mono">[ Screenshot of README Jobs List goes here ]</span>
        </div>
      </div>
    </section>
  );
}