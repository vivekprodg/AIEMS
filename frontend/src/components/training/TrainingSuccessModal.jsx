"use client";

import React from "react";
import { FaCircleCheck, FaCircleInfo, FaPhone } from "react-icons/fa6";

export default function TrainingSuccessModal({ leadData = {}, onReset }) {
  if (!leadData || !leadData.ref_id) return null;

  const modules = Array.isArray(leadData.selected_modules)
    ? leadData.selected_modules
    : [];

  return (
    <div className="py-8 text-center space-y-6">
      <div className="w-16 h-16 bg-emerald-100 text-primary rounded-full flex items-center justify-center text-3xl mx-auto shadow-md animate-bounce">
        <FaCircleCheck />
      </div>

      <div className="space-y-2">
        <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3 py-1 bg-primary/10 rounded-full inline-block">
          Registration Confirmed
        </span>
        <h2 className="font-display font-extrabold text-2xl sm:text-3xl text-secondary">
          Congratulations, <span className="text-primary">{leadData.full_name || "Student"}</span>!
        </h2>
        <p className="text-slate-600 text-xs sm:text-sm max-w-lg mx-auto">
          Your seat inquiry for the <strong>AIEMS TechBridge: Practical IT Training Program</strong> has been recorded successfully.
        </p>
      </div>

      {/* Generated Lead Slip */}
      <div className="max-w-md mx-auto bg-surface border border-slate-200 rounded-2xl p-5 text-left space-y-2.5 text-xs shadow-sm">
        <div className="flex justify-between border-b border-slate-200 pb-2">
          <span className="text-slate-500 font-medium">Application Ref ID:</span>
          <strong className="text-secondary font-mono font-bold text-sm">{leadData.ref_id}</strong>
        </div>
        <div className="flex justify-between border-b border-slate-200 pb-2">
          <span className="text-slate-500 font-medium">Program Duration:</span>
          <strong className="text-primary font-bold">{leadData.timeframe || "3 Months (Certificate Track)"}</strong>
        </div>
        <div className="flex justify-between border-b border-slate-200 pb-2">
          <span className="text-slate-500 font-medium">Selected Time Slot:</span>
          <strong className="text-secondary font-bold">{leadData.time_slot}</strong>
        </div>
        <div className="flex justify-between border-b border-slate-200 pb-2">
          <span className="text-slate-500 font-medium">Primary Contact:</span>
          <strong className="text-slate-800">{leadData.phone}</strong>
        </div>
        <div className="pt-1">
          <span className="text-slate-500 font-medium block mb-1.5">Enrolled Curriculum Modules:</span>
          <div className="flex flex-wrap gap-1.5">
            {modules.map((mod, idx) => (
              <span
                key={idx}
                className="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold text-[10px] rounded-md border border-emerald-200"
              >
                {mod}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Next Steps Callout */}
      <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 text-xs max-w-md mx-auto text-left flex items-start gap-2.5">
        <FaCircleInfo className="text-primary mt-0.5 text-base shrink-0" />
        <span>
          Our academic counseling desk will call/WhatsApp you with your batch orientation schedule and lab allocation pass.
        </span>
      </div>

      <div className="pt-2 flex flex-col sm:flex-row justify-center gap-3 max-w-md mx-auto">
        <button
          onClick={onReset}
          className="px-6 py-3 bg-secondary hover:bg-secondary-hover text-white rounded-xl font-bold text-xs transition-all cursor-pointer"
        >
          Register Another Student
        </button>
        <a
          href="tel:9802113456"
          className="px-6 py-3 bg-primary hover:bg-primary-hover text-white rounded-xl font-bold text-xs transition-all flex items-center justify-center gap-2"
        >
          <FaPhone /> Call Admissions Desk
        </a>
      </div>
    </div>
  );
}