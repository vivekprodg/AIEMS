"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Button, Card, Badge, Spin } from "antd";
import { 
  FaWifi, 
  FaPhone, 
  FaEnvelope, 
  FaMapMarkerAlt, 
  FaSync, 
  FaExclamationTriangle 
} from "react-icons/fa";
import { getHomeContent } from "@/lib/api/home";

export default function OfflinePage() {
  const router = useRouter();
  const [isChecking, setIsChecking] = useState(false);
  const [isOnline, setIsOnline] = useState(true);
  const [siteData, setSiteData] = useState(null);

  useEffect(() => {
    let active = true;
    const fetchSiteDetails = async () => {
      try {
        const data = await getHomeContent();
        if (active) {
          setSiteData(data);
        }
      } catch (err) {
        console.error("Error retrieving site contacts for offline page:", err);
      }
    };

    fetchSiteDetails();
    return () => {
      active = false;
    };
  }, []);

  const contactInfo = siteData?.admission_contact || {};
  const siteSettings = siteData?.site_settings || {};

  const phone = contactInfo.contact || siteSettings.primary_phone || "";
  const email = contactInfo.mail_id || siteSettings.primary_email || "";
  const address = siteSettings.location_address || "";

  const verifyActualConnectivity = async () => {
    if (typeof window === "undefined" || !navigator.onLine) {
      return false;
    }
    try {
      const response = await fetch("/manifest.json?t=" + Date.now(), {
        method: "HEAD",
        cache: "no-store",
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  };

  const handleManualRetry = async () => {
    setIsChecking(true);
    const connected = await verifyActualConnectivity();
    setIsOnline(connected);
    setIsChecking(false);

    if (connected) {
      router.refresh();
      router.push("/home");
    }
  };

  useEffect(() => {
    if (typeof window === "undefined") return;

    setIsOnline(navigator.onLine);

    const handleOnlineEvent = async () => {
      const connected = await verifyActualConnectivity();
      setIsOnline(connected);
      if (connected) {
        router.refresh();
        router.push("/home");
      }
    };

    const handleOfflineEvent = () => {
      setIsOnline(false);
    };

    window.addEventListener("online", handleOnlineEvent);
    window.addEventListener("offline", handleOfflineEvent);

    return () => {
      window.removeEventListener("online", handleOnlineEvent);
      window.removeEventListener("offline", handleOfflineEvent);
    };
  }, [router]);

  return (
    <div className="min-h-[75vh] flex items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-xl"
      >
        <Card className="shadow-xl rounded-2xl border-t-4 border-t-primary overflow-hidden">
          <div className="text-center space-y-6">
            
            {/* Animated Connection Indicator Icon */}
            <div className="flex justify-center relative">
              <div className="relative flex items-center justify-center w-24 h-24 bg-gray-100 rounded-full">
                <AnimatePresence mode="wait">
                  {!isOnline ? (
                    <motion.div
                      key="offline-icon"
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      exit={{ scale: 0.8, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                      className="text-gray-400 text-5xl"
                    >
                      <FaWifi />
                    </motion.div>
                  ) : (
                    <motion.div
                      key="online-icon"
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: [1, 1.2, 1], opacity: 1 }}
                      exit={{ scale: 0.8, opacity: 0 }}
                      transition={{ duration: 0.5, repeat: Infinity, repeatDelay: 2 }}
                      className="text-primary text-5xl"
                    >
                      <FaWifi />
                    </motion.div>
                  )}
                </AnimatePresence>
                
                <div className="absolute bottom-1 right-1">
                  <Badge 
                    status={isOnline ? "success" : "warning"} 
                    className="scale-125"
                  />
                </div>
              </div>
            </div>

            {/* Heading Content */}
            <div className="space-y-2">
              <h1 className="text-3xl font-extrabold text-secondary tracking-tight">
                Connection Interrupted
              </h1>
              <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-50 rounded-full text-xs font-semibold text-amber-800 border border-amber-200">
                <FaExclamationTriangle className="shrink-0" />
                <span>Running in Offline Mode</span>
              </div>
            </div>

            <p className="text-gray-600 text-base max-w-md mx-auto leading-relaxed">
              You are currently disconnected from the network. Previously loaded cached assets remain available.
            </p>

            {/* Reconnect Try Button */}
            <div className="pt-2">
              <Button
                type="primary"
                size="large"
                disabled={isChecking}
                onClick={handleManualRetry}
                className="btn_primary_fill min-w-[200px] h-12 rounded-xl flex items-center justify-center gap-2 mx-auto"
                aria-label="Retry network connection"
              >
                {isChecking ? (
                  <Spin size="small" className="brightness-200" />
                ) : (
                  <FaSync className="text-sm shrink-0" />
                )}
                <span>{isChecking ? "Testing link..." : "Retry Connection"}</span>
              </Button>
            </div>

            {/* Emergency Hotline / Institutional Contact Box */}
            {(phone || email || address) && (
              <div className="mt-8 pt-6 border-t border-gray-100 text-left">
                <h2 className="text-sm font-bold text-secondary uppercase tracking-wider mb-4">
                  Institutional Contacts
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  
                  {phone && (
                    <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
                      <FaPhone className="text-primary mt-1 shrink-0" aria-hidden="true" />
                      <div>
                        <p className="text-xs text-gray-500 font-medium">Hotline Support</p>
                        <a 
                          href={`tel:${phone}`} 
                          className="text-sm font-bold text-secondary hover:text-primary hover:underline"
                        >
                          {phone}
                        </a>
                      </div>
                    </div>
                  )}

                  {email && (
                    <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors">
                      <FaEnvelope className="text-primary mt-1 shrink-0" aria-hidden="true" />
                      <div>
                        <p className="text-xs text-gray-500 font-medium">Admissions Desk</p>
                        <a 
                          href={`mailto:${email}`} 
                          className="text-sm font-bold text-secondary hover:text-primary hover:underline break-all"
                        >
                          {email}
                        </a>
                      </div>
                    </div>
                  )}

                </div>

                {address && (
                  <div className="mt-4 flex items-center gap-2 p-3 bg-gray-50 rounded-xl text-xs text-gray-600">
                    <FaMapMarkerAlt className="text-primary shrink-0" aria-hidden="true" />
                    <span><strong>Campus Address:</strong> {address}</span>
                  </div>
                )}
              </div>
            )}

          </div>
        </Card>
      </motion.div>
    </div>
  );
}