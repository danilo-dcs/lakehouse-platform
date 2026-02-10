/// <reference types="vite/client" />
/// <reference types="vue/ref-macros" />

declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// PrimeVue type declarations
declare module 'primevue/config'
declare module 'primevue/toastservice'
declare module 'primevue/dialogservice'
declare module 'primevue/tooltip'
declare module '@primeuix/themes/aura'
