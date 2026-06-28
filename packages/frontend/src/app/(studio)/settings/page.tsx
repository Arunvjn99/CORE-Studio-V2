"use client";
import { useAuthStore } from "@/lib/store/auth-store";
import { Settings, User, Key, Bell, Cpu } from "lucide-react";

export default function SettingsPage() {
  const { user } = useAuthStore();

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-semibold text-surface-900 mb-8">Settings</h1>

      <div className="space-y-4">
        {/* Profile */}
        <div className="bg-white border border-surface-200 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-surface-800 flex items-center gap-2 mb-4">
            <User className="w-4 h-4" /> Profile
          </h2>
          <div className="space-y-3">
            {[
              { label: "Full Name", value: user?.full_name },
              { label: "Email", value: user?.email },
              { label: "Username", value: user?.username },
              { label: "Role", value: user?.role },
            ].map(({ label, value }) => (
              <div key={label} className="flex items-center justify-between py-1">
                <span className="text-xs text-surface-500">{label}</span>
                <span className="text-xs font-medium text-surface-800 capitalize">{value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Model Config */}
        <div className="bg-white border border-surface-200 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-surface-800 flex items-center gap-2 mb-4">
            <Cpu className="w-4 h-4" /> Model Configuration
          </h2>
          <div className="space-y-2 text-xs text-surface-600">
            {[
              { tier: "Fast (Complexity 1-3)", model: "Claude Haiku 4.5", use: "Classification, routing, simple transforms" },
              { tier: "Standard (4-7)", model: "Claude Sonnet 4.5", use: "Design generation, UX analysis" },
              { tier: "Advanced (8-10)", model: "Claude Opus 4.5", use: "Complex architecture, deep research" },
            ].map(row => (
              <div key={row.tier} className="flex items-start gap-3 p-3 bg-surface-50 rounded-lg">
                <div className="flex-1">
                  <div className="font-medium text-surface-700 mb-0.5">{row.tier}</div>
                  <div className="text-surface-500">{row.use}</div>
                </div>
                <span className="text-brand-600 font-medium bg-brand-50 px-2 py-0.5 rounded">{row.model}</span>
              </div>
            ))}
            <p className="text-surface-400 mt-2 text-xs">
              The orchestrator automatically selects the optimal model based on task complexity.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
