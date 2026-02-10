<!-- ControlAccessContent -->

<script setup lang="ts">
import DataView from 'primevue/dataview'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import Chip from 'primevue/chip'
import Tag from 'primevue/tag'

import { onMounted, ref, inject, nextTick, type Ref, computed } from 'vue'
import type { DynamicDialogInstance } from 'primevue/dynamicdialogoptions'
import { useToast } from 'primevue'

import type { CatalogCollectionRecord } from '@/shared/interfaces/http/CatalogCollectionResponse'

import type { AccessRequestSearchPayload } from '@/shared/interfaces/http/AccessRequestSearchPayload'
import type {
  AccessRequestModel,
  AccessRequestSearchResponse,
} from '@/shared/interfaces/http/AccessRequestSearchResponse'
import moment from 'moment'

import { useUserStore } from '@/stores/userStore'
import { apiRequestHandler } from '@/shared/api/apiRequestHandler'

const userStore = useUserStore()

const dialogRef = inject('dialogRef') as Ref<DynamicDialogInstance>

const toast = useToast()
const user_id = computed(() => userStore.userId)

const collection = ref<CatalogCollectionRecord>()

const latestAccessRequests = ref<AccessRequestModel[]>([])

const loadingGrantButton = ref<boolean>(false)
const loadingRevokeButton = ref<boolean>(false)

const statusOptions = {
  requested: 'requested',
  granted: 'granted',
  revoked: 'revoked',
}

// LIFECYCLE

onMounted(() => {
  const param = dialogRef.value.data
  collection.value = param as CatalogCollectionRecord

  refreshList()
})

// ACTIONS
const getStatusColor = (status: string): string => {
  return status === statusOptions.granted
    ? 'bg-emerald-500'
    : status === statusOptions.requested
      ? 'bg-amber-400'
      : 'bg-red-400'
}

const refreshList = () => {
  fetchAccessRequestData()
}

const formatUnixDate = (timestamp: number): string => {
  return moment.unix(timestamp).format('YYYY-MM-DD')
}

const filterAccessRequestPerUser = (data: AccessRequestSearchResponse): AccessRequestModel[] => {
  if (data.access_requests.length === 0) {
    return [] as AccessRequestModel[]
  }

  const unique_ids = new Set(data.access_requests.map((item) => item.requested_by))

  const requestor_ids = [...unique_ids]

  let access_requests = [] as AccessRequestModel[]

  requestor_ids.forEach((id) => {
    const access_per_user = data.access_requests.filter((item) => item.requested_by === id)

    const ordered_per_user = access_per_user.sort(
      (item1, item2) => item2.requested_at - item1.requested_at,
    )

    access_requests.push(ordered_per_user[0])
  })

  access_requests = access_requests.filter((item) => item.status !== statusOptions.revoked)

  return access_requests
}

const grantAccessAction = async (data: AccessRequestModel) => {
  loadingGrantButton.value = true

  await grantAccessRequest(data.id)

  loadingGrantButton.value = false
  toast.add({
    severity: 'success',
    summary: 'Success',
    detail: 'Access granted',
    life: 4000,
  })
  refreshList()
}

const revokeAccessAction = async (data: AccessRequestModel) => {
  loadingRevokeButton.value = true

  await revokeAccessRequest(data.id)

  loadingRevokeButton.value = false

  toast.add({
    severity: 'success',
    summary: 'Success',
    detail: 'Access revoked',
    life: 4000,
  })
  refreshList()
}

// API REQUESTS

const fetchAccessRequestData = async () => {
  const url = '/access-request/search'

  const body: AccessRequestSearchPayload = {
    collection_id: collection.value?.id,
    owner_id: user_id.value || undefined,
  }

  const responseData = await apiRequestHandler<AccessRequestSearchResponse>(url, 'POST', body)

  latestAccessRequests.value = filterAccessRequestPerUser(responseData)
}

const grantAccessRequest = async (access_request_id: string) => {
  const url = '/access-request/grant'

  const body = { access_request_id }

  await apiRequestHandler<AccessRequestSearchResponse>(url, 'POST', body)

  refreshList()
}

const revokeAccessRequest = async (access_request_id: string) => {
  const url = '/access-request/revoke'

  const body = { access_request_id }

  await apiRequestHandler<AccessRequestSearchResponse>(url, 'POST', body)

  refreshList()
}
</script>

<template>
  <Toast />
  <DataView :value="latestAccessRequests" data-key="collection">
    <template #empty> No Access Requests </template>
    <template #list="slotProps">
      <div class="flex flex-col">
        <div v-for="(item, index) in slotProps.items" :key="index" class="hover:bg-gray-50">
          <div
            class="flex flex-col sm:flex-row sm:items-center p-6 gap-4"
            :class="{ 'border-t border-surface-200 dark:border-surface-700': index !== 0 }"
          >
            <div class="flex flex-col md:flex-row justify-between md:items-center flex-1 gap-6">
              <div class="flex items-center">
                <div class="w-1 h-12 mr-4" :class="getStatusColor(item.status)"></div>
                <div>
                  <span class="font-medium text-surface-500 dark:text-surface-400 text-sm"
                    >Email:</span
                  >
                  <div class="text-lg font-medium mt-2">{{ item.requestor_email }}</div>
                </div>
              </div>

              <div class="flex items-center">
                <div>
                  <span class="font-medium text-surface-500 dark:text-surface-400 text-sm"
                    >Status:</span
                  >
                  <div>
                    <Chip
                      :label="String(item.status).toUpperCase()"
                      class="text-white"
                      :class="getStatusColor(item.status)"
                    />
                  </div>
                </div>
              </div>

              <div class="flex items-center">
                <div>
                  <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">
                    {{ item.status === statusOptions.granted ? 'Granted at:' : 'Requested at:' }}
                  </span>
                  <div>
                    <Tag :value="formatUnixDate(Number(item.requested_at))" />
                  </div>
                </div>
              </div>

              <div class="flex items-center">
                <div>
                  <span class="font-medium text-surface-500 dark:text-surface-400 text-sm"
                    >Actions:</span
                  >
                  <div class="flex flex-row-reverse md:flex-row gap-2">
                    <Button
                      v-if="item.status === statusOptions.requested"
                      class="text-green-500 bg-green-50 border-green-500 hover:bg-green-100"
                      icon="pi pi-check"
                      outlined
                      :loading="loadingGrantButton"
                      :disabled="loadingRevokeButton"
                      v-tooltip.bottom="'Grant access'"
                      @click="grantAccessAction(item)"
                      size="small"
                    ></Button>
                    <Button
                      class="text-red-500 bg-red-50 border-red-500 hover:bg-red-100"
                      icon="pi pi-times"
                      outlined
                      v-tooltip.bottom="'Revoke/Reject access'"
                      :loading="loadingRevokeButton"
                      :disabled="loadingGrantButton"
                      @click="revokeAccessAction(item)"
                      size="small"
                    ></Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </DataView>
</template>
