"use client";

import { useState } from "react";
import { useDetection } from "@/hooks/use-detection";
import { useHumanization } from "@/hooks/use-humanization";
import { DetectionResults } from "@/components/detection-results";
import { HumanizationResults } from "@/components/humanization-results";
import type { Language, Intensity } from "@/lib/types";
import { IntensitySelector } from "@/components/intensity-selector";
import { HumanizationProgress } from "@/components/humanization-progress";
import { HowDetectionWorks } from "@/components/how-detection-works";
import { Shield, Sparkles, Loader2, RotateCcw } from "lucide-react";

export default function Home() {
  const [text, setText] = useState("");
  const [language, setLanguage] = useState<Language>("en");
  const [intensity, setIntensity] = useState<Intensity>("medium");
  const [activeView, setActiveView] = useState<"none" | "detection" | "humanization">("none");

  const detection = useDetection();
  const humanization = useHumanization();

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const canSubmit = text.trim().length >= 50;

  const handleDetect = async () => {
    if (!canSubmit) return;
    setActiveView("detection");
    humanization.reset();
    await detection.detect(text, language);
  };

  const handleHumanize = async () => {
    if (!canSubmit) return;
    setActiveView("humanization");
    detection.reset();
    await humanization.humanize(text, language, intensity);
  };

  const handleReset = () => {
    setText("");
    setActiveView("none");
    detection.reset();
    humanization.reset();
  };

  const isLoading = detection.loading || humanization.loading;

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b border-border px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <Shield className="w-5 h-5 text-primary-foreground" />
            </div>
            <h1 className="text-xl font-bold">Humanizer</h1>
            <span className="text-xs text-muted-foreground px-2 py-0.5 rounded-full bg-muted">
              v0.1
            </span>
          </div>
          <p className="text-sm text-muted-foreground hidden sm:block">
            AI Text Detection & Humanization
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
          {/* Left Panel: Input */}
          <div className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">Input Text</h2>
              {text && (
                <button
                  onClick={handleReset}
                  className="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
                >
                  <RotateCcw className="w-3 h-3" />
                  Reset
                </button>
              )}
            </div>

            {/* Text Area */}
            <div className="relative flex-1">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your text here to analyze or humanize... (minimum 50 characters)"
                className="w-full h-full min-h-[300px] p-4 rounded-lg bg-card border border-border text-sm leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-ring placeholder:text-muted-foreground"
                disabled={isLoading}
              />
              <div className="absolute bottom-3 right-3 text-xs text-muted-foreground tabular-nums">
                {text.length} chars · {wordCount} words
              </div>
            </div>

            {/* Controls */}
            <div className="flex flex-wrap items-center gap-3">
              {/* Language Selector */}
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value as Language)}
                className="px-3 py-2 rounded-lg bg-card border border-border text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                disabled={isLoading}
              >
                <option value="en">English</option>
                <option value="es">Espanol (Espana)</option>
              </select>

              {/* Intensity Selector */}
              <IntensitySelector value={intensity} onChange={setIntensity} disabled={isLoading} />

              <div className="flex-1" />

              {/* Action Buttons */}
              <button
                onClick={handleDetect}
                disabled={!canSubmit || isLoading}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-secondary text-secondary-foreground text-sm font-medium hover:bg-secondary/80 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {detection.loading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Shield className="w-4 h-4" />
                )}
                Detect AI
              </button>

              <button
                onClick={handleHumanize}
                disabled={!canSubmit || isLoading}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {humanization.loading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Sparkles className="w-4 h-4" />
                )}
                Humanize
              </button>
            </div>

            {/* Minimum length hint */}
            {text.length > 0 && text.length < 50 && (
              <p className="text-xs text-warning">
                Minimum 50 characters required ({50 - text.length} more needed)
              </p>
            )}
          </div>

          {/* Right Panel: Results */}
          <div className="flex flex-col gap-4">
            <h2 className="text-lg font-semibold">Results</h2>

            <div className="flex-1 p-6 rounded-lg bg-card border border-border overflow-y-auto min-h-[300px]">
              {/* Loading State: Detection */}
              {detection.loading && (
                <div className="flex flex-col items-center justify-center h-full gap-4">
                  <Loader2 className="w-8 h-8 animate-spin text-primary" />
                  <p className="text-sm text-muted-foreground">
                    Analyzing text for AI patterns...
                  </p>
                </div>
              )}

              {/* Loading State: Humanization */}
              {humanization.loading && (
                <HumanizationProgress
                  isActive={humanization.loading}
                  isComplete={false}
                />
              )}

              {/* Error State */}
              {(detection.error || humanization.error) && !isLoading && (
                <div className="flex flex-col items-center justify-center h-full gap-3">
                  <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20">
                    <p className="text-sm text-destructive">
                      {detection.error || humanization.error}
                    </p>
                  </div>
                </div>
              )}

              {/* Detection Results */}
              {activeView === "detection" &&
                detection.result &&
                !detection.loading && (
                  <div className="animate-fade-in">
                    <DetectionResults result={detection.result} />
                  </div>
                )}

              {/* Humanization Results */}
              {activeView === "humanization" &&
                humanization.result &&
                !humanization.loading && (
                  <div className="animate-fade-in">
                    <HumanizationResults result={humanization.result} />
                  </div>
                )}

              {/* Empty State */}
              {activeView === "none" && !isLoading && (
                <div className="flex flex-col gap-4 h-full">
                  {/* Action cards */}
                  <div className="space-y-3">
                    <div className="flex items-start gap-3 p-3 rounded-lg bg-muted/30 border border-border">
                      <Shield className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                      <div>
                        <p className="text-sm font-medium">Detect AI</p>
                        <p className="text-xs text-muted-foreground mt-0.5">
                          Analyzes your text against 4 statistical tests to determine if it was written by AI, human, or a mix.
                        </p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3 p-3 rounded-lg bg-muted/30 border border-border">
                      <Sparkles className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                      <div>
                        <p className="text-sm font-medium">Humanize</p>
                        <p className="text-xs text-muted-foreground mt-0.5">
                          Rewrites AI-generated text to sound naturally human while preserving the original meaning.
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* How detection works */}
                  <HowDetectionWorks />

                  <p className="text-xs text-muted-foreground text-center mt-auto">
                    Paste text and click &quot;Detect AI&quot; or &quot;Humanize&quot; to get started
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border px-6 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between text-xs text-muted-foreground">
          <span>Humanizer v0.1.0</span>
          <span>EN / ES (Spain) supported</span>
        </div>
      </footer>
    </div>
  );
}
