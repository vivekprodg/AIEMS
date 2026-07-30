"use client";

import React, { useState } from "react";
import Link from "next/link";
import { 
  FaChevronDown, 
  FaChevronRight,
  FaCircleCheck, 
  FaPhone, 
  FaEnvelope, 
  FaLocationDot,
  FaCalendarDay
} from "react-icons/fa6";
import EligibilityCalculator from "@/components/home/client/EligibilityCalculator";
import { submitCourseApplication, resolveMediaUrl } from "@/lib/api/home";

/**
 * ISO Date Formatter for News & Updates
 */
const formatDate = (isoDate) => {
  if (!isoDate) return "";
  try {
    const date = new Date(isoDate);
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    }).format(date);
  } catch (error) {
    return "";
  }
};

/**
 * HomeInteractive Component
 * Renders interactive components in exact requested section order:
 * 1. Eligibility Calculator (#eligibility-calculator) - Placed directly below Featured Program Showcase
 * 2. Campus Facilities / Tech Labs (#facilities)
 * 3. Online Admissions & Requirements (#admissions)
 * 4. Frequently Asked Questions Accordion (Limited to 4 items + "View All FAQs" CTA)
 * 5. Latest News & Updates (#news)
 * 6. Call to Action Banner (#contact)
 */
export default function HomeInteractive({ content = {} }) {
  const [activeFaq, setActiveFaq] = useState(null);
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const eligibilityConfig = content?.eligibility_config || {};
  const campusFacilitiesData = content?.campus_facilities || {};
  const admissionDetail = content?.admission_detail || {};
  const admissionContact = content?.admission_contact || {};
  const siteSettings = content?.site_settings || {};
  const faqCategories = Array.isArray(content?.faqs) ? content.faqs : [];
  const newsEvents = content?.news_events || {};

  const facilityItems = Array.isArray(campusFacilitiesData.items) ? campusFacilitiesData.items : [];
  const allFaqs = faqCategories.flatMap((cat) => (Array.isArray(cat.faq_items) ? cat.faq_items : []));
  const displayedFaqs = allFaqs.slice(0, 4); // Max 4 FAQs on Homepage
  const criteriaRules = Array.isArray(admissionDetail.items) ? admissionDetail.items : [];
  const newsItems = Array.isArray(newsEvents.items) ? newsEvents.items : [];

  const toggleFaq = (index) => {
    setActiveFaq(activeFaq === index ? null : index);
  };

  const handleAdmissionSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    const formEl = e.target;
    
    const payload = {
      name: formEl.fullName.value.trim(),
      gender: formEl.gender.value,
      contact: formEl.contact.value.trim(),
      email: formEl.email.value.trim(),
      institution: formEl.institution.value.trim(),
      message: formEl.message.value.trim(),
    };

    try {
      await submitCourseApplication(payload);
      setFormSubmitted(true);
      formEl.reset();
    } catch (err) {
      console.error("Course application submission error:", err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="w-full">
      
      {/* ============================================================================== */}
      {/* 1. INTERACTIVE EVALUATION: BSC. CSIT ELIGIBILITY CALCULATOR */}
      {/* ============================================================================== */}
      <EligibilityCalculator eligibilityConfig={eligibilityConfig} />

      {/* ============================================================================== */}
      {/* 2. CAMPUS FACILITIES / TECH LABS */}
      {/* ============================================================================== */}
      {facilityItems.length > 0 && (
        <section id="facilities" className="py-24 bg-white border-t border-slate-100 scroll-mt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-3xl mx-auto mb-12">
              <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3 py-1 bg-primary/10 rounded-full inline-block">
                Modern Setup
              </span>
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                {campusFacilitiesData.heading || "Our Technical Infrastructure"}
              </h2>
              {campusFacilitiesData.sub_heading && (
                <p className="text-slate-600 text-base mt-2">
                  {campusFacilitiesData.sub_heading}
                </p>
              )}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {facilityItems.map((fac) => {
                const facImg = resolveMediaUrl(fac.image);
                return (
                  <div key={fac.id} className="group relative rounded-2xl overflow-hidden shadow-md h-72">
                    {facImg && (
                      <img
                        src={facImg}
                        alt="Campus Facility"
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-secondary/90 via-secondary/30 to-transparent" />
                  </div>
                );
              })}
            </div>
          </div>
        </section>
      )}

      {/* ============================================================================== */}
      {/* 3. ONLINE ADMISSIONS & REQUIREMENTS SECTION */}
      {/* ============================================================================== */}
      <section id="admissions" className="py-24 bg-surface scroll-mt-20 border-t border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center max-w-3xl mx-auto mb-12">
            <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3.5 py-1.5 bg-primary/10 rounded-full inline-block">
              Online Admissions
            </span>
            <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
              {admissionDetail.heading || "Admission Requirements"}
            </h2>
            {admissionDetail.sub_heading && (
              <p className="text-slate-600 text-sm sm:text-base mt-2">
                {admissionDetail.sub_heading}
              </p>
            )}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            
            {/* Left Column: Admission Criteria Rules */}
            {criteriaRules.length > 0 && (
              <div className="lg:col-span-5 bg-white rounded-3xl shadow-ultra border border-slate-100 p-6 sm:p-8 space-y-5">
                <h3 className="font-display font-extrabold text-xl text-secondary border-b border-slate-100 pb-3 flex items-center gap-2">
                  <FaCircleCheck className="text-primary shrink-0" />
                  {admissionDetail.sub_content || "Eligibility Criteria"}
                </h3>
                
                <ul className="space-y-3.5 text-xs sm:text-sm text-slate-700 font-medium list-none p-0 m-0">
                  {criteriaRules.map((rule, idx) => (
                    <li key={rule.id || idx} className="flex items-start gap-3 p-3.5 bg-surface rounded-2xl border border-slate-200/70 shadow-sm">
                      <FaCircleCheck className="text-primary text-lg shrink-0 mt-0.5" />
                      <span className="leading-relaxed">{rule.content}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Right Column: Online Admission Form */}
            <div className={`${
              criteriaRules.length > 0 ? "lg:col-span-7" : "max-w-3xl mx-auto lg:col-span-12"
            } w-full bg-white rounded-3xl shadow-ultra border border-slate-100 p-6 sm:p-10`}>
              
              <div className="mb-6">
                <h3 className="font-display font-extrabold text-2xl text-secondary">
                  Apply Online
                </h3>
                <p className="text-slate-500 text-xs mt-1">
                  Fill out your details below to begin your enrollment.
                </p>
              </div>

              <form onSubmit={handleAdmissionSubmit} className="space-y-5">
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-secondary uppercase mb-2">Full Name *</label>
                    <input
                      name="fullName"
                      type="text"
                      placeholder="Enter your complete name"
                      className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:outline-none"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-secondary uppercase mb-2">Gender *</label>
                    <select
                      name="gender"
                      className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:outline-none"
                      required
                    >
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-secondary uppercase mb-2">Contact Number *</label>
                    <input
                      name="contact"
                      type="tel"
                      placeholder="Enter contact number"
                      className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:outline-none"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-secondary uppercase mb-2">Email Address *</label>
                    <input
                      name="email"
                      type="email"
                      placeholder="you@example.com"
                      className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:outline-none"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-secondary uppercase mb-2">School / College Name *</label>
                  <input
                    name="institution"
                    type="text"
                    placeholder="High school or +2 institution name"
                    className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:outline-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-secondary uppercase mb-2">Additional Notes / Inquiries</label>
                  <textarea
                    name="message"
                    rows="3"
                    placeholder="Any questions or notes..."
                    className="w-full bg-surface border border-slate-300 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:outline-none"
                  />
                </div>

                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full bg-primary hover:bg-primary-hover text-white font-bold py-4 rounded-xl shadow-lg shadow-primary/25 transition-all text-sm uppercase tracking-wider cursor-pointer"
                >
                  {submitting ? "Submitting..." : "Submit Application"}
                </button>

              </form>

              {formSubmitted && (
                <div className="mt-6 p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-center text-sm font-semibold flex items-center justify-center gap-2">
                  <FaCircleCheck className="text-primary text-xl" />
                  <span>Your application has been logged! Our admissions team will get back to you shortly.</span>
                </div>
              )}

            </div>

          </div>

        </div>
      </section>

      {/* ============================================================================== */}
      {/* 4. FAQ ACCORDION SECTION (LIMITED TO 4 ITEMS + SEE MORE BUTTON) */}
      {/* ============================================================================== */}
      {allFaqs.length > 0 && (
        <section className="py-24 bg-surface border-t border-slate-100">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <div className="text-center mb-12">
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                Frequently Asked Questions
              </h2>
            </div>

            <div className="space-y-4">
              {displayedFaqs.map((faq, idx) => (
                <div key={faq.id || idx} className="bg-white rounded-2xl border border-slate-200 overflow-hidden transition-all">
                  <button
                    onClick={() => toggleFaq(idx)}
                    className="w-full p-6 text-left font-display font-bold text-secondary text-base sm:text-lg flex justify-between items-center gap-4 focus:outline-none cursor-pointer"
                  >
                    <span>{faq.question}</span>
                    <FaChevronDown
                      className={`text-primary transition-transform duration-300 shrink-0 ${
                        activeFaq === idx ? "rotate-180" : ""
                      }`}
                    />
                  </button>
                  {activeFaq === idx && (
                    <div className="px-6 pb-6 text-slate-600 text-sm leading-relaxed border-t border-slate-100 pt-4">
                      {faq.answer}
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* View All FAQs CTA Button */}
            <div className="text-center mt-10">
              <Link
                href="/faqs"
                className="inline-flex items-center gap-2 bg-primary hover:bg-primary-hover text-white font-bold px-8 py-3.5 rounded-xl shadow-md hover:shadow-lg transition-all text-sm uppercase tracking-wider"
              >
                View All FAQs <FaChevronRight className="text-xs" />
              </Link>
            </div>

          </div>
        </section>
      )}

      {/* ============================================================================== */}
      {/* 5. LATEST NEWS & UPDATES SECTION */}
      {/* ============================================================================== */}
      {newsEvents.heading && newsItems.length > 0 && (
        <section id="news" className="py-24 bg-white border-t border-slate-100 scroll-mt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <div className="text-center max-w-3xl mx-auto mb-12">
              <span className="text-xs font-extrabold uppercase tracking-widest text-primary px-3.5 py-1.5 bg-primary/10 rounded-full inline-block">
                Latest Updates
              </span>
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-secondary mt-3">
                {newsEvents.heading}
              </h2>
              {newsEvents.sub_heading && (
                <p className="text-slate-600 text-base mt-2">{newsEvents.sub_heading}</p>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {newsItems.map((item) => (
                <article key={item.id} className="bg-surface rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                  <div className="bg-secondary text-white px-6 py-3 text-xs font-bold uppercase tracking-wider flex items-center justify-between">
                    <span className="flex items-center gap-1.5">
                      <FaCalendarDay className="text-accent" /> {formatDate(item.date)}
                    </span>
                  </div>
                  <div className="p-6 space-y-3">
                    <h3 className="font-display font-bold text-lg text-secondary">{item.heading}</h3>
                    <p className="text-slate-600 text-xs leading-relaxed">{item.content}</p>
                  </div>
                </article>
              ))}
            </div>

          </div>
        </section>
      )}

      {/* ============================================================================== */}
      {/* 6. CALL TO ACTION BANNER */}
      {/* ============================================================================== */}
      {(admissionContact.heading || siteSettings.primary_phone) && (
        <section id="contact" className="py-16 bg-secondary text-white relative overflow-hidden">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center space-y-6">
            <h2 className="font-display font-extrabold text-3xl sm:text-4xl">
              {admissionContact.heading || siteSettings.site_title}
            </h2>
            <p className="text-slate-300 text-base max-w-2xl mx-auto">
              {admissionContact.sub_heading || ""}
            </p>

            <div className="flex flex-wrap items-center justify-center gap-6 pt-4 text-sm font-semibold">
              {(admissionContact.contact || siteSettings.primary_phone) && (
                <a href={`tel:${admissionContact.contact || siteSettings.primary_phone}`} className="flex items-center gap-2 hover:text-accent transition-colors">
                  <FaPhone className="text-primary" /> {admissionContact.contact || siteSettings.primary_phone}
                </a>
              )}
              {(admissionContact.mail_id || siteSettings.primary_email) && (
                <a href={`mailto:${admissionContact.mail_id || siteSettings.primary_email}`} className="flex items-center gap-2 hover:text-accent transition-colors">
                  <FaEnvelope className="text-primary" /> {admissionContact.mail_id || siteSettings.primary_email}
                </a>
              )}
              {siteSettings.location_address && (
                <span className="flex items-center gap-2 text-slate-300">
                  <FaLocationDot className="text-primary" /> {siteSettings.location_address}
                </span>
              )}
            </div>

            <div className="pt-4">
              <Link href="/apply-now" className="inline-block bg-primary hover:bg-primary-hover text-white font-bold px-8 py-4 rounded-xl shadow-glow-primary transition-all">
                Apply Online Now
              </Link>
            </div>
          </div>
        </section>
      )}

    </div>
  );
}