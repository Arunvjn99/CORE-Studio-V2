"use client";
import { useState, useRef, useEffect, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import {
  Users, Search, FileText, BarChart3, BookOpen, ChevronRight,
  Loader2, Sparkles, GitBranch, Map, Workflow, Upload, X, ImageIcon, FileCheck, Zap
} from "lucide-react";
import { api } from "@/lib/api/client";
import { cn } from "@/lib/utils/cn";
import { ArtifactResultPanel } from "@/components/shared/ArtifactResultPanel";
import { FlowCanvas } from "@/components/studio/FlowCanvas";

const RESEARCH_TYPES = [
  {
    id: "user_flow",
    icon: GitBranch,
    label: "User Flow",
    description: "Node-based flow diagram with screens, decisions & UX analysis",
    color: "text-fuchsia-600",
    bg: "bg-fuchsia-50",
    border: "border-fuchsia-200",
    example: "User enrollment flow for retirement portal",
    isFlow: true,
    imageTip: "Upload a screen to map its actual flows",
  },
  {
    id: "journey_map",
    icon: Map,
    label: "Journey Map",
    description: "Customer journey with stages, emotions & opportunities",
    color: "text-cyan-600",
    bg: "bg-cyan-50",
    border: "border-cyan-200",
    example: "Loan application customer journey",
    isFlow: true,
    imageTip: "Upload a screen to map the journey from its UI",
  },
  {
    id: "task_flow",
    icon: Workflow,
    label: "Task Flow",
    description: "Step-by-step task breakdown with decisions and system actions",
    color: "text-violet-600",
    bg: "bg-violet-50",
    border: "border-violet-200",
    example: "Submit loan repayment task flow",
    isFlow: true,
    imageTip: "Upload a screen to extract exact task steps",
  },
  {
    id: "user_stories",
    icon: FileText,
    label: "User Stories + AC",
    description: "Generate user stories with acceptance criteria in Gherkin format",
    color: "text-emerald-600",
    bg: "bg-emerald-50",
    border: "border-emerald-200",
    example: "Loan repayment dashboard feature",
    imageTip: "Upload a screen to generate stories from its UI",
  },
  {
    id: "personas",
    icon: Users,
    label: "User Personas",
    description: "Create detailed user personas with goals, frustrations, and scenarios",
    color: "text-violet-600",
    bg: "bg-violet-50",
    border: "border-violet-200",
    example: "Retirement portal mobile app",
    imageTip: "Upload a screen to infer target personas",
  },
  {
    id: "competitor",
    icon: Search,
    label: "Competitor Analysis",
    description: "Analyse 4 competitors — strengths, weaknesses, market gaps",
    color: "text-blue-600",
    bg: "bg-blue-50",
    border: "border-blue-200",
    example: "Loan repayment mobile apps",
    imageTip: "Upload a competitor screen to analyze",
  },
  {
    id: "prd",
    icon: BookOpen,
    label: "Product Requirements",
    description: "Full PRD with objectives, requirements, constraints, and timeline",
    color: "text-amber-600",
    bg: "bg-amber-50",
    border: "border-amber-200",
    example: "Benefits enrollment platform",
    imageTip: "Upload a screen to generate PRD from its features",
  },
  {
    id: "market",
    icon: BarChart3,
    label: "Market Research",
    description: "Market size, trends, user needs, regulatory considerations",
    color: "text-rose-600",
    bg: "bg-rose-50",
    border: "border-rose-200",
    example: "Healthcare insurance comparison tool",
    imageTip: "Upload a screen to ground market research",
  },
];

const DOMAINS = ["retirement", "loan", "insurance", "healthcare", "banking", "ecommerce", "general"];

export default function AnalystPage() {
  const [activeType, setActiveType] = useState<string | null>(null);
  const [topic, setTopic] = useState("");
  const [domain, setDomain] = useState("general");
  const [context, setContext] = useState("");
  const [result, setResult] = useState<any>(null);
  const [tokenUsage, setTokenUsage] = useState<{total: number; calls: number; model: string} | null>(null);
  const [flowResult, setFlowResult] = useState<any>(null);
  const [flowSteps, setFlowSteps] = useState<string[]>([]);
  const [flowLoading, setFlowLoading] = useState(false);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const activeConfig = RESEARCH_TYPES.find(r => r.id === activeType);
  const isFlow = activeConfig?.isFlow;

  useEffect(() => () => { wsRef.current?.close(); }, []);

  // Reset image when switching types
  useEffect(() => {
    setImageFile(null);
    setImagePreview(null);
    setResult(null);
    setTokenUsage(null);
    setFlowResult(null);
    setFlowSteps([]);
  }, [activeType]);

  const handleImageSelect = useCallback((file: File) => {
    if (!file.type.startsWith("image/")) { toast.error("Please upload an image file"); return; }
    if (file.size > 10 * 1024 * 1024) { toast.error("Image must be under 10MB"); return; }
    setImageFile(file);
    const reader = new FileReader();
    reader.onload = e => setImagePreview(e.target?.result as string);
    reader.readAsDataURL(file);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) handleImageSelect(file);
  }, [handleImageSelect]);

  // Build multipart FormData for API calls
  const buildFormData = (extraFields: Record<string, string>) => {
    const fd = new FormData();
    Object.entries(extraFields).forEach(([k, v]) => fd.append(k, v));
    if (imageFile) fd.append("image", imageFile);
    return fd;
  };

  const researchMutation = useMutation({
    mutationFn: (fd: FormData) =>
      api.post("/analyst/research", fd, { headers: { "Content-Type": "multipart/form-data" } }).then(r => r.data),
    onSuccess: (data) => {
      setResult(data.result);
      if (data.token_usage) setTokenUsage(data.token_usage);
      if (data.image_used) toast.success(`${activeType} research complete (with screen analysis)`);
      else toast.success(`${activeType} research complete`);
    },
    onError: (e: any) => toast.error(e.response?.data?.detail || "Research failed"),
  });

  const flowMutation = useMutation({
    mutationFn: (fd: FormData) =>
      api.post("/analyst/flow", fd, { headers: { "Content-Type": "multipart/form-data" } }).then(r => r.data),
    onSuccess: (data) => { connectFlowWS(data.generation_id); },
    onError: () => { toast.error("Flow generation failed"); setFlowLoading(false); },
  });

  const connectFlowWS = (genId: string) => {
    wsRef.current?.close();
    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000"}/ws/design/${genId}`);
    wsRef.current = ws;
    ws.onopen = () => {
      const ping = setInterval(() => ws.readyState === 1 && ws.send("ping"), 20000);
      ws.onclose = () => clearInterval(ping);
    };
    ws.onmessage = (e) => {
      const ev = JSON.parse(e.data);
      if (ev.type === "pong") return;
      if (ev.message) setFlowSteps(prev => [...prev, ev.message]);
      if (ev.type === "complete" && ev.result) {
        setFlowResult(ev.result);
        setFlowLoading(false);
        toast.success(imageFile ? "Flow generated from screen" : "Flow generated");
      }
      if (ev.type === "error") { toast.error(ev.message); setFlowLoading(false); }
    };
  };

  const handleRun = () => {
    if (!activeType || !topic.trim()) return;
    if (isFlow) {
      setFlowResult(null);
      setFlowSteps([]);
      setFlowLoading(true);
      const fd = buildFormData({ prompt: topic, flow_type: activeType, domain });
      flowMutation.mutate(fd);
    } else {
      setResult(null);
      const fd = buildFormData({ research_type: activeType, topic, domain, context });
      researchMutation.mutate(fd);
    }
  };

  return (
    <div className="flex h-full">
      {/* Left — type selector + form */}
      <div className="w-80 flex-shrink-0 border-r border-gray-100 bg-white flex flex-col">
        <div className="p-4 border-b border-gray-100">
          <h2 className="text-sm font-semibold text-gray-800">Research Type</h2>
          <p className="text-xs text-gray-500 mt-0.5">Select what you want to generate</p>
        </div>

        <div className="flex-1 overflow-auto p-3 space-y-1.5">
          {RESEARCH_TYPES.map(rt => {
            const Icon = rt.icon;
            const isActive = activeType === rt.id;
            return (
              <button
                key={rt.id}
                onClick={() => { setActiveType(rt.id); setTopic(rt.example); }}
                className={cn(
                  "w-full text-left p-3 rounded-xl border transition-all",
                  isActive ? `${rt.bg} ${rt.border} border` : "border-gray-100 hover:border-gray-200 hover:bg-gray-50"
                )}
              >
                <div className="flex items-start gap-2.5">
                  <div className={cn("w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5", isActive ? rt.bg : "bg-gray-100")}>
                    <Icon className={cn("w-3.5 h-3.5", isActive ? rt.color : "text-gray-500")} />
                  </div>
                  <div>
                    <div className={cn("text-xs font-semibold", isActive ? rt.color : "text-gray-700")}>{rt.label}</div>
                    <div className="text-[10px] text-gray-500 mt-0.5 leading-relaxed">{rt.description}</div>
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        {/* Form */}
        {activeType && (
          <div className="p-4 border-t border-gray-100 space-y-3">
            <div>
              <label className="block text-[11px] font-medium text-gray-600 mb-1">Topic / Product</label>
              <input
                value={topic}
                onChange={e => setTopic(e.target.value)}
                placeholder={activeConfig?.example}
                className="w-full h-8 px-2.5 text-xs rounded-lg border border-gray-200 focus:outline-none focus:border-indigo-400 focus:ring-1 focus:ring-indigo-100"
              />
            </div>

            <div>
              <label className="block text-[11px] font-medium text-gray-600 mb-1">Domain</label>
              <div className="flex flex-wrap gap-1">
                {DOMAINS.map(d => (
                  <button key={d} onClick={() => setDomain(d)}
                    className={cn("text-[10px] px-2 py-0.5 rounded-full border capitalize transition-all",
                      domain === d ? "bg-indigo-500 text-white border-indigo-500" : "bg-gray-50 text-gray-600 border-gray-200 hover:border-gray-300"
                    )}
                  >{d}</button>
                ))}
              </div>
            </div>

            {!isFlow && (
              <div>
                <label className="block text-[11px] font-medium text-gray-600 mb-1">Additional Context</label>
                <textarea value={context} onChange={e => setContext(e.target.value)}
                  placeholder="Any extra context or constraints..."
                  className="w-full h-14 px-2.5 py-2 text-xs rounded-lg border border-gray-200 focus:outline-none focus:border-indigo-400 resize-none"
                />
              </div>
            )}

            {/* Image Upload */}
            <div>
              <label className="block text-[11px] font-medium text-gray-600 mb-1">
                Screen Image <span className="text-gray-400 font-normal">(optional)</span>
              </label>
              {imagePreview ? (
                <div className="relative rounded-lg overflow-hidden border border-gray-200 group">
                  <img src={imagePreview} alt="Uploaded screen" className="w-full h-28 object-cover" />
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all flex items-center justify-center">
                    <button
                      onClick={() => { setImageFile(null); setImagePreview(null); }}
                      className="opacity-0 group-hover:opacity-100 w-7 h-7 bg-white rounded-full flex items-center justify-center shadow-md transition-all"
                    >
                      <X className="w-3.5 h-3.5 text-gray-700" />
                    </button>
                  </div>
                  <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/50 px-2 py-1.5">
                    <p className="text-[10px] text-white font-medium flex items-center gap-1">
                      <ImageIcon className="w-3 h-3" /> {imageFile?.name?.slice(0, 24) || "Screen uploaded"}
                    </p>
                  </div>
                </div>
              ) : (
                <div
                  onDrop={handleDrop}
                  onDragOver={e => e.preventDefault()}
                  onClick={() => fileInputRef.current?.click()}
                  className="border border-dashed border-gray-300 rounded-lg p-3 text-center cursor-pointer hover:border-indigo-400 hover:bg-indigo-50/30 transition-all"
                >
                  <Upload className="w-4 h-4 text-gray-400 mx-auto mb-1" />
                  <p className="text-[10px] text-gray-500 leading-relaxed">
                    {activeConfig?.imageTip || "Upload a screen for richer analysis"}
                  </p>
                  <p className="text-[9px] text-gray-400 mt-0.5">PNG, JPG, WEBP · max 10MB</p>
                </div>
              )}
              <input ref={fileInputRef} type="file" accept="image/*" className="hidden"
                onChange={e => { const f = e.target.files?.[0]; if (f) handleImageSelect(f); }}
              />
            </div>

            <button
              onClick={handleRun}
              disabled={!topic.trim() || researchMutation.isPending || flowLoading}
              className="w-full h-8 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-medium rounded-lg flex items-center justify-center gap-1.5 transition-colors disabled:opacity-50"
            >
              {(researchMutation.isPending || flowLoading) ? (
                <><Loader2 className="w-3.5 h-3.5 animate-spin" /> {imageFile ? "Analyzing screen..." : "Generating..."}</>
              ) : (
                <><Sparkles className="w-3.5 h-3.5" /> Generate {activeConfig?.label}</>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Right — results */}
      <div className="flex-1 overflow-hidden flex flex-col">
        {!activeType && (
          <div className="h-full flex items-center justify-center">
            <div className="text-center max-w-sm">
              <div className="w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="w-6 h-6 text-blue-500" />
              </div>
              <h2 className="text-base font-semibold text-gray-900 mb-2">Analyst Team</h2>
              <p className="text-sm text-gray-500 leading-relaxed">
                Research, personas, user stories, PRDs, and node-based user flows.
                Upload a screen image to ground any analysis in real UI.
                RAG checks your org documents for compliance on every response.
              </p>
            </div>
          </div>
        )}

        {/* Flow loading */}
        {isFlow && flowLoading && (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <div className="w-8 h-8 border-2 border-fuchsia-200 border-t-fuchsia-500 rounded-full animate-spin mx-auto mb-3" />
              <p className="text-sm text-gray-600">{flowSteps[flowSteps.length - 1] || "Designing flow..."}</p>
              {imageFile && <p className="text-xs text-indigo-500 mt-1 flex items-center justify-center gap-1"><ImageIcon className="w-3 h-3" /> Analyzing uploaded screen</p>}
            </div>
          </div>
        )}

        {/* Flow canvas result */}
        {isFlow && flowResult && !flowLoading && (
          <>
            <div className="px-5 py-2.5 border-b border-gray-100 bg-white flex items-center gap-3">
              <span className="text-sm font-semibold text-gray-800">{flowResult.flow_name}</span>
              <span className="text-[11px] text-gray-400">{flowResult.nodes?.length || 0} nodes</span>
              {flowResult._image_analyzed && (
                <span className="text-[10px] bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded flex items-center gap-1">
                  <ImageIcon className="w-2.5 h-2.5" /> from screen
                </span>
              )}
              {flowResult.ux_analysis?.estimated_completion_rate && (
                <span className="text-[11px] bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded ml-auto">
                  ~{flowResult.ux_analysis.estimated_completion_rate} completion
                </span>
              )}
              {flowResult.ux_analysis?.cognitive_load && (
                <span className={cn("text-[11px] px-2 py-0.5 rounded",
                  flowResult.ux_analysis.cognitive_load === "low" ? "bg-emerald-50 text-emerald-700" :
                  flowResult.ux_analysis.cognitive_load === "high" ? "bg-red-50 text-red-700" :
                  "bg-amber-50 text-amber-700"
                )}>
                  {flowResult.ux_analysis.cognitive_load} load
                </span>
              )}
            </div>
            <div className="flex-1 flex overflow-hidden">
              <div className="flex-1 relative">
                <FlowCanvas nodes={flowResult.nodes || []} edges={flowResult.edges || []} />
              </div>
              <div className="w-72 border-l border-gray-100 bg-white overflow-auto p-4 space-y-4">
                <div>
                  <h3 className="text-xs font-semibold text-gray-700 mb-1">Goal</h3>
                  <p className="text-[11px] text-gray-600">{flowResult.goal}</p>
                </div>
                {flowResult.ux_analysis?.friction_points?.length > 0 && (
                  <div>
                    <h3 className="text-xs font-semibold text-gray-700 mb-2">Friction Points</h3>
                    <div className="space-y-2">
                      {flowResult.ux_analysis.friction_points.map((f: any, i: number) => (
                        <div key={i} className={cn("p-2 rounded-lg text-[10px] border",
                          f.severity === "high" ? "bg-red-50 border-red-100" :
                          f.severity === "medium" ? "bg-amber-50 border-amber-100" : "bg-gray-50 border-gray-100"
                        )}>
                          <div className="font-medium text-gray-700">{f.issue}</div>
                          <div className="text-gray-500 mt-0.5">→ {f.fix}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {flowResult.recommendations?.length > 0 && (
                  <div>
                    <h3 className="text-xs font-semibold text-gray-700 mb-2">Recommendations</h3>
                    <ul className="space-y-1">
                      {flowResult.recommendations.map((r: string, i: number) => (
                        <li key={i} className="text-[10px] text-gray-600 flex gap-1.5">
                          <span className="text-fuchsia-400">→</span>{r}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </>
        )}

        {/* Research loading */}
        {!isFlow && researchMutation.isPending && (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <div className="w-8 h-8 border-2 border-indigo-200 border-t-indigo-500 rounded-full animate-spin mx-auto mb-3" />
              <p className="text-sm text-gray-600">
                {imageFile ? "Analyzing screen + generating research..." : "Researching..."}
              </p>
              {imageFile && <p className="text-xs text-indigo-500 mt-1 flex items-center justify-center gap-1"><ImageIcon className="w-3 h-3" /> Screen analysis in progress</p>}
            </div>
          </div>
        )}

        {/* Research result */}
        {!isFlow && result && !researchMutation.isPending && (
          <div className="overflow-auto p-6">
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
              {/* Token usage badge */}
              {tokenUsage && (
                <div className="mb-3 flex items-center gap-2 text-[11px] text-gray-600 bg-gray-50 border border-gray-200 rounded-lg px-3 py-2">
                  <Zap className="w-3.5 h-3.5 text-violet-500 flex-shrink-0" />
                  <span className="font-medium">{(tokenUsage.total / 1000).toFixed(1)}k tokens</span>
                  <span className="text-gray-400">·</span>
                  <span>{tokenUsage.calls} API call{tokenUsage.calls !== 1 ? "s" : ""}</span>
                  {tokenUsage.model && (
                    <>
                      <span className="text-gray-400">·</span>
                      <span className="text-violet-600 font-medium">{tokenUsage.model.replace("claude-","").replace("-20250514","").replace("-20251001","")}</span>
                    </>
                  )}
                </div>
              )}
              {/* Image used badge */}
              {result._image_analyzed && (
                <div className="mb-3 flex items-center gap-2 text-[11px] text-indigo-600 bg-indigo-50 border border-indigo-100 rounded-lg px-3 py-2">
                  <ImageIcon className="w-3.5 h-3.5 flex-shrink-0" />
                  Grounded in uploaded screen — {result._image_context_summary || "visual analysis applied"}
                </div>
              )}
              {/* RAG compliance notes */}
              {result.rag_compliance_notes && (
                <div className="mb-3 bg-amber-50 border border-amber-100 rounded-lg px-3 py-2 space-y-1">
                  <div className="flex items-center gap-1.5 text-[11px] font-semibold text-amber-700">
                    <FileCheck className="w-3.5 h-3.5" /> Org Document Compliance Notes
                  </div>
                  {result.rag_compliance_notes.notes.slice(0, 2).map((note: string, i: number) => (
                    <p key={i} className="text-[10px] text-amber-600 line-clamp-2">{note}</p>
                  ))}
                </div>
              )}
              <ArtifactResultPanel result={result} type={activeType!} title={activeConfig?.label || "Result"} />
            </motion.div>
          </div>
        )}
      </div>
    </div>
  );
}
