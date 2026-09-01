/**
 * AIEMS IT & AI Training API Client Layer
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
 * Normalizes raw Training CMS payloads from Django DRF into clean, null-safe objects.
 */
export function normalizeTrainingContent(data) {
  if (!data || typeof data !== "object") {
    return {
      badge_text: "Zero Coding or Technical Background Required",
      heading: "Bridge Into Tech: Practical IT & AI Training for Non-Tech Students",
      sub_heading: "Tailored exclusively for Management, Humanities, Arts, Education, and Law students. Master modern AI tools, coding logic, web essentials, cybersecurity, and cloud workspace through 100% hands-on lab sessions at AIEMS Bardibas.",
      image: null,
      primary_btn_text: "Reserve Your Seat",
      primary_btn_url: "#trainingLeadForm",
      modules: [
        { id: 1, title: "1. AI Fundamentals", description: "ChatGPT, AI Prompting, smart research, and daily workflow automation.", icon_class: "fa-solid fa-brain" },
        { id: 2, title: "2. Coding Fundamentals", description: "Core programming logic, simplified Python, and algorithmic problem solving.", icon_class: "fa-solid fa-code" },
        { id: 3, title: "3. Web Development Basics", description: "HTML5, CSS3, modern page structures, domain hosting, and website design.", icon_class: "fa-solid fa-globe" },
        { id: 4, title: "4. Cybersecurity & Safety", description: "Password hygiene, scam prevention, account privacy, and safe digital transactions.", icon_class: "fa-solid fa-shield-halved" },
        { id: 5, title: "5. Networking Fundamentals", description: "Internet mechanics, IP addressing, WiFi setup, routers, and troubleshooting.", icon_class: "fa-solid fa-network-wired" },
        { id: 6, title: "6. Cloud Computing Basics", description: "Cloud storage, Google Workspace automation, intro to AWS/Azure concepts.", icon_class: "fa-solid fa-cloud" },
        { id: 7, title: "7. Digital Media", description: "Graphic design basics, UI/UX introduction, Canva/Figma, and presentation assets.", icon_class: "fa-solid fa-photo-film" }
      ],
      time_slots: [
        { id: 1, time_range: "4:00 PM - 5:00 PM", slot_tag: "Evening Slot A" },
        { id: 2, time_range: "5:00 PM - 6:00 PM", slot_tag: "Evening Slot B" },
        { id: 3, time_range: "6:00 PM - 7:00 PM", slot_tag: "Twilight Slot C" },
        { id: 4, time_range: "7:00 PM - 8:00 PM", slot_tag: "Night Slot D" }
      ],
      perks: [
        { id: 1, title: "Dedicated Computer Lab Setup", icon_class: "fa-solid fa-check" },
        { id: 2, title: "Printed Step-by-Step Cheatsheets", icon_class: "fa-solid fa-check" },
        { id: 3, title: "AIEMS Official Certificate", icon_class: "fa-solid fa-check" },
        { id: 4, title: "Career Guidance for Tech Degrees", icon_class: "fa-solid fa-check" }
      ],
      stream_options: [
        { id: 1, name: "+2 Management / BBS / BBA" },
        { id: 2, name: "+2 Humanities / BA / Social Sciences" },
        { id: 3, name: "+2 Education / B.Ed" },
        { id: 4, name: "+2 Law / B.A. LL.B" },
        { id: 5, name: "High School Graduate (Awaiting +2 Results)" },
        { id: 6, name: "Working Professional / Entrepreneur" },
        { id: 7, name: "Other Non-Technical Background" }
      ],
      timeframe_options: [
        { id: 1, name: "1 Month (Foundation Crash Course)" },
        { id: 2, name: "3 Months (Certificate Track — Recommended)" },
        { id: 3, name: "6 Months (Mastery & Project Track)" }
      ],
      delivery_modes: [
        { id: 1, name: "Physical Lab at AIEMS Campus, Bardibas" },
        { id: 2, name: "Hybrid (Physical Lab + Recorded Access)" }
      ],
      experience_levels: [
        { id: 1, name: "Absolute Beginner (Basic typing/browsing only)" },
        { id: 2, name: "Intermediate (Use MS Word, Email, Social Media daily)" },
        { id: 3, name: "Curious Explorer (Want career-ready digital skills)" }
      ],
      meta_title: "Practical IT & AI Training for Non-Technical Students | AIEMS Bardibas",
      meta_description: "Join AIEMS Bardibas for beginner-friendly IT & AI training. Master ChatGPT, Python coding logic, web design, cybersecurity, and cloud tools in hands-on labs.",
      meta_keywords: "AIEMS IT Training, AI Training Bardibas, Non-tech IT course, Python for beginners Nepal, Computer Training Bardibas",
      structured_data: null
    };
  }

  return {
    id: data.id ?? null,
    badge_text: data.badge_text || "Zero Coding or Technical Background Required",
    heading: data.heading || "Bridge Into Tech: Practical IT & AI Training for Non-Tech Students",
    sub_heading: data.sub_heading || "",
    image: data.image ? resolveMediaUrl(data.image) : null,
    primary_btn_text: data.primary_btn_text || "Reserve Your Seat",
    primary_btn_url: data.primary_btn_url || "#trainingLeadForm",
    modules: Array.isArray(data.modules) ? data.modules : [],
    time_slots: Array.isArray(data.time_slots) ? data.time_slots : [],
    perks: Array.isArray(data.perks) ? data.perks : [],
    stream_options: Array.isArray(data.stream_options) ? data.stream_options : [],
    timeframe_options: Array.isArray(data.timeframe_options) ? data.timeframe_options : [],
    delivery_modes: Array.isArray(data.delivery_modes) ? data.delivery_modes : [],
    experience_levels: Array.isArray(data.experience_levels) ? data.experience_levels : [],
    meta_title: data.meta_title || "",
    meta_description: data.meta_description || "",
    meta_keywords: data.meta_keywords || "",
    structured_data: data.structured_data || null
  };
}

/**
 * Retrieves compiled training page CMS payload directly from the Django backend.
 */
export async function getTrainingPageContent(options = {}) {
  const { bypassCache = false, revalidate = 3600 } = options;
  const endpoint = `${API_BASE_URL}/api/training/content/${bypassCache ? '?bypass_cache=true' : ''}`;

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
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    return normalizeTrainingContent(data);
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === "AbortError") {
      console.warn(`[AIEMS Training API] Timeout/Abort at ${endpoint}. Backend may be offline.`);
    } else {
      console.warn("[AIEMS Training API] Data retrieval fallback triggered:", error.message || error);
    }
    return normalizeTrainingContent(null);
  }
}

/**
 * Submits student lead registration payload to Django REST endpoint.
 */
export async function submitTrainingApplication(payload) {
  const url = `${API_BASE_URL}/api/training/apply/`;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
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
      let errorMessage = "Unable to submit application. Please check your details.";
      if (parsedData && typeof parsedData === "object") {
        if (parsedData.error) errorMessage = parsedData.error;
        else if (parsedData.detail) errorMessage = parsedData.detail;
        else {
          const firstKey = Object.keys(parsedData)[0];
          if (firstKey) {
            errorMessage = Array.isArray(parsedData[firstKey]) ? parsedData[firstKey][0] : parsedData[firstKey];
          }
        }
      }
      throw new Error(errorMessage);
    }

    return parsedData;
  } catch (error) {
    clearTimeout(timeoutId);
    throw error;
  }
}