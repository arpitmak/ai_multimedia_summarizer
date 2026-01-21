import { BrowserRouter as Router, Routes, Route, Outlet } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import SummaryPage from "./pages/SummaryPage";
import QAPage from "./pages/QAPage";
import Navbar from "./components/Navbar";

// Create a Layout wrapper
function WorkspaceLayout() {
  return (
    <div className="max-w-6xl mx-auto px-6 pb-20">
      <Navbar />
      <Outlet /> {/* This renders the specific page (Summary or QA) */}
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#09090b] text-zinc-200 font-sans">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          
          {/* All workspace routes go inside the Layout */}
          <Route element={<WorkspaceLayout />}>
            <Route path="/summary" element={<SummaryPage />} />
            <Route path="/qna" element={<QAPage />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}