import { useState } from "react";
import axios from "axios";
import { queryOnce, queryStream } from "../api/streamClient";

export default function QA() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [source, setSource] = useState("");
  const [sourceType, setSourceType] = useState("youtube");

  const [loading, setLoading] = useState(false);
  const [ingesting, setIngesting] = useState(false);

  // 🔹 INGEST FOR QnA
  const ingestForQnA = async () => {
    setIngesting(true);

    try {
      await axios.post("http://127.0.0.1:8000/api/v1/ingest/qna", {
        source_type: sourceType,
        source: source
      });
    } catch (err) { 
      console.error(err);
      alert("Ingestion failed");
    }

    setIngesting(false);
  };

  // 🔹 NORMAL QnA
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

  // 🔹 STREAMING QnA
  const askStream = async () => {
    setAnswer("");
    await queryStream(question, (token) => {
      setAnswer((prev) => prev + token);
    });
  };

  return (
    <div className="p-6 max-w-2xl mx-auto space-y-4">

      <h1 className="text-xl font-bold">Video QnA</h1>

      {/* 🔹 SOURCE INPUT */}
      <input
        className="w-full border p-2 text-black"
        placeholder={
          sourceType === "youtube"
            ? "Paste YouTube URL"
            : "Enter uploaded filename (e.g. video.mp4)"
        }
        value={source}
        onChange={(e) => setSource(e.target.value)}
      />

      {/* 🔹 INGEST BUTTONS */}
      <div className="flex gap-2">
        <button
          onClick={() => {
            setSourceType("youtube");
            ingestForQnA();
          }}
          className="bg-red-600 text-white px-4 py-2 rounded"
          disabled={ingesting}
        >
          {ingesting && sourceType === "youtube"
            ? "Ingesting..."
            : "YouTube Ingest"}
        </button>

        <button
          onClick={() => {
            setSourceType("local");
            ingestForQnA();
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded"
          disabled={ingesting}
        >
          {ingesting && sourceType === "local"
            ? "Ingesting..."
            : "File Ingest"}
        </button>
      </div>

      <hr />

      {/* 🔹 QUESTION INPUT */}
      <textarea
        className="w-full border p-2 text-black"
        rows={3}
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      {/* 🔹 QnA BUTTONS */}
      <div className="flex gap-2">
        <button
          onClick={ask}
          className="bg-black text-white px-4 py-2 rounded"
          disabled={loading}
        >
          Ask
        </button>

        <button
          onClick={askStream}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Stream Ask
        </button>
      </div>

      {/* 🔹 ANSWER */}
      {answer && (
        <div className="p-4 border rounded bg-gray-50 text-black whitespace-pre-wrap">
          {answer}
        </div>
      )}
    </div>
  );
}
