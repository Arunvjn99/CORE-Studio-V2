"use client";
import * as React from "react";
import { cn } from "@/lib/utils";

interface TabsContextType { value: string; onChange: (v: string) => void; }
const TabsContext = React.createContext<TabsContextType>({ value: "", onChange: () => {} });

function Tabs({ value, onValueChange, defaultValue, children, className, ...props }: { value?: string; onValueChange?: (v: string) => void; defaultValue?: string; children: React.ReactNode; className?: string; }) {
  const [internal, setInternal] = React.useState(defaultValue || "");
  const current = value ?? internal;
  const onChange = onValueChange ?? setInternal;
  return <TabsContext.Provider value={{ value: current, onChange }}><div className={cn("", className)} {...props}>{children}</div></TabsContext.Provider>;
}

function TabsList({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("inline-flex items-center rounded-md bg-gray-100 p-1", className)} {...props}>{children}</div>;
}

function TabsTrigger({ value, className, children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement> & { value: string }) {
  const ctx = React.useContext(TabsContext);
  return (
    <button
      onClick={() => ctx.onChange(value)}
      className={cn("px-3 py-1.5 text-sm font-medium rounded-md transition-all", ctx.value === value ? "bg-white shadow-sm" : "text-gray-500 hover:text-gray-700", className)}
      {...props}
    >{children}</button>
  );
}

function TabsContent({ value, className, children, ...props }: React.HTMLAttributes<HTMLDivElement> & { value: string }) {
  const ctx = React.useContext(TabsContext);
  if (ctx.value !== value) return null;
  return <div className={cn("mt-2", className)} {...props}>{children}</div>;
}

export { Tabs, TabsList, TabsTrigger, TabsContent };
