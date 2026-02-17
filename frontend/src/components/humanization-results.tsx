"use client";

import { useState } from "react";
import type { HumanizationResult } from "@/lib/types";
import { FeatureBar } from "./feature-bar";
import { Copy, Check, ArrowDown } from "lucide-react";

interface HumanizationResultsProps {
  result: HumanizationResult;
}

export function HumanizationResults({ result }: HumanizationResultsProps) {
  const [tab, setTab] = useState<"output" | "comparison">("output");
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(result.humanized_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const scoreDelta =
    result.detection_before.overall_score -
    result.detection_after.overall_score;
  const improved = scoreDelta > 0;

  return (
    <div className="space-y-4">
      {/* Score comparison */}
      <div className="flex items-center justify-between p-4 rounded-lg bg-muted/50 border border-border">
        <div className="text-center">
          <p className="text-xs text-muted-foreground mb-1">Before</p>
          <p className="text-2xl font-bold text-destructive">
            {Math.round(result.detection_before.overall_score * 100)}%
          </p>
          <p className="text-xs text-muted-foreground">AI Score</p>
        </div>
        <div className="flex flex-col items-center">
          <ArrowDown
            className={`w-5 h-5 ${improved ? "text-success rotate-0" : "text-destructive rotate-180"}`}
          />
          <span
            className={`text-sm font-medium ${improved ? "text-success" : "text-destructive"}`}
          >
            {improved ? "-" : "+"}
            {Math.abs(Math.round(scoreDelta * 100))}%
          </span>
        </div>
        <div className="text-center">
          <p className="text-xs text-muted-foreground mb-1">After</p>
          <p className="text-2xl font-bold text-success">
            {Math.round(result.detection_after.overall_score * 100)}%
          </p>
          <p className="text-xs text-muted-foreground">AI Score</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-border">
        <button
          onClick={() => setTab("output")}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            tab === "output"
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          }`}
        >
          Humanized Text
        </button>
        <button
          onClick={() => setTab("comparison")}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            tab === "comparison"
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          }`}
        >
          Details
        </button>
      </div>

      {/* Tab Content */}
      {tab === "output" ? (
        <div className="relative">
          <div className="p-4 rounded-lg bg-muted/30 border border-border min-h-[200px] max-h-[400px] overflow-y-auto">
            <p className="text-sm leading-relaxed whitespace-pre-wrap">
              {result.humanized_text}
            </p>
          </div>
          <button
            onClick={handleCopy}
            className="absolute top-2 right-2 p-2 rounded-md bg-card hover:bg-secondary transition-colors"
            title="Copy to clipboard"
          >
            {copied ? (
              <Check className="w-4 h-4 text-success" />
            ) : (
              <Copy className="w-4 h-4 text-muted-foreground" />
            )}
          </button>
          <div className="flex justify-between text-xs text-muted-foreground mt-2">
            <span>
              Words: {result.word_count_original} → {result.word_count_humanized}
            </span>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Changes Summary */}
          {result.changes_summary.length > 0 && (
            <div>
              <h4 className="text-sm font-medium mb-2">Changes Made</h4>
              <ul className="space-y-1">
                {result.changes_summary.map((change, i) => (
                  <li
                    key={i}
                    className="text-xs text-muted-foreground flex items-start gap-2"
                  >
                    <span className="text-primary mt-0.5">-</span>
                    {change}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Feature comparison */}
          <div>
            <h4 className="text-sm font-medium mb-2">Feature Scores (After)</h4>
            <div className="space-y-2">
              {Object.entries(result.detection_after.features).map(
                ([key, value]) => (
                  <FeatureBar
                    key={key}
                    label={key.replace(/_/g, " ")}
                    score={value}
                  />
                ),
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
