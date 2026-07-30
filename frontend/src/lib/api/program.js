/**
 * AIEMS Academic Program Detail API Client Layer
 * 100% Dynamic CMS Data Retrieval with Media URL Resolution & Fast Fallbacks.
 */

import { resolveMediaUrl } from "./home";

const getApiBaseUrl = () => {
  if (process.env.NEXT_PUBLIC_API_BASE_URL) {
    return process.env.NEXT_PUBLIC_API_BASE_URL.replace(/\/+$/, "");
  }
  if (typeof window !== "undefined" && window.location.hostname === "localhost") {
    return "http://127.0.0.1:8000";
  }
  if (process.env.NODE_ENV === "development") {
    return "http://127.0.0.1:8000";
  }
  return "https://api.aiems.edu.np";
};

const API_BASE_URL = getApiBaseUrl();

/**
 * Normalizes raw Program CMS payloads from Django DRF into clean objects.
 * Performs media URL resolution and ensures array fields are safely typed.
 */
export function normalizeProgramContent(data) {
  if (!data || typeof data !== "object") {
    return null;
  }

  // Resolve Banner Image
  let processedBanner = null;
  if (data.program_banner && typeof data.program_banner === "object") {
    processedBanner = {
      ...data.program_banner,
      image: resolveMediaUrl(data.program_banner.image),
    };
  }

  // Resolve Summary Metrics
  const processedSummary = Array.isArray(data.program_summary)
    ? data.program_summary.map((item) => ({
        ...item,
        icon_image: resolveMediaUrl(item.icon_image),
      }))
    : [];

  // Resolve About Program & Features
  let processedAbout = null;
  if (data.about_programs && typeof data.about_programs === "object") {
    processedAbout = {
      ...data.about_programs,
      image: resolveMediaUrl(data.about_programs.image),
      features: Array.isArray(data.about_programs.features) ? data.about_programs.features : [],
    };
  }

  // Resolve Entry Requirements
  let processedEntry = null;
  if (data.entry_requirements && typeof data.entry_requirements === "object") {
    processedEntry = {
      ...data.entry_requirements,
      icon: resolveMediaUrl(data.entry_requirements.icon),
      items: Array.isArray(data.entry_requirements.items) ? data.entry_requirements.items : [],
    };
  }

  // Resolve Course Details and Semesters
  const processedCourseDetails = Array.isArray(data.course_details)
    ? data.course_details.map((sem) => ({
        ...sem,
        courses: Array.isArray(sem.courses) ? sem.courses : [],
      }))
    : [];

  // Resolve Industry Certifications
  const processedCertifications = Array.isArray(data.industry_certifications)
    ? data.industry_certifications
    : [];

  // Resolve Career Outcomes
  let processedCareerOutcomes = null;
  if (data.career_outcomes && typeof data.career_outcomes === "object") {
    processedCareerOutcomes = {
      ...data.career_outcomes,
      child_outcomes: Array.isArray(data.career_outcomes.child_outcomes)
        ? data.career_outcomes.child_outcomes.map((child) => ({
            ...child,
            icon_image: resolveMediaUrl(child.icon_image),
          }))
        : [],
    };
  }

  return {
    id: data.id ?? null,
    heading: data.heading || "",
    sub_content: data.sub_content || "",
    program_title: data.program_title || "",
    icon_image: resolveMediaUrl(data.icon_image),
    program_banner: processedBanner,
    program_summary: processedSummary,
    about_programs: processedAbout,
    entry_requirements: processedEntry,
    course_details: processedCourseDetails,
    industry_certifications: processedCertifications,
    career_outcomes: processedCareerOutcomes,
  };
}

/**
 * Retrieves dynamic program detail payload directly from Django REST endpoint.
 *
 * @param {string|number} programId - ID of the target academic program.
 * @param {Object} options - Configuration options (revalidate, timeout).
 * @returns {Promise<Object|null>} Normalized Program data object.
 */
export async function getProgramDetails(programId, options = {}) {
  if (!programId) return null;

  const { revalidate = 3600, timeout = 10000 } = options;
  const endpoint = `${API_BASE_URL}/api/program/${programId}/`;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(endpoint, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      next: { revalidate },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      if (response.status === 404) {
        console.warn(`[AIEMS Program API] Program ID ${programId} not found.`);
        return null;
      }
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    return normalizeProgramContent(data);
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === "AbortError") {
      console.warn(`[AIEMS Program API] Timeout at ${endpoint}. Server unreachable.`);
    } else {
      console.warn(`[AIEMS Program API] Failed to fetch program ${programId}:`, error.message);
    }
    return null;
  }
}