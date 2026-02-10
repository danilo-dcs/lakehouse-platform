import '@/assets/styles/style.css'

import 'primeicons/primeicons.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import router from '@/router'

import PrimeVue from 'primevue/config'
import DialogService from 'primevue/dialogservice'
import ToastService from 'primevue/toastservice'
import Tooltip from 'primevue/tooltip'

import { CustomTheme } from '@/customTheme'

const piniaStores = createPinia()

const app = createApp(App)

app.use(piniaStores)
app.use(DialogService)
app.use(ToastService)

app.directive('tooltip', Tooltip)

// app.use(createPinia())

app.use(PrimeVue, {
  theme: {
    preset: CustomTheme,
    options: {
      prefix: 'p',
      darkModeSelector: 'none',
      cssLayer: {
        name: 'primevue',
        order: 'theme, base, primevue',
      },
    },
  },
})

app.use(router)

app.mount('#app')
