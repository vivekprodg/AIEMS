"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { Input, Spin } from "antd";
import { 
  FaChevronDown, 
  FaSearch, 
  FaQuestionCircle, 
  FaEnvelope, 
  FaPhone 
} from "react-icons/fa";

import SlideInFromLeft from "@/components/animations/slideInfromLeft";
import SlideInOnScroll from "@/components/animations/sliceInonScroll";
import JsonLd from "@/components/seo/JsonLd";
import { getFAQs, getHomeContent } from "@/lib/api/home";

/**
 * Accessible FAQ Accordion Item Component
 */
const AccordionItem = ({ id, question, answer, isOpen, onToggle }) => {
  return (
    <div className="border border-gray-200/80 rounded-xl bg-white shadow-sm overflow-hidden mb-4 hover:border-primary/50 transition-colors">
      <h3>
        <button
          type="button"
          onClick={() => onToggle(id)}
          aria-expanded={isOpen}
          className="w-full flex justify-between items-center p-5 text-left text-base md:text-lg font-semibold text-secondary hover:text-primary transition-colors focus:outline-none px-6 cursor-pointer"
        >
          <span className="flex items-center gap-3">
            <FaQuestionCircle className="text-primary shrink-0 text-xl" />
            {question}
          </span>
          <span className={`transform transition-transform duration-300 shrink-0 text-primary ml-4 ${isOpen ? "rotate-180" : ""}`}>
            <FaChevronDown />
          </span>
        </button>
      </h3>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: "easeInOut" }}
            className="overflow-hidden"
          >
            <div className="pb-6 px-6 pl-14 text-sm md:text-base text-gray-600 leading-relaxed border-t border-gray-50 pt-4">
              {answer}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default function FAQsPage() {
  const [categories, setCategories] = useState([]);
  const [siteData, setSiteData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [activeFaq, setActiveFaq] = useState(null);

  useEffect(() => {
    let active = true;
    const fetchFAQContent = async () => {
      try {
        setLoading(true);
        const [fetchedCategories, homeData] = await Promise.all([
          getFAQs(),
          getHomeContent()
        ]);
        if (active) {
          setCategories(Array.isArray(fetchedCategories) ? fetchedCategories : []);
          setSiteData(homeData);
        }
      } catch (err) {
        console.error("[AIEMS FAQs] Failed to load FAQ dataset from backend:", err);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    fetchFAQContent();
    return () => {
      active = false;
    };
  }, []);

  const handleFaqToggle = (id) => {
    setActiveFaq(activeFaq === id ? null : id);
  };

  const contactInfo = siteData?.admission_contact || {};
  const siteSettings = siteData?.site_settings || {};

  const phone = contactInfo.contact || siteSettings.primary_phone || "";
  const email = contactInfo.mail_id || siteSettings.primary_email || "";

  const allFaqItems = categories.flatMap((cat) =>
    (cat.faq_items || []).map((item) => ({
      ...item,
      category_slug: item.category_slug || cat.slug,
    }))
  );

  const filteredFaqs = allFaqItems.filter((item) => {
    const matchesCategory = selectedCategory === "all" || item.category_slug === selectedCategory;
    const matchesSearch =
      (item.question && item.question.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (item.answer && item.answer.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const filterCategories = [
    { slug: "all", label: "All Questions" },
    ...categories.map((cat) => ({
      slug: cat.slug,
      label: cat.name,
    })),
  ];

  return (
    <div className="scroll-smooth bg-gray-50/50 min-h-screen">
      {allFaqItems.length > 0 && <JsonLd type="faq" data={allFaqItems} />}

      {/* Banner Section */}
      <div className="relative h-[320px] md:h-[400px] bg-secondary flex items-center justify-center px-6">
        <div className="absolute inset-0 bg-black/40 z-0" />

        <div className="relative z-10 text-center text-white max-w-3xl mx-auto">
          <SlideInFromLeft>
            <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight">
              Frequently Asked Questions
            </h1>
            <div className="h-1 w-20 bg-primary mx-auto rounded-full mt-4 mb-4" />
          </SlideInFromLeft>
        </div>
      </div>

      {/* Floating Content Card Section */}
      <div className="relative z-20 -mt-16 md:-mt-24 px-4 sm:px-6 lg:px-8 pb-20">
        <SlideInOnScroll>
          <div className="max-w-4xl mx-auto bg-white p-6 md:p-12 rounded-2xl shadow-xl border border-gray-200/80">
            
            {/* Search Bar */}
            <div className="max-w-md mx-auto mb-10">
              <Input
                size="large"
                placeholder="Search questions or keywords..."
                prefix={<FaSearch className="text-gray-400 mr-2" />}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="rounded-xl shadow-sm border-gray-200 hover:border-primary focus:border-primary"
                allowClear
              />
            </div>

            {/* Category Filter Tabs */}
            {!loading && filterCategories.length > 1 && (
              <div className="flex flex-wrap gap-2 justify-center mb-10">
                {filterCategories.map((cat) => (
                  <button
                    key={cat.slug}
                    onClick={() => {
                      setSelectedCategory(cat.slug);
                      setActiveFaq(null);
                    }}
                    className={`px-5 py-2.5 rounded-full font-semibold text-xs md:text-sm transition-all duration-200 border cursor-pointer ${
                      selectedCategory === cat.slug
                        ? "bg-primary text-white border-primary shadow-md"
                        : "bg-white text-secondary border-gray-200 hover:border-primary/50"
                    }`}
                  >
                    {cat.label}
                  </button>
                ))}
              </div>
            )}

            {/* FAQs Accordion Block */}
            <div className="space-y-4">
              {loading ? (
                <div className="text-center py-20 flex flex-col items-center justify-center">
                  <Spin size="large" />
                  <p className="mt-4 text-slate-600 font-medium text-sm">Retrieving FAQs...</p>
                </div>
              ) : filteredFaqs.length > 0 ? (
                filteredFaqs.map((faq) => (
                  <AccordionItem
                    key={faq.id}
                    id={faq.id}
                    question={faq.question}
                    answer={faq.answer}
                    isOpen={activeFaq === faq.id}
                    onToggle={handleFaqToggle}
                  />
                ))
              ) : (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-12 bg-gray-50 rounded-xl border border-dashed border-gray-200"
                >
                  <p className="text-gray-500 text-base">No matching questions found.</p>
                  <button
                    onClick={() => {
                      setSelectedCategory("all");
                      setSearchQuery("");
                    }}
                    className="mt-4 text-primary font-bold hover:underline cursor-pointer"
                  >
                    Reset Filters
                  </button>
                </motion.div>
              )}
            </div>

            {/* Institutional Contact Box */}
            {(email || phone) && (
              <div className="mt-16 bg-secondary text-white rounded-2xl p-8 md:p-12 shadow-lg text-center relative overflow-hidden">
                <div className="relative z-10 max-w-2xl mx-auto space-y-6">
                  <h2 className="text-2xl md:text-3xl font-bold">Still have questions?</h2>
                  <div className="flex flex-col sm:flex-row justify-center items-center gap-6 pt-2">
                    {email && (
                      <a
                        href={`mailto:${email}`}
                        className="flex items-center gap-2 hover:text-accent transition-colors font-semibold text-white"
                      >
                        <FaEnvelope className="text-primary text-lg" />
                        {email}
                      </a>
                    )}
                    {phone && (
                      <a
                        href={`tel:${phone}`}
                        className="flex items-center gap-2 hover:text-accent transition-colors font-semibold text-white"
                      >
                        <FaPhone className="text-primary text-lg" />
                        {phone}
                      </a>
                    )}
                  </div>
                  <div className="pt-4 flex flex-wrap justify-center gap-4">
                    <Link
                      href="/contact-us"
                      className="px-6 py-2.5 bg-primary hover:bg-primary-hover text-white font-semibold rounded-xl text-center transition-colors duration-200 text-sm shadow-md"
                    >
                      Contact Admissions Desk
                    </Link>
                    <Link
                      href="/apply-now"
                      className="px-6 py-2.5 bg-transparent border-2 border-white hover:bg-white hover:text-secondary text-white font-semibold rounded-xl text-center transition-all duration-200 text-sm"
                    >
                      Apply Now
                    </Link>
                  </div>
                </div>
              </div>
            )}

            {/* Back to Home CTA */}
            <div className="mt-12 pt-8 border-t border-gray-150 flex justify-center">
              <Link
                href="/"
                className="px-6 py-2.5 bg-primary hover:bg-primary-hover text-white font-semibold rounded-xl text-center transition-colors duration-200 text-sm shadow-md"
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