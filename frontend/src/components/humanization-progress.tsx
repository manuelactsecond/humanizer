"use client";

import { useState, useEffect, useRef } from "react";
import { Check, Loader2, Search, Sparkles, Paintbrush, ShieldCheck } from "lucide-react";

interface HumanizationProgressProps {
  isActive: boolean;
  isComplete: boolean;
}

const STAGES = [
  { label: "Analyzing text patterns", icon: Search, duration: 3000 },
  { label: "Rewriting with AI", icon: Sparkles, duration: 14000 },
  { label: "Polishing vocabulary & grammar", icon: Paintbrush, duration: 3000 },
  { label: "Running final quality check", icon: ShieldCheck, duration: 4000 },
];

const TOTAL_DURATION = STAGES.reduce((sum, s) => sum + s.duration, 0);

export function HumanizationProgress({ isActive, isComplete }: HumanizationProgressProps) {
  const [currentStage, setCurrentStage] = useState(0);
  const [stageProgress, setStageProgress] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const startTimeRef = useRef(Date.now());
  const timeoutsRef = useRef<NodeJS.Timeout[]>([]);

  // Stage advancement
  useEffect(() => {
    if (!isActive) return;

    startTimeRef.current = Date.now();
    setCurrentStage(0);
    setStageProgress(0);
    setElapsed(0);

    const timeouts: NodeJS.Timeout[] = [];
    let accumulated = 0;

    STAGES.forEach((stage, i) => {
      // Start stage: reset progress then trigger fill
      timeouts.push(
        setTimeout(() => {
          setCurrentStage(i);
          setStageProgress(0);
          requestAnimationFrame(() => {
            requestAnimationFrame(() => {
              setStageProgress(i === STAGES.length - 1 ? 90 : 100);
            });
          });
        }, accumulated)
      );
      accumulated += stage.duration;
    });

    timeoutsRef.current = timeouts;
    return () => timeouts.forEach(clearTimeout);
  }, [isActive]);

  // Elapsed timer
  useEffect(() => {
    if (!isActive) return;
    const interval = setInterval(() => {
      setElapsed(Math.floor((Date.now() - startTimeRef.current) / 1000));
    }, 1000);
    return () => clearInterval(interval);
  }, [isActive]);

  // Fast-forward on completion
  useEffect(() => {
    if (isComplete) {
      timeoutsRef.current.forEach(clearTimeout);
      setCurrentStage(STAGES.length);
      setStageProgress(100);
    }
  }, [isComplete]);

  // Calculate overall progress
  const completedDuration = STAGES.slice(0, Math.min(currentStage, STAGES.length)).reduce(
    (sum, s) => sum + s.duration,
    0
  );
  const currentStageDuration = currentStage < STAGES.length ? STAGES[currentStage].duration : 0;
  const overallProgress = Math.min(
    ((completedDuration + (stageProgress / 100) * currentStageDuration) / TOTAL_DURATION) * 100,
    isComplete ? 100 : 95
  );

  return (
    <div className="flex flex-col gap-5 py-4">
      {/* Overall progress bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>Humanizing...</span>
          <span>{Math.round(overallProgress)}%</span>
        </div>
        <div className="h-1.5 rounded-full bg-muted overflow-hidden">
          <div
            className="h-full rounded-full bg-primary"
            style={{
              width: `${overallProgress}%`,
              transition: "width 1s linear",
            }}
          />
        </div>
      </div>

      {/* Stage list */}
      <div className="space-y-3">
        {STAGES.map((stage, i) => {
          const Icon = stage.icon;
          const isDone = i < currentStage || isComplete;
          const isCurrent = i === currentStage && !isComplete;
          const isPending = i > currentStage && !isComplete;

          return (
            <div key={i} className="flex items-start gap-3">
              {/* Status icon */}
              <div className="mt-0.5">
                {isDone ? (
                  <Check className="w-4 h-4 text-success" />
                ) : isCurrent ? (
                  <Loader2 className="w-4 h-4 animate-spin text-primary" />
                ) : (
                  <div className="w-4 h-4 rounded-full border border-border" />
                )}
              </div>

              {/* Label + progress */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <Icon
                    className={`w-3.5 h-3.5 shrink-0 ${
                      isDone
                        ? "text-muted-foreground"
                        : isCurrent
                          ? "text-foreground"
                          : "text-muted-foreground/40"
                    }`}
                  />
                  <span
                    className={`text-sm ${
                      isDone
                        ? "text-muted-foreground"
                        : isCurrent
                          ? "text-foreground font-medium"
                          : "text-muted-foreground/40"
                    }`}
                  >
                    {stage.label}
                    {isCurrent && currentStage === STAGES.length - 1 && elapsed > 22 && (
                      <span className="text-muted-foreground font-normal"> — Almost there...</span>
                    )}
                  </span>
                </div>

                {isCurrent && (
                  <div className="h-1 mt-1.5 rounded-full bg-muted overflow-hidden">
                    <div
                      className="h-full rounded-full bg-primary/60"
                      style={{
                        width: `${stageProgress}%`,
                        transition: `width ${stage.duration}ms linear`,
                      }}
                    />
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer */}
      <div className="flex justify-between text-xs text-muted-foreground pt-2 border-t border-border">
        <span>This usually takes 15-25 seconds</span>
        <span className="tabular-nums">{elapsed}s elapsed</span>
      </div>
    </div>
  );
}
