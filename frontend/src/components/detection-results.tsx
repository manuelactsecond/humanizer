"use client";

import type { DetectionResult } from "@/lib/types";
import { ScoreGauge } from "./score-gauge";
import { FeatureBar } from "./feature-bar";
import { HowDetectionWorks } from "./how-detection-works";

interface DetectionResultsProps {
  result: DetectionResult;
}

const FEATURE_LABELS: Record<string, { en: string; description: string }> = {
  perplexity: {
    en: "Perplexity",
    description: "How predictable the text is to language models",
  },
  burstiness: {
    en: "Burstiness",
    description: "Variation in sentence length and complexity",
  },
  vocabulary_richness: {
    en: "Vocabulary",
    description: "Lexical diversity and AI-typical word usage",
  },
  sentence_variance: {
    en: "Structure",
    description: "Monotony in sentence patterns and openers",
  },
};

const VERDICT_STYLES: Record<
  string,
  { label: string; bg: string; text: string }
> = {
  likely_human: {
    label: "Likely Human",
    bg: "bg-success/15",
    text: "text-success",
  },
  mixed: {
    label: "Mixed",
    bg: "bg-warning/15",
    text: "text-warning",
  },
  likely_ai: {
    label: "Likely AI",
    bg: "bg-destructive/15",
    text: "text-destructive",
  },
};

export function DetectionResults({ result }: DetectionResultsProps) {
  const verdict = VERDICT_STYLES[result.verdict] || VERDICT_STYLES.mixed;

  return (
    <div className="space-y-6">
      {/* How it works */}
      <HowDetectionWorks />

      {/* Header: Score + Verdict */}
      <div className="flex items-center gap-6">
        <div className="relative">
          <ScoreGauge score={result.overall_score} size={100} />
        </div>
        <div className="space-y-2">
          <span
            className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${verdict.bg} ${verdict.text}`}
          >
            {verdict.label}
          </span>
          <p className="text-sm text-muted-foreground">
            Confidence: {Math.round(result.confidence * 100)}%
          </p>
        </div>
      </div>

      {/* Feature Scores */}
      <div className="space-y-3">
        <h3 className="text-sm font-medium text-foreground">Feature Analysis</h3>
        {Object.entries(result.features).map(([key, value]) => {
          const meta = FEATURE_LABELS[key];
          return (
            <FeatureBar
              key={key}
              label={meta?.en || key}
              score={value}
              description={meta?.description}
            />
          );
        })}
      </div>

      {/* Explanation */}
      <div className="p-3 rounded-lg bg-muted/50 border border-border">
        <p className="text-sm text-secondary-foreground leading-relaxed">
          {result.explanation}
        </p>
      </div>
    </div>
  );
}
