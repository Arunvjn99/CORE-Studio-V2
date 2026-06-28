"use client";
import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Check, CheckCircle2, Loader2, Sparkles, Brain, Eye,
  BookOpen, GripVertical, X, ChevronDown
} from "lucide-react";
import { cn } from "@/lib/utils/cn";

export interface PlannedScreen {
  id: string;
  name: string;
  purpose: string;
}

export interface AgentStep {
  type: string;
  step?: string;
  message?: string;
  thought_process?: string;
  analyze_request?: string;
  planned_screens?: PlannedScreen[];
  screen_name?: string;
}

interface Props {
  steps: AgentStep[];
  phase: "idle" | "planning" | "planned" | "generating" | "complete";
  plannedScreens: PlannedScreen[];
  onApprove: (selectedIds: string[]) => void;
  onReject: () => void;
  isGenerating: boolean;
}

const STEP_ICON: Record<string, any> = {
  vision: Eye,
  vision_done: Eye,
  rag: BookOpen,
  rag_done: BookOpen,
  thinking: Brain,
  thought: Brain,
};

export function AgentPanel({ steps, phase, plannedScreens, onApprove, onReject, isGenerating }: Props) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [orderedScreens, setOrderedScreens] = useState<PlannedScreen[]>([]);
  const [dragIdx, setDragIdx] = useState<number | null>(null);

  // Initialize selection when plan arrives
  useEffect(() => {
    if (plannedScreens.length > 0) {
      setSelected(new Set(plannedScreens.map(s => s.id)));
      setOrderedScreens(plannedScreens);
    }
  }, [plannedScreens]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [steps, plannedScreens]);

  const toggle = (id: string) => {
    setSelected(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const thoughtStep = steps.find(s => s.type === "thought");
  const analyzeText = thoughtStep?.analyze_request;
  const thoughtText = thoughtStep?.thought_process;

  // Drag to reorder
  const onDragStart = (idx: number) => setDragIdx(idx);
  const onDragOver = (e: React.DragEvent, idx: number) => {
    e.preventDefault();
    if (dragIdx === null || dragIdx === idx) return;
    setOrderedScreens(prev => {
      const next = [...prev];
      const [moved] = next.splice(dragIdx, 1);
      next.splice(idx, 0, moved);
      return next;
    });
    setDragIdx(idx);
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-gray-100">
        <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-violet-500 to-violet-700 flex items-center justify-center">
          <Sparkles className="w-3.5 h-3.5 text-white" />
        </div>
        <div>
          <div className="text-sm font-semibold text-gray-800">Design Agent</div>
          <div className="text-[10px] text-gray-400">
            {phase === "planning" && "Analyzing your request..."}
            {phase === "planned" && "Review the plan below"}
            {phase === "generating" && "Generating screens..."}
            {phase === "complete" && "Flow complete"}
            {phase === "idle" && "Ready"}
          </div>
        </div>
        {(phase === "planning" || phase === "generating") && (
          <Loader2 className="w-4 h-4 text-violet-500 animate-spin ml-auto" />
        )}
      </div>

      {/* Activity feed */}
      <div ref={scrollRef} className="flex-1 overflow-auto px-4 py-3 space-y-3">
        {/* Analyze Request */}
        {analyzeText && (
          <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }}>
            <div className="flex items-center gap-1.5 mb-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
              <span className="text-xs font-semibold text-gray-700">Analyze Request</span>
            </div>
            <p className="text-[11px] text-gray-600 leading-relaxed pl-5">{analyzeText}</p>
          </motion.div>
        )}

        {/* Thought process */}
        {thoughtText && (
          <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }}>
            <div className="flex items-center gap-1.5 mb-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
              <span className="text-xs font-semibold text-gray-700">Thought Process</span>
            </div>
            <p className="text-[11px] text-gray-600 leading-relaxed pl-5">{thoughtText}</p>
          </motion.div>
        )}

        {/* Step log */}
        <div className="space-y-1.5">
          <AnimatePresence initial={false}>
            {steps
              .filter(s => !["thought", "plan_ready", "complete", "pong", "started"].includes(s.type) && s.message)
              .slice(-12)
              .map((step, i) => {
                const Icon = STEP_ICON[step.step as string] || null;
                const isDone = step.type?.includes("done") || step.type === "screen_complete";
                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -4 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="flex items-start gap-2"
                  >
                    {isDone ? (
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 mt-0.5 flex-shrink-0" />
                    ) : Icon ? (
                      <Icon className="w-3.5 h-3.5 text-violet-400 mt-0.5 flex-shrink-0" />
                    ) : (
                      <div className="w-3.5 h-3.5 flex items-center justify-center mt-0.5">
                        <div className="w-1 h-1 rounded-full bg-gray-300" />
                      </div>
                    )}
                    <span className="text-[11px] text-gray-600 leading-relaxed">{step.message}</span>
                  </motion.div>
                );
              })}
          </AnimatePresence>

          {phase === "planning" && (
            <div className="flex items-center gap-2 text-[11px] text-violet-500 pl-0.5">
              <Loader2 className="w-3 h-3 animate-spin" />
              Planning screens...
            </div>
          )}
        </div>

        {/* Reviewed Screens approval card */}
        {phase === "planned" && orderedScreens.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl border border-violet-200 bg-violet-50/40 overflow-hidden"
          >
            <div className="px-3 py-2.5 border-b border-violet-100">
              <div className="text-xs font-semibold text-gray-800">Reviewed Screens</div>
              <div className="text-[10px] text-gray-500">Select, reorder, or deselect before approval</div>
            </div>
            <div className="p-2 space-y-1">
              {orderedScreens.map((screen, idx) => (
                <div
                  key={`${screen.id}-${idx}`}
                  draggable
                  onDragStart={() => onDragStart(idx)}
                  onDragOver={(e) => onDragOver(e, idx)}
                  onDragEnd={() => setDragIdx(null)}
                  className={cn(
                    "flex items-center gap-2 px-2 py-2 rounded-lg bg-white border transition-all cursor-move",
                    selected.has(screen.id) ? "border-violet-200" : "border-gray-100 opacity-50"
                  )}
                >
                  <GripVertical className="w-3.5 h-3.5 text-gray-300 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-[11px] font-medium text-gray-800 truncate">{screen.name}</div>
                    <div className="text-[10px] text-gray-500 truncate">{screen.purpose}</div>
                  </div>
                  <button
                    onClick={() => toggle(screen.id)}
                    className={cn(
                      "w-4 h-4 rounded flex items-center justify-center flex-shrink-0 transition-all",
                      selected.has(screen.id)
                        ? "bg-violet-500 text-white"
                        : "border border-gray-300 bg-white"
                    )}
                  >
                    {selected.has(screen.id) && <Check className="w-3 h-3" />}
                  </button>
                </div>
              ))}
            </div>
            <div className="flex items-center gap-2 p-2 border-t border-violet-100">
              <button
                onClick={onReject}
                className="flex-1 h-8 text-xs font-medium text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Reject
              </button>
              <button
                onClick={() => onApprove(orderedScreens.filter(s => selected.has(s.id)).map(s => s.id))}
                disabled={selected.size === 0}
                className="flex-1 h-8 text-xs font-medium text-white bg-gradient-to-br from-violet-500 to-violet-700 rounded-lg hover:from-violet-600 hover:to-violet-800 transition-all flex items-center justify-center gap-1.5 disabled:opacity-40"
              >
                <Check className="w-3.5 h-3.5" />
                Approve & Generate ({selected.size})
              </button>
            </div>
          </motion.div>
        )}

        {/* Generating screens progress */}
        {phase === "generating" && (
          <div className="space-y-1.5">
            {steps.filter(s => s.type === "screen_complete").map((s, i) => (
              <div key={i} className="flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                <span className="text-[11px] text-gray-600">{s.message}</span>
              </div>
            ))}
            <div className="flex items-center gap-2 text-[11px] text-violet-500">
              <Loader2 className="w-3 h-3 animate-spin" />
              Rendering screens...
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
