"use client";

import React, { useState } from "react";
import {
  FaBrain,
  FaCode,
  FaGlobe,
  FaShieldHalved,
  FaNetworkWired,
  FaCloud,
  FaPhotoFilm,
  FaClock,
  FaHourglassHalf,
  FaCheck,
  FaArrowRight,
  FaSpinner,
  FaCircleExclamation
} from "react-icons/fa6";
import { submitTrainingApplication } from "@/lib/api/training";
import TrainingSuccessModal from "./TrainingSuccessModal";

const renderDynamicIcon = (iconClass, fallback = <FaCode />) => {
  if (!iconClass || typeof iconClass !== "string") return fallback;
  const cls = iconClass.toLowerCase().trim();

  if (cls.includes("brain") || cls.includes("ai") || cls.includes("robot")) return <FaBrain />;
  if (cls.includes("code") || cls.includes("laptop")) return <FaCode />;
  if (cls.includes("globe") || cls.includes("web")) return <FaGlobe />;
  if (cls.includes("shield") || cls.includes("cyber") || cls.includes("security")) return <FaShieldHalved />;
  if (cls.includes("network") || cls.includes("wifi")) return <FaNetworkWired />;
  if (cls.includes("cloud")) return <FaCloud />;
  if (cls.includes("photo") || cls.includes("film") || cls.includes("media")) return <FaPhotoFilm />;

  return fallback;
};

