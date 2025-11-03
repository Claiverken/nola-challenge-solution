// nuxt.config.ts

export default defineNuxtConfig({
  // Isto diz ao Nuxt para carregar o módulo Tailwind CSS que instalámos
  modules: [
    '@nuxtjs/tailwindcss'
  ],

  // Isto é para o modo de desenvolvimento, ajuda a recarregar mais rápido
  devtools: { enabled: true }
})
