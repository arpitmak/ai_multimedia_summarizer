import { useState } from "react";
import ModeToggle from "./components/ModeToggle";
import QA from "./pages/QA";
import Summary from "./pages/summary";

export default function App() {
  const [mode, setMode] = useState("qna");

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-4">
        AI Multimedia Assistant
      </h1>

      <ModeToggle mode={mode} setMode={setMode} />

      {mode === "qna" ? <QA /> : <Summary />}
    </div>
  );
}
