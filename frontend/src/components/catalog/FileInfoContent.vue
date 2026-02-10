<!-- FileInfoContent -->
<template>
  <Panel header="Description">
    <p class="mx-2">
      {{ file_details?.file_description }}
    </p>
  </Panel>
</template>

<script setup lang="ts">
import type { CatalogFileRecord } from '@/shared/interfaces/http/CatalogFileResponse'
import type { DynamicDialogInstance } from 'primevue/dynamicdialogoptions'
import Panel from 'primevue/panel'
import { onMounted, ref, inject, type Ref, computed } from 'vue'
const dialogRef = inject('dialogRef') as Ref<DynamicDialogInstance>

const file_details = ref<CatalogFileRecord>()

onMounted(() => {
  const param = dialogRef.value.data
  file_details.value = param as CatalogFileRecord
})
</script>
