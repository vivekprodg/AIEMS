/**
 * AIEMS Homepage & Public Submission API Client Layer
 * 100% Dynamic CMS Integration with Fast Failure Safeguards & Null Safety.
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
 * Idempotent Media URL Resolver.
 */
export function resolveMediaUrl(url) {
  if (!url || typeof url !== "string") return null;
  const trimmed = url.trim();
  if (!trimmed) return null;

  if (
    trimmed.startsWith("/logo") || 
    trimmed.startsWith("logo") || 
    trimmed.startsWith("/assets/") || 
    trimmed.startsWith("assets/")
  ) {
    return trimmed.startsWith("/") ? trimmed : `/${trimmed}`;
  }
  
  if (trimmed.startsWith("http://") || trimmed.startsWith("https://")) {
    if (trimmed.includes("localhost:8000") || trimmed.includes("127.0.0.1:8000")) {
      const pathPart = trimmed.replace(/^https?:\/\/[^\/]+/, "");
      return `${API_BASE_URL}${pathPart}`;
    }
    if (trimmed.startsWith("http://api.aiems.edu.np")) {
      return trimmed.replace("http://api.aiems.edu.np", "https://api.aiems.edu.np");
    }
    if (typeof window !== "undefined" && window.location.protocol === "https:" && trimmed.startsWith("http://")) {
      return trimmed.replace("http://", "https://");
    }
    return trimmed;
  }
  
  let cleanPath = trimmed;
  if (!cleanPath.startsWith("/")) {
    cleanPath = `/${cleanPath}`;
  }
  if (!cleanPath.startsWith("/img/")) {
    cleanPath = `/img${cleanPath}`;
  }

  return `${API_BASE_URL}${cleanPath}`;
}

/**
 * Validates and normalizes raw homepage CMS payloads.
 * Strictly dynamic with isolated homepage showcase support and null safety.
 */
