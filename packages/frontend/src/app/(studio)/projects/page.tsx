"use client";
import { useState } from "react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { Plus, FolderOpen, ChevronRight, Wand2, Search, ArrowRight, Sparkles } from "lucide-react";
import { toast } from "sonner";
import { api } from "@/lib/api/client";
import { cn } from "@/lib/utils/cn";
import { formatDistanceToNow } from "date-fns";

const DOMAINS = ["retirement", "loan", "insurance", "healthcare", "banking", "other"];
const DOMAIN_COLORS: Record<string, string> = {
  retirement: "bg-violet-50 text-violet-700 border-violet-100",
  loan: "bg-blue-50 text-blue-700 border-blue-100",
  insurance: "bg-emerald-50 text-emerald-700 border-emerald-100",
  healthcare: "bg-red-50 text-red-700 border-red-100",
  banking: "bg-amber-50 text-amber-700 border-amber-100",
  other: "bg-surface-50 text-surface-600 border-surface-100",
};

interface Project {
  id: string;
  name: string;
  description?: string;
  domain: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export default function ProjectsPage() {
  const qc = useQueryClient();
  const [creating, setCreating] = useState(false);
  const [search, setSearch] = useState("");
  const [form, setForm] = useState({ name: "", description: "", domain: "other" });

  const { data: projects = [], isLoading } = useQuery<Project[]>({
    queryKey: ["projects"],
    queryFn: () => api.get("/projects").then(r => r.data),
  });

  const createMutation = useMutation({
    mutationFn: (data: typeof form) => api.post("/projects", data).then(r => r.data),
    onSuccess: (project) => {
      qc.invalidateQueries({ queryKey: ["projects"] });
      setCreating(false);
      setForm({ name: "", description: "", domain: "other" });
      toast.success(`Project "${project.name}" created`);
    },
    onError: () => toast.error("Failed to create project"),
  });

  const filtered = projects.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.description?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-semibold text-surface-900">Projects</h1>
          <p className="text-sm text-surface-500 mt-0.5">
            {projects.length} project{projects.length !== 1 ? "s" : ""}
          </p>
        </div>
        <button
          onClick={() => setCreating(true)}
          className="flex items-center gap-1.5 h-9 px-4 bg-brand-500 hover:bg-brand-600
                     text-white text-sm font-medium rounded-lg transition-colors"
        >
          <Plus className="w-4 h-4" />
          New Project
        </button>
      </div>

      {/* Search */}
      {projects.length > 0 && (
        <div className="relative mb-6">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-400" />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search projects..."
            className="w-full max-w-sm h-9 pl-9 pr-3 text-sm rounded-lg border border-surface-200
                       focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100"
          />
        </div>
      )}

      {/* Create project form */}
      <AnimatePresence>
        {creating && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="mb-6 p-5 bg-white border border-surface-200 rounded-xl shadow-sm"
          >
            <h3 className="text-sm font-semibold text-surface-900 mb-4">New Project</h3>
            <div className="space-y-3">
              <input
                value={form.name}
                onChange={e => setForm({ ...form, name: e.target.value })}
                placeholder="Project name (e.g. Loan Center Portal)"
                className="w-full h-9 px-3 text-sm rounded-lg border border-surface-200
                           focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100"
              />
              <input
                value={form.description}
                onChange={e => setForm({ ...form, description: e.target.value })}
                placeholder="Brief description (optional)"
                className="w-full h-9 px-3 text-sm rounded-lg border border-surface-200
                           focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100"
              />
              <div className="flex gap-2 flex-wrap">
                {DOMAINS.map(d => (
                  <button
                    key={d}
                    onClick={() => setForm({ ...form, domain: d })}
                    className={cn(
                      "px-3 py-1 text-xs rounded-full border capitalize transition-all",
                      form.domain === d
                        ? "bg-brand-500 text-white border-brand-500"
                        : "bg-surface-50 text-surface-600 border-surface-200 hover:border-surface-300"
                    )}
                  >
                    {d}
                  </button>
                ))}
              </div>
              <div className="flex gap-2 pt-1">
                <button
                  onClick={() => createMutation.mutate(form)}
                  disabled={!form.name.trim() || createMutation.isPending}
                  className="h-8 px-4 bg-brand-500 hover:bg-brand-600 text-white text-sm font-medium
                             rounded-lg transition-colors disabled:opacity-50"
                >
                  {createMutation.isPending ? "Creating..." : "Create"}
                </button>
                <button
                  onClick={() => setCreating(false)}
                  className="h-8 px-4 text-sm text-surface-600 hover:text-surface-900 rounded-lg
                             hover:bg-surface-100 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Empty state */}
      {!isLoading && projects.length === 0 && (
        <div className="flex flex-col items-center justify-center py-24 text-center">
          <div className="w-12 h-12 rounded-2xl bg-brand-50 flex items-center justify-center mb-4">
            <Wand2 className="w-6 h-6 text-brand-500" />
          </div>
          <h3 className="text-base font-semibold text-surface-900 mb-1">No projects yet</h3>
          <p className="text-sm text-surface-500 mb-6 max-w-sm">
            Create your first project to start designing with AI agents.
          </p>
          <button
            onClick={() => setCreating(true)}
            className="flex items-center gap-1.5 h-9 px-5 bg-brand-500 hover:bg-brand-600
                       text-white text-sm font-medium rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4" />
            Create Project
          </button>
        </div>
      )}

      {/* Project grid */}
      {!isLoading && filtered.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((project, i) => (
            <motion.div
              key={project.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.04 }}
            >
              <Link href={`/projects/${project.id}`}>
                <div className="group bg-white border border-surface-200 rounded-xl p-5
                                hover:border-brand-200 hover:shadow-sm transition-all duration-150">
                  {/* Domain badge */}
                  <div className="flex items-start justify-between mb-3">
                    <span className={cn(
                      "text-2xs font-medium px-2 py-0.5 rounded-full border capitalize",
                      DOMAIN_COLORS[project.domain] || DOMAIN_COLORS.other
                    )}>
                      {project.domain}
                    </span>
                    <ChevronRight className="w-4 h-4 text-surface-300 group-hover:text-brand-400
                                             group-hover:translate-x-0.5 transition-all" />
                  </div>

                  <h3 className="text-sm font-semibold text-surface-900 mb-1 group-hover:text-brand-600
                                  transition-colors">
                    {project.name}
                  </h3>

                  {project.description && (
                    <p className="text-xs text-surface-500 leading-relaxed line-clamp-2 mb-4">
                      {project.description}
                    </p>
                  )}

                  <div className="flex items-center justify-between pt-3 border-t border-surface-100">
                    <span className="text-2xs text-surface-400">
                      {formatDistanceToNow(new Date(project.updated_at), { addSuffix: true })}
                    </span>
                    <div className="flex items-center gap-1 text-2xs text-brand-500 opacity-0
                                    group-hover:opacity-100 transition-opacity font-medium">
                      Open <ArrowRight className="w-3 h-3" />
                    </div>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
