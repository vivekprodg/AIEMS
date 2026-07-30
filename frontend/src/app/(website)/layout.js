import React, { Suspense } from "react";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";
import TawkToScript from "@/components/TawkToScript";
import Loading from "./loading";
import { getHomeContent } from "@/lib/api/home";

export const dynamic = "force-dynamic";

export default async function WebsiteLayout({ children }) {
  const globalData = await getHomeContent({ bypassCache: false });

  const admissionContact = globalData?.admission_contact || {};
  const applyJobDetail = globalData?.apply_job_detail || {};
  const footerConfig = globalData?.footer_config || {};
  const announcements = Array.isArray(globalData?.announcements) ? globalData.announcements : [];
  const siteSettings = globalData?.site_settings || {};

  return (
    <div className="bg-white min-h-screen flex flex-col justify-between">
      {/* Dynamic Site-Wide Tawk.to Live Chat Script */}
      <TawkToScript />

      <Navbar 
        contactInfo={admissionContact} 
        footerConfig={footerConfig} 
        announcements={announcements}
        siteSettings={siteSettings}
      />
      
      <main id="main-content" role="main" className="w-full flex-grow">
        <Suspense fallback={<Loading />}>
          {children}
        </Suspense>
      </main>

      <Footer 
        contactInfo={admissionContact} 
        jobInfo={applyJobDetail} 
        footerConfig={footerConfig} 
        siteSettings={siteSettings}
      />
    </div>
  );
}