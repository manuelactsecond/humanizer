"use client";

import type { Intensity } from "@/lib/types";

interface IntensitySelectorProps {
  value: Intensity;
  onChange: (value: Intensity) => void;
  disabled?: boolean;
}

const OPTIONS: { value: Intensity; label: string; description: string }[] = [
  { value: "light", label: "Light", description: "Minimal edits — fixes obvious AI tells" },
  { value: "medium", label: "Medium", description: "Balanced rewrite — natural flow" },
  { value: "aggressive", label: "Aggressive", description: "Full restyle — max naturalness" },
];

export function IntensitySelector({ value, onChange, disabled }: IntensitySelectorProps) {
  return (
    <div className="flex gap-1.5">
      {OPTIONS.map((opt) => {
        const isSelected = value === opt.value;
        return (
          <button
            key={opt.value}
            type="button"
            onClick={() => onChange(opt.value)}
            disabled={disabled}
            className={`flex-1 px-2 py-1.5 rounded-lg border text-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
              isSelected
                ? "border-primary bg-primary/10 text-foreground"
                : "border-border bg-card text-muted-foreground hover:border-muted-foreground/50"
            }`}
          >
            <span className="text-xs font-medium">{opt.label}</span>
            <p className={`text-[10px] leading-tight mt-0.5 ${isSelected ? "text-muted-foreground" : "text-muted-foreground/60"}`}>
              {opt.description}
            </p>
          </button>
        );
      })}
    </div>
  );
}
