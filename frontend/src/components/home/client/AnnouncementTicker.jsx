"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { FaPhone, FaEnvelope, FaDownload, FaStar } from "react-icons/fa6";
import { usePWA } from "@/lib/pwa/register-sw";

/**
 * Deterministic route resolver.
 * Converts absolute local URLs into relative routes consistently across SSR and Client.
 */
function getRouteDetails(rawUrl) {
  if (!rawUrl) return { isExternal: false, path: "" };

  const str = rawUrl.trim();

  // 1. Direct relative or anchor links
  if (str.startsWith("/") || str.startsWith("#")) {
    return { isExternal: false, path: str };
  }

  const lower = str.toLowerCase();

  // 2. Localhost or domain matches
  const isLocalHost = 
    lower.startsWith("http://localhost") || 
    lower.startsWith("https://localhost") || 
    lower.startsWith("http://127.0.0.1") || 
    lower.startsWith("https://127.0.0.1");

  const isDomain = 
    lower.startsWith("http://aiems.edu.np") || 
    lower.startsWith("https://aiems.edu.np") || 
    lower.startsWith("http://api.aiems.edu.np") || 
    lower.startsWith("https://api.aiems.edu.np");

  if (isLocalHost || isDomain) {
    const path = str.replace(/^https?:\/\/[^\/]+/, "") || "/";
    return { isExternal: false, path };
  }

  // 3. Truly external third-party links
  if (str.startsWith("http://") || str.startsWith("https://")) {
    return { isExternal: true, path: str };
  }

  return { isExternal: false, path: str.startsWith("/") ? str : `/${str}` };
}

export default function AnnouncementTicker({ announcements = [], contactInfo = {}, siteSettings = {} }) {
  const { isInstallable, installApp } = usePWA();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const phone = contactInfo.contact || siteSettings.primary_phone || "";
  const email = contactInfo.mail_id || siteSettings.primary_email || "";

  const hasAnnouncements = Array.isArray(announcements) && announcements.length > 0;

  const renderTickerItem = (item, index, isLoop = false) => {
    const key = isLoop ? `loop-${item.id || index}` : `item-${item.id || index}`;
    const rawUrl = item.target_url ? item.target_url.trim() : "";

    const content = (
      <>
        <strong className="text-accent mr-1 font-bold">[{item.badge_label}]</strong>{" "}
        <span className={rawUrl ? "group-hover:underline" : ""}>
          {item.text_content}
        </span>
      </>
    );

    if (!rawUrl) {
      return (
        <span key={key} className="mr-12 inline-flex items-center text-white/90">
          {content}
        </span>
      );
    }

    const { isExternal, path } = getRouteDetails(rawUrl);

    if (isExternal) {
      return (
        <a
          key={key}
          href={path}
          target="_blank"
          rel="noopener noreferrer"
          suppressHydrationWarning
          className="mr-12 inline-flex items-center text-white/90 hover:text-white transition-colors cursor-pointer group"
          title={`Open ${item.text_content}`}
        >
          {content}
        </a>
      );
    }

    return (
      <Link
        key={key}
        href={path}
        suppressHydrationWarning
        className="mr-12 inline-flex items-center text-white/90 hover:text-white transition-colors cursor-pointer group"
        title={`Navigate to ${item.text_content}`}
      >
        {content}
      </Link>
    );
  };

  return (
    <div className="bg-secondary text-white text-xs md:text-sm py-2 px-4 border-b border-white/10 relative z-50">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-2">
        
        {/* Dynamic CMS Announcement Ticker */}
        <div className="flex items-center gap-3 overflow-hidden w-full md:w-2/3">
          {hasAnnouncements && (
            <span className="bg-primary text-white text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded-full shrink-0 tracking-wider flex items-center gap-1">
              <FaStar className="animate-pulse text-accent text-[10px]" /> Update
            </span>
          )}
          <div className="overflow-hidden whitespace-nowrap relative w-full">
            {hasAnnouncements ? (
              <div className="animate-ticker text-white/90">
                {announcements.map((item, idx) => renderTickerItem(item, idx, false))}
                {announcements.map((item, idx) => renderTickerItem(item, idx, true))}
              </div>
            ) : (
              <span className="text-slate-300 text-xs italic">
                Welcome to AIEMS Bardibas
              </span>
            )}
          </div>
        </div>

        {/* Dynamic Quick Contact & PWA Install Button */}
        <div className="hidden md:flex items-center gap-6 text-xs text-white/80 shrink-0">
          {phone && (
            <a href={`tel:${phone}`} className="hover:text-accent transition-colors flex items-center gap-1.5">
              <FaPhone className="text-primary" /> {phone}
            </a>
          )}
          {email && (
            <a href={`mailto:${email}`} className="hover:text-accent transition-colors flex items-center gap-1.5">
              <FaEnvelope className="text-primary" /> {email}
            </a>
          )}
          {mounted && isInstallable && (
            <button
              onClick={installApp}
              className="bg-accent/20 hover:bg-accent hover:text-secondary text-accent font-semibold px-2.5 py-1 rounded transition-all flex items-center gap-1 cursor-pointer"
            >
              <FaDownload /> Install App
            </button>
          )}
        </div>

      </div>
    </div>
  );
}