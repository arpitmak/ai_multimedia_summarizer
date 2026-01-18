import { useState } from "react";

export default function Summary() {
  const [sourceType, setSourceType] = useState("youtube");
  const [url, setUrl] = useState("");
  const [file, setFile] = useState(null);

  const [summary, setSummary] = useState("");
  const [status, setStatus] = useState("");

  const generateSummary = async () => {
    setSummary("");
    setStatus("Starting...");

    let payload;

    // ---- INGEST ----
    if (sourceType === "youtube") {
      setStatus("Downloading YouTube audio...");
      payload = {
        source_type: "youtube",
        source: url,
      };
    } else {
      setStatus("Uploading file...");

      const formData = new FormData();
      formData.append("file", file);

      const uploadRes = await fetch("http://localhost:8000/api/v1/ingest/upload", {
        method: "POST",
        body: formData,
      });

      const uploadData = await uploadRes.json();

      payload = {
        source_type: "local",
        source: uploadData.path,
      };
    }

    // ---- SUMMARY (STREAM) ----
    setStatus("Transcribing & summarizing...");

    const res = await fetch("http://localhost:8000/api/v1/summary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      setSummary((prev) => prev + decoder.decode(value));
    }

    setStatus("Done ✅");
  };

  return (
    <div className="space-y-4">

      {/* Source selector */}
      <div className="flex gap-4">
        <button
          onClick={() => setSourceType("youtube")}
          className={`px-4 py-2 rounded ${
            sourceType === "youtube"
              ? "bg-green-500 text-black"
              : "bg-gray-700"
          }`}
        >
          YouTube
        </button>

        <button
          onClick={() => setSourceType("local")}
          className={`px-4 py-2 rounded ${
            sourceType === "local"
              ? "bg-green-500 text-black"
              : "bg-gray-700"
          }`}
        >
          Local File
        </button>
      </div>

      {/* Input */}
      {sourceType === "youtube" ? (
        <input
          className="w-full p-2 text-black rounded"
          placeholder="YouTube URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
      ) : (
        <input
          type="file"
          accept="video/*,audio/*"
          onChange={(e) => setFile(e.target.files[0])}
        />
      )}

      {/* Action */}
      <button
        onClick={generateSummary}
        disabled={sourceType === "local" && !file}
        className="bg-green-500 px-4 py-2 rounded text-black"
      >
        Generate Summary
      </button>

      {/* Progress */}
      {status && (
        <div className="text-sm text-gray-300">
          {status}
        </div>
      )}

      {/* Output */}
      <pre className="whitespace-pre-wrap bg-gray-800 p-4 rounded">
        {summary}
      </pre>
    </div>
  );
}