export function normalizeHomeContent(data) {
  if (!data || typeof data !== "object") {
    return {
      site_settings: { navbar_links: [] },
      announcements: [],
      eligibility_config: {},
      top_banners: { technical_tags: [], landing_stats: [] },
      about_banners: {},
      programs: { items: [], isolated_showcase_cards: [] },
      admission_contact: {},
      admission_detail: {},
      teams: {},
      apply_job_detail: {},
      news_events: {},
      footer_config: { footer_links: [] },
      faqs: [],
    };
  }

  let processedSiteSettings = { navbar_links: [] };
  if (data.site_settings && typeof data.site_settings === "object") {
    const apiSettings = data.site_settings;
    processedSiteSettings = {
      ...apiSettings,
      logo: apiSettings.logo ? resolveMediaUrl(apiSettings.logo) : null,
      navbar_links: Array.isArray(apiSettings.navbar_links) ? apiSettings.navbar_links : [],
    };
  }

  let processedTopBanners = { technical_tags: [], landing_stats: [] };
  if (data.top_banners && typeof data.top_banners === "object") {
    const apiTopBanner = data.top_banners;
    processedTopBanners = {
      ...apiTopBanner,
      image: apiTopBanner.image ? resolveMediaUrl(apiTopBanner.image) : null,
      technical_tags: Array.isArray(apiTopBanner.technical_tags) ? apiTopBanner.technical_tags : [],
      landing_stats: Array.isArray(apiTopBanner.landing_stats) ? apiTopBanner.landing_stats : [],
    };
  }

  let processedAboutBanners = {};
  if (data.about_banners && typeof data.about_banners === "object") {
    const apiAboutBanner = data.about_banners;
    processedAboutBanners = {
      ...apiAboutBanner,
      image: apiAboutBanner.image ? resolveMediaUrl(apiAboutBanner.image) : null,
      items: Array.isArray(apiAboutBanner.items) ? apiAboutBanner.items : [],
    };
  }

  let processedPrograms = { items: [], isolated_showcase_cards: [] };
  if (data.programs && typeof data.programs === "object") {
    const apiProgTitle = data.programs;
    const rawItems = Array.isArray(apiProgTitle.items) ? apiProgTitle.items : [];

    const processedItems = rawItems.map((prog) => {
      let banner = null;
      if (prog.program_banner && typeof prog.program_banner === "object") {
        banner = {
          ...prog.program_banner,
          image: prog.program_banner.image ? resolveMediaUrl(prog.program_banner.image) : null,
        };
      }

      let summary = [];
      if (Array.isArray(prog.program_summary)) {
        summary = prog.program_summary.map((sum) => ({
          ...sum,
          icon_image: sum.icon_image ? resolveMediaUrl(sum.icon_image) : null,
        }));
      }

      let aboutProg = null;
      if (prog.about_programs && typeof prog.about_programs === "object") {
        aboutProg = {
          ...prog.about_programs,
          image: prog.about_programs.image ? resolveMediaUrl(prog.about_programs.image) : null,
          features: Array.isArray(prog.about_programs.features) ? prog.about_programs.features : [],
        };
      }

      let entryReq = null;
      if (prog.entry_requirements && typeof prog.entry_requirements === "object") {
        entryReq = {
          ...prog.entry_requirements,
          icon: prog.entry_requirements.icon ? resolveMediaUrl(prog.entry_requirements.icon) : null,
          items: Array.isArray(prog.entry_requirements.items) ? prog.entry_requirements.items : [],
        };
      }

      return {
        ...prog,
        icon_image: prog.icon_image ? resolveMediaUrl(prog.icon_image) : null,
        program_banner: banner,
        program_summary: summary,
        about_programs: aboutProg,
        entry_requirements: entryReq,
      };
    });

    const rawIsolatedCards = Array.isArray(apiProgTitle.isolated_showcase_cards) 
      ? apiProgTitle.isolated_showcase_cards 
      : [];

    const processedIsolatedCards = rawIsolatedCards.map((card) => ({
      ...card,
      banner_image: card.banner_image ? resolveMediaUrl(card.banner_image) : null,
      summary_points: Array.isArray(card.summary_points) ? card.summary_points : [],
      features: Array.isArray(card.features) ? card.features : [],
      requirements: Array.isArray(card.requirements) ? card.requirements : [],
    }));

    processedPrograms = {
      ...apiProgTitle,
      items: processedItems,
      isolated_showcase_cards: processedIsolatedCards,
    };
  }

  let processedFooterConfig = { footer_links: [] };
  if (data.footer_config && typeof data.footer_config === "object") {
    const apiFooter = data.footer_config;
    processedFooterConfig = {
      id: apiFooter.id ?? null,
      logo: apiFooter.logo ? resolveMediaUrl(apiFooter.logo) : null,
      branding_description: apiFooter.branding_description || "",
      facebook_url: apiFooter.facebook_url || "",
      instagram_url: apiFooter.instagram_url || "",
      linkedin_url: apiFooter.linkedin_url || "",
      footer_links: Array.isArray(apiFooter.footer_links) ? apiFooter.footer_links : [],
      created_at: apiFooter.created_at ?? null,
    };
  }

  return {
    site_settings: processedSiteSettings,
    announcements: Array.isArray(data.announcements) ? data.announcements : [],
    eligibility_config: data.eligibility_config || {},
    top_banners: processedTopBanners,
    about_banners: processedAboutBanners,
    programs: processedPrograms,
    admission_contact: data.admission_contact || {},
    admission_detail: data.admission_detail || {},
    teams: data.teams || {},
    apply_job_detail: data.apply_job_detail || {},
    news_events: data.news_events || {},
    footer_config: processedFooterConfig,
    faqs: Array.isArray(data.faqs) ? data.faqs : [],
  };
}

/**
 * Standard fetch engine with 10000ms timeout safeguard.
 */
