"use client";
import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Paintbrush, BarChart3, CheckSquare, Code2,
  BookOpen, Settings, FolderOpen, ChevronRight,
  LogOut, Cpu, Zap, GitBranch, FileSearch
} from "lucide-react";
import { useAuthStore } from "@/lib/store/auth-store";
import { cn } from "@/lib/utils/cn";

const DEPARTMENTS = [
  {
    id: "design",
    href: "/studio",
    icon: Paintbrush,
    label: "Design",
    color: "text-violet-600",
    bg: "bg-violet-50",
    border: "border-violet-200",
    dot: "bg-violet-500",
    description: "UX, UI, Review",
  },
  {
    id: "analyst",
    href: "/analyst",
    icon: BarChart3,
    label: "Analyst",
    color: "text-blue-600",
    bg: "bg-blue-50",
    border: "border-blue-200",
    dot: "bg-blue-500",
    description: "Research, PRD, Stories",
  },
  // QA and Engineering are temporarily hidden for the demo (design/BA flow only).
  // Routes and pages still exist — re-add these entries to restore nav access.
  // {
  //   id: "qa",
  //   href: "/qa",
  //   icon: CheckSquare,
  //   label: "QA",
  //   color: "text-emerald-600",
  //   bg: "bg-emerald-50",
  //   border: "border-emerald-200",
  //   dot: "bg-emerald-500",
  //   description: "Tests, Accessibility",
  // },
  // {
  //   id: "engineering",
  //   href: "/engineering",
  //   icon: Code2,
  //   label: "Engineering",
  //   color: "text-amber-600",
  //   bg: "bg-amber-50",
  //   border: "border-amber-200",
  //   dot: "bg-amber-500",
  //   description: "Code, API, Architecture",
  // },
];

const NAV_BOTTOM = [
  { href: "/projects", icon: FolderOpen, label: "Projects" },
  { href: "/documents", icon: FileSearch, label: "Documents" },
  { href: "/settings", icon: Settings, label: "Settings" },
];

export default function StudioLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { user, accessToken, _hasHydrated, clearAuth } = useAuthStore();

  useEffect(() => {
    if (_hasHydrated && !accessToken) router.push("/login");
  }, [_hasHydrated, accessToken, router]);

  if (!_hasHydrated) return null;
  if (!user) return null;

  const activeDept = DEPARTMENTS.find(d => pathname.startsWith(d.href));

  return (
    <div className="flex h-screen bg-[#f8f8f8] overflow-hidden">
      {/* Sidebar */}
      <aside className="w-52 bg-white border-r border-gray-100 flex flex-col flex-shrink-0">
        {/* Logo */}
        <div className="px-4 py-4 border-b border-gray-100">
          <div className="flex items-center gap-2.5">
            <img src="/core-logo.png" alt="CORE" className="h-6 w-auto" />
            <div className="flex flex-col">
              <span className="text-[11px] font-semibold text-gray-700 leading-tight">Studio</span>
              <div className="text-[9px] text-gray-400 flex items-center gap-1">
                <span className="w-1 h-1 rounded-full bg-emerald-400 inline-block" />
                AI Office
              </div>
            </div>
          </div>
        </div>

        {/* Departments */}
        <nav className="flex-1 px-2 py-3 space-y-0.5 overflow-auto">
          <p className="px-2 text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-2">
            Departments
          </p>

          {DEPARTMENTS.map(dept => {
            const Icon = dept.icon;
            const isActive = pathname.startsWith(dept.href);
            return (
              <Link key={dept.id} href={dept.href}>
                <div className={cn(
                  "flex items-center gap-2.5 px-2.5 py-2 rounded-lg cursor-pointer transition-all duration-100",
                  isActive
                    ? `${dept.bg} border ${dept.border}`
                    : "hover:bg-gray-50"
                )}>
                  <div className={cn(
                    "w-6 h-6 rounded-md flex items-center justify-center flex-shrink-0",
                    isActive ? dept.bg : "bg-gray-100"
                  )}>
                    <Icon className={cn("w-3.5 h-3.5", isActive ? dept.color : "text-gray-500")} />
                  </div>
                  <div className="min-w-0">
                    <div className={cn("text-xs font-medium truncate", isActive ? dept.color : "text-gray-700")}>
                      {dept.label}
                    </div>
                    <div className="text-[10px] text-gray-400 truncate">{dept.description}</div>
                  </div>
                </div>
              </Link>
            );
          })}

          <div className="pt-4 pb-1">
            <p className="px-2 text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-2">
              Workspace
            </p>
          </div>

          {NAV_BOTTOM.map(({ href, icon: Icon, label }) => {
            const isActive = pathname === href || pathname.startsWith(href + "/");
            return (
              <Link key={href} href={href}>
                <div className={cn(
                  "flex items-center gap-2 px-2.5 py-2 rounded-lg text-xs font-medium transition-all cursor-pointer",
                  isActive
                    ? "bg-gray-100 text-gray-900"
                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-800"
                )}>
                  <Icon className="w-3.5 h-3.5 flex-shrink-0" />
                  {label}
                </div>
              </Link>
            );
          })}
        </nav>

        {/* AI Status */}
        <div className="mx-2 mb-2 px-2.5 py-2 rounded-lg bg-gray-50 border border-gray-100">
          <div className="flex items-center gap-1.5">
            <Cpu className="w-3 h-3 text-indigo-500" />
            <span className="text-[10px] font-medium text-gray-600">Local AI</span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 ml-auto" />
          </div>
          <div className="text-[9px] text-gray-400 mt-0.5">deepseek-r1 · qwen-coder · llava</div>
        </div>

        {/* User */}
        <div className="p-2 border-t border-gray-100">
          <div className="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-gray-50 cursor-pointer group">
            <div className="w-6 h-6 rounded-full bg-gradient-to-br from-indigo-400 to-indigo-600 flex items-center justify-center flex-shrink-0">
              <span className="text-white text-[10px] font-semibold">
                {user.full_name?.charAt(0)?.toUpperCase()}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-[11px] font-medium text-gray-800 truncate">{user.full_name}</div>
              <div className="text-[9px] text-gray-400 capitalize">{user.role}</div>
            </div>
            <button
              onClick={() => { clearAuth(); router.push("/login"); }}
              className="opacity-0 group-hover:opacity-100 transition-opacity"
              title="Sign out"
            >
              <LogOut className="w-3 h-3 text-gray-400 hover:text-red-500" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 overflow-auto min-w-0">
        {/* Department header bar */}
        {activeDept && (
          <div className="bg-white border-b border-gray-100 px-6 py-3 flex items-center gap-2">
            <div className={cn("w-5 h-5 rounded-md flex items-center justify-center", activeDept.bg)}>
              <activeDept.icon className={cn("w-3 h-3", activeDept.color)} />
            </div>
            <span className="text-sm font-semibold text-gray-800">{activeDept.label} Team</span>
            <span className="text-xs text-gray-400 ml-1">— {activeDept.description}</span>
          </div>
        )}
        {children}
      </main>
    </div>
  );
}
