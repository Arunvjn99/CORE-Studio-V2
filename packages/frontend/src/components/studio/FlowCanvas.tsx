"use client";
import { useRef, useState, useCallback, useEffect } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils/cn";

export interface FlowNode {
  id: string;
  type: string;       // start | screen | decision | action | end | system
  label: string;
  description?: string;
  row: number;
  col: number;
  lane?: string;
}
export interface FlowEdge {
  from: string;
  to: string;
  label?: string;
}

interface Props {
  nodes: FlowNode[];
  edges: FlowEdge[];
  onSelectNode?: (node: FlowNode) => void;
  selectedNodeId?: string | null;
}

const NODE_W = 150;
const NODE_H = 64;
const GAP_X = 90;
const GAP_Y = 70;

const NODE_STYLES: Record<string, { bg: string; border: string; text: string; shape: string }> = {
  start:    { bg: "bg-emerald-50", border: "border-emerald-300", text: "text-emerald-700", shape: "rounded-full" },
  end:      { bg: "bg-red-50", border: "border-red-300", text: "text-red-700", shape: "rounded-full" },
  screen:   { bg: "bg-white", border: "border-violet-300", text: "text-violet-700", shape: "rounded-xl" },
  decision: { bg: "bg-amber-50", border: "border-amber-300", text: "text-amber-700", shape: "rounded-lg rotate-0" },
  action:   { bg: "bg-blue-50", border: "border-blue-300", text: "text-blue-700", shape: "rounded-lg" },
  system:   { bg: "bg-gray-50", border: "border-gray-300", text: "text-gray-700", shape: "rounded-lg" },
};

