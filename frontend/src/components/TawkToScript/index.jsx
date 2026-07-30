"use client";

import { useEffect } from "react";

/**
 * TawkToScript Component
 * Dynamically loads the Tawk.to live chat widget and enforces a minimal,
 * non-intrusive widget state upon initialization.
 */
const TawkToScript = () => {
  useEffect(() => {
    const scriptId = "tawk-to-script";

    // Initialize Tawk_API global configuration
    window.Tawk_API = window.Tawk_API || {};
    window.Tawk_LoadStart = new Date();

    // Enforce minimal widget state as soon as Tawk loads
    window.Tawk_API.onLoad = function () {
      if (typeof window.Tawk_API.minimize === "function") {
        window.Tawk_API.minimize();
      }
    };

    // Avoid duplicate script insertions
    if (document.getElementById(scriptId)) return;

    const s1 = document.createElement("script");
    s1.id = scriptId;
    s1.async = true;
    s1.src = "https://embed.tawk.to/6a6b7d0700c8c61d49f132ee/1jupu0q4t";
    s1.charset = "UTF-8";
    s1.setAttribute("crossorigin", "*");

    document.body.appendChild(s1);

    return () => {
      const existingScript = document.getElementById(scriptId);
      if (existingScript) {
        existingScript.remove();
      }
    };
  }, []);

  return null;
};

export default TawkToScript;