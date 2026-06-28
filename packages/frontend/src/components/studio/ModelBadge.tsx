import { cn } from "@/lib/utils/cn";
import { Cpu } from "lucide-react";

const MODEL_CONFIG: Record<string, { label: string; color: string }> = {
  "claude-haiku-4-5": { label: "Haiku", color: "text-emerald-600 bg-emerald-50" },
  "claude-sonnet-4-5": { label: "Sonnet", color: "text-blue-600 bg-blue-50" },
  "claude-opus-4-5": { label: "Opus", color: "text-violet-600 bg-violet-50" },
  "gpt-4o-mini": { label: "GPT-4o mini", color: "text-surface-600 bg-surface-50" },
  "gpt-4o": { label: "GPT-4o", color: "text-surface-700 bg-surface-100" },
};

export function ModelBadge({ model }: { model: string }) {
  const cfg = MODEL_CONFIG[model] || { label: model, color: "text-surface-500 bg-surface-50" };
  return (
    <span className={cn(
      "inline-flex items-center gap-1 text-2xs font-medium px-1.5 py-0.5 rounded",
      cfg.color
    )}>
      <Cpu className="w-2.5 h-2.5" />
      {cfg.label}
    </span>
  );
}
