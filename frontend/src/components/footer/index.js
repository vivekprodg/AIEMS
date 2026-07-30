"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { 
  FaFacebookF, 
  FaLinkedinIn, 
  FaInstagram, 
  FaPhone, 
  FaEnvelope, 
  FaLocationDot 
} from "react-icons/fa6";
import { resolveMediaUrl } from "@/lib/api/home";

const sanitizeDialerNumber = (phoneStr) => {
  if (!phoneStr) return "";
  return String(phoneStr).replace(/[^0-9+]/g, "");
};

/**
 * Footer Component
 * Renders brand logo, links, social platforms, and contact details dynamically from CMS context.
 */
export default function Footer({ contactInfo = {}, jobInfo = {}, footerConfig = {}, siteSettings = {} }) {
  const [imageError, setImageError] = useState(false);
  const currentYear = new Date().getFullYear();

  useEffect(() => {
    setImageError(false);
  }, [footerConfig?.logo, siteSettings?.logo]);

  // Resolve logo URL from site settings or footer configuration
  const cmsLogoUrl = siteSettings?.logo 
    ? resolveMediaUrl(siteSettings.logo) 
    : (footerConfig?.logo ? resolveMediaUrl(footerConfig.logo) : null);

  const logoSrc = (!imageError && cmsLogoUrl) ? cmsLogoUrl : "/logo.svg";

  const contactPhone = contactInfo?.contact || siteSettings?.primary_phone || jobInfo?.contact || "";
  const contactEmail = contactInfo?.mail_id || siteSettings?.primary_email || jobInfo?.mail_id || "";
  const contactAddress = siteSettings?.location_address || "";

  const brandingDescription = footerConfig?.branding_description || siteSettings?.site_title || "";

  const facebookUrl = footerConfig?.facebook_url || "";
  const linkedinUrl = footerConfig?.linkedin_url || "";
  const instagramUrl = footerConfig?.instagram_url || "";

  const dynamicLinks = Array.isArray(footerConfig?.footer_links) ? footerConfig.footer_links : [];

  // Filter links dynamically by category
  const navigationLinks = dynamicLinks.filter(
    (link) => !link.category || link.category === "navigation"
  );
  const academicsLinks = dynamicLinks.filter(
    (link) => link.category === "academics"
  );

  return (
    <footer className="bg-[#EEF2F6] text-slate-700 pt-16 pb-8 border-t border-slate-300/60 text-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10 pb-12 border-b border-slate-300">
        
        {/* Column 1: CMS Branding & Logo */}
        <div className="space-y-4">
          <Link href="/" className="inline-block group focus:outline-none">
            <img 
              src={logoSrc} 
              alt="AIEMS Institutional Logo" 
              onError={() => setImageError(true)}
              className="h-[120px] w-auto object-contain transition-transform duration-300 group-hover:scale-105"
            />
          </Link>

          {brandingDescription && (
            <p className="text-slate-600 text-sm leading-relaxed max-w-sm">
              {brandingDescription}
            </p>
          )}
        </div>

        {/* Column 2: Navigation Links */}
        <div className="space-y-4">
          <h4 className="text-emerald-600 font-bold text-base uppercase tracking-wider">
            Navigation
          </h4>
          <ul className="space-y-2.5 text-sm font-medium text-slate-600 list-none p-0 m-0">
            {navigationLinks.length > 0 ? (
              navigationLinks.map((link) => (
                <li key={link.id || link.url}>
                  <Link 
                    href={link.url || "#"} 
                    target={link.open_in_new_tab ? "_blank" : "_self"}
                    rel={link.open_in_new_tab ? "noopener noreferrer" : undefined}
                    className="hover:text-emerald-600 transition-colors"
                  >
                    {link.title}
                  </Link>
                </li>
              ))
            ) : (
              <>
                <li>
                  <Link href="/home" className="hover:text-emerald-600 transition-colors">
                    Home
                  </Link>
                </li>
                <li>
                  <Link href="/about-us" className="hover:text-emerald-600 transition-colors">
                    About AIEMS
                  </Link>
                </li>
                <li>
                  <Link href="/apply-now" className="hover:text-emerald-600 transition-colors">
                    Admissions
                  </Link>
                </li>
                <li>
                  <Link href="/faqs" className="hover:text-emerald-600 transition-colors">
                    FAQs
                  </Link>
                </li>
                <li>
                  <Link href="/contact-us" className="hover:text-emerald-600 transition-colors">
                    Contact Desk
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>

        {/* Column 3: Academic Pathways (Now 100% CMS-Driven) */}
        <div className="space-y-4">
          <h4 className="text-emerald-600 font-bold text-base uppercase tracking-wider">
            Academics
          </h4>
          <ul className="space-y-2.5 text-sm font-medium text-slate-600 list-none p-0 m-0">
            {academicsLinks.length > 0 ? (
              academicsLinks.map((link) => (
                <li key={link.id || link.url}>
                  <Link 
                    href={link.url || "#"} 
                    target={link.open_in_new_tab ? "_blank" : "_self"}
                    rel={link.open_in_new_tab ? "noopener noreferrer" : undefined}
                    className="hover:text-emerald-600 transition-colors"
                  >
                    {link.title}
                  </Link>
                </li>
              ))
            ) : (
              <>
                <li>
                  <Link href="/home#program" className="hover:text-emerald-600 transition-colors">
                    Academic Programs
                  </Link>
                </li>
                <li>
                  <Link href="/home#facilities" className="hover:text-emerald-600 transition-colors">
                    Campus Facilities
                  </Link>
                </li>
                <li>
                  <Link href="/home#eligibility-calculator" className="hover:text-emerald-600 transition-colors">
                    Eligibility Calculator
                  </Link>
                </li>
                <li>
                  <Link href="/about-us#leadership" className="hover:text-emerald-600 transition-colors">
                    Leadership Directory
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>

        {/* Column 4: Contact & Social Directories */}
        <div className="space-y-4">
          <h4 className="text-emerald-600 font-bold text-base uppercase tracking-wider">
            Connect With Us
          </h4>
          <div className="space-y-3 text-sm font-medium text-slate-600">
            {contactPhone && (
              <p className="flex items-center gap-2.5">
                <FaPhone className="text-emerald-600 text-base shrink-0" />
                <a 
                  href={`tel:${sanitizeDialerNumber(contactPhone)}`} 
                  className="hover:text-emerald-600 transition-colors"
                >
                  {contactPhone}
                </a>
              </p>
            )}
            {contactEmail && (
              <p className="flex items-center gap-2.5">
                <FaEnvelope className="text-emerald-600 text-base shrink-0" />
                <a 
                  href={`mailto:${contactEmail}`} 
                  className="hover:text-emerald-600 transition-colors break-all"
                >
                  {contactEmail}
                </a>
              </p>
            )}
            {contactAddress && (
              <p className="flex items-center gap-2.5">
                <FaLocationDot className="text-emerald-600 text-base shrink-0" />
                <span>{contactAddress}</span>
              </p>
            )}
          </div>

          <div className="flex gap-4 text-xl text-slate-600 pt-3">
            {facebookUrl && (
              <a 
                href={facebookUrl} 
                target="_blank" 
                rel="noopener noreferrer" 
                aria-label="Official Facebook Page" 
                className="hover:text-emerald-600 transition-colors"
              >
                <FaFacebookF />
              </a>
            )}
            {linkedinUrl && (
              <a 
                href={linkedinUrl} 
                target="_blank" 
                rel="noopener noreferrer" 
                aria-label="Official LinkedIn Page" 
                className="hover:text-emerald-600 transition-colors"
              >
                <FaLinkedinIn />
              </a>
            )}
            {instagramUrl && (
              <a 
                href={instagramUrl} 
                target="_blank" 
                rel="noopener noreferrer" 
                aria-label="Official Instagram Page" 
                className="hover:text-emerald-600 transition-colors"
              >
                <FaInstagram />
              </a>
            )}
          </div>
        </div>

      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
        <p>© {currentYear} {siteSettings?.site_title || "AIEMS Campus"}. All Rights Reserved.</p>
        <div className="flex gap-6">
          <Link href="/privacy-policy" className="hover:text-slate-800 transition-colors">
            Privacy Policy
          </Link>
          <Link href="/terms-and-conditions" className="hover:text-slate-800 transition-colors">
            Terms and Conditions
          </Link>
        </div>
      </div>
    </footer>
  );
}