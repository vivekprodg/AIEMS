import React from "react";
import { FaPaperPlane, FaLaptopCode, FaBan, FaCertificate, FaChalkboardUser } from "react-icons/fa6";

export default function TrainingHero({ bannerData = {} }) {
  const heroImage = bannerData.image || "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1600&auto=format&fit=crop";

  return (
    <section className="relative min-h-[55vh] flex items-center justify-center bg-secondary overflow-hidden py-16 sm:py-20 px-4 sm:px-6 lg:px-8 text-white">
      {/* Background Media Asset with Brand Gradient Overlay */}
      <div className="absolute inset-0 z-0 select-none">
        <img
          src={heroImage}
          alt={bannerData.heading || "AIEMS IT Training"}
          className="w-full h-full object-cover object-center"
        />
        <div className="absolute inset-0 hero-overlay" aria-hidden="true" />
      </div>

      {/* Hero Content Block */}
      <div className="relative z-10 max-w-5xl mx-auto text-center space-y-4">
        {bannerData.badge_text && (
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass-dark text-accent text-xs font-semibold border border-accent/30 shadow-lg">
            <span className="w-2 h-2 rounded-full bg-primary animate-ping" />
            {bannerData.badge_text}
          </div>
        )}

        <h1 className="font-display font-extrabold text-3xl sm:text-5xl lg:text-6xl tracking-tight leading-tight max-w-4xl mx-auto">
          {bannerData.heading}
        </h1>

        {bannerData.sub_heading && (
          <p className="text-slate-200 text-sm sm:text-base md:text-lg max-w-3xl mx-auto font-normal leading-relaxed">
            {bannerData.sub_heading}
          </p>
        )}

        {/* 4 Feature Badges */}
        <div className="pt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-3xl mx-auto text-xs font-semibold text-slate-200">
          <div className="p-2.5 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center gap-2 backdrop-blur-sm">
            <FaBan className="text-accent" /> Zero Prerequisites
          </div>
          <div className="p-2.5 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center gap-2 backdrop-blur-sm">
            <FaLaptopCode className="text-primary" /> 100% Lab Sessions
          </div>
          <div className="p-2.5 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center gap-2 backdrop-blur-sm">
            <FaCertificate className="text-accent" /> AIEMS Certificate
          </div>
          <div className="p-2.5 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center gap-2 backdrop-blur-sm">
            <FaChalkboardUser className="text-primary" /> Industry Mentors
          </div>
        </div>

        {/* Scroll CTA Button */}
        <div className="pt-4">
          <a
            href={bannerData.primary_btn_url || "#trainingLeadForm"}
            className="inline-flex items-center gap-2 bg-primary hover:bg-primary-hover text-white font-display font-bold text-sm px-8 py-3.5 rounded-xl shadow-glow-primary hover:shadow-primary/50 transition-all cursor-pointer"
          >
            <FaPaperPlane className="text-xs" /> {bannerData.primary_btn_text || "Reserve Your Seat"}
          </a>
        </div>
      </div>
    </section>
  );
}