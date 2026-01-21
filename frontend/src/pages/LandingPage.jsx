import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useRef } from "react";

export default function LandingPage() {
  const briefingRef = useRef(null);

  const scrollToBriefing = () => {
    briefingRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const typewriterText = "Experience the power of AI-driven video synthesis. Skip the watch, get the knowledge.";
  const sentence = { hidden: { opacity: 1 }, visible: { opacity: 1, transition: { staggerChildren: 0.03 } } };
  const letter = { hidden: { opacity: 0, display: "none" }, visible: { opacity: 1, display: "inline" } };

  return (
    <div className="max-w-6xl mx-auto px-6">
      {/* Hero Section */}
      <section className="h-screen flex flex-col items-center justify-center border-b border-zinc-900">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="px-4 py-1 mb-8 rounded-full border border-zinc-800 bg-zinc-900/50 text-zinc-500 text-[10px] font-bold tracking-[0.2em] uppercase shadow-sm">
          Enterprise AI Platform
        </motion.div>
        
        <h1 className="text-7xl md:text-8xl font-semibold tracking-tighter text-white mb-6 text-center">
          VidInsight<span className="text-indigo-500">.</span>
        </h1>

        <motion.p variants={sentence} initial="hidden" animate="visible" className="text-zinc-500 text-lg max-w-lg text-center leading-relaxed mb-12 min-h-[3rem]">
          {typewriterText.split("").map((char, index) => (
            <motion.span key={index} variants={letter}>{char}</motion.span>
          ))}
        </motion.p>

        <button onClick={scrollToBriefing} className="px-10 py-3.5 bg-zinc-100 text-black font-bold rounded-xl hover:bg-white transition-all text-sm active:scale-95">
          Discover More
        </button>
      </section>

      {/* Briefing Section */}
      <section ref={briefingRef} id="briefing" className="py-32">
        <div className="text-center mb-24">
          <h2 className="text-4xl font-bold tracking-tight mb-4 text-white">What we do.</h2>
          <p className="text-zinc-500 max-w-xl mx-auto leading-relaxed">
            Turn YouTube videos into usable knowledge.
            Paste a link to generate transcripts, summaries, and ask questions — powered by AI.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-24">
          {/* Summary Option */}
          <Link to="/summary" className="group p-10 bg-zinc-900/50 border border-zinc-800 rounded-[2rem] hover:border-indigo-500/50 transition-all hover:bg-zinc-900">
            <div className="w-12 h-12 bg-indigo-500/10 rounded-2xl flex items-center justify-center text-indigo-500 font-bold mb-8 group-hover:bg-indigo-500 group-hover:text-white transition-all">Σ</div>
            <h3 className="text-2xl font-bold mb-4 text-white">Synthesis Engine</h3>
            <p className="text-zinc-500 mb-8 leading-relaxed">Paste a YouTube link to generate an AI-powered summary based on the full transcript.</p>
            <span className="text-xs font-bold uppercase tracking-widest text-indigo-500 group-hover:gap-3 transition-all flex items-center gap-2">Open Workspace →</span>
          </Link>

          {/* QnA Option */}
          <Link to="/qna" className="group p-10 bg-zinc-900/50 border border-zinc-800 rounded-[2rem] hover:border-indigo-500/50 transition-all hover:bg-zinc-900">
            <div className="w-12 h-12 bg-zinc-800 rounded-2xl flex items-center justify-center text-zinc-400 font-bold mb-8 group-hover:bg-indigo-500 group-hover:text-white transition-all">?</div>
            <h3 className="text-2xl font-bold mb-4 text-white">Intelligence Hub</h3>
            <p className="text-zinc-500 mb-8 leading-relaxed">Interrogate video context through natural language to find specific answers instantly.</p>
            <span className="text-xs font-bold uppercase tracking-widest text-indigo-500 group-hover:gap-3 transition-all flex items-center gap-2">Start Chatting →</span>
          </Link>
        </div>
      </section>
    </div>
  );
}