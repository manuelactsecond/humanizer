export interface FeatureScores {
  perplexity: number;
  burstiness: number;
  vocabulary_richness: number;
  sentence_variance: number;
}

export interface DetectionResult {
  overall_score: number;
  confidence: number;
  verdict: "likely_human" | "mixed" | "likely_ai";
  features: FeatureScores;
  explanation: string;
}

export interface HumanizationResult {
  original_text: string;
  humanized_text: string;
  changes_summary: string[];
  detection_before: DetectionResult;
  detection_after: DetectionResult;
  word_count_original: number;
  word_count_humanized: number;
}

export type Language = "en" | "es";
export type Intensity = "light" | "medium" | "aggressive";
