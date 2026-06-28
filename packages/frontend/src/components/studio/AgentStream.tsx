"use client";
import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle, AlertCircle, Clock, Cpu } from "lucide-react";
import { cn } from "@/lib/utils/cn";

interface WorkflowEvent {
  type: string;
  agent?: string;
  step?: string;
  message?: string;
  data?: any;
  gate_id?: string;
  artifact_id?: string;
}

interface Props {
  events: WorkflowEvent[];
  activeAgent: string | null;
  streamBuffer: Record<string, string>;
  agentConfig: Record<string, { label: string; color: string; textColor: string; bgLight: string; icon: string }>;
}

const EVENT_ICONS: Record<string, React.ReactNode> = {
  step_start: <Clock className="w-3 h-3" />,
  step_complete: <CheckCircle className="w-3 h-3 text-emerald-500" />,
  agent_start: <Cpu className="w-3 h-3" />,
  approval_required: <AlertCircle className="w-3 h-3 text-amber-500" />,
  workflow_complete: <CheckCircle className="w-3 h-3 text-emerald-500" />,
};

export function AgentStream({ events, activeAgent, streamBuffer, agentConfig }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [events]);

  const displayEvents = events.filter(e =>
    !["stream_token", "pong"].includes(e.type)
  );

  return (
    <div className="flex flex-col h-full">
      {/* Active agent indicator */}
      <AnimatePresence>
        {activeAgent && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="border-b border-surface-100"
          >
            <div className={cn(
              "mx-4 my-3 p-3 rounded-lg",
              agentConfig[activeAgent]?.bgLight || "bg-surface-50"
            )}>
              <div className="flex items-center gap-2 mb-1">
                <div className={cn(
                  "w-1.5 h-1.5 rounded-full animate-pulse",
                  agentConfig[activeAgent]?.color || "bg-brand-500"
                )} />
                <span className={cn(
                  "text-xs font-semibold",
                  agentConfig[activeAgent]?.textColor || "text-surface-700"
                )}>
                  {agentConfig[activeAgent]?.icon} {agentConfig[activeAgent]?.label} is thinking...
                </span>
              </div>

              {/* Token stream preview */}
              {streamBuffer[activeAgent] && (
                <p className="text-xs text-surface-600 font-mono leading-relaxed line-clamp-3 mt-1">
                  {streamBuffer[activeAgent].slice(-200)}
                  <span className="inline-block w-1 h-3 bg-brand-500 ml-0.5 animate-pulse" />
                </p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Events log */}
      <div className="flex-1 overflow-auto px-4 py-3 space-y-2">
        {displayEvents.length === 0 && (
          <div className="text-center py-8">
            <div className="w-5 h-5 border-2 border-brand-200 border-t-brand-500 rounded-full
                            animate-spin mx-auto mb-2" />
            <p className="text-xs text-surface-400">Starting pipeline...</p>
          </div>
        )}

        <AnimatePresence initial={false}>
          {displayEvents.map((event, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-start gap-2.5"
            >
              <div className="w-5 h-5 flex items-center justify-center mt-0.5 flex-shrink-0 text-surface-400">
                {EVENT_ICONS[event.type] || <div className="w-1 h-1 rounded-full bg-surface-300 mt-1.5" />}
              </div>
              <div className="flex-1 min-w-0">
                <p className={cn(
                  "text-xs leading-relaxed",
                  event.type === "approval_required" ? "text-amber-700 font-medium" :
                  event.type === "workflow_complete" ? "text-emerald-700 font-medium" :
                  "text-surface-600"
                )}>
                  {event.message}
                </p>
                {event.data?.complexity && (
                  <span className="text-2xs text-surface-400 mt-0.5 block">
                    Complexity: {event.data.complexity}/10
                  </span>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        <div ref={bottomRef} />
      </div>
    </div>
  );
}
