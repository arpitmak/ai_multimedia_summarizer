import { motion } from "framer-motion";

export default function ModeToggle({ mode, setMode }) {
  return (
    <div className="relative flex p-1 bg-zinc-100 border border-zinc-200 rounded-lg shadow-inner">
      <motion.div
        className="absolute h-[calc(100%-8px)] bg-white rounded-md shadow-sm border border-zinc-200/50"
        initial={false}
        animate={{
          width: "50%",
          x: mode === "summary" ? 0 : "100%",
        }}
        transition={{ type: "spring", stiffness: 350, damping: 35 }}
      />

      <button
        onClick={() => setMode("summary")}
        className={`relative z-10 flex-1 px-6 py-2 text-[11px] font-bold tracking-widest uppercase transition-colors duration-200 ${
          mode === "summary" ? "text-indigo-600" : "text-zinc-400 hover:text-zinc-600"
        }`}
      >
        Summary
      </button>

      <button
        onClick={() => setMode("qna")}
        className={`relative z-10 flex-1 px-6 py-2 text-[11px] font-bold tracking-widest uppercase transition-colors duration-200 ${
          mode === "qna" ? "text-indigo-600" : "text-zinc-400 hover:text-zinc-600"
        }`}
      >
        Q&A
      </button>
    </div>
  );
}