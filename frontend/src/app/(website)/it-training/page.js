import React from "react";
import TrainingHero from "@/components/training/TrainingHero";
import TrainingSidebar from "@/components/training/TrainingSidebar";
import TrainingForm from "@/components/training/TrainingForm";
import JsonLd from "@/components/seo/JsonLd";
import { getTrainingPageContent } from "@/lib/api/training";
import { getHomeContent } from "@/lib/api/home";

/**
 * Dynamic Server-Side Metadata Generator for /it-training Route.
 */
export async function generateMetadata() {
  const trainingData = await getTrainingPageContent({ revalidate: 3600 });

  const title = trainingData.meta_title || "Practical IT & AI Training for Non-Technical Students | AIEMS";
  const description = trainingData.meta_description || "Zero-prerequisite IT & AI training for non-tech students in Bardibas. Hands-on coding, ChatGPT tools, and web basics.";
  const keywords = trainingData.meta_keywords 
    ? trainingData.meta_keywords.split(",").map((k) => k.trim())
    : ["AIEMS", "IT Training Bardibas", "AI course Nepal", "Non-tech computer training"];

  const bannerImage = trainingData.image || "/assets/banner1.jpg";

  return {
    title,
    description,
    keywords,
    openGraph: {
      title,
      description,
      images: [{ url: bannerImage }],
      url: "https://aiems.edu.np/it-training",
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
 * Server Component Route for IT & AI Training Page.
 */
export default async function ITTrainingPage() {
  const [trainingData, homeContent] = await Promise.all([
    getTrainingPageContent({ revalidate: 3600 }),
    getHomeContent({ revalidate: 3600 }),
  ]);

  const siteSettings = homeContent?.site_settings || {};
  const contactInfo = homeContent?.admission_contact || {};

  const structuredSchema = trainingData.structured_data || {
    "@context": "https://schema.org",
    "@type": "Course",
    "name": trainingData.heading,
    "description": trainingData.sub_heading,
    "provider": {
      "@type": "CollegeOrUniversity",
      "name": "Ankur Institute of Engineering and Management Studies (AIEMS)",
      "url": "https://aiems.edu.np"
    }
  };

  return (
    <div className="bg-surface text-slate-800 font-sans antialiased selection:bg-primary selection:text-white min-h-screen">
      {/* Schema.org JSON-LD Structured Data */}
      <JsonLd schema={structuredSchema} />

      {/* 1. Hero Banner Component */}
      <TrainingHero bannerData={trainingData} />

      {/* 2. Main Two-Column Layout (Sidebar + Registration Form) */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 pb-20 relative z-20 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column: 7 Modules Syllabus Summary & Student Perks */}
          <div className="lg:col-span-4">
            <TrainingSidebar
              modulesList={trainingData.modules}
              perksList={trainingData.perks}
              contactInfo={contactInfo}
              siteSettings={siteSettings}
            />
          </div>

          {/* Right Column: Dynamic Lead Capture Form with Dynamic Timeframes */}
          <div className="lg:col-span-8 bg-white rounded-3xl p-6 sm:p-10 border border-slate-200 shadow-ultra">
            <TrainingForm
              modulesList={trainingData.modules}
              timeSlotsList={trainingData.time_slots}
              streamOptionsList={trainingData.stream_options}
              timeframeOptionsList={trainingData.timeframe_options}
              deliveryModesList={trainingData.delivery_modes}
              experienceLevelsList={trainingData.experience_levels}
            />
          </div>

        </div>
      </main>
    </div>
  );
}