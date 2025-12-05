<script setup lang="ts">
import InputText from 'primevue/inputtext'
import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
import Toast from 'primevue/toast'
import Password from 'primevue/password'
import DynamicDialog from 'primevue/dynamicdialog'

import uiConf from '../assets/configs/ui.json'

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useDialog } from 'primevue/usedialog'

import type { UiConfigs } from '@/shared/interfaces/configs/UiConfigs'
import type { LoginResponse } from '@/shared/interfaces/http/LoginResponse'
import type { SourceConfigs } from '@/shared/interfaces/configs/SourceConfigs'

import SubscriptionForm from '@/components/login/SubscriptionForm.vue'
import PasswordRecoveryForm from '@/components/login/PasswordRecoveryForm.vue'

import { useUserStore } from '@/stores/userStore'
import { apiRequestHandler } from '@/shared/api/apiRequestHandler'

const userStore = useUserStore()

const dialog = useDialog()

const uiSettings: UiConfigs = uiConf

const pageTitle = ref(uiSettings.landing_page_title)
const pageText = ref(uiSettings.landing_page_text)

const toast = useToast()

// Reactive references with types
const formValues = ref({
  email: '',
  password: '',
})

const router = useRouter()

const dialogDefaultProps = {
  header: 'Product List',
  style: {
    width: '50vw',
  },
  breakpoints: {
    '960px': '75vw',
    '640px': '90vw',
  },
  modal: true,
}

const openSubscribeModal = (): void => {
  const dialogSpecs = {
    props: {
      ...dialogDefaultProps,
      header: 'Sign up to get started with Data Lakehouse',
      style: {
        width: '50vw',
      },
    },
    templates: {},
    modal: true,
    maximizable: true,
    breakpoints: { '960px': '75vw', '640px': '90vw' },
    onClose: () => {},
  }

  const dialogRef = dialog.open(SubscriptionForm, dialogSpecs)
}

const openPasswordRecoveryModal = (): void => {
  const dialogSpecs = {
    props: {
      ...dialogDefaultProps,
      header: 'Password Recovery',
      style: {
        width: '50vw',
      },
    },
    templates: {},
    modal: true,
    maximizable: true,
    breakpoints: { '960px': '75vw', '640px': '90vw' },
    onClose: () => {},
  }

  const dialogRef = dialog.open(PasswordRecoveryForm, dialogSpecs)
}

const loginOnSubmit = async (): Promise<void> => {
  try {
    if (!formValues.value.email || !formValues.value.password) {
      throw new Error('Empty Fields')
    }

    const url = '/auth/login'

    const body = {
      email: formValues.value.email,
      password: formValues.value.password,
    }

    const responseData = await apiRequestHandler<LoginResponse>(url, 'POST', body)

    userStore.setUser({
      email: formValues.value.email,
      role: responseData.user_role,
      userId: responseData.user_id,
      accessToken: responseData.access_token,
      refreshToken: responseData.refresh_token,
      tokenType: responseData.token_type,
    })

    // Redirect to home page
    router.push('/')
  } catch (err: unknown) {
    let error = ''
    if (err instanceof Error) {
      error = err.message
    } else {
      error = 'Login failed'
    }
    toast.add({
      severity: 'error',
      summary: 'Login error',
      detail: error,
      life: 4000,
    })
  }
}
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#3986c2] via-[#63a4da] to-[#ffffff] relative overflow-hidden"
  >
    <Toast />
    <DynamicDialog />

    <!-- Subtle Glow Overlay -->
    <div
      class="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.1),_transparent_50%)]"
    ></div>

    <div
      class="relative z-10 bg-white shadow-2xl rounded-2xl p-10 w-[90%] max-w-md flex flex-col items-center animate-fade-in"
    >
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-[#3986c2]">{{ pageTitle }}</h2>
        <Divider class="my-3" />
        <h1 class="text-gray-700 text-xl font-medium mt-2">{{ pageText }}</h1>
        <p class="text-gray-500 text-sm mt-3">Welcome! Please log into your account</p>
      </div>

      <div class="w-full space-y-5">
        <InputGroup>
          <InputGroupAddon>
            <i class="pi pi-envelope text-[#3986c2]"></i>
          </InputGroupAddon>
          <InputText
            id="email"
            v-model="formValues.email"
            class="w-full border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#3986c2]"
            type="email"
            placeholder="Email"
            required
          />
        </InputGroup>

        <InputGroup>
          <InputGroupAddon>
            <i class="pi pi-lock text-[#3986c2]"></i>
          </InputGroupAddon>
          <Password
            id="password"
            v-model="formValues.password"
            class="w-full border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#3986c2]"
            placeholder="Password"
            toggleMask
            :feedback="false"
            required
          />
        </InputGroup>

        <div class="flex justify-end">
          <Button
            variant="text"
            size="small"
            @click="openPasswordRecoveryModal()"
            label="Forgot Password?"
          />
        </div>

        <div class="space-y-4 mt-12">
          <Button
            class="w-full border-none bg-[#3986c2] hover:bg-[#4a92cf] text-white font-semibold py-2 rounded-md shadow-md active:scale-95 transition duration-150"
            @click="loginOnSubmit"
            label="Login"
          />
          <Button
            class="w-full border-none bg-gray-800 hover:bg-gray-700 text-white font-semibold py-2 rounded-md shadow-md active:scale-95 transition duration-150"
            @click="openSubscribeModal()"
            label="Subscribe"
          />
        </div>
      </div>

      <p class="text-gray-500 text-sm mt-8">© {{ new Date().getFullYear() }} INFORM Africa Hub</p>
    </div>
  </div>
</template>
