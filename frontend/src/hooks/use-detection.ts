"use client";

import { useState } from "react";
import { detectText, ApiError } from "@/lib/api";
import type { DetectionResult, Language } from "@/lib/types";

export function useDetection() {
  const [result, setResult] = useState<DetectionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const detect = async (text: string, language: Language) => {
    setLoading(true);
    setError(null);
    try {
      const data = await detectText(text, language);
      setResult(data);
    } catch (e) {
      setError(
        e instanceof ApiError ? e.detail : "Detection failed. Is the backend running?",
      );
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
  };

  return { result, loading, error, detect, reset };
}
