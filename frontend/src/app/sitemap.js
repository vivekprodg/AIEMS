const API_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL || "https://api.aiems.edu.np").replace(/\/+$/, "");
const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || "https://aiems.edu.np").replace(/\/+$/, "");

/**
 * Safely fetches dataset items from target CMS API endpoints.
 */
async function fetchSitemapData(endpoint) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      next: { revalidate: 3600 },
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
    });

    if (!response.ok) {
      return [];
    }

    const data = await response.json();
    return Array.isArray(data) ? data : data?.results || [];
  } catch (error) {
    console.error(`Sitemap data resolution skipped for ${endpoint}:`, error);
    return [];
  }
}

/**
 * Next.js App Router Sitemap Generator.
 * Generates an indexable XML map of static and dynamic educational entities.
 */
export default async function sitemap() {
  const staticPages = [
    {
      url: `${SITE_URL}`,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1.0,
    },
    {
      url: `${SITE_URL}/home`,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 0.9,
    },
    {
      url: `${SITE_URL}/about-us`,
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 0.9,
    },
    {
      url: `${SITE_URL}/apply-now`,
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 0.8,
    },
    {
      url: `${SITE_URL}/faqs`,
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 0.7,
    },
    {
      url: `${SITE_URL}/contact-us`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.7,
    },
    {
      url: `${SITE_URL}/privacy-policy`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.3,
    },
    {
      url: `${SITE_URL}/terms-and-conditions`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.3,
    },
  ];

  const [programs, faculties] = await Promise.all([
    fetchSitemapData("/api/home/programs/"),
    fetchSitemapData("/api/home/teamfaculties/"),
  ]);

  const programPages = programs.map((program) => ({
    url: `${SITE_URL}/programs/${program.id}`,
    lastModified: program.created_at ? new Date(program.created_at) : new Date(),
    changeFrequency: "weekly",
    priority: 0.9,
  }));

  const careerPages = faculties.map((faculty) => ({
    url: `${SITE_URL}/apply-for-job/${faculty.id}`,
    lastModified: faculty.created_at ? new Date(faculty.created_at) : new Date(),
    changeFrequency: "weekly",
    priority: 0.6,
  }));

  return [...staticPages, ...programPages, ...careerPages];
}