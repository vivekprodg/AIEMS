/**
 * AIEMS About Us API Client Layer
 * 100% Dynamic CMS Data Retrieval with Fast Fallbacks.
 */

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
 * Validates and normalizes raw About Us CMS API payloads.
 */
export function normalizeAboutContent(data) {
  if (!data || typeof data !== "object") {
    return {
      top_banner: {},
      about_banner: {},
      about_vision: {},
      core_values: {},
      metrics: [],
      leadership: {},
      campus_facilities: {},
      vision_research: {},
      achievements: {},
      learn_more_contact: {}
    };
  }

  return {
    top_banner: data.top_banner || {},
    about_banner: data.about_banner || {},
    about_vision: data.about_vision || {},
    core_values: data.core_values || {},
    metrics: Array.isArray(data.metrics) ? data.metrics : [],
    leadership: data.leadership || {},
    campus_facilities: data.campus_facilities || {},
    vision_research: data.vision_research || {},
    achievements: data.achievements || {},
    learn_more_contact: data.learn_more_contact || {}
  };
}

/**
 * Retrieves About Us page CMS payload directly from the Django backend.
 */
export async function getAboutContent(options = {}) {
  const { bypassCache = false, revalidate = 3600 } = options;
  const endpoint = `${API_BASE_URL}/api/about/about-content/${bypassCache ? '?bypass_cache=true' : ''}`;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);

  try {
    const response = await fetch(endpoint, {
      method: "GET",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      next: { revalidate },
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return normalizeAboutContent(data);
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === "AbortError") {
      console.warn(`[AIEMS About API] Timeout/Abort at ${endpoint}. Django backend at ${API_BASE_URL} may be offline.`);
    } else {
      console.warn("[AIEMS About API] API retrieval fallback triggered:", error.message || error);
    }
    return normalizeAboutContent(null);
  }
}