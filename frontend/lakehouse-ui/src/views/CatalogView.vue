<script setup lang="ts">
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import Toast from 'primevue/toast'

import CollectionsTable from '@/components/catalog/CollectionsTable.vue'
</script>

<template>
  <div id="container" class="flex flex-col items-center w-full bg-stone-100">
    <Toast />
    <div
      id="row-1"
      class="card w-[80%] mt-10 shadow-md flex justify-center items-center py-10 bg-white"
    >
      <i class="pi pi-book text-3xl text-primary-500 mr-5"></i>
      <p class="font-abel text-3xl text-primary-500 font-bold">CATALOG</p>
    </div>

    <div class="card w-[80%] h-full shadow-md my-5 flex flex-col overflow-hidden">
      <Tabs value="0" class="flex-1 flex flex-col" lazy select-on-focus>
        <TabList class="bg-none">
          <Tab value="0">All Collections</Tab>
          <Tab value="1">My Collections</Tab>
          <!-- <Tab value="2">All Files</Tab> -->
        </TabList>
        <TabPanels class="flex-1">
          <TabPanel value="0" class="h-full flex flex-col justify-center items-center">
            <div class="w-[90%] h-full">
              <CollectionsTable viewmode="all" />
            </div>
          </TabPanel>
          <TabPanel value="1" class="h-full flex flex-col justify-center items-center">
            <div class="w-[90%] h-full">
              <CollectionsTable viewmode="my" />
            </div>
          </TabPanel>
          <TabPanel
            value="2"
            class="h-full flex-1 flex justify-center items-center overflow-hidden"
          >
            <!-- <div class="w-[90%] h-full">
              <FilesTable />
            </div> -->
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
  </div>
</template>
