// nuxt.config.ts

export default defineNuxtConfig({
  // Isto diz ao Nuxt para carregar o módulo Tailwind CSS que instalámos
  modules: [
    '@nuxtjs/tailwindcss'
  ],

  // Isto é para o modo de desenvolvimento, ajuda a recarregar mais rápido
  devtools: { enabled: true }

  // --- ADICIONE ISTO ---
  runtimeConfig: {
    public: {
      // Definimos o nome da nossa variável
      apiBase: 'http://127.0.0.1:8000/api/v1' // Valor padrão (para local)
    }
  }
  // --- FIM DA ADIÇÃO ---
})
})
