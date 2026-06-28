"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion } from "framer-motion";
import { toast } from "sonner";
import { Eye, EyeOff, ArrowRight } from "lucide-react";
import { useAuthStore } from "@/lib/store/auth-store";
import { api } from "@/lib/api/client";

const schema = z.object({
  full_name: z.string().min(2, "Name required"),
  username: z.string().min(3, "Username must be at least 3 chars").regex(/^[a-z0-9_]+$/, "Lowercase, numbers, _ only"),
  email: z.string().email("Valid email required"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});
type FormData = z.infer<typeof schema>;

export default function RegisterPage() {
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
      const res = await api.post("/auth/register", data);
      setAuth(res.data.user, res.data.access_token, res.data.refresh_token);
      toast.success("Welcome to CORE Studio!");
      router.push("/projects");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center p-8">
      <motion.div
        className="w-full max-w-sm"
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center gap-2 mb-10">
          <img src="/core-logo.png" alt="CORE" className="h-6 w-auto" />
          <span className="font-semibold text-surface-900">Studio</span>
        </div>

        <div className="mb-8">
          <h2 className="text-2xl font-semibold text-surface-900">Create account</h2>
          <p className="text-surface-500 text-sm mt-1">
            Already have one?{" "}
            <Link href="/login" className="text-brand-600 hover:text-brand-700 font-medium">Sign in</Link>
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-3.5">
          {[
            { field: "full_name", label: "Full Name", placeholder: "Jane Smith", type: "text" },
            { field: "username", label: "Username", placeholder: "jane_smith", type: "text" },
            { field: "email", label: "Email", placeholder: "jane@company.com", type: "email" },
          ].map(({ field, label, placeholder, type }) => (
            <div key={field}>
              <label className="block text-xs font-medium text-surface-700 mb-1.5">{label}</label>
              <input
                {...register(field as keyof FormData)}
                type={type}
                placeholder={placeholder}
                className="w-full h-10 px-3 text-sm rounded-lg border border-surface-200 bg-white
                           focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100
                           placeholder:text-surface-300 transition-all"
              />
              {errors[field as keyof FormData] && (
                <p className="text-red-500 text-xs mt-1">{errors[field as keyof FormData]?.message}</p>
              )}
            </div>
          ))}

          <div>
            <label className="block text-xs font-medium text-surface-700 mb-1.5">Password</label>
            <div className="relative">
              <input
                {...register("password")}
                type={showPass ? "text" : "password"}
                placeholder="8+ characters"
                className="w-full h-10 px-3 pr-10 text-sm rounded-lg border border-surface-200 bg-white
                           focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100
                           placeholder:text-surface-300 transition-all"
              />
              <button type="button" onClick={() => setShowPass(!showPass)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-surface-400">
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
                       disabled:opacity-50 disabled:cursor-not-allowed mt-1"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>Create account <ArrowRight className="w-4 h-4" /></>
            )}
          </button>
        </form>
      </motion.div>
    </div>
  );
}
