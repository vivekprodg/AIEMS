import React from "react";
import Script from "next/script";
import HomeContent from "@/components/home/server/HomeContent";
import HomeInteractive from "@/components/home/client/HomeInteractive";
import JsonLd from "@/components/seo/JsonLd";
import { getHomeContent } from "@/lib/api/home";

/**
 * Server-Side Metadata Generator for /home route.
 */
export async function generateMetadata() {
  const content = await getHomeContent();
  const banner = content?.top_banners || {};

  const title = banner.meta_title || "AIEMS — Ankur Institute of Engineering and Management Studies | BSc. CSIT";
  const description = banner.meta_description || "Ankur Institute of Engineering and Management Studies (AIEMS) — Brand new technical college offering RJU affiliated BSc. CSIT in Bardibas, Nepal.";
  const keywords = banner.meta_keywords 
    ? banner.meta_keywords.split(",").map(k => k.trim()) 
    : ["AIEMS", "BSc CSIT", "Rajarshi Janak University", "RJU Affiliated", "Bardibas CSIT College"];

  return {
    title,
    description,
    keywords,
    openGraph: {
      title,
      description,
      images: banner.image ? [{ url: banner.image }] : [{ url: "/assets/banner1.jpg" }],
      url: "https://aiems.edu.np/home",
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: banner.image ? [banner.image] : ["/assets/banner1.jpg"],
    }
  };
}

/**
 * Main Home Page Server Component.
 * Integrates Server Content and Client Interactive overlays in seamless sequence:
 * Hero -> Landing Stats -> About AIEMS -> 12-Column Split Program Showcase Card -> Eligibility Calculator -> Tech Labs -> Admissions -> FAQs -> News -> Contact CTA
 */
export default async function HomePage() {
  const homeContent = await getHomeContent();

  return (
    <div className="w-full min-h-screen bg-surface">
      {/* Tawk.to Customer Support Live Chat Script (Updated Property ID) */}
      <Script
        id="tawk-to-script"
        strategy="lazyOnload"
        src="https://embed.tawk.to/6a6b7d0700c8c61d49f132ee/1jupu0q4t"
        crossOrigin="*"
      />

      {/* JSON-LD Schema.org Structured Data */}
      <JsonLd type="combined" data={homeContent} />

      {/* Server Rendered Layout Content (Hero, Stats, About, 12-Column Split Program Showcase) */}
      <HomeContent content={homeContent} />

      {/* Client Interactive Overlay (Eligibility Calculator, Tech Labs, Admissions, FAQs, News, CTA) */}
      <HomeInteractive content={homeContent} />
    </div>
  );
}