import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "secondary" | "outline" | "destructive" | "success";
}

const variantStyles: Record<string, string> = {
  default:     "bg-blue-100 text-blue-800",
  secondary:   "bg-gray-100 text-gray-700",
  outline:     "border border-gray-200 text-gray-700",
  destructive: "bg-red-100 text-red-700",
  success:     "bg-green-100 text-green-700",
};

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        variantStyles[variant] || variantStyles.default,
        className,
      )}
      {...props}
    />
  );
}

export { Badge };
