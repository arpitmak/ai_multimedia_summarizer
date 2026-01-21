import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function Summary() {
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [status, setStatus] = useState("");

  const generateSummary = async () => {
    setSummary("");
    setStatus("Processing Audio/Visual...");
    try {
      const res = await fetch("http://localhost:8000/api/v1/summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_type: "youtube", source: url }),
      });
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        setSummary((prev) => prev + decoder.decode(value));
      }
      setStatus("Complete");
    } catch (err) {
      setStatus("Error");
    }
  };

  return (
    
    <div className="max-w-4xl mx-auto">
      <div className="mb-10">
        <h2 className="text-3xl font-bold text-white mb-3 tracking-tight text-center md:text-left">
          Synthesis Engine
        </h2>
        <p className="text-zinc-500 font-medium text-center md:text-left text-sm">
          Convert video streams into structured intelligence briefs.
        </p>
      </div>

      <div className="space-y-12">
        {/* --- Input Section --- */}
        <section className="bg-zinc-900/40 border border-zinc-800/60 p-8 rounded-2xl shadow-2xl backdrop-blur-sm">
          <label className="block text-[10px] font-bold uppercase tracking-[0.2em]  text-white  mb-5 ml-1">
            Video Source
          </label>
          <div className="flex flex-col md:flex-row gap-4">
            <input
              className="flex-1 bg-black border border-zinc-800 p-4 rounded-xl text-sm text-zinc-300 focus:border-indigo-500/50 outline-none font-mono transition-all placeholder:text-zinc-700"
              placeholder="https://youtube.com/watch?v=..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button
              onClick={generateSummary}
              disabled={!url || (status && status !== "Complete")}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-10 py-4 rounded-xl text-[10px] font-black tracking-widest uppercase transition-all shadow-lg shadow-indigo-900/20 disabled:opacity-30"
            >
              {status && status !== "Complete" ? "PROCESSING..." : "GENERATE"}
            </button>
          </div>
          {status && (
            <div className="mt-4 flex items-center gap-2 ml-1">
              <div className={`w-1.5 h-1.5 rounded-full ${status === "Complete" ? "bg-emerald-500" : "bg-indigo-500 animate-pulse"}`} />
              <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-widest">{status}</span>
            </div>
          )}
        </section>

        {/* --- Brief Section --- */}
        <AnimatePresence>
          {summary && (
            <motion.section initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="pt-4 px-2">
              <div className="flex justify-between items-center mb-8">
                <h3 className="text-[11px] font-bold uppercase tracking-widest text-zinc-500 border-l-2 border-indigo-600 pl-4">
                  Executive Brief
                </h3>
                <button 
                  onClick={() => navigator.clipboard.writeText(summary)} 
                  className="text-[10px] text-zinc-500 hover:text-indigo-400 transition-colors uppercase tracking-widest font-black"
                >
                  Copy Output
                </button>
              </div>
              <div className="text-zinc-300 leading-relaxed text-[16px] font-medium pl-4 selection:bg-indigo-500/30">
                <pre className="whitespace-pre-wrap font-sans">{summary}</pre>
              </div>
            </motion.section>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}