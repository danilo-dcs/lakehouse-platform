// tailwind.config.js
import PrimeUI from 'tailwindcss-primeui'

import uiConfig from './src/assets/configs/ui.json'

export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        primary: uiConfig.primary_color,
      },
      fontFamily: {
        abel: ['Abel', 'sans-serif'],
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [PrimeUI],
}
