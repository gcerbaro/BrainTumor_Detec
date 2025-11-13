// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  ssr: false,
  devtools: { enabled: true },
  modules: ["@nuxt/eslint", "@nuxt/ui", "nuxt-viewport"],
  css: ["~/assets/css/main.css"],
  app: {
    head: {
      title: "Detector de Tumores Cerebrais",
      htmlAttrs: {
        lang: "pt-BR",
      },
    },
  },
  viewport: {
    breakpoints: {
      xs: 320,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
      "2xl": 1536,
    },

    defaultBreakpoints: {
      desktop: "lg",
      mobile: "xs",
      tablet: "md",
    },

    fallbackBreakpoint: "lg",
  },
  runtimeConfig: {
    public: {
      apiBaseURL: "http://localhost:5000",
    },
  },
});