export default function TrainingForm({
  modulesList = [],
  timeSlotsList = [],
  streamOptionsList = [],
  timeframeOptionsList = [],
  deliveryModesList = [],
  experienceLevelsList = []
}) {
  const [submitting, setSubmitting] = useState(false);
  const [submittedLead, setSubmittedLead] = useState(null);
  const [errors, setErrors] = useState({});

  // Fallback options in case CMS returns empty datasets
  const fallbackTimeframeOptions = [
    { id: "fallback-tf-1", name: "1 Month (Foundation Crash Course)" },
    { id: "fallback-tf-2", name: "3 Months (Certificate Track — Recommended)" },
    { id: "fallback-tf-3", name: "6 Months (Mastery & Project Track)" }
  ];

  const fallbackDeliveryModes = [
    { id: "fallback-dm-1", name: "Physical Lab at AIEMS Campus, Bardibas" },
    { id: "fallback-dm-2", name: "Hybrid (Physical Lab + Recorded Access)" }
  ];

  const fallbackExperienceLevels = [
    { id: "fallback-exp-1", name: "Absolute Beginner (Basic typing/browsing only)" },
    { id: "fallback-exp-2", name: "Intermediate (Use MS Word, Email, Social Media daily)" },
    { id: "fallback-exp-3", name: "Curious Explorer (Want career-ready digital skills)" }
  ];

  const effectiveTimeframes = timeframeOptionsList && timeframeOptionsList.length > 0
    ? timeframeOptionsList
    : fallbackTimeframeOptions;

  const effectiveDeliveryModes = deliveryModesList && deliveryModesList.length > 0
    ? deliveryModesList
    : fallbackDeliveryModes;

  const effectiveExperienceLevels = experienceLevelsList && experienceLevelsList.length > 0
    ? experienceLevelsList
    : fallbackExperienceLevels;

  // 100% UNSELECTED DEFAULT STARTING STATES
  const [selectedModules, setSelectedModules] = useState([]);
  const [selectedTimeframe, setSelectedTimeframe] = useState("");
  const [selectedTimeSlot, setSelectedTimeSlot] = useState("");

  const handleModuleToggle = (moduleTitle) => {
    setSelectedModules((prev) => {
      const next = prev.includes(moduleTitle)
        ? prev.filter((title) => title !== moduleTitle)
        : [...prev, moduleTitle];
      if (next.length > 0) {
        setErrors((prevErr) => ({ ...prevErr, modules: undefined }));
      }
      return next;
    });
  };

  const handleTimeframeSelect = (timeframeName) => {
    setSelectedTimeframe(timeframeName);
    setErrors((prevErr) => ({ ...prevErr, timeframe: undefined }));
  };

  const handleTimeSlotSelect = (slotRange) => {
    setSelectedTimeSlot(slotRange);
    setErrors((prevErr) => ({ ...prevErr, timeSlot: undefined }));
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    const formEl = e.target;
    const fullName = formEl.fullName.value.trim();
    const gender = formEl.gender.value;
    const phone = formEl.phone.value.trim().replace(/\s+/g, "");
    const whatsapp = formEl.whatsapp.value.trim();
    const email = formEl.email.value.trim().toLowerCase();
    const academicStream = formEl.academicStream.value;
    const institution = formEl.institution.value.trim();
    const trainingMode = formEl.trainingMode.value;
    const experienceLevel = formEl.experienceLevel.value;
    const learningGoal = formEl.learningGoal.value.trim();

    const newErrors = {};

    if (!fullName || fullName.length < 3) {
      newErrors.fullName = "Please provide your complete name.";
    }
    if (!gender) {
      newErrors.gender = "Please select your gender.";
    }
    if (!phone || phone.length < 8 || phone.length > 15) {
      newErrors.phone = "Please enter a valid phone number (e.g. 98XXXXXXXX).";
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
      newErrors.email = "Please provide a valid email address.";
    }
    if (!academicStream) {
      newErrors.academicStream = "Please select your academic background.";
    }
    if (!institution) {
      newErrors.institution = "Please specify your school/college name.";
    }

    // MANDATORY SELECTION VALIDATIONS FOR MODULES, DURATION, AND TIME SLOTS
    if (selectedModules.length === 0) {
      newErrors.modules = "You must select at least 1 training module to proceed.";
    }
    if (!selectedTimeframe || !selectedTimeframe.trim()) {
      newErrors.timeframe = "You must select a program duration / timeframe.";
    }
    if (!selectedTimeSlot || !selectedTimeSlot.trim()) {
      newErrors.timeSlot = "You must select a preferred daily evening time slot.";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);

      // Scroll smoothly to first relevant error block
      if (newErrors.modules) {
        document.getElementById("section-modules")?.scrollIntoView({ behavior: "smooth", block: "center" });
      } else if (newErrors.timeframe) {
        document.getElementById("section-timeframe")?.scrollIntoView({ behavior: "smooth", block: "center" });
      } else if (newErrors.timeSlot) {
        document.getElementById("section-timeslot")?.scrollIntoView({ behavior: "smooth", block: "center" });
      }
      return;
    }

    setSubmitting(true);

    const payload = {
      full_name: fullName,
      gender,
      phone,
      whatsapp: whatsapp || phone,
      email,
      academic_stream: academicStream,
      institution,
      selected_modules: selectedModules,
      timeframe: selectedTimeframe,
      time_slot: selectedTimeSlot,
      training_mode: trainingMode,
      experience_level: experienceLevel,
      learning_goal: learningGoal || "N/A"
    };

    try {
      const response = await submitTrainingApplication(payload);
      setSubmittedLead(response);
    } catch (err) {
      setErrors({ global: err.message || "Failed to submit registration. Please check your connection and try again." });
    } finally {
      setSubmitting(false);
    }
  };

  const resetForm = () => {
    setSubmittedLead(null);
    setErrors({});
    setSelectedModules([]);
    setSelectedTimeframe("");
    setSelectedTimeSlot("");
  };

  if (submittedLead) {
    return <TrainingSuccessModal leadData={submittedLead} onReset={resetForm} />;
  }

  return (
    <div id="trainingLeadForm">
      <div className="border-b border-slate-100 pb-5 mb-8">
        <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3 py-1 bg-primary/10 rounded-full inline-block mb-2">
          Registration & Assessment Form
        </span>
        <h2 className="font-display font-extrabold text-2xl sm:text-3xl text-secondary">
          Reserve Your Training Seat
        </h2>
        <p className="text-slate-500 text-xs sm:text-sm mt-1">
          Select your customized training modules, course duration, and daily evening time slot.
        </p>
      </div>

      {errors.global && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl font-semibold flex items-center gap-2">
          <FaCircleExclamation className="text-sm shrink-0" />
          <span>{errors.global}</span>
        </div>
      )}

      <form onSubmit={handleFormSubmit} className="space-y-8">
        
        {/* STEP 1: APPLICANT PROFILE */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-secondary">
            <span className="w-6 h-6 rounded-md bg-primary text-white flex items-center justify-center text-xs font-bold font-display">1</span>
            <h3 className="font-display font-bold text-base sm:text-lg">Applicant Background</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Full Name */}
            <div>
              <label className="block text-xs font-bold text-secondary uppercase tracking-wider mb-1.5">
                Full Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="fullName"
                placeholder="e.g. Ramesh Karki"
                className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-all"
              />
              {errors.fullName && <p className="text-red-500 text-xs mt-1 font-semibold">{errors.fullName}</p>}
            </div>

            {/* Gender */}
            <div>
              <label className="block text-xs font-bold text-secondary uppercase tracking-wider mb-1.5">
                Gender <span className="text-red-500">*</span>
              </label>
              <select
                name="gender"
                defaultValue=""
                className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-all"
              >
                <option value="" disabled>Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
              {errors.gender && <p className="text-red-500 text-xs mt-1 font-semibold">{errors.gender}</p>}
            </div>

            {/* Mobile Phone */}
            <div>
              <label className="block text-xs font-bold text-secondary uppercase tracking-wider mb-1.5">
                Mobile Number <span className="text-red-500">*</span>
              </label>
              <input
                type="tel"
                name="phone"
                placeholder="e.g. 98XXXXXXXX"
                className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-all"
              />
              {errors.phone && <p className="text-red-500 text-xs mt-1 font-semibold">{errors.phone}</p>}
            </div>

            {/* WhatsApp */}
            <div>
              <label className="block text-xs font-bold text-secondary uppercase tracking-wider mb-1.5">
                WhatsApp Number (Optional)
              </label>
              <input
                type="tel"
                name="whatsapp"
                placeholder="WhatsApp phone number"
                className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-all"
              />
            </div>

            {/* Email */}
            <div>
              <label className="block text-xs font-bold text-secondary uppercase tracking-wider mb-1.5">
                Email Address <span className="text-red-500">*</span>
              </label>
              <input
                type="email"
                name="email"
                placeholder="name@example.com"
                className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-all"
              />
              {errors.email && <p className="text-red-500 text-xs mt-1 font-semibold">{errors.email}</p>}
            </div>

            {/* Academic Stream */}
            <div>
              <label className="block text-xs font-bold text-secondary uppercase tracking-wider mb-1.5">
                Current Field / Stream <span className="text-red-500">*</span>
              </label>
              <select
                name="academicStream"
                defaultValue=""
                className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-all"
              >
                <option value="" disabled>Select Your Background</option>
                {streamOptionsList.map((opt) => (
                  <option key={opt.id || opt.name} value={opt.name}>
                    {opt.name}
                  </option>
                ))}
              </select>
              {errors.academicStream && <p className="text-red-500 text-xs mt-1 font-semibold">{errors.academicStream}</p>}
            </div>

            {/* Previous School/College */}
            <div className="sm:col-span-2">
              <label className="block text-xs font-bold text-secondary uppercase tracking-wider mb-1.5">
                Previous School / College / City <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="institution"
                placeholder="e.g. Gaurishankar College, Bardibas"
                className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-all"
              />
              {errors.institution && <p className="text-red-500 text-xs mt-1 font-semibold">{errors.institution}</p>}
            </div>

          </div>
        </div>

        {/* STEP 2: MODULE SELECTION (100% UNSELECTED START) */}
        <div id="section-modules" className="border-t border-slate-100 pt-6 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center gap-2 text-secondary">
              <span className="w-6 h-6 rounded-md bg-primary text-white flex items-center justify-center text-xs font-bold font-display">2</span>
              <h3 className="font-display font-bold text-base sm:text-lg">Select Training Modules</h3>
            </div>
            <span className="text-xs text-primary font-bold bg-primary/10 px-3 py-1 rounded-full self-start sm:self-auto">
              Choose 1 or more modules
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            {modulesList.map((mod, idx) => {
              const isChecked = selectedModules.includes(mod.title);

              return (
                <div
                  key={mod.id || idx}
                  onClick={() => handleModuleToggle(mod.title)}
                  className={`p-3.5 rounded-2xl border-2 transition-all cursor-pointer flex items-start gap-3 select-none ${
                    isChecked
                      ? "border-primary bg-emerald-50/70 shadow-sm"
                      : "border-slate-200 bg-surface hover:border-slate-300"
                  }`}
                >
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-lg shrink-0 transition-colors ${
                    isChecked ? "bg-primary text-white" : "bg-primary/10 text-primary"
                  }`}>
                    {renderDynamicIcon(mod.icon_class, <FaCode />)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h4 className="font-display font-bold text-secondary text-xs sm:text-sm">{mod.title}</h4>
                      <span
                        className={`w-4 h-4 rounded-full border flex items-center justify-center text-[9px] transition-colors ${
                          isChecked
                            ? "bg-primary text-white border-primary"
                            : "border-slate-300 text-transparent"
                        }`}
                      >
                        <FaCheck />
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-500 mt-0.5 leading-relaxed">{mod.description}</p>
                  </div>
                </div>
              );
            })}
          </div>
          {errors.modules && (
            <p className="text-red-500 text-xs font-bold mt-2 flex items-center gap-1.5 bg-red-50 p-2.5 rounded-lg border border-red-200">
              <FaCircleExclamation /> {errors.modules}
            </p>
          )}
        </div>

        {/* STEP 3: PROGRAM DURATION / TIMEFRAME (100% UNSELECTED START) */}
        <div id="section-timeframe" className="border-t border-slate-100 pt-6 space-y-4">
          <div className="flex items-center gap-2 text-secondary">
            <span className="w-6 h-6 rounded-md bg-primary text-white flex items-center justify-center text-xs font-bold font-display">3</span>
            <h3 className="font-display font-bold text-base sm:text-lg">Program Duration / Timeframe</h3>
          </div>
          <p className="text-xs text-slate-500">
            Choose the duration that matches your learning pace and academic schedule.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {effectiveTimeframes.map((tf, idx) => {
              const isSelected = selectedTimeframe === tf.name;

              return (
                <div
                  key={tf.id || idx}
                  onClick={() => handleTimeframeSelect(tf.name)}
                  className={`p-4 rounded-2xl border-2 transition-all cursor-pointer select-none text-left flex flex-col justify-between ${
                    isSelected
                      ? "border-primary bg-emerald-50/80 shadow-sm"
                      : "border-slate-200 bg-surface hover:border-slate-300"
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <FaHourglassHalf className={isSelected ? "text-primary text-lg" : "text-slate-400 text-base"} />
                    <span
                      className={`w-4 h-4 rounded-full border flex items-center justify-center text-[9px] transition-colors ${
                        isSelected
                          ? "bg-primary text-white border-primary"
                          : "border-slate-300 text-transparent"
                      }`}
                    >
                      <FaCheck />
                    </span>
                  </div>
                  <strong className="font-display font-bold text-xs sm:text-sm text-secondary block leading-snug">
                    {tf.name}
                  </strong>
                </div>
              );
            })}
          </div>
          {errors.timeframe && (
            <p className="text-red-500 text-xs font-bold mt-2 flex items-center gap-1.5 bg-red-50 p-2.5 rounded-lg border border-red-200">
              <FaCircleExclamation /> {errors.timeframe}
            </p>
          )}
        </div>

        {/* STEP 4: DAILY EVENING TIME SLOTS (100% UNSELECTED START) */}
        <div id="section-timeslot" className="border-t border-slate-100 pt-6 space-y-4">
          <div className="flex items-center gap-2 text-secondary">
            <span className="w-6 h-6 rounded-md bg-primary text-white flex items-center justify-center text-xs font-bold font-display">4</span>
            <h3 className="font-display font-bold text-base sm:text-lg">Preferred Daily Time Slot</h3>
          </div>
          <p className="text-xs text-slate-500">
            Classes run 1 hour daily in our dedicated computer lab at AIEMS Campus, Bardibas.
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {timeSlotsList.map((slot, idx) => {
              const isSelected = selectedTimeSlot === slot.time_range;

              return (
                <div
                  key={slot.id || idx}
                  onClick={() => handleTimeSlotSelect(slot.time_range)}
                  className={`p-3.5 rounded-2xl border-2 text-center transition-all cursor-pointer select-none ${
                    isSelected
                      ? "border-primary bg-secondary text-white shadow-md scale-[1.02]"
                      : "border-slate-200 bg-surface text-slate-800 hover:border-slate-300"
                  }`}
                >
                  <FaClock
                    className={`text-lg mb-1 mx-auto block transition-colors ${
                      isSelected ? "text-accent" : "text-primary"
                    }`}
                  />
                  <span className="font-display font-bold text-xs sm:text-sm block">{slot.time_range}</span>
                  <span
                    className={`text-[10px] block mt-0.5 ${
                      isSelected ? "text-slate-300" : "text-slate-500"
                    }`}
                  >
                    {slot.slot_tag}
                  </span>
                </div>
              );
            })}
          </div>
          {errors.timeSlot && (
            <p className="text-red-500 text-xs font-bold mt-2 flex items-center gap-1.5 bg-red-50 p-2.5 rounded-lg border border-red-200">
              <FaCircleExclamation /> {errors.timeSlot}
            </p>
          )}
        </div>

        {/* STEP 5: DELIVERY MODE & GOALS */}
        <div className="border-t border-slate-100 pt-6 space-y-4">
          <div className="flex items-center gap-2 text-secondary">
            <span className="w-6 h-6 rounded-md bg-primary text-white flex items-center justify-center text-xs font-bold font-display">5</span>
            <h3 className="font-display font-bold text-base sm:text-lg">Delivery & Goals</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Delivery Mode */}
            <div>
              <label className="block text-xs font-bold text-secondary uppercase tracking-wider mb-1.5">
                Delivery Mode <span className="text-red-500">*</span>
              </label>
              <select
                name="trainingMode"
                defaultValue={effectiveDeliveryModes[0]?.name || ""}
                className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-all"
              >
                {effectiveDeliveryModes.map((mode, mIdx) => (
                  <option key={mode.id || mIdx} value={mode.name}>
                    {mode.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Experience Level */}
            <div>
              <label className="block text-xs font-bold text-secondary uppercase tracking-wider mb-1.5">
                Current Computer Experience <span className="text-red-500">*</span>
              </label>
              <select
                name="experienceLevel"
                defaultValue={effectiveExperienceLevels[0]?.name || ""}
                className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-all"
              >
                {effectiveExperienceLevels.map((exp, eIdx) => (
                  <option key={exp.id || eIdx} value={exp.name}>
                    {exp.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Specific Learning Goals */}
            <div className="sm:col-span-2">
              <label className="block text-xs font-bold text-secondary uppercase tracking-wider mb-1.5">
                Any specific questions or goals? (Optional)
              </label>
              <textarea
                name="learningGoal"
                rows="3"
                placeholder="e.g. I want to build a portfolio and learn generative AI tools to support my business studies..."
                className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-all"
              />
            </div>
          </div>
        </div>

        {/* STEP 6: SUBMIT BUTTON */}
        <div className="pt-4 space-y-4">
          <label className="flex items-start gap-3 cursor-pointer">
            <input
              type="checkbox"
              required
              defaultChecked
              className="mt-1 w-4 h-4 rounded text-primary focus:ring-primary border-slate-300 cursor-pointer"
            />
            <span className="text-xs text-slate-600 leading-normal">
              I confirm that all details provided are accurate so the AIEMS Academic Counseling Team can send me batch schedules and lab allocation passes.
            </span>
          </label>

          <button
            type="submit"
            disabled={submitting}
            className="w-full bg-primary hover:bg-primary-hover text-white font-display font-bold text-sm sm:text-base py-4 rounded-xl shadow-glow-primary hover:shadow-primary/50 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-75"
          >
            {submitting ? (
              <>
                <FaSpinner className="animate-spin text-sm" />
                <span>Submitting Registration...</span>
              </>
            ) : (
              <>
                <span>Submit Training Registration</span>
                <FaArrowRight className="text-xs" />
              </>
            )}
          </button>
        </div>

      </form>
    </div>
  );
}