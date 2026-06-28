"use client";
import { useState } from "react";
import { Copy, Check, FileText, Eye } from "lucide-react";
import { cn } from "@/lib/utils/cn";

interface Props {
  result: any;
  type: string;
  title: string;
}

export function ArtifactResultPanel({ result, type, title }: Props) {
  const [view, setView] = useState<"preview" | "json">("preview");
  const [copied, setCopied] = useState(false);

  const copyJSON = async () => {
    await navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3 border-b border-gray-100">
        <h3 className="text-sm font-semibold text-gray-800">{title}</h3>
        <div className="flex items-center gap-2">
          <div className="flex items-center bg-gray-100 rounded-lg p-0.5">
            <button
              onClick={() => setView("preview")}
              className={cn("flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium transition-all",
                view === "preview" ? "bg-white shadow-sm text-gray-900" : "text-gray-500")}
            >
              <Eye className="w-3 h-3" /> Preview
            </button>
            <button
              onClick={() => setView("json")}
              className={cn("flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium transition-all",
                view === "json" ? "bg-white shadow-sm text-gray-900" : "text-gray-500")}
            >
              <FileText className="w-3 h-3" /> JSON
            </button>
          </div>
          <button onClick={copyJSON} className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700 transition-colors">
            {copied ? <><Check className="w-3 h-3 text-emerald-500" /> Copied</> : <><Copy className="w-3 h-3" /> Copy</>}
          </button>
        </div>
      </div>

      {view === "preview" ? (
        <div className="p-5 overflow-auto max-h-[600px]">
          <PreviewByType result={result} type={type} />
        </div>
      ) : (
        <div className="overflow-auto max-h-[600px]">
          <pre className="p-5 text-xs font-mono text-gray-700 whitespace-pre-wrap leading-relaxed">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

function PreviewByType({ result, type }: { result: any; type: string }) {
  if (type === "personas" && result.personas) {
    return (
      <div className="space-y-4">
        {result.personas.map((p: any, i: number) => (
          <div key={i} className="p-4 rounded-xl border border-gray-100 bg-gray-50">
            <div className="flex items-start gap-3 mb-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-white font-semibold text-sm flex-shrink-0">
                {p.name?.charAt(0) || "?"}
              </div>
              <div>
                <div className="text-sm font-semibold text-gray-900">{p.name}</div>
                <div className="text-xs text-gray-500">{p.role} · Age {p.age}</div>
              </div>
            </div>
            <blockquote className="text-xs italic text-gray-600 border-l-2 border-indigo-200 pl-3 mb-3">
              "{p.quote}"
            </blockquote>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div>
                <div className="font-medium text-gray-700 mb-1">Goals</div>
                <ul className="space-y-0.5">
                  {p.goals?.map((g: string, j: number) => <li key={j} className="text-gray-500 flex gap-1"><span className="text-indigo-400">+</span>{g}</li>)}
                </ul>
              </div>
              <div>
                <div className="font-medium text-gray-700 mb-1">Frustrations</div>
                <ul className="space-y-0.5">
                  {p.frustrations?.map((f: string, j: number) => <li key={j} className="text-gray-500 flex gap-1"><span className="text-red-400">−</span>{f}</li>)}
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (type === "user_stories" && result.user_stories) {
    return (
      <div className="space-y-3">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-sm font-semibold text-gray-800">{result.epic}</h4>
          <span className="text-xs text-gray-500">{result.total_story_points} story points</span>
        </div>
        {result.user_stories.map((s: any, i: number) => (
          <div key={i} className="p-3 rounded-lg border border-gray-100 bg-gray-50">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-[10px] font-mono bg-indigo-100 text-indigo-700 px-1.5 py-0.5 rounded">{s.id}</span>
              <span className={cn("text-[10px] px-1.5 py-0.5 rounded font-medium",
                s.priority === "Must Have" ? "bg-red-100 text-red-700" :
                s.priority === "Should Have" ? "bg-amber-100 text-amber-700" :
                "bg-gray-100 text-gray-600")}>{s.priority}</span>
              <span className="text-xs text-gray-500 ml-auto">{s.story_points} pts</span>
            </div>
            <p className="text-xs text-gray-700 mb-2">
              <span className="font-medium">As a</span> {s.as_a}, <span className="font-medium">I want to</span> {s.i_want} <span className="font-medium">so that</span> {s.so_that}
            </p>
            {s.acceptance_criteria?.length > 0 && (
              <details className="mt-2">
                <summary className="text-[10px] text-gray-500 cursor-pointer hover:text-gray-700">
                  {s.acceptance_criteria.length} acceptance criteria
                </summary>
                <ul className="mt-1.5 space-y-1">
                  {s.acceptance_criteria.map((ac: string, j: number) => (
                    <li key={j} className="text-[10px] text-gray-600 flex gap-1.5">
                      <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>{ac}
                    </li>
                  ))}
                </ul>
              </details>
            )}
          </div>
        ))}
      </div>
    );
  }

  if (type === "competitor" && result.competitors) {
    return (
      <div className="space-y-3">
        <p className="text-xs text-gray-600 italic">{result.market_overview}</p>
        {result.competitors.map((c: any, i: number) => (
          <div key={i} className="p-3 rounded-lg border border-gray-100 bg-gray-50">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-sm font-semibold text-gray-800">{c.name}</span>
              <span className="text-[10px] bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">{c.category}</span>
              <span className="text-[10px] text-gray-500 ml-auto">UX: {c.ux_quality}</span>
            </div>
            <p className="text-xs text-gray-600 mb-2">{c.description}</p>
            <div className="grid grid-cols-2 gap-2 text-[10px]">
              <div>
                <div className="font-medium text-emerald-700 mb-0.5">Strengths</div>
                {c.strengths?.map((s: string, j: number) => <div key={j} className="text-gray-600">+ {s}</div>)}
              </div>
              <div>
                <div className="font-medium text-red-600 mb-0.5">Weaknesses</div>
                {c.weaknesses?.map((w: string, j: number) => <div key={j} className="text-gray-600">− {w}</div>)}
              </div>
            </div>
          </div>
        ))}
        {result.market_gaps?.length > 0 && (
          <div className="p-3 rounded-lg bg-indigo-50 border border-indigo-100">
            <div className="text-xs font-semibold text-indigo-700 mb-2">Market Gaps</div>
            {result.market_gaps.map((g: string, i: number) => (
              <div key={i} className="text-xs text-indigo-600 flex gap-1.5">
                <span>→</span>{g}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  if (type === "test_cases" && result.test_cases) {
    return (
      <div className="space-y-3">
        <div className="grid grid-cols-4 gap-2 mb-4">
          {Object.entries(result.coverage_summary || {}).map(([k, v]) => (
            <div key={k} className="text-center p-2 bg-gray-50 rounded-lg border border-gray-100">
              <div className="text-lg font-bold text-gray-800">{v as any}</div>
              <div className="text-[10px] text-gray-500 capitalize">{k.replace("_", " ")}</div>
            </div>
          ))}
        </div>
        {result.test_cases.map((tc: any, i: number) => (
          <div key={i} className="p-3 rounded-lg border border-gray-100 bg-gray-50">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-[10px] font-mono bg-indigo-100 text-indigo-700 px-1.5 py-0.5 rounded">{tc.id}</span>
              <span className="text-xs font-medium text-gray-700">{tc.title}</span>
              <span className={cn("text-[10px] px-1.5 py-0.5 rounded ml-auto",
                tc.priority === "P1" ? "bg-red-100 text-red-700" :
                tc.priority === "P2" ? "bg-amber-100 text-amber-700" :
                "bg-gray-100 text-gray-600")}>{tc.priority}</span>
            </div>
            <div className="text-[10px] text-gray-500 mb-2">{tc.category}</div>
            <ol className="space-y-1">
              {tc.steps?.map((s: any, j: number) => (
                <li key={j} className="text-[10px] text-gray-600 flex gap-2">
                  <span className="text-gray-400 w-4 flex-shrink-0">{s.step}.</span>
                  <span>{s.action} → <span className="text-emerald-600">{s.expected}</span></span>
                </li>
              ))}
            </ol>
          </div>
        ))}
      </div>
    );
  }

  // Generic key-value preview
  return (
    <div className="space-y-3">
      {Object.entries(result).map(([key, value]) => {
        if (key === "error" || key === "raw") return null;
        return (
          <div key={key} className="p-3 bg-gray-50 rounded-lg border border-gray-100">
            <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-1">
              {key.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-gray-700">
              {typeof value === "string" ? value :
               Array.isArray(value) ? value.map((v, i) => <div key={i}>• {typeof v === "string" ? v : JSON.stringify(v)}</div>) :
               <pre className="text-[10px] font-mono whitespace-pre-wrap">{JSON.stringify(value, null, 2)}</pre>}
            </div>
          </div>
        );
      })}
    </div>
  );
}
