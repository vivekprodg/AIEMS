import React from "react";
import {
  FaBrain,
  FaCode,
  FaGlobe,
  FaShieldHalved,
  FaNetworkWired,
  FaCloud,
  FaPhotoFilm,
  FaCheck,
  FaGift,
  FaPhone,
  FaEnvelope
} from "react-icons/fa6";

const renderDynamicIcon = (iconClass, fallback = <FaCode />) => {
  if (!iconClass || typeof iconClass !== "string") return fallback;
  const cls = iconClass.toLowerCase().trim();

  if (cls.includes("brain") || cls.includes("ai") || cls.includes("robot")) return <FaBrain />;
  if (cls.includes("code") || cls.includes("laptop")) return <FaCode />;
  if (cls.includes("globe") || cls.includes("web")) return <FaGlobe />;
  if (cls.includes("shield") || cls.includes("cyber") || cls.includes("security")) return <FaShieldHalved />;
  if (cls.includes("network") || cls.includes("wifi")) return <FaNetworkWired />;
  if (cls.includes("cloud")) return <FaCloud />;
  if (cls.includes("photo") || cls.includes("film") || cls.includes("media") || cls.includes("image")) return <FaPhotoFilm />;

  return fallback;
};

export default function TrainingSidebar({
  modulesList = [],
  perksList = [],
  contactInfo = {},
  siteSettings = {}
}) {
  const phone = contactInfo.contact || siteSettings.primary_phone || "9802113456";
  const email = contactInfo.mail_id || siteSettings.primary_email || "info@aiems.edu.np";

  return (
    <aside className="space-y-6">
      {/* 1. What You Will Learn Card */}
      <div className="bg-white rounded-3xl p-6 sm:p-7 border border-slate-200 shadow-ultra space-y-6">
        <div className="border-b border-slate-100 pb-4">
          <h3 className="font-display font-bold text-xl text-secondary">
            What You Will Learn
          </h3>
          <p className="text-xs text-slate-500 mt-1 leading-relaxed">
            Practical modules designed from the ground up for non-tech students.
          </p>
        </div>

        <div className="space-y-4 text-xs">
          {modulesList.map((item, idx) => (
            <div key={item.id || idx} className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center text-sm font-bold shrink-0 mt-0.5">
                {renderDynamicIcon(item.icon_class, <FaCode />)}
              </div>
              <div>
                <h4 className="font-bold text-secondary text-sm">{item.title}</h4>
                <p className="text-slate-500 mt-0.5 leading-relaxed">{item.description}</p>
              </div>
            </div>
          ))}
        </div>

        {/* 2. Training Perks Box */}
        {perksList.length > 0 && (
          <div className="p-4 bg-gradient-to-br from-secondary/5 to-primary/10 rounded-2xl border border-primary/20 space-y-2.5">
            <h5 className="font-display font-extrabold text-xs text-primary uppercase tracking-wider flex items-center gap-1.5">
              <FaGift /> Student Training Perks
            </h5>
            <ul className="space-y-1.5 text-xs text-slate-700 font-medium list-none p-0 m-0">
              {perksList.map((perk, idx) => (
                <li key={perk.id || idx} className="flex items-center gap-2">
                  <FaCheck className="text-primary text-[10px] shrink-0" />
                  <span>{perk.title}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* 3. Direct Counseling Contact Card */}
      <div className="bg-secondary text-white rounded-3xl p-6 border border-white/10 space-y-3 text-xs">
        <span className="text-accent font-extrabold uppercase tracking-widest text-[10px]">
          Direct Admissions Desk
        </span>
        <h4 className="font-display font-bold text-base text-white">Have questions before applying?</h4>
        <p className="text-slate-300 leading-relaxed">
          Our counselors are available daily at the campus reception in Bardibas to explain curriculum details and lab timings.
        </p>
        <div className="pt-2 space-y-2 font-semibold">
          {phone && (
            <a href={`tel:${phone}`} className="flex items-center gap-2 text-white hover:text-accent transition-colors">
              <FaPhone className="text-primary" /> {phone}
            </a>
          )}
          {email && (
            <a href={`mailto:${email}`} className="flex items-center gap-2 text-white hover:text-accent transition-colors break-all">
              <FaEnvelope className="text-primary" /> {email}
            </a>
          )}
        </div>
      </div>
    </aside>
  );
}