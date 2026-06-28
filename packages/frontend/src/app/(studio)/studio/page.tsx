"use client";
import { useState, useRef, useEffect, useCallback } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import {
  Send, Sparkles, Wand2, Box, Palette, Check, Loader2,
  Smartphone, Monitor, Tablet, X, Code, ChevronDown, Plus,
  Download, Share2, FileCode, Cloud, Cpu, Zap, ShieldCheck,
  AlertTriangle, CheckCircle2, BarChart2, Layers, Info
} from "lucide-react";
import { api } from "@/lib/api/client";
import { cn } from "@/lib/utils/cn";
import { DesignCanvas, CanvasScreen } from "@/components/studio/DesignCanvas";
import { AgentPanel, AgentStep, PlannedScreen } from "@/components/studio/AgentPanel";

interface TokenUsage {
  input: number;
  output: number;
  calls: number;
  total: number;
  model: string;
}

interface ComplianceMetrics {
  accessibility_score: number;
  compliance_standards: string[];
  checks: Array<{ name: string; status: "pass" | "warning" | "fail"; detail: string }>;
  design_metrics: {
    screens_generated: number;
    fidelity: string;
    design_system: string;
    components_used: string[];
    models_used: string[];
  };
  wcag_level: string;
  summary: string;
}

const DOMAINS = ["retirement", "loan", "insurance", "healthcare", "banking", "ecommerce", "general"];
const DEVICES = [
  { id: "mobile", label: "Mobile", icon: Smartphone, width: 390, height: 760 },
  { id: "tablet", label: "Tablet", icon: Tablet, width: 768, height: 1024 },
  { id: "desktop", label: "Desktop", icon: Monitor, width: 1280, height: 820 },
];

interface DesignSystem {
  id: string; name: string; description: string; primary_color: string;
}

type Phase = "idle" | "planning" | "planned" | "generating" | "complete";

