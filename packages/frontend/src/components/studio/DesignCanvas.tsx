"use client";
import { useRef, useState, useCallback, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Loader2, Maximize2, Code, RefreshCw, Pencil, X, Monitor, Smartphone, Tablet } from "lucide-react";
import { cn } from "@/lib/utils/cn";

export interface ScreenVersionEntry {
  version: number;
  html: string;
  instruction: string | null;
  change_summary: string;
  created_at: string;
}

export interface CanvasScreen {
  screen_id: string;
  name: string;
  purpose?: string;
  html: string;
  version?: number;
  layout_type?: string;
  screen_type?: string;  // mobile | tablet | web_dashboard | website | desktop_app
  canvas_size?: { width: number; height: number };
  model_used?: string;
  refinement_history?: ScreenVersionEntry[];
  x?: number;
  y?: number;
}

// Canonical dimensions per screen_type
const SCREEN_DIMS: Record<string, { width: number; height: number }> = {
  mobile:       { width: 390,  height: 844  },
  tablet:       { width: 768,  height: 1024 },
  web_dashboard:{ width: 1440, height: 900  },
  website:      { width: 1440, height: 900  },
  desktop_app:  { width: 1280, height: 800  },
};

function getScreenDims(s: CanvasScreen, fallback: { width: number; height: number }) {
  if (s.canvas_size?.width && s.canvas_size?.height) return s.canvas_size;
  if (s.screen_type && SCREEN_DIMS[s.screen_type]) return SCREEN_DIMS[s.screen_type];
  return fallback;
}

interface Props {
  screens: CanvasScreen[];
  generatingScreens?: string[];   // names of screens currently being generated
  device: { id: string; width: number; height: number };
  forceDevice?: boolean;  // when true, device picker overrides LLM canvas_size/screen_type
  onSelectScreen?: (screen: CanvasScreen) => void;
  onRegenerateScreen?: (screen: CanvasScreen) => void;
  onViewCode?: (screen: CanvasScreen) => void;
  onEditScreen?: (screen: CanvasScreen) => void;
  selectedScreenId?: string | null;
}

const GAP = 80;

