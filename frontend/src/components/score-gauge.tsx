"use client";

interface ScoreGaugeProps {
  score: number; // 0-1
  size?: number;
  label?: string;
}

export function ScoreGauge({ score, size = 120, label }: ScoreGaugeProps) {
  const radius = (size - 12) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = circumference * (1 - score);

  // Color: green (human) -> yellow (mixed) -> red (AI)
  const getColor = (s: number) => {
    if (s < 0.35) return "#22c55e"; // green
    if (s < 0.65) return "#eab308"; // yellow
    return "#e54545"; // red
  };

  const color = getColor(score);
  const percentage = Math.round(score * 100);

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width={size} height={size} className="-rotate-90">
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--color-border)"
          strokeWidth="8"
        />
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={progress}
          strokeLinecap="round"
          className="transition-all duration-700 ease-out"
        />
      </svg>
      {/* Center text - positioned over the SVG */}
      <div
        className="flex flex-col items-center justify-center absolute"
        style={{
          width: size,
          height: size,
          marginTop: -(size + 8),
        }}
      >
        <span
          className="font-bold tabular-nums"
          style={{ color, fontSize: size / 4 }}
        >
          {percentage}%
        </span>
      </div>
      {label && (
        <span className="text-sm text-muted-foreground">{label}</span>
      )}
    </div>
  );
}
