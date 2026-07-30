/**
 * AIEMS Search Engine & Crawler Configuration (robots.txt Generator)
 * Follows Next.js App Router dynamic metadata conventions to serve environment-aware directives.
 * 
 * Configures indexation rules dynamically based on environments:
 * - Production: Custom directives allowing optimized crawling of academic profiles, programs, and news events.
 * - Staging / Dev: Standard global disallow block to preserve crawl budget and prevent indexing search result duplication.
 */
export default function robots() {
  // Leverage the same fallback configuration as the dynamic sitemap builder
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://aiems.edu.np';
  
  // Identify environment variables to prevent search engines from parsing development, testing, or staging servers
  const isStagingOrDev =
    process.env.NEXT_PUBLIC_IS_STAGING === 'true' ||
    process.env.NODE_ENV !== 'production';

  if (isStagingOrDev) {
    return {
      rules: {
        userAgent: '*',
        disallow: '/',
      },
    };
  }

  return {
    rules: [
      {
        userAgent: '*',
        // Explicitly white-list verified public pathways extracted from the institutional router structure
        allow: [
          '/',
          '/home',
          '/about-us',
          '/apply-now',
          '/contact-us',
          '/programs/',
          '/apply-for-job/',
        ],
        // Safely restrict system directories, internal static build outputs, and query-parameter loops
        disallow: [
          '/_next/',       // Next.js client-side asset optimization directories
          '/api/',         // Client-side endpoint proxies
          '/*?*',          // Limit parameterized crawl loops (tracking links, filter parameters, etc.)
          '/static/img/',  // Backend media assets served directly from storage layers
        ],
      },
      {
        // Explicit constraints for generative artificial intelligence content-scraping agents
        userAgent: ['GPTBot', 'ChatGPT-User', 'CCBot', 'Google-Extended'],
        disallow: [
          '/apply-now',
          '/contact-us',
          '/apply-for-job/',
        ],
      }
    ],
    sitemap: `${siteUrl}/sitemap.xml`,
    host: siteUrl,
  };
}