export function DesignCanvas({
  screens, generatingScreens = [], device, forceDevice = false,
  onSelectScreen, onRegenerateScreen, onViewCode, onEditScreen, selectedScreenId,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [transform, setTransform] = useState({ x: 100, y: 80, scale: 0.7 });
  const [isPanning, setIsPanning] = useState(false);
  const panStart = useRef({ x: 0, y: 0, tx: 0, ty: 0 });
  const [expandedScreen, setExpandedScreen] = useState<CanvasScreen | null>(null);

  // Per-screen dimensions — when forceDevice is true the picker overrides LLM screen_type/canvas_size
  const getDims = (s: CanvasScreen) => forceDevice ? device : getScreenDims(s, device);

  // Layout: place screens left-to-right, wrapping at 4. Each row height = tallest in that row.
  const PERROW = 4;
  const positioned = screens.map((s, i) => {
    const col = i % PERROW;
    const row = Math.floor(i / PERROW);
    // Compute x offset = sum of widths of all prior screens in same row + gaps
    const rowStart = row * PERROW;
    let xOffset = 0;
    for (let j = rowStart; j < i; j++) {
      xOffset += getDims(screens[j]).width + GAP;
    }
    // Compute y offset = sum of max-heights of all prior rows + label gap
    let yOffset = 0;
    for (let r = 0; r < row; r++) {
      const rowScreens = screens.slice(r * PERROW, r * PERROW + PERROW);
      const maxH = Math.max(...rowScreens.map(rs => getDims(rs).height));
      yOffset += maxH + GAP + 60; // 60 = label height
    }
    return { ...s, x: xOffset, y: yOffset };
  });

  // ── Pan (space+drag or middle mouse or drag on empty) ──────────────────────
  const onPointerDown = useCallback((e: React.PointerEvent) => {
    // Only pan when clicking the canvas background (not a screen frame)
    if ((e.target as HTMLElement).closest("[data-screen-frame]")) return;
    setIsPanning(true);
    panStart.current = { x: e.clientX, y: e.clientY, tx: transform.x, ty: transform.y };
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
  }, [transform]);

  const onPointerMove = useCallback((e: React.PointerEvent) => {
    if (!isPanning) return;
    const dx = e.clientX - panStart.current.x;
    const dy = e.clientY - panStart.current.y;
    setTransform(t => ({ ...t, x: panStart.current.tx + dx, y: panStart.current.ty + dy }));
  }, [isPanning]);

  const onPointerUp = useCallback(() => setIsPanning(false), []);

  // ── Zoom on wheel (ctrl/cmd) or trackpad pinch ─────────────────────────────
  const onWheel = useCallback((e: React.WheelEvent) => {
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault();
      const delta = -e.deltaY * 0.002;
      setTransform(t => {
        const newScale = Math.min(2, Math.max(0.2, t.scale + delta));
        // Zoom toward cursor
        const rect = containerRef.current?.getBoundingClientRect();
        if (!rect) return { ...t, scale: newScale };
        const cx = e.clientX - rect.left;
        const cy = e.clientY - rect.top;
        const ratio = newScale / t.scale;
        return {
          scale: newScale,
          x: cx - (cx - t.x) * ratio,
          y: cy - (cy - t.y) * ratio,
        };
      });
    } else {
      // Pan with two-finger scroll
      setTransform(t => ({ ...t, x: t.x - e.deltaX, y: t.y - e.deltaY }));
    }
  }, []);

  const fitToScreen = useCallback(() => {
    if (!positioned.length || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const maxX = Math.max(...positioned.map((s, i) => (s.x || 0) + getDims(screens[i]).width));
    const maxY = Math.max(...positioned.map((s, i) => (s.y || 0) + getDims(screens[i]).height + 60));
    const scaleX = (rect.width - 120) / maxX;
    const scaleY = (rect.height - 120) / maxY;
    const scale = Math.min(scaleX, scaleY, 1);
    setTransform({ x: 60, y: 60, scale: Math.max(0.15, scale) });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [positioned]);

  useEffect(() => {
    if (positioned.length > 0) fitToScreen();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [screens.length]);

  return (
    <div
      ref={containerRef}
      className={cn(
        "relative w-full h-full overflow-hidden bg-[#fafafa]",
        isPanning ? "cursor-grabbing" : "cursor-grab"
      )}
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
      {/* Canvas content */}
      <div
        className="absolute top-0 left-0 origin-top-left"
        style={{
          transform: `translate(${transform.x}px, ${transform.y}px) scale(${transform.scale})`,
          transition: isPanning ? "none" : "transform 0.1s ease-out",
        }}
      >
        {positioned.map((screen, idx) => {
          const isSelected = selectedScreenId === screen.screen_id;
          const dims = getDims(screen);
          const typeLabel = screen.screen_type ?? (dims.width >= 1000 ? "web" : dims.width >= 700 ? "tablet" : "mobile");
          const TypeIcon = dims.width >= 1000 ? Monitor : dims.width >= 700 ? Tablet : Smartphone;

          return (
            <div
              key={screen.screen_id}
              data-screen-frame
              className="absolute"
              style={{ left: screen.x, top: screen.y }}
            >
              {/* Frame label */}
              <div className="flex items-center gap-2 mb-2 px-1">
                <span className="w-5 h-5 rounded-full bg-violet-500 text-white text-[11px] font-bold flex items-center justify-center flex-shrink-0">
                  {idx + 1}
                </span>
                <span className="text-sm font-semibold text-gray-800 whitespace-nowrap">{screen.name}</span>
                {screen.version && screen.version > 0 && (
                  <span className="text-[10px] font-bold bg-violet-100 text-violet-700 px-1.5 py-0.5 rounded">
                    V{screen.version}
                  </span>
                )}
                {/* Device type badge */}
                <span className="flex items-center gap-1 text-[10px] text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded">
                  <TypeIcon className="w-2.5 h-2.5" />
                  {dims.width}×{dims.height}
                </span>
                {/* Actions */}
                <div className="flex items-center gap-1 ml-1">
                  <button
                    onClick={(e) => { e.stopPropagation(); setExpandedScreen(screen); }}
                    className="w-6 h-6 rounded-md bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 shadow-sm"
                    title="Expand full screen"
                  ><Maximize2 className="w-3 h-3 text-gray-500" /></button>
                  <button
                    onClick={(e) => { e.stopPropagation(); onViewCode?.(screen); }}
                    className="w-6 h-6 rounded-md bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 shadow-sm"
                    title="View code"
                  ><Code className="w-3 h-3 text-gray-500" /></button>
                  <button
                    onClick={(e) => { e.stopPropagation(); onRegenerateScreen?.(screen); }}
                    className="w-6 h-6 rounded-md bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 shadow-sm"
                    title="Refine screen"
                  ><RefreshCw className="w-3 h-3 text-gray-500" /></button>
                  <button
                    onClick={(e) => { e.stopPropagation(); onEditScreen?.(screen); }}
                    className="w-6 h-6 rounded-md bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 shadow-sm"
                    title="Edit screen (with version history)"
                  ><Pencil className="w-3 h-3 text-gray-500" /></button>
                </div>
              </div>

              {/* Screen frame — fixed canvas size, scrollable inside */}
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                onClick={() => onSelectScreen?.(screen)}
                className={cn(
                  "bg-white rounded-2xl overflow-hidden shadow-lg transition-all cursor-pointer relative",
                  isSelected
                    ? "ring-4 ring-violet-300 shadow-2xl"
                    : "ring-1 ring-gray-200 hover:ring-2 hover:ring-violet-200"
                )}
                style={{ width: dims.width, height: dims.height }}
              >
                <iframe
                  srcDoc={wrapHTML(screen.html, dims)}
                  className="w-full border-0"
                  style={{ height: dims.height, display: "block" }}
                  title={screen.name}
                  sandbox="allow-same-origin allow-scripts"
                  scrolling="yes"
                />
              </motion.div>
            </div>
          );
        })}

        {/* Skeleton frames for screens being generated */}
        {generatingScreens.map((name, idx) => {
          const i = positioned.length + idx;
          const col = i % PERROW;
          const row = Math.floor(i / PERROW);
          const xOff = col * (device.width + GAP);
          const yOff = row * (device.height + GAP + 60);
          return (
            <div
              key={`gen-${idx}`}
              data-screen-frame
              className="absolute"
              style={{ left: xOff, top: yOff }}
            >
              <div className="flex items-center gap-2 mb-2 px-1">
                <span className="w-5 h-5 rounded-full bg-gray-300 text-white text-[11px] font-bold flex items-center justify-center">
                  {i + 1}
                </span>
                <span className="text-sm font-medium text-gray-400">{name}</span>
              </div>
              <div
                className="bg-white rounded-2xl border-2 border-dashed border-violet-200 flex items-center justify-center"
                style={{ width: device.width, height: device.height }}
              >
                <div className="text-center">
                  <Loader2 className="w-7 h-7 text-violet-400 animate-spin mx-auto mb-3" />
                  <p className="text-sm text-gray-500">Generating...</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Canvas controls */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-1 bg-white rounded-xl border border-gray-200 shadow-lg px-2 py-1.5">
        <button onClick={() => setTransform(t => ({ ...t, scale: Math.max(0.2, t.scale - 0.1) }))}
          className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-600 text-sm font-medium">−</button>
        <span className="text-xs font-mono text-gray-600 w-12 text-center">{Math.round(transform.scale * 100)}%</span>
        <button onClick={() => setTransform(t => ({ ...t, scale: Math.min(2, t.scale + 0.1) }))}
          className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-600 text-sm font-medium">+</button>
        <div className="w-px h-5 bg-gray-200 mx-1" />
        <button onClick={fitToScreen}
          className="px-2 h-7 flex items-center gap-1 rounded-lg hover:bg-gray-100 text-gray-600 text-xs">
          <Maximize2 className="w-3 h-3" /> Fit
        </button>
      </div>

      {/* Hint */}
      <div className="absolute top-4 right-4 text-[10px] text-gray-400 bg-white/80 backdrop-blur px-2 py-1 rounded-md border border-gray-100">
        ⌘ + scroll to zoom · drag to pan
      </div>

      {/* Expand modal */}
      <AnimatePresence>
        {expandedScreen && (() => {
          const dims = getDims(expandedScreen);
          return (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-black/60 flex items-center justify-center z-50"
              onClick={() => setExpandedScreen(null)}
            >
              <motion.div
                initial={{ scale: 0.92, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.92, opacity: 0 }}
                transition={{ type: "spring", damping: 24, stiffness: 280 }}
                className="relative bg-white rounded-2xl shadow-2xl overflow-hidden"
                style={{
                  width: Math.min(dims.width, window.innerWidth - 80),
                  height: Math.min(dims.height, window.innerHeight - 80),
                }}
                onClick={(e) => e.stopPropagation()}
              >
                {/* Modal header */}
                <div className="flex items-center justify-between px-4 py-2.5 border-b border-gray-100 bg-gray-50">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-gray-800">{expandedScreen.name}</span>
                    <span className="text-xs text-gray-400">{dims.width}×{dims.height}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => { onViewCode?.(expandedScreen); setExpandedScreen(null); }}
                      className="flex items-center gap-1 px-2 py-1 text-xs text-gray-600 bg-white border border-gray-200 rounded-md hover:bg-gray-50"
                    >
                      <Code className="w-3 h-3" /> Code
                    </button>
                    <button
                      onClick={() => setExpandedScreen(null)}
                      className="w-7 h-7 flex items-center justify-center rounded-md hover:bg-gray-200 text-gray-500"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                {/* Full iframe — scrollable */}
                <iframe
                  srcDoc={wrapHTML(expandedScreen.html, dims)}
                  className="w-full border-0 block"
                  style={{ height: Math.min(dims.height, window.innerHeight - 80) - 44 }}
                  title={expandedScreen.name}
                  sandbox="allow-same-origin allow-scripts"
                  scrolling="yes"
                />
              </motion.div>
            </motion.div>
          );
        })()}
      </AnimatePresence>
    </div>
  );
}

function wrapHTML(html: string, dims?: { width: number; height: number }): string {
  const w = dims?.width ?? 390;

  // For desktop screens (≥ 1000px), don't scale — render at true pixel size
  const viewport = w >= 1000
    ? `width=${w}, initial-scale=1`
    : `width=device-width, initial-scale=1`;

  const inject = `<meta charset="utf-8"/>
  <meta name="viewport" content="${viewport}"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet"/>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: { extend: { fontFamily: { sans: ["Inter","system-ui","sans-serif"] } } }
    }
  </script>
  <style>
    * { box-sizing: border-box; }
    html { height: 100%; }
    body { margin: 0; font-family: "Inter", system-ui, sans-serif; -webkit-font-smoothing: antialiased; min-height: 100%; }
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 4px; }
  </style>`;

  if (html.includes("<html") || html.includes("<!DOCTYPE")) {
    // Full doc — inject missing deps only
    let out = html;
    if (!out.includes("tailwindcss") && !out.includes("tailwind.config")) {
      out = out.replace(/<\/head>/i, `<script src="https://cdn.tailwindcss.com"></script>\n</head>`);
    }
    if (!out.includes("fonts.googleapis.com")) {
      out = out.replace(/<\/head>/i, `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>\n</head>`);
    }
    return out;
  }

  return `<!DOCTYPE html>
<html lang="en">
<head>
  ${inject}
</head>
<body>${html}</body>
</html>`;
}