export function FlowCanvas({ nodes, edges, onSelectNode, selectedNodeId }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [transform, setTransform] = useState({ x: 60, y: 60, scale: 1 });
  const [panning, setPanning] = useState(false);
  const panStart = useRef({ x: 0, y: 0, tx: 0, ty: 0 });

  // Position nodes
  const positioned = nodes.map(n => ({
    ...n,
    x: (n.col ?? 0) * (NODE_W + GAP_X),
    y: (n.row ?? 0) * (NODE_H + GAP_Y),
  }));
  const nodeById = Object.fromEntries(positioned.map(n => [n.id, n]));

  const onPointerDown = useCallback((e: React.PointerEvent) => {
    if ((e.target as HTMLElement).closest("[data-node]")) return;
    setPanning(true);
    panStart.current = { x: e.clientX, y: e.clientY, tx: transform.x, ty: transform.y };
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
  }, [transform]);
  const onPointerMove = useCallback((e: React.PointerEvent) => {
    if (!panning) return;
    setTransform(t => ({ ...t, x: panStart.current.tx + (e.clientX - panStart.current.x), y: panStart.current.ty + (e.clientY - panStart.current.y) }));
  }, [panning]);
  const onPointerUp = useCallback(() => setPanning(false), []);
  const onWheel = useCallback((e: React.WheelEvent) => {
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault();
      setTransform(t => ({ ...t, scale: Math.min(2, Math.max(0.3, t.scale - e.deltaY * 0.002)) }));
    } else {
      setTransform(t => ({ ...t, x: t.x - e.deltaX, y: t.y - e.deltaY }));
    }
  }, []);

  const fit = useCallback(() => {
    if (!positioned.length || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const maxX = Math.max(...positioned.map(n => n.x + NODE_W));
    const maxY = Math.max(...positioned.map(n => n.y + NODE_H));
    const scale = Math.min((rect.width - 120) / maxX, (rect.height - 120) / maxY, 1.2);
    setTransform({ x: 60, y: 60, scale: Math.max(0.3, scale) });
  }, [positioned]);

  useEffect(() => { if (positioned.length) fit(); /* eslint-disable-next-line */ }, [nodes.length]);

  return (
    <div
      ref={containerRef}
      className={cn("relative w-full h-full overflow-hidden bg-[#fafafa]", panning ? "cursor-grabbing" : "cursor-grab")}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onWheel={onWheel}
      style={{
        backgroundImage: "radial-gradient(circle, #e0e0e0 1px, transparent 1px)",
        backgroundSize: "24px 24px",
        backgroundPosition: `${transform.x}px ${transform.y}px`,
      }}
    >
      <div
        className="absolute top-0 left-0 origin-top-left"
        style={{ transform: `translate(${transform.x}px, ${transform.y}px) scale(${transform.scale})`, transition: panning ? "none" : "transform 0.1s" }}
      >
        {/* Edges (SVG layer) */}
        <svg className="absolute top-0 left-0 overflow-visible pointer-events-none" style={{ width: 1, height: 1 }}>
          <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8" />
            </marker>
          </defs>
          {edges.map((edge, i) => {
            const from = nodeById[edge.from];
            const to = nodeById[edge.to];
            if (!from || !to) return null;
            // Connect from right-center of `from` to left-center of `to` (or vertical if stacked)
            const horizontal = Math.abs(from.col - to.col) >= Math.abs(from.row - to.row);
            let x1, y1, x2, y2;
            if (horizontal) {
              const goingRight = to.x >= from.x;
              x1 = from.x + (goingRight ? NODE_W : 0);
              y1 = from.y + NODE_H / 2;
              x2 = to.x + (goingRight ? 0 : NODE_W);
              y2 = to.y + NODE_H / 2;
            } else {
              const goingDown = to.y >= from.y;
              x1 = from.x + NODE_W / 2;
              y1 = from.y + (goingDown ? NODE_H : 0);
              x2 = to.x + NODE_W / 2;
              y2 = to.y + (goingDown ? 0 : NODE_H);
            }
            const midX = (x1 + x2) / 2;
            const midY = (y1 + y2) / 2;
            const path = horizontal
              ? `M ${x1} ${y1} C ${midX} ${y1}, ${midX} ${y2}, ${x2} ${y2}`
              : `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`;
            return (
              <g key={i}>
                <path d={path} fill="none" stroke="#94a3b8" strokeWidth={1.5} markerEnd="url(#arrow)" />
                {edge.label && (
                  <g>
                    <rect x={midX - edge.label.length * 3.2 - 4} y={midY - 8} width={edge.label.length * 6.4 + 8} height={16} rx={4} fill="white" stroke="#e2e8f0" />
                    <text x={midX} y={midY + 3} textAnchor="middle" fontSize={10} fill="#64748b">{edge.label}</text>
                  </g>
                )}
              </g>
            );
          })}
        </svg>

        {/* Nodes */}
        {positioned.map((node, idx) => {
          const style = NODE_STYLES[node.type] || NODE_STYLES.action;
          const isSelected = selectedNodeId === node.id;
          const isDiamond = node.type === "decision";
          return (
            <motion.div
              key={node.id}
              data-node
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: idx * 0.03 }}
              onClick={() => onSelectNode?.(node)}
              className="absolute cursor-pointer"
              style={{ left: node.x, top: node.y, width: NODE_W, height: NODE_H }}
            >
              <div className={cn(
                "w-full h-full border-2 flex flex-col items-center justify-center px-2 text-center transition-all shadow-sm hover:shadow-md",
                style.bg, style.border,
                isDiamond ? "rounded-lg" : style.shape,
                isSelected && "ring-2 ring-offset-2 ring-violet-400"
              )}>
                <div className={cn("text-[11px] font-semibold leading-tight", style.text)}>{node.label}</div>
                {node.type && (
                  <div className="text-[8px] uppercase tracking-wider text-gray-400 mt-0.5">{node.type}</div>
                )}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Controls */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-1 bg-white rounded-xl border border-gray-200 shadow-lg px-2 py-1.5">
        <button onClick={() => setTransform(t => ({ ...t, scale: Math.max(0.3, t.scale - 0.1) }))} className="w-7 h-7 rounded-lg hover:bg-gray-100 text-gray-600">−</button>
        <span className="text-xs font-mono text-gray-600 w-12 text-center">{Math.round(transform.scale * 100)}%</span>
        <button onClick={() => setTransform(t => ({ ...t, scale: Math.min(2, t.scale + 0.1) }))} className="w-7 h-7 rounded-lg hover:bg-gray-100 text-gray-600">+</button>
        <div className="w-px h-5 bg-gray-200 mx-1" />
        <button onClick={fit} className="px-2 h-7 rounded-lg hover:bg-gray-100 text-gray-600 text-xs">Fit</button>
      </div>

      {/* Legend */}
      <div className="absolute top-4 left-4 bg-white/90 backdrop-blur rounded-lg border border-gray-100 p-2 flex flex-wrap gap-2 max-w-xs">
        {Object.entries(NODE_STYLES).map(([type, s]) => (
          <div key={type} className="flex items-center gap-1">
            <div className={cn("w-2.5 h-2.5 border", s.bg, s.border, type === "start" || type === "end" ? "rounded-full" : "rounded")} />
            <span className="text-[9px] text-gray-500 capitalize">{type}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
