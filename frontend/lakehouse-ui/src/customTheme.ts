import Aura from '@primeuix/themes/aura'
import { definePreset } from '@primeuix/themes'
import { palette } from '@primeuix/themes'

import uiConfig from '@/assets/configs/ui.json'

const primaryPalette = palette(String(uiConfig.primary_color))

export const CustomTheme = definePreset(Aura, {
  semantic: {
    primary: primaryPalette,
  },
  colorScheme: {
    light: {
      formField: {
        hoverBorderColor: '{primary.color}',
      },
    },
    dark: {
      formField: {
        hoverBorderColor: '{primary.color}',
      },
    },
  },
})
