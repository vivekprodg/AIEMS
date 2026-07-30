import React from "react";
import Link from "next/link";
import SlideInFromLeft from "@/components/animations/slideInfromLeft";
import SlideInOnScroll from "@/components/animations/sliceInonScroll";
import JsonLd from "@/components/seo/JsonLd";
import { getDynamicPage } from "@/lib/api/home";

const getActiveSections = (contentJson) => {
  if (!contentJson) return [];
  if (Array.isArray(contentJson)) return contentJson;
  if (contentJson.sections && Array.isArray(contentJson.sections)) return contentJson.sections;
  return [];
};

export async function generateMetadata() {
  const pageData = await getDynamicPage("terms-and-conditions");

  const title = pageData?.meta_title || pageData?.title || "Terms and Conditions";
  const description = pageData?.meta_description || "";
  const keywords = pageData?.meta_keywords ? pageData.meta_keywords.split(",").map(k => k.trim()) : [];

  return {
    title,
    description,
    keywords,
    openGraph: {
      title,
      description,
      type: "website",
    },
  };
}

export default async function TermsAndConditions() {
  const pageData = await getDynamicPage("terms-and-conditions");

  const activeTitle = pageData?.title || "Terms & Conditions";
  const activeSubtitle = pageData?.subtitle || "";
  const activeSections = getActiveSections(pageData?.content_json);

  return (
    <div className="scroll-smooth bg-gray-50/50 min-h-screen">
      {pageData?.structured_data && (
        <JsonLd schema={pageData.structured_data} />
      )}

      {/* Banner Section */}
      <div className="relative h-[320px] md:h-[400px] bg-secondary flex items-center justify-center px-6">
        <div className="absolute inset-0 bg-black/50 z-0" />

        <div className="relative z-10 text-center text-white max-w-3xl mx-auto">
          <SlideInFromLeft>
            <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight">
              {activeTitle}
            </h1>
            {activeSubtitle && (
              <p className="text-white/80 text-base md:text-lg mt-4">
                {activeSubtitle}
              </p>
            )}
          </SlideInFromLeft>
        </div>
      </div>

      {/* Dynamic Content Sections */}
      <div className="relative z-20 -mt-16 md:-mt-24 px-4 sm:px-6 lg:px-8 pb-20">
        <SlideInOnScroll>
          <div className="max-w-4xl mx-auto bg-white p-8 md:p-12 rounded-2xl shadow-xl border border-gray-200/80">
            {activeSections.length > 0 ? (
              <div className="space-y-10">
                {activeSections.map((section) => (
                  <section key={section.id || section.title} id={section.id} className="scroll-mt-32">
                    {section.title && (
                      <h2 className="text-2xl font-bold text-secondary mb-4 tracking-tight border-b border-gray-150 pb-2">
                        {section.title}
                      </h2>
                    )}
                    <div className="space-y-4">
                      {section.paragraphs && Array.isArray(section.paragraphs) ? (
                        section.paragraphs.map((para, idx) => (
                          <p key={idx} className="text-gray-600 text-base leading-relaxed">
                            {para}
                          </p>
                        ))
                      ) : null}
                    </div>
                  </section>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                Terms and conditions are currently being updated in the administrative CMS.
              </div>
            )}

            <div className="mt-12 pt-8 border-t border-gray-150 flex justify-center">
              <Link
                href="/"
                className="px-6 py-2.5 bg-primary hover:bg-[#007a36] text-white font-semibold rounded-lg text-center transition-colors duration-200 text-sm shadow-md"
              >
                Back to Home
              </Link>
            </div>
          </div>
        </SlideInOnScroll>
      </div>
    </div>
  );
}