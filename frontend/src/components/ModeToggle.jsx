export default function ModeToggle({ mode, setMode }) {
  return (
    <div className="flex gap-4 mb-6">
      <button
        onClick={() => setMode("qna")}
        className={`px-6 py-2 rounded ${
          mode === "qna"
            ? "bg-green-500 text-black"
            : "bg-gray-700 text-white"
        }`}
      >
        QnA
      </button>

      <button
        onClick={() => setMode("summary")}
        className={`px-6 py-2 rounded ${
          mode === "summary"
            ? "bg-green-500 text-black"
            : "bg-gray-700 text-white"
        }`}
      >
        Summary
      </button>
    </div>
  );
}
