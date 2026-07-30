"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  FaBars, 
  FaXmark, 
  FaHouse, 
  FaBuildingColumns, 
  FaLaptopCode, 
  FaUserGraduate, 
  FaMicrochip, 
  FaNewspaper, 
  FaAddressBook, 
  FaArrowRight, 
  FaCalculator,
  FaLink
} from "react-icons/fa6";
import AnnouncementTicker from "@/components/home/client/AnnouncementTicker";
import { resolveMediaUrl } from "@/lib/api/home";

/**
 * Dynamic Icon Resolver for CMS Navbar Icons
 */
const renderDynamicIcon = (iconClass, fallback = <FaLink className="w-5" />) => {
  if (!iconClass || typeof iconClass !== "string") return fallback;
  const cls = iconClass.toLowerCase().trim();

  if (cls.includes("house") || cls.includes("home")) return <FaHouse className="w-5" />;
  if (cls.includes("building") || cls.includes("university") || cls.includes("about")) return <FaBuildingColumns className="w-5" />;
  if (cls.includes("laptop") || cls.includes("code") || cls.includes("program")) return <FaLaptopCode className="w-5" />;
  if (cls.includes("graduate") || cls.includes("user") || cls.includes("admission") || cls.includes("apply")) return <FaUserGraduate className="w-5" />;
  if (cls.includes("microchip") || cls.includes("facility") || cls.includes("campus")) return <FaMicrochip className="w-5" />;
  if (cls.includes("newspaper") || cls.includes("faq") || cls.includes("question")) return <FaNewspaper className="w-5" />;
  if (cls.includes("address") || cls.includes("contact") || cls.includes("phone")) return <FaAddressBook className="w-5" />;
  if (cls.includes("calculator")) return <FaCalculator className="w-5" />;

  return fallback;
};

// Fallback navbar configuration in case CMS links are empty
const DEFAULT_NAVBAR_LINKS = [
  { id: "def-1", title: "Home", url: "/home", icon_class: "fa-solid fa-house", is_button: false },
  { id: "def-2", title: "About Us", url: "/about-us", icon_class: "fa-solid fa-building-columns", is_button: false },
  { id: "def-3", title: "Programs", url: "/home#program", icon_class: "fa-solid fa-laptop-code", is_button: false },
  { id: "def-4", title: "Admissions", url: "/apply-now", icon_class: "fa-solid fa-user-graduate", is_button: false },
  { id: "def-5", title: "Facilities", url: "/home#facilities", icon_class: "fa-solid fa-microchip", is_button: false },
  { id: "def-6", title: "FAQs", url: "/faqs", icon_class: "fa-solid fa-newspaper", is_button: false },
  { id: "def-7", title: "Contact", url: "/contact-us", icon_class: "fa-solid fa-address-book", is_button: false },
  { id: "def-8", title: "Check Eligibility", url: "/home#eligibility-calculator", icon_class: "fa-solid fa-calculator", is_button: true },
  { id: "def-9", title: "Apply Now", url: "/apply-now", icon_class: "fa-solid fa-user-graduate", is_button: true }
];

/**
 * Navbar Component
 * Fixed Topbar + Header globally pinned to top-0 across all pages, 100% CMS-Driven Dynamic Navigation & CTAs.
 */
