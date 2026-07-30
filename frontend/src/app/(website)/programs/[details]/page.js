import React from "react";
import { notFound } from "next/navigation";
import ProgramInteractive from "@/components/program/ProgramInteractive";
import JsonLd from "@/components/seo/JsonLd";
import { getProgramDetails } from "@/lib/api/program";
import { getHomeContent } from "@/lib/api/home";

/**
 * Dynamic Server-Side Metadata Generator for Program Detail Pages.
 */
export async function generateMetadata({ params }) {
  const resolvedParams = await params;
  const programId = resolvedParams?.details;

  if (!programId) {
    return {
      title: "Academic Program | AIEMS",
      description: "Explore industry-aligned academic computing degrees at AIEMS.",
    };
  }

  const program = await getProgramDetails(programId, { revalidate: 3600 });

  if (!program) {
    return {
      title: "Program Not Found | AIEMS",
      description: "The requested academic program could not be found.",
    };
  }

  const title = `${program.heading || "Academic Program"} | AIEMS Bardibas`;
  const description =
    program.sub_content ||
    `Explore curriculum details, entrance criteria, and career outcomes for ${program.heading} at AIEMS.`;

  const bannerImage = program.program_banner?.image || "/assets/banner1.jpg";

  return {
    title,
    description,
    keywords: [
      program.heading,
      "AIEMS CSIT",
      "Academic Program Bardibas",
      "Engineering and Management",
      "CSIT Syllabus Nepal",
    ],
    openGraph: {
      title,
      description,
      images: [{ url: bannerImage }],
      url: `https://aiems.edu.np/programs/${programId}`,
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [bannerImage],
    },
  };
}

/**
 * Server Component Route for Program Details.
 */
export default async function ProgramDetailPage({ params }) {
  const resolvedParams = await params;
  const programId = resolvedParams?.details;

  if (!programId) {
    notFound();
  }

  // Fetch Program Details and Global Site Settings concurrently
  const [programData, homeContent] = await Promise.all([
    getProgramDetails(programId, { revalidate: 3600 }),
    getHomeContent({ revalidate: 3600 }),
  ]);

  if (!programData) {
    notFound();
  }

  const siteSettings = homeContent?.site_settings || {};
  const contactInfo = homeContent?.admission_contact || {};

  return (
    <div className="bg-surface text-slate-800 font-sans antialiased selection:bg-primary selection:text-white overflow-x-hidden scroll-smooth min-h-screen">
      {/* Dynamic Course Schema JSON-LD */}
      <JsonLd type="course" data={programData} />

      {/* Render Dynamic Interactive Client UI */}
      <ProgramInteractive
        program={programData}
        siteSettings={siteSettings}
        contactInfo={contactInfo}
      />
    </div>
  );
}