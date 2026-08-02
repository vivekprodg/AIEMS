"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import {
  FaChevronRight,
  FaPaperPlane,
  FaBookOpen,
  FaBuildingColumns,
  FaCode,
  FaNetworkWired,
  FaUserGear,
  FaStar,
  FaGraduationCap,
  FaAward,
  FaMicrochip,
  FaLightbulb,
  FaUsers,
  FaCircleCheck,
  FaDatabase,
  FaLaptopCode,
  FaSitemap,
  FaArrowRight,
  FaCalculator
} from "react-icons/fa6";
import { resolveMediaUrl } from "@/lib/api/home";

/**
 * AnimatedCounter
 * Scroll-triggered count-up animation for numeric stats.
 */
const AnimatedCounter = ({ targetValue, duration = 1.5 }) => {
  const [count, setCount] = useState(0);
  const elementRef = useRef(null);

  useEffect(() => {
    const el = elementRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            let start = 0;
            const end = parseInt(targetValue, 10);
            if (isNaN(end)) {
              setCount(targetValue);
              return;
            }

            const stepTime = Math.abs(Math.floor((duration * 1000) / end));
            const timer = setInterval(() => {
              start += Math.ceil(end / 40);
              if (start >= end) {
                setCount(end);
                clearInterval(timer);
              } else {
                setCount(start);
              }
            }, Math.max(stepTime, 20));

            observer.unobserve(el);
          }
        });
      },
      { threshold: 0.3 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [targetValue, duration]);

  return <span ref={elementRef}>{count}</span>;
};

/**
 * Dynamic Icon Resolver
 */
const renderDynamicIcon = (iconClass, fallback = <FaCode />) => {
  if (!iconClass || typeof iconClass !== "string") return fallback;
  const cls = iconClass.toLowerCase().trim();

  if (cls.includes("circle-check") || cls.includes("check-circle") || cls.includes("check")) return <FaCircleCheck />;
  if (cls.includes("building") || cls.includes("university") || cls.includes("columns")) return <FaBuildingColumns />;
  if (cls.includes("code") || cls.includes("laptop") || cls.includes("terminal")) return <FaCode />;
  if (cls.includes("network") || cls.includes("sitemap")) return <FaNetworkWired />;
  if (cls.includes("user-gear") || cls.includes("gear") || cls.includes("mentor")) return <FaUserGear />;
  if (cls.includes("users") || cls.includes("people") || cls.includes("instructor")) return <FaUsers />;
  if (cls.includes("graduation") || cls.includes("cap")) return <FaGraduationCap />;
  if (cls.includes("award") || cls.includes("trophy") || cls.includes("certificate")) return <FaAward />;
  if (cls.includes("microchip") || cls.includes("hardware")) return <FaMicrochip />;
  if (cls.includes("database") || cls.includes("sql")) return <FaDatabase />;
  if (cls.includes("star")) return <FaStar />;
  if (cls.includes("lightbulb") || cls.includes("idea")) return <FaLightbulb />;

  return fallback;
};