async function fetcher(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const { timeout = 10000, ...fetchOptions } = options;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  const headers = {
    "Accept": "application/json",
    ...(fetchOptions.headers || {}),
  };

  if (!(fetchOptions.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  try {
    const response = await fetch(url, {
      ...fetchOptions,
      headers,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    const rawText = await response.text();
    let parsedData = null;
    
    if (rawText) {
      try {
        parsedData = JSON.parse(rawText);
      } catch (e) {
        parsedData = null;
      }
    }

    if (!response.ok) {
      let serverMessage = `Request failed with HTTP status ${response.status}`;
      if (parsedData && typeof parsedData === "object") {
        if (parsedData.error) serverMessage = parsedData.error;
        else if (parsedData.detail) serverMessage = parsedData.detail;
      }
      throw new Error(serverMessage);
    }

    return parsedData;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === "AbortError") {
      console.warn(`[AIEMS API Client] Timeout/Abort at ${endpoint}. Django backend at ${API_BASE_URL} may be offline or unreadable.`);
    } else {
      console.warn(`[AIEMS API Client] Connection recovery fallback at ${endpoint}: ${error.message}`);
    }
    throw error;
  }
}

export async function getHomeContent(options = {}) {
  const { bypassCache = false, revalidate = 0 } = options;
  const endpoint = bypassCache 
    ? `/api/home/home-content/?bypass_cache=true&t=${Date.now()}` 
    : "/api/home/home-content/";
  
  try {
    const data = await fetcher(endpoint, {
      method: "GET",
      next: { revalidate },
    });
    return normalizeHomeContent(data);
  } catch (error) {
    return normalizeHomeContent(null);
  }
}

export async function getNavbarLinks(options = {}) {
  const { revalidate = 3600 } = options;
  try {
    const response = await fetcher("/api/home/navbar-links/", {
      method: "GET",
      next: { revalidate },
    });
    return Array.isArray(response) ? response : response?.results || [];
  } catch (error) {
    return [];
  }
}

export async function getPrograms(options = {}) {
  const { revalidate = 3600 } = options;
  try {
    const response = await fetcher("/api/home/programs/", {
      method: "GET",
      next: { revalidate },
    });
    return Array.isArray(response) ? response : response?.results || [];
  } catch (error) {
    return [];
  }
}

export async function getTeamFaculties(options = {}) {
  const { revalidate = 3600 } = options;
  try {
    const response = await fetcher("/api/home/teamfaculties/", {
      method: "GET",
      next: { revalidate },
    });
    return Array.isArray(response) ? response : response?.results || [];
  } catch (error) {
    return [];
  }
}

export async function submitContactInquiry(payload) {
  return fetcher("/api/home/contact-us/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function submitCourseApplication(payload) {
  return fetcher("/api/home/apply-course/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function submitVacancyApplication(formData) {
  return fetcher("/api/home/apply-position/", {
    method: "POST",
    body: formData,
  });
}

export async function getApplyCourseBanner(options = {}) {
  const { revalidate = 3600 } = options;
  try {
    return await fetcher("/api/home/apply-course-banner/", {
      method: "GET",
      next: { revalidate },
    });
  } catch (error) {
    return {};
  }
}

export async function getApplyPositionBanner(options = {}) {
  const { revalidate = 3600 } = options;
  try {
    return await fetcher("/api/home/apply-position-banner/", {
      method: "GET",
      next: { revalidate },
    });
  } catch (error) {
    return {};
  }
}

export async function getFAQs(options = {}) {
  const { revalidate = 3600 } = options;
  try {
    const response = await fetcher("/api/home/faq-categories/", {
      method: "GET",
      next: { revalidate },
    });
    return Array.isArray(response) ? response : response?.results || [];
  } catch (error) {
    return [];
  }
}

export async function getDynamicPage(pageKey, options = {}) {
  const { revalidate = 3600 } = options;
  try {
    if (!pageKey) {
      throw new Error("A page key parameter must be provided.");
    }
    return await fetcher(`/api/home/page-contents/${pageKey}/`, {
      method: "GET",
      next: { revalidate },
    });
  } catch (error) {
    return {
      id: null,
      page_key: pageKey,
      title: "",
      subtitle: "",
      content_json: null,
      is_active: false,
      meta_title: "",
      meta_description: "",
      meta_keywords: "",
      structured_data: null
    };
  }
}