"use client";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { toast } from "sonner";
import {
  Code2, Network, Layers, FileCode,
  Loader2, Sparkles, Copy, Check
} from "lucide-react";
import { api } from "@/lib/api/client";
import { cn } from "@/lib/utils/cn";

const ENG_MODES = [
  {
    id: "code",
    icon: Code2,
    label: "Code Generator",
    description: "React, HTML, or Vue code from design — powered by qwen2.5-coder:7b",
    color: "text-amber-600",
    bg: "bg-amber-50",
    border: "border-amber-200",
  },
  {
    id: "api",
    icon: Network,
    label: "API Designer",
    description: "REST API design with endpoints, models, authentication, and error codes",
    color: "text-blue-600",
    bg: "bg-blue-50",
    border: "border-blue-200",
  },
  {
    id: "architecture",
    icon: Layers,
    label: "Architecture Planner",
    description: "Full system architecture — components, data flow, infra, security, ADRs",
    color: "text-violet-600",
    bg: "bg-violet-50",
    border: "border-violet-200",
  },
];

const CODE_FORMATS = ["react", "html", "vue", "flutter"];
const SCALES = ["small", "medium", "enterprise"];

export default function EngineeringPage() {
  const [mode, setMode] = useState<string | null>(null);
  const [topic, setTopic] = useState("");
  const [codeFormat, setCodeFormat] = useState("react");
  const [scale, setScale] = useState("medium");
  const [result, setResult] = useState<any>(null);
  const [copied, setCopied] = useState<string | null>(null);

  const codeMutation = useMutation({
    mutationFn: (data: any) => api.post("/engineering/code", data).then(r => r.data),
    onSuccess: d => { setResult(d.result); toast.success("Code generated"); },
    onError: (e: any) => toast.error(e.response?.data?.detail || "Failed"),
  });

  const apiMutation = useMutation({
    mutationFn: (data: any) => api.post("/engineering/api-design", data).then(r => r.data),
    onSuccess: d => { setResult(d.result); toast.success("API design complete"); },
    onError: (e: any) => toast.error(e.response?.data?.detail || "Failed"),
  });

  const archMutation = useMutation({
    mutationFn: (data: any) => api.post("/engineering/architecture", data).then(r => r.data),
    onSuccess: d => { setResult(d.result); toast.success("Architecture plan ready"); },
    onError: (e: any) => toast.error(e.response?.data?.detail || "Failed"),
  });

  const isLoading = codeMutation.isPending || apiMutation.isPending || archMutation.isPending;

  const handleRun = () => {
    if (!mode || !topic.trim()) return;
    setResult(null);
    if (mode === "code") {
      codeMutation.mutate({ output_format: codeFormat, topic });
    } else if (mode === "api") {
      apiMutation.mutate({ topic, requirements: {}, user_stories: [] });
    } else if (mode === "architecture") {
      archMutation.mutate({ topic, requirements: {}, scale });
    }
  };

  const copyCode = async (code: string, id: string) => {
    await navigator.clipboard.writeText(code);
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="flex h-full">
      {/* Left */}
      <div className="w-80 flex-shrink-0 border-r border-gray-100 bg-white flex flex-col">
        <div className="p-4 border-b border-gray-100">
          <h2 className="text-sm font-semibold text-gray-800">Engineering Mode</h2>
          <p className="text-xs text-gray-500 mt-0.5">Generate code, APIs, or architecture</p>
        </div>

        <div className="flex-1 overflow-auto p-3 space-y-1.5">
          {ENG_MODES.map(m => {
            const Icon = m.icon;
            const isActive = mode === m.id;
            return (
              <button key={m.id} onClick={() => setMode(m.id)} className={cn(
                "w-full text-left p-3 rounded-xl border transition-all",
                isActive ? `${m.bg} ${m.border}` : "border-gray-100 hover:bg-gray-50"
              )}>
                <div className="flex items-start gap-2.5">
                  <div className={cn("w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5", isActive ? m.bg : "bg-gray-100")}>
                    <Icon className={cn("w-3.5 h-3.5", isActive ? m.color : "text-gray-500")} />
                  </div>
                  <div>
                    <div className={cn("text-xs font-semibold", isActive ? m.color : "text-gray-700")}>{m.label}</div>
                    <div className="text-[10px] text-gray-500 mt-0.5 leading-relaxed">{m.description}</div>
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        {mode && (
          <div className="p-4 border-t border-gray-100 space-y-3">
            <div>
              <label className="block text-[11px] font-medium text-gray-600 mb-1">Product / Feature</label>
              <input
                value={topic}
                onChange={e => setTopic(e.target.value)}
                placeholder="e.g. Loan repayment dashboard"
                className="w-full h-8 px-2.5 text-xs rounded-lg border border-gray-200 focus:outline-none focus:border-indigo-400"
              />
            </div>

            {mode === "code" && (
              <div>
                <label className="block text-[11px] font-medium text-gray-600 mb-1">Framework</label>
                <div className="flex flex-wrap gap-1">
                  {CODE_FORMATS.map(f => (
                    <button key={f} onClick={() => setCodeFormat(f)} className={cn(
                      "text-[10px] px-2 py-0.5 rounded-full border uppercase transition-all",
                      codeFormat === f ? "bg-amber-500 text-white border-amber-500" : "bg-gray-50 text-gray-600 border-gray-200"
                    )}>{f}</button>
                  ))}
                </div>
              </div>
            )}

            {mode === "architecture" && (
              <div>
                <label className="block text-[11px] font-medium text-gray-600 mb-1">Scale</label>
                <div className="flex gap-1">
                  {SCALES.map(s => (
                    <button key={s} onClick={() => setScale(s)} className={cn(
                      "text-[10px] px-2 py-0.5 rounded-full border capitalize transition-all",
                      scale === s ? "bg-violet-500 text-white border-violet-500" : "bg-gray-50 text-gray-600 border-gray-200"
                    )}>{s}</button>
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={handleRun}
              disabled={!topic.trim() || isLoading}
              className="w-full h-8 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-medium rounded-lg flex items-center justify-center gap-1.5 transition-colors disabled:opacity-50"
            >
              {isLoading ? <><Loader2 className="w-3.5 h-3.5 animate-spin" /> Generating...</> : <><Sparkles className="w-3.5 h-3.5" /> Generate</>}
            </button>
          </div>
        )}
      </div>

      {/* Right */}
      <div className="flex-1 overflow-auto p-6">
        {!mode && (
          <div className="h-full flex items-center justify-center">
            <div className="text-center max-w-sm">
              <div className="w-12 h-12 rounded-2xl bg-amber-50 flex items-center justify-center mx-auto mb-4">
                <Code2 className="w-6 h-6 text-amber-500" />
              </div>
              <h2 className="text-base font-semibold text-gray-900 mb-2">Engineering Team</h2>
              <p className="text-sm text-gray-500 leading-relaxed">
                Generate production code with qwen2.5-coder:7b, design REST APIs,
                or plan complete system architectures.
              </p>
            </div>
          </div>
        )}

        {isLoading && (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <div className="w-8 h-8 border-2 border-amber-200 border-t-amber-500 rounded-full animate-spin mx-auto mb-3" />
              <p className="text-sm text-gray-600">
                {mode === "code" ? "qwen2.5-coder:7b generating code..." : "deepseek-r1:8b designing..."}
              </p>
              <p className="text-xs text-gray-400 mt-1">Local model — may take 1-3 minutes</p>
            </div>
          </div>
        )}

        {result && !isLoading && (
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
            {/* Code files */}
            {result.files && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-semibold text-gray-800">Generated Files ({result.files.length})</h3>
                  {result.setup_instructions?.length > 0 && (
                    <div className="text-xs text-gray-500">
                      Setup: {result.setup_instructions[0]}
                    </div>
                  )}
                </div>
                {result.files.map((file: any, i: number) => (
                  <div key={i} className="bg-gray-900 rounded-xl overflow-hidden">
                    <div className="flex items-center justify-between px-4 py-2.5 border-b border-gray-700">
                      <span className="text-xs font-mono text-gray-300">{file.path}{file.filename}</span>
                      <button
                        onClick={() => copyCode(file.code, `file-${i}`)}
                        className="flex items-center gap-1 text-[10px] text-gray-400 hover:text-white transition-colors"
                      >
                        {copied === `file-${i}` ? <><Check className="w-3 h-3" /> Copied</> : <><Copy className="w-3 h-3" /> Copy</>}
                      </button>
                    </div>
                    <pre className="p-4 text-[11px] font-mono text-gray-300 overflow-x-auto max-h-64 leading-relaxed">
                      {file.code}
                    </pre>
                  </div>
                ))}
              </div>
            )}

            {/* API endpoints */}
            {result.endpoints && (
              <div className="bg-white rounded-xl border border-gray-200 p-5">
                <h3 className="text-sm font-semibold text-gray-800 mb-3">API Endpoints ({result.endpoints.length})</h3>
                <div className="space-y-2">
                  {result.endpoints.map((ep: any, i: number) => (
                    <div key={i} className="flex items-start gap-3 p-2.5 rounded-lg bg-gray-50">
                      <span className={cn(
                        "text-[10px] font-bold font-mono px-1.5 py-0.5 rounded flex-shrink-0",
                        ep.method === "GET" ? "bg-blue-100 text-blue-700" :
                        ep.method === "POST" ? "bg-emerald-100 text-emerald-700" :
                        ep.method === "PUT" ? "bg-amber-100 text-amber-700" :
                        "bg-red-100 text-red-700"
                      )}>{ep.method}</span>
                      <div>
                        <div className="text-xs font-mono text-gray-700">{ep.path}</div>
                        <div className="text-[11px] text-gray-500">{ep.description}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Architecture */}
            {result.components && (
              <div className="bg-white rounded-xl border border-gray-200 p-5">
                <h3 className="text-sm font-semibold text-gray-800 mb-1">{result.architecture_name}</h3>
                <p className="text-xs text-gray-500 mb-3">{result.overview}</p>
                <div className="grid grid-cols-2 gap-2">
                  {result.components.map((comp: any, i: number) => (
                    <div key={i} className="p-2.5 rounded-lg bg-gray-50 border border-gray-100">
                      <div className="text-xs font-semibold text-gray-700">{comp.name}</div>
                      <div className="text-[10px] text-indigo-600 font-mono">{comp.technology}</div>
                      <div className="text-[10px] text-gray-500 mt-0.5">{comp.responsibility}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}