export default function HomeContent({ content = {} }) {
  const topBanner = content?.top_banners || {};
  const aboutBanner = content?.about_banners || {};
  const programData = content?.programs || {};

  const heroImage = resolveMediaUrl(topBanner.image);
  const aboutBannerImage = resolveMediaUrl(aboutBanner.image);

  const technicalTags = Array.isArray(topBanner.technical_tags) ? topBanner.technical_tags : [];
  const rawLandingStats = Array.isArray(topBanner.landing_stats) ? topBanner.landing_stats : [];
  const aboutItems = Array.isArray(aboutBanner.items) ? aboutBanner.items : [];

  const isolatedCards = Array.isArray(programData.isolated_showcase_cards) ? programData.isolated_showcase_cards : [];
  const standardProgramItems = Array.isArray(programData.items) ? programData.items : [];
  
  const hasIsolatedCards = isolatedCards.length > 0;

  // Exact Copy Fallbacks from index.html
  const defaultLandingStats = [
    { id: "fallback-1", prefix: "", target_number: 1, suffix: "st", label: "Pioneer Cohort", sub_label: "Founding CSIT Batch" },
    { id: "fallback-2", prefix: "", target_number: 100, suffix: "%", label: "Practical Labs", sub_label: "Hands-on technical setup" },
    { id: "fallback-3", prefix: "", target_number: 10, suffix: "+", label: "Expert Instructors", sub_label: "Experienced CSIT faculty" },
    { id: "fallback-4", prefix: "TU", target_number: 0, suffix: "", label: "Affiliated Curriculum", sub_label: "Tribhuvan University" }
  ];

  const landingStats = rawLandingStats.length > 0 ? rawLandingStats : defaultLandingStats;

  // Dynamic Content with Smart Fallbacks matching index.html
  const heroBadge = topBanner.badge_text || "Inaugural Batch 2026/2027 — Brand New Technical Institute in Bardibas";
  const heroHeading = topBanner.heading || "Master Computer Science & Information Technology";
  const heroSubHeading = topBanner.sub_heading || "Join the pioneer batch at Ankur Institute. Offering Tribhuvan University affiliated BSc. CSIT with hands-on software development, database administration, and computer networking.";
  const primaryBtnText = topBanner.primary_btn_text || "Apply For BSc. CSIT";
  const primaryBtnUrl = topBanner.primary_btn_url || "#admissions";
  const secondaryBtnText = topBanner.secondary_btn_text || "Explore Syllabus & Modules";
  const secondaryBtnUrl = topBanner.secondary_btn_url || "#program";

  return (
    <div className="w-full space-y-0">
      
      {/* ============================================================================== */}
      {/* 1. HERO SECTION */}
      {/* ============================================================================== */}
      <section className="relative min-h-[75vh] md:min-h-[85vh] flex items-center justify-center bg-secondary overflow-hidden pb-12 sm:pb-16">
        {heroImage && (
          <div className="absolute inset-0 z-0">
            <img
              src={heroImage}
              alt={heroHeading}
              className="w-full h-full object-cover object-center select-none"
            />
            <div className="absolute inset-0 hero-overlay" aria-hidden="true" />
          </div>
        )}

        {/* Background Gradient Accents */}
        <div className="absolute top-1/4 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-accent/20 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-12 sm:pb-16 text-center text-white">
          
          {/* Badge */}
          {heroBadge && (
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-dark text-accent text-xs md:text-sm font-semibold mb-6 border border-accent/30 shadow-lg">
              <span className="w-2.5 h-2.5 rounded-full bg-primary animate-ping" />
              {heroBadge}
            </div>
          )}

          {/* Main Headline */}
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl md:text-6xl lg:text-7xl leading-tight tracking-tight max-w-5xl mx-auto">
            {heroHeading}
          </h1>

          {/* Sub-headline */}
          {heroSubHeading && (
            <p className="mt-6 text-base sm:text-lg md:text-xl text-slate-200 max-w-3xl mx-auto font-normal leading-relaxed">
              {heroSubHeading}
            </p>
          )}

          {/* Action CTA Buttons */}
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto sm:max-w-none">
            {primaryBtnText && (
              <a
                href={primaryBtnUrl}
                className="w-full sm:w-auto bg-primary hover:bg-primary-hover text-white font-bold text-base px-8 py-4 rounded-xl shadow-glow-primary hover:shadow-primary/60 hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-2"
              >
                <FaPaperPlane /> {primaryBtnText}
              </a>
            )}
            {secondaryBtnText && (
              <a
                href={secondaryBtnUrl}
                className="w-full sm:w-auto glass-dark hover:bg-white/10 text-white font-semibold text-base px-8 py-4 rounded-xl border border-white/30 hover:border-white transition-all duration-300 flex items-center justify-center gap-2"
              >
                <FaBookOpen /> {secondaryBtnText}
              </a>
            )}
          </div>

          {/* Technical Tags Bar */}
          {technicalTags.length > 0 && (
            <div className="mt-14 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto pt-8 border-t border-white/15 text-xs sm:text-sm font-medium text-slate-300">
              {technicalTags.map((tag, idx) => (
                <div key={tag.id || idx} className="flex items-center justify-center gap-2 text-center">
                  <span className="text-accent text-base shrink-0">
                    {renderDynamicIcon(tag.icon_class, <FaBuildingColumns />)}
                  </span>
                  <span>{tag.title}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* ============================================================================== */}
      {/* 2. FLOATING OVERLAPPING STATS CARD (COMPACT HEIGHT, CLEAN TYPOGRAPHY) */}
      {/* ============================================================================== */}
      {landingStats.length > 0 && (
        <div className="relative z-20 -translate-y-[30%] max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl shadow-ultra border border-slate-100 py-4 px-6 md:py-5 md:px-8">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 divide-y sm:divide-y-0 sm:divide-x divide-slate-100 text-center">
              {landingStats.map((stat, idx) => {
                const hasTargetNumber =
                  stat.target_number !== null &&
                  stat.target_number !== undefined &&
                  Number(stat.target_number) > 0;

                return (
                  <div
                    key={stat.id || idx}
                    className={`flex flex-col items-center justify-center p-1 sm:p-1.5 ${
                      idx > 0 ? "pt-4 sm:pt-1.5" : ""
                    }`}
                  >
                    {/* Number / Value Row */}
                    <div className="text-3xl sm:text-4xl md:text-5xl font-display font-extrabold text-primary flex items-center justify-center whitespace-nowrap leading-none gap-0.5">
                      {stat.prefix && <span>{stat.prefix}</span>}
                      {hasTargetNumber ? (
                        <AnimatedCounter targetValue={stat.target_number} />
                      ) : null}
                      {stat.suffix && <span className="text-accent">{stat.suffix}</span>}
                    </div>

                    {/* Primary Title Label */}
                    {stat.label && (
                      <span className="text-secondary font-bold text-sm sm:text-base mt-2 block leading-snug">
                        {stat.label}
                      </span>
                    )}

                    {/* Secondary Sub-label */}
                    {stat.sub_label && (
                      <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">
                        {stat.sub_label}
                      </p>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* ============================================================================== */}
      {/* 3. ABOUT AIEMS SECTION */}
      {/* ============================================================================== */}
      {(aboutBanner.heading || aboutBannerImage) && (
        <section id="about" className="pt-8 sm:pt-12 pb-24 bg-surface scroll-mt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              
              {/* Left Column: Featured Image & Floating Glass Badge Overlay */}
              <div className="lg:col-span-6 relative">
                {aboutBannerImage ? (
                  <div className="relative z-10 rounded-2xl overflow-hidden shadow-2xl border-4 border-white">
                    <img
                      src={aboutBannerImage}
                      alt={aboutBanner.heading || "About AIEMS"}
                      className="w-full h-auto object-cover transform hover:scale-105 transition-transform duration-700"
                    />
                  </div>
                ) : (
                  <div className="relative z-10 rounded-2xl overflow-hidden shadow-2xl border-4 border-white bg-secondary/10 min-h-[350px] flex items-center justify-center text-slate-400 font-medium text-sm">
                    No image configured in CMS
                  </div>
                )}

                {/* Floating Glass Badge Overlay */}
                {(aboutBanner.floating_badge_title || aboutBanner.floating_badge_subtitle) && (
                  <div className="absolute -bottom-6 -right-6 z-20 glass-card bg-white p-6 rounded-2xl shadow-xl max-w-xs hidden sm:block border-l-4 border-primary">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-full bg-primary/10 text-primary flex items-center justify-center text-2xl font-bold shrink-0">
                        {renderDynamicIcon(aboutBanner.floating_badge_icon_class, <FaMicrochip />)}
                      </div>
                      <div>
                        {aboutBanner.floating_badge_title && (
                          <h4 className="font-bold text-secondary text-sm">
                            {aboutBanner.floating_badge_title}
                          </h4>
                        )}
                        {aboutBanner.floating_badge_subtitle && (
                          <p className="text-xs text-slate-500">
                            {aboutBanner.floating_badge_subtitle}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Right Column: Narrative Copy & Checkmark Cards */}
              <div className="lg:col-span-6 space-y-6">
                {aboutBanner.badge_text && (
                  <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3 py-1 bg-primary/10 rounded-full inline-block">
                    {aboutBanner.badge_text}
                  </span>
                )}

                {aboutBanner.heading && (
                  <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary leading-tight">
                    {aboutBanner.heading}
                  </h2>
                )}

                {aboutBanner.sub_heading && (
                  <p className="text-slate-600 text-base leading-relaxed">
                    {aboutBanner.sub_heading}
                  </p>
                )}

                {aboutBanner.content_paragraph_2 && (
                  <p className="text-slate-600 text-sm leading-relaxed">
                    {aboutBanner.content_paragraph_2}
                  </p>
                )}

                {/* 2-Card Checkmark Feature Grid */}
                {aboutItems.length > 0 && (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                    {aboutItems.map((item, idx) => (
                      <div
                        key={item.id || idx}
                        className="p-4 bg-white rounded-xl border border-slate-200/80 shadow-sm flex items-start gap-3"
                      >
                        <div className="text-primary text-xl mt-0.5 shrink-0">
                          {renderDynamicIcon(item.icon_class, <FaCircleCheck />)}
                        </div>
                        <div>
                          <h4 className="font-bold text-secondary text-sm">{item.heading}</h4>
                          <p className="text-xs text-slate-500 mt-1">{item.content}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Action CTAs */}
                <div className="pt-4 flex items-center gap-6">
                  {aboutBanner.primary_btn_text && (
                    <a
                      href={aboutBanner.primary_btn_url || "#program"}
                      className="bg-secondary hover:bg-secondary-hover text-white font-semibold px-6 py-3.5 rounded-xl shadow-md transition-all text-sm"
                    >
                      {aboutBanner.primary_btn_text}
                    </a>
                  )}
                  {aboutBanner.secondary_btn_text && (
                    <a
                      href={aboutBanner.secondary_btn_url || "#contact"}
                      className="text-primary font-bold text-sm hover:underline flex items-center gap-1.5"
                    >
                      {aboutBanner.secondary_btn_text} <FaChevronRight className="text-xs" />
                    </a>
                  )}
                </div>

              </div>

            </div>
          </div>
        </section>
      )}

      {/* ============================================================================== */}
      {/* 4. FEATURED PROGRAM SHOWCASE */}
      {/* ============================================================================== */}
      {programData.heading && (
        <section id="program" className="py-24 bg-white scroll-mt-20 border-t border-slate-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            {/* Section Header */}
            <div className="text-center max-w-3xl mx-auto mb-16">
              <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3 py-1 bg-primary/10 rounded-full inline-block">
                Featured Program
              </span>
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                {programData.heading}
              </h2>
              {programData.sub_heading && (
                <p className="text-slate-600 text-base mt-3">
                  {programData.sub_heading}
                </p>
              )}
            </div>

            {hasIsolatedCards ? (
              <div className="space-y-12">
                {isolatedCards.map((card) => {
                  const bannerImg = card.banner_image || "/assets/banner1.jpg";
                  const featurePills = Array.isArray(card.features) ? card.features : [];
                  const requirementRules = Array.isArray(card.requirements) ? card.requirements : [];
                  const summaryPoints = Array.isArray(card.summary_points) ? card.summary_points : [];

                  const summaryText = summaryPoints.length > 0
                    ? summaryPoints.map(s => `${s.value} ${s.sub_text || s.title}`).join(" | ")
                    : "4 Years | 8 Semesters | 126 Credit Hours";

                  const charterBadgeTag = card.charter_badge_tag || "Rajarshi Janak University Affiliated Institution";
                  const specializationsTitle = card.specializations_title || "Core Technical Specializations";
                  const narrativeCopy = card.sub_content || "";
                  const prerequisiteTitle = card.prerequisite_title || "Entry Prerequisites (+2 Science)";
                  const prerequisiteOverview = card.prerequisite_overview || (requirementRules.length > 0 ? requirementRules.map(r => r.content).join(" - ") : "");

                  const targetSyllabusUrl = card.custom_syllabus_redirect_url || (
                    card.target_program_id ? `/programs/${card.target_program_id}` : "/home"
                  );

                  return (
                    <div
                      key={card.id}
                      className="bg-surface rounded-3xl border border-slate-200 overflow-hidden shadow-xl grid grid-cols-1 lg:grid-cols-12 gap-0"
                    >
                      {/* Left Banner Image & Badges */}
                      <div className="lg:col-span-5 relative min-h-[320px] lg:min-h-full">
                        <img
                          src={bannerImg}
                          alt={card.heading || "Showcase Banner"}
                          className="w-full h-full object-cover"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-secondary/90 via-secondary/40 to-transparent" />

                        <div className="absolute bottom-6 left-6 right-6 text-white space-y-2 z-10">
                          {charterBadgeTag && (
                            <span className="bg-primary text-white text-xs font-extrabold px-3 py-1 rounded-full uppercase tracking-wider inline-block">
                              {charterBadgeTag}
                            </span>
                          )}
                          <h3 className="font-display font-bold text-2xl">
                            {card.heading}
                          </h3>
                          <p className="text-xs text-slate-300">
                            {summaryText}
                          </p>
                        </div>
                      </div>

                      {/* Right Course Details */}
                      <div className="lg:col-span-7 p-8 sm:p-12 space-y-6 flex flex-col justify-between">
                        <div className="space-y-4">
                          <div className="flex items-center justify-between flex-wrap gap-2">
                            <span className="text-xs font-extrabold text-primary uppercase tracking-wider bg-primary/10 px-3 py-1 rounded-full">
                              {card.status_badge_text || "Now Accepting Applications"}
                            </span>
                            <span className="text-xs font-bold text-slate-400">
                              {card.cohort_tag || "Inaugural Cohort"}
                            </span>
                          </div>

                          <h4 className="font-display font-bold text-2xl text-secondary">
                            {specializationsTitle}
                          </h4>

                          {narrativeCopy && (
                            <p className="text-slate-600 text-sm leading-relaxed">
                              {narrativeCopy}
                            </p>
                          )}

                          {featurePills.length > 0 && (
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                              {featurePills.map((feat, fIdx) => (
                                <div
                                  key={feat.id || fIdx}
                                  className="p-3 bg-white rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 flex items-center gap-2 shadow-sm"
                                >
                                  <span className="text-primary text-sm shrink-0">
                                    {renderDynamicIcon(feat.icon_class, <FaCode />)}
                                  </span>
                                  <span>{feat.title}</span>
                                </div>
                              ))}
                            </div>
                          )}

                          {prerequisiteOverview && (
                            <div className="p-4 bg-primary/5 rounded-xl border border-primary/20 text-xs text-slate-700 space-y-1 mt-4">
                              <strong className="text-primary block font-bold flex items-center gap-1.5">
                                <FaCircleCheck className="text-primary shrink-0" /> {prerequisiteTitle}:
                              </strong>
                              <p className="leading-relaxed text-slate-600 pl-5">
                                {prerequisiteOverview}
                              </p>
                            </div>
                          )}
                        </div>

                        {/* Bottom Action Buttons */}
                        <div className="pt-6 border-t border-slate-200 flex flex-col sm:flex-row items-center gap-4">
                          <a
                            href="#admissions"
                            className="w-full sm:w-auto bg-primary hover:bg-primary-hover text-white font-bold px-8 py-3.5 rounded-xl shadow-lg shadow-primary/20 text-center text-sm transition-all flex items-center justify-center gap-2"
                          >
                            {card.apply_button_text || `Apply For ${card.heading}`} <FaArrowRight className="text-xs" />
                          </a>
                          <a
                            href="#eligibility-calculator"
                            className="w-full sm:w-auto bg-white border border-slate-300 hover:border-secondary text-secondary font-semibold px-6 py-3.5 rounded-xl text-center text-sm transition-all flex items-center justify-center gap-2"
                          >
                            <FaCalculator className="text-primary" /> {card.eligibility_button_text || "Check Your Eligibility"}
                          </a>
                          <Link
                            href={targetSyllabusUrl}
                            className="w-full sm:w-auto text-primary font-bold text-xs hover:underline text-center sm:ml-auto"
                          >
                            {card.syllabus_button_text || "View Full Syllabus"} <FaChevronRight className="inline text-[10px]" />
                          </Link>
                        </div>

                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              standardProgramItems.length > 0 && (
                <div className="space-y-12">
                  {standardProgramItems.map((prog) => {
                    const bannerImg = prog.program_banner?.image || resolveMediaUrl(prog.icon_image) || "/assets/banner1.jpg";
                    const aboutProg = prog.about_programs || {};
                    const featurePills = Array.isArray(aboutProg.features) ? aboutProg.features : [];
                    const entryReq = prog.entry_requirements || {};
                    const entryItems = Array.isArray(entryReq.items) ? entryReq.items : [];

                    const summaryPoints = Array.isArray(prog.program_summary) ? prog.program_summary : [];
                    const summaryText = summaryPoints.length > 0
                      ? summaryPoints.map(s => `${s.value} ${s.sub_text || s.title}`).join(" | ")
                      : "4 Years | 8 Semesters | 126 Credit Hours";

                    const charterBadgeTag = aboutProg.charter_badge_tag || aboutProg.charter_badge_title || "Affiliated Degree";
                    const specializationsTitle = aboutProg.title || "Core Technical Specializations";
                    const narrativeCopy = aboutProg.content || prog.sub_content || "";
                    const prerequisiteTitle = entryReq.title || "Entry Prerequisites (+2 Science)";
                    const prerequisiteOverview = entryReq.content || (entryItems.length > 0 ? entryItems.map(i => i.content).join(" - ") : "");

                    return (
                      <div
                        key={prog.id}
                        className="bg-surface rounded-3xl border border-slate-200 overflow-hidden shadow-xl grid grid-cols-1 lg:grid-cols-12 gap-0"
                      >
                        <div className="lg:col-span-5 relative min-h-[320px] lg:min-h-full">
                          <img
                            src={bannerImg}
                            alt={prog.heading || "Program Image"}
                            className="w-full h-full object-cover"
                          />
                          <div className="absolute inset-0 bg-gradient-to-t from-secondary/90 via-secondary/40 to-transparent" />

                          <div className="absolute bottom-6 left-6 right-6 text-white space-y-2 z-10">
                            {charterBadgeTag && (
                              <span className="bg-primary text-white text-xs font-extrabold px-3 py-1 rounded-full uppercase tracking-wider inline-block">
                                {charterBadgeTag}
                              </span>
                            )}
                            <h3 className="font-display font-bold text-2xl">
                              {prog.heading}
                            </h3>
                            <p className="text-xs text-slate-300">
                              {summaryText}
                            </p>
                          </div>
                        </div>

                        <div className="lg:col-span-7 p-8 sm:p-12 space-y-6 flex flex-col justify-between">
                          <div className="space-y-4">
                            <div className="flex items-center justify-between flex-wrap gap-2">
                              <span className="text-xs font-extrabold text-primary uppercase tracking-wider bg-primary/10 px-3 py-1 rounded-full">
                                Now Accepting Applications
                              </span>
                              <span className="text-xs font-bold text-slate-400">Inaugural Cohort</span>
                            </div>

                            <h4 className="font-display font-bold text-2xl text-secondary">
                              {specializationsTitle}
                            </h4>

                            {narrativeCopy && (
                              <p className="text-slate-600 text-sm leading-relaxed">
                                {narrativeCopy}
                              </p>
                            )}

                            {featurePills.length > 0 && (
                              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                                {featurePills.map((feat, fIdx) => (
                                  <div
                                    key={feat.id || fIdx}
                                    className="p-3 bg-white rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 flex items-center gap-2 shadow-sm"
                                  >
                                    <span className="text-primary text-sm shrink-0">
                                      {renderDynamicIcon(feat.icon_class, <FaCode />)}
                                    </span>
                                    <span>{feat.title}</span>
                                  </div>
                                ))}
                              </div>
                            )}

                            {prerequisiteOverview && (
                              <div className="p-4 bg-primary/5 rounded-xl border border-primary/20 text-xs text-slate-700 space-y-1 mt-4">
                                <strong className="text-primary block font-bold flex items-center gap-1.5">
                                  <FaCircleCheck className="text-primary shrink-0" /> {prerequisiteTitle}:
                                </strong>
                                <p className="leading-relaxed text-slate-600 pl-5">
                                  {prerequisiteOverview}
                                </p>
                              </div>
                            )}
                          </div>

                          <div className="pt-6 border-t border-slate-200 flex flex-col sm:flex-row items-center gap-4">
                            <a
                              href="#admissions"
                              className="w-full sm:w-auto bg-primary hover:bg-primary-hover text-white font-bold px-8 py-3.5 rounded-xl shadow-lg shadow-primary/20 text-center text-sm transition-all flex items-center justify-center gap-2"
                            >
                              Apply For {prog.heading} <FaArrowRight className="text-xs" />
                            </a>
                            <a
                              href="#eligibility-calculator"
                              className="w-full sm:w-auto bg-white border border-slate-300 hover:border-secondary text-secondary font-semibold px-6 py-3.5 rounded-xl text-center text-sm transition-all flex items-center justify-center gap-2"
                            >
                              <FaCalculator className="text-primary" /> Check Your Eligibility
                            </a>
                            <Link
                              href={`/programs/${prog.id}`}
                              className="w-full sm:w-auto text-primary font-bold text-xs hover:underline text-center sm:ml-auto"
                            >
                              View Full Syllabus <FaChevronRight className="inline text-[10px]" />
                            </Link>
                          </div>

                        </div>
                      </div>
                    );
                  })}
                </div>
              )
            )}

          </div>
        </section>
      )}

    </div>
  );
}