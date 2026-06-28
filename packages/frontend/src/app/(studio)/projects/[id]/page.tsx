"use client";
import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import {
  ArrowLeft, Wand2, Plus, FileText, Layers, Monitor,
  Clock, CheckCircle, AlertCircle, ChevronRight, Cpu
} from "lucide-react";
import { api } from "@/lib/api/client";
import { cn } from "@/lib/utils/cn";
import { formatDistanceToNow } from "date-fns";
import { ModelBadge } from "@/components/studio/ModelBadge";

const ARTIFACT_ICONS: Record<string, string> = {
  requirement: "📋",
  user_flow: "🎯",
  wireframe: "📐",
  hifi_screen: "🎨",
  review_report: "✅",
  code_react: "⚛️",
  documentation: "📖",
};

export default function ProjectDetailPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;

  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => api.get(`/projects/${projectId}`).then(r => r.data),
  });

  const { data: artifacts = [] } = useQuery({
    queryKey: ["artifacts", projectId],
    queryFn: () => api.get(`/projects/${projectId}/artifacts`).then(r => r.data),
    refetchInterval: 10000,
  });

  const artifactsByType = artifacts.reduce((acc: any, a: any) => {
    if (!acc[a.type]) acc[a.type] = [];
    acc[a.type].push(a);
    return acc;
  }, {});

  return (
    <div className="p-8 max-w-6xl mx-auto">
      {/* Back + header */}
      <div className="mb-8">
        <Link
          href="/projects"
          className="inline-flex items-center gap-1.5 text-sm text-surface-500 hover:text-surface-700 mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          Projects
        </Link>

        {project && (
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-semibold text-surface-900">{project.name}</h1>
              {project.description && (
                <p className="text-sm text-surface-500 mt-1">{project.description}</p>
              )}
              <div className="flex items-center gap-2 mt-2">
                <span className="text-xs bg-surface-100 text-surface-600 px-2 py-0.5 rounded capitalize">
                  {project.domain}
                </span>
                <span className="text-xs text-surface-400">
                  Updated {formatDistanceToNow(new Date(project.updated_at), { addSuffix: true })}
                </span>
              </div>
            </div>

            <Link
              href={`/studio?project=${projectId}`}
              className="flex items-center gap-1.5 h-9 px-4 bg-brand-500 hover:bg-brand-600
                         text-white text-sm font-medium rounded-lg transition-colors"
            >
              <Wand2 className="w-4 h-4" />
              Design Studio
            </Link>
          </div>
        )}
      </div>

      {/* Artifacts */}
      {artifacts.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-24 text-center">
          <div className="w-12 h-12 rounded-2xl bg-brand-50 flex items-center justify-center mb-4">
            <Layers className="w-6 h-6 text-brand-500" />
          </div>
          <h3 className="text-base font-semibold text-surface-900 mb-1">No artifacts yet</h3>
          <p className="text-sm text-surface-500 mb-6">
            Start a design in the studio to generate requirements, flows, and screens.
          </p>
          <Link
            href={`/studio?project=${projectId}`}
            className="flex items-center gap-1.5 h-9 px-5 bg-brand-500 hover:bg-brand-600
                       text-white text-sm font-medium rounded-lg transition-colors"
          >
            <Wand2 className="w-4 h-4" />
            Open Studio
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {Object.entries(artifactsByType).map(([type, typeArtifacts]: [string, any]) => (
            <div key={type}>
              <div className="flex items-center gap-2 mb-3">
                <span className="text-base">{ARTIFACT_ICONS[type] || "📄"}</span>
                <h2 className="text-sm font-semibold text-surface-800 capitalize">
                  {type.replace("_", " ")}s
                </h2>
                <span className="text-xs text-surface-400 bg-surface-100 px-1.5 rounded">
                  {typeArtifacts.length}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {typeArtifacts.map((artifact: any) => (
                  <motion.div
                    key={artifact.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="group artifact-card"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <ArtifactStatus status={artifact.status} />
                          <span className="text-sm font-medium text-surface-800 truncate">
                            {artifact.name}
                          </span>
                        </div>
                        <div className="flex items-center gap-2 text-2xs text-surface-400">
                          {artifact.model_used && <ModelBadge model={artifact.model_used} />}
                          {artifact.tokens_used && (
                            <span>{artifact.tokens_used.toLocaleString()} tokens</span>
                          )}
                          <span>{formatDistanceToNow(new Date(artifact.created_at), { addSuffix: true })}</span>
                        </div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-surface-300 group-hover:text-brand-400
                                               opacity-0 group-hover:opacity-100 flex-shrink-0 transition-all" />
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function ArtifactStatus({ status }: { status: string }) {
  const config: Record<string, { icon: React.ReactNode; className: string }> = {
    approved: {
      icon: <CheckCircle className="w-3 h-3" />,
      className: "text-emerald-500",
    },
    pending_approval: {
      icon: <Clock className="w-3 h-3" />,
      className: "text-amber-500",
    },
    rejected: {
      icon: <AlertCircle className="w-3 h-3" />,
      className: "text-red-500",
    },
    draft: {
      icon: <div className="w-2 h-2 rounded-full bg-surface-300" />,
      className: "text-surface-400",
    },
  };
  const cfg = config[status] || config.draft;
  return <span className={cfg.className}>{cfg.icon}</span>;
}
