"use client";

import { useState } from "react";
import { Info, ChevronDown, ChevronUp } from "lucide-react";

export function HowDetectionWorks() {
  const [open, setOpen] = useState(false);

  return (
    <div className="rounded-lg border border-border overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-2 px-3 py-2 text-xs text-muted-foreground hover:text-foreground transition-colors"
      >
        <Info className="w-3.5 h-3.5 shrink-0" />
        <span className="flex-1 text-left">How does detection work?</span>
        {open ? (
          <ChevronUp className="w-3.5 h-3.5 shrink-0" />
        ) : (
          <ChevronDown className="w-3.5 h-3.5 shrink-0" />
        )}
      </button>

      {open && (
        <div className="px-3 pb-3 space-y-2 text-xs text-secondary-foreground leading-relaxed animate-fade-in">
          <p className="text-muted-foreground">
            Four independent tests analyze your text from different angles, then combine into a single score.
          </p>

          <div className="space-y-1.5">
            <p>
              <span className="font-medium text-foreground">Perplexity (35%)</span>{" "}
              — Measures how predictable the text is. AI follows highly probable word patterns; human writing surprises more.
            </p>
            <p>
              <span className="font-medium text-foreground">Burstiness (25%)</span>{" "}
              — Humans write with varied rhythm: short punchy sentences mixed with longer ones. AI tends toward uniform length.
            </p>
            <p>
              <span className="font-medium text-foreground">Vocabulary (20%)</span>{" "}
              — Checks for AI-typical words (&quot;delve&quot;, &quot;moreover&quot;, &quot;it&apos;s important to note&quot;) and measures lexical diversity.
            </p>
            <p>
              <span className="font-medium text-foreground">Structure (20%)</span>{" "}
              — Looks at sentence opener variety and syntactic patterns. AI repeats the same constructions.
            </p>
          </div>

          <p className="text-muted-foreground pt-1 border-t border-border">
            Below 35% = likely human. Above 65% = likely AI. In between = mixed signals.
          </p>
        </div>
      )}
    </div>
  );
}
