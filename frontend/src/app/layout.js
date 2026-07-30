import { Geist, Geist_Mono, Roboto, Poppins, Inter, Roboto_Mono } from "next/font/google";
import "./globals.scss";
import "../assets/sass/style.scss";
import { ConfigProvider } from "antd";
import { AntdRegistry } from "@ant-design/nextjs-registry";
import { PWARegistrar } from "@/lib/pwa/register-sw";

// ==============================================================================
// TYPOGRAPHY CONFIGURATION
// ==============================================================================
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const poppins = Poppins({
  subsets: ["latin"],
  variable: "--font-poppins",
  weight: ["300", "400", "500", "600", "700", "800"],
  style: ["normal", "italic"],
  display: "swap",
});

const robotoMono = Roboto_Mono({
  subsets: ["latin"],
  variable: "--font-roboto-mono",
  display: "swap",
  weight: ["400", "700"],
});

const roboto = Roboto({
  subsets: ["latin"],
  variable: "--font-roboto",
  weight: ["400", "700"],
  style: ["normal", "italic"],
  display: "swap",
});

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  display: "swap",
});

// ==============================================================================
// ENTERPRISE METADATA & OPEN GRAPH OPTIMIZATION
// ==============================================================================
export const metadata = {
  title: {
    default: "AIEMS — Ankur Institute of Engineering and Management Studies",
    template: "%s | AIEMS",
  },
  description: "Ankur Institute of Engineering and Management Studies (AIEMS) — Brand new technical college offering RJU affiliated BSc. CSIT in Bardibas, Nepal.",
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "https://aiems.edu.np"),
  keywords: [
    "AIEMS",
    "Ankur Institute of Engineering and Management Studies",
    "BSc. CSIT Admissions",
    "BSc CSIT College Nepal",
    "RJU Affiliated CSIT",
    "Rajarshi Janak University",
    "IT Education Bardibas",
    "Computer Science College Bardibas",
  ],
  authors: [{ name: "AIEMS Academic Team", url: "https://aiems.edu.np" }],
  creator: "AIEMS",
  publisher: "Ankur Institute of Engineering and Management Studies",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    title: "AIEMS — Ankur Institute of Engineering and Management Studies",
    description: "Join AIEMS for RJU-affiliated BSc. CSIT in Bardibas. Hands-on practical computer science labs and industry-experienced faculty.",
    url: "https://aiems.edu.np",
    siteName: "AIEMS",
    images: [
      {
        url: "/assets/banner1.jpg",
        width: 1200,
        height: 630,
        alt: "AIEMS Technical Campus Bardibas",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "AIEMS — Ankur Institute of Engineering and Management Studies",
    description: "Offering RJU Affiliated BSc. CSIT in Bardibas, Nepal. Empowering students through core computer science education.",
    images: ["/assets/banner1.jpg"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "AIEMS",
  },
};

// ==============================================================================
// VIEWPORT & DISPLAY COMPATIBILITY
// ==============================================================================
export const viewport = {
  themeColor: "#009444",
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

// ==============================================================================
// ROOT APPLICATION SHELL
// ==============================================================================
export default function RootLayout({ children }) {
  return (
    <html lang="en" className="scroll-smooth">
      <body
        className={`
          ${inter.variable} 
          ${poppins.variable} 
          ${geistSans.variable} 
          ${geistMono.variable} 
          ${roboto.variable} 
          ${robotoMono.variable} 
          font-sans bg-surface text-slate-800 antialiased selection:bg-primary selection:text-white
        `.trim()}
      >
        <AntdRegistry>
          <ConfigProvider
            theme={{
              token: {
                colorPrimary: "#009444",
                colorLink: "#009444",
                borderRadius: 8,
                fontFamily: "var(--font-inter), sans-serif",
              },
              components: {
                Button: {
                  colorPrimaryHover: "#007a36",
                  defaultHoverBg: "",
                },
              },
            }}
          >
            {/* Service worker registration disabled during development to prevent localhost hangs */}
            <PWARegistrar dev={false} />
            {children}
          </ConfigProvider>
        </AntdRegistry>
      </body>
    </html>
  );
}