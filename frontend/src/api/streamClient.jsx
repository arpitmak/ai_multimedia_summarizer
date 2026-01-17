import axios from "axios";

const API_BASE = "http://localhost:8000/api/v1";

// NON-STREAM (Axios)
export async function queryOnce(question) {
  const res = await axios.post(`${API_BASE}/query`, {query:question});
  return res.data;
}

// STREAM (Fetch)
export async function queryStream(question, onToken) {
  const res = await fetch(`${API_BASE}/query/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query:question }),
  });

  const reader = res.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    onToken(decoder.decode(value));
  }
}
