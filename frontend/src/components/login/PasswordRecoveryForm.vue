<script setup lang="ts">
import { inject, ref, type Ref } from 'vue'
import InputText from 'primevue/inputtext'
import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import Password from 'primevue/password'
import Button from 'primevue/button'

import Stepper from 'primevue/stepper'
import StepList from 'primevue/steplist'
import StepPanels from 'primevue/steppanels'
import Step from 'primevue/step'
import StepPanel from 'primevue/steppanel'

import { useToast } from 'primevue/usetoast'

import type { PasswordRecoveryRequest } from '@/shared/interfaces/http/PasswordRecoveryRequest'
import type { PasswordChangeRequest } from '@/shared/interfaces/http/PasswordChangeRequest'
import type { DynamicDialogInstance } from 'primevue/dynamicdialogoptions'
import { apiRequestHandler } from '@/shared/api/apiRequestHandler'

const toast = useToast()

const dialogRef = inject('dialogRef') as Ref<DynamicDialogInstance>

const form = ref({
  email: '',
  new_password: '',
  new_password_confirm: '',
  token: '',
})

const activeStep = ref(1)

const passwordRecoveryRequest = async (userData: PasswordRecoveryRequest) => {
  const url = `/user/password-recovery`
  await apiRequestHandler<any>(url, 'POST', userData)
}

const passwordChangeRequest = async (userData: PasswordChangeRequest) => {
  const url = `/user/password-change`
  await apiRequestHandler<any>(url, 'POST', userData)
}

const handleStep1 = async (goNext: () => void) => {
  if (!form.value.email) {
    toast.add({
      severity: 'warn',
      summary: 'Missing Email',
      detail: 'Please provide your email address.',
      life: 3000,
    })
    return
  }

  await passwordRecoveryRequest({ user_email: form.value.email })

  toast.add({
    severity: 'success',
    summary: 'Email Sent',
    detail: 'Check your email for the recovery token.',
    life: 4000,
  })

  goNext()
}

const handleStep2 = async (goNext: () => void) => {
  const { new_password, new_password_confirm, token } = form.value
  if (!new_password || !new_password_confirm || !token) {
    toast.add({
      severity: 'warn',
      summary: 'Missing Fields',
      detail: 'Please fill all fields.',
      life: 3000,
    })
    return
  }
  if (new_password !== new_password_confirm) {
    toast.add({
      severity: 'error',
      summary: 'Password Mismatch',
      detail: 'Passwords do not match.',
      life: 4000,
    })
    return
  }

  await passwordChangeRequest({ new_password, token })
  toast.add({
    severity: 'success',
    summary: 'Password Changed',
    detail: 'You can now log in with your new password.',
    life: 4000,
  })

  goNext()
}

const closeDialog = () => dialogRef.value.close()
</script>

<template>
  <div class="card flex justify-center">
    <Stepper v-model:value="activeStep" :linear="true" class="basis-[50rem]">
      <StepList>
        <Step :value="1">Request</Step>
        <Step :value="2">Confirm</Step>
        <Step :value="3">Finish</Step>
      </StepList>

      <StepPanels>
        <StepPanel v-slot="{ activateCallback }" :value="1">
          <div class="flex flex-col gap-6 mt-6">
            <span class="text-gray-700 text-center">
              Enter your registered email to receive a recovery token.
            </span>

            <InputGroup>
              <InputGroupAddon><i class="pi pi-envelope text-[#3986c2]"></i></InputGroupAddon>
              <InputText
                v-model="form.email"
                placeholder="Email"
                class="w-full border-gray-300 rounded-md focus:ring-2 focus:ring-[#3986c2]"
              />
            </InputGroup>

            <Button
              label="Send Recovery Email"
              class="w-full bg-[#3986c2] hover:bg-[#4a92cf] border-none text-white font-semibold"
              @click="() => handleStep1(() => activateCallback(2))"
            />
          </div>
        </StepPanel>

        <!-- step index 1 -->
        <StepPanel v-slot="{ activateCallback }" :value="2">
          <div class="flex flex-col gap-6 mt-6">
            <span class="text-gray-700 text-center">
              Enter the recovery token and your new password below.
            </span>

            <InputGroup>
              <InputGroupAddon><i class="pi pi-lock text-[#3986c2]"></i></InputGroupAddon>
              <Password
                v-model="form.new_password"
                placeholder="New Password"
                toggleMask
                :feedback="false"
                class="w-full border-gray-300 rounded-md focus:ring-2 focus:ring-[#3986c2]"
              />
            </InputGroup>

            <InputGroup>
              <InputGroupAddon><i class="pi pi-check-circle text-[#3986c2]"></i></InputGroupAddon>
              <Password
                v-model="form.new_password_confirm"
                placeholder="Confirm Password"
                toggleMask
                :feedback="false"
                class="w-full border-gray-300 rounded-md focus:ring-2 focus:ring-[#3986c2]"
              />
            </InputGroup>

            <InputGroup>
              <InputGroupAddon><i class="pi pi-key text-[#3986c2]"></i></InputGroupAddon>
              <InputText
                v-model="form.token"
                placeholder="Recovery Token"
                class="w-full border-gray-300 rounded-md focus:ring-2 focus:ring-[#3986c2]"
              />
            </InputGroup>

            <Button
              label="Change Password"
              class="w-full bg-[#3986c2] hover:bg-[#4a92cf] border-none text-white font-semibold"
              @click="() => handleStep2(() => activateCallback(3))"
            />
          </div>
        </StepPanel>

        <StepPanel :value="3">
          <div class="flex flex-col items-center justify-center mt-10 text-center">
            <i class="pi pi-check-circle text-green-500 text-6xl mb-4"></i>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Password Reset Successful!</h3>
            <p class="text-gray-600 mb-8">You can now log in with your new password.</p>
            <Button
              label="Close"
              class="bg-[#3986c2] hover:bg-[#4a92cf] border-none text-white font-semibold px-6"
              @click="closeDialog"
            />
          </div>
        </StepPanel>
      </StepPanels>
    </Stepper>
  </div>
</template>
