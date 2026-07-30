import React from "react";
import {
  getOrganizationSchema,
  getCollegeSchema,
  getCourseSchema,
  getBreadcrumbSchema,
  getNewsArticleSchema,
  getFAQSchema,
  getCombinedHomepageSchema,
} from "@/lib/schema/home-schema";

/**
 * Centralized JSON-LD structured data injection component.
 * Integrates directly with the AIEMS CMS-driven schema generators (home-schema.js)
 * to output highly secure, optimized JSON-LD scripts for standard search crawlers,
 * rich search features, and modern Answer Engine Optimization (AEO) models.
 *
 * Supported Integrations:
 * 1. CMS-driven Generation (Recommended):
 *    <JsonLd type="organization" data={homeContent} />
 *    <JsonLd type="college" data={homeContent} />
 *    <JsonLd type="combined" data={homeContent} />
 *    <JsonLd type="course" data={program} />
 *    <JsonLd type="faq" data={faqs} />
 *    <JsonLd type="breadcrumb" data={[{ name: "Home", path: "/" }, { name: "Admissions", path: "/apply-now" }]} />
 *    <JsonLd type="news" data={newsItem} />
 * 
 * 2. Custom Manual Schema Injection (Escape hatch):
 *    <JsonLd schema={customSchemaObject} />
 */
export default function JsonLd({ type, data, schema }) {
  let resolvedSchema = null;

  // 1. Resolve schemas based on passed type and dynamic CMS dataset
  if (type && data) {
    try {
      switch (type.toLowerCase()) {
        case "organization":
          resolvedSchema = getOrganizationSchema(data);
          break;
        case "college":
          resolvedSchema = getCollegeSchema(data);
          break;
        case "course":
          resolvedSchema = getCourseSchema(data);
          break;
        case "breadcrumb":
          resolvedSchema = getBreadcrumbSchema(data);
          break;
        case "news":
          resolvedSchema = getNewsArticleSchema(data);
          break;
        case "faq":
          resolvedSchema = getFAQSchema(data);
          break;
        case "combined":
          resolvedSchema = getCombinedHomepageSchema(data);
          break;
        default:
          console.warn(`[AIEMS SEO] Unsupported schema type requested: "${type}"`);
          break;
      }
    } catch (err) {
      console.error(`[AIEMS SEO] Failed to generate structured data for type "${type}":`, err);
    }
  } else if (schema) {
    // 2. Fall back to direct manual schema object injection override
    resolvedSchema = schema;
  }

  // If no schema could be resolved or built, exit silently to maintain page stability
  if (!resolvedSchema) {
    return null;
  }

  // 3. Serialize and sanitize payload securely to prevent injection attacks (XSS)
  let serializedPayload = "";
  try {
    const rawString = JSON.stringify(resolvedSchema);
    // Escapes critical angle brackets with their Unicode representations
    // to strictly prevent nested inline script tags or browser content-sniffing exploits.
    serializedPayload = rawString
      .replace(/</g, "\\u003c")
      .replace(/>/g, "\\u003e");
  } catch (err) {
    console.error("[AIEMS SEO] Failed to serialize structured data schema payload:", err);
    return null;
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: serializedPayload }}
    />
  );
}