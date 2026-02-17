"use client";

import { useState } from "react";
import { humanizeText, ApiError } from "@/lib/api";
import type { HumanizationResult, Language, Intensity } from "@/lib/types";

export function useHumanization() {
  const [result, setResult] = useState<HumanizationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const humanize = async (
    text: string,
    language: Language,
    intensity: Intensity,
  ) => {
    setLoading(true);
    setError(null);
    try {
      const data = await humanizeText(text, language, intensity);
      setResult(data);
    } catch (e) {
      setError(
        e instanceof ApiError ? e.detail : "Humanization failed. Is the backend running?",
      );
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
  };

  return { result, loading, error, humanize, reset };
}
