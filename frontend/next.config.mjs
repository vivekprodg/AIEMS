import { URL } from 'url';

/**
 * Parses the public API URL from system environment variables
 * to register dynamic image remote patterns matching production and local hosts.
 */
const getDynamicApiEndpoint = () => {
  const fallbackUrl = 'https://api.aiems.edu.np';
  const rawUrl = process.env.NEXT_PUBLIC_API_BASE_URL || fallbackUrl;

  try {
    const parsed = new URL(rawUrl);
    return {
      protocol: parsed.protocol.replace(':', ''),
      hostname: parsed.hostname,
      port: parsed.port || '',
    };
  } catch (error) {
    return {
      protocol: 'https',
      hostname: 'api.aiems.edu.np',
      port: '',
    };
  }
};

const apiOrigin = getDynamicApiEndpoint();

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  poweredByHeader: false,
  compress: true,

  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'api.aiems.edu.np',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: 'api.aiems.edu.np',
        port: '',
        pathname: '/**',
      },
      {
        protocol: apiOrigin.protocol,
        hostname: apiOrigin.hostname,
        port: apiOrigin.port,
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: '127.0.0.1',
        port: '8000',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
        port: '',
        pathname: '/**',
      },
    ],
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60,
    dangerouslyAllowSVG: true,
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },

  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload',
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=(), interest-cohort=()',
          },
        ],
      },
      {
        source: '/assets/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};

export default nextConfig;