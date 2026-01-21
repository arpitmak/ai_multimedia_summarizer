import { useNavigate, useLocation } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNav = (path) => {
    // This is a pure JS state change, NOT a page load
    navigate(path, { replace: true });
  };

  return (
    <nav className="flex justify-between items-center py-8 mb-16 border-b border-zinc-800/50">
      <div onClick={() => navigate("/")} className="cursor-pointer text-2xl font-bold">
        VidInsight<span className="text-indigo-500">.</span>
      </div>
      
      <div className="flex bg-black p-1 rounded-xl border border-zinc-800">
        {/* Use BUTTONS, not links, to ensure no refresh */}
        <button 
          onClick={() => handleNav("/summary")}
          className={`px-6 py-2 rounded-lg text-[10px] font-black uppercase transition-all ${
            location.pathname === "/summary" ? "bg-zinc-800 text-white" : "text-zinc-500"
          }`}
        >
          Summary
        </button>
        <button 
          onClick={() => handleNav("/qna")}
          className={`px-6 py-2 rounded-lg text-[10px] font-black uppercase transition-all ${
            location.pathname === "/qna" ? "bg-zinc-800 text-white" : "text-zinc-500"
          }`}
        >
          Q&A
        </button>
      </div>
    </nav>
  );
}