export default function Navbar({ contactInfo = {}, footerConfig = {}, announcements = [], siteSettings = {} }) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [imageError, setImageError] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    setImageError(false);
  }, [footerConfig?.logo, siteSettings?.logo]);

  // Resolve logo from global site settings or footer config
  const cmsLogoUrl = siteSettings?.logo 
    ? resolveMediaUrl(siteSettings.logo) 
    : (footerConfig?.logo ? resolveMediaUrl(footerConfig.logo) : null);
    
  const logoSrc = (!imageError && cmsLogoUrl) ? cmsLogoUrl : "/logo.svg";

  const toggleDrawer = () => setDrawerOpen(!drawerOpen);
  const closeDrawer = () => setDrawerOpen(false);

  const contactPhone = contactInfo?.contact || siteSettings?.primary_phone || "";
  const isLinkActive = (path) => pathname === path;

  // Extract CMS Dynamic Navbar Links with fallback
  const rawCmsLinks = Array.isArray(siteSettings?.navbar_links) && siteSettings.navbar_links.length > 0
    ? siteSettings.navbar_links
    : DEFAULT_NAVBAR_LINKS;

  const standardNavLinks = rawCmsLinks.filter(item => !item.is_button);
  const ctaButtonLinks = rawCmsLinks.filter(item => item.is_button);

  return (
    <>
      {/* 
        UNIFIED FIXED STICKY TOPBAR + NAVBAR WRAPPER
        Using sticky top-0 z-50 guarantees both the topbar and main header remain permanently anchored to top-0 
        across all pages while the hero section and body content scroll underneath it.
      */}
      <div className="sticky top-0 z-50 shadow-md bg-white w-full">
        
        {/* Topbar Announcement Ticker */}
        <AnnouncementTicker 
          announcements={announcements} 
          contactInfo={contactInfo} 
          siteSettings={siteSettings} 
        />

        {/* Main Navigation Header */}
        <header className="glass-nav border-b border-slate-200/80 transition-all duration-300">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
            
            {/* Brand Logo Anchor */}
            <Link href="/" className="flex items-center group focus:outline-none my-auto shrink-0">
              <img 
                src={logoSrc} 
                alt={siteSettings?.site_title || "AIEMS Campus Logo"} 
                onError={() => setImageError(true)}
                className="h-[80px] w-auto object-contain transition-transform duration-300 group-hover:scale-105 shrink-0"
              />
            </Link>

            {/* Dynamic CMS Navigation Links (Desktop) */}
            <nav className="hidden lg:flex items-center gap-7 font-medium text-sm text-slate-700">
              {standardNavLinks.map((link) => (
                <Link
                  key={link.id || link.url}
                  href={link.url || "#"}
                  target={link.open_in_new_tab ? "_blank" : "_self"}
                  rel={link.open_in_new_tab ? "noopener noreferrer" : undefined}
                  className={`transition-colors ${
                    isLinkActive(link.url) ? "text-primary font-semibold" : "hover:text-primary"
                  }`}
                >
                  {link.title}
                </Link>
              ))}
            </nav>

            {/* Dynamic Action CTA Buttons (Desktop) */}
            <div className="hidden lg:flex items-center gap-4">
              {ctaButtonLinks.length > 0 ? (
                ctaButtonLinks.map((cta, idx) => {
                  const isPrimary = idx === ctaButtonLinks.length - 1;
                  if (isPrimary) {
                    return (
                      <Link
                        key={cta.id || cta.url}
                        href={cta.url || "/apply-now"}
                        target={cta.open_in_new_tab ? "_blank" : "_self"}
                        rel={cta.open_in_new_tab ? "noopener noreferrer" : undefined}
                        className="bg-primary hover:bg-primary-hover text-white font-semibold text-sm px-6 py-2.5 rounded-xl shadow-lg shadow-primary/20 hover:shadow-primary/40 hover:-translate-y-0.5 transition-all duration-200 flex items-center gap-2"
                      >
                        {cta.title} <FaArrowRight className="text-xs" />
                      </Link>
                    );
                  }
                  return (
                    <Link
                      key={cta.id || cta.url}
                      href={cta.url || "#"}
                      target={cta.open_in_new_tab ? "_blank" : "_self"}
                      rel={cta.open_in_new_tab ? "noopener noreferrer" : undefined}
                      className="text-xs font-bold text-secondary hover:text-primary transition-colors flex items-center gap-1.5"
                    >
                      {renderDynamicIcon(cta.icon_class, <FaCalculator className="text-primary" />)} {cta.title}
                    </Link>
                  );
                })
              ) : (
                <Link
                  href="/apply-now"
                  className="bg-primary hover:bg-primary-hover text-white font-semibold text-sm px-6 py-2.5 rounded-xl shadow-lg shadow-primary/20 hover:shadow-primary/40 hover:-translate-y-0.5 transition-all duration-200 flex items-center gap-2"
                >
                  Apply Now <FaArrowRight className="text-xs" />
                </Link>
              )}
            </div>

            {/* Mobile Drawer Trigger */}
            <button
              onClick={toggleDrawer}
              aria-label="Toggle Mobile Navigation"
              className="lg:hidden text-secondary hover:text-primary p-2 text-2xl focus:outline-none cursor-pointer"
            >
              <FaBars />
            </button>

          </div>
        </header>

      </div>

      {/* Mobile Navigation Drawer */}
      <div
        className={`fixed inset-0 bg-secondary/80 backdrop-blur-md z-50 transition-all duration-300 lg:hidden flex justify-end ${
          drawerOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
        }`}
        onClick={closeDrawer}
      >
        <div
          className={`bg-white w-4/5 max-w-sm h-full shadow-2xl p-6 flex flex-col justify-between overflow-y-auto transform transition-transform duration-300 ${
            drawerOpen ? "translate-x-0" : "translate-x-full"
          }`}
          onClick={(e) => e.stopPropagation()}
        >
          <div>
            <div className="flex items-center justify-between pb-6 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <img 
                  src={logoSrc} 
                  alt="AIEMS Logo" 
                  onError={() => setImageError(true)}
                  className="h-10 w-auto object-contain" 
                />
              </div>
              <button onClick={closeDrawer} className="text-slate-400 hover:text-slate-700 text-2xl cursor-pointer">
                <FaXmark />
              </button>
            </div>

            {/* Dynamic Mobile Nav Links */}
            <nav className="flex flex-col gap-4 mt-6 text-base font-semibold text-slate-700">
              {rawCmsLinks.map((link) => (
                <Link
                  key={link.id || link.url}
                  href={link.url || "#"}
                  onClick={closeDrawer}
                  target={link.open_in_new_tab ? "_blank" : "_self"}
                  rel={link.open_in_new_tab ? "noopener noreferrer" : undefined}
                  className={`mobile-link flex items-center gap-3 ${
                    isLinkActive(link.url) ? "text-primary font-bold" : "hover:text-primary"
                  }`}
                >
                  {renderDynamicIcon(link.icon_class)}
                  <span>{link.title}</span>
                </Link>
              ))}
            </nav>
          </div>

          <div className="pt-6 border-t border-slate-100 space-y-3">
            <Link
              href="/apply-now"
              onClick={closeDrawer}
              className="block w-full text-center bg-primary text-white font-bold py-3 rounded-xl shadow-lg"
            >
              Apply For Admission
            </Link>
            {contactPhone && (
              <div className="text-center text-xs text-slate-500 pt-2">
                Hotline: <a href={`tel:${contactPhone}`} className="text-primary font-bold">{contactPhone}</a>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}