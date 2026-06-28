"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle, XCircle, MessageSquare, ChevronUp, ThumbsUp, ThumbsDown, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils/cn";

interface Props {
  gateId: string;
  step: string;
  artifactId: string;
  onApprove: (comment: string) => void;
  onReject: (comment: string) => void;
  onRequestChanges: (comment: string) => void;
  isLoading: boolean;
}

const STEP_NAMES: Record<string, string> = {
  planner: "Requirement Blueprint",
  ux: "UX Blueprint",
  ui: "UI Design",
  review: "Review Report",
};

const STEP_NEXT: Record<string, string> = {
  planner: "UX Agent will design user flows",
  ux: "UI Agent will design visual screens",
  ui: "Review Agent will validate quality",
  review: "Design workflow complete",
};

export function ApprovalGate({
  step, artifactId, onApprove, onReject, onRequestChanges, isLoading
}: Props) {
  const [comment, setComment] = useState("");
  const [showComment, setShowComment] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 16 }}
      className="border-t border-surface-200 bg-white"
    >
      <div className="px-6 py-4">
        <div className="flex items-start justify-between mb-3">
          <div>
            <div className="flex items-center gap-2 mb-0.5">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              <span className="text-sm font-semibold text-surface-900">Review Required</span>
            </div>
            <p className="text-xs text-surface-500">
              {STEP_NAMES[step] || step} is ready. Review and approve to continue.
            </p>
            {STEP_NEXT[step] && (
              <p className="text-xs text-brand-600 mt-0.5">
                → {STEP_NEXT[step]}
              </p>
            )}
          </div>
        </div>

        {/* Comment toggle */}
        {showComment && (
          <div className="mb-3">
            <textarea
              value={comment}
              onChange={e => setComment(e.target.value)}
              placeholder="Add feedback or change requests..."
              className="w-full h-20 px-3 py-2 text-xs rounded-lg border border-surface-200
                         focus:outline-none focus:border-brand-400 resize-none"
            />
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => onApprove(comment)}
            disabled={isLoading}
            className="flex items-center gap-1.5 h-8 px-4 bg-emerald-500 hover:bg-emerald-600
                       text-white text-xs font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            <ThumbsUp className="w-3.5 h-3.5" />
            Approve
          </button>

          <button
            onClick={() => onRequestChanges(comment)}
            disabled={isLoading}
            className="flex items-center gap-1.5 h-8 px-3 bg-amber-50 hover:bg-amber-100
                       text-amber-700 text-xs font-medium rounded-lg border border-amber-200 transition-colors disabled:opacity-50"
          >
            <MessageSquare className="w-3.5 h-3.5" />
            Request Changes
          </button>

          <button
            onClick={() => onReject(comment)}
            disabled={isLoading}
            className="flex items-center gap-1.5 h-8 px-3 bg-red-50 hover:bg-red-100
                       text-red-600 text-xs font-medium rounded-lg border border-red-200 transition-colors disabled:opacity-50"
          >
            <ThumbsDown className="w-3.5 h-3.5" />
            Reject
          </button>

          <button
            onClick={() => setShowComment(!showComment)}
            className="ml-auto flex items-center gap-1 h-8 px-3 text-xs text-surface-500
                       hover:text-surface-700 rounded-lg hover:bg-surface-50 transition-colors"
          >
            <MessageSquare className="w-3.5 h-3.5" />
            {showComment ? "Hide" : "Add note"}
          </button>
        </div>
      </div>
    </motion.div>
  );
}
