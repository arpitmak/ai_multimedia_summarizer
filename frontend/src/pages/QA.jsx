import { useState } from "react";
import axios from "axios";
import { queryStream } from "../api/streamClient";
import { motion, AnimatePresence } from "framer-motion";
import Navbar from "../components/Navbar";

export default function QA() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [source, setSource] = useState("");
  const [ingesting, setIngesting] = useState(false);
  const [ingestStatus, setIngestStatus] = useState("");

  const ingestForQnA = async () => {
    setIngesting(true);
    setIngestStatus("");
    try {
      await axios.post("http://127.0.0.1:8000/api/v1/ingest/qna", { 
        source_type: "youtube", 
        source: source 
      });
      setIngestStatus("Context synchronized. System ready.");
    } catch (err) { 
      alert("Ingestion failed"); 
    }
    setIngesting(false);
  };

  const askStream = async () => {
    if (!question) return;
    setAnswer("");
    await queryStream(question, (token) => {
      setAnswer((prev) => prev + token);
    });
  };

  return (
    
    <div className="max-w-6xl mx-auto px-6 pb-20">
      
      
      <div className="bg-zinc-900/40 border border-zinc-800/60 rounded-3xl p-8 md:p-12 shadow-2xl backdrop-blur-sm">
        <div className="max-w-3xl mx-auto space-y-12">
          
          <div className="mb-2">
            <h2 className="text-3xl font-bold text-white mb-2 tracking-tight">Intelligence Hub</h2>
            <p className="text-zinc-500 text-sm">Q&A on YouTube Videos
Ask questions grounded in the video’s content — not guesses.</p>
          </div>

          {/* --- SECTION 1: DATA SOURCE --- */}
          <section>
            <label className="block text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-600 mb-4 ml-1">
              Data Source
            </label>
            {/* Flex Container 1 */}
            <div className="flex flex-col md:flex-row gap-4">
              <input
                className="flex-1 bg-black border border-zinc-800 p-4 rounded-xl text-sm text-zinc-300 focus:border-indigo-500/50 outline-none font-mono transition-all placeholder:text-zinc-700"
                placeholder="https://youtube.com/watch?v=..."
                value={source}
                onChange={(e) => { setSource(e.target.value); setIngestStatus(""); }}
              />
              <button
                onClick={ingestForQnA}
                disabled={ingesting || !source}
                className="w-full md:w-[160px] bg-indigo-600 hover:bg-indigo-700 text-white py-4 rounded-xl text-[10px] font-black tracking-widest uppercase transition-all shadow-lg shadow-indigo-900/20 disabled:opacity-30"
              >
                {ingesting ? "ANALYZING..." : "ANALYZE"}
              </button>
            </div>
            {ingestStatus && (
              <p className="mt-4 text-emerald-500/80 text-[10px] font-mono font-bold uppercase ml-1 tracking-tighter">
                // {ingestStatus}
              </p>
            )}
          </section>

          {/* --- SECTION 2: WORKSPACE QUERY --- */}
          <section>
            <label className="block text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-600 mb-4 ml-1">
              Workspace Query
            </label>
            {/* Flex Container 2 (Aligned to Container 1) */}
            <div className="flex flex-col md:flex-row gap-4">
              <input
                className="flex-1 bg-black border border-zinc-800 p-4 rounded-xl text-sm text-zinc-100 focus:border-indigo-500/50 outline-none transition-all placeholder:text-zinc-800 font-medium"
                placeholder="Enter your question here..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && askStream()}
              />
              <button
                onClick={askStream}
                disabled={!question}
                className="w-full md:w-[160px] bg-indigo-600 hover:bg-indigo-700 text-white py-4 rounded-xl text-[10px] font-black tracking-widest uppercase transition-all shadow-lg shadow-indigo-900/20 disabled:opacity-30"
              >
                Ask
              </button>
            </div>

            <AnimatePresence>
              {answer && (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }} 
                  animate={{ opacity: 1, y: 0 }} 
                  className="mt-10 p-10 bg-black/60 border border-zinc-800 rounded-2xl shadow-inner relative overflow-hidden"
                >
                  <div className="absolute top-0 left-0 w-1.5 h-full bg-indigo-600" />
                  <span className="block text-[10px] font-bold text-indigo-500 uppercase mb-6 tracking-[0.2em]">Synthesized Response</span>
                  <p className="whitespace-pre-wrap font-medium text-zinc-300 leading-relaxed text-[16px]">{answer}</p>
                </motion.div>
              )}
            </AnimatePresence>
          </section>

        </div>
      </div>
    </div>
  );
}