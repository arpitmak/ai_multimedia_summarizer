export async function ingestFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("http://localhost:8000/api/v1/ingest/qna", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Ingestion failed");
  return res.json();
}

export async function ingestYoutube(url) {
  const res = await fetch("http://localhost:8000/api/v1/ingest/qna", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) throw new Error("Ingestion failed");
  return res.json();
}
