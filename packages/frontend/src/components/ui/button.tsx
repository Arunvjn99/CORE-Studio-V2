import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "secondary" | "outline" | "ghost" | "destructive" | "link";
  size?: "default" | "sm" | "lg" | "icon";
}

const variantStyles: Record<string, string> = {
  default:     "bg-[var(--primary)] text-white hover:opacity-90",
  secondary:   "bg-gray-100 text-gray-900 hover:bg-gray-200",
  outline:     "border border-gray-200 bg-white hover:bg-gray-50",
  ghost:       "hover:bg-gray-100",
  destructive: "bg-red-500 text-white hover:bg-red-600",
  link:        "text-blue-600 underline-offset-4 hover:underline",
};

const sizeStyles: Record<string, string> = {
  default: "h-9 px-4 py-2 text-sm",
  sm:      "h-8 px-3 text-xs",
  lg:      "h-10 px-6",
  icon:    "h-9 w-9",
};

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "inline-flex items-center justify-center rounded-md font-medium transition-colors",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-1",
        "disabled:pointer-events-none disabled:opacity-50 cursor-pointer",
        variantStyles[variant] || variantStyles.default,
        sizeStyles[size] || sizeStyles.default,
        className,
      )}
      {...props}
    />
  )
);
Button.displayName = "Button";
export { Button };
