"use client";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { Code, Eye, FileText, Layers, Copy, Check, ExternalLink, Cpu, Clock } from "lucide-react";
import { cn } from "@/lib/utils/cn";
import { api } from "@/lib/api/client";
import { ModelBadge } from "./ModelBadge";
import { DesignCanvas } from "@/components/canvas/DesignCanvas";

interface Props {
  artifactId: string;
}

type ViewMode = "preview" | "json" | "code";

export function ArtifactViewer({ artifactId }: Props) {
  const [viewMode, setViewMode] = useState<ViewMode>("preview");
  const [copied, setCopied] = useState(false);
  const [activeScreen, setActiveScreen] = useState(0);

  const { data: artifact, isLoading } = useQuery({
    queryKey: ["artifact", artifactId],
    queryFn: () => api.get(`/artifacts/${artifactId}`).then(r => r.data),
    enabled: !!artifactId,
    refetchInterval: 5000,
  });

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-brand-200 border-t-brand-500 rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm text-surface-500">Loading artifact...</p>
        </div>
      </div>
    );
  }

  if (!artifact) return null;

  const content = artifact.content || {};
  const hasHTML = getScreens(content).some((s: any) => s.html);
  const hasCode = getScreens(content).some((s: any) => s.react_component);

  const copyJSON = async () => {
    await navigator.clipboard.writeText(JSON.stringify(content, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="h-full flex flex-col"
    >
      {/* Artifact header */}
      <div className="bg-white rounded-xl border border-surface-200 mb-4 p-4">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <ArtifactTypeIcon type={artifact.type} />
              <h2 className="text-sm font-semibold text-surface-900">{artifact.name}</h2>
              <StatusBadge status={artifact.status} />
            </div>
            <div className="flex items-center gap-3 text-2xs text-surface-400">
              {artifact.agent_type && (
                <span className="flex items-center gap-1">
                  <Cpu className="w-3 h-3" />
                  {artifact.agent_type} agent
                </span>
              )}
              {artifact.model_used && <ModelBadge model={artifact.model_used} />}
              {artifact.tokens_used && (
                <span>{artifact.tokens_used.toLocaleString()} tokens</span>
              )}
              {artifact.complexity_score && (
                <span>Complexity {artifact.complexity_score}/10</span>
              )}
            </div>
          </div>

          {/* View mode toggle */}
          <div className="flex items-center gap-1 bg-surface-100 rounded-lg p-1">
            {([
              { id: "preview", icon: Eye, label: "Preview" },
              ...(hasCode ? [{ id: "code", icon: Code, label: "Code" }] : []),
              { id: "json", icon: FileText, label: "JSON" },
            ] as { id: ViewMode; icon: any; label: string }[]).map(({ id, icon: Icon, label }) => (
              <button
                key={id}
                onClick={() => setViewMode(id)}
                className={cn(
                  "flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium transition-all",
                  viewMode === id
                    ? "bg-white text-surface-900 shadow-xs"
                    : "text-surface-500 hover:text-surface-700"
                )}
              >
                <Icon className="w-3 h-3" />
                {label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 bg-white rounded-xl border border-surface-200 overflow-hidden flex flex-col">
        {viewMode === "preview" && <PreviewView content={content} type={artifact.type} />}
        {viewMode === "json" && (
          <div className="flex-1 relative overflow-auto">
            <button
              onClick={copyJSON}
              className="absolute top-4 right-4 flex items-center gap-1.5 text-xs text-surface-500
                         hover:text-surface-700 bg-white border border-surface-200 rounded-md px-2 py-1 z-10"
            >
              {copied ? <Check className="w-3 h-3 text-emerald-500" /> : <Copy className="w-3 h-3" />}
              {copied ? "Copied" : "Copy"}
            </button>
            <pre className="p-5 text-xs font-mono text-surface-700 leading-relaxed overflow-auto whitespace-pre-wrap">
              {JSON.stringify(content, null, 2)}
            </pre>
          </div>
        )}
        {viewMode === "code" && (
          <div className="flex-1 overflow-auto">
            <ScreenTabs screens={getScreens(content)} activeScreen={activeScreen} onSelect={setActiveScreen} />
            <div className="p-4">
              <pre className="text-xs font-mono text-surface-700 leading-relaxed bg-surface-50
                              rounded-lg p-4 overflow-auto">
                {getScreens(content)[activeScreen]?.react_component || "No code available"}
              </pre>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
}

function PreviewView({ content, type }: { content: any; type: string }) {
  if (type === "review_report") return <ReviewPreview content={content} />;
  if (type === "requirement") return <RequirementPreview content={content} />;
  if (type === "user_flow") return <UXPreview content={content} />;
  if (type === "hifi_screen") return <UIPreview content={content} />;
  return <GenericPreview content={content} />;
}

function RequirementPreview({ content }: { content: any }) {
  return (
    <div className="flex-1 overflow-auto p-6 space-y-5">
      {content.executive_summary && (
        <div className="p-4 bg-brand-50 rounded-lg border border-brand-100">
          <p className="text-sm text-brand-800 leading-relaxed">{content.executive_summary}</p>
        </div>
      )}

      {content.user_stories?.length > 0 && (
        <div>
          <h3 className="text-xs font-semibold text-surface-700 uppercase tracking-wider mb-3">User Stories</h3>
          <div className="space-y-2">
            {content.user_stories.map((story: any, i: number) => (
              <div key={i} className="p-3 bg-surface-50 rounded-lg border border-surface-200">
                <div className="flex items-start gap-2">
                  <span className="text-2xs bg-brand-100 text-brand-700 px-1.5 py-0.5 rounded font-mono">
                    {story.id}
                  </span>
                  <div>
                    <p className="text-xs text-surface-700">
                      <span className="font-medium">As a</span> {story.as_a},{" "}
                      <span className="font-medium">I want to</span> {story.i_want}{" "}
                      <span className="font-medium">so that</span> {story.so_that}
                    </p>
                    {story.acceptance_criteria?.length > 0 && (
                      <ul className="mt-1.5 space-y-0.5">
                        {story.acceptance_criteria.map((ac: string, j: number) => (
                          <li key={j} className="text-2xs text-surface-500 flex items-start gap-1">
                            <span className="text-emerald-500 mt-0.5">✓</span> {ac}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {content.screens_needed?.length > 0 && (
        <div>
          <h3 className="text-xs font-semibold text-surface-700 uppercase tracking-wider mb-2">Screens Needed</h3>
          <div className="flex flex-wrap gap-2">
            {content.screens_needed.map((screen: string, i: number) => (
              <span key={i} className="text-xs bg-surface-100 text-surface-600 px-2.5 py-1 rounded-full border border-surface-200">
                {screen}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function UXPreview({ content }: { content: any }) {
  return (
    <div className="flex-1 overflow-auto p-6 space-y-5">
      {content.screens?.map((screen: any, i: number) => (
        <div key={i} className="border border-surface-200 rounded-lg overflow-hidden">
          <div className="px-4 py-2.5 bg-surface-50 border-b border-surface-200 flex items-center justify-between">
            <span className="text-xs font-semibold text-surface-800">{screen.name}</span>
            <span className="text-2xs text-surface-400 bg-surface-100 px-2 py-0.5 rounded capitalize">
              {screen.layout_type}
            </span>
          </div>
          <div className="p-4 space-y-2">
            <p className="text-xs text-surface-600">{screen.purpose}</p>
            <div className="grid grid-cols-2 gap-2">
              {screen.sections?.map((section: any, j: number) => (
                <div key={j} className="p-2.5 bg-surface-50 rounded-lg border border-surface-100">
                  <div className="text-2xs font-medium text-surface-700 mb-1 flex items-center justify-between">
                    {section.name}
                    <span className="text-surface-400 bg-white border border-surface-200 px-1.5 rounded capitalize">
                      {section.position}
                    </span>
                  </div>
                  <p className="text-2xs text-surface-500">{section.content}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function UIPreview({ content }: { content: any }) {
  // Use V1 DesignCanvas for data-driven rendering — no hardcoding
  if (content.screens && content.screens.length > 0 && content.screens[0].elements) {
    return (
      <div className="flex-1 overflow-auto p-4">
        <DesignCanvas design={content} />
      </div>
    );
  }

  // Fallback for HTML-based screens
  const screens = content.screens || [];
  return (
    <div className="flex-1 overflow-auto">
      {screens.map((screen: any, i: number) => (
        <div key={i} className="border-b border-surface-100 last:border-0">
          <div className="px-4 py-2.5 bg-surface-50 border-b border-surface-100 flex items-center gap-2">
            <span className="text-xs font-semibold text-surface-800">{screen.name}</span>
          </div>
          {screen.html ? (
            <div className="p-4">
              <div
                className="border border-surface-200 rounded-lg overflow-auto"
                style={{ maxHeight: "600px" }}
                dangerouslySetInnerHTML={{ __html: screen.html }}
              />
            </div>
          ) : (
            <div className="p-4 text-xs text-surface-500">
              <pre className="whitespace-pre-wrap">{JSON.stringify(screen, null, 2)}</pre>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function ReviewPreview({ content }: { content: any }) {
  const statusColors = {
    approved: "text-emerald-700 bg-emerald-50 border-emerald-200",
    approved_with_changes: "text-amber-700 bg-amber-50 border-amber-200",
    rejected: "text-red-700 bg-red-50 border-red-200",
  };

  return (
    <div className="flex-1 overflow-auto p-6 space-y-5">
      {/* Score */}
      <div className="flex items-center gap-4">
        <div className="text-4xl font-bold text-surface-900">{content.overall_score}</div>
        <div>
          <div className={cn(
            "text-xs font-semibold px-2.5 py-1 rounded-full border capitalize",
            statusColors[content.overall_status as keyof typeof statusColors] || "text-surface-600 bg-surface-50 border-surface-200"
          )}>
            {content.overall_status?.replace("_", " ")}
          </div>
          <p className="text-xs text-surface-500 mt-1">{content.summary}</p>
        </div>
      </div>

      {/* Issues */}
      {content.recommended_changes?.length > 0 && (
        <div>
          <h3 className="text-xs font-semibold text-surface-700 uppercase tracking-wider mb-3">
            Recommended Changes
          </h3>
          <div className="space-y-2">
            {content.recommended_changes.map((change: any, i: number) => (
              <div key={i} className={cn(
                "p-3 rounded-lg border text-xs",
                change.priority === "critical" ? "bg-red-50 border-red-200" :
                change.priority === "high" ? "bg-amber-50 border-amber-200" :
                "bg-surface-50 border-surface-200"
              )}>
                <div className="flex items-start justify-between gap-2">
                  <span className="font-medium text-surface-800">{change.area}</span>
                  <span className={cn(
                    "text-2xs px-1.5 py-0.5 rounded capitalize flex-shrink-0",
                    change.priority === "critical" ? "bg-red-100 text-red-700" :
                    change.priority === "high" ? "bg-amber-100 text-amber-700" :
                    "bg-surface-100 text-surface-600"
                  )}>
                    {change.priority}
                  </span>
                </div>
                <p className="text-surface-700 mt-0.5">{change.change}</p>
                <p className="text-surface-500 mt-0.5">{change.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function GenericPreview({ content }: { content: any }) {
  return (
    <div className="flex-1 overflow-auto p-6">
      <pre className="text-xs font-mono text-surface-700 whitespace-pre-wrap leading-relaxed">
        {JSON.stringify(content, null, 2)}
      </pre>
    </div>
  );
}

function ScreenTabs({ screens, activeScreen, onSelect }: any) {
  if (!screens?.length) return null;
  return (
    <div className="flex gap-1 p-3 border-b border-surface-100 overflow-x-auto">
      {screens.map((screen: any, i: number) => (
        <button
          key={i}
          onClick={() => onSelect(i)}
          className={cn(
            "flex-shrink-0 px-3 py-1.5 text-xs font-medium rounded-md transition-all",
            activeScreen === i
              ? "bg-surface-900 text-white"
              : "text-surface-500 hover:text-surface-700 hover:bg-surface-100"
          )}
        >
          {screen.name || `Screen ${i + 1}`}
        </button>
      ))}
    </div>
  );
}

function ArtifactTypeIcon({ type }: { type: string }) {
  const icons: Record<string, string> = {
    requirement: "📋",
    user_flow: "🎯",
    wireframe: "📐",
    hifi_screen: "🎨",
    review_report: "✅",
  };
  return <span className="text-base">{icons[type] || "📄"}</span>;
}

function StatusBadge({ status }: { status: string }) {
  const config: Record<string, { label: string; className: string }> = {
    draft: { label: "Draft", className: "bg-surface-100 text-surface-600" },
    pending_approval: { label: "Awaiting Review", className: "bg-amber-50 text-amber-700 border border-amber-200" },
    approved: { label: "Approved", className: "bg-emerald-50 text-emerald-700" },
    rejected: { label: "Rejected", className: "bg-red-50 text-red-700" },
  };
  const cfg = config[status] || { label: status, className: "bg-surface-100 text-surface-600" };
  return (
    <span className={cn("text-2xs px-2 py-0.5 rounded-full font-medium", cfg.className)}>
      {cfg.label}
    </span>
  );
}

function getScreens(content: any): any[] {
  return content.screens || [];
}
