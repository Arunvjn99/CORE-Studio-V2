"use client";
import { useState, useRef, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import {
  Upload, FileText, Trash2, Send, Sparkles, BookOpen, Loader2,
  FileSearch, X, CheckCircle, AlertCircle, ArrowRight, MessageSquare,
  ChevronRight,
} from "lucide-react";
import { api } from "@/lib/api/client";
import { cn } from "@/lib/utils/cn";

// ── Types ────────────────────────────────────────────────────────────────────

interface KnowledgeDoc {
  id: string;
  name: string;
  category: string;
  subcategory?: string;
  file_type: string;
  status: "processing" | "indexed" | "failed";
  chunk_count?: number;
  created_at: string;
}

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: { name: string; relevance: number }[];
  next_steps?: string[];
  domain?: string;
  has_context?: boolean;
}

const CATEGORY_OPTIONS = [
  { value: "guidelines", label: "Guidelines" },
  { value: "company_standards", label: "Company Standards" },
  { value: "compliance", label: "Compliance" },
  { value: "design_patterns", label: "Design Patterns" },
  { value: "past_designs", label: "Past Designs" },
  { value: "documents", label: "General Documents" },
];

const DOMAIN_COLORS: Record<string, string> = {
  retirement: "#5B5EF4",
  loan: "#FF9500",
  insurance: "#34C759",
  tax: "#FF3B30",
  investment: "#007AFF",
  general: "#8A8A8A",
};

const DOMAIN_LABELS: Record<string, string> = {
  retirement: "Retirement Planning",
  loan: "Loan & Mortgage",
  insurance: "Insurance",
  tax: "Tax Planning",
  investment: "Investment",
  general: "General",
};

const STARTER_QUESTIONS = [
  "What is the maximum 401(k) contribution limit this year?",
  "How does compound interest affect my loan repayment?",
  "When should I start taking Social Security benefits?",
  "What's the difference between a Traditional IRA and Roth IRA?",
];

// ── Main Component ───────────────────────────────────────────────────────────

