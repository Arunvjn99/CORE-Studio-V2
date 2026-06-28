"use client";
import { useState, useCallback } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import {
  Upload, BookOpen, Search, FileText, Trash2,
  CheckCircle, Clock, AlertCircle, FolderOpen,
  ChevronRight, Database, Plus
} from "lucide-react";
import { api } from "@/lib/api/client";
import { cn } from "@/lib/utils/cn";

const CATEGORIES = [
  {
    id: "domain",
    label: "Domain Knowledge",
    description: "Industry-specific knowledge (retirement, loan, insurance...)",
    icon: "🏛️",
    subcategories: ["retirement", "loan", "insurance", "healthcare", "banking"],
  },
  {
    id: "company",
    label: "Company Standards",
    description: "UX standards, branding, accessibility, compliance rules",
    icon: "🏢",
    subcategories: ["ux-standards", "branding", "accessibility", "compliance", "approved-patterns"],
  },
  {
    id: "design_system",
    label: "Design Systems",
    description: "Component libraries and design system documentation",
    icon: "🎨",
    subcategories: ["material", "shadcn", "apple", "linear", "stripe", "custom"],
  },
];

export default function KnowledgePage() {
  const qc = useQueryClient();
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadForm, setUploadForm] = useState({ category: "domain", subcategory: "" });
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searching, setSearching] = useState(false);

  const { data: documents = [], isLoading } = useQuery({
    queryKey: ["knowledge-docs", activeCategory],
    queryFn: () => api.get("/knowledge", {
      params: activeCategory ? { category: activeCategory } : {}
    }).then(r => r.data),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.delete(`/knowledge/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["knowledge-docs"] });
      toast.success("Document deleted");
    },
  });

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("category", uploadForm.category);
    if (uploadForm.subcategory) formData.append("subcategory", uploadForm.subcategory);

    setUploading(true);
    try {
      await api.post("/knowledge/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      qc.invalidateQueries({ queryKey: ["knowledge-docs"] });
      toast.success(`"${file.name}" uploaded and indexing...`);
    } catch {
      toast.error("Upload failed");
    } finally {
      setUploading(false);
    }
    e.target.value = "";
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearching(true);
    try {
      const res = await api.post("/knowledge/search", {
        query: searchQuery,
        category: activeCategory || undefined,
        top_k: 5,
      });
      setSearchResults(res.data.results);
    } catch {
      toast.error("Search failed");
    } finally {
      setSearching(false);
    }
  };

  const statusIcon = (status: string) => {
    if (status === "indexed") return <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />;
    if (status === "processing") return <Clock className="w-3.5 h-3.5 text-amber-500 animate-spin" />;
    return <AlertCircle className="w-3.5 h-3.5 text-red-500" />;
  };

  return (
    <div className="p-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-semibold text-surface-900">Knowledge Base</h1>
          <p className="text-sm text-surface-500 mt-0.5">
            Organizational knowledge that powers every agent
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs text-surface-500 bg-brand-50 border border-brand-100 px-3 py-2 rounded-lg">
          <Database className="w-3.5 h-3.5 text-brand-500" />
          <span className="text-brand-700">{documents.length} documents indexed</span>
        </div>
      </div>

      <div className="grid grid-cols-[220px_1fr] gap-6">
        {/* Category sidebar */}
        <div className="space-y-1">
          <button
            onClick={() => setActiveCategory(null)}
            className={cn("sidebar-item w-full", !activeCategory && "sidebar-item-active")}
          >
            <FolderOpen className="w-4 h-4" />
            All Documents
          </button>
          {CATEGORIES.map(cat => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={cn("sidebar-item w-full text-left", activeCategory === cat.id && "sidebar-item-active")}
            >
              <span>{cat.icon}</span>
              {cat.label}
            </button>
          ))}
        </div>

        {/* Main content */}
        <div className="space-y-5">
          {/* Category info + upload */}
          {activeCategory && (
            <div className="bg-white rounded-xl border border-surface-200 p-5">
              {CATEGORIES.filter(c => c.id === activeCategory).map(cat => (
                <div key={cat.id}>
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-lg">{cat.icon}</span>
                        <h3 className="text-sm font-semibold text-surface-900">{cat.label}</h3>
                      </div>
                      <p className="text-xs text-surface-500">{cat.description}</p>
                    </div>
                    <label className={cn(
                      "flex items-center gap-1.5 h-8 px-4 bg-brand-500 hover:bg-brand-600 text-white",
                      "text-xs font-medium rounded-lg cursor-pointer transition-colors",
                      uploading && "opacity-50 pointer-events-none"
                    )}>
                      {uploading ? (
                        <div className="w-3 h-3 border border-white/30 border-t-white rounded-full animate-spin" />
                      ) : (
                        <Upload className="w-3.5 h-3.5" />
                      )}
                      Upload
                      <input type="file" className="hidden" accept=".pdf,.docx,.txt,.md" onChange={handleUpload} />
                    </label>
                  </div>

                  {/* Subcategory select */}
                  <div className="mt-3 flex gap-2 flex-wrap">
                    {cat.subcategories.map(sub => (
                      <button
                        key={sub}
                        onClick={() => setUploadForm(f => ({ ...f, subcategory: f.subcategory === sub ? "" : sub }))}
                        className={cn(
                          "text-xs px-2.5 py-1 rounded-full border capitalize transition-all",
                          uploadForm.subcategory === sub
                            ? "bg-brand-500 text-white border-brand-500"
                            : "bg-surface-50 text-surface-600 border-surface-200 hover:border-surface-300"
                        )}
                      >
                        {sub}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Semantic search */}
          <div className="bg-white rounded-xl border border-surface-200 p-4">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-400" />
                <input
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  onKeyDown={e => e.key === "Enter" && handleSearch()}
                  placeholder="Search knowledge base semantically..."
                  className="w-full h-9 pl-9 pr-3 text-sm rounded-lg border border-surface-200
                             focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100"
                />
              </div>
              <button
                onClick={handleSearch}
                disabled={searching}
                className="h-9 px-4 bg-surface-900 hover:bg-surface-800 text-white text-sm
                           font-medium rounded-lg transition-colors disabled:opacity-50"
              >
                {searching ? "..." : "Search"}
              </button>
            </div>

            {searchResults.length > 0 && (
              <div className="mt-3 space-y-2">
                {searchResults.map((r, i) => (
                  <div key={i} className="p-3 bg-surface-50 rounded-lg border border-surface-200">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-2xs font-medium text-surface-700">{r.document_name}</span>
                      <span className="text-2xs text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded">
                        {Math.round(r.similarity * 100)}% match
                      </span>
                    </div>
                    <p className="text-xs text-surface-600 line-clamp-3 leading-relaxed">{r.content}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Documents list */}
          {!isLoading && documents.length === 0 ? (
            <div className="text-center py-16">
              <div className="w-12 h-12 rounded-2xl bg-brand-50 flex items-center justify-center mx-auto mb-4">
                <BookOpen className="w-6 h-6 text-brand-500" />
              </div>
              <h3 className="text-sm font-semibold text-surface-900 mb-1">No knowledge yet</h3>
              <p className="text-xs text-surface-500 mb-4">
                Upload PDF, Word, or Markdown files to build organizational knowledge.
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {documents.map((doc: any) => (
                <motion.div
                  key={doc.id}
                  initial={{ opacity: 0, y: 4 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-center gap-4 p-4 bg-white rounded-xl border border-surface-200
                             hover:border-surface-300 transition-all group"
                >
                  <div className="flex items-center justify-center w-9 h-9 bg-surface-100 rounded-lg flex-shrink-0">
                    <FileText className="w-4 h-4 text-surface-500" />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      {statusIcon(doc.status)}
                      <span className="text-sm font-medium text-surface-800 truncate">{doc.name}</span>
                    </div>
                    <div className="flex items-center gap-2 text-2xs text-surface-400">
                      <span className="capitalize bg-surface-100 px-1.5 py-0.5 rounded">{doc.category}</span>
                      {doc.subcategory && <span>/ {doc.subcategory}</span>}
                      {doc.chunk_count > 0 && <span>{doc.chunk_count} chunks</span>}
                      <span className="uppercase">{doc.file_type}</span>
                    </div>
                  </div>

                  <button
                    onClick={() => deleteMutation.mutate(doc.id)}
                    className="opacity-0 group-hover:opacity-100 p-1.5 text-surface-400 hover:text-red-500
                               hover:bg-red-50 rounded-md transition-all"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
