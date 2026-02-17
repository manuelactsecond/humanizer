import type { DetectionResult, HumanizationResult, Intensity, Language } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string,
  ) {
    super(detail);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new ApiError(res.status, data.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

export async function detectText(
  text: string,
  language: Language,
): Promise<DetectionResult> {
  return request<DetectionResult>("/api/v1/detection/analyze", {
    text,
    language,
  });
}

export async function humanizeText(
  text: string,
  language: Language,
  intensity: Intensity,
): Promise<HumanizationResult> {
  return request<HumanizationResult>("/api/v1/humanization/humanize", {
    text,
    language,
    intensity,
  });
}

export { ApiError };