export default function DocumentsPage() {
  const qc = useQueryClient();

  // Upload
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadCategory, setUploadCategory] = useState("documents");
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Chat
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isAsking, setIsAsking] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const { data: docs = [], refetch: refetchDocs } = useQuery<KnowledgeDoc[]>({
    queryKey: ["knowledge-docs"],
    queryFn: () => api.get("/knowledge/").then((r) => r.data),
    refetchInterval: (query) => {
      const data = query.state.data as KnowledgeDoc[] | undefined;
      return data?.some((d) => d.status === "processing") ? 3000 : false;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.delete(`/knowledge/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["knowledge-docs"] });
      toast.success("Document removed");
    },
  });

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // ── Upload ─────────────────────────────────────────────────────────────────

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const ext = file.name.split(".").pop()?.toLowerCase();
    if (!["pdf", "docx", "txt", "md"].includes(ext || "")) {
      toast.error("Only PDF, DOCX, TXT, and MD files are supported");
      return;
    }
    setUploadFile(file);
  };

  const handleUpload = async () => {
    if (!uploadFile) return;
    setIsUploading(true);
    try {
      const form = new FormData();
      form.append("file", uploadFile);
      form.append("category", uploadCategory);
      await api.post("/knowledge/upload", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      toast.success(`"${uploadFile.name}" uploaded — indexing in background`);
      setUploadFile(null);
      if (fileInputRef.current) fileInputRef.current.value = "";
      refetchDocs();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  // ── Ask ────────────────────────────────────────────────────────────────────

  const handleAsk = async (question?: string) => {
    const q = (question ?? inputValue).trim();
    if (!q || isAsking) return;
    setInputValue("");

    const userMsg: ChatMessage = {
      id: `u-${Date.now()}`,
      role: "user",
      content: q,
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsAsking(true);

    try {
      const history = messages.slice(-8).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await api.post("/knowledge/ask", {
        question: q,
        top_k: 8,
        conversation_history: history,
      });

      const data = res.data;
      setMessages((prev) => [
        ...prev,
        {
          id: `a-${Date.now()}`,
          role: "assistant",
          content: data.answer,
          sources: data.sources,
          next_steps: data.next_steps,
          domain: data.domain,
          has_context: data.has_context,
        },
      ]);
    } catch {
      toast.error("Failed to get an answer");
      setMessages((prev) => prev.filter((m) => m.id !== userMsg.id));
    } finally {
      setIsAsking(false);
    }
  };

  const indexedCount = docs.filter((d) => d.status === "indexed").length;

  // ── Render ─────────────────────────────────────────────────────────────────

  return (
    <div
      className="flex overflow-hidden"
      style={{
        height: "calc(100vh - 44px)",
        background: "#F7F7F7",
        fontFamily: "Inter, -apple-system, sans-serif",
      }}
    >
      {/* ── Left: Documents ──────────────────────────────────────────── */}
      <div
        className="flex flex-col w-72 flex-shrink-0 border-r overflow-hidden"
        style={{ background: "#FFFFFF", borderColor: "#E5E5EA" }}
      >
        {/* Header */}
        <div className="px-4 py-4 border-b" style={{ borderColor: "#E5E5EA" }}>
          <div className="flex items-center gap-2 mb-0.5">
            <BookOpen size={16} style={{ color: "#5B5EF4" }} />
            <span className="text-sm font-semibold" style={{ color: "#171717" }}>
              Document Center
            </span>
          </div>
          <p className="text-xs" style={{ color: "#8A8A8A" }}>
            {indexedCount} doc{indexedCount !== 1 ? "s" : ""} indexed
          </p>
        </div>

        {/* Upload */}
        <div className="px-3 py-3 border-b" style={{ borderColor: "#E5E5EA" }}>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.txt,.md"
            className="hidden"
            onChange={handleFileSelect}
          />

          {!uploadFile ? (
            <button
              onClick={() => fileInputRef.current?.click()}
              className="w-full rounded-xl border-2 border-dashed py-4 flex flex-col items-center gap-1.5 transition-colors hover:border-indigo-300"
              style={{ borderColor: "#E5E5EA", background: "#F7F7F7" }}
            >
              <Upload size={18} style={{ color: "#8A8A8A" }} />
              <span className="text-xs font-medium" style={{ color: "#525252" }}>
                Upload document
              </span>
              <span className="text-xs" style={{ color: "#8A8A8A" }}>
                PDF, DOCX, TXT, MD
              </span>
            </button>
          ) : (
            <div
              className="rounded-xl p-3"
              style={{ background: "#F7F7F7", border: "1px solid #E5E5EA" }}
            >
              <div className="flex items-center gap-2 mb-2.5">
                <FileText size={13} style={{ color: "#5B5EF4" }} />
                <span
                  className="text-xs font-medium flex-1 truncate"
                  style={{ color: "#171717" }}
                >
                  {uploadFile.name}
                </span>
                <button onClick={() => setUploadFile(null)}>
                  <X size={12} style={{ color: "#8A8A8A" }} />
                </button>
              </div>

              <select
                value={uploadCategory}
                onChange={(e) => setUploadCategory(e.target.value)}
                className="w-full text-xs rounded-lg px-2.5 py-1.5 mb-2"
                style={{
                  border: "1px solid #E5E5EA",
                  background: "#FFFFFF",
                  color: "#171717",
                  outline: "none",
                }}
              >
                {CATEGORY_OPTIONS.map((c) => (
                  <option key={c.value} value={c.value}>
                    {c.label}
                  </option>
                ))}
              </select>

              <button
                onClick={handleUpload}
                disabled={isUploading}
                className="w-full py-2 rounded-lg text-xs font-semibold text-white flex items-center justify-center gap-1.5"
                style={{ background: "#5B5EF4" }}
              >
                {isUploading ? (
                  <Loader2 size={12} className="animate-spin" />
                ) : (
                  <Upload size={12} />
                )}
                {isUploading ? "Uploading…" : "Upload & Index"}
              </button>
            </div>
          )}
        </div>

        {/* Doc list */}
        <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">
          {docs.length === 0 ? (
            <div className="text-center py-8">
              <FileSearch
                size={24}
                className="mx-auto mb-2"
                style={{ color: "#D1D1D6" }}
              />
              <p className="text-xs" style={{ color: "#8A8A8A" }}>
                No documents yet
              </p>
            </div>
          ) : (
            docs.map((doc) => (
              <div
                key={doc.id}
                className="flex items-start gap-2 rounded-lg px-2.5 py-2 group"
                style={{ background: "#F7F7F7" }}
              >
                <FileText
                  size={13}
                  className="mt-0.5 flex-shrink-0"
                  style={{ color: "#5B5EF4" }}
                />
                <div className="flex-1 min-w-0">
                  <p
                    className="text-xs font-medium truncate"
                    style={{ color: "#171717" }}
                  >
                    {doc.name}
                  </p>
                  <div className="flex items-center gap-1 mt-0.5 flex-wrap">
                    <span className="text-xs" style={{ color: "#8A8A8A" }}>
                      {doc.category}
                    </span>
                    {doc.status === "processing" && (
                      <span
                        className="flex items-center gap-0.5 text-xs"
                        style={{ color: "#FF9500" }}
                      >
                        <Loader2 size={9} className="animate-spin" /> indexing
                      </span>
                    )}
                    {doc.status === "indexed" && (
                      <span
                        className="flex items-center gap-0.5 text-xs"
                        style={{ color: "#34C759" }}
                      >
                        <CheckCircle size={9} /> {doc.chunk_count ?? ""} chunks
                      </span>
                    )}
                    {doc.status === "failed" && (
                      <span
                        className="flex items-center gap-0.5 text-xs"
                        style={{ color: "#FF3B30" }}
                      >
                        <AlertCircle size={9} /> failed
                      </span>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => deleteMutation.mutate(doc.id)}
                  className="opacity-0 group-hover:opacity-100 transition-opacity pt-0.5"
                >
                  <Trash2 size={12} style={{ color: "#FF3B30" }} />
                </button>
              </div>
            ))
          )}
        </div>
      </div>

      {/* ── Right: Chat ───────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Chat header */}
        <div
          className="px-5 py-3.5 border-b flex items-center gap-3 flex-shrink-0"
          style={{ background: "#FFFFFF", borderColor: "#E5E5EA" }}
        >
          <div
            className="w-8 h-8 rounded-xl flex items-center justify-center"
            style={{
              background: "linear-gradient(135deg, #5B5EF4, #4A4DD6)",
            }}
          >
            <Sparkles size={15} color="white" />
          </div>
          <div>
            <p className="text-sm font-semibold" style={{ color: "#171717" }}>
              Document Assistant
            </p>
            <p className="text-xs" style={{ color: "#8A8A8A" }}>
              Ask about retirement, loans, insurance — grounded in your documents
            </p>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-5 py-5 space-y-5">
          {messages.length === 0 && (
            <EmptyState onSuggestion={(q) => handleAsk(q)} />
          )}
          {messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              message={msg}
              onNextStep={(q) => handleAsk(q)}
            />
          ))}
          {isAsking && <ThinkingBubble />}
          <div ref={chatEndRef} />
        </div>

        {/* Input */}
        <div
          className="px-5 py-3.5 border-t flex-shrink-0"
          style={{ background: "#FFFFFF", borderColor: "#E5E5EA" }}
        >
          <div className="flex gap-2.5 items-end">
            <div
              className="flex-1 rounded-xl px-3.5 py-2.5"
              style={{ border: "1.5px solid #E5E5EA", background: "#F7F7F7" }}
            >
              <textarea
                rows={1}
                className="w-full resize-none bg-transparent text-sm outline-none"
                style={{ color: "#171717", maxHeight: "100px" }}
                placeholder="Ask about retirement planning, loan terms, insurance coverage…"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleAsk();
                  }
                }}
              />
            </div>
            <button
              onClick={() => handleAsk()}
              disabled={!inputValue.trim() || isAsking}
              className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 disabled:opacity-40"
              style={{ background: "#5B5EF4" }}
            >
              {isAsking ? (
                <Loader2 size={15} color="white" className="animate-spin" />
              ) : (
                <Send size={15} color="white" />
              )}
            </button>
          </div>
          <p className="text-xs mt-1.5 text-center" style={{ color: "#8A8A8A" }}>
            Answers grounded in your documents · Press ↵ to send
          </p>
        </div>
      </div>
    </div>
  );
}

// ── Sub-components ───────────────────────────────────────────────────────────

function EmptyState({ onSuggestion }: { onSuggestion: (q: string) => void }) {
  return (
    <div className="flex flex-col items-center justify-center h-full py-10 text-center">
      <div
        className="w-12 h-12 rounded-2xl flex items-center justify-center mb-4"
        style={{ background: "#5B5EF415" }}
      >
        <MessageSquare size={22} style={{ color: "#5B5EF4" }} />
      </div>
      <h2 className="text-base font-semibold mb-1.5" style={{ color: "#171717" }}>
        Ask your documents anything
      </h2>
      <p
        className="text-sm mb-6 max-w-xs"
        style={{ color: "#525252", lineHeight: 1.6 }}
      >
        Upload financial documents and ask questions. Answers are grounded in
        your files with citations.
      </p>
      <div className="space-y-2 w-full max-w-md">
        {STARTER_QUESTIONS.map((q) => (
          <button
            key={q}
            onClick={() => onSuggestion(q)}
            className="w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-left hover:opacity-80 transition-opacity"
            style={{ background: "#FFFFFF", border: "1px solid #E5E5EA" }}
          >
            <ChevronRight size={13} style={{ color: "#5B5EF4", flexShrink: 0 }} />
            <span className="text-sm" style={{ color: "#525252" }}>
              {q}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

function ThinkingBubble() {
  return (
    <div className="flex gap-2.5">
      <div
        className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0"
        style={{ background: "linear-gradient(135deg, #5B5EF4, #4A4DD6)" }}
      >
        <Sparkles size={13} color="white" />
      </div>
      <div
        className="rounded-2xl px-4 py-3"
        style={{ background: "#FFFFFF", border: "1px solid #E5E5EA" }}
      >
        <div
          className="flex items-center gap-1.5 text-xs"
          style={{ color: "#8A8A8A" }}
        >
          <span>Searching documents</span>
          {[0, 150, 300].map((delay) => (
            <span
              key={delay}
              className="animate-bounce"
              style={{ animationDelay: `${delay}ms` }}
            >
              ·
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

function MessageBubble({
  message,
  onNextStep,
}: {
  message: ChatMessage;
  onNextStep: (q: string) => void;
}) {
  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div
          className="max-w-lg rounded-2xl px-4 py-3"
          style={{ background: "#5B5EF4" }}
        >
          <p className="text-sm leading-relaxed" style={{ color: "white" }}>
            {message.content}
          </p>
        </div>
      </div>
    );
  }

  const domainColor = DOMAIN_COLORS[message.domain || "general"];
  const domainLabel = DOMAIN_LABELS[message.domain || "general"];

  return (
    <div className="flex gap-2.5">
      <div
        className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
        style={{ background: "linear-gradient(135deg, #5B5EF4, #4A4DD6)" }}
      >
        <Sparkles size={13} color="white" />
      </div>

      <div className="flex-1 min-w-0">
        {/* Domain tag */}
        {message.domain && message.domain !== "general" && (
          <div className="mb-1.5">
            <span
              className="inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full"
              style={{
                background: `${domainColor}15`,
                color: domainColor,
              }}
            >
              {domainLabel}
            </span>
          </div>
        )}

        {/* Answer bubble */}
        <div
          className="rounded-2xl px-4 py-3.5"
          style={{ background: "#FFFFFF", border: "1px solid #E5E5EA" }}
        >
          <p
            className="text-sm whitespace-pre-wrap leading-relaxed"
            style={{ color: "#171717" }}
          >
            {message.content}
          </p>

          {/* Sources */}
          {message.sources && message.sources.length > 0 && (
            <div
              className="mt-3 pt-3 border-t flex flex-wrap gap-1.5"
              style={{ borderColor: "#F0F0F0" }}
            >
              {message.sources.map((src, i) => (
                <span
                  key={i}
                  className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full"
                  style={{
                    background: "#F7F7F7",
                    border: "1px solid #E5E5EA",
                    color: "#525252",
                  }}
                >
                  <FileText size={9} />
                  {src.name}
                  <span style={{ color: "#34C759", fontWeight: 600 }}>
                    {Math.round(src.relevance * 100)}%
                  </span>
                </span>
              ))}
            </div>
          )}

          {/* No-context notice */}
          {message.has_context === false && (
            <p
              className="text-xs mt-2 pt-2 border-t"
              style={{ color: "#8A8A8A", borderColor: "#F0F0F0" }}
            >
              ℹ️ No matching documents found — answered from general knowledge
            </p>
          )}
        </div>

        {/* Jarvis next steps */}
        {message.next_steps && message.next_steps.length > 0 && (
          <div className="mt-2.5">
            <p
              className="text-xs font-semibold mb-1.5 ml-0.5"
              style={{ color: "#8A8A8A" }}
            >
              SUGGESTED NEXT STEPS
            </p>
            <div className="space-y-1.5">
              {message.next_steps.map((step, i) => (
                <button
                  key={i}
                  onClick={() => onNextStep(step)}
                  className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-left hover:opacity-80 transition-opacity"
                  style={{ background: "#FFFFFF", border: "1px solid #E5E5EA" }}
                >
                  <ArrowRight
                    size={12}
                    style={{ color: "#5B5EF4", flexShrink: 0 }}
                  />
                  <span className="text-xs" style={{ color: "#525252" }}>
                    {step}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
