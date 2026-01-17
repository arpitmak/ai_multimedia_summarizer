import { useState } from "react";
import { queryOnce } from "../api/streamClient";
import { queryStream } from "../api/streamClient";

export default function QA() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState(false);


  const ask = async () => {
    setLoading(true);
    setAnswer("");

    try {
      const res = await queryOnce(question);
      setAnswer(res.answer);
    } catch (err) {
      setAnswer("Error fetching answer");
    }

    setLoading(false);
  };

  const askStream = async () => {
  setAnswer("");
  setStreaming(true);

  await queryStream(question, (token) => {
    setAnswer((prev) => prev + token);
  });

  setStreaming(false);
};

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-xl font-bold mb-4">Ask your data</h1>

      <textarea 
        className="w-full border p-2 mb-3 text-black"
        rows={3}
        placeholder="Ask something..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button
        onClick={ask}
        className="bg-black text-white px-4 py-2 rounded"
        disabled={loading}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>
      <button
  onClick={askStream}
  className="bg-green-600 text-white px-4 py-2 rounded ml-2"
>
  Stream Ask
</button>

      {answer && (
        <div className="mt-4 p-4 border rounded bg-gray-50 text-black">
          {answer}
        </div>
      )}
    </div>
  );
}
