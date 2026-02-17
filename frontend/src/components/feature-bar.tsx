"use client";

interface FeatureBarProps {
  label: string;
  score: number; // 0-1
  description?: string;
}

export function FeatureBar({ label, score, description }: FeatureBarProps) {
  const percentage = Math.round(score * 100);

  const getColor = (s: number) => {
    if (s < 0.35) return "bg-success";
    if (s < 0.65) return "bg-warning";
    return "bg-destructive";
  };

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span className="text-foreground">{label}</span>
        <span className="text-muted-foreground tabular-nums">{percentage}%</span>
      </div>
      <div className="h-2 rounded-full bg-muted overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ease-out ${getColor(score)}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      {description && (
        <p className="text-xs text-muted-foreground">{description}</p>
      )}
    </div>
  );
}
