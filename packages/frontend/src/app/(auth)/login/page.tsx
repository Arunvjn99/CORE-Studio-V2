"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion } from "framer-motion";
import { toast } from "sonner";
import { Eye, EyeOff, ArrowRight, Sparkles } from "lucide-react";
import { useAuthStore } from "@/lib/store/auth-store";
import { api } from "@/lib/api/client";

const schema = z.object({
  email: z.string().email("Valid email required"),
  password: z.string().min(6, "Password required"),
});
type FormData = z.infer<typeof schema>;

export default function LoginPage() {
  const router = useRouter();
  const { setAuth } = useAuthStore();
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    setLoading(true);
    try {
      const res = await api.post("/auth/login", data);
      setAuth(res.data.user, res.data.access_token, res.data.refresh_token);
      toast.success(`Welcome back, ${res.data.user.full_name}`);
      router.push("/projects");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex">
      {/* Left — branding panel */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-surface-950 via-surface-900 to-[#1a1b3e] p-12 flex-col justify-between">
        <div className="flex items-center gap-3">
          <img src="/core-logo.png" alt="CORE" className="h-6 w-auto" />
          <span className="text-white font-semibold text-lg">Studio</span>
        </div>

        <div className="space-y-6">
          <div className="inline-flex items-center gap-2 bg-white/10 text-white/70 text-xs px-3 py-1.5 rounded-full border border-white/10">
            <Sparkles className="w-3 h-3" />
            AI-Powered Design Office
          </div>
          <h1 className="text-4xl font-semibold text-white leading-tight">
            Where requirements
            <br />
            <span className="text-brand-400">become designs.</span>
          </h1>
          <p className="text-surface-400 text-base leading-relaxed max-w-sm">
            A virtual product office powered by AI agents — Planner, UX, UI, and Review
            working together on your design challenges.
          </p>

          {/* Feature chips */}
          <div className="flex flex-wrap gap-2 pt-2">
            {["Prompt Pipeline", "Smart Model Router", "Human Approvals", "Self-Learning"].map((f) => (
              <span key={f} className="text-xs text-white/50 border border-white/10 px-3 py-1 rounded-full">
                {f}
              </span>
            ))}
          </div>
        </div>

        <p className="text-surface-600 text-xs">CORE Studio v2.0 — Design Team</p>
      </div>

      {/* Right — auth form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <motion.div
          className="w-full max-w-sm"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {/* Mobile logo */}
          <div className="flex items-center gap-2 mb-10 lg:hidden">
            <img src="/core-logo.png" alt="CORE" className="h-6 w-auto" />
            <span className="font-semibold text-surface-900">Studio</span>
          </div>

          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-surface-900">Sign in</h2>
            <p className="text-surface-500 text-sm mt-1">
              New here?{" "}
              <Link href="/register" className="text-brand-600 hover:text-brand-700 font-medium">
                Create an account
              </Link>
            </p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-surface-700 mb-1.5">Email</label>
              <input
                {...register("email")}
                type="email"
                placeholder="you@company.com"
                className="w-full h-10 px-3 text-sm rounded-lg border border-surface-200 bg-white
                           focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100
                           placeholder:text-surface-300 transition-all"
              />
              {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email.message}</p>}
            </div>

            <div>
              <label className="block text-xs font-medium text-surface-700 mb-1.5">Password</label>
              <div className="relative">
                <input
                  {...register("password")}
                  type={showPass ? "text" : "password"}
                  placeholder="••••••••"
                  className="w-full h-10 px-3 pr-10 text-sm rounded-lg border border-surface-200 bg-white
                             focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100
                             placeholder:text-surface-300 transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowPass(!showPass)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-surface-400 hover:text-surface-600"
                >
                  {showPass ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full h-10 bg-brand-500 hover:bg-brand-600 text-white text-sm font-medium
                         rounded-lg flex items-center justify-center gap-2 transition-colors
                         disabled:opacity-50 disabled:cursor-not-allowed mt-2"
            >
              {loading ? (
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>Sign in <ArrowRight className="w-4 h-4" /></>
              )}
            </button>
          </form>
        </motion.div>
      </div>
    </div>
  );
}
