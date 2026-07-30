"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Spin } from "antd";
import {
  FaPhone,
  FaEnvelope,
  FaGraduationCap,
  FaChevronDown,
  FaChevronRight,
  FaEye,
  FaBullseye,
  FaRocket,
  FaCheck,
  FaLightbulb,
  FaCertificate,
  FaChalkboardUser,
  FaPeopleGroup,
  FaBookBookmark,
  FaIcons,
  FaAward,
  FaHandshake,
  FaShieldHalved,
  FaLaptopCode,
  FaGem,
  FaScaleBalanced,
  FaHeart,
  FaStar,
  FaCompass,
  FaUsers,
  FaBriefcase
} from "react-icons/fa6";

import JsonLd from "@/components/seo/JsonLd";
import { getAboutContent } from "@/lib/api/about";
import { resolveMediaUrl } from "@/lib/api/home";

const getInitials = (fullName) => {
  if (!fullName || typeof fullName !== "string") return "AI";
  const parts = fullName.trim().split(/\s+/);
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
};

const renderDynamicIcon = (iconClass, fallback = <FaLightbulb />) => {
  if (!iconClass || typeof iconClass !== "string") return fallback;

  const normalized = iconClass.toLowerCase().trim();

  if (
    normalized.includes("users") ||
    normalized.includes("user") ||
    normalized.includes("people") ||
    normalized.includes("faculty") ||
    normalized.includes("group")
  ) {
    return <FaUsers />;
  }
  if (
    normalized.includes("briefcase") ||
    normalized.includes("work") ||
    normalized.includes("career") ||
    normalized.includes("job") ||
    normalized.includes("suitcase")
  ) {
    return <FaBriefcase />;
  }
  if (
    normalized.includes("code") ||
    normalized.includes("laptop") ||
    normalized.includes("terminal") ||
    normalized.includes("computer")
  ) {
    return <FaLaptopCode />;
  }
  if (
    normalized.includes("award") ||
    normalized.includes("trophy") ||
    normalized.includes("medal") ||
    normalized.includes("certificate")
  ) {
    return <FaAward />;
  }
  if (normalized.includes("handshake") || normalized.includes("integrity")) {
    return <FaHandshake />;
  }
  if (normalized.includes("lightbulb") || normalized.includes("idea") || normalized.includes("innovation")) {
    return <FaLightbulb />;
  }
  if (
    normalized.includes("graduation") ||
    normalized.includes("cap") ||
    normalized.includes("education") ||
    normalized.includes("student")
  ) {
    return <FaGraduationCap />;
  }
  if (normalized.includes("shield") || normalized.includes("security")) {
    return <FaShieldHalved />;
  }
  if (normalized.includes("scale") || normalized.includes("balance")) {
    return <FaScaleBalanced />;
  }
  if (normalized.includes("gem") || normalized.includes("diamond")) {
    return <FaGem />;
  }
  if (normalized.includes("heart")) {
    return <FaHeart />;
  }
  if (normalized.includes("star")) {
    return <FaStar />;
  }
  if (normalized.includes("compass")) {
    return <FaCompass />;
  }
  if (normalized.includes("eye")) {
    return <FaEye />;
  }
  if (normalized.includes("bullseye") || normalized.includes("target")) {
    return <FaBullseye />;
  }
  if (normalized.includes("rocket")) {
    return <FaRocket />;
  }
  if (normalized.includes("book")) {
    return <FaBookBookmark />;
  }
  if (normalized.includes("chalkboard")) {
    return <FaChalkboardUser />;
  }

  return fallback;
};

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
      { threshold: 0.4 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [targetValue, duration]);

  return <span ref={elementRef}>{count}</span>;
};

export default function AboutUsPage() {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    const fetchPagePayload = async () => {
      try {
        setLoading(true);
        const data = await getAboutContent();
        if (active) {
          setContent(data);
        }
      } catch (err) {
        console.error("Error retrieving About Us payload:", err);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    fetchPagePayload();
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-surface">
        <Spin size="large" />
        <p className="mt-4 text-slate-600 font-medium text-sm">Loading About Us Content...</p>
      </div>
    );
  }

  const topBanner = content?.top_banner || {};
  const aboutBanner = content?.about_banner || {};
  const visionSec = content?.about_vision || {};
  const coreValues = content?.core_values || {};
  const metricsList = Array.isArray(content?.metrics) ? content.metrics : [];
  const leadershipSec = content?.leadership || {};
  const campusSec = content?.campus_facilities || {};
  const researchSec = content?.vision_research || {};
  const achievementSec = content?.achievements || {};
  const learnMore = content?.learn_more_contact || {};

  const topBannerImage = resolveMediaUrl(topBanner.image);
  const aboutMainImage = resolveMediaUrl(aboutBanner.main_image);

  return (
    <div className="bg-surface text-slate-800 font-sans antialiased selection:bg-primary selection:text-white overflow-x-hidden scroll-smooth">
      <JsonLd type="college" data={content} />

      {/* Hero Banner Section */}
      {topBanner.heading && (
        <section className="relative min-h-[65vh] flex items-center justify-center bg-secondary overflow-hidden py-24">
          {topBannerImage && (
            <div className="absolute inset-0 z-0">
              <img
                src={topBannerImage}
                alt={topBanner.heading}
                className="w-full h-full object-cover object-center select-none"
              />
              <div className="absolute inset-0 hero-overlay" aria-hidden="true" />
            </div>
          )}

          <div className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              {topBanner.badge_text && (
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-dark text-accent text-xs md:text-sm font-semibold mb-6 border border-accent/30 shadow-lg">
                  <span className="w-2.5 h-2.5 rounded-full bg-primary animate-ping" />
                  {topBanner.badge_text}
                </div>
              )}
              
              <h1 className="font-display font-extrabold text-3xl sm:text-5xl md:text-6xl leading-tight tracking-tight max-w-4xl mx-auto">
                {topBanner.heading}
              </h1>
              
              {topBanner.sub_heading && (
                <p className="mt-6 text-base sm:text-xl text-slate-200 max-w-3xl mx-auto font-normal leading-relaxed">
                  {topBanner.sub_heading}
                </p>
              )}

              <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
                {topBanner.primary_btn_text && (
                  <a
                    href={topBanner.primary_btn_url || "#about-intro"}
                    className="w-full sm:w-auto bg-primary hover:bg-primary-hover text-white font-bold px-8 py-3.5 rounded-xl shadow-glow-primary transition-all flex items-center justify-center gap-2"
                  >
                    {topBanner.primary_btn_text} <FaChevronDown className="text-xs" />
                  </a>
                )}
                {topBanner.secondary_btn_text && (
                  <a
                    href={topBanner.secondary_btn_url || "#vision-mission"}
                    className="w-full sm:w-auto glass-dark hover:bg-white/10 text-white font-semibold px-8 py-3.5 rounded-xl border border-white/30 transition-all flex items-center justify-center gap-2"
                  >
                    {topBanner.secondary_btn_text}
                  </a>
                )}
              </div>
            </motion.div>
          </div>
        </section>
      )}

      {/* Manifesto Section */}
      {aboutBanner.heading && (
        <section id="about-intro" className="py-24 bg-surface scroll-mt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              
              <motion.div
                className="lg:col-span-6 relative"
                initial={{ opacity: 0, x: -50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
                viewport={{ once: true }}
              >
                {aboutMainImage && (
                  <div className="relative z-10 rounded-3xl overflow-hidden shadow-2xl border-4 border-white">
                    <img
                      src={aboutMainImage}
                      alt={aboutBanner.heading}
                      className="w-full h-[450px] object-cover"
                    />
                  </div>
                )}
                
                {aboutBanner.charter_badge_subtitle && (
                  <div className="absolute -bottom-8 -right-4 z-20 glass-card p-5 rounded-2xl shadow-ultra max-w-xs border-l-4 border-primary">
                    <div className="flex items-center gap-4">
                      <div className="w-14 h-14 rounded-2xl bg-secondary text-white flex items-center justify-center text-2xl font-black shrink-0 shadow-md">
                        <FaCertificate className="text-accent" />
                      </div>
                      <div>
                        {aboutBanner.charter_badge_title && (
                          <span className="text-[11px] font-extrabold text-primary uppercase tracking-wider block">
                            {aboutBanner.charter_badge_title}
                          </span>
                        )}
                        <h4 className="font-display font-extrabold text-secondary text-sm leading-snug">
                          {aboutBanner.charter_badge_subtitle}
                        </h4>
                        {aboutBanner.charter_badge_degree && (
                          <p className="text-[11px] text-slate-500 font-medium">
                            {aboutBanner.charter_badge_degree}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </motion.div>

              <motion.div
                className="lg:col-span-6 space-y-6"
                initial={{ opacity: 0, x: 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
                viewport={{ once: true }}
              >
                {aboutBanner.badge_text && (
                  <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-4 py-1.5 bg-primary/10 rounded-full inline-block">
                    {aboutBanner.badge_text}
                  </span>
                )}

                <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary leading-tight">
                  {aboutBanner.heading}
                </h2>

                {aboutBanner.content_paragraph_1 && (
                  <p className="text-slate-600 text-base leading-relaxed">
                    {aboutBanner.content_paragraph_1}
                  </p>
                )}

                {aboutBanner.content_paragraph_2 && (
                  <p className="text-slate-600 text-sm leading-relaxed">
                    {aboutBanner.content_paragraph_2}
                  </p>
                )}

                {Array.isArray(aboutBanner.differentiators) && aboutBanner.differentiators.length > 0 && (
                  <div className="space-y-3 pt-2">
                    {aboutBanner.differentiators.map((diff) => (
                      <div key={diff.id} className="p-4 bg-white rounded-2xl border border-slate-200/90 shadow-sm flex items-start gap-4">
                        <div className="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center text-lg font-bold shrink-0">
                          {renderDynamicIcon(diff.icon_class, <FaGraduationCap />)}
                        </div>
                        <div>
                          <h4 className="font-bold text-secondary text-sm">{diff.title}</h4>
                          <p className="text-xs text-slate-500">{diff.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                <div className="pt-4 flex items-center gap-6">
                  <a href="#vision-mission" className="bg-primary hover:bg-primary-hover text-white font-semibold px-7 py-3.5 rounded-xl shadow-lg transition-all text-sm">
                    Explore Strategic Goals
                  </a>
                  <a href="#contact" className="text-secondary font-bold text-sm hover:underline flex items-center gap-1.5">
                    Contact Academic Desk <FaChevronRight className="text-xs text-primary" />
                  </a>
                </div>
              </motion.div>

            </div>
          </div>
        </section>
      )}

      {/* Vision & Mission Section */}
      {visionSec.heading && (
        <section id="vision-mission" className="py-20 bg-white scroll-mt-20 border-t border-slate-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-16">
              {visionSec.badge_text && (
                <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3 py-1 bg-primary/10 rounded-full">
                  {visionSec.badge_text}
                </span>
              )}
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                {visionSec.heading}
              </h2>
              {visionSec.sub_heading && (
                <p className="text-slate-600 text-base mt-2">{visionSec.sub_heading}</p>
              )}
            </div>

            {Array.isArray(visionSec.items) && visionSec.items.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {visionSec.items.map((pillar, idx) => {
                  const getPillarIcon = (index) => {
                    if (index === 0) return <FaEye />;
                    if (index === 1) return <FaBullseye />;
                    return <FaRocket />;
                  };

                  return (
                    <motion.div
                      key={pillar.id || idx}
                      className={`bg-surface p-8 rounded-2xl border-l-8 ${pillar.border_color_class || 'border-primary'} shadow-lg hover:shadow-2xl transition-all duration-300 flex flex-col justify-between`}
                      whileHover={{ y: -6 }}
                    >
                      <div>
                        <div className="w-14 h-12 rounded-xl bg-primary/10 text-primary flex items-center justify-center text-2xl mb-6">
                          {renderDynamicIcon(pillar.icon_class, getPillarIcon(idx))}
                        </div>
                        <h3 className="font-display font-bold text-2xl text-secondary mb-3">{pillar.heading}</h3>
                        <p className="text-slate-600 text-sm leading-relaxed mb-4">{pillar.content}</p>
                      </div>
                      {Array.isArray(pillar.items) && pillar.items.length > 0 && (
                        <ul className="space-y-2 text-xs text-slate-500 font-medium border-t border-slate-200 pt-4 mt-4 list-none p-0">
                          {pillar.items.map((item) => (
                            <li key={item.id} className="flex items-center gap-2">
                              <FaCheck className="text-primary shrink-0" /> {item.content}
                            </li>
                          ))}
                        </ul>
                      )}
                    </motion.div>
                  );
                })}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Core Values Section */}
      {coreValues.heading && (
        <section className="py-20 bg-surface border-t border-slate-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="bg-white rounded-3xl p-8 md:p-12 shadow-ultra border border-slate-200/80">
              <div className="text-center max-w-2xl mx-auto mb-12">
                <div className="w-16 h-16 rounded-full bg-primary/10 text-primary text-3xl flex items-center justify-center mx-auto mb-4">
                  <FaLightbulb />
                </div>
                <h3 className="font-display font-bold text-3xl text-secondary">
                  {coreValues.heading}
                </h3>
                {coreValues.sub_heading && (
                  <p className="text-slate-600 text-sm mt-2">{coreValues.sub_heading}</p>
                )}
              </div>

              {Array.isArray(coreValues.items) && coreValues.items.length > 0 && (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {coreValues.items.map((val) => {
                    const resolvedValImage = val.image ? resolveMediaUrl(val.image) : null;
                    return (
                      <div key={val.id} className="p-6 bg-surface rounded-xl border border-slate-200 hover:border-primary hover:-translate-y-1.5 transition-all duration-300">
                        <div className="text-primary text-2xl mb-3">
                          {resolvedValImage ? (
                            <img src={resolvedValImage} alt={val.heading} className="w-8 h-8 object-contain" />
                          ) : (
                            renderDynamicIcon(val.icon_class, <FaLightbulb />)
                          )}
                        </div>
                        <strong className="text-secondary text-lg block mb-1">{val.heading}</strong>
                        <span className="text-slate-600 text-xs leading-relaxed block">{val.content}</span>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        </section>
      )}

      {/* Distinction Metrics */}
      {metricsList.length > 0 && (
        <section className="py-20 bg-secondary text-white relative overflow-hidden">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center divide-y sm:divide-y-0 sm:divide-x divide-white/10">
              {metricsList.map((m) => (
                <div key={m.id} className="p-4 pt-6 sm:pt-4">
                  <div className="font-display font-extrabold text-4xl lg:text-5xl text-primary flex justify-center items-center gap-0.5">
                    <span>{m.prefix}</span>
                    <AnimatedCounter targetValue={m.target_number} />
                    <span className="text-accent">{m.suffix}</span>
                  </div>
                  <div className="font-bold text-sm mt-2 text-white">{m.label}</div>
                  {m.sub_label && <p className="text-xs text-slate-300 mt-1">{m.sub_label}</p>}
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Leadership Directory */}
      {leadershipSec.heading && (
        <section id="leadership" className="py-20 bg-white scroll-mt-20 border-t border-slate-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-16">
              {leadershipSec.badge_text && (
                <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3.5 py-1.5 bg-primary/10 rounded-full inline-block">
                  {leadershipSec.badge_text}
                </span>
              )}
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                {leadershipSec.heading}
              </h2>
              {leadershipSec.sub_heading && (
                <p className="text-slate-600 text-base mt-2">{leadershipSec.sub_heading}</p>
              )}
            </div>

            {Array.isArray(leadershipSec.items) && leadershipSec.items.length > 0 && (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 xl:gap-8 items-stretch">
                {leadershipSec.items.map((leader) => {
                  const leaderPortrait = resolveMediaUrl(leader.image);
                  const initials = getInitials(leader.heading);

                  return (
                    <motion.div
                      key={leader.id || leader.heading}
                      className="bg-white p-6 sm:p-7 rounded-2xl border border-slate-200/90 shadow-md hover:shadow-xl hover:border-primary/40 transition-all duration-300 flex flex-col justify-between h-full group"
                      whileHover={{ y: -6 }}
                    >
                      <div className="flex flex-col items-center text-center flex-1">
                        
                        <div className="relative w-28 h-28 sm:w-32 sm:h-32 rounded-full overflow-hidden border-4 border-white shadow-md ring-4 ring-primary/10 mb-5 bg-gradient-to-br from-secondary/10 to-primary/10 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform duration-300">
                          {leaderPortrait ? (
                            <img
                              src={leaderPortrait}
                              alt={leader.heading}
                              className="w-full h-full object-cover object-top"
                            />
                          ) : (
                            <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-tr from-secondary to-primary text-white">
                              <span className="font-display font-extrabold text-2xl tracking-wider">
                                {initials}
                              </span>
                            </div>
                          )}
                        </div>

                        <h3 className="font-display font-bold text-lg sm:text-xl text-secondary leading-snug min-h-[2.75rem] flex items-center justify-center">
                          {leader.heading}
                        </h3>

                        <div className="mt-2 min-h-[2.25rem] flex items-center justify-center">
                          <span className="text-[11px] font-extrabold uppercase tracking-wider text-primary px-3 py-1 bg-primary/10 rounded-full inline-block text-center leading-tight">
                            {leader.designation}
                          </span>
                        </div>

                        <p className="text-slate-600 text-xs sm:text-sm leading-relaxed mt-4 flex-1 text-center font-normal">
                          {leader.content}
                        </p>

                      </div>
                    </motion.div>
                  );
                })}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Learning Ecosystem Bento Grid */}
      {campusSec.heading && (
        <section id="environment-ecosystem" className="py-24 bg-surface scroll-mt-20 border-t border-slate-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-16">
              {campusSec.badge_text && (
                <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3.5 py-1.5 bg-primary/10 rounded-full">
                  {campusSec.badge_text}
                </span>
              )}
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                {campusSec.heading}
              </h2>
              {campusSec.sub_heading && (
                <p className="text-slate-600 text-base mt-2">{campusSec.sub_heading}</p>
              )}
            </div>

            {Array.isArray(campusSec.items) && campusSec.items.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
                {campusSec.items.map((item, idx) => {
                  const itemImg = resolveMediaUrl(item.image);
                  const getBentoIcon = (index) => {
                    if (index === 0) return <FaChalkboardUser />;
                    if (index === 1) return <FaPeopleGroup />;
                    if (index === 2) return <FaBookBookmark />;
                    return <FaIcons />;
                  };

                  return (
                    <div
                      key={item.id || idx}
                      className={`${item.bento_span_class || 'md:col-span-4'} bg-white rounded-3xl p-8 border border-slate-200 shadow-md hover:shadow-xl transition-all duration-300 flex flex-col justify-between group overflow-hidden relative min-h-[280px]`}
                    >
                      {itemImg && (
                        <div className="absolute inset-0 z-0 opacity-15 group-hover:scale-105 transition-transform duration-500">
                          <img src={itemImg} alt={item.title} className="w-full h-full object-cover" />
                        </div>
                      )}
                      <div className="relative z-10">
                        <div className="w-12 h-12 rounded-2xl bg-primary text-white flex items-center justify-center text-xl font-bold mb-4 shadow-sm">
                          {renderDynamicIcon(item.icon_class, getBentoIcon(idx))}
                        </div>
                        {item.category_badge && (
                          <span className="text-xs font-extrabold text-primary uppercase tracking-wider block mb-1">{item.category_badge}</span>
                        )}
                        <h3 className="font-display font-bold text-2xl text-secondary">{item.title}</h3>
                        <p className="text-slate-600 text-sm leading-relaxed mt-2 max-w-xl">{item.description}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Research Section */}
      {researchSec.heading && (
        <section id="research-innovation" className="py-20 bg-white scroll-mt-20 border-t border-slate-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-12">
              {researchSec.badge_text && (
                <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3 py-1 bg-primary/10 rounded-full">
                  {researchSec.badge_text}
                </span>
              )}
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                {researchSec.heading}
              </h2>
            </div>

            {Array.isArray(researchSec.items) && researchSec.items.length > 0 && (
              <div className="space-y-6 max-w-4xl mx-auto">
                {researchSec.items.map((item) => (
                  <div key={item.id} className="bg-surface p-8 shadow-md rounded-2xl border-l-4 border-primary">
                    <h3 className="font-display font-semibold text-2xl text-secondary mb-2">{item.heading}</h3>
                    <p className="text-slate-700 text-base leading-relaxed">{item.content}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Achievements & Milestones Section */}
      {achievementSec.heading && (
        <section id="achievements" className="py-20 bg-surface scroll-mt-20 border-t border-slate-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-12">
              <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3.5 py-1.5 bg-primary/10 rounded-full inline-block">
                Milestones & Progress
              </span>
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                {achievementSec.heading}
              </h2>
            </div>

            {Array.isArray(achievementSec.items) && achievementSec.items.length > 0 && (
              <div className="space-y-6 max-w-4xl mx-auto">
                {achievementSec.items.map((item) => (
                  <div key={item.id || item.heading} className="bg-white p-8 shadow-md rounded-2xl border-l-4 border-primary border border-slate-200/80">
                    <h3 className="font-display font-bold text-2xl text-secondary mb-2">{item.heading}</h3>
                    <p className="text-slate-700 text-base leading-relaxed">{item.content}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Contact CTA */}
      {learnMore.heading && (
        <section id="contact" className="py-16 bg-secondary text-white relative overflow-hidden my-12 max-w-7xl mx-auto rounded-3xl shadow-ultra">
          <div className="relative z-10 max-w-4xl mx-auto px-6 text-center space-y-6">
            <h2 className="font-display font-extrabold text-3xl sm:text-4xl tracking-tight">
              {learnMore.heading}
            </h2>
            {learnMore.sub_heading && (
              <p className="text-lg text-slate-200 font-medium">{learnMore.sub_heading}</p>
            )}

            <div className="flex flex-wrap items-center justify-center gap-6 pt-2 text-sm sm:text-base font-semibold">
              {learnMore.mail_id && (
                <a href={`mailto:${learnMore.mail_id}`} className="flex items-center gap-2 hover:text-accent transition-colors underline">
                  <FaEnvelope className="text-primary" /> {learnMore.mail_id}
                </a>
              )}
              {learnMore.contact && (
                <a href={`tel:${learnMore.contact}`} className="flex items-center gap-2 hover:text-accent transition-colors underline">
                  <FaPhone className="text-primary" /> {learnMore.contact}
                </a>
              )}
            </div>

            {learnMore.button_text && (
              <div className="pt-4">
                <Link
                  href={learnMore.button_url || "/contact-us"}
                  className="inline-block bg-primary hover:bg-primary-hover text-white font-bold px-8 py-4 rounded-xl shadow-glow-primary transition-all text-sm uppercase tracking-wider"
                >
                  {learnMore.button_text}
                </Link>
              </div>
            )}
          </div>
        </section>
      )}
    </div>
  );
}