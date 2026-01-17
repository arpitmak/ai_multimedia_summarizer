import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
});

export const uploadFile = (formData) =>
  api.post("/ingest/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

export const ingestYoutube = (url) =>
  api.post("/ingest/youtube-transcribe", { url });
