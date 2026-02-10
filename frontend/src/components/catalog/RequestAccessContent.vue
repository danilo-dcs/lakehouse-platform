<!-- RequestAccessContent -->

<script setup lang="ts">
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import { useToast } from 'primevue'

import type { CatalogCollectionRecord } from '@/shared/interfaces/http/CatalogCollectionResponse'
import type { DynamicDialogInstance } from 'primevue/dynamicdialogoptions'
import { onMounted, ref, inject, type Ref, computed } from 'vue'
import type {
  AccessRequestModel,
  AccessRequestSearchResponse,
} from '@/shared/interfaces/http/AccessRequestSearchResponse'
import type { AccessRequestSearchPayload } from '@/shared/interfaces/http/AccessRequestSearchPayload'
import type { AccessRequestCreateResponse } from '@/shared/interfaces/http/AccessRequestCreateResponse'
import { useRouter } from 'vue-router'

import { useUserStore } from '@/stores/userStore'
import { apiRequestHandler } from '@/shared/api/apiRequestHandler'

const userStore = useUserStore()

const toast = useToast()
const router = useRouter()

const dialogRef = inject('dialogRef') as Ref<DynamicDialogInstance>

const collection = ref<CatalogCollectionRecord>()

const user_id = computed(() => userStore.userId)

const userAccessRequests = ref<AccessRequestSearchResponse>()

const sendButtonLoading = ref<boolean>(false)

// LIFECYCLE
onMounted(() => {
  const param = dialogRef.value.data
  collection.value = param as CatalogCollectionRecord

  fetchAccessRequestData()
})

// ACTIONS

const wasRequested = (): boolean => {
  const lastRequest = userAccessRequests.value?.access_requests[0] ?? ({} as AccessRequestModel)

  if (!lastRequest || Object.keys(lastRequest).length === 0) {
    return false
  }

  if (lastRequest && lastRequest.status !== 'requested') {
    return false
  }

  return true
}

const hasDeclinedRequests = (): boolean => {
  const lastRequest = userAccessRequests.value?.access_requests ?? ([] as AccessRequestModel[])

  if (!lastRequest || lastRequest.length === 0) {
    return false
  }

  const declinedRequests = lastRequest.some((item) => item.status === 'revoked')

  return declinedRequests
}

const sendReequest = async () => {
  sendButtonLoading.value = true

  const newRequest = await createAccessRequest()

  toast.add({
    severity: 'success',
    summary: 'Success',
    detail: 'Access requeset successfully sent',
    life: 4000,
  })
  sendButtonLoading.value = false
}

// API REQUESTS

const createAccessRequest = async (): Promise<AccessRequestCreateResponse> => {
  const url = '/access-request/create'

  const [owner_id, ...rest] = collection.value?.inserted_by.split(':')!

  const body = {
    collection_id: collection.value?.id,
    requested_by: user_id.value,
    owner_id: owner_id,
  }

  const responseData = await apiRequestHandler<AccessRequestCreateResponse>(url, 'POST', body)

  return responseData
}

const fetchAccessRequestData = async () => {
  const url = '/access-request/search'

  const body: AccessRequestSearchPayload = {
    collection_id: collection.value?.id,
    requested_by: user_id.value || undefined,
  }

  const responseData = await apiRequestHandler<AccessRequestSearchResponse>(url, 'POST', body)

  userAccessRequests.value = responseData
}

const closeDialog = () => {
  dialogRef.value.close()
}
</script>

<template>
  <Toast />
  <div class="flex flex-column justify-center" v-if="wasRequested()">
    <span>
      <i class="pi pi-lock-open text-green-500 mr-4"></i>
      <b>You have already requested access to this collection. Please wait for approval</b>
    </span>
  </div>
  <div class="flex flex-column justify-center mt-5" v-else>
    <div class="flex flex-col items-center">
      <p class="mb-4 text-center">Request access by sending an email to the collection's owner</p>
      <Button
        class="mt-5"
        icon="pi pi-envelope"
        severity="bg-primary-500"
        label="Send"
        @click="sendReequest()"
        :loading="sendButtonLoading"
      />
    </div>
  </div>
  <div v-if="hasDeclinedRequests()" class="mt-10 bg-orange-200 rounded-lg p-4 flex items-center">
    <i class="pi pi-exclamation-circle text-orange-400 mr-2"></i>
    <b>Your previous access was declined</b>
  </div>
</template>
