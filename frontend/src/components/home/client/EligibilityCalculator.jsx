"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { FaCircleCheck, FaCircleXmark, FaTriangleExclamation, FaArrowRight } from "react-icons/fa6";

/**
 * EligibilityCalculator Component
 * Interactive grade validation tool with dynamic evaluation parameters and visual stream options from CMS.
 */
export default function EligibilityCalculator({ eligibilityConfig = {} }) {
  const defaultStreams = [
    { id: 1, name: "Science Stream", is_eligible: true },
    { id: 2, name: "Management Stream", is_eligible: false },
    { id: 3, name: "Humanities / Other", is_eligible: false }
  ];

  const streams = (
    Array.isArray(eligibilityConfig?.stream_options) && eligibilityConfig.stream_options.length > 0
      ? eligibilityConfig.stream_options
      : defaultStreams
  );

  const [stream, setStream] = useState(streams[0]?.name || "Science Stream");
  const [evalType, setEvalType] = useState("cgpa");
  const [score, setScore] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    if (streams.length > 0 && !streams.some((s) => String(s.name) === String(stream))) {
      setStream(streams[0].name);
    }
  }, [eligibilityConfig]);

  // Parse numeric thresholds dynamically from CMS configuration
  const minCgpaThreshold = eligibilityConfig?.min_cgpa ? parseFloat(eligibilityConfig.min_cgpa) : 2.2;
  const minPercentageThreshold = eligibilityConfig?.min_percentage ? parseFloat(eligibilityConfig.min_percentage) : 55.0;

  const headingText = eligibilityConfig?.heading || "Eligibility Calculator";
  const subHeadingText = eligibilityConfig?.sub_heading || "";
  const requiredStreamText = eligibilityConfig?.required_stream_text || "";
  const passMessage = eligibilityConfig?.eligible_message || "Your score meets the academic requirements.";
  const failMessage = eligibilityConfig?.ineligible_message || "Your score falls below the required threshold.";

  const handleCalculate = (e) => {
    e.preventDefault();
    const parsedScore = parseFloat(score);

    if (isNaN(parsedScore)) {
      setResult({
        status: "warning",
        message: "Please enter a valid numeric grade score.",
      });
      return;
    }

    const selectedStreamObj = streams.find((s) => String(s.name) === String(stream));
    const isStreamEligible = selectedStreamObj ? selectedStreamObj.is_eligible !== false : true;

    if (!isStreamEligible) {
      setResult({
        status: "error",
        message: `Ineligible: Selected stream (${selectedStreamObj?.name || stream}) does not meet entrance prerequisites.`,
      });
      return;
    }

    let isScoreEligible = false;
    if (evalType === "cgpa" && parsedScore >= minCgpaThreshold) isScoreEligible = true;
    if (evalType === "percentage" && parsedScore >= minPercentageThreshold) isScoreEligible = true;

    if (isScoreEligible) {
      setResult({
        status: "success",
        message: `${passMessage} (Evaluated Score: ${parsedScore})`,
      });
    } else {
      setResult({
        status: "error",
        message: `${failMessage} (Evaluated Score: ${parsedScore})`,
      });
    }
  };

  return (
    <div id="eligibility-calculator" className="py-24 bg-surface scroll-mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-3xl shadow-ultra border border-slate-100 p-8 md:p-12">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            
            {/* Left Column Description */}
            <div className="lg:col-span-5 space-y-6">
              <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3 py-1 bg-primary/10 rounded-full">
                Interactive Evaluation
              </span>
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary leading-tight">
                {headingText}
              </h2>
              {subHeadingText && (
                <p className="text-slate-600 text-sm sm:text-base leading-relaxed">
                  {subHeadingText}
                </p>
              )}

              <div className="space-y-3 pt-2">
                {requiredStreamText && (
                  <div className="flex items-start gap-3">
                    <FaCircleCheck className="text-primary text-xl mt-0.5 shrink-0" />
                    <p className="text-xs sm:text-sm text-slate-700 font-medium">
                      {requiredStreamText}
                    </p>
                  </div>
                )}
                <div className="flex items-start gap-3">
                  <FaCircleCheck className="text-primary text-xl mt-0.5 shrink-0" />
                  <p className="text-xs sm:text-sm text-slate-700">
                    <strong>Minimum Benchmark:</strong> {minCgpaThreshold} CGPA or {minPercentageThreshold}% aggregate.
                  </p>
                </div>
              </div>
            </div>

            {/* Right Calculator Form */}
            <div className="lg:col-span-7 bg-surface p-6 sm:p-8 rounded-2xl border border-slate-200">
              <form onSubmit={handleCalculate} className="space-y-5">
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-secondary uppercase mb-2">
                      Academic Stream (+2 / Grade 12)
                    </label>
                    <select
                      value={stream}
                      onChange={(e) => setStream(e.target.value)}
                      className="w-full bg-white border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:outline-none"
                    >
                      {streams.map((st) => (
                        <option key={st.id || st.name} value={st.name}>
                          {st.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-secondary uppercase mb-2">
                      Grading Scale
                    </label>
                    <select
                      value={evalType}
                      onChange={(e) => setEvalType(e.target.value)}
                      className="w-full bg-white border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:outline-none"
                    >
                      <option value="cgpa">CGPA Scale (4.0 Max)</option>
                      <option value="percentage">Percentage Scale (%)</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-secondary uppercase mb-2">
                    Obtained Score / CGPA / %
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={score}
                    onChange={(e) => setScore(e.target.value)}
                    placeholder="Enter your CGPA or % score"
                    className="w-full bg-white border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:outline-none"
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-primary hover:bg-primary-hover text-white font-bold py-3.5 rounded-xl shadow-lg shadow-primary/20 transition-all text-sm cursor-pointer"
                >
                  Evaluate Eligibility Now
                </button>

              </form>

              {/* Dynamic Evaluation Output */}
              {result && (
                <div className="mt-6">
                  {result.status === "success" && (
                    <div className="p-5 rounded-xl border bg-emerald-50 border-emerald-200 text-emerald-800 text-xs sm:text-sm font-medium flex items-start gap-3">
                      <FaCircleCheck className="text-primary text-2xl shrink-0 mt-0.5" />
                      <div>
                        <strong className="block text-emerald-900 font-bold mb-1">Eligible!</strong>
                        <p>{result.message}</p>
                        <Link
                          href="/apply-now"
                          className="inline-flex items-center gap-1.5 mt-3 text-xs font-bold text-primary hover:underline"
                        >
                          Proceed to Admission Application <FaArrowRight className="text-[10px]" />
                        </Link>
                      </div>
                    </div>
                  )}

                  {result.status === "error" && (
                    <div className="p-5 rounded-xl border bg-amber-50 border-amber-200 text-amber-900 text-xs sm:text-sm font-medium flex items-start gap-3">
                      <FaCircleXmark className="text-amber-600 text-2xl shrink-0 mt-0.5" />
                      <div>
                        <strong className="block text-amber-900 font-bold mb-1">Requirement Check</strong>
                        <p>{result.message}</p>
                        <Link
                          href="/contact-us"
                          className="inline-flex items-center gap-1.5 mt-3 text-xs font-bold text-amber-900 hover:underline"
                        >
                          Contact Admissions Desk <FaArrowRight className="text-[10px]" />
                        </Link>
                      </div>
                    </div>
                  )}

                  {result.status === "warning" && (
                    <div className="p-4 rounded-xl border bg-amber-50 border-amber-200 text-amber-800 text-xs sm:text-sm font-medium flex items-center gap-2">
                      <FaTriangleExclamation className="text-amber-600 shrink-0" />
                      <span>{result.message}</span>
                    </div>
                  )}
                </div>
              )}

            </div>

          </div>
        </div>
      </div>
    </div>
  );
}