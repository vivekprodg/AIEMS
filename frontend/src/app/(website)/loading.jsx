"use client";

import React from "react";
import { Spin } from "antd";

/**
 * Non-blocking App Router Loading Shell
 * Prevents full-screen DOM locks during Server Component hydration.
 */
export default function Loading() {
  return (
    <div className="min-h-[60vh] w-full flex flex-col items-center justify-center py-20 bg-surface">
      <Spin size="large" />
      <p className="mt-4 text-slate-600 font-medium text-sm">Loading AIEMS Content...</p>
    </div>
  );
}