"use client";

import { useState, useEffect } from "react";

/**
 * PWA Store Class (Singleton Pattern)
 * Centralizes browser PWA capabilities, handling installation lifecycle events,
 * connectivity status, background sync, and push notifications.
 */
class PWAStore {
  constructor() {
    this.listeners = new Set();
    this.state = {
      isSupported: false,
      isRegistered: false,
      isInstallable: false,
      isInstalled: false,
      updateAvailable: false,
      isOnline: true,
    };
    this.deferredPrompt = null;
    this.registration = null;

    if (typeof window !== "undefined") {
      this.state.isSupported = "serviceWorker" in navigator;
      this.state.isOnline = navigator.onLine;
      this.state.isInstalled = window.matchMedia("(display-mode: standalone)").matches;
      this.initListeners();
    }
  }

  /**
   * Safe initialization of standard window and navigator listeners.
   */
  initListeners() {
    window.addEventListener("online", () => this.setOnline(true));
    window.addEventListener("offline", () => this.setOnline(false));

    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.updateState({ isInstallable: true });
    });

    window.addEventListener("appinstalled", () => {
      console.log("[AIEMS PWA] App installed successfully.");
      this.deferredPrompt = null;
      this.updateState({ isInstallable: false, isInstalled: true });
    });

    const mediaQuery = window.matchMedia("(display-mode: standalone)");
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener("change", (e) => {
        this.updateState({ isInstalled: e.matches });
      });
    }
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  updateState(newState) {
    this.state = { ...this.state, ...newState };
    this.listeners.forEach((listener) => {
      try {
        listener(this.state);
      } catch (err) {
        console.error("[AIEMS PWA] Hook subscriber error:", err);
      }
    });
  }

  setOnline(status) {
    this.updateState({ isOnline: status });
  }

  /**
   * Registers sw.js with optional constraints for development environments.
   */
  register(options = {}) {
    const { dev = false } = options;
    const isDev = process.env.NODE_ENV === "development";

    if (!this.state.isSupported) {
      return;
    }

    if (isDev && !dev) {
      console.log("[AIEMS PWA] Service Worker registration skipped in development context.");
      return;
    }

    const registerWorker = () => {
      navigator.serviceWorker
        .register("/sw.js")
        .then((registration) => {
          this.registration = registration;
          this.updateState({ isRegistered: true });

          if (registration.waiting) {
            this.updateState({ updateAvailable: true });
          }

          registration.addEventListener("updatefound", () => {
            const installingWorker = registration.installing;
            if (!installingWorker) return;

            installingWorker.addEventListener("statechange", () => {
              if (installingWorker.state === "installed") {
                if (navigator.serviceWorker.controller) {
                  this.updateState({ updateAvailable: true });
                  console.log("[AIEMS PWA] New update is available for application shell.");
                }
              }
            });
          });
        })
        .catch((error) => {
          console.error("[AIEMS PWA] Service Worker registration failed:", error);
        });
    };

    if (document.readyState === "complete") {
      registerWorker();
    } else {
      window.addEventListener("load", registerWorker);
    }
  }

  /**
   * Prompts native home-screen installation layout if available.
   */
  async install() {
    if (!this.deferredPrompt) {
      console.warn("[AIEMS PWA] Installation prompt is currently unavailable.");
      return false;
    }
    try {
      this.deferredPrompt.prompt();
      const { outcome } = await this.deferredPrompt.userChoice;
      this.deferredPrompt = null;
      this.updateState({ isInstallable: false });
      return outcome === "accepted";
    } catch (err) {
      console.error("[AIEMS PWA] Failed to prompt client installation:", err);
      return false;
    }
  }

  /**
   * Sends SKIP_WAITING signal to waiting Service Worker and reloads safely.
   */
  update() {
    if (!this.registration || !this.registration.waiting) {
      return;
    }
    this.registration.waiting.postMessage({ type: "SKIP_WAITING" });

    navigator.serviceWorker.addEventListener("controllerchange", () => {
      window.location.reload();
    });
  }

  /**
   * Register a background sync transaction tag safely.
   */
  async registerSync(tag) {
    if (!this.state.isSupported || !this.registration) {
      throw new Error("Service Worker must be registered and active to queue sync actions.");
    }
    if (!("sync" in this.registration)) {
      throw new Error("Background Sync API is unsupported in this browser.");
    }
    try {
      await this.registration.sync.register(tag);
      console.log(`[AIEMS PWA] Sync trigger queued: ${tag}`);
    } catch (error) {
      console.error("[AIEMS PWA] Failed to queue sync target:", error);
      throw error;
    }
  }

  /**
   * Encapsulates Web Push subscription management.
   */
  async subscribePush(vapidPublicKey) {
    if (!this.state.isSupported || !this.registration) {
      throw new Error("PWA push utilities require an active Service Worker.");
    }
    try {
      const permission = await Notification.requestPermission();
      if (permission !== "granted") {
        throw new Error("Notification permission denied by user.");
      }

      const subscription = await this.registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: this.urlBase64ToUint8Array(vapidPublicKey),
      });

      return subscription;
    } catch (error) {
      console.error("[AIEMS PWA] Push registration failed:", error);
      throw error;
    }
  }

  urlBase64ToUint8Array(base64String) {
    const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding).replace(/\-/g, "+").replace(/_/g, "/");
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }
}

const serverFallbackStore = {
  state: {
    isSupported: false,
    isRegistered: false,
    isInstallable: false,
    isInstalled: false,
    updateAvailable: false,
    isOnline: true,
  },
  subscribe: () => () => {},
  register: () => {},
  install: async () => false,
  update: () => {},
  registerSync: async () => {},
  subscribePush: async () => {
    throw new Error("Server environments cannot execute Push Manager setups.");
  },
};

export const pwaStore = typeof window !== "undefined" ? new PWAStore() : serverFallbackStore;

/**
 * React Subscription Hook.
 */
export function usePWA() {
  const [pwaState, setPWAState] = useState(pwaStore.state);

  useEffect(() => {
    const unsubscribe = pwaStore.subscribe((state) => {
      setPWAState(state);
    });
    setPWAState(pwaStore.state);
    return unsubscribe;
  }, []);

  return {
    ...pwaState,
    installApp: () => pwaStore.install(),
    updateApp: () => pwaStore.update(),
    registerSync: (tag) => pwaStore.registerSync(tag),
    subscribePush: (vapidKey) => pwaStore.subscribePush(vapidKey),
  };
}

/**
 * PWARegistrar Declarative Component.
 */
export function PWARegistrar({ dev = false }) {
  useEffect(() => {
    pwaStore.register({ dev });
  }, [dev]);

  return null;
}