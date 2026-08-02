"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { FaXmark, FaArrowRight } from "react-icons/fa6";

/**
 * PopupBannerModal Component
 * Interactive, responsive popup modal for college announcements, notices, and flyers.
 * Dynamically shrink-wraps to fit the exact width & height of the uploaded image/banner
 * with zero awkward left/right or top/bottom whitespace for any aspect ratio.
 */
export default function PopupBannerModal({ popupData = {} }) {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (!popupData || !popupData.id || !popupData.image || popupData.is_active === false) {
      return;
    }

    // Dynamic session storage key incorporating banner ID to allow redisplay on new updates
    const storageKey = `aiems_popup_dismissed_${popupData.id}`;
    const isDismissed = typeof window !== "undefined" ? sessionStorage.getItem(storageKey) : null;

    if (!isDismissed) {
      const timer = setTimeout(() => {
        setIsOpen(true);
      }, 600);
      return () => clearTimeout(timer);
    }
  }, [popupData]);

  const handleClose = () => {
    setIsOpen(false);
    if (popupData?.id && typeof window !== "undefined") {
      const storageKey = `aiems_popup_dismissed_${popupData.id}`;
      sessionStorage.setItem(storageKey, "true");
    }
  };

  if (!popupData || !popupData.id || !popupData.image) {
    return null;
  }

  const rawUrl = popupData.action_url ? popupData.action_url.trim() : "";
  const isExternal = rawUrl.startsWith("http://") || rawUrl.startsWith("https://");

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
          {/* Backdrop Blur Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            onClick={handleClose}
            className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm cursor-pointer"
            aria-hidden="true"
          />

          {/* Modal Container: w-fit shrink-wraps around the exact image width */}
          <motion.div
            initial={{ opacity: 0, scale: 0.85, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="relative z-10 w-fit max-w-[92vw] max-h-[92vh] bg-white rounded-3xl p-4 sm:p-5 shadow-2xl border border-slate-200/90 overflow-hidden flex flex-col items-center justify-center my-auto"
            role="dialog"
            aria-modal="true"
            aria-labelledby="popup-banner-title"
          >
            {/* Close Button */}
            <button
              onClick={handleClose}
              aria-label="Close Announcement Popup"
              className="absolute top-2.5 right-2.5 sm:top-3.5 sm:right-3.5 z-30 bg-slate-900/80 hover:bg-primary text-white p-2 sm:p-2.5 rounded-full shadow-lg backdrop-blur-md transition-all duration-200 hover:scale-110 cursor-pointer focus:outline-none ring-2 ring-white/40"
            >
              <FaXmark className="text-sm sm:text-lg" />
            </button>

            {/* Scrollable Wrapper for Overflow Protection on Small Screens */}
            <div className="overflow-y-auto max-h-[85vh] w-full flex flex-col items-center justify-center scrollbar-none">
              
              {/* Optional Heading */}
              {popupData.heading && (
                <div className="text-center mb-3 pr-8 pl-2 max-w-full">
                  <h3 id="popup-banner-title" className="font-display font-extrabold text-lg sm:text-2xl text-secondary leading-tight">
                    {popupData.heading}
                  </h3>
                  {popupData.sub_heading && (
                    <p className="text-xs sm:text-sm text-slate-600 mt-1 font-normal leading-relaxed">
                      {popupData.sub_heading}
                    </p>
                  )}
                </div>
              )}

              {/* Pure Auto-Fit Image Element (No Gray Background Box) */}
              <div className="relative w-fit h-fit flex items-center justify-center my-auto overflow-hidden rounded-xl">
                {rawUrl ? (
                  isExternal ? (
                    <a
                      href={rawUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block group"
                    >
                      <img
                        src={popupData.image}
                        alt={popupData.heading || "College Announcement Flyer"}
                        className="max-h-[62vh] sm:max-h-[68vh] w-auto max-w-[85vw] object-contain mx-auto rounded-xl transition-transform duration-300 group-hover:scale-[1.01] block"
                      />
                    </a>
                  ) : (
                    <Link
                      href={rawUrl}
                      onClick={handleClose}
                      className="block group"
                    >
                      <img
                        src={popupData.image}
                        alt={popupData.heading || "College Announcement Flyer"}
                        className="max-h-[62vh] sm:max-h-[68vh] w-auto max-w-[85vw] object-contain mx-auto rounded-xl transition-transform duration-300 group-hover:scale-[1.01] block"
                      />
                    </Link>
                  )
                ) : (
                  <img
                    src={popupData.image}
                    alt={popupData.heading || "College Announcement Flyer"}
                    className="max-h-[62vh] sm:max-h-[68vh] w-auto max-w-[85vw] object-contain mx-auto rounded-xl block"
                  />
                )}
              </div>

              {/* Action CTA Button */}
              {popupData.show_cta_button !== false && rawUrl && (
                <div className="mt-3.5 pt-1 w-full text-center">
                  {isExternal ? (
                    <a
                      href={rawUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center justify-center gap-2 bg-primary hover:bg-primary-hover text-white font-bold px-7 py-3 rounded-xl shadow-lg shadow-primary/25 hover:shadow-primary/40 transition-all text-xs sm:text-sm uppercase tracking-wider cursor-pointer"
                    >
                      {popupData.button_text || "Learn More"} <FaArrowRight className="text-xs" />
                    </a>
                  ) : (
                    <Link
                      href={rawUrl}
                      onClick={handleClose}
                      className="inline-flex items-center justify-center gap-2 bg-primary hover:bg-primary-hover text-white font-bold px-7 py-3 rounded-xl shadow-lg shadow-primary/25 hover:shadow-primary/40 transition-all text-xs sm:text-sm uppercase tracking-wider cursor-pointer"
                    >
                      {popupData.button_text || "Learn More"} <FaArrowRight className="text-xs" />
                    </Link>
                  )}
                </div>
              )}

            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}