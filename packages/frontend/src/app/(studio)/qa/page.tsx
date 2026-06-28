"use client";
import { useState, useRef, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { toast } from "sonner";
import {
  ClipboardList, ShieldCheck, AlertTriangle,
  CheckCircle, XCircle, AlertCircle, Loader2, Sparkles,
  Upload, X, ImageIcon, Eye, Zap, Users
} from "lucide-react";
import { api } from "@/lib/api/client";
import { cn } from "@/lib/utils/cn";
import { ArtifactResultPanel } from "@/components/shared/ArtifactResultPanel";

const QA_MODES = [
  {
    id: "test_cases",
    icon: ClipboardList,
    label: "Test Cases",
    description: "Generate functional, E2E, or regression test cases from requirements",
    color: "text-emerald-600",
    bg: "bg-emerald-50",
    border: "border-emerald-200",
  },
  {
    id: "accessibility",
    icon: ShieldCheck,
    label: "Accessibility Review",
    description: "Full WCAG 2.1 AA check — upload a screen for visual analysis or run on design tokens",
    color: "text-blue-600",
    bg: "bg-blue-50",
    border: "border-blue-200",
    supportsImage: true,
  },
  {
    id: "compliance",
    icon: AlertTriangle,
    label: "Compliance Check",
    description: "WCAG, GDPR, HIPAA, SOC2 — check your design against regulatory standards",
    color: "text-amber-600",
    bg: "bg-amber-50",
    border: "border-amber-200",
  },
];

const TEST_TYPES = ["functional", "integration", "e2e", "regression", "performance"];
const COMPLIANCE_TYPES = ["wcag", "gdpr", "hipaa", "soc2", "all"];

const WCAG_LEVELS: Record<string, { color: string; bg: string; border: string; label: string }> = {
  AAA:  { color: "text-emerald-700", bg: "bg-emerald-50", border: "border-emerald-200", label: "AAA" },
  AA:   { color: "text-blue-700",    bg: "bg-blue-50",    border: "border-blue-200",    label: "AA" },
  A:    { color: "text-amber-700",   bg: "bg-amber-50",   border: "border-amber-200",   label: "A" },
  FAIL: { color: "text-red-700",     bg: "bg-red-50",     border: "border-red-200",     label: "FAIL" },
};

export default function QAPage() {
  const [mode, setMode] = useState<string | null>(null);
  const [topic, setTopic] = useState("");
  const [testType, setTestType] = useState("functional");
  const [complianceType, setComplianceType] = useState("wcag");
  const [result, setResult] = useState<any>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const activeCfg = QA_MODES.find(m => m.id === mode);

  // Reset image when switching away from accessibility
  const handleModeChange = (m: string) => {
    setMode(m);
    setResult(null);
    if (m !== "accessibility") { setImageFile(null); setImagePreview(null); }
  };

  const handleImageSelect = useCallback((file: File) => {
    if (!file.type.startsWith("image/")) { toast.error("Please upload an image file"); return; }
    if (file.size > 10 * 1024 * 1024) { toast.error("Image must be under 10MB"); return; }
    setImageFile(file);
    const reader = new FileReader();
    reader.onload = e => setImagePreview(e.target?.result as string);
    reader.readAsDataURL(file);
  }, []);

  const testMutation = useMutation({
    mutationFn: (data: any) => api.post("/qa/test-cases", data).then(r => r.data),
    onSuccess: d => { setResult(d.result); toast.success("Test cases generated"); },
    onError: (e: any) => toast.error(e.response?.data?.detail || "Failed"),
  });

  const a11yMutation = useMutation({
    mutationFn: (fd: FormData) =>
      api.post("/qa/accessibility", fd, { headers: { "Content-Type": "multipart/form-data" } }).then(r => r.data),
    onSuccess: d => {
      setResult(d.result);
      toast.success(d.image_used ? "WCAG check complete (from screenshot)" : "Accessibility review complete");
    },
    onError: (e: any) => toast.error(e.response?.data?.detail || "Failed"),
  });

  const complianceMutation = useMutation({
    mutationFn: (data: any) => api.post("/qa/compliance", data).then(r => r.data),
    onSuccess: d => { setResult(d.result); toast.success("Compliance check complete"); },
    onError: (e: any) => toast.error(e.response?.data?.detail || "Failed"),
  });

  const isLoading = testMutation.isPending || a11yMutation.isPending || complianceMutation.isPending;

  const handleRun = () => {
    if (!mode || !topic.trim()) return;
    setResult(null);
    if (mode === "test_cases") {
      testMutation.mutate({ test_type: testType, topic, requirements: {}, user_stories: [] });
    } else if (mode === "accessibility") {
      const fd = new FormData();
      fd.append("topic", topic);
      fd.append("ui_design_json", "{}");
      fd.append("ux_flow_json", "{}");
      if (imageFile) fd.append("image", imageFile);
      a11yMutation.mutate(fd);
    } else if (mode === "compliance") {
      complianceMutation.mutate({ compliance_type: complianceType, topic, domain: "general", design_context: {} });
    }
  };

  return (
    <div className="flex h-full">
      {/* Left panel */}
      <div className="w-80 flex-shrink-0 border-r border-gray-100 bg-white flex flex-col">
        <div className="p-4 border-b border-gray-100">
          <h2 className="text-sm font-semibold text-gray-800">QA Mode</h2>
          <p className="text-xs text-gray-500 mt-0.5">Select the type of QA check</p>
        </div>

        <div className="flex-1 overflow-auto p-3 space-y-1.5">
          {QA_MODES.map(m => {
            const Icon = m.icon;
            const isActive = mode === m.id;
            return (
              <button key={m.id} onClick={() => handleModeChange(m.id)}
                className={cn("w-full text-left p-3 rounded-xl border transition-all",
                  isActive ? `${m.bg} ${m.border}` : "border-gray-100 hover:bg-gray-50"
                )}
              >
                <div className="flex items-start gap-2.5">
                  <div className={cn("w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5", isActive ? m.bg : "bg-gray-100")}>
                    <Icon className={cn("w-3.5 h-3.5", isActive ? m.color : "text-gray-500")} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1.5">
                      <div className={cn("text-xs font-semibold", isActive ? m.color : "text-gray-700")}>{m.label}</div>
                      {m.supportsImage && (
                        <span className="text-[9px] bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded font-medium">+ Image</span>
                      )}
                    </div>
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
              <input value={topic} onChange={e => setTopic(e.target.value)}
                placeholder="e.g. Loan repayment dashboard"
                className="w-full h-8 px-2.5 text-xs rounded-lg border border-gray-200 focus:outline-none focus:border-indigo-400"
              />
            </div>

            {mode === "test_cases" && (
              <div>
                <label className="block text-[11px] font-medium text-gray-600 mb-1">Test Type</label>
                <div className="flex flex-wrap gap-1">
                  {TEST_TYPES.map(t => (
                    <button key={t} onClick={() => setTestType(t)}
                      className={cn("text-[10px] px-2 py-0.5 rounded-full border capitalize transition-all",
                        testType === t ? "bg-emerald-500 text-white border-emerald-500" : "bg-gray-50 text-gray-600 border-gray-200"
                      )}
                    >{t}</button>
                  ))}
                </div>
              </div>
            )}

            {mode === "compliance" && (
              <div>
                <label className="block text-[11px] font-medium text-gray-600 mb-1">Standard</label>
                <div className="flex flex-wrap gap-1">
                  {COMPLIANCE_TYPES.map(t => (
                    <button key={t} onClick={() => setComplianceType(t)}
                      className={cn("text-[10px] px-2 py-0.5 rounded-full border uppercase transition-all",
                        complianceType === t ? "bg-amber-500 text-white border-amber-500" : "bg-gray-50 text-gray-600 border-gray-200"
                      )}
                    >{t}</button>
                  ))}
                </div>
              </div>
            )}

            {/* Image upload — only for accessibility */}
            {mode === "accessibility" && (
              <div>
                <label className="block text-[11px] font-medium text-gray-600 mb-1">
                  Screen Image <span className="text-gray-400 font-normal">(optional but recommended)</span>
                </label>
                {imagePreview ? (
                  <div className="relative rounded-lg overflow-hidden border border-gray-200 group">
                    <img src={imagePreview} alt="Screen to check" className="w-full h-28 object-cover" />
                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all flex items-center justify-center">
                      <button onClick={() => { setImageFile(null); setImagePreview(null); }}
                        className="opacity-0 group-hover:opacity-100 w-7 h-7 bg-white rounded-full flex items-center justify-center shadow-md transition-all"
                      >
                        <X className="w-3.5 h-3.5 text-gray-700" />
                      </button>
                    </div>
                    <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/50 px-2 py-1.5">
                      <p className="text-[10px] text-white font-medium flex items-center gap-1">
                        <ImageIcon className="w-3 h-3" /> Ready to check WCAG compliance
                      </p>
                    </div>
                  </div>
                ) : (
                  <div
                    onDrop={e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) handleImageSelect(f); }}
                    onDragOver={e => e.preventDefault()}
                    onClick={() => fileInputRef.current?.click()}
                    className="border border-dashed border-blue-200 rounded-lg p-3 text-center cursor-pointer hover:border-blue-400 hover:bg-blue-50/30 transition-all bg-blue-50/20"
                  >
                    <Upload className="w-4 h-4 text-blue-400 mx-auto mb-1" />
                    <p className="text-[10px] text-blue-600 font-medium">Upload screen for visual WCAG check</p>
                    <p className="text-[9px] text-gray-400 mt-0.5">Vision AI extracts colors, contrast & structure</p>
                  </div>
                )}
                <input ref={fileInputRef} type="file" accept="image/*" className="hidden"
                  onChange={e => { const f = e.target.files?.[0]; if (f) handleImageSelect(f); }}
                />
                {!imageFile && (
                  <p className="text-[9px] text-gray-400 mt-1">Without image: checks design tokens from existing artifacts</p>
                )}
              </div>
            )}

            <button onClick={handleRun} disabled={!topic.trim() || isLoading}
              className="w-full h-8 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-medium rounded-lg flex items-center justify-center gap-1.5 transition-colors disabled:opacity-50"
            >
              {isLoading
                ? <><Loader2 className="w-3.5 h-3.5 animate-spin" /> {imageFile ? "Analyzing screen..." : "Running..."}</>
                : <><Sparkles className="w-3.5 h-3.5" /> Run {activeCfg?.label}</>
              }
            </button>
          </div>
        )}
      </div>

      {/* Right panel */}
      <div className="flex-1 overflow-auto p-6">
        {!mode && (
          <div className="h-full flex items-center justify-center">
            <div className="text-center max-w-sm">
              <div className="w-12 h-12 rounded-2xl bg-emerald-50 flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-6 h-6 text-emerald-500" />
              </div>
              <h2 className="text-base font-semibold text-gray-900 mb-2">QA Team</h2>
              <p className="text-sm text-gray-500 leading-relaxed">
                Generate test cases, run full WCAG 2.1 AA accessibility checks from screenshots
                (42 criteria, real contrast math, RAG-loaded standards), and validate compliance.
              </p>
            </div>
          </div>
        )}

        {isLoading && (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <div className="w-8 h-8 border-2 border-emerald-200 border-t-emerald-500 rounded-full animate-spin mx-auto mb-3" />
              <p className="text-sm text-gray-600">
                {mode === "accessibility" && imageFile ? "Extracting visual data + checking all WCAG criteria..." : "Running QA checks..."}
              </p>
              {mode === "accessibility" && imageFile && (
                <div className="mt-3 space-y-1 text-xs text-gray-400">
                  <p>① Vision AI analyzing screen</p>
                  <p>② Contrast math on extracted colors</p>
                  <p>③ Checking 42 WCAG 2.1 AA criteria</p>
                  <p>④ Loading WCAG standards from knowledge base</p>
                </div>
              )}
            </div>
          </div>
        )}

        {result && !isLoading && (
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
            {mode === "accessibility" ? (
              <A11yResultView result={result} />
            ) : (
              <ArtifactResultPanel result={result} type={mode!}
                title={mode === "test_cases" ? "Test Suite" : "Compliance Report"}
              />
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}


function A11yResultView({ result }: { result: any }) {
  const [activeTab, setActiveTab] = useState<"overview" | "checks" | "critical" | "visual">("overview");
  const score = result.overall_score ?? 0;
  const level = result.wcag_level ?? "FAIL";
  const lvlStyle = WCAG_LEVELS[level] || WCAG_LEVELS.FAIL;
  const isImageBased = result.source === "image";

  const allChecks = result.all_checks || [...(result.static_checks || []), ...(result.wcag_checks || [])];
  const criticalIssues = result.critical_issues || result.all_issues || [];
  const stats = result.stats || {
    total: allChecks.length,
    passed: allChecks.filter((c: any) => c.status === "pass" || c.passed).length,
    failed: allChecks.filter((c: any) => c.status === "fail" || c.passed === false).length,
    warnings: allChecks.filter((c: any) => c.status === "warning").length,
  };

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "checks",   label: `Checks (${allChecks.length})` },
    { id: "critical", label: `Issues (${criticalIssues.length})`, warn: criticalIssues.length > 0 },
    ...(isImageBased && result.visual_data ? [{ id: "visual", label: "Visual Data" }] : []),
  ] as const;

  return (
    <div className="space-y-4">
      {/* Score header */}
      <div className={cn("rounded-xl border p-5 flex items-center gap-5", lvlStyle.bg, lvlStyle.border)}>
        <div className={cn("w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold border-4 bg-white", lvlStyle.border, lvlStyle.color)}>
          {score}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={cn("text-lg font-bold", lvlStyle.color)}>WCAG 2.1 {level}</span>
            {isImageBased && (
              <span className="text-[10px] bg-white border border-blue-200 text-blue-600 px-2 py-0.5 rounded flex items-center gap-1">
                <ImageIcon className="w-3 h-3" /> from screenshot
              </span>
            )}
            {result.rag_context_used && (
              <span className="text-[10px] bg-white border border-emerald-200 text-emerald-600 px-2 py-0.5 rounded">
                ✓ RAG standards loaded
              </span>
            )}
          </div>
          <p className="text-sm text-gray-600 mt-1 leading-snug">{result.summary}</p>
        </div>
        {/* Stats row */}
        <div className="flex gap-4 text-center flex-shrink-0">
          {[
            { label: "Passed",   value: stats.passed,   color: "text-emerald-600" },
            { label: "Failed",   value: stats.failed,   color: "text-red-600" },
            { label: "Warnings", value: stats.warnings, color: "text-amber-600" },
          ].map(s => (
            <div key={s.label}>
              <div className={cn("text-xl font-bold", s.color)}>{s.value}</div>
              <div className="text-[10px] text-gray-500">{s.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-gray-100 pb-0">
        {tabs.map(t => (
          <button key={t.id} onClick={() => setActiveTab(t.id as any)}
            className={cn("px-3 py-1.5 text-xs font-medium rounded-t-lg -mb-px border border-b-white transition-all",
              activeTab === t.id
                ? "bg-white border-gray-200 text-gray-800"
                : "bg-gray-50 border-transparent text-gray-500 hover:text-gray-700",
              "warn" in t && t.warn ? "text-red-600" : ""
            )}
          >{t.label}</button>
        ))}
      </div>

      {/* Overview tab */}
      {activeTab === "overview" && (
        <div className="space-y-3">
          {/* Quick wins */}
          {result.quick_wins?.length > 0 && (
            <div className="bg-blue-50 border border-blue-100 rounded-xl p-4">
              <h3 className="text-xs font-semibold text-blue-700 mb-2 flex items-center gap-1.5">
                <Zap className="w-3.5 h-3.5" /> Quick Wins
              </h3>
              <ul className="space-y-1">
                {result.quick_wins.map((qw: string, i: number) => (
                  <li key={i} className="text-xs text-blue-600 flex items-start gap-1.5">
                    <span className="text-blue-300 mt-0.5">→</span>{qw}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {/* User impact */}
          {result.user_impact && (
            <div className="bg-purple-50 border border-purple-100 rounded-xl p-4">
              <h3 className="text-xs font-semibold text-purple-700 mb-1.5 flex items-center gap-1.5">
                <Users className="w-3.5 h-3.5" /> User Impact
              </h3>
              <p className="text-xs text-purple-600">{result.user_impact}</p>
            </div>
          )}
          {/* Principle breakdown */}
          {allChecks.length > 0 && (() => {
            const cats = ["Perceivable", "Operable", "Understandable", "Robust"];
            return (
              <div className="bg-white border border-gray-200 rounded-xl p-4">
                <h3 className="text-xs font-semibold text-gray-700 mb-3">By WCAG Principle</h3>
                <div className="space-y-2">
                  {cats.map(cat => {
                    const catChecks = allChecks.filter((c: any) => c.category === cat);
                    if (!catChecks.length) return null;
                    const catPassed = catChecks.filter((c: any) => c.status === "pass" || c.passed).length;
                    const pct = Math.round(catPassed / catChecks.length * 100);
                    return (
                      <div key={cat}>
                        <div className="flex justify-between text-[11px] mb-1">
                          <span className="text-gray-600 font-medium">{cat}</span>
                          <span className="text-gray-500">{catPassed}/{catChecks.length}</span>
                        </div>
                        <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                          <div className={cn("h-full rounded-full", pct >= 80 ? "bg-emerald-400" : pct >= 60 ? "bg-amber-400" : "bg-red-400")}
                            style={{ width: `${pct}%` }} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* Checks tab */}
      {activeTab === "checks" && (
        <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-2">
          {allChecks.map((check: any, i: number) => {
            const passing = check.status === "pass" || check.passed === true;
            const warning = check.status === "warning";
            const failing = check.status === "fail" || check.passed === false;
            return (
              <div key={i} className={cn("flex items-start gap-3 p-2.5 rounded-lg",
                passing ? "bg-gray-50" : warning ? "bg-amber-50" : "bg-red-50"
              )}>
                {passing ? <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                  : warning ? <AlertCircle className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" />
                  : <XCircle className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-xs font-medium text-gray-700">{check.name}</span>
                    <span className="text-[10px] text-gray-400 font-mono">{check.wcag_criterion}</span>
                    <span className="text-[10px] bg-gray-100 text-gray-500 px-1 rounded">{check.level}</span>
                  </div>
                  <div className="text-[11px] text-gray-500 mt-0.5">{check.finding || check.details}</div>
                  {(failing || warning) && check.recommendation && (
                    <div className={cn("text-[11px] mt-0.5", warning ? "text-amber-600" : "text-red-600")}>
                      → {check.recommendation}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Critical issues tab */}
      {activeTab === "critical" && (
        <div className="space-y-3">
          {criticalIssues.length === 0 ? (
            <div className="bg-emerald-50 border border-emerald-100 rounded-xl p-6 text-center">
              <CheckCircle className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
              <p className="text-sm text-emerald-700 font-medium">No critical issues found</p>
            </div>
          ) : criticalIssues.map((issue: any, i: number) => (
            <div key={i} className="bg-white border border-red-100 rounded-xl p-4 space-y-2">
              <div className="flex items-center gap-2">
                <XCircle className="w-4 h-4 text-red-500 flex-shrink-0" />
                <span className="text-sm font-semibold text-gray-800">{issue.issue || issue.details}</span>
                {issue.criterion && <span className="text-[10px] font-mono text-gray-400 ml-auto">{issue.criterion}</span>}
              </div>
              {issue.impact && <p className="text-xs text-gray-600 pl-6">{issue.impact}</p>}
              {issue.fix && (
                <div className="pl-6 flex items-start gap-1.5">
                  <span className="text-[10px] font-semibold text-red-600 mt-0.5">FIX:</span>
                  <p className="text-xs text-red-700">{issue.fix}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Visual data tab (image-based only) */}
      {activeTab === "visual" && result.visual_data && (
        <div className="space-y-3">
          {result.visual_data.screen_description && (
            <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
              <h3 className="text-xs font-semibold text-gray-700 mb-1">Screen Description</h3>
              <p className="text-xs text-gray-600">{result.visual_data.screen_description}</p>
            </div>
          )}
          {result.visual_data.estimated_colors && (
            <div className="bg-white border border-gray-200 rounded-xl p-4">
              <h3 className="text-xs font-semibold text-gray-700 mb-3">Extracted Colors</h3>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(result.visual_data.estimated_colors).map(([key, val]: [string, any]) => (
                  val && !val.toString().includes("approx") && (
                    <div key={key} className="flex items-center gap-2">
                      <div className="w-5 h-5 rounded border border-gray-200 flex-shrink-0" style={{ background: val }} />
                      <div>
                        <div className="text-[10px] text-gray-500 capitalize">{key.replace(/_/g, " ")}</div>
                        <div className="text-[10px] font-mono text-gray-700">{val}</div>
                      </div>
                    </div>
                  )
                ))}
              </div>
            </div>
          )}
          {result.visual_data.obvious_violations?.length > 0 && (
            <div className="bg-red-50 border border-red-100 rounded-xl p-4">
              <h3 className="text-xs font-semibold text-red-700 mb-2">Visual Violations Detected</h3>
              <ul className="space-y-1">
                {result.visual_data.obvious_violations.map((v: any, i: number) => (
                  <li key={i} className="text-xs text-red-600 flex items-start gap-1.5">
                    <span className="text-red-400 mt-0.5">→</span>
                    <span><span className="font-mono text-[10px]">{v.wcag_criterion}</span> — {v.issue}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