export default function StudioPage() {
  const queryClient = useQueryClient();

  // Config
  const [designSystemId, setDesignSystemId] = useState("company");
  const [fidelity, setFidelity] = useState<"wireframe" | "hifi">("hifi");
  const [autoCount, setAutoCount] = useState(true);   // agent decides count
  const [screenCount, setScreenCount] = useState(3);
  const [domain, setDomain] = useState("general");
  const [device, setDevice] = useState("mobile");
  const [deviceForced, setDeviceForced] = useState(false);
  const [showConfig, setShowConfig] = useState(true);

  // Session + conversation
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [prompt, setPrompt] = useState("");

  // Reference image
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [referenceMode, setReferenceMode] = useState("improve");

  // Agent state
  const [phase, setPhase] = useState<Phase>("idle");
  const [steps, setSteps] = useState<AgentStep[]>([]);
  const [plannedScreens, setPlannedScreens] = useState<PlannedScreen[]>([]);
  const [currentGenId, setCurrentGenId] = useState<string | null>(null);

  // Canvas state
  const [screens, setScreens] = useState<CanvasScreen[]>([]);
  const [generatingNames, setGeneratingNames] = useState<string[]>([]);
  const [selectedScreen, setSelectedScreen] = useState<CanvasScreen | null>(null);
  const [codeScreen, setCodeScreen] = useState<CanvasScreen | null>(null);

  // Token tracking + compliance
  const [liveTokens, setLiveTokens] = useState<TokenUsage | null>(null);
  const [complianceMetrics, setComplianceMetrics] = useState<ComplianceMetrics | null>(null);
  const [showCompliance, setShowCompliance] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 10 * 1024 * 1024) { toast.error("Image must be under 10MB"); return; }
    setImageFile(file);
    setImagePreview(URL.createObjectURL(file));
    setReferenceMode("recreate");
  };
  const removeImage = () => {
    setImageFile(null);
    if (imagePreview) URL.revokeObjectURL(imagePreview);
    setImagePreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  // Design systems
  const { data: dsData } = useQuery({
    queryKey: ["design-systems"],
    queryFn: () => api.get("/design/systems").then(r => r.data),
  });
  const designSystems: DesignSystem[] = dsData?.systems || [];

  // AI backend status
  const { data: aiStatus, refetch: refetchAI } = useQuery({
    queryKey: ["ai-status"],
    queryFn: () => api.get("/ai/status").then(r => r.data),
    refetchInterval: 30000,
  });

  const switchAIMutation = useMutation({
    mutationFn: (backend: "cloud" | "ollama") => api.post("/ai/switch", { backend }).then(r => r.data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["ai-status"] });
      toast.success(data.message);
    },
    onError: (e: any) => toast.error(e.response?.data?.detail || "Failed to switch AI backend"),
  });

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [prompt]);

  // ── WebSocket connection per generation ─────────────────────────────────────
  const connectWS = useCallback((genId: string) => {
    if (wsRef.current) wsRef.current.close();
    const url = `${process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000"}/ws/design/${genId}`;
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      const ping = setInterval(() => ws.readyState === 1 && ws.send("ping"), 20000);
      ws.onclose = () => clearInterval(ping);
    };

    ws.onmessage = (e) => {
      const ev = JSON.parse(e.data);
      if (ev.type === "pong") return;

      setSteps(prev => [...prev, ev]);

      // Update live token counter from every event
      if (ev.token_usage && ev.token_usage.total > 0) {
        setLiveTokens(ev.token_usage);
      }

      switch (ev.type) {
        case "plan_ready":
          setPlannedScreens(ev.planned_screens || []);
          setPhase("planned");
          break;
        case "screen_start":
          setGeneratingNames(prev => [...new Set([...prev, ev.screen_name])]);
          break;
        case "screen_complete":
          if (ev.screen) {
            // Replace if screen_id already exists (no duplicates)
            setScreens(prev =>
              prev.some(s => s.screen_id === ev.screen.screen_id)
                ? prev.map(s => s.screen_id === ev.screen.screen_id ? ev.screen : s)
                : [...prev, ev.screen]
            );
            setGeneratingNames(prev => prev.filter(n => n !== ev.screen.name));
          }
          break;
        case "screen_regenerated":
          if (ev.screen) {
            setScreens(prev => prev.map(s => s.screen_id === ev.screen.screen_id ? ev.screen : s));
            toast.success(ev.message);
          }
          break;
        case "complete":
          setPhase("complete");
          setGeneratingNames([]);
          if (ev.compliance_metrics) {
            setComplianceMetrics(ev.compliance_metrics);
            setShowCompliance(true);
          }
          break;
        case "error":
          toast.error(ev.message);
          setPhase("idle");
          break;
      }
    };

    return ws;
  }, []);

  useEffect(() => {
    return () => { if (wsRef.current) wsRef.current.close(); };
  }, []);

  // ── Phase 1: Plan ──────────────────────────────────────────────────────────
  const planMutation = useMutation({
    mutationFn: () => {
      const fd = new FormData();
      fd.append("prompt", prompt);
      if (sessionId) fd.append("session_id", sessionId);
      fd.append("design_system", designSystemId);
      fd.append("fidelity", fidelity);
      fd.append("screen_count", String(autoCount ? 0 : screenCount));
      fd.append("domain", domain);
      if (imageFile) {
        fd.append("image", imageFile);
        fd.append("reference_mode", referenceMode);
      }
      return api.post("/design/plan", fd, { headers: { "Content-Type": "multipart/form-data" } }).then(r => r.data);
    },
    onSuccess: (data) => {
      setDeviceForced(false);  // reset override so AI screen_type renders at intended size
      setSessionId(data.session_id);
      setCurrentGenId(data.generation_id);
      connectWS(data.generation_id);
    },
    onError: (e: any) => {
      toast.error(e.response?.data?.detail || "Planning failed");
      setPhase("idle");
    },
  });

  // ── Phase 2: Approve & Generate ────────────────────────────────────────────
  const approveMutation = useMutation({
    mutationFn: (approvedIds: string[]) => api.post("/design/approve", {
      generation_id: currentGenId,
      session_id: sessionId,
      approved_screen_ids: approvedIds,
    }).then(r => r.data),
    onSuccess: (data) => {
      setPhase("generating");
      setCurrentGenId(data.generation_id);
      connectWS(data.generation_id);
    },
    onError: (e: any) => toast.error(e.response?.data?.detail || "Generation failed"),
  });

  // ── Regenerate a screen ────────────────────────────────────────────────────
  const regenMutation = useMutation({
    mutationFn: ({ screenId, refinement }: { screenId: string; refinement: string }) =>
      api.post("/design/regenerate-screen", {
        session_id: sessionId,
        screen_id: screenId,
        refinement,
      }).then(r => r.data),
    onSuccess: (data) => {
      connectWS(data.generation_id);
      toast.info("Refining screen...");
    },
  });

  const handleSubmit = () => {
    if (!prompt.trim() || phase === "planning" || phase === "generating") return;
    setSteps([]);
    setScreens([]);           // clear previous generation's screens
    setPlannedScreens([]);
    setSelectedScreen(null);
    setLiveTokens(null);
    setComplianceMetrics(null);
    setShowCompliance(false);
    setDeviceForced(false);
    setPhase("planning");
    setShowConfig(false);
    planMutation.mutate();
  };

  const handleApprove = (ids: string[]) => approveMutation.mutate(ids);
  const handleReject = () => {
    setPhase("idle");
    setPlannedScreens([]);
    toast.info("Plan rejected. Refine your prompt and try again.");
  };

  const handleRegenerate = (screen: CanvasScreen) => {
    const refinement = window.prompt(`How should I refine "${screen.name}"?`, "Improve the visual hierarchy and spacing");
    if (refinement) regenMutation.mutate({ screenId: screen.screen_id, refinement });
  };

  // ── Export ─────────────────────────────────────────────────────────────────
  const exportMutation = useMutation({
    mutationFn: (format: string) => api.post("/design/export", {
      session_id: sessionId,
      format,
      screens: screens.map(s => ({ screen_id: s.screen_id, name: s.name, html: s.html })),
    }).then(r => r.data),
    onSuccess: (data) => {
      if (data.format === "html") {
        const blob = new Blob([data.content], { type: "text/html" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url; a.download = data.filename; a.click();
        URL.revokeObjectURL(url);
        toast.success(`Exported ${data.screen_count} screens as HTML`);
      } else {
        const blob = new Blob([JSON.stringify(data.content, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url; a.download = data.filename; a.click();
        URL.revokeObjectURL(url);
        toast.success("Figma JSON downloaded — import via CORE Studio plugin");
      }
    },
    onError: () => toast.error("Export failed"),
  });

  const handleNewPrompt = () => {
    // Continue conversation — keep sessionId for context
    setPrompt("");
    setPhase("idle");
    setSteps([]);
    setPlannedScreens([]);
  };

  const deviceCfg = DEVICES.find(d => d.id === device)!;
  const hasContent = phase !== "idle" || screens.length > 0;
  const isWorking = phase === "planning" || phase === "generating";

  return (
    <div className="flex h-[calc(100vh-44px)]">
      {/* ── Left: Config + Chat ──────────────────────────────────────────────── */}
      <div className="w-[340px] flex-shrink-0 border-r border-gray-100 bg-white flex flex-col overflow-hidden">
        {/* Config (collapsible) */}
        <div className="border-b border-gray-100">
          <button
            onClick={() => setShowConfig(s => !s)}
            className="w-full flex items-center justify-between px-4 py-3 hover:bg-gray-50"
          >
            <div className="flex items-center gap-2">
              <Wand2 className="w-4 h-4 text-violet-500" />
              <span className="text-sm font-semibold text-gray-800">Design Settings</span>
            </div>
            <ChevronDown className={cn("w-4 h-4 text-gray-400 transition-transform", showConfig && "rotate-180")} />
          </button>

          <AnimatePresence>
            {showConfig && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="overflow-hidden"
              >
                <div className="px-4 pb-4 space-y-4">
                  {/* Design System */}
                  <div>
                    <label className="block text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-1.5">
                      Design System
                    </label>
                    <div className="grid grid-cols-2 gap-1">
                      {designSystems.map(ds => (
                        <button
                          key={ds.id}
                          onClick={() => setDesignSystemId(ds.id)}
                          className={cn(
                            "flex items-center gap-1.5 px-2 py-1.5 rounded-lg border text-left transition-all",
                            designSystemId === ds.id ? "border-violet-300 bg-violet-50" : "border-gray-100 hover:bg-gray-50"
                          )}
                        >
                          <div className="w-3 h-3 rounded-md flex-shrink-0 border border-white shadow-sm" style={{ background: ds.primary_color }} />
                          <span className={cn("text-[10px] font-medium truncate", designSystemId === ds.id ? "text-violet-700" : "text-gray-600")}>
                            {ds.name.replace(" Design", "").replace(" App Style", "").replace(" Design System", "")}
                          </span>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Fidelity */}
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={() => setFidelity("wireframe")}
                      className={cn("p-2 rounded-lg border text-center transition-all",
                        fidelity === "wireframe" ? "border-gray-400 bg-gray-50" : "border-gray-100")}
                    >
                      <Box className="w-3.5 h-3.5 text-gray-500 mx-auto mb-0.5" />
                      <span className="text-[10px] font-medium text-gray-700">Wireframe</span>
                    </button>
                    <button
                      onClick={() => setFidelity("hifi")}
                      className={cn("p-2 rounded-lg border text-center transition-all",
                        fidelity === "hifi" ? "border-violet-300 bg-violet-50" : "border-gray-100")}
                    >
                      <Palette className={cn("w-3.5 h-3.5 mx-auto mb-0.5", fidelity === "hifi" ? "text-violet-500" : "text-gray-500")} />
                      <span className={cn("text-[10px] font-medium", fidelity === "hifi" ? "text-violet-700" : "text-gray-700")}>Hi-Fi</span>
                    </button>
                  </div>

                  {/* Screen count — agent decides by default */}
                  <div>
                    <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider">Screens</label>
                    <div className="mt-1.5 grid grid-cols-2 gap-1.5">
                      <button
                        onClick={() => setAutoCount(true)}
                        className={cn("p-2 rounded-lg border text-center transition-all",
                          autoCount ? "border-violet-300 bg-violet-50" : "border-gray-100")}
                      >
                        <Sparkles className={cn("w-3.5 h-3.5 mx-auto mb-0.5", autoCount ? "text-violet-500" : "text-gray-400")} />
                        <span className={cn("text-[10px] font-medium", autoCount ? "text-violet-700" : "text-gray-600")}>Agent decides</span>
                      </button>
                      <button
                        onClick={() => setAutoCount(false)}
                        className={cn("p-2 rounded-lg border text-center transition-all",
                          !autoCount ? "border-gray-400 bg-gray-50" : "border-gray-100")}
                      >
                        <span className="text-[10px] font-medium text-gray-700">Fixed: {screenCount}</span>
                        {!autoCount && (
                          <input type="range" min={1} max={8} value={screenCount}
                            onChange={e => setScreenCount(Number(e.target.value))}
                            onClick={e => e.stopPropagation()}
                            className="w-full h-1 mt-1 bg-gray-200 rounded-full appearance-none cursor-pointer accent-violet-500" />
                        )}
                      </button>
                    </div>
                  </div>

                  {/* Domain */}
                  <div>
                    <label className="block text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-1.5">Domain</label>
                    <div className="flex flex-wrap gap-1">
                      {DOMAINS.map(d => (
                        <button key={d} onClick={() => setDomain(d)}
                          className={cn("text-[9px] px-1.5 py-0.5 rounded-full border capitalize",
                            domain === d ? "bg-violet-500 text-white border-violet-500" : "bg-white text-gray-600 border-gray-200")}>
                          {d}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* AI Backend switcher */}
                  <div>
                    <label className="block text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-1.5">AI Backend</label>
                    <div className="grid grid-cols-2 gap-1">
                      <button
                        onClick={() => switchAIMutation.mutate("cloud")}
                        disabled={switchAIMutation.isPending}
                        className={cn(
                          "flex items-center gap-1.5 px-2 py-1.5 rounded-lg border text-left transition-all",
                          aiStatus?.backend === "cloud"
                            ? "border-violet-300 bg-violet-50"
                            : "border-gray-100 hover:bg-gray-50 opacity-60"
                        )}
                      >
                        <Cloud className={cn("w-3 h-3 flex-shrink-0", aiStatus?.backend === "cloud" ? "text-violet-600" : "text-gray-400")} />
                        <div>
                          <div className={cn("text-[10px] font-semibold", aiStatus?.backend === "cloud" ? "text-violet-700" : "text-gray-600")}>
                            Cloud API
                          </div>
                          <div className="text-[9px] text-gray-400 capitalize">{aiStatus?.provider || "none"}</div>
                        </div>
                        {aiStatus?.backend === "cloud" && <Check className="w-3 h-3 text-violet-600 ml-auto" />}
                      </button>
                      <button
                        onClick={() => switchAIMutation.mutate("ollama")}
                        disabled={switchAIMutation.isPending}
                        className={cn(
                          "flex items-center gap-1.5 px-2 py-1.5 rounded-lg border text-left transition-all",
                          aiStatus?.backend === "ollama"
                            ? "border-emerald-300 bg-emerald-50"
                            : "border-gray-100 hover:bg-gray-50",
                          !aiStatus?.providers_detected?.ollama && "opacity-40 cursor-not-allowed"
                        )}
                      >
                        <Cpu className={cn("w-3 h-3 flex-shrink-0", aiStatus?.backend === "ollama" ? "text-emerald-600" : "text-gray-400")} />
                        <div>
                          <div className={cn("text-[10px] font-semibold", aiStatus?.backend === "ollama" ? "text-emerald-700" : "text-gray-600")}>
                            Local AI
                          </div>
                          <div className="text-[9px] text-gray-400">
                            {aiStatus?.providers_detected?.ollama ? "Ollama ready" : "Ollama offline"}
                          </div>
                        </div>
                        {aiStatus?.backend === "ollama" && <Check className="w-3 h-3 text-emerald-600 ml-auto" />}
                      </button>
                    </div>
                    {aiStatus && (
                      <p className="mt-1 text-[9px] text-gray-400">
                        Active: {aiStatus.active_models?.standard || aiStatus.active_models?.reasoning || "—"}
                      </p>
                    )}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Agent activity (when working) */}
        <div className="flex-1 overflow-hidden">
          {phase === "idle" && screens.length === 0 ? (
            <div className="h-full flex items-center justify-center p-6">
              <div className="text-center">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-violet-100 to-violet-200 flex items-center justify-center mx-auto mb-3">
                  <Sparkles className="w-6 h-6 text-violet-600" />
                </div>
                <p className="text-xs text-gray-500 leading-relaxed">
                  Describe what you want.<br />
                  The agent will analyze, plan, and<br />generate — you approve each step.
                </p>
              </div>
            </div>
          ) : (
            <AgentPanel
              steps={steps}
              phase={phase}
              plannedScreens={plannedScreens}
              onApprove={handleApprove}
              onReject={handleReject}
              isGenerating={phase === "generating"}
            />
          )}
        </div>

        {/* Chat input */}
        <div className="border-t border-gray-100 p-3">
          {phase === "complete" && (
            <button
              onClick={handleNewPrompt}
              className="w-full mb-2 h-7 text-[11px] text-violet-600 border border-violet-200 rounded-lg hover:bg-violet-50 flex items-center justify-center gap-1"
            >
              <Plus className="w-3 h-3" /> Continue — add more screens
            </button>
          )}
          {/* Reference image preview */}
          {imagePreview && (
            <div className="mb-2 p-2 bg-violet-50 rounded-lg border border-violet-100">
              <div className="flex items-start gap-2">
                <img src={imagePreview} alt="ref" className="h-14 rounded-md border border-violet-200 object-cover" />
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] font-medium text-violet-700">Reference image</span>
                    <button onClick={removeImage} className="text-violet-400 hover:text-violet-600"><X className="w-3 h-3" /></button>
                  </div>
                  <div className="flex gap-1">
                    {[
                      { id: "recreate", label: "🔁 Recreate" },
                      { id: "improve", label: "✨ Improve" },
                      { id: "inspire", label: "💡 Inspire" },
                    ].map(m => (
                      <button key={m.id} onClick={() => setReferenceMode(m.id)}
                        className={cn("text-[9px] px-1.5 py-0.5 rounded border transition-all",
                          referenceMode === m.id ? "bg-violet-500 text-white border-violet-500" : "bg-white text-gray-600 border-gray-200")}>
                        {m.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          <div className="relative rounded-xl border border-gray-200 focus-within:border-violet-400 focus-within:ring-2 focus-within:ring-violet-100 bg-white">
            <textarea
              ref={textareaRef}
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
              onKeyDown={e => {
                if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) { e.preventDefault(); handleSubmit(); }
              }}
              placeholder={
                imageFile
                  ? `Tell me what to do with this image...`
                  : screens.length > 0
                  ? `Continue the flow... e.g. "create next flow of screens"`
                  : `Describe what to design...\ne.g. "Retirement planning landing page"`
              }
              disabled={isWorking}
              className="w-full px-3 py-2.5 text-sm bg-transparent focus:outline-none resize-none placeholder:text-gray-400 leading-relaxed min-h-[56px] disabled:opacity-50"
              rows={2}
            />
            <div className="flex items-center justify-between px-3 py-2 border-t border-gray-100">
              <div className="flex items-center gap-1.5">
                <input ref={fileInputRef} type="file" accept="image/*" onChange={handleImageSelect} className="hidden" />
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className={cn("h-6 w-6 flex items-center justify-center rounded-md transition-all",
                    imageFile ? "bg-violet-100 text-violet-600" : "text-gray-400 hover:bg-gray-100")}
                  title="Attach reference image"
                >
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14M4 8h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                </button>
                <span className="text-[10px] text-gray-400">⌘+Enter</span>
              </div>
              <button
                onClick={handleSubmit}
                disabled={!prompt.trim() || isWorking}
                className="h-7 px-3 bg-gradient-to-br from-violet-500 to-violet-700 text-white text-xs font-medium rounded-md flex items-center gap-1.5 disabled:opacity-40 transition-all"
              >
                {isWorking ? <Loader2 className="w-3 h-3 animate-spin" /> : <><Sparkles className="w-3 h-3" /> Generate</>}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* ── Right: Canvas ────────────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col bg-gray-50 overflow-hidden relative">
        {/* Toolbar */}
        <div className="px-4 py-2 border-b border-gray-100 bg-white flex items-center gap-3 flex-shrink-0">
          <div className="text-xs text-gray-500">
            {screens.length > 0 ? `${screens.length} screens` : "Canvas"}
          </div>

          {/* Live token usage badge */}
          {liveTokens && (
            <div className={cn(
              "flex items-center gap-1.5 px-2 py-1 rounded-full border text-[10px] font-medium transition-all",
              isWorking
                ? "bg-violet-50 border-violet-200 text-violet-700 animate-pulse"
                : "bg-gray-50 border-gray-200 text-gray-600"
            )}>
              <Zap className="w-2.5 h-2.5" />
              <span>{(liveTokens.total / 1000).toFixed(1)}k tokens</span>
              <span className="text-gray-400">·</span>
              <span>{liveTokens.calls} call{liveTokens.calls !== 1 ? "s" : ""}</span>
              {liveTokens.model && (
                <>
                  <span className="text-gray-400">·</span>
                  <span className="truncate max-w-[90px]">{liveTokens.model.replace("claude-", "").replace("-20250514","").replace("-20251001","")}</span>
                </>
              )}
            </div>
          )}

          {/* Compliance score badge (after complete) */}
          {complianceMetrics && phase === "complete" && (
            <button
              onClick={() => setShowCompliance(s => !s)}
              className={cn(
                "flex items-center gap-1.5 px-2 py-1 rounded-full border text-[10px] font-medium transition-all",
                complianceMetrics.accessibility_score >= 80
                  ? "bg-emerald-50 border-emerald-200 text-emerald-700 hover:bg-emerald-100"
                  : "bg-amber-50 border-amber-200 text-amber-700 hover:bg-amber-100"
              )}
            >
              <ShieldCheck className="w-2.5 h-2.5" />
              <span>A11y {complianceMetrics.accessibility_score}/100</span>
              <span className="text-current opacity-50">·</span>
              <span>WCAG {complianceMetrics.wcag_level}</span>
            </button>
          )}

          {/* Export buttons */}
          {screens.length > 0 && phase === "complete" && (
            <div className="flex items-center gap-1 ml-3">
              <button
                onClick={() => exportMutation.mutate("html")}
                disabled={exportMutation.isPending}
                className="h-6 px-2 flex items-center gap-1 text-[11px] text-gray-600 border border-gray-200 rounded-md hover:bg-gray-50"
              >
                <FileCode className="w-3 h-3" /> HTML
              </button>
              <button
                onClick={() => exportMutation.mutate("figma_json")}
                disabled={exportMutation.isPending}
                className="h-6 px-2 flex items-center gap-1 text-[11px] text-gray-600 border border-gray-200 rounded-md hover:bg-gray-50"
              >
                <Share2 className="w-3 h-3" /> Figma
              </button>
            </div>
          )}

          <div className="ml-auto flex items-center bg-gray-100 rounded-lg p-0.5">
            {DEVICES.map(d => {
              const Icon = d.icon;
              return (
                <button key={d.id} onClick={() => { setDevice(d.id); setDeviceForced(true); }}
                  className={cn("h-6 w-7 flex items-center justify-center rounded-md",
                    device === d.id ? "bg-white shadow-sm text-gray-800" : "text-gray-500")}>
                  <Icon className="w-3 h-3" />
                </button>
              );
            })}
          </div>
        </div>

        {/* Canvas */}
        <div className="flex-1 relative">
          {screens.length === 0 && phase === "idle" ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center max-w-sm px-6">
                <div className="w-14 h-14 rounded-2xl bg-white border border-gray-200 flex items-center justify-center mx-auto mb-4 shadow-sm">
                  <Wand2 className="w-7 h-7 text-violet-500" />
                </div>
                <h2 className="text-base font-semibold text-gray-900 mb-2">Your canvas is empty</h2>
                <p className="text-sm text-gray-500 mb-5">
                  Type a prompt — even a simple one. The agent will improvise,
                  plan a full flow, and let you approve before generating.
                </p>
                <div className="flex flex-wrap gap-1.5 justify-center">
                  {["Retirement planning page", "Loan dashboard", "Onboarding flow"].map(ex => (
                    <button
                      key={ex}
                      onClick={() => setPrompt(ex)}
                      className="text-[11px] bg-white border border-gray-200 text-gray-600 px-2.5 py-1 rounded-full hover:border-violet-300 hover:text-violet-600"
                    >{ex}</button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <DesignCanvas
              screens={screens}
              generatingScreens={generatingNames}
              device={deviceCfg}
              forceDevice={deviceForced}
              selectedScreenId={selectedScreen?.screen_id}
              onSelectScreen={setSelectedScreen}
              onRegenerateScreen={handleRegenerate}
              onViewCode={setCodeScreen}
            />
          )}
        </div>
      </div>

      {/* Compliance & Accessibility Panel */}
      <AnimatePresence>
        {showCompliance && complianceMetrics && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="fixed bottom-0 left-[548px] right-0 z-40 bg-white border-t border-gray-200 shadow-lg"
            style={{ maxHeight: "320px" }}
          >
            <div className="flex items-center justify-between px-5 py-3 border-b border-gray-100">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                <span className="text-sm font-semibold text-gray-800">Design Quality Report</span>
                <span className="text-[10px] text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full">Auto-generated</span>
              </div>
              <button onClick={() => setShowCompliance(false)} className="text-gray-400 hover:text-gray-600">
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="p-4 overflow-auto" style={{ maxHeight: "270px" }}>
              <div className="grid grid-cols-4 gap-3 mb-4">
                {/* Accessibility Score */}
                <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-xl p-3 border border-emerald-200">
                  <div className="text-[10px] font-semibold text-emerald-600 uppercase tracking-wider mb-1">Accessibility</div>
                  <div className="text-2xl font-bold text-emerald-800">{complianceMetrics.accessibility_score}</div>
                  <div className="text-[9px] text-emerald-600">/ 100 · WCAG {complianceMetrics.wcag_level}</div>
                </div>
                {/* Screens */}
                <div className="bg-gradient-to-br from-violet-50 to-violet-100 rounded-xl p-3 border border-violet-200">
                  <div className="text-[10px] font-semibold text-violet-600 uppercase tracking-wider mb-1">Screens</div>
                  <div className="text-2xl font-bold text-violet-800">{complianceMetrics.design_metrics.screens_generated}</div>
                  <div className="text-[9px] text-violet-600 capitalize">{complianceMetrics.design_metrics.fidelity} fidelity</div>
                </div>
                {/* Standards */}
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-3 border border-blue-200">
                  <div className="text-[10px] font-semibold text-blue-600 uppercase tracking-wider mb-1">Standards</div>
                  <div className="text-2xl font-bold text-blue-800">{complianceMetrics.compliance_standards.length}</div>
                  <div className="text-[9px] text-blue-600">compliance checks</div>
                </div>
                {/* Token Usage */}
                <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-3 border border-gray-200">
                  <div className="text-[10px] font-semibold text-gray-600 uppercase tracking-wider mb-1">Tokens Used</div>
                  <div className="text-2xl font-bold text-gray-800">{liveTokens ? `${(liveTokens.total / 1000).toFixed(1)}k` : "—"}</div>
                  <div className="text-[9px] text-gray-500">{liveTokens ? `${liveTokens.calls} API call${liveTokens.calls !== 1 ? "s" : ""}` : ""}</div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                {/* Compliance Checks */}
                <div>
                  <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-2">Compliance Checks</div>
                  <div className="space-y-1.5">
                    {complianceMetrics.checks.map((check, i) => (
                      <div key={i} className="flex items-start gap-2">
                        {check.status === "pass" ? (
                          <CheckCircle2 className="w-3 h-3 text-emerald-500 flex-shrink-0 mt-0.5" />
                        ) : (
                          <AlertTriangle className="w-3 h-3 text-amber-500 flex-shrink-0 mt-0.5" />
                        )}
                        <div>
                          <div className="text-[10px] font-medium text-gray-700">{check.name}</div>
                          <div className="text-[9px] text-gray-400">{check.detail}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Standards Applied + Components */}
                <div className="space-y-3">
                  <div>
                    <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-2">Standards Applied</div>
                    <div className="flex flex-wrap gap-1">
                      {complianceMetrics.compliance_standards.map((s, i) => (
                        <span key={i} className="text-[9px] bg-blue-50 text-blue-700 border border-blue-200 px-1.5 py-0.5 rounded-full">
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                  {complianceMetrics.design_metrics.components_used.length > 0 && (
                    <div>
                      <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-2">Components Used</div>
                      <div className="flex flex-wrap gap-1">
                        {complianceMetrics.design_metrics.components_used.slice(0, 8).map((c, i) => (
                          <span key={i} className="text-[9px] bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded-full">{c}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {complianceMetrics.design_metrics.models_used.length > 0 && (
                    <div>
                      <div className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-2">AI Models</div>
                      <div className="flex flex-wrap gap-1">
                        {complianceMetrics.design_metrics.models_used.map((m, i) => (
                          <span key={i} className="text-[9px] bg-violet-50 text-violet-700 border border-violet-200 px-1.5 py-0.5 rounded-full">
                            {m.replace("claude-","").replace("-20250514","").replace("-20251001","")}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Code modal */}
      <AnimatePresence>
        {codeScreen && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-8"
            onClick={() => setCodeScreen(null)}
          >
            <motion.div
              initial={{ scale: 0.95, y: 10 }} animate={{ scale: 1, y: 0 }}
              className="bg-gray-900 rounded-xl overflow-hidden max-w-3xl w-full max-h-[80vh] flex flex-col"
              onClick={e => e.stopPropagation()}
            >
              <div className="flex items-center justify-between px-4 py-3 border-b border-gray-700">
                <span className="text-sm font-mono text-gray-300">{codeScreen.name}.html</span>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => { navigator.clipboard.writeText(codeScreen.html); toast.success("Copied"); }}
                    className="text-xs text-gray-400 hover:text-white flex items-center gap-1"
                  ><Code className="w-3 h-3" /> Copy</button>
                  <button onClick={() => setCodeScreen(null)} className="text-gray-400 hover:text-white">
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
              <pre className="p-4 text-xs font-mono text-gray-300 overflow-auto leading-relaxed">
                {codeScreen.html.replace(/></g, ">\n<")}
              </pre>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
