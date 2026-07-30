/**
 * AIEMS Centralized Structured Data (Schema.org / JSON-LD) Generator
 * Defensive, XSS-safe schema builders strictly utilizing live CMS properties.
 */

const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || "https://aiems.edu.np").replace(/\/+$/, "");

function cleanString(str) {
  if (!str || typeof str !== "string") return "";
  return str
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"')
    .replace(/\n/g, "\\n")
    .replace(/\r/g, "\\r")
    .trim();
}

export function getCmsStructuredData(content) {
  if (!content) return null;

  const rawData = content.structured_data;
  if (!rawData) return null;

  if (typeof rawData === "object") {
    return rawData;
  }

  try {
    return JSON.parse(rawData);
  } catch (error) {
    console.error("[AIEMS Schema] Error parsing CMS JSON-LD structured data:", error);
    return null;
  }
}

export function getOrganizationSchema(homeContent) {
  const contact = homeContent?.admission_contact || {};
  const siteSettings = homeContent?.site_settings || {};
  const about = homeContent?.about_banners || {};

  const name = cleanString(siteSettings.site_title || about.heading) || "AIEMS";
  const description = cleanString(about.sub_heading) || "";

  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": `${SITE_URL}/#organization`,
    "name": name,
    "url": SITE_URL,
    "logo": {
      "@type": "ImageObject",
      "url": siteSettings.logo || `${SITE_URL}/logo.svg`,
    },
    "description": description,
    "telephone": cleanString(contact.contact || siteSettings.primary_phone) || "",
    "email": cleanString(contact.mail_id || siteSettings.primary_email) || "",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": cleanString(siteSettings.location_address) || "",
      "addressCountry": "NP"
    }
  };
}

export function getCollegeSchema(homeContent) {
  const contact = homeContent?.admission_contact || homeContent?.learn_more_contact || {};
  const siteSettings = homeContent?.site_settings || {};
  const about = homeContent?.about_banners || homeContent?.about_banner || {};
  const banner = homeContent?.top_banners || homeContent?.top_banner || {};

  const name = cleanString(siteSettings.site_title) || "AIEMS";
  const description = cleanString(about.sub_heading) || "";
  const image = banner.image ? cleanString(banner.image) : "";

  return {
    "@context": "https://schema.org",
    "@type": "CollegeOrUniversity",
    "@id": `${SITE_URL}/#college`,
    "name": name,
    "url": SITE_URL,
    "logo": siteSettings.logo || `${SITE_URL}/logo.svg`,
    "image": image,
    "description": description,
    "telephone": cleanString(contact.contact || siteSettings.primary_phone) || "",
    "email": cleanString(contact.mail_id || siteSettings.primary_email) || "",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": cleanString(siteSettings.location_address) || "",
      "addressCountry": "NP"
    }
  };
}

/**
 * Generates dynamic Schema.org/Course JSON-LD metadata for Academic Programs.
 */
export function getCourseSchema(program) {
  if (!program || !program.id) return null;

  const title = cleanString(program.heading) || "Academic Program";
  const description = cleanString(program.sub_content) || "";
  
  // Extract entry requirements dynamically
  let prerequisites = "";
  if (program.entry_requirements) {
    const entryObj = program.entry_requirements;
    const overview = cleanString(entryObj.content);
    const itemBullets = Array.isArray(entryObj.items)
      ? entryObj.items.map((i) => cleanString(typeof i === "string" ? i : i.content)).filter(Boolean).join("; ")
      : "";

    prerequisites = [overview, itemBullets].filter(Boolean).join(" - ");
  }

  // Extract affiliate / university information dynamically from AboutProgram
  const providerName = cleanString(program.about_programs?.charter_badge_title) || "AIEMS";

  return {
    "@context": "https://schema.org",
    "@type": "Course",
    "@id": `${SITE_URL}/programs/${program.id}#course`,
    "name": title,
    "description": description,
    "provider": {
      "@type": "CollegeOrUniversity",
      "name": providerName,
      "url": SITE_URL
    },
    "courseCode": `AIEMS-PROG-${program.id}`,
    "educationalCredentialAwarded": title,
    "programPrerequisites": prerequisites
  };
}

export function getBreadcrumbSchema(items = []) {
  if (!Array.isArray(items) || items.length === 0) return null;

  const itemListElement = items.map((item, index) => {
    const cleanName = cleanString(item.name);
    const resolvedPath = item.path ? item.path.replace(/^\/+/, "") : "";
    const absoluteItemUrl = resolvedPath ? `${SITE_URL}/${resolvedPath}` : SITE_URL;

    return {
      "@type": "ListItem",
      "position": index + 1,
      "name": cleanName,
      "item": absoluteItemUrl
    };
  });

  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": itemListElement
  };
}

export function getNewsArticleSchema(newsItem) {
  if (!newsItem || !newsItem.id) return null;

  const heading = cleanString(newsItem.heading);
  const content = cleanString(newsItem.content);
  const datePublished = newsItem.date ? newsItem.date : new Date().toISOString().split("T")[0];

  return {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "@id": `${SITE_URL}/home#news-event-${newsItem.id}`,
    "headline": heading,
    "description": content.length > 150 ? `${content.substring(0, 147)}...` : content,
    "datePublished": datePublished,
    "publisher": {
      "@type": "CollegeOrUniversity",
      "name": "AIEMS",
      "logo": {
        "@type": "ImageObject",
        "url": `${SITE_URL}/logo.svg`
      }
    }
  };
}

export function getFAQSchema(faqs = []) {
  if (!Array.isArray(faqs) || faqs.length === 0) return null;

  const mainEntity = faqs.map(faq => ({
    "@type": "Question",
    "name": cleanString(faq.question),
    "acceptedAnswer": {
      "@type": "Answer",
      "text": cleanString(faq.answer)
    }
  }));

  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": mainEntity
  };
}

export function getCombinedHomepageSchema(homeContent) {
  const schemas = [];

  const org = getOrganizationSchema(homeContent);
  const college = getCollegeSchema(homeContent);
  
  if (org) schemas.push(org);
  if (college) schemas.push(college);

  if (homeContent?.news_events?.items && Array.isArray(homeContent.news_events.items)) {
    homeContent.news_events.items.forEach(item => {
      const newsSchema = getNewsArticleSchema(item);
      if (newsSchema) schemas.push(newsSchema);
    });
  }

  const cmsStructuredData = getCmsStructuredData(homeContent?.top_banners);
  if (cmsStructuredData) {
    if (Array.isArray(cmsStructuredData)) {
      schemas.push(...cmsStructuredData);
    } else {
      schemas.push(cmsStructuredData);
    }
  }

  return schemas;
}