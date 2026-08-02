"use client";

import React, { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  FaClock,
  FaAward,
  FaGraduationCap,
  FaUsers,
  FaBuildingColumns,
  FaCertificate,
  FaCode,
  FaShieldHalved,
  FaCircleCheck,
  FaChevronDown,
  FaChevronUp,
  FaSquareCheck,
  FaUserNinja,
  FaCloud,
  FaNetworkWired,
  FaLinux,
  FaBrain,
  FaDatabase,
  FaBuilding,
  FaEnvelope,
  FaPhone,
  FaPaperPlane,
  FaBookOpen,
  FaArrowRight,
  FaCalculator,
  FaStar,
  FaLaptopCode,
  FaChalkboardUser,
  FaMicrochip,
} from "react-icons/fa6";

const renderDynamicIcon = (iconClass, fallback = <FaCode />) => {
  if (!iconClass || typeof iconClass !== "string") return fallback;
  const cls = iconClass.toLowerCase().trim();

  if (cls.includes("clock")) return <FaClock />;
  if (cls.includes("award")) return <FaAward />;
  if (cls.includes("graduation") || cls.includes("cap")) return <FaGraduationCap />;
  if (cls.includes("users") || cls.includes("user")) return <FaUsers />;
  if (cls.includes("building-columns") || cls.includes("university")) return <FaBuildingColumns />;
  if (cls.includes("certificate")) return <FaCertificate />;
  if (cls.includes("shield")) return <FaShieldHalved />;
  if (cls.includes("user-ninja") || cls.includes("ninja")) return <FaUserNinja />;
  if (cls.includes("cloud")) return <FaCloud />;
  if (cls.includes("network")) return <FaNetworkWired />;
  if (cls.includes("linux")) return <FaLinux />;
  if (cls.includes("brain")) return <FaBrain />;
  if (cls.includes("database")) return <FaDatabase />;
  if (cls.includes("building")) return <FaBuilding />;
  if (cls.includes("envelope")) return <FaEnvelope />;
  if (cls.includes("phone")) return <FaPhone />;
  if (cls.includes("paper-plane")) return <FaPaperPlane />;
  if (cls.includes("book-open") || cls.includes("book")) return <FaBookOpen />;
  if (cls.includes("arrow-right")) return <FaArrowRight />;
  if (cls.includes("calculator")) return <FaCalculator />;
  if (cls.includes("star")) return <FaStar />;
  if (cls.includes("laptop")) return <FaLaptopCode />;
  if (cls.includes("chalkboard")) return <FaChalkboardUser />;
  if (cls.includes("microchip")) return <FaMicrochip />;
  if (cls.includes("code")) return <FaCode />;

  return fallback;
};

export default function ProgramInteractive({ program = {}, siteSettings = {}, contactInfo = {} }) {
  const [openSemesters, setOpenSemesters] = useState({ 0: true });
  const [selectedElectives, setSelectedElectives] = useState({});

  if (!program || !program.id) {
    return null;
  }

  const toggleAccordion = (index) => {
    setOpenSemesters((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const handleElectiveChoice = (electiveKey, optionValue) => {
    setSelectedElectives((prev) => ({
      ...prev,
      [electiveKey]: optionValue,
    }));
  };

  const bannerImage = program.program_banner?.image || "";
  const summaryMetrics = program.program_summary || [];
  const aboutSection = program.about_programs;
  const overviewFeatures = aboutSection?.features || [];
  const entryReq = program.entry_requirements;
  const eligibilityItems = entryReq?.items || [];
  const curriculumSemesters = program.course_details || [];
  const industryCerts = program.industry_certifications || [];
  const careerOutcomesData = program.career_outcomes;
  const careerRoles = careerOutcomesData?.child_outcomes || [];

  const primaryPhone = contactInfo.contact || siteSettings.primary_phone || "";
  const primaryEmail = contactInfo.mail_id || siteSettings.primary_email || "";

  return (
    <div className="w-full">
      {/* 1. HERO BANNER SECTION */}
      <section className="relative min-h-[50vh] flex items-center justify-center bg-secondary overflow-hidden py-20">
        {bannerImage && (
          <div className="absolute inset-0 z-0">
            <img
              src={bannerImage}
              alt={program.heading}
              className="w-full h-full object-cover object-center select-none"
            />
            <div className="absolute inset-0 hero-overlay" aria-hidden="true" />
          </div>
        )}

        <div className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            {program.program_title && (
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-dark text-accent text-xs md:text-sm font-semibold mb-6 border border-accent/30 shadow-lg">
                <span className="w-2.5 h-2.5 rounded-full bg-primary animate-ping" />
                {program.program_title}
              </div>
            )}

            <h1 className="font-display font-extrabold text-3xl sm:text-5xl md:text-6xl leading-tight tracking-tight max-w-4xl mx-auto">
              {program.heading}
            </h1>

            {program.sub_content && (
              <p className="mt-6 text-base sm:text-xl text-slate-200 max-w-3xl mx-auto font-normal leading-relaxed">
                {program.sub_content}
              </p>
            )}

            <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/apply-now"
                className="w-full sm:w-auto bg-primary hover:bg-primary-hover text-white font-bold px-8 py-3.5 rounded-xl shadow-glow-primary transition-all flex items-center justify-center gap-2"
              >
                Apply For Entrance <FaPaperPlane className="text-xs" />
              </Link>
              {curriculumSemesters.length > 0 && (
                <a
                  href="#curriculum"
                  className="w-full sm:w-auto glass-dark hover:bg-white/10 text-white font-semibold px-8 py-3.5 rounded-xl border border-white/30 transition-all flex items-center justify-center gap-2"
                >
                  View Syllabus & Electives <FaBookOpen className="text-xs" />
                </a>
              )}
            </div>
          </motion.div>
        </div>
      </section>

      {/* 2. PROGRAM SUMMARY METRICS GRID */}
      {summaryMetrics.length > 0 && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-12 relative z-20">
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {summaryMetrics.map((metric, idx) => (
              <motion.div
                key={metric.id || idx}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.05, duration: 0.5 }}
                className="bg-white p-5 rounded-2xl shadow-xl border border-slate-200/90 hover:border-primary transition-all"
              >
                <div className="text-xs font-bold uppercase tracking-wider text-primary flex items-center gap-2">
                  {metric.icon_image ? (
                    <img src={metric.icon_image} alt={metric.title} className="w-5 h-5 object-contain" />
                  ) : (
                    <span className="text-base">{renderDynamicIcon(metric.icon_class, <FaClock />)}</span>
                  )}
                  {metric.title}
                </div>
                <div className="mt-2 text-lg font-extrabold text-secondary">{metric.value}</div>
                {metric.sub_text && (
                  <span className="text-[11px] text-slate-500 font-medium block">{metric.sub_text}</span>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* 3. PROGRAM OVERVIEW SECTION */}
      {aboutSection && (aboutSection.title || aboutSection.content) && (
        <section className="py-24 bg-surface scroll-mt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              <motion.div
                className="lg:col-span-7 space-y-6"
                initial={{ opacity: 0, x: -30 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
                viewport={{ once: true }}
              >
                {aboutSection.small_title && (
                  <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-4 py-1.5 bg-primary/10 rounded-full inline-block">
                    {aboutSection.small_title}
                  </span>
                )}

                {aboutSection.title && (
                  <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary leading-tight">
                    {aboutSection.title}
                  </h2>
                )}

                {aboutSection.content && (
                  <p className="text-slate-600 text-base leading-relaxed">{aboutSection.content}</p>
                )}

                {aboutSection.content_paragraph_2 && (
                  <p className="text-slate-600 text-sm leading-relaxed">
                    {aboutSection.content_paragraph_2}
                  </p>
                )}

                {overviewFeatures.length > 0 && (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                    {overviewFeatures.map((feat, idx) => (
                      <div
                        key={feat.id || idx}
                        className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm flex items-start gap-4"
                      >
                        <div className="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center text-lg font-bold shrink-0">
                          {renderDynamicIcon(feat.icon_class, <FaCode />)}
                        </div>
                        <div>
                          <h4 className="font-bold text-secondary text-sm">{feat.title}</h4>
                          {feat.description && (
                            <p className="text-xs text-slate-500 mt-0.5">{feat.description}</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </motion.div>

              {aboutSection.image && (
                <motion.div
                  className="lg:col-span-5 relative"
                  initial={{ opacity: 0, x: 30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6 }}
                  viewport={{ once: true }}
                >
                  <div className="relative z-10 rounded-3xl overflow-hidden shadow-2xl border-4 border-white">
                    <img
                      src={aboutSection.image}
                      alt={aboutSection.title || program.heading}
                      className="w-full h-[420px] object-cover"
                    />
                  </div>

                  {aboutSection.charter_badge_title && (
                    <div className="absolute -bottom-6 -left-6 z-20 glass-card p-5 rounded-2xl shadow-ultra max-w-xs border-l-4 border-primary">
                      <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-xl bg-secondary text-white flex items-center justify-center text-xl font-bold shrink-0">
                          <FaCertificate className="text-accent" />
                        </div>
                        <div>
                          {aboutSection.charter_badge_tag && (
                            <span className="text-[10px] font-extrabold text-primary uppercase tracking-wider block">
                              {aboutSection.charter_badge_tag}
                            </span>
                          )}
                          <h4 className="font-display font-extrabold text-secondary text-sm">
                            {aboutSection.charter_badge_title}
                          </h4>
                          {aboutSection.charter_badge_subtext && (
                            <p className="text-[11px] text-slate-500 font-medium">
                              {aboutSection.charter_badge_subtext}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </motion.div>
              )}
            </div>
          </div>
        </section>
      )}

      {/* 4. ENTRANCE ELIGIBILITY SECTION */}
      {entryReq && (entryReq.title || eligibilityItems.length > 0) && (
        <section id="eligibility" className="py-16 bg-white border-t border-b border-slate-100 scroll-mt-20">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="bg-gradient-to-br from-emerald-50 via-white to-sky-50 rounded-3xl p-8 md:p-12 shadow-xl border border-emerald-100 relative overflow-hidden">
              <div className="text-center max-w-3xl mx-auto space-y-4">
                <div className="w-16 h-16 rounded-2xl bg-primary text-white flex items-center justify-center text-3xl mx-auto shadow-md">
                  {entryReq.icon ? (
                    <img src={entryReq.icon} alt="Requirement" className="w-8 h-8 object-contain" />
                  ) : (
                    renderDynamicIcon(entryReq.icon_class, <FaGraduationCap />)
                  )}
                </div>

                {entryReq.title && (
                  <h2 className="font-display font-extrabold text-3xl text-secondary">
                    {entryReq.title}
                  </h2>
                )}

                {entryReq.content && (
                  <p className="text-slate-700 text-sm sm:text-base leading-relaxed">
                    {entryReq.content}
                  </p>
                )}

                {eligibilityItems.length > 0 && (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-left pt-4">
                    {eligibilityItems.map((item, idx) => (
                      <div
                        key={item.id || idx}
                        className="p-4 bg-white/80 rounded-xl border border-emerald-200/60 flex items-start gap-3"
                      >
                        <FaCircleCheck className="text-primary text-lg mt-0.5 shrink-0" />
                        <span className="text-xs sm:text-sm text-slate-700 font-medium leading-relaxed">
                          {item.content || item}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* 5. CURRICULUM ACCORDION & STRUCTURED ELECTIVES STREAM */}
      {curriculumSemesters.length > 0 && (
        <section id="curriculum" className="py-24 bg-surface scroll-mt-20">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-12">
              <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-4 py-1.5 bg-primary/10 rounded-full inline-block">
                Semester Curriculum & Electives
              </span>
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                Detailed Course Structure
              </h2>
            </div>

            <div className="space-y-4">
              {curriculumSemesters.map((sem, sIdx) => {
                const isOpen = !!openSemesters[sIdx];
                const semesterNum = sem.semester || sIdx + 1;
                const allCourses = Array.isArray(sem.courses) ? sem.courses : [];

                const coreCourses = allCourses.filter(
                  (c) => !c.is_elective && (!c.elective_options || c.elective_options.length === 0)
                );
                const electiveSubjects = allCourses.filter(
                  (c) => c.is_elective || (c.elective_options && c.elective_options.length > 0)
                );

                return (
                  <div
                    key={sem.id || sIdx}
                    className={`bg-white rounded-2xl overflow-hidden shadow-sm transition-all ${
                      electiveSubjects.length > 0
                        ? "border-2 border-primary/40 shadow-md"
                        : "border border-slate-200 hover:border-primary/50"
                    }`}
                  >
                    <button
                      onClick={() => toggleAccordion(sIdx)}
                      className={`w-full px-6 py-5 text-left flex justify-between items-center cursor-pointer focus:outline-none transition-colors ${
                        electiveSubjects.length > 0
                          ? "bg-emerald-50/40 hover:bg-emerald-50/80"
                          : "bg-slate-50/80 hover:bg-slate-100/80"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span
                          className={`w-8 h-8 rounded-lg font-extrabold text-sm flex items-center justify-center ${
                            electiveSubjects.length > 0
                              ? "bg-primary text-white"
                              : "bg-primary/10 text-primary"
                          }`}
                        >
                          S{semesterNum}
                        </span>
                        <div>
                          <div className="flex items-center gap-2 flex-wrap">
                            <h3 className="text-base sm:text-lg font-bold text-secondary">
                              {sem.title || `Semester ${semesterNum}`}
                            </h3>
                            {electiveSubjects.length > 0 && (
                              <span className="px-2.5 py-0.5 bg-primary text-white font-extrabold text-[10px] uppercase rounded-full tracking-wide">
                                Elective Stream Offered
                              </span>
                            )}
                          </div>
                          {sem.credit_summary_text && (
                            <p className="text-xs text-slate-500">{sem.credit_summary_text}</p>
                          )}
                        </div>
                      </div>

                      {isOpen ? (
                        <FaChevronUp className="text-primary transition-transform duration-300" />
                      ) : (
                        <FaChevronDown className="text-primary transition-transform duration-300" />
                      )}
                    </button>

                    <AnimatePresence initial={false}>
                      {isOpen && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.25, ease: "easeInOut" }}
                          className="overflow-hidden"
                        >
                          <div className="p-6 border-t border-slate-100 space-y-6">
                            {/* Core Courses Table */}
                            {coreCourses.length > 0 && (
                              <div>
                                {electiveSubjects.length > 0 && (
                                  <h4 className="font-bold text-secondary text-xs uppercase tracking-wider mb-3">
                                    Core Mandatory Courses ({coreCourses.length})
                                  </h4>
                                )}
                                <div className="overflow-x-auto">
                                  <table className="w-full text-left text-xs sm:text-sm text-slate-700 border-collapse">
                                    <thead>
                                      <tr className="border-b border-slate-200 text-secondary font-bold uppercase tracking-wider bg-slate-50">
                                        <th className="py-3 px-4">Course Name</th>
                                        <th className="py-3 px-4">Course Code</th>
                                        <th className="py-3 px-4">Credit Hours</th>
                                        <th className="py-3 px-4">Course Type</th>
                                      </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-100">
                                      {coreCourses.map((c, cIdx) => (
                                        <tr key={c.id || cIdx} className="hover:bg-emerald-50/30">
                                          <td className="py-3 px-4 font-semibold text-secondary">
                                            {c.course_name}
                                          </td>
                                          <td className="py-3 px-4 font-mono text-slate-500">
                                            {c.course_code}
                                          </td>
                                          <td className="py-3 px-4">
                                            {c.credit_hours ? `${c.credit_hours} Hrs` : "-"}
                                          </td>
                                          <td className="py-3 px-4">
                                            <span className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded font-semibold text-[11px]">
                                              {c.course_type || "Core"}
                                            </span>
                                          </td>
                                        </tr>
                                      ))}
                                    </tbody>
                                  </table>
                                </div>
                              </div>
                            )}

                            {/* Elective Subjects Block */}
                            {electiveSubjects.length > 0 && (
                              <div className="space-y-6">
                                {electiveSubjects.map((eleSub, eleIdx) => {
                                  const options = eleSub.elective_options || [];
                                  const electiveKey = `sem_${semesterNum}_subject_${eleSub.id || eleIdx}`;
                                  
                                  const defaultSelection = options.length > 0
                                    ? `${options[0].course_name} (${options[0].course_code})`
                                    : "";
                                  const activeChoice = selectedElectives[electiveKey] || defaultSelection;

                                  return (
                                    <div
                                      key={eleSub.id || eleIdx}
                                      className="p-5 bg-gradient-to-r from-secondary/5 via-white to-primary/5 rounded-2xl border border-primary/30 space-y-4"
                                    >
                                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-3">
                                        <div>
                                          <h4 className="font-display font-extrabold text-secondary text-sm flex items-center gap-2">
                                            <FaSquareCheck className="text-primary" />
                                            {eleSub.course_name} ({eleSub.course_code})
                                          </h4>
                                          <p className="text-xs text-slate-500 mt-0.5">
                                            Select 1 Elective Option {eleSub.credit_hours ? `(${eleSub.credit_hours} Credit Hours)` : ""}
                                          </p>
                                        </div>
                                        {activeChoice && (
                                          <span className="text-xs font-bold text-primary bg-white px-3.5 py-1.5 rounded-full border border-primary/30 shadow-sm self-start sm:self-auto">
                                            Active Selection: {activeChoice}
                                          </span>
                                        )}
                                      </div>

                                      {/* Render Structured Elective Options One by One */}
                                      {options.length > 0 ? (
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                          {options.map((opt, optIdx) => {
                                            const optionValue = `${opt.course_name} (${opt.course_code})`;
                                            const isChecked = activeChoice === optionValue;

                                            return (
                                              <label
                                                key={opt.id || optIdx}
                                                className={`p-4 bg-white rounded-xl border hover:border-primary cursor-pointer flex items-start gap-3.5 transition-all shadow-sm group ${
                                                  isChecked
                                                    ? "border-primary ring-1 ring-primary/30"
                                                    : "border-slate-200"
                                                }`}
                                              >
                                                <input
                                                  type="radio"
                                                  name={electiveKey}
                                                  value={opt.course_code}
                                                  checked={isChecked}
                                                  onChange={() =>
                                                    handleElectiveChoice(electiveKey, optionValue)
                                                  }
                                                  className="mt-1 accent-primary scale-125 cursor-pointer"
                                                />
                                                <div className="w-full">
                                                  <div className="flex items-center justify-between gap-2">
                                                    <strong className="text-xs sm:text-sm text-secondary block font-bold group-hover:text-primary transition-colors">
                                                      {opt.course_name}
                                                    </strong>
                                                    <span className="px-2 py-0.5 bg-slate-100 text-slate-600 font-mono text-[10px] rounded font-bold shrink-0">
                                                      {opt.course_code}
                                                    </span>
                                                  </div>
                                                  {opt.credit_hours && (
                                                    <span className="text-[11px] text-primary font-semibold block mt-0.5">
                                                      <FaAward className="inline mr-1" /> {opt.credit_hours} Credit Hours
                                                    </span>
                                                  )}
                                                  {opt.description && (
                                                    <p className="text-[11px] text-slate-600 mt-1.5 leading-relaxed">
                                                      {opt.description}
                                                    </p>
                                                  )}
                                                </div>
                                              </label>
                                            );
                                          })}
                                        </div>
                                      ) : eleSub.description ? (
                                        <p className="text-xs text-slate-600 leading-relaxed bg-white p-3.5 rounded-xl border border-slate-200">
                                          {eleSub.description}
                                        </p>
                                      ) : null}
                                    </div>
                                  );
                                })}
                              </div>
                            )}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                );
              })}
            </div>
          </div>
        </section>
      )}

      {/* 6. PARTNERED INDUSTRY CERTIFICATIONS */}
      {industryCerts.length > 0 && (
        <section className="py-20 bg-white border-t border-b border-slate-200/80">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-16">
              <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-4 py-1.5 bg-primary/10 rounded-full inline-block">
                Industry Certification Co-Tracks
              </span>
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                Partnered Professional Certifications
              </h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {industryCerts.map((cert, idx) => (
                <motion.div
                  key={cert.id || idx}
                  whileHover={{ y: -6 }}
                  className="p-6 bg-surface rounded-2xl border border-slate-200 hover:border-primary transition-all duration-300 shadow-sm flex flex-col justify-between group"
                >
                  <div>
                    <div className="w-14 h-14 rounded-2xl bg-secondary text-white flex items-center justify-center text-2xl font-black mb-5 shadow-md group-hover:bg-primary transition-colors">
                      {renderDynamicIcon(cert.icon_class, <FaCertificate className="text-accent" />)}
                    </div>

                    {cert.category_badge && (
                      <span
                        className={`text-[10px] font-extrabold uppercase tracking-wider px-2.5 py-1 rounded-full ${
                          cert.badge_color_class || "text-primary bg-primary/10"
                        }`}
                      >
                        {cert.category_badge}
                      </span>
                    )}

                    <h3 className="font-display font-extrabold text-xl text-secondary mt-3">
                      {cert.partner_name}
                    </h3>

                    {cert.description && (
                      <p className="text-slate-600 text-xs leading-relaxed mt-2">
                        {cert.description}
                      </p>
                    )}
                  </div>

                  {cert.track_label && (
                    <div className="pt-4 border-t border-slate-200/80 mt-6 flex items-center justify-between text-xs font-bold text-secondary">
                      <span>{cert.track_label}</span>
                      <FaArrowRight className="text-primary" />
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* 7. CAREER OUTCOMES SECTION */}
      {careerOutcomesData && (careerOutcomesData.title || careerRoles.length > 0) && (
        <section className="bg-secondary text-white py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-5xl mx-auto text-center space-y-8">
            <div>
              <span className="text-xs font-extrabold uppercase tracking-widest text-accent px-3.5 py-1 bg-white/10 rounded-full inline-block">
                Career Outlook
              </span>
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl mt-3">
                {careerOutcomesData.title || "Graduate Career Roles"}
              </h2>
              {careerOutcomesData.content && (
                <p className="text-slate-300 text-sm sm:text-base mt-2 max-w-2xl mx-auto">
                  {careerOutcomesData.content}
                </p>
              )}
            </div>

            {careerRoles.length > 0 && (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 text-left pt-4">
                {careerRoles.map((role, idx) => (
                  <div
                    key={role.id || idx}
                    className="p-5 bg-white/5 rounded-2xl border border-white/10 flex items-center gap-4 hover:bg-white/10 transition-colors"
                  >
                    <div className="w-12 h-12 rounded-xl bg-primary text-white flex items-center justify-center text-xl shrink-0 shadow-md overflow-hidden">
                      {role.icon_image ? (
                        <img src={role.icon_image} alt={role.title} className="w-7 h-7 object-contain" />
                      ) : (
                        renderDynamicIcon(role.icon_class, <FaCode />)
                      )}
                    </div>
                    <div>
                      <span className="font-bold text-sm text-slate-100 block">{role.title}</span>
                      {role.sub_title && (
                        <span className="text-xs text-slate-400 block mt-0.5">{role.sub_title}</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      )}

      {/* 8. CALL TO ACTION (CTA) SECTION */}
      <section id="apply" className="py-16 bg-secondary text-white relative overflow-hidden my-12 max-w-7xl mx-auto rounded-3xl shadow-ultra">
        <div className="relative z-10 max-w-4xl mx-auto px-6 text-center space-y-6">
          <h2 className="font-display font-extrabold text-3xl sm:text-4xl tracking-tight">
            Ready to Enroll in {program.heading}?
          </h2>

          <p className="text-lg text-slate-200 font-medium">
            Take the first step toward your technology degree at AIEMS. Applications are currently open.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-6 pt-2 text-sm sm:text-base font-semibold">
            {primaryEmail && (
              <a href={`mailto:${primaryEmail}`} className="flex items-center gap-2 hover:text-accent transition-colors underline">
                <FaEnvelope className="text-primary" /> {primaryEmail}
              </a>
            )}
            {primaryPhone && (
              <a href={`tel:${primaryPhone}`} className="flex items-center gap-2 hover:text-accent transition-colors underline">
                <FaPhone className="text-primary" /> {primaryPhone}
              </a>
            )}
          </div>

          <div className="pt-4 flex flex-wrap justify-center gap-4">
            <Link
              href="/apply-now"
              className="inline-block bg-primary hover:bg-primary-hover text-white font-bold px-8 py-4 rounded-xl shadow-glow-primary transition-all text-sm uppercase tracking-wider"
            >
              Apply For Entrance
            </Link>
            <Link
              href="/contact-us"
              className="inline-block glass-dark hover:bg-white/10 text-white font-semibold px-8 py-4 rounded-xl border border-white/30 transition-all text-sm uppercase tracking-wider"
            >
              Contact Counseling Desk
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}