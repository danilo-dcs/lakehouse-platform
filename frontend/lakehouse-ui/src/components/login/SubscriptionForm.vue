<script setup lang="ts">
import { ref, inject, type Ref } from 'vue'
import InputText from 'primevue/inputtext'
import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import Password from 'primevue/password'
import Button from 'primevue/button'
import { useToast } from 'primevue/usetoast'
import type { DynamicDialogInstance } from 'primevue/dynamicdialogoptions'
import type { CreateUserPayload } from '@/shared/interfaces/http/CreateUserPayload'

import { useRouter } from 'vue-router'
import { apiRequestHandler } from '@/shared/api/apiRequestHandler'

const dialogRef = inject('dialogRef') as Ref<DynamicDialogInstance>

const toast = useToast()

const router = useRouter()

const form = ref({
  name: '',
  affiliation: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const createUserRequest = async (userData: CreateUserPayload) => {
  try {
    const url = `/user/create`
    await apiRequestHandler<any>(url, 'POST', userData)
  } catch (error) {
    console.error('Fetch error:', error)
    toast.add({
      severity: 'error',
      summary: 'Unable to reach server',
      detail: String(error),
      life: 4000,
    })
  }
}

const handleSubmit = async () => {
  if (
    !form.value.email ||
    !form.value.password ||
    !form.value.confirmPassword ||
    !form.value.name ||
    !form.value.affiliation
  ) {
    toast.add({
      severity: 'warn',
      summary: 'Missing fields',
      detail: 'Please fill all fields',
      life: 3000,
    })
  }

  if (form.value.password !== form.value.confirmPassword) {
    toast.add({
      severity: 'error',
      summary: 'Password mismatch',
      detail: 'Passwords do not match',
      life: 3000,
    })
    return
  }

  await createUserRequest({
    name: form.value.name,
    affiliation: form.value.affiliation,
    email: form.value.email,
    password: form.value.password,
  })

  toast.add({
    severity: 'success',
    summary: 'User created successfully',
    detail: 'Please login with your new account',
    life: 4000,
  })

  closeDialog()
}

const closeDialog = () => {
  dialogRef.value.close()
}
</script>

<template>
  <div>
    <div class="w-full space-y-5">
      <InputGroup>
        <InputGroupAddon>
          <i class="pi pi-user text-[#3986c2]"></i>
        </InputGroupAddon>
        <InputText
          v-model="form.name"
          type="text"
          placeholder="Name"
          class="w-full border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#3986c2]"
          required
        />
      </InputGroup>

      <InputGroup>
        <InputGroupAddon>
          <i class="pi pi-address-book text-[#3986c2]"></i>
        </InputGroupAddon>
        <InputText
          v-model="form.affiliation"
          type="text"
          placeholder="Affiliation"
          class="w-full border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#3986c2]"
          required
        />
      </InputGroup>

      <InputGroup>
        <InputGroupAddon>
          <i class="pi pi-envelope text-[#3986c2]"></i>
        </InputGroupAddon>
        <InputText
          v-model="form.email"
          type="email"
          placeholder="Email"
          class="w-full border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#3986c2]"
          required
        />
      </InputGroup>

      <InputGroup>
        <InputGroupAddon>
          <i class="pi pi-lock text-[#3986c2]"></i>
        </InputGroupAddon>
        <Password
          v-model="form.password"
          placeholder="Password"
          toggleMask
          :feedback="false"
          class="w-full border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#3986c2]"
          required
        />
      </InputGroup>

      <InputGroup>
        <InputGroupAddon>
          <i class="pi pi-check-circle text-[#3986c2]"></i>
        </InputGroupAddon>
        <Password
          v-model="form.confirmPassword"
          placeholder="Confirm Password"
          toggleMask
          :feedback="false"
          class="w-full border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#3986c2]"
          required
        />
      </InputGroup>

      <Button
        label="Sign Up"
        class="w-full border-none bg-[#3986c2] hover:bg-[#4a92cf] text-white font-semibold py-2 rounded-md shadow-md active:scale-95 transition duration-150"
        @click="handleSubmit"
      />
    </div>

    <p class="text-gray-500 text-sm mt-8">
      Already have an account?
      <Button to="/login" variant="text" size="small" @click="closeDialog()"> Login here </Button>
    </p>
  </div>
</template>
