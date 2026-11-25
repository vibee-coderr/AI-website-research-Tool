
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getStatus = () => API.get("/status");

export const processArticles = (urls) =>
  API.post("/process-urls", { urls });

export const askQuestion = (question) =>
  API.post("/ask", { question